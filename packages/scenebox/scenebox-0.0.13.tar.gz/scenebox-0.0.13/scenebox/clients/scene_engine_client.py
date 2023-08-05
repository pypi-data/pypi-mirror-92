#  Copyright (c) 2020 Caliber Data Labs.
#  All rights reserved.
#
import io
import json
import os
import pickle
import re
import threading
import time
from collections import OrderedDict
from datetime import datetime
from os.path import join
from typing import List, Optional, Tuple, Union

import requests
from deprecated import deprecated

from ..clients.job_manager_client import wait_for_jobs
from ..constants import (AnnotationMediaTypes, AssetsConstants, ConfigTypes,
                         EntityInfluenceTypes, EntityTypes, SetsAssets)
from ..custom_exceptions import (AssetError, IndexingException,
                                 InvalidAssetType, InvalidSetIdentifier,
                                 InvalidTimeError, ResponseError, SetsError)
from ..models.annotation import Annotation
from ..tools.logger import get_logger
from ..tools.misc import chunk_list, decorate_all_inherited_methods, get_guid
from ..tools.time_utils import datetime_or_str_to_iso_utc
from .asset_manager_client import AssetManagerClient

DEFAULT_MAX_ASSETS = 250
VERSION_POSTFIX = "v1"

logger = get_logger(__name__)


def no_set_provided_error():
    raise ValueError(
        "No set_id provided and no default set_id exists. Either provide or set with _use_set(<set_id>)")


def no_asset_provided_error():
    raise ValueError(
        "No asset_type provided and no default asset_type exists. Either provide or set with _set_asset_state("
        "<asset_type>, <metadata:only>)")


def invalid_set_asset_error(asset_type):
    raise ValueError(
        "The asset_type {} is not a valid set asset type. Valid set assets are: {}".format(
            asset_type, SetsAssets.VALID_ASSET_TYPES))


def before_method(f):
    """Decorator to be run before methods are called."""

    def wrapper(*args, **kwargs):
        self = args[0]
        if not self.asset_type:
            raise InvalidAssetType(
                "No asset type provided. Please call the `with_asset_state()` method to update.")
        return f(*args, **kwargs)

    return wrapper


@decorate_all_inherited_methods(before_method)
class SceneEngineClient(AssetManagerClient):
    """Utility class for interacting with the SceneEngine programmatically.

    This class is intended to be used directly by the client
    Usage:
        - Interact with assets by setting:
            - asset_type
            - metadata_only
        - Special utility methods for interacting with sets and projects
            - Search for sets/projects
            - Search media within a set/project
            - Zip a set
            - Download all media within a set
    """

    def __init__(
            self,
            scene_engine_url: str,
            auth_token: Optional[str] = None,
            asset_manager_url: Optional[str] = None,
            artifacts_path: Optional[str] = None,
    ):
        self.scene_engine_url = scene_engine_url
        self._fix_scene_engine_url()
        self.set_id = None
        self.project_id = None
        self.requests = SceneEngineRequestHandler(
            self.scene_engine_url, auth_token)

        asset_manager_url_ = asset_manager_url or self._get_asset_manager_url()
        super().__init__(
            asset_type=None,
            asset_manager_url=asset_manager_url_,
            auth_token=auth_token,
        )
        self.artifacts_path = artifacts_path or self.cache_location

    def _fix_scene_engine_url(self):
        if not self.scene_engine_url:
            return
        if self.scene_engine_url.endswith("/{}".format(VERSION_POSTFIX)):
            pass
        elif self.scene_engine_url.endswith("/{}/".format(VERSION_POSTFIX)):
            self.scene_engine_url = self.scene_engine_url[:-1]
        elif self.scene_engine_url.endswith("/"):
            self.scene_engine_url += VERSION_POSTFIX
        else:
            self.scene_engine_url += "/{}".format(VERSION_POSTFIX)

    def _get_asset_manager_url(self) -> str:
        resp = self.requests.get("status", remove_version=True)
        resp.raise_for_status()

        version = resp.json().get("asset_manager_url")
        if version is None:
            ValueError("cannot get asset_manager_url")
        return version

    def with_auth(self,
                  auth_token: Optional[str] = None,
                  ):
        if auth_token:
            self.auth_token = auth_token

        # Need to also call with_auth of AssetManagerClient in order
        # to update the asset cache
        super().with_auth(auth_token)

        self.requests.with_auth(
            auth_token=auth_token)

        return self

    def get_version(self) -> str:
        """
        get the version of the SceneBox platform
        :return: version number
        """
        resp = self.requests.get("status", remove_version=True)
        resp.raise_for_status()

        version = resp.json().get("version")
        if version is None:
            ValueError("cannot get version")

        return version

    def get_state(self) -> str:
        """
        get the state of the SceneBox platform
        :return: state
        """
        resp = self.requests.get("status", remove_version=True)
        resp.raise_for_status()

        state = resp.json().get("state")
        if state is None:
            ValueError("cannot get version")

        return state

    def update_state(self, desired_state: str) -> bool:
        """update the state of the SceneBox platform."""
        options = {
            "state": desired_state
        }
        resp = self.requests.post("status", json=options, remove_version=True)
        resp.raise_for_status()

        return True

    def update_artifact_path(self, artifacts_path):
        self.artifacts_path = artifacts_path

    @deprecated("use create_project instead")
    def create_annotation_project(
            self,
            project_id,
            name,
            description,
            labelling_requirements,
            provider,
            client_id=None,
            provider_auth_token=None,
            wait_for_completion=True):
        options = {
            "name": name,
            "description": description,
            "labelling_requirements": labelling_requirements
        }
        headers = {
            "client_id": client_id,
            "auth_token": provider_auth_token
        }
        params = self.with_asset_state(
            AssetsConstants.ANNOTATION_PROJECTS_ASSET_ID,
            True) .add_asset_manager_params(
            {
                "provider": provider})
        resp = self.requests.post(
            "annotation_projects/add/{}".format(project_id),
            trailing_slash=False,
            params=params,
            headers=headers,
            json=options)
        if not resp.ok:
            raise ResponseError(
                "Could not create the annotation project: {}".format(
                    resp.content))
        identifier = resp.json()["id"]
        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)
        return identifier

    def create_project(
            self,
            name: str,
            description: Optional[str] = None) -> str:
        options = {
            "name": name,
            "description": description
        }
        resp = self.requests.post(
            "projects/add/",
            trailing_slash=True,
            json=options)
        if not resp.ok:
            raise ResponseError(
                "Could not create the project: {}".format(
                    resp.content))

        identifier = resp.json()["id"]
        return identifier

    def delete_project(
            self,
            project_id: str):
        resp = self.requests.delete(
            "projects/meta/{}".format(project_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not delete the project: {}".format(
                    resp.content))

    def create_operation(self,
                         name: str,
                         operation_type: str,
                         project_id: str,
                         config: dict,
                         stage: int = 0,
                         description: Optional[str] = None) -> str:
        options = {
            "name": name,
            "type": operation_type,
            "stage": stage,
            "project_id": project_id,
            "config": config,
            "description": description
        }

        resp = self.requests.post(
            "operations/add/",
            trailing_slash=True,
            json=options)
        if not resp.ok:
            raise ResponseError(
                "Could not create the operation: {}".format(
                    resp.content))

        identifier = resp.json()["id"]
        return identifier

    def delete_operation(self, operation_id: str):

        resp = self.requests.delete(
            "operations/{}".format(operation_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not delete the operation: {}".format(
                    resp.content))

    def start_operation(
            self,
            operation_id: str,
            wait_for_completion: bool = False) -> str:

        resp = self.requests.put(
            "operations/control/{}".format(operation_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not delete the operation: {}".format(
                    resp.content))

        job_id = resp.json().get("job_id")

        if wait_for_completion:
            self._wait_for_job_completion(job_id)

        return job_id

    def get_operation_status(self, operation_id: str) -> dict:
        resp = self.requests.get("operations/{}/status/".format(operation_id))
        resp.raise_for_status()
        return resp.json()

    def add_sets_to_project(
            self,
            project_id: str,
            sets: List[str],
            stage: int = 0):
        options = {
            "sets": sets,
            "stage": stage,
        }

        resp = self.requests.post(
            "projects/{}/add_sets/".format(project_id),
            trailing_slash=True,
            json=options)
        resp.raise_for_status()

    def remove_sets_from_project(
            self,
            project_id: str,
            sets: List[str],
            stage: int = 0):
        options = {
            "sets": sets,
            "stage": stage,
        }

        resp = self.requests.post(
            "projects/{}/remove_sets/".format(project_id),
            trailing_slash=True,
            json=options)
        resp.raise_for_status()

    def create_set(
            self,
            name: str,
            asset_type: str,
            origin: Optional[str] = None,
            description: Optional[str] = None,
            expected_count: Optional[int] = None,
            tags: Optional[List[str]] = None,
            raise_if_set_exists=False,
    ) -> str:
        """Create a set."""
        same_name_sets = self.with_asset_state(
            asset_type=AssetsConstants.SETS_ASSET_ID,
            metadata_only=True).search_assets(
            query={
                "filters": [
                    {
                        "field": "name",
                        "values": [name]}]})

        if same_name_sets:
            if raise_if_set_exists:
                raise SetsError("set name {} already exists".format(name))
            else:
                return same_name_sets[0]

        options = {
            "assets_type": asset_type,
            "name": name,
            "description": description,
            "origin": origin,
            "expected_count": expected_count,
            "tags": tags or []
        }
        resp = self.requests.post(
            "sets/add/",
            trailing_slash=True,
            json=options)

        if not resp.ok:
            raise ResponseError(
                "Could not create the set: {}".format(
                    resp.content))

        identifier = resp.json()["id"]
        return identifier

    def create_annotation_instruction(
            self,
            name: str,
            key: str,
            annotator: str,
            annotation_type: str,
            payload: dict,
            media_type: str = AnnotationMediaTypes.IMAGE,
            description: Optional[str] = None) -> str:
        """Create an annotation_instruction."""
        options = {
            "name": name,
            "key": key,
            "annotator": annotator,
            "type": ConfigTypes.ANNOTATION_INSTRUCTION,
            "annotation_type": annotation_type,
            "config": payload,
            "media_type": media_type,
            "description": description,
        }
        resp = self.requests.post(
            "configs/add/",
            trailing_slash=True,
            json=options)

        if not resp.ok:
            raise ResponseError(
                "Could not create the annotation_instruction: {}".format(
                    resp.content))

        identifier = resp.json()["id"]
        return identifier

    def delete_annotation_instruction(self, annotation_instruction_id: str):

        resp = self.requests.delete(
            "configs/meta/{}".format(annotation_instruction_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not delete the annotation_instruction: {}".format(
                    resp.content))

    def create_config(
            self,
            name: str,
            type: str,
            config: dict,
            description: Optional[str] = None,
            **kwarg) -> str:
        """Create a config."""
        options = kwarg
        options.update({
            "name": name,
            "type": type,
            "config": config,
            "description": description,
        })
        resp = self.requests.post(
            "configs/add/",
            trailing_slash=True,
            json=options)

        if not resp.ok:
            raise ResponseError(
                "Could not create the config: {}".format(
                    resp.content))

        identifier = resp.json()["id"]
        return identifier

    def delete_config(self, config_id: str):

        resp = self.requests.delete(
            "configs/meta/{}".format(config_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not delete the config_id: {}".format(
                    resp.content))

    def get_config(self, config_id: str, complete_info=False) -> dict:

        resp = self.requests.get(
            "configs/meta/{}".format(config_id),
            trailing_slash=False)
        if not resp.ok:
            raise ResponseError(
                "Could not delete the config_id: {}".format(
                    resp.content))

        if complete_info:
            return resp.json()
        else:
            return resp.json().get("config", {})

    def set_lock(self, set_id: str) -> bool:
        resp = self.requests.put("sets/{}/lock".format(set_id))
        resp.raise_for_status()

        return True

    def set_unlock(self, set_id: str) -> bool:
        resp = self.requests.delete("sets/{}/lock".format(set_id))
        resp.raise_for_status()

        return True

    def set_is_locked(self, set_id: str) -> bool:
        resp = self.requests.get("sets/{}/lock".format(set_id))
        resp.raise_for_status()

        return resp.json().get("locked")

    def delete_set(
            self,
            set_id: str = None,
            wait_for_completion: bool = False) -> str:
        """Delete a set."""
        if not set_id and not self.set_id:
            no_set_provided_error()
        set_id = set_id or self.set_id
        resp = self.requests.delete("sets/{}".format(set_id))
        resp.raise_for_status()
        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)
        return resp.json().get("job_id")

    def get_set_status(self, set_id: str = None) -> dict:
        if not set_id and not self.set_id:
            no_set_provided_error()
        resp = self.requests.get("sets/{}/status/".format(set_id))
        resp.raise_for_status()
        return resp.json()

    def add_assets_to_set(
            self,
            query: dict = None,
            ids: list = None,
            set_id: str = None,
            wait_for_availability: bool = True,
            timeout: int = 30,
            wait_for_completion=False,
    ) -> str:
        """Add assets to a set either by query or by ids."""
        if not set_id and not self.set_id:
            no_set_provided_error()

        set_id = set_id or self.set_id
        if not set_id:
            raise ValueError("No default set available")

        if query is None and ids is None:
            raise ValueError(
                "Either a search query or a list of ids must be provided")

        if self.set_is_locked(set_id):
            if wait_for_availability:
                t_start = time.time()
                while True:
                    time.sleep(1)
                    if time.time() - t_start > timeout:
                        raise TimeoutError(
                            "Timeout waiting for set {} to unlock".format(set_id))
                    if not self.set_is_locked(set_id):
                        logger.info(
                            "Set {} is locked, waiting 1s to add assets".format(set_id))
                        break
            else:
                raise SetsError("Set {} is locked".format(set_id))

        if query:
            resp = self.requests.post(
                "sets/{}/add_assets_query/".format(set_id),
                trailing_slash=True,
                json=query)
        else:
            assets_payload = {"asset_list": ids}
            resp = self.requests.post(
                "sets/{}/add_assets_list/".format(set_id),
                trailing_slash=True,
                json=assets_payload)

        if not resp.ok:
            raise ResponseError(
                "Could not add assets to set: {}, {}".format(
                    resp.content, resp.reason))

        if wait_for_completion:
            job_id = resp.json()["job_id"]
            self._wait_for_job_completion(job_id)

        return resp.json().get("job_id")

    def assets_in_set(self, set_id: Optional[str] = None) -> List[str]:
        """List assets within a set."""
        return self.search_within_set(set_id=set_id, show_meta=False)

    def search_within_set(
            self,
            query: Optional[dict] = None,
            set_id: Optional[str] = None,
            show_meta: bool = True) -> List:
        """Search for assets within a set."""
        query = self._validate_query(query)
        if not set_id and not self.set_id:
            no_set_provided_error()

        set_id = set_id or self.set_id
        if show_meta:
            resp = self.requests.post(
                "sets/{}/list_assets_meta/".format(set_id),
                trailing_slash=True,
                json=query)
        else:
            resp = self.requests.post(
                "sets/{}/list_assets/".format(set_id),
                trailing_slash=True,
                json=query)

        if not resp.ok:
            raise ResponseError(
                "Could not perform the search: {}".format(
                    resp.content))

        return resp.json()["results"]

    def search_over_sets(self, query=None, show_meta=True):
        """Search over available sets with a query."""
        query = self._validate_query(query)
        if show_meta:
            return self.with_asset_state("sets", True).search_meta(query)
        else:
            return self.with_asset_state("sets", True).search_assets(query)

    def zip_set(self, set_id: Optional[str] = None) -> [str, str]:
        """Create a zipfile of the set."""
        if not set_id and not self.set_id:
            no_set_provided_error()
        set_id = set_id or self.set_id
        resp = self.requests.get(
            "sets/{}/zip_all_assets/".format(set_id),
            trailing_slash=True)
        resp.raise_for_status()
        return resp.json().get("job_id"), resp.json().get("filename")

    def download_zipfile(self,
                         zip_filename: str,
                         output_filename: Optional[str] = None) -> Union[str,
                                                                         io.BytesIO]:
        """Download a zipfile into either a bytesIO object or a file."""
        data_bytes = self.with_asset_state(
            "zipfiles", False).get_file(zip_filename)
        if output_filename:
            if not output_filename.endswith(".zip"):
                output_filename += ".zip"
            fpath = join(self.artifacts_path, output_filename)
            with open(fpath, "wb") as f:
                f.write(data_bytes)
            return fpath
        else:
            bytes_file = io.BytesIO(data_bytes)
            return bytes_file

    def zip_set_and_download(self,
                             set_id: Optional[str] = None,
                             filename: Optional[str] = None) -> Union[str,
                                                                      io.BytesIO]:
        job_id, zip_filename = self.zip_set(set_id)
        self._wait_for_job_completion(job_id)
        return self.download_zipfile(zip_filename, output_filename=filename)

    def with_asset_state(
            self,
            asset_type: str,
            metadata_only: bool = False
    ):
        """Set the asset state, for use in chaining.

        Eg. client.with_asset_state("images", True).search_files({})
        """
        return self._set_asset_state(
            asset_type=asset_type,
            metadata_only=metadata_only,
        )

    def register_rosbag_session(
            self,
            session_name: str,
            session_directory_path: Optional[str] = None,
            rosbag_ids: Optional[List[str]] = None,
            config_name: Optional[str] = None,
            wait_for_completion: bool = True,
    ) -> Tuple[str, str]:
        """Register a rosbag session with the scene engine.

        Args:
            session_name (str): Name of the session
            session_directory_path (str): Local path (on ros-extractor) to a session directory
            rosbag_ids (list): List of rosbag IDs belonging to the session
            config_name (str): Name of the session configuration file
            wait_for_completion: should we wait till completion
        """
        if session_directory_path is None and rosbag_ids is None:
            # Insufficient arguments provided
            raise ValueError(
                "Must provide either session_directory_path or rosbag_ids")

        json_payload = {
            'session_name': session_name,
            'session_directory_path': session_directory_path,
            'source_data': rosbag_ids,
            'session_configuration': config_name,
        }

        resp = self.requests.post(
            "indexing/register_rosbag_session/",
            trailing_slash=True,
            json=json_payload)

        job_id = resp.json()["job_id"]

        if wait_for_completion:
            self._wait_for_job_completion(job_id)

        session_uid = resp.json()["session_uid"]

        return job_id, session_uid

    def get_session_resolution_status(self, session_uid: str) -> str:
        """Get the status of the session resolution task (if it exists)"""
        resp = self.requests.get(
            "session_manager/resolution_status/{}".format(session_uid),
            trailing_slash=False
        )
        return resp.json()['status']

    def submit_rosbag_indexing_request(
            self,
            session_uid: str,
            session_directory_path: Optional[str] = None,
            rosbag_ids: Optional[List[str]] = None,
            config_name: Optional[str] = None,
            extraction_sensors: Optional[List[dict]] = None,
            extraction_types: Optional[List[dict]] = None,
            extraction_settings: Optional[dict] = None,
            re_resolve: bool = False,
    ) -> str:
        """Submit indexing requests to the scene-engine.

        Args:
            session_uid (str): UID of the session
            session_directory_path (str): Local path (on ros-extractor) to a session directory
            rosbag_ids (list): List of rosbag IDs belonging to the session
            config_name (str): Name of the session configuration file
            extraction_sensors (dict): List of sensor extractions of form:
                {
                    "sensor_name": <sensor name>,
                    "extraction_settings": <dict of extraction settings>,
                    "extraction_types": <list of applicable extraction types>
                }
            extraction_types (list): List of type extractions of form:
                {
                    "extraction_type": <Type of extraction>,
                    "extraction_settings": <Extraction settings for this type>
                }
            extraction_settings (dict): Fallback extraction settings
            wait_for_completion: should we wait till completion
        """
        if session_directory_path is None and rosbag_ids is None:
            # Insufficient arguments provided
            raise ValueError(
                "Must provide either session_directory_path or rosbag_ids")

        if extraction_types is None and extraction_sensors is None:
            raise ValueError(
                "Must provide one of extraction_types or extraction_sensors")

        json_payload = {
            'session_uid': session_uid,
            'session_directory_path': session_directory_path,
            'source_data': rosbag_ids,
            'session_configuration': config_name,
            'extraction_config': {
                'extraction_sensors': extraction_sensors or [],
                'extraction_types': extraction_types or [],
                'extraction_settings': extraction_settings or {},
            },
            're_resolve': re_resolve
        }

        return self.requests.post(
            "indexing/index_rosbag_session/",
            trailing_slash=True,
            json=json_payload)

    def submit_video_indexing_request(
            self,
            session_name: str,
            video_session_data: Optional[dict] = None,
            video_filenames: Optional[List[str]] = None,
            raw_videos: Optional[dict] = None,
            session_formatting_strategy: Optional[str] = None,
            extraction_config: Optional[dict] = None,
            session_resolution: float = 1.0,
            wait_for_completion: bool = True,
            retry: Optional[bool] = False,
            enrichments:Optional[List[dict]]= None,
            session_uid: Optional[str] = None

    ) -> dict:

        resp = self.requests.post(
            "indexing/index_video_session/",
            trailing_slash=True,
            json={
                'session_name': session_name,
                'video_session_data': video_session_data or [],
                'raw_videos': raw_videos or {},
                'extraction_config': extraction_config or {},
                'session_resolution': session_resolution,
                'video_filenames': video_filenames,
                'session_formatting_strategy': session_formatting_strategy,
                'retry': retry,
                'enrichments':enrichments,
                'session_uid': session_uid,
            }
        )

        airflow_job_info = resp.json()
        session_uid = resp.json()["session_uid"]

        if not resp.ok:
            raise IndexingException(
                "Failed to index video session: {} -- {}".format(resp.reason, resp.content))

        if wait_for_completion:
            successful_jobs = 0
            failed_jobs = 0

            for job_map_key in [
                'compression_job_map',
                'image_extraction_job_map',
                "concatenation_job_map",
            ]:
                jobs_ids = list(airflow_job_info[job_map_key].values())
                t1 = time.time()
                job_info = wait_for_jobs(
                    job_ids=jobs_ids,
                    asset_manager_url=self.asset_manager_url,
                    auth_token=self.auth_token,
                    timeout=None,
                    raise_on_error=True)
                logger.info(
                    "JOB {} finished in {} seconds".format(
                        job_map_key, round(
                            time.time() - t1), 2))
                successful_jobs += job_info['successful']
                failed_jobs += job_info['failed']

            return {
                "successful": successful_jobs,
                "failed_jobs": failed_jobs,
                "session_uid": session_uid
            }
        else:
            return airflow_job_info

    def extract_video_images_and_compress(
            self, video_id: str, session_name: str):
        resp = self.requests.post(
            'videos/extract_and_compress_video/',
            json={
                'video_id': video_id,
                'session_name': session_name
            },
            trailing_slash=True
        )
        return resp.json()

    def submit_hls_indexing_request(
            self,
            session_name: str,
            session_directory_path: Optional[str] = None,
            hls_ids: Optional[List[str]] = None,
            config_name: Optional[str] = None,
            extraction_sensors: Optional[List[dict]] = None,
            extraction_types: Optional[List[dict]] = None,
            extraction_settings: Optional[dict] = None,
    ):
        # TODO have a separate client for HLS related methods
        """Submit indexing requests to the scene-engine.

        Args:
            session_name (str): Name of the session
            session_directory_path (str): Local path to a session directory
            hls_ids (list): List of hls IDs belonging to the session
            config_name (str): Name of the session configuration file
            extraction_sensors (dict): List of sensor extractions of form:
                {
                    "sensor_name": <sensor name>,
                    "extraction_settings": <dict of extraction settings>,
                    "extraction_types": <list of applicable extraction types>
                }
            extraction_types (list): List of type extractions of form:
                {
                    "extraction_type": <Type of extraction>,
                    "extraction_settings": <Extraction settings for this type>
                }
            extraction_settings (dict): Fallback extraction settings
        """

        if session_directory_path is None and hls_ids is None:
            # Insufficient arguments provided
            raise ValueError(
                "Must provide either session_directory_path or hls_ids")

        if extraction_types is None and extraction_sensors is None:
            raise ValueError(
                "Must provide one of extraction_types or extraction_sensors")

        json_payload = {
            'session_name': session_name,
            'session_directory_path': session_directory_path,
            'source_data': hls_ids,
            'session_configuration': config_name,
            'extraction_config': {
                'extraction_sensors': extraction_sensors or [],
                'extraction_types': extraction_types or [],
                'extraction_settings': extraction_settings or {},
            }
        }

        resp = self.requests.post(
            "indexing/index_hls_session/",
            trailing_slash=True,
            json=json_payload)
        return resp.json()

    def submit_add_cdl_request(
            self,
            session_uid: str,
            cdl_id: str,
            session_directory_path: Optional[str] = None,
    ):
        # TODO have a separate client for HLS related methods
        """Submit ingestion request to the scene-engine.

        Args:
            session_uid (str): UID of the session
            cdl_id (str): single cdl ID per session
            session_directory_path (str): Local path to cdl directory
        """
        json_payload = {
            'session_uid': session_uid,
            'session_directory_path': session_directory_path,
            'source_data': [cdl_id],
        }
        logger.info("sec: cdl_id {}".format(cdl_id))
        resp = self.requests.post(
            "indexing/add_cdl/",
            trailing_slash=True,
            json=json_payload)
        return resp.json()

    def get_indexing_job_components(self, indexing_job_task_id):
        resp = self.requests.get(
            "indexing/job_components/{}".format(indexing_job_task_id),
            trailing_slash=False
        )
        return resp.json()

    def wait_for_labelling_project(
            self,
            annotation_project_id,
            total,
            n_stop=None,
            timeout=None):
        """Wait for a labelling project to finish (i.e. for all assets to be
        labelled)

        n_stop (int/None): Only wait for this many assets to be labelled
        (for demo purposes)
        """
        # TODO: This should use the JOBs API to check for progress, however this only works for inference labelling
        # TODO: Replace session_filenames with annotation_project_id

        if not n_stop:
            n_stop = total
        else:
            n_stop = min(n_stop, total)

        annotation_project_assets = self.get_annotation_project_assets(
            annotation_project_id)
        all_annotation_filenames = self.get_asset_annotation_files(
            annotation_project_assets)

        annotation_filenames = []
        t_start = time.time()
        while True:
            for identifier in all_annotation_filenames:
                if self.with_asset_state(
                        AssetsConstants.ANNOTATIONS_ASSET_ID,
                        metadata_only=True).exists(identifier):
                    annotation_filenames.append(identifier)
            if len(annotation_filenames) >= n_stop:
                break

            time.sleep(1)

            if timeout and (time.time() - t_start > timeout):
                logger.info(
                    "wait_for_labelling_project:: Timeout after {} s".format(timeout))
                break

        return annotation_filenames

    def put_session_assets_into_project(
            self,
            session_search_query,
            asset_type=AssetsConstants.IMAGES_ASSET_ID,
            max_training_assets=None,
            max_sessions=None):
        """Create sets from each session satisfying the session_search_query,
        where sets are populated with the given asset type.

        Note: This method is intended primarily for DEMO purposes

        :param session_search_query: (dict) Search query matching sessions
        :param asset_type: (str) The asset type to add
        :param max_training_assets: (int) The maximum number of assets to consider
        :return: Dict containing:
        {
            "project_id": project_id,
            "set_id_to_session_name": set_id_to_session_name,
            "set_id_to_asset_ids": set_id_to_asset_ids,
            "total_assets": len(all_training_image_filenames)
        }
        """

        if asset_type != AssetsConstants.IMAGES_ASSET_ID:
            raise ValueError("only image assets are implemented")

        if not max_training_assets:
            max_training_assets = DEFAULT_MAX_ASSETS
        session_filenames = self.get_indexed_session_filenames(
            session_search_query)

        if max_sessions is None:
            max_sessions = len(session_filenames)
        else:
            session_filenames = session_filenames[0:max_sessions]
        # Get images corresponding to these sessions & add images to a set
        set_id_to_session_name = {}
        all_training_image_filenames = []
        set_id_to_asset_ids = {}
        for session_name in session_filenames:
            # Get the images from the session
            session_images = self.with_asset_state("images", metadata_only=True).search_assets(
                {"search_text": "filename: ~{}".format(session_name)},
                size=int(max_training_assets / max_sessions)
            )
            logger.info(
                "Extracted {} assets from session {}".format(
                    len(session_images), session_name))

            # Create a new set
            set_name = self.experiment_name + "_" + session_name + "_images"
            set_description = (
                "A collection of images for the experiment " +
                self.experiment_name)
            set_id = self.create_set(
                name=set_name,
                asset_type=asset_type,
                description=set_description,
            )
            set_id_to_asset_ids[set_id] = session_images
            logger.info("Created set: {}".format(set_id))
            # Add the session-images to the set
            self.add_assets_to_set(
                ids=session_images,
                set_id=set_id,
                wait_for_completion=True)
            # Keep track of the set_id for each session
            set_id_to_session_name[set_id] = session_name
            all_training_image_filenames.extend(session_images)
        logger.info(
            "Training dataset has {} images from {} sessions".format(
                len(all_training_image_filenames),
                max_sessions))
        # Sleep for a time to allow all training assets to add
        # TODO: Currently there's no good way to wait for assets to be added to
        # sets/projects
        logger.info("Adding assets to a project")
        # Create a new project and add the sets to a project
        project_name = self.experiment_name + "_project"
        project_description = "A project for the experiment " + self.experiment_name
        project_id = self.create_project(
            name=project_name,
            description=project_description,
        )
        logger.info("Created project: {}".format(project_id))
        set_ids = list(set_id_to_session_name.keys())
        self.add_assets_to_project(
            ids=set_ids,
            project_id=project_id,
            wait_for_completion=True)
        logger.info("Project ID is::: {}".format(project_id))
        # TODO: Currently there's no good way to wait for assets to be added to
        # sets/projects
        return {
            "project_id": project_id,
            "set_id_to_session_name": set_id_to_session_name,
            "set_id_to_asset_ids": set_id_to_asset_ids,
            "total_assets": len(all_training_image_filenames)
        }

    def get_annotation_project_assets(self, annotation_project_id):
        annotation_project_state = self.with_asset_state(
            AssetsConstants.ANNOTATION_PROJECTS_ASSET_ID,
            True).get_metadata(annotation_project_id)["state"]
        annotation_project_files = []
        for set_id, set_files in json.loads(annotation_project_state).items():
            annotation_project_files.extend(set_files)
        return annotation_project_files

    def get_asset_annotation_files(self, assets_list):
        # TODO: It's not currently possible to have more than on annotation for the same asset, and needs to be fixed
        # TODO: Handle cases other than images
        annotation_filenames = [i.replace(".png", ".ann") for i in assets_list]
        return annotation_filenames

    def get_annotations_from_binary(self, annotation_filenames):
        """
        :param annotation_filenames: IDs of the annotation
        :return: (dict) Annotation json corresponding get_annotation_binary the annotation ID
        """
        annotation_binaries = []
        failed_filenames = []

        # Create a new instance of SceneEngineClient for fetching data
        # This is since fetching is done in threads, and we update the state of the
        # object with `with_asset_state`
        sec = SceneEngineClient(
            auth_token=self.auth_token,
            scene_engine_url=self.scene_engine_url,
            asset_manager_url=self.asset_manager_url,
        )

        for annotation_filename in annotation_filenames:
            # Get the metadata
            sec = sec.with_asset_state(
                AssetsConstants.ANNOTATIONS_ASSET_ID, True)
            try:
                annotation_binary_id = sec.get_metadata(
                    annotation_filename).get("binary_id")
            except AssetError:
                failed_filenames.append(annotation_filename)
                logger.error(
                    "Failed to fetch annotation file {}".format(annotation_filename))
                continue

            annotation_file_binary = sec.with_asset_state(
                "annotations", False).get_file(annotation_binary_id)
            annotation_file = pickle.loads(annotation_file_binary)[0]
            annotation_binaries.append({
                "filename": annotation_filename,
                "payload": annotation_file
            })
        return failed_filenames, annotation_binaries

    def get_annotations_from_binary_async(
            self, annotation_filenames, num_threads=10):
        """Fetch annotation binaries from storage asynchronously."""
        fetched_annotation_data = []
        annotation_filename_set = set(annotation_filenames)
        failed_files = set()

        def _get_annotations_from_binary(filenames):
            failed_filenames, successfully_fetched_data = self.get_annotations_from_binary(
                filenames)
            fetched_annotation_data.extend(successfully_fetched_data)
            [failed_files.add(f) for f in failed_filenames]

        def _wait_for_data():
            # Wait for threads to complete
            n_waiting_for = len(annotation_filename_set.difference(
                failed_files)) - len(fetched_annotation_data)
            while n_waiting_for:
                time.sleep(2)
                logger.info(
                    "Waiting for {} annotations to load from storage".format(
                        n_waiting_for)
                )
                n_waiting_for = len(annotation_filename_set.difference(
                    failed_files)) - len(fetched_annotation_data)

        # Schedule threads
        chunk_size = int(len(fetched_annotation_data) / num_threads + 1)
        chunked_annotation_filenames = chunk_list(
            annotation_filenames, chunk_size)
        for annotation_filenames_chunk in chunked_annotation_filenames:
            t = threading.Thread(
                target=_get_annotations_from_binary,
                args=(annotation_filenames_chunk,),
            )
            t.start()

        _wait_for_data()

        # Order the received annotations in the same way as the filenames
        ordered_annotation_jsons = OrderedDict().fromkeys(
            [i for i in annotation_filenames if i not in failed_files])
        for data in fetched_annotation_data:
            ordered_annotation_jsons[data["filename"]] = data["payload"]

        logger.info(
            "{} training assets failed to fetch".format(
                len(failed_files)))
        return list(ordered_annotation_jsons.values())

    def get_searchable_field_statistics(self):
        return self.requests.get(
            route=os.path.join(
                self.asset_type,
                'meta',
                'searchable_field_statistics'),
            trailing_slash=True).json()

    def get_image_meta(self, image_filename):
        image_metadata = self.with_asset_state(
            AssetsConstants.IMAGES_ASSET_ID,
            False).get_metadata(image_filename)
        return image_metadata

    def get_metadata(
            self,
            identifier: str,
            with_session_metadata: bool = False):
        if with_session_metadata is False:
            return super().get_metadata(identifier)
        else:
            resp = self.requests.get(
                route=os.path.join(
                    self.asset_type,
                    'meta',
                    identifier),
                trailing_slash=False,
                params={'with_session_metadata': True}
            )
            if not resp.ok:
                raise ResponseError(
                    "{} ::: {} with token::: {}".format(
                        resp.reason, resp.content, self.auth_token))
            return resp.json()

    def compress_images(self,
                        image_ids: List[str],
                        image_format: str,
                        desired_shape: Optional[Tuple[int,
                                                      ...]] = None,
                        thumbnail_tag: Optional[str] = None,
                        use_preset: Optional[str] = None):
        resp = self.requests.post(
            "images/compress_images/",
            trailing_slash=True,
            json={
                "image_ids": image_ids,
                "desired_shape": desired_shape,  # h x w x ..
                "image_format": image_format,
                "thumbnail_tag": thumbnail_tag,
                "use_preset": use_preset,
            }
        )

        return resp.json()

    def compress_videos(self,
                        video_ids: List[str],
                        desired_shape: Optional[Tuple[int,
                                                      ...]] = None,
                        thumbnail_tag: Optional[str] = None,
                        use_preset: Optional[str] = None,
                        job_id: Optional[str] = None
                        ):
        resp = self.requests.post(
            "videos/compress_videos/",
            trailing_slash=True,
            json={
                "video_ids": video_ids,
                "desired_shape": desired_shape,  # h x w x ..
                "thumbnail_tag": thumbnail_tag,
                "use_preset": use_preset,
                "job_id": job_id
            }
        )

        return resp.json()

    def concatenate_videos(
            self,
            video_ids: List[str],
            output_video_id: str,
            video_metadata: dict,
            job_id: Optional[str] = None):
        resp = self.requests.post(
            "videos/concatenate_videos/",
            trailing_slash=True,
            json={
                "video_ids": video_ids,
                "output_video_id": output_video_id,
                "video_metadata": video_metadata,
                "job_id": job_id
            }
        )

        return resp.json()

    def put_annotation(self,
                       annotation: Annotation,
                       raw_annotation: str):
        if not annotation.id.endswith(".ann"):
            annotation.id += ".ann"

        metadata = annotation.to_dic()

        self.with_asset_state(
            asset_type=AssetsConstants.ANNOTATIONS_ASSET_ID).put_metadata(
            identifier=annotation.id, metadata=metadata)
        self.with_asset_state(
            asset_type=AssetsConstants.ANNOTATIONS_ASSET_ID).put_string(
            content_str=raw_annotation,
            identifier=annotation.id)

    def get_standardized_session_name(self, session_name: str):
        resp = self.requests.post(
            "sessions/standardize_name/",
            trailing_slash=True,
            json={
                'session_name': session_name})

        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))
        return resp.json()['session_name']

    def get_indexed_session_filenames(self, search_query):
        # Get all the indexed sessions
        indexed_sessions = self.with_asset_state(
            AssetsConstants.SESSIONS_ASSET_ID,
            metadata_only=True).search_assets(search_query)
        return indexed_sessions

    def _get_asset_response_model(self, asset_type: str):
        if asset_type not in AssetsConstants.VALID_ASSETS:
            raise ValueError("Invalid asset type {}".format(asset_type))
        return self.requests.get(
            route=os.path.join(asset_type, 'meta', 'response_model'),
            trailing_slash=True
        ).json()

    def _use_set(self, set_id):
        """Set the default set id."""
        previous_asset, previous_metadata = self.asset_type, self.metadata_only
        if not self.with_asset_state("sets", True).exists(set_id):
            raise InvalidSetIdentifier(
                "The set_id {} does not exist".format(set_id))
        self.set_id = set_id
        self.asset_type, self.metadata_only = previous_asset, previous_metadata

    def add_session(self, session_name: str, session_type: str) -> str:
        resp = self.requests.post(
            "sessions/add/",
            trailing_slash=True,
            json={"session_name": session_name, "session_type": session_type})
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))
        return resp.json().get("session_uid")

    def add_entity(self, entity_dict: dict) -> dict:
        resp = self.requests.post(
            "session_manager/add_entity/",
            trailing_slash=True,
            json={"entity_dict": entity_dict})
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))
        return resp.json()

    def resolve_session(self, session_uid: str) -> dict:
        resp = self.requests.post(
            "session_manager/resolve_session/{}".format(session_uid))
        if not resp.ok:
            raise ResponseError("{} ::: {}".format(resp.reason, resp.content))
        return resp.json()

    def add_event_interval(self,
                           event_name: str,
                           event_value: str,
                           start_time: datetime,
                           end_time: datetime,
                           session_uid: str) -> str:
        if start_time > end_time:
            raise InvalidTimeError("start time cannot be after the end time")

        entity_id = get_guid()
        entity_dict = {
            "session": session_uid,
            "start_time": datetime_or_str_to_iso_utc(start_time),
            "end_time": datetime_or_str_to_iso_utc(end_time),
            "timestamp": datetime_or_str_to_iso_utc(start_time),
            "enrichments": [],
            "entity_id": entity_id,
            "entity_name": event_name,
            "entity_value": event_value,
            "entity_type": EntityTypes.STATE_ENTITY_TYPE,
            "influence": EntityInfluenceTypes.AFFECT_FORWARD
        }

        self.add_entity(entity_dict=entity_dict)
        self.resolve_session(session_uid=session_uid)

        return entity_id

    def add_scalar_measurements(self,
                                measurement_name: str,
                                measurement_values: List[float],
                                timestamps: List[Union[datetime, str]],
                                session_uid: str) -> List[str]:

        entity_ids = []
        if len(timestamps) != len(measurement_values):
            raise IndexError(
                "measurement_values and timestamps should have same length")

        for timestamp, measurement_value in zip(
                timestamps, measurement_values):

            entity_id = get_guid()
            entity_dict = {
                "session": session_uid,
                "timestamp": datetime_or_str_to_iso_utc(timestamp),
                "enrichments": [],
                "entity_id": entity_id,
                "entity_name": measurement_name,
                "entity_value": measurement_value,
                "entity_type": EntityTypes.SCALAR_ENTITY_TYPE,
                "influence": EntityInfluenceTypes.LINEAR_INTERPOLATION
            }
            self.add_entity(entity_dict=entity_dict)
            entity_ids.append(entity_id)

        self.resolve_session(session_uid=session_uid)
        return entity_ids


class SceneEngineRequestHandler:
    """Helper for making authenticated requests to the scene engine."""

    def __init__(
            self,
            scene_engine_url,
            auth_token=None):
        self.scene_engine_url = scene_engine_url
        self.auth_token = auth_token

    def with_auth(self,
                  auth_token: Optional[str] = None,
                  ):
        if auth_token:
            self.auth_token = auth_token

        return self

    def get(self,
            route,
            trailing_slash=False,
            params=None,
            headers=None,
            remove_version=False):
        return self.__make_scene_engine_request(
            method="get",
            route=route,
            trailing_slash=trailing_slash,
            params=params,
            headers=headers,
            remove_version=remove_version)

    def post(
            self,
            route,
            trailing_slash=False,
            params=None,
            json=None,
            headers=None,
            remove_version=False):
        return self.__make_scene_engine_request(
            method="post",
            route=route,
            trailing_slash=trailing_slash,
            params=params,
            json=json,
            headers=headers,
            remove_version=remove_version)

    def put(
            self,
            route,
            trailing_slash=False,
            params=None,
            json=None,
            headers=None,
            remove_version=False):
        return self.__make_scene_engine_request(
            method="put",
            route=route,
            trailing_slash=trailing_slash,
            params=params,
            json=json,
            headers=headers,
            remove_version=remove_version)

    def delete(
            self,
            route,
            trailing_slash=False,
            params=None,
            json=None,
            headers=None,
            remove_version=False):
        return self.__make_scene_engine_request(
            method="delete",
            route=route,
            trailing_slash=trailing_slash,
            params=params,
            json=json,
            headers=headers,
            remove_version=remove_version)

    def __make_scene_engine_request(
            self,
            method,
            route="",
            trailing_slash=False,
            params=None,
            json=None,
            headers=None,
            remove_version=False):
        assert method in {"get", "post", "put", "delete"}
        url = self.__get_scene_engine_url(
            route, trailing_slash, remove_version)
        request_ = getattr(requests, method)
        if self.auth_token:
            if not params:
                params = {}
            params["token"] = self.auth_token
        resp = request_(
            url,
            params=params,
            json=json,
            headers=headers)
        if not resp.ok:
            raise ResponseError(
                "{} ::: {} with token::: {}".format(
                    resp.reason, resp.content, self.auth_token))
        return resp

    def __get_scene_engine_url(self, route, trailing_slash, remove_version):

        if remove_version:
            scene_engine_url_ = re.sub(
                "{}".format(VERSION_POSTFIX), "", self.scene_engine_url)
        else:
            scene_engine_url_ = self.scene_engine_url

        url = join(scene_engine_url_, route)
        if trailing_slash and not url.endswith("/"):
            url += "/"
        return url
