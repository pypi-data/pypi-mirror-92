import codecs
import json
import os
from datetime import datetime
from typing import List, Union
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from ruamel.yaml import YAML

from teko.helpers.clog import CLog
from teko.helpers.exceptions import TekoJiraException
from teko.models.jira_testcase import JiraTestcase


class JiraService:
    """
    Jira API docs: https://support.smartbear.com/zephyr-scale-server/api-docs/v1/
    """
    def __init__(self, config={}):
        """

        :param config: a dict like this, if something is missing, it will get from env variable
                {
                    "server": "https://jira.teko.vn",
                    "jira_username": "jira_username",
                    "jira_password": "jira_password",
                    "confluence_username": "confluence_username",
                    "confluence_password": "confluence_password",
                    "project_key": "PRJ",
                }
        """

        self.success = None

        load_dotenv()
        self.project_key = config.get('project_key') or os.getenv('JIRA_PROJECT_KEY')
        server = config.get('server') or os.getenv('JIRA_SERVER')
        jira_username = config.get('jira_username') or os.getenv('JIRA_USERNAME')
        jira_password = config.get('jira_password') or os.getenv('JIRA_PASSWORD')
        confluence_username = config.get('confluence_username') or os.getenv('CONFLUENCE_USERNAME')
        confluence_password = config.get('confluence_password') or os.getenv('CONFLUENCE_PASSWORD')

        if not self.project_key or not server or not jira_username or not jira_password or not confluence_username or not confluence_password:
            msg = "No valid JIRA configuration found, please set JIRA_SERVER, JIRA_PROJECT_KEY, JIRA_USERNAME, " \
                  "JIRA_PASSWORD, CONFLUENCE_USERNAME and CONFLUENCE_PASSWORD environment variables first."
            CLog.error(msg)
            raise TekoJiraException(msg)

        if not server.startswith("http://") and not server.startswith("https://"):
            server = "https://" + server
        self.base_api_url = urljoin(server, '/rest/atm/1.0')
        self.base_api_tests_url = urljoin(server, '/rest/tests/1.0')

        self.jira_session = requests.session()
        self.jira_session.auth = (jira_username, jira_password)

        self.confluence_session = requests.session()
        self.confluence_session.auth = (confluence_username, confluence_password)

    def search_testcases(self, issues=[], name=None):
        """

        :param issues: list of issue keys to filter
        :return:
        """
        query = f'projectKey = "{self.project_key}"'
        if issues:
            query += f' AND issueKeys IN ({",".join(issues)})'
        if name:
            query += f' AND name = "{name}"'

        params = {
            "query": query
        }

        url = self.base_api_url + "/testcase/search"

        res = self.jira_session.get(url=url, params=params)

        if res.status_code != 200:
            CLog.error(f"Failed to search for test case {name}.")
            if res.status_code == 401:
                CLog.error(f"Unauthorized: Authenticated failed.")
            elif res.status_code == 403:
                CLog.error(f"Forbidden: You don't have permission to send request GET to {url} with params {params}.")
            else:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}.")
            return []
        raw = res.text

        testcases_json = json.loads(raw)

        testcases = []
        for t in testcases_json:
            testcases.append(JiraTestcase().from_dict(t))
        return testcases

    def delete_trace_link(self, link_id):
        url = self.base_api_url + f"/tracelink/{link_id}"

        res = self.jira_session.delete(url=url)

        if res.status_code != 200:
            CLog.error(f"Failed to delete trace link {link_id}.")
            if res.status_code == 401:
                CLog.error(f"Unauthorized: Authenticated failed.")
            elif res.status_code == 403:
                CLog.error(f"Forbidden: You don't have permission to send request DELETE to {url}.")
            else:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}.")
            return
        raw = res.text

        testcases_json = json.loads(raw)

        CLog.info(f"{json.dumps(testcases_json)}")

    def empty_trace_links(self, test_id):
        url_confluence = self.base_api_tests_url + f"/testcase/{test_id}/tracelinks/confluencepage"

        res = self.jira_session.get(url=url_confluence)

        if res.status_code != 200:
            CLog.error(f"Failed to clear confluence links for test case {test_id}.")
            if res.status_code == 401:
                CLog.error(f"Unauthorized: Authenticated failed.")
            elif res.status_code == 403:
                CLog.error(f"Forbidden: You don't have permission to send request GET to {url_confluence}.")
            else:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}.")
        else:
            raw = res.text
            links = json.loads(raw)
            for link in links:
                self.delete_trace_link(link["id"])

        url_web = self.base_api_tests_url + f"/testcase/{test_id}/tracelinks/weblink"

        res = self.jira_session.get(url=url_web)

        if res.status_code != 200:
            CLog.error(f"Failed to clear web links for test case {test_id}.")
            if res.status_code == 401:
                CLog.error(f"Unauthorized: Authenticated failed.")
            elif res.status_code == 403:
                CLog.error(f"Forbidden: You don't have permission to send request GET to {url_web}.")
            else:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}.")
        else:
            raw = res.text
            links = json.loads(raw)
            for link in links:
                self.delete_trace_link(link["id"])

    def add_confluence_links(self, test_id, confluences: List[str]):
        url = self.base_api_tests_url + "/tracelink/bulk/create"

        if not confluences:
            return

        confluences_data = []

        for confluence_url in confluences:
            res = self.confluence_session.get(url=confluence_url)
            if res.status_code != 200:
                CLog.error(f"Failed to get id of confluence page {confluence_url}.")
                if res.status_code == 401:
                    CLog.error(f"Unauthorized: Authenticated failed.")
                elif res.status_code == 403:
                    CLog.error(f"Forbidden: You don't have permission to send request GET to {confluence_url}.")
                else:
                    CLog.error(f"HTTP Error {res.status_code}: {res.text}.")
                self.success = False
                return

            html = res.text
            soup = BeautifulSoup(html, "html.parser")
            page_id = soup.find("meta", {"name": "ajs-page-id"})["content"]

            confluences_data.append({
                "testCaseId": test_id,
                "confluencePageId": page_id,
                "typeId": 1
            })

        res = self.jira_session.post(url=url, json=confluences_data)

        if res.status_code != 200:
            CLog.error(f"Failed to add confluence links for test case {test_id}.")
            if res.status_code == 401:
                CLog.error(f"Unauthorized: Authenticated failed.")
            elif res.status_code == 403:
                CLog.error(f"Forbidden: You don't have permission to send request POST to {url} with payload {confluences_data}.")
            else:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}.")
            self.success = False

    def add_web_links(self, test_id, webs: List[Union[str, dict]]):
        url = self.base_api_tests_url + "/tracelink/bulk/create"

        if not webs:
            return

        webs_data = []

        for web in webs:
            if isinstance(web, str):
                webs_data.append({
                    "url": web,
                    "urlDescription": web,
                    "testCaseId": test_id,
                    "typeId": 1
                })
            else:
                webs_data.append({
                    "url": web.get('url'),
                    "urlDescription": web.get('description'),
                    "testCaseId": test_id,
                    "typeId": 1
                })

        res = self.jira_session.post(url=url, json=webs_data)

        if res.status_code != 200:
            CLog.error(f"Failed to add web links for test case {test_id}.")
            if res.status_code == 401:
                CLog.error(f"Unauthorized: Authenticated failed.")
            elif res.status_code == 403:
                CLog.error(f"Forbidden: You don't have permission to send request POST to {url} with payload {webs_data}.")
            else:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}.")
            self.success = False

    def add_links(self, test_id, confluences: List[str], webs: List[dict]):
        self.empty_trace_links(test_id)

        self.add_confluence_links(test_id, confluences)

        self.add_web_links(test_id, webs)

    def create_folder(self, name: str, type: str):
        data = {
            "projectKey": self.project_key,
            "name": name,
            "type": type
        }

        url = self.base_api_url + "/folder"

        """
        Ignore failure
        """
        res = self.jira_session.post(url=url, json=data)
        if res.status_code == 401:
            CLog.error(f"Cannot create {type} folder {name}.")
            CLog.error(f"Unauthorized: Authenticated failed.")
        if res.status_code == 403:
            CLog.error(f"Cannot create {type} folder {name}.")
            CLog.error(f"Forbidden: You don't have permission to send request POST to {url} with payload {data}.")
        if res.status_code != 201:
            CLog.info(f"{type} Folder {name} has already exists.")

    def get_test_id(self, test_key):
        url = self.base_api_tests_url + f"/testcase/{test_key}"

        res = self.jira_session.get(url=url, params={"fields": "id"})
        if res.status_code != 200:
            CLog.error(f"Failed to get id of test case {test_key}.")
            if res.status_code == 401:
                CLog.error(f"Unauthorized: Authenticated failed.")
            elif res.status_code == 403:
                CLog.error(f"Forbidden: You don't have permission to send request GET to {url}.")
            else:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}")
            self.success = False
            return

        raw = res.text
        return json.loads(raw).get('id')

    def create_or_update_testcases_by_name(self, testcases: List[JiraTestcase], issues=[]):
        CLog.info("Creating/Updating test cases.")
        self.success = True

        folders = set()

        for testcase in testcases:
            if testcase.folder:
                folders.add(testcase.folder)

        for folder in folders:
            self.create_folder(folder, "TEST_CASE")

        for testcase in testcases:
            existing_testcases = self.search_testcases(issues=issues, name=testcase.name)
            if not existing_testcases:
                key = self.create_testcase(testcase)
                testcase.key = key
            else:
                key = self.update_testcase(existing_testcases[0].key, testcase)
                testcase.key = key
            if key:
                self.add_links(
                    test_id=self.get_test_id(key),
                    confluences=testcase.confluenceLinks,
                    webs=testcase.webLinks
                )
        if not self.success:
            msg = "Creating/updating test cases process does not succeeded."
            CLog.info(msg)
            raise TekoJiraException(msg)
        return testcases

    def prepare_testcase_data(self, testcase: JiraTestcase):
        if not testcase.projectKey:
            testcase.projectKey = self.project_key

        data = {
            'name': testcase.name,
            'projectKey': testcase.projectKey,
            'folder': testcase.folder,
            'objective': testcase.objective,
            'precondition': testcase.precondition,
            'status': testcase.status
        }

        data.pop("status")

        if testcase.testScript:
            testscript = testcase.testScript.to_dict()
            testscript.pop("id")
            if testscript["type"] == "PLAIN_TEXT":
                testscript.pop("steps")
            elif testscript["type"] == "STEP_BY_STEP":
                testscript.pop("text")
            data.update({'testScript': testscript})

        if testcase.folder == "":
            data.pop("folder")

        if testcase.issueLinks:
            data['issueLinks'] = testcase.issueLinks

        return data

    def update_testcase(self, key: str, testcase: JiraTestcase):
        url = self.base_api_url + f"/testcase/{key}"
        data = self.prepare_testcase_data(testcase)
        data.pop('projectKey')
        res = self.jira_session.put(url=url, json=data)

        if res.status_code != 200:
            CLog.error(f"Failed to update test case `{testcase.name}`.")
            if res.status_code == 401:
                CLog.error(f"Unauthorized: Authenticated failed.")
            elif res.status_code == 403:
                CLog.error(f"Forbidden: You don't have permission to send request PUT to {url} with payload {data}.")
            else:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}.")
            self.success = False
            return None

        CLog.info(f"Updated test `{testcase.name}` successfully. Test key: {key}.")
        return key

    def create_testcase(self, testcase: JiraTestcase):
        data = self.prepare_testcase_data(testcase)
        url = self.base_api_url + "/testcase"
        res = self.jira_session.post(url=url, json=data)

        if res.status_code != 201:
            CLog.error(f"Failed to create test case `{testcase.name}`.")
            if res.status_code == 401:
                CLog.error(f"Unauthorized: Authenticated failed.")
            elif res.status_code == 403:
                CLog.error(f"Forbidden: You don't have permission to send request POST to {url} with payload {data}.")
            else:
                CLog.error(f"HTTP Error {res.status_code}: {res.text}.")
            self.success = False
            return None

        raw = res.text

        testcase_json = json.loads(raw)
        key = testcase_json['key']
        CLog.info(f"Created test `{testcase.name}` successfully. Test key: {key}.")
        return key

    def prepare_testrun_data(self, testcase: JiraTestcase):
        if not testcase.projectKey:
            testcase.projectKey = self.project_key

        data = {
            'testCaseKey': testcase.key,
            'status': testcase.testrun_status,
            'environment': testcase.testrun_environment,
            'executionTime': testcase.testrun_duration,
            'executionDate': testcase.testrun_date,
        }

        return data

    def create_test_cycle(self, testcases: List[JiraTestcase]):
        CLog.info("Creating test cycles.")
        self.success = True
        items_by_folder = dict()
        for testcase in testcases:
            existing_testcases = self.search_testcases(name=testcase.name)
            if not existing_testcases:
                CLog.error(f"Testcase with name `{testcase.name}` not existed.")
                self.success = False
            else:
                testcase.key = existing_testcases[0].key
                CLog.info(f"Testcase with name `{testcase.name}` existed.")
                if items_by_folder.get(testcase.testrun_folder) is None:
                    items_by_folder[testcase.testrun_folder] = []
                items_by_folder[testcase.testrun_folder].append(self.prepare_testrun_data(testcase))

        if not self.success:
            msg = "Creating test cycle process does not succeeded."
            CLog.error(msg)
            raise TekoJiraException(msg)

        url = self.base_api_url + "/testrun"

        for folder in items_by_folder.keys():
            self.create_folder(folder, "TEST_RUN")

        for folder, items in items_by_folder.items():
            data = {
                "projectKey": self.project_key,
                "name": f"[{self.project_key}] Cycle {datetime.now()}",
                "folder": folder,
                "items": items
            }

            if not folder:
                data.pop("folder")

            res = self.jira_session.post(url=url, json=data)

            if res.status_code != 201:
                CLog.error(f"Failed to create test cycle.")
                if res.status_code == 401:
                    CLog.error(f"Unauthorized: Authenticated failed.")
                elif res.status_code == 403:
                    CLog.error(f"Forbidden: You don't have permission to send request POST to {url} with payload {data}.")
                else:
                    CLog.error(f"HTTP Error {res.status_code}: {res.text}.")
                self.success = False
                return

            raw = res.text

            testcase_json = json.loads(raw)
            key = testcase_json['key']
            if folder:
                CLog.info(f"Test cycle {key} created in folder {folder}.")
            else:
                CLog.info(f"Test cycle {key} created.")

        if not self.success:
            msg = "Creating test cycle process does not succeeded."
            CLog.error(msg)
            raise TekoJiraException(msg)
        
    @staticmethod
    def read_testcases_from_file(testcase_file):
        """

        :param testcase_file: yaml or json file
        :return:
        """
        filename, ext = os.path.splitext(testcase_file)
        CLog.info(f"Reading {os.path.abspath(testcase_file)}.")
        if ext == ".json":
            with codecs.open(testcase_file, "r", encoding="utf-8") as f:
                try:
                    testcase_data = json.load(f)
                except Exception:
                    msg = "Invalid json format."
                    CLog.error(msg)
                    raise TekoJiraException(msg) from None

        elif ext == ".yaml":
            with codecs.open(testcase_file, "r", encoding="utf-8") as f:
                yaml = YAML(typ="safe")
                try:
                    testcase_data = yaml.load(f)
                except Exception:
                    msg = "Invalid yaml format"
                    CLog.error(msg)
                    raise TekoJiraException(msg) from None
        else:
            msg = f"File format not supported: {ext}."
            CLog.error(msg)
            raise TekoJiraException(msg)

        testcases = []
        for t in testcase_data:
            if t.get('folder') and t['folder'][0] != '/':
                t['folder'] = '/' + t['folder']
            if t.get('testrun_folder') and t['testrun_folder'][0] != '/':
                t['testrun_folder'] = '/' + t['testrun_folder']
            try:
                testcases.append(JiraTestcase().from_dict(t))
            except Exception:
                msg = f"Failed to parse test data from file {testcase_file}."
                CLog.error(msg)
                raise TekoJiraException(msg) from None

        return testcases

    @staticmethod
    def write_testcases_to_file(testcase_file, testcases):
        """

        :param testcase_file: yaml or json file
        :return:
        """
        testcases_json = []
        for t in testcases:
            CLog.info(f"{t}")
            data = t.to_dict()
            testcases_json.append(data)

        filename, ext = os.path.splitext(testcase_file)
        CLog.info(filename, ext)
        if ext == ".json":
            with codecs.open(testcase_file, "w", encoding="utf-8") as f:
                json.dump(testcases_json, f, indent=2)
        elif ext == ".yaml":
            with codecs.open(testcase_file, "w", encoding="utf-8") as f:
                yaml = YAML(typ="safe")
                yaml.indent(offset=2)
                yaml.dump(testcases_json, f)
        else:
            msg = f"File format not supported: {ext}."
            CLog.error(msg)
            raise TekoJiraException(msg) from None


if __name__ == "__main__":
    jira_srv = JiraService()

    testcase_file = "../../../sample/testcases.json"
    testcases = JiraService.read_testcases_from_file(testcase_file)
    jira_srv.create_or_update_testcases_by_name(testcases)

    testcycle_file = "../../../sample/testcycles.json"
    testcases = JiraService.read_testcases_from_file(testcycle_file)
    jira_srv.create_test_cycle(testcases)



