#  Copyright (c) 2020 Caliber Data Labs.
#  All rights reserved.
#

import io
import json
import os
import re
import shutil
import tempfile
import time
from os.path import exists, join
from typing import Dict, List, Optional

import requests
from deprecated import deprecated
from diskcache import Cache

from ..constants import AssetsConstants, JobConstants
from ..custom_exceptions import (AssetError, IdentityError, InvalidAssetType,
                                 InvalidAuthorization, JobError)
from ..tools import misc
from ..tools.logger import get_logger
from ..tools.naming import standardize_name
from ..tools.time_utils import jsonify_metadata

DEFAULT_SEARCH_SIZE = 50
PAUSE_TIME = 0.05

logger = get_logger(__name__)

VERSION_PATTERN = re.compile(r'/v\d+')
temp_dir = tempfile.TemporaryDirectory(dir='/tmp').name.split('/')[-2]
DEFAULT_CACHE_DIR = os.getenv('CACHE_DIR', temp_dir)
DEFAULT_CACHE_SIZE = os.getenv("CACHE_MAX_SIZE", 50)
DEFAULT_CACHE_SUB_DIR = "default"
DEFAULT_ORGANIZATION_SUB_DIR = 'default'


class AssetManagerClientCache(object):
    """File cache for assets fetched via the AssetManagerClient.

    Using the least-frequently-used eviction policy, the cache will fill
    until the size_limit_gb is reached and will begin eviction
    """

    def __init__(
            self,
            cache_size_gb: int = None,
            disabled: bool = False,
            asset_type: Optional[str] = None,
            identity: Optional[dict] = None
    ):

        if not cache_size_gb:
            cache_size_gb = DEFAULT_CACHE_SIZE

        self.cache_disabled = disabled
        self.cache_size_gb = int(cache_size_gb)

        # Initialized in the _set_cache method
        self.cache_location = None
        self.cache = None
        self._set_cache(asset_type=asset_type, identity=identity)

    def _get_cache_location(
            self,
            asset_type: Optional[str] = None,
            identity: Optional[dict] = None):
        # When not provided, defaults to <DEFAULT_CACHE_DIR,asset_type>.
        # If asset_type is None (for example, when initializing SceneEngineClient),
        # then defaults to a default sub directory.
        if asset_type:
            cache_location = os.path.join(DEFAULT_CACHE_DIR, asset_type)
        else:
            cache_location = os.path.join(
                DEFAULT_CACHE_DIR, DEFAULT_CACHE_SUB_DIR)

        organization = self._get_sanitized_organization_name(identity)
        cache_location = os.path.join(cache_location, organization)
        self.cache_location = cache_location
        return cache_location

    def _get_sanitized_organization_name(
            self,
            identity: Optional[dict] = None,
            replace_char: str = '_'):
        # Sanitize the organization name
        if identity:
            organization = identity.get('organization', '')
        else:
            organization = DEFAULT_ORGANIZATION_SUB_DIR
        organization = organization.lower()
        for symbol in [' ', '/', '\'', '\"', '(', ')']:
            organization = organization.replace(symbol, replace_char)
        return organization

    def _set_cache(
            self,
            asset_type: Optional[str] = None,
            identity: Optional[dict] = None) -> None:
        """Set the cache location.

        Args:
            asset_type (str): Asset type
            identity (dict): User identity dict
        """
        try:
            self.cache_location = self._get_cache_location(
                asset_type=asset_type, identity=identity)
            os.makedirs(self.cache_location, exist_ok=True)
        except Exception as e:
            logger.info(
                " cache_location ::: could not create {} because of {}, instead {} is created".format(
                    self.cache_location, e, temp_dir))
            self.cache_location = temp_dir
            os.makedirs(self.cache_location, exist_ok=True)

    def get_file_from_cache(self, key):
        if self.cache_disabled:
            return
        # Read a file as a File object
        with Cache(
                directory=self.cache_location,
                eviction_policy='least-frequently-used',
                size_limit=self.cache_size_gb * (2 ** 30)
        ) as ref:
            return ref.get(key, read=True)

    def put_file_into_cache(self, key, value):
        if self.cache_disabled:
            return
        # Put a file as a File object
        with Cache(
                directory=self.cache_location,
                eviction_policy='least-frequently-used',
                size_limit=self.cache_size_gb * (2 ** 30)
        ) as ref:
            return ref.set(key, value, read=True)

    def get_bytes_from_cache(self, key):
        if self.cache_disabled:
            return
        # Read a file as a bytes array
        with Cache(
                directory=self.cache_location,
                eviction_policy='least-frequently-used',
                size_limit=self.cache_size_gb * (2 ** 30)
        ) as ref:
            return ref.get(key, read=False)

    def put_bytes_into_cache(self, key, value):
        if self.cache_disabled:
            return
        with Cache(
                directory=self.cache_location,
                eviction_policy='least-frequently-used',
                size_limit=self.cache_size_gb * (2 ** 30)
        ) as ref:
            return ref.set(key, value, read=False)


class AssetManagerClient(AssetManagerClientCache):
    def __init__(
            self,
            asset_type: Optional[str] = None,
            asset_manager_url: Optional[str] = None,
            metadata_only: bool = False,
            auth_token: Optional[str] = None,
            cache_disabled: bool = False,
            is_non_standard_asset: bool = False
    ):
        """Asset manager client for fetching/putting assets and metadata.

        :param asset_type: (str) The type of asset
        :param asset_manager_url: (str) The URL of the asset manager
        :param metadata_only: (bool) Whether to only return metadata
        :param auth_token: (str) Authentication token of the user -- must be provided
        :param cache_disabled: (bool): Disable caching; defaults to False
        :param is_non_standard_asset (bool): Whether the asset is a non-standard asset.
               If True, ignore asset-type checks.
        """

        if is_non_standard_asset is False and asset_type not in AssetsConstants.VALID_ASSETS:
            raise ValueError('Invalid asset_type `{}`'.format(asset_type))

        # Override enabled cache with env variable
        if misc.as_bool(os.environ.get("DISABLE_CACHING", False)):
            cache_disabled = True

        self.is_non_standard_asset = is_non_standard_asset
        self.asset_type = asset_type
        self.metadata_only = metadata_only

        if asset_manager_url is None:
            raise AssetError('asset_manager_url must be provided')
        self.asset_manager_url = asset_manager_url
        self.jobs_namespace_url = join(asset_manager_url, "jobs")
        self.assets_namespace_url = join(asset_manager_url, "assets")

        self.auth_token = auth_token
        if self.auth_token:
            self.identity = self._get_identity()
        else:
            self.identity = None

        super().__init__(
            asset_type=asset_type,
            cache_size_gb=DEFAULT_CACHE_SIZE,
            disabled=cache_disabled,
            identity=self.identity
        )

    def _get_identity(
            self,
            wait_for_connection: bool = True,
            max_wait_time: int = 60):
        env_user_identity = os.getenv('SCENEBOX_USER_IDENTITY')
        if env_user_identity:
            # TODO: This is a temporary fix and should be improved
            return json.loads(env_user_identity)
        else:
            if self.auth_token is None:
                raise IdentityError(
                    'Cannot get identity when no auth has been provided')
            params = {}
            if self.auth_token:
                params['token'] = self.auth_token

            # Strip version from asset manager URL
            version_match = re.search(VERSION_PATTERN, self.asset_manager_url)
            if version_match:
                version = version_match.group()
                root_url = self.asset_manager_url.split(version)[0]
            else:
                root_url = self.asset_manager_url

            wait_time = 0
            sleep_time = 5
            while True:
                try:
                    resp = requests.get(
                        os.path.join(
                            root_url,
                            'auth'),
                        params=params)
                    break
                except requests.exceptions.ConnectionError as e:
                    if not wait_for_connection or wait_time > max_wait_time:
                        raise e
                    else:
                        logger.warning(
                            "could not connect to {}, retrying in {} seconds".format(
                                root_url, sleep_time))
                        time.sleep(sleep_time)
                        wait_time = wait_time + sleep_time
            if not resp.ok:
                raise IdentityError(
                    "Could not obtain the user identity {}", resp.content)
            return resp.json()

    def _set_asset_state(
            self,
            asset_type: str,
            metadata_only: bool
    ):
        if asset_type not in AssetsConstants.VALID_ASSETS:
            raise InvalidAssetType(
                "The asset type {} is invalid. Valid types are: {}".format(
                    asset_type, AssetsConstants.VALID_ASSETS))

        if not isinstance(metadata_only, bool):
            raise ValueError("metadata_only must be a boolean")

        self.asset_type = asset_type
        self.metadata_only = metadata_only

        if metadata_only is False:
            self._set_cache(asset_type=asset_type, identity=self.identity)
        return self

    def add_asset_manager_params(
            self, params_dict: Optional[dict] = None) -> dict:

        if self.auth_token is None:
            raise InvalidAuthorization(
                "No authorization is provided in AssetManagerClient")

        params_dict = params_dict or {}
        params_dict['asset_type'] = self.asset_type
        params_dict['metadata_only'] = self.metadata_only
        if self.auth_token:
            params_dict['token'] = self.auth_token
        return params_dict

    def with_auth(self,
                  auth_token: Optional[str] = None,
                  ):
        if auth_token:
            self.auth_token = auth_token

        self.identity = self._get_identity()
        self._set_cache(asset_type=self.asset_type, identity=self.identity)
        return self

    def register_field(self, field_dict: dict):
        url = self.get_assets_url('register_field/')
        params = self.add_asset_manager_params({})
        resp = requests.post(
            url,
            json=field_dict,
            params=params)
        if not resp.ok:
            raise AssetError(
                'Could not register the field ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def delete(
            self,
            identifier: str,
            delete_contents: bool = True,
            wait_for_deletion: bool = True) -> dict:

        identifier = self._check_identifier(identifier)
        url = self.get_assets_url(identifier)
        params = {
            'delete_contents': delete_contents
        }
        params = self.add_asset_manager_params(params)
        resp = requests.delete(url, params=params)

        if not resp.ok:
            raise AssetError(
                'Could not delete the file ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))

        if wait_for_deletion:
            self._wait_for_non_existence(identifier)

        return resp.json()

    def put_directory(self, directory_path, identifier, temp_dir=temp_dir):
        """Convert a directory to a zipfile and upload."""
        identifier = self._check_identifier(identifier)
        if not os.path.exists(directory_path):
            raise IOError('Path does not exist')

        with tempfile.NamedTemporaryFile(dir=temp_dir) as f:
            zip_ext = 'zip'
            temp_zipfile_path = f.name
            shutil.make_archive(temp_zipfile_path, zip_ext, directory_path)

            self.put_file(
                "{}.{}".format(temp_zipfile_path, zip_ext),
                identifier=identifier,
                wait_for_completion=True)

    def put_file(
            self,
            file,
            identifier,
            metadata: Optional[Dict] = None,
            wait_for_completion=False):
        """ Register and upload a file with the asset manager
        Args:
            file (BytesIO or filepath): The BytesIO object or filepath to upload as binary
            identifier (str): the uid of the file
            metadata (Optional[dict]): Optionally put metadata with the file
            wait_for_completion (bool): Whether to wait for the upload to finish before returning
        :return:
        """
        identifier = self._check_identifier(identifier)
        self._check_storage()

        if isinstance(file, io.BytesIO):
            file.seek(0)
            filestr = file.read()
        elif isinstance(file, bytes):
            filestr = file
        else:
            if not exists(file):
                raise AssetError(
                    'The provided file is not a BytesIO object or the filepath does not exist')
            else:
                with open(file, 'rb') as fin:
                    filestr = fin.read()

        # try:
            # if self.exists(identifier):
            # Delete the file but leave the contents, in the event that
            # metadata was written prior to the file upload
        #    self.delete(
        #        identifier,
        #        delete_contents=False,
        #        wait_for_deletion=True)
        # except AssetError:
            # File does not exist
        #    pass
        upload_params = self.get_temporary_upload_url(filenames=[identifier])
        url = upload_params[identifier]["url"]
        files = upload_params[identifier]["fields"]
        files["file"] = filestr
        resp = requests.post(url, files=files)
        if not resp.ok:
            raise AssetError(
                'Could not put the file ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))

        if metadata is not None:
            self.put_metadata(identifier, metadata=metadata)

        if wait_for_completion:
            self._wait_for_existence(identifier)

        return resp

    def _get_file_url(self, identifier):
        identifier = self._check_identifier(identifier)
        url = self.get_assets_url(identifier)
        params = self.add_asset_manager_params({"return_url": True})
        resp = requests.get(url, params=params)
        if not resp.ok:
            raise AssetError(
                'Could not get the file ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()['url']

    def get_file(
            self,
            identifier,
            return_url=False,
            write_filepath=None,
            return_file_path: bool = False):
        """Get a file from the asset manager.

        Args:
            identifier (str): The unique identifier for the file
            return_url (bool): Whether to return the file's storage URL (True)
                or the file-like object (False)
            write_filepath (str or None): If provided, write the binary data to the file path. If None, return bytes
            return_file_path (bool): If True, return the local path to the file in the AssetManagerCache
        Returns:
            if return_url=True, returns a string URL
            if return_url=False, returns a bytes array
        """
        identifier = self._check_identifier(identifier)
        if return_url:
            return self._get_file_url(identifier)

        # Check if the response object exists locally in the cache
        data_bytes = self.get_bytes_from_cache(identifier)

        if not data_bytes:
            self._check_storage()
            url = self.get_assets_url(identifier)
            params = self.add_asset_manager_params(
                {"return_url": return_url})
            resp = requests.get(url, params=params)
            if not resp.ok:
                raise AssetError(
                    'Could not get the file ::: {} -- {} -- {}'.format(
                        self.asset_type, resp.reason, resp.content))
            data_bytes = resp.content

            self.put_bytes_into_cache(identifier, data_bytes)

        if return_file_path:
            file = self.get_file_from_cache(identifier)
            return file.name

        if write_filepath:
            bytesio_data = io.BytesIO(data_bytes)
            with open(write_filepath, 'wb') as fout:
                fout.write(bytesio_data.read())
        else:
            return data_bytes

    @deprecated("Using `put_file_path` is bug prone until redesigned")
    def put_file_path(self, identifier, file_path):
        identifier = self._check_identifier(identifier)
        payload = {'file_path': file_path}
        url = self.get_assets_url('file_path/{}'.format(identifier))
        params = self.add_asset_manager_params()
        resp = requests.put(url, json=payload, params=params)
        if not resp.ok:
            raise AssetError(
                'Could not put the file path ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def exists(self, identifier):
        identifier = self._check_identifier(identifier)
        url = self.get_assets_url('exists/{}'.format(identifier))
        params = self.add_asset_manager_params()
        resp = requests.get(url, params=params)
        if not resp.ok:
            raise AssetError(
                'Could not find the identifier ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def copy(self, identifier: str, new_identifier: str):
        identifier = self._check_identifier(identifier)
        url = self.get_assets_url('copy/{}'.format(identifier))
        params = self.add_asset_manager_params({"new_id": new_identifier})
        resp = requests.put(url, params=params)
        if not resp.ok:
            raise AssetError(
                'Could not copy the identifier {} to {} ::: {} -- {} -- {}'.format(
                    identifier,
                    new_identifier,
                    self.asset_type,
                    resp.reason,
                    resp.content))
        return resp.json()

    def count(self, search_dic: Optional[dict] = None) -> int:
        url = self.get_assets_url('count/')
        params = self.add_asset_manager_params()
        search_dic = search_dic or {}
        resp = requests.post(
            url,
            json=search_dic,
            params=params)
        if not resp.ok:
            raise AssetError(
                'Could not count the files::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def get_file_path(self, identifier):
        identifier = self._check_identifier(identifier)
        url = self.get_assets_url('file_path/{}'.format(identifier))
        params = self.add_asset_manager_params()
        resp = requests.get(url, params=params)
        if not resp.ok:
            raise AssetError(
                'Could not get the file path ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def get_file_path_from_metadata(self, metadata, identifier):
        identifier = self._check_identifier(identifier)
        url = self.get_assets_url(
            'file_path_from_metadata/{}'.format(identifier))
        params = self.add_asset_manager_params()
        metadata = jsonify_metadata(metadata)
        resp = requests.post(url, json=metadata, params=params)
        if not resp.ok:
            raise AssetError(
                'Could not get the file path from metadata ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def get_metadata(self, identifier: str) -> dict:
        identifier = self._check_identifier(identifier)
        url = self.get_assets_url('meta/{}'.format(identifier))
        params = self.add_asset_manager_params()
        resp = requests.get(url, params=params)
        if not resp.ok:
            raise AssetError(
                'Could not get the metadata from the identifier ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def put_string(self,
                   content_str: str,
                   identifier: str,
                   wait_for_completion: bool = False):
        identifier = self._check_identifier(identifier)
        self._check_storage()
        try:
            # if self.exists(identifier):
            # Delete the file but leave the contents, in the event that
            # metadata was written prior to the file upload
            self.delete(
                identifier,
                delete_contents=False,
                wait_for_deletion=True)
        except AssetError:
            # File does not exist
            pass

        url = self.get_assets_url('string/{}'.format(identifier))
        params = self.add_asset_manager_params()
        resp = requests.put(
            url,
            params=params,
            data=content_str)

        if not resp.ok:
            raise AssetError(
                'Could not put the metadata and string for the identifier ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        if wait_for_completion:
            self._wait_for_existence(identifier)
        return resp.json()

    def put_metadata(self,
                     identifier: str,
                     metadata: dict,
                     replace: bool = True,
                     replace_sets: bool = False,
                     mappings: Optional[dict] = None):
        identifier = self._check_identifier(identifier)
        url = self.get_assets_url("meta/{}".format(identifier))
        params = {
            "replace": replace,
            "mappings": mappings,
            "replace_sets": replace_sets}
        params = self.add_asset_manager_params(params)
        metadata_json = jsonify_metadata(metadata)

        resp = requests.put(
            url,
            json=metadata_json,
            params=params)

        if not resp.ok:
            raise AssetError(
                'Could not replace the metadata for the identifier ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def update_metadata(
            self,
            identifier: str,
            metadata: dict,
            replace_sets: bool = False) -> dict:
        identifier = self._check_identifier(identifier)
        url = self.get_assets_url('meta/{}'.format(identifier))
        params = {'replace': 'false', 'replace_sets': replace_sets}
        params = self.add_asset_manager_params(params)
        metadata_json = jsonify_metadata(metadata)

        resp = requests.put(
            url,
            json=metadata_json,
            params=params)
        if not resp.ok:
            raise AssetError(
                'Could not update the metadata for the identifier ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def search_assets(
            self,
            query: Optional[dict] = None,
            size: int = DEFAULT_SEARCH_SIZE,
            offset: int = 0,
            scan: bool = False) -> List[str]:
        query = self._validate_query(query)
        params = {'size': size, 'offset': offset, 'scan': scan}
        url = self.get_assets_url('')
        params = self.add_asset_manager_params(params)
        resp = requests.post(url, json=query, params=params)
        if not resp.ok:
            raise AssetError(
                'Could not search the files ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()['results']

    def remove_with_query(self,
                          query: Optional[dict] = None,
                          wait_for_completion: bool = False) -> str:
        query = self._validate_query(query)
        params = self.add_asset_manager_params()
        url = self.get_assets_url('remove_with_query/')
        resp = requests.post(url, json=query, params=params)
        if not resp.ok:
            raise AssetError(
                'Could not remove the assets ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))

        job_id = resp.json()['job_id']
        if wait_for_completion:
            self._wait_for_job_completion(job_id)

        return job_id

    def remove_with_list(self,
                         assets_list: Optional[list] = None,
                         wait_for_completion: bool = False) -> str:
        assets_list = assets_list or []
        params = self.add_asset_manager_params()
        url = self.get_assets_url('remove_with_list/')
        resp = requests.post(
            url,
            json={
                "assets_list": assets_list},
            params=params)
        if not resp.ok:
            raise AssetError(
                'Could not remove the assets ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))

        job_id = resp.json()['job_id']
        if wait_for_completion:
            self._wait_for_job_completion(job_id)

        return job_id

    def search_meta(
            self,
            query=None,
            size=DEFAULT_SEARCH_SIZE,
            offset=0,
            sort_field=None,
            sort_order=None,
            scan=False):
        query = self._validate_query(query)
        params = {'size': size, 'offset': offset, 'scan': scan}
        if sort_field:
            params['sort_field'] = sort_field
        if sort_order:
            params['sort_order'] = sort_order
        url = self.get_assets_url('meta')
        params = self.add_asset_manager_params(params)
        resp = requests.post(url, json=query, params=params)
        if not resp.ok:
            raise AssetError(
                'Could not search the metadata ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def summary_meta(self, summary_request):
        url = self.get_assets_url('meta/summary/')
        params = self.add_asset_manager_params()
        resp = requests.post(
            url,
            json=summary_request,
            params=params)
        if not resp.ok:
            raise AssetError(
                'Could not retrieve the metadata summary ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def api_status(self):
        url = self.get_assets_url('status/')
        params = self.add_asset_manager_params()
        resp = requests.get(url, params=params)
        if not resp.ok:
            raise AssetError(
                'Could not check the status of the API ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))

    def get_assets_url(self, route=""):
        url = join(self.assets_namespace_url, route)
        return url

    def get_statistics(self, field_dicts: List[dict]):
        statistics_endpoint = self.get_assets_url("field_statistics/")
        params = self.add_asset_manager_params()
        resp = requests.post(
            statistics_endpoint,
            params=params,
            json={
                'field_dicts': field_dicts})
        if not resp.ok:
            raise AssetError(
                'Could not get field statistics ::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()

    def _get_job_status(self, job_id):
        """Get the status of the async job.

        Assumes that the job_id is the same as the celery task_id

        :param job_id: Celery task ID
        :return:
        """
        status_endpoint = os.path.join(
            self.jobs_namespace_url, "status", job_id)
        params = {}
        if self.auth_token:
            params['token'] = self.auth_token
        resp = requests.get(status_endpoint, params=params)
        status = resp.json().get('status')
        return status

    def _wait_for_job_completion(self, job_id):
        while True:
            status = self._get_job_status(job_id)
            if status == JobConstants.STATUS_FINISHED:
                break
            elif status in {JobConstants.STATUS_CANCELLED, JobConstants.STATUS_ABORTED}:
                job_metadata = self.with_asset_state(
                    'jobs', True).get_metadata(job_id)
                job_notes = job_metadata['notes']
                raise JobError(
                    'Job {} encountered error with status {} with notes::: {}'.format(
                        job_id, status, job_notes))
            else:
                time.sleep(1)

    def _wait_for_existence(self, identifier):
        identifier = self._check_identifier(identifier)
        while not self.exists(identifier):
            time.sleep(PAUSE_TIME)

    def _wait_for_non_existence(self, identifier):
        identifier = self._check_identifier(identifier)
        while self.exists(identifier):
            time.sleep(PAUSE_TIME)

    def _check_storage(self):
        if self.metadata_only:
            raise AssetError('Asset client is metadata only')

    def update_asset_state(self, asset_type: str, metadata_only: bool = False):

        if self.is_non_standard_asset is False and asset_type not in AssetsConstants.VALID_ASSETS:
            raise InvalidAssetType(
                "The asset type {} is invalid. Valid types are: {}".format(
                    asset_type, AssetsConstants.VALID_ASSETS))

        if not isinstance(metadata_only, bool):
            raise ValueError("metadata_only must be a boolean")

        self.asset_type = asset_type
        self.metadata_only = metadata_only

    def with_asset_state(self, asset_type: str, metadata_only: bool = False):
        """Set the asset state, for use in chaining.

        Eg. client.with_asset_state("images", True).search_files({})
        """

        self.update_asset_state(
            asset_type=asset_type,
            metadata_only=metadata_only)
        return self

    def _validate_query(self, query):
        if query is None:
            query = {}
        elif not isinstance(query, dict):
            raise ValueError('Query parameter must be a dictionary')
        return query

    def _check_identifier(self, identifier: str) -> str:
        # Perform any preprocessing on the identifier
        if self.asset_type == AssetsConstants.SESSIONS_ASSET_ID:
            identifier = standardize_name(identifier)
        return identifier

    def download_data_with_query(self,
                                 destination_dir,
                                 query=None,
                                 size=DEFAULT_SEARCH_SIZE,
                                 offset=0,
                                 scan=False,
                                 download_metadata=True):

        if not os.path.isdir(destination_dir):
            raise NotADirectoryError(
                "{} does not exist".format(destination_dir))

        identifiers = self.search_assets(
            query=query, size=size, offset=offset, scan=scan)

        for identifier in identifiers:
            logger.info(
                "downloading binary and metadata for {}".format(identifier))
            if not self.metadata_only:
                filepath = os.path.join(destination_dir, identifier)
                self.get_file(identifier=identifier, write_filepath=filepath)
            if download_metadata:
                metadata = self.get_metadata(identifier=identifier)
                json_filepath = os.path.join(
                    destination_dir, '{}.json'.format(identifier))
                with open(json_filepath, 'w') as file:
                    file.write(json.dumps(metadata))

    def get_temporary_upload_url(self, filenames: List[str]):
        url = self.get_assets_url('temporary_upload_url/')
        params = self.add_asset_manager_params()
        body = {"filenames": filenames}
        resp = requests.post(
            url,
            json=body,
            params=params)
        if not resp.ok:
            raise AssetError(
                'Could not get temporary upload url::: {} -- {} -- {}'.format(
                    self.asset_type, resp.reason, resp.content))
        return resp.json()
