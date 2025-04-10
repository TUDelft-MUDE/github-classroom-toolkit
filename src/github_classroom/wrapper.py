import io
import json
import urllib.parse
import zipfile
import logging
from datetime import datetime
from pathlib import Path

import requests


class GithubClassroom:
    # todo: decide on making objects for results/reusing github wrapper package objects
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://github.com'
        self.api_url = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {self.token}',
            'X-GitHub-Api-Version': '2022-11-28',
        }
        # todo: send a test request here to see if token works?

    def _do_request(self, link, retry_count=5, use_api_url=True, **params):
        """
        Returns response object
        """
        if use_api_url:
            url_prefix = self.api_url
        else:
            url_prefix = self.base_url
        query_string = urllib.parse.urlencode(params)
        url = f'{url_prefix}{link}?{query_string}'
        try:
            response = requests.get(url, headers=self.headers)
        except requests.exceptions.RequestException as e:
            logging.error(f"exception occurred, request to link={link} retried, {retry_count} retries left")
            logging.error(f"exception: {e}")
            return self._do_request(link, retry_count=retry_count - 1, use_api_url=use_api_url, **params)
        if response.status_code == 200:
            logging.error(f"request to link={link} successful")
            return response
        elif retry_count > 0:
            logging.error(f"request to link={link} retried, {retry_count} retries left")
            return self._do_request(link, retry_count=retry_count - 1, use_api_url=use_api_url, **params)
        else:
            raise Exception(f'Request failed too many times')

    def _request_all_pages(self, link, state=None) -> list:
        """
        This function is needed as GitHub puts a limit on the amount of data you can request at once.
        The limit is 100, so for 250 students we need to place 3 requests.


        """
        result = []
        last_result = None
        current_page = 1
        while last_result is None or len(last_result) != 0:
            logging.error(f'requesting page {current_page} from {link}')
            json = self._do_request(link, page=current_page, per_page=100, state=state).json()
            # json = self._do_request(link, state='all', page=current_page, per_page=100).json()
            current_page += 1
            last_result = json
            result.extend(json)
        return result

    def list_classrooms(self):
        return self._request_all_pages('/classrooms')

    def get_classroom(self, classroom_id: int):
        response = self._do_request(f'/classrooms/{classroom_id}')
        result = response.json()
        return result

    def list_assignments(self, classroom_id: int):
        return self._request_all_pages(f'/classrooms/{classroom_id}/assignments')

    def get_assignment(self, assignment_id: int):
        response = self._do_request(f'/assignments/{assignment_id}')
        result = response.json()
        return result

    def list_accepted_assignments(self, assignment_id: int):
        return self._request_all_pages(f'/assignments/{assignment_id}/accepted_assignments')

    def list_grades(self, assignment_id: int):
        response = self._do_request(f'/assignments/{assignment_id}/grades')
        result = response.json()
        return result

    def get_repo_zip(self, group_name, repo_name, extract_to):
        # example: https://github.com/MUDE-2024/ga-1-4-alke1/archive/refs/heads/main.zip
        response = self._do_request(f'/{group_name}/{repo_name}/archive/refs/heads/main.zip', use_api_url=False)
        zip_file_bytes = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_file_bytes, 'r') as zip_ref:
            zip_ref.extractall(path=extract_to)

    @staticmethod
    def dump(file_name, path, json_data):
        now = datetime.now()
        now_formatted = now.strftime("%Y%m%d_%H%M%S")
        # todo: think about where the file should go, maybe let pass a path
        file_path = Path(f'{file_name}_{now_formatted}.json')
        full_path = path / file_path
        with open(full_path, 'w') as file:
            json.dump(json_data, file, indent=4)

    @staticmethod
    def is_valid(token) -> bool:
        # todo make cleaner with whole API
        url = "https://api.github.com/user"
        headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {token}',
            'X-GitHub-Api-Version': '2022-11-28',
        }

        response = requests.get(url, headers=headers)

        return response.status_code == 200
