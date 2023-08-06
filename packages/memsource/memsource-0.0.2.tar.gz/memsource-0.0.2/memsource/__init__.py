#!/usr/bin/env python

"""."""

import json
import os.path
import requests

from memsource import auth
from memsource import exceptions
from memsource.constants import MEMSOURCE_ENDPOINT_V1_URL, MEMSOURCE_ENDPOINT_V2_URL


class Memsource:
    """."""

    def __init__(self, username, password):
        self.auth = auth.Auth(username, password)

    def handle_rest_call(self, url, method="GET", data=None, headers=None, files=None, payload=None):
        """Handle HTTP Rest calls to the API"""

        if not headers:
            headers = {
                "Content-type": "application/json",
            }

        headers.update({"Authorization": "ApiToken %s" % self.auth.token})

        if method == "GET":
            result = requests.get(url, headers=headers, params=payload)
        elif method == "POST":
            result = requests.post(url, headers=headers, json=data, files=files)
        elif method == "DELETE":
            result = requests.delete(url, headers=headers, json=data, params=payload)

        if result.status_code == 400:
            raise exceptions.MemsourceHTTPBadRequestException(result)
        if result.status_code == 401:
            raise exceptions.MemsourceHTTPNotAuthorizedException(result)
        elif result.status_code == 403:
            raise exceptions.MemsourceHTTPForbiddenException(result)
        elif result.status_code == 404:
            raise exceptions.MemsourceHTTPNotFoundException(result)
        elif result.status_code == 405:
            raise exceptions.MemsourceHTTPMethodNotAllowedException(result)

        return result

    # Endpoint: projectTemplates
    #
    def get_templates(self, filters=None):
        """List all Memsource templates"""

        url = "%s/projectTemplates" % MEMSOURCE_ENDPOINT_V1_URL

        try:
            templates = self.handle_rest_call(url, "GET").json()["content"]
            return templates if not filters else [item for item in templates if filters.items() <= item.items()]
        except Exception as exc:
            raise exc

        return templates

    # Endpoint: importSettings
    #
    def get_import_settings(self, filters=None):
        """List all Memsource importSettings"""

        url = "%s/importSettings" % MEMSOURCE_ENDPOINT_V1_URL

        try:
            import_settings = self.handle_rest_call(url, "GET").json()["content"]

            return import_settings if not filters else [item for item in import_settings if filters.items() <= item.items()]
        except Exception as exc:
            raise exc

    # Endpoint: projects
    #
    def get_projects(self, filters=None):
        """List all Memsource projects"""

        url = "%s/projects" % MEMSOURCE_ENDPOINT_V1_URL

        try:
            projects = self.handle_rest_call(url, "GET").json()["content"]
            return projects if not filters else [item for item in projects if filters.items() <= item.items()]
        except Exception as exc:
            raise exc

    def get_project_by_id(self, project_id):
        """Retrieve Memsource project by its id"""

        url = "%s/projects/%s" % (MEMSOURCE_ENDPOINT_V1_URL, project_id)

        try:
            return self.handle_rest_call(url, "GET").json()
        except Exception as exc:
            raise exc

    def delete_project(self, project_id, purge=None, do_not_fail_on_404=False):
        """Delete a Memsource project by its id"""

        url = "%s/projects/%s" % (MEMSOURCE_ENDPOINT_V1_URL, project_id)

        query_param = {'purge': purge} if purge is not None else None

        try:
            return self.handle_rest_call(url, "DELETE", payload=query_param)
        except exceptions.MemsourceHTTPNotFoundException as exc:
            if do_not_fail_on_404:
                resp = requests.models.Response()
                resp.status_code = 404
                return resp
            raise exc
        except Exception as exc:
            raise exc

    def get_jobs(self, project_id, filters=None):
        """List all Memsource jobs attached to a project"""

        url = "%s/projects/%s/jobs" % (MEMSOURCE_ENDPOINT_V2_URL, project_id)

        try:
            jobs = self.handle_rest_call(url, "GET").json()["content"]
            return jobs if not filters else [item for item in jobs if filters.items() <= item.items()]
        except Exception as exc:
            raise exc

    def get_job_by_id(self, job_id, project_id):
        """Retrieve a Memsource job by its id"""

        url = "%s/projects/%s/jobs/%s" % (MEMSOURCE_ENDPOINT_V1_URL, project_id, job_id)

        try:
            return self.handle_rest_call(url, "GET").json()
        except Exception as exc:
            raise exc

    def get_job_targetfile(self, job_id, project_id):
        """Download job target file."""

        url = "%s/projects/%s/jobs/%s/targetFile" % (MEMSOURCE_ENDPOINT_V1_URL, project_id, job_id)

        try:
            return self.handle_rest_call(url, "GET")
        except Exception as exc:
            raise exc

    def delete_job(self, job_id, project_id, purge=None):
        """Delete a Memsource job by its id"""

        return self.delete_jobs([job_id], project_id, purge)

    def delete_jobs(self, job_ids, project_id, purge=None, do_not_fail_on_404=False):
        """Delete a Memsource job by its id"""

        url = "%s/projects/%s/jobs/batch" % (MEMSOURCE_ENDPOINT_V1_URL, project_id)

        query_param = {'purge': purge} if purge is not None else None

        if not isinstance(job_ids, list):
            job_ids = list(job_ids)

        kwargs = {'jobs': [{'uid': job} for job in job_ids]}

        try:
            return self.handle_rest_call(url, "DELETE", payload=query_param, data=kwargs)
        except exceptions.MemsourceHTTPNotFoundException as exc:
            if do_not_fail_on_404:
                resp = requests.models.Response()
                resp.status_code = 404
                return resp
            raise exc
        except Exception as exc:
            raise exc

    def create_project_from_template(self, name, template_id, **kwargs):
        """Create a Memsource project from an existing template."""

        url = "%s/projects/applyTemplate/%s" % (MEMSOURCE_ENDPOINT_V2_URL, template_id)

        try:
            kwargs.update({"name": name})
            return self.handle_rest_call(url, "POST", data=kwargs).json()
        except Exception as exc:
            raise exc

    def create_job(self, project_id, langs, filename, split_filename=None, **kwargs):
        """Create a Memsource job for a given project and lang"""

        url = "%s/projects/%s/jobs" % (MEMSOURCE_ENDPOINT_V1_URL, project_id)

        kwargs.update({'targetLangs': langs})

        files = {
            'file': open(filename, 'rb')
        }

        if split_filename:
            kwargs.update({'path': os.path.dirname(filename)})
            _filename = os.path.basename(filename)
        else:
            _filename = filename

        headers = {
            'Content-type': 'application/octet-stream',
            'Content-Disposition': 'filename=' + _filename,
            'Memsource': json.dumps(kwargs),
        }

        try:
            return self.handle_rest_call(url, "POST", data=kwargs, headers=headers, files=files).json()
        except Exception as exc:
            raise exc

    # Endpoint: subDomains
    #
    def get_subdomains(self):
        """List all Memsource subDomains"""

        url = "%s/subDomains" % MEMSOURCE_ENDPOINT_V1_URL

        try:
            return self.handle_rest_call(url, "GET").json()["content"]
        except Exception as exc:
            raise exc
