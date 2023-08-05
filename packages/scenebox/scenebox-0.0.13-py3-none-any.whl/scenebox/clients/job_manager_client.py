"""Jobs manager client.

Copyright 2020 Caliber Data Labs
"""

#  Copyright (c) 2020 Caliber Data Labs.
#  All rights reserved.
#

import json
import time
from os.path import join
from typing import Callable, Dict, List, Optional, Union

import requests

from ..constants import ACK_OK_RESPONSE, JobConstants, JobTypes
from ..custom_exceptions import JobError
from ..tools.logger import get_logger

DEFAULT_SEARCH_SIZE = 500

# seconds. Note that this determines the minimum job time.
CHECK_JOB_STATUS_INTERVAL = 10

logger = get_logger(__name__)

STATUS_INTERVAL = 30


class JobManagerClient(JobConstants):
    """Client for interacting with the Job Manager."""

    def __init__(
        self,
        asset_manager_url: str,
        auth_token: str,
        job_id: Optional[str] = None,
        asset_type: Optional[str] = None,
        asset_id: Optional[str] = None,
        username: Optional[str] = None,
        job_type: Optional[str] = None,
        notes: Optional[Union[List[str], str]] = None,
        description: Optional[str] = None,
        stage: Optional[str] = None
    ):
        """
        asset_manager_url: URL to asset manager
        auth_token: Auth token to use
        job_id: unique identifier of a job
        asset_type: Type of asset ( used for updating job metadata)
        asset_id: Asset ID (used for updating job metadata)
        username: Username (used for updating job metadata)
        job_type: Type of the job (used for updating job metadata)
        notes: time-history of the events in the job (started at what time, queued at what time) (used for updating job metadata)
        description: the description of the job (used for updating job metadata)
        stage: Job stage (used for updating job metadata)
        ttl: job's time to live in seconds
        sync_interval: Time interval to wait before checking if timeout > TTL or job failure,
        """

        self.jobs_api_url = join(asset_manager_url, "jobs")
        self.auth_token = auth_token

        if not job_id:
            job_id = self.create_job(
                asset_type,
                asset_id,
                username,
                job_type,
                notes,
                description,
                stage)

        self.job_id = job_id

    def create_job(
            self,
            asset_type: str,
            asset_id: str,
            username: str,
            job_type: str,
            notes: list,
            description: str,
            stage: str) -> str:

        if job_type not in JobTypes.VALID_TYPES:
            raise JobError("invalid job type {}".format(job_type))

        asset_id = asset_id or 'undefined'

        json_payload = {
            "asset_type": asset_type,
            "asset_id": asset_id,
            "user": username,
            "job_type": job_type or '',
            "notes": notes or [],
            "description": description or '',
            "stage": stage or '',
        }
        params = self.add_asset_manager_params()

        url = self.get_jobs_url("add/")
        resp = requests.post(url, json=json_payload, params=params)
        if not resp.ok:
            raise JobError(
                "Could not create the job ::: {} -- {}".format(
                    resp.reason, resp.content
                )
            )
        return resp.json()["job_id"]

    def queue(self):
        url = self.get_jobs_url('queue/{}'.format(self.job_id))
        params = self.add_asset_manager_params()
        resp = requests.put(url, params=params)
        if not resp.ok:
            raise JobError(
                "Could not queue the job ::: {} -- {}".format(
                    resp.reason, resp.content)
            )
        return resp.json()

    def run(self):
        url = self.get_jobs_url('run/{}'.format(self.job_id))
        params = self.add_asset_manager_params()
        resp = requests.put(url, params=params)
        if not resp.ok:
            raise JobError(
                "Could not run the job ::: {} -- {}".format(
                    resp.reason, resp.content)
            )
        return resp.json()

    def finish(self):
        if self.get_status() == JobConstants.STATUS_FINISHED:
            return
        url = self.get_jobs_url('finish/{}'.format(self.job_id))
        params = self.add_asset_manager_params()
        resp = requests.put(url, params=params)
        if not resp.ok:
            raise JobError(
                "Could not finish the job ::: {} -- {}".format(
                    resp.reason, resp.content
                )
            )
        return resp.json()

    def abort(self, error_string='', alert=False):
        error_string = str(error_string)
        if self.get_status() == JobConstants.STATUS_ABORTED:
            return
        url = self.get_jobs_url('abort/{}'.format(self.job_id))
        params = {'error_string': error_string, 'alert': alert}
        params = self.add_asset_manager_params(params)
        resp = requests.put(url, params=params)
        if not resp.ok:
            raise JobError(
                "Could not abort the job ::: {} -- {}".format(
                    resp.reason, resp.content)
            )
        return resp.json()

    def cancel(self):
        url = self.get_jobs_url('cancel/{}'.format(self.job_id))
        params = self.add_asset_manager_params()
        resp = requests.put(url, params=params)
        if not resp.ok:
            raise JobError(
                "Could not cancel the job ::: {} -- {}".format(
                    resp.reason, resp.content
                )
            )
        return resp.json()

    def append_note(self, note):
        url = self.get_jobs_url('append_note/{}'.format(self.job_id))
        params = {'note': note}
        params = self.add_asset_manager_params(params)
        resp = requests.put(url, params=params)
        if not resp.ok:
            raise JobError(
                "Could not append_note to the job ::: {} -- {}".format(
                    resp.reason, resp.content
                )
            )
        return resp.json()

    def update_meta(self, key, value):
        url = self.get_jobs_url('meta/{}'.format(self.job_id))
        data = {'key': key, 'value': value}
        params = self.add_asset_manager_params()
        resp = requests.put(url, json=data, params=params)
        if not resp.ok:
            raise JobError(
                "Could not update meta of the job ::: {} -- {}".format(
                    resp.reason, resp.content
                )
            )
        return resp.json()

    def get_meta(self):
        url = self.get_jobs_url('meta/{}'.format(self.job_id))
        params = self.add_asset_manager_params()
        resp = requests.get(url, params=params)
        if not resp.ok:
            raise JobError(
                "Could not get meta of the job ::: {} -- {}".format(
                    resp.reason, resp.content
                )
            )
        return resp.json().get("dict", {})

    def update_stage(self, stage):
        url = self.get_jobs_url('stage/{}'.format(self.job_id))
        params = {'stage': stage}
        params = self.add_asset_manager_params(params)
        resp = requests.put(url, params=params)
        if not resp.ok:
            raise JobError(
                "Could not update stage of the job ::: {} -- {}".format(
                    resp.reason, resp.content
                )
            )
        return resp.json()

    def get_status(self):
        url = self.get_jobs_url('status/{}'.format(self.job_id))
        params = self.add_asset_manager_params()
        resp = requests.get(url, params=params)
        if not resp.ok:
            raise JobError(
                "Could not get status of the job ::: {} -- {} -- with auth token: {}".format(
                    resp.reason, resp.content, self.auth_token))
        return resp.json()["status"]

    def get_progress(self):
        url = self.get_jobs_url('get_progress/{}'.format(self.job_id))
        params = self.add_asset_manager_params()
        resp = requests.put(url, params=params)
        if not resp.ok:
            raise JobError("Could not get the job progress")
        if not resp.ok:
            raise JobError(
                "Could not get progress the job ::: {} -- {}".format(
                    resp.reason, resp.content
                )
            )
        return resp.json()

    def update_progress(self, progress: float):
        """
        Args:
            progress (float): percentage of job progress
        """
        params = {'progress': progress}
        url = self.get_jobs_url('progress/{}'.format(self.job_id))
        params = self.add_asset_manager_params(params)
        resp = requests.put(url, params=params)
        if not resp.ok:
            raise JobError(
                "Could not update_progress of the job ::: {} -- {}".format(
                    resp.reason, resp.content
                )
            )
        return resp.json()

    def set_resubmit_data(self, resubmission_dict: dict):
        """Set the data for job resubmission."""
        resubmission_str = json.dumps(resubmission_dict)
        self.update_meta('resubmit', resubmission_str)
        return ACK_OK_RESPONSE

    def resubmit(self):
        """Resubmit an extraction job."""
        url = self.get_jobs_url('resubmit/{}'.format(self.job_id))
        params = self.add_asset_manager_params()
        resp = requests.put(url, params=params)
        if not resp.ok:
            raise JobError(
                "Could not resubmit the job ::: {} -- {}".format(
                    resp.reason, resp.content
                )
            )
        return resp.json()

    def get_jobs_url(self, route):
        url = join(self.jobs_api_url, route)
        return url

    def add_asset_manager_params(self, params_dict=None):
        if params_dict is None:
            params_dict = {}
        if self.auth_token:
            params_dict["token"] = self.auth_token
        return params_dict


def wait_for_jobs(
        job_ids: List[str],
        asset_manager_url: str,
        auth_token: str,
        timeout: Optional[int] = None,
        raise_on_error: bool = False
):
    failed_enrichment_jobs = set()
    successful_job_ids = set()
    logger.info("Waiting for {} jobs to finish:: {}".format(
        len(job_ids), job_ids[0:10]))

    # Wait for all enrichment tasks to finish
    enrichment_job_ids_to_clients = dict(
        [
            (
                job_id,
                JobManagerClient(
                    job_id=job_id,
                    asset_manager_url=asset_manager_url,
                    auth_token=auth_token
                )
            )
            for job_id in job_ids
        ]
    )
    logger.info("enrichment jobs being done: {}".format(
        enrichment_job_ids_to_clients))
    t1 = time.time()
    while True:
        finished_jobs = set()
        for job_id, job_manager_client in enrichment_job_ids_to_clients.items():
            job_status = job_manager_client.get_status()
            if job_status in {
                    JobManagerClient.STATUS_FINISHED,
                    JobManagerClient.STATUS_ABORTED}:
                if job_status == JobManagerClient.STATUS_FINISHED:
                    successful_job_ids.add(job_id)
                    logger.info('Job {} finished'.format(job_id))
                elif job_status == JobManagerClient.STATUS_ABORTED:
                    failed_enrichment_jobs.add(job_id)
                    logger.info('Job {} failed'.format(job_id))
                    if raise_on_error:
                        raise JobError(
                            "Job {} encountered failure".format(job_id))
                finished_jobs.add(job_id)

        enrichment_job_ids_to_clients = {
            k: v for k,
            v in enrichment_job_ids_to_clients.items() if k not in finished_jobs}
        if len(enrichment_job_ids_to_clients) == 0:
            break
        else:
            logger.info(
                "Waiting for {} jobs to finish:: {}".format(
                    len(enrichment_job_ids_to_clients), list(
                        enrichment_job_ids_to_clients.keys())[
                        0:5]))
            time.sleep(CHECK_JOB_STATUS_INTERVAL)
            if timeout and time.time() - t1 > timeout:
                raise TimeoutError(
                    "Waiting for {} jobs exceeded timeout of {}s".format(
                        len(job_ids), timeout))

    return {
        "successful": len(list(successful_job_ids)),
        "failed": len(list(failed_enrichment_jobs))
    }
