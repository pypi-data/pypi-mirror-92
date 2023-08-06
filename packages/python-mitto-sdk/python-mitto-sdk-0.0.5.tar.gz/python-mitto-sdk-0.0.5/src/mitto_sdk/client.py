import requests


class Mitto:
    """
    Mitto instance
    """
    def __init__(self, base_url, api_key, verify=True):
        if base_url.endswith("/"):
            self.base_url = base_url[:-1]
        else:
            self.base_url = base_url
        self.api_key = api_key
        self.api_root = "/api"

        self.verify = verify

        # set up the session
        self.session = requests.Session()
        self.session.params = {
            "API_KEY": self.api_key
        }

    def page_through_results(self, url, params, limit=50, offset=0):
        """
        Page through results returned by Mitto API.
        """
        params["offset"] = offset
        params["limit"] = limit
        more_pages = True

        while more_pages:
            response = self.session.get(url=url, params=params)
            response.raise_for_status()
            data = response.json()
            pagination = data.get("pagination")
            if pagination:
                more_pages = pagination.get("more_pages")
                offset = pagination.get("offset")
                params["offset"] = offset + params["limit"]
            yield data

    def get_jobs(self, search=None, tag=None, job_type=None, status=None, **kwargs):
        """
        Get jobs from Mitto API. Filter using search, tag, type, and/or status.
        """
        uri = "/v2/jobs"
        url = f"{self.base_url}{self.api_root}{uri}"

        params = {
            "search": search,
            "tag": tag,
            "type": job_type,
            "status": status
        }

        results = self.page_through_results(url=url, params=params, **kwargs)
        for result in results:
            yield from result["jobs"]

    def get_job(self, job_id):
        """
        Get job from Mitto API. Pass in a valid job id.
        """
        uri = f"/v2/jobs/{job_id}"
        url = f"{self.base_url}{self.api_root}{uri}"

        results = self.session.get(url)
        return results.json()

    def get_about(self):
        """
        Get system information from Mitto API.
        """
        uri = "/about"
        url = f"{self.base_url}{self.api_root}{uri}"

        results = self.session.get(url)
        return results.json()

    def create_job(self, job, **kwargs):
        """
        Create a new Mitto job.
        """
        assert isinstance(job, dict)

        uri = f"/v2/jobs"
        url = f"{self.base_url}{self.api_root}{uri}"

        results = self.session.post(url=url, json=job, **kwargs)
        results.raise_for_status()
        return results.json()

    def update_job_conf(self, job_id=None, job_conf=None, **kwargs):
        """
        Update an existing Mitto job.
        """
        assert isinstance(job_conf, dict)
        assert isinstance(job_id, int)

        uri = f"/job/{job_id}/conf"
        url = f"{self.base_url}{self.api_root}{uri}"

        results = self.session.post(url=url, json=job_conf, **kwargs)
        results.raise_for_status()
        return results.json()

    def get_job_schedule(self, job_id=None, **kwargs):
        """
        Get a job's schedule. Pass in a valid job id.
        """

        assert isinstance(job_id, int)

        uri = f"/job/{job_id}/schedule"
        url = f"{self.base_url}{self.api_root}{uri}"

        results = self.session.get(url=url, **kwargs)
        results.raise_for_status()
        return results.json()

    def update_job_schedule(self, job_id=None, job_schedule=None, **kwargs):
        """
        Update a job's schedule. Pass in a valid id and schedule.
        """
        assert isinstance(job_id, int)
        assert isinstance(job_schedule, dict)

        uri = f"/job/{job_id}/schedule"
        url = f"{self.base_url}{self.api_root}{uri}"

        results = self.session.post(url=url, json=job_schedule, **kwargs)
        results.raise_for_status()
        return results.json()
