from dataclasses import dataclass, field
from typing import List, Union

from dataclasses_json import dataclass_json
from typer.models import NoneType


@dataclass_json
@dataclass
class JiraTestScriptStep:
    # id: str = ""
    # index: int = 0
    description: str = ""
    testData: str = ""
    expectedResult: str = ""


@dataclass_json
@dataclass
class JiraTestScript:
    id: str = ""
    text: str = ""
    type: str = "PLAIN_TEXT"  # PLAIN_TEXT | STEP_BY_STEP
    steps: List[JiraTestScriptStep] = field(default_factory=list)


@dataclass_json
@dataclass
class JiraTestcase:
    # owner: str = ""
    id: int = 0
    key: str = ""
    projectKey: str = ""
    name: str = ""
    folder: str = ""
    status: str = "Draft"  # Approved | Draft
    # lastTestResultStatus: str = ""
    priority: str = "Normal"
    # createdOn: str = ""
    # createdBy: str = ""
    objective: str = ""
    precondition: str = ""
    testScript: Union[JiraTestScript, NoneType] = None
    issueLinks: List[str] = field(default_factory=list)
    confluenceLinks: List[str] = field(default_factory=list)
    webLinks: List[Union[str, dict]] = field(default_factory=list)
    # parameters: dict = None

    # test result fields
    testrun_folder: str = ""
    testrun_status: str = ""
    testrun_environment: str = ""
    testrun_comment: str = ""
    testrun_duration: str = ""  # 183000
    testrun_date: str = ""  # 2020-12-12T14:54:00Z


@dataclass_json
@dataclass
class JiraTestCycle:
    projectKey: str = ""
    name: str = ""
    description: str = ""
    items: List[JiraTestcase] = field(default_factory=list)
