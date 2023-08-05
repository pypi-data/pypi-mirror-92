# Teko CLI Tools

This is a Python package that contains some classed and CLI tools to be used during development 
process at Teko Vietnam (https://teko.vn).

List of tools:

- Teko Jira Tools
- Teko pytest test report fixture (coming soon)
- Teko CodeSignal Tournament Result Fetching (coming soon) 
- More to come...

## Installation 

To use this tools, Python 3.6+ should be instaled. 

Instal and/or upgrade to the latest version:

```shell
$ pip install --upgrade teko-cli
```

After successul installation, you should be able to use `teko` command in your 
console terminal:

```
$ teko
```

You should see this kind of help message:

```
Usage: teko [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  cs
  jira
``` 

## Using Teko Jira tool

### Configure Jira credential 

This tool use user/pass authentication to Jira server, and working with one Jira project 
at the same time. Jira server authentication uses 4 environment variables below. 
You can set these variables to the your environment, or save it to `.env` file in working
directory:

Sample content of `.env` file:

```
export JIRA_SERVER=jira.teko.vn
export JIRA_USERNAME=thuc.nc
export JIRA_PASSWORD=sample_password
export JIRA_PROJECT_KEY=TESTING
```

### Submit (create) list of testcases to a Jira Project

To push testcases to a Jira Project, you should prepare a `.yaml` 
or a `.json` file, containing list of testcases to be created in Jira, 
then use following command:

```
$ teko jira create-tests {testcase_file}
```

To see help message, use `--help` option: `teko jira create-tests --help`:

```
Usage: teko jira create-tests [OPTIONS] FILE



Arguments:
  FILE  The name of a testcase definition file  [required]

Options:
  --help  Show this message and exit.
```

**Note** that this tool use test case `name` as key, so existing tests with same `name` 
will be updated with latest information. 

#### Sample testcases file

- `.yaml` file

```yaml
- name: Testcase 01
  issueLinks: [TESTING-4]
  objective: Test 01 Objective
  precondition: Test 01 Precondition
  testScript:
    type: PLAIN_TEXT
    text: >
      - init x and y <br/>
      - call func add(x, y)
- name: Testcase 02
  issueLinks: [TESTING-4, TESTING-5]
  objective: Test 02 Objective
  precondition: Test 02 Precondition
  priority: Normal
  status: Draft
  testScript:
    type: STEP_BY_STEP
    steps:
    - description: Step 1
      testData: <code>(x,y) = (1,3)</code>
      expectedResult: <strong>4</strong>
    - description: Step 2
      testData: <code>(x,y) = (4,5)</code>
      expectedResult: <strong>9</strong>
```

- Equivalent `.json` file:

```json
[
  {
    "name": "Testcase 01",
    "issueLinks": [
      "TESTING-4"
    ],
    "objective": "Test 01 Objective",
    "precondition": "Test 01 Precondition",
    "testScript": {
      "type": "PLAIN_TEXT",
      "text": "- init x and y <br/> - call func add(x, y)\n"
    }
  },
  {
    "name": "Testcase 02",
    "issueLinks": [
      "TESTING-4",
      "TESTING-5"
    ],
    "objective": "Test 02 Objective",
    "precondition": "Test 02 Precondition",
    "priority": "Normal",
    "status": "Draft",
    "testScript": {
      "type": "STEP_BY_STEP",
      "steps": [
        {
          "description": "Step 1",
          "testData": "<code>(x,y) = (1,3)</code>",
          "expectedResult": "<strong>4</strong>"
        },
        {
          "description": "Step 2",
          "testData": "<code>(x,y) = (4,5)</code>",
          "expectedResult": "<strong>9</strong>"
        }
      ]
    }
  }
]
```

### Create test cycle (testrun result) in a Jira Project

To create a testrun report (cycle) to a Jira Project, you should prepare a `.yaml` 
or a `.json` file, containing list of testcases and **their result** to be created 
in Jira, then use following command:

```
$ teko jira create-cycle {testcase_file}
```

The testcase file stuctures are the same as above, with following additional fields 
for test result:

```
testrun_status: Pass
testrun_environment: Dev
testrun_comment: The test has failed on some automation tool procedure
testrun_duration: 300000 #ms
testrun_date: "2020-12-12T14:54:00Z" # put datetime inside double quotes to avoid parsing
``` 

#### Sample testrun (cycle) file

- `.yaml` file

```yaml
- name: Testcase 01
  testrun_status: Pass
  testrun_environment: Dev
  testrun_comment: The test has failed on some automation tool procedure
  testrun_duration: 300000 #ms
  testrun_date: "2020-12-12T14:54:00Z" 
- name: Testcase 02
  testrun_status: Fail
  testrun_environment: Test1
  testrun_comment: The test has failed on some automation tool procedure
  testrun_duration: 30000 #ms
  testrun_date: "2020-12-12T14:54:00Z"
```

- Equivalent `.json` file

```json
[
  {
    "name": "Testcase 01",
    "testrun_status": "Pass",
    "testrun_environment": "Dev",
    "testrun_comment": "The test has failed on some automation tool procedure",
    "testrun_duration": 300000,
    "testrun_date": "2020-12-12T14:54:00Z"
  },
  {
    "name": "Testcase 02",
    "testrun_status": "Fail",
    "testrun_environment": "Test1",
    "testrun_comment": "The test has failed on some automation tool procedure",
    "testrun_duration": 30000,
    "testrun_date": "2020-12-12T14:54:00Z"
  }
]
```

Please **note** that the files use **same structure** as in case of creating testcases above,
with additional fields, and also uses testcase `name` as key in Jira. 
So you can you a single combined file for both operation: create tests and create cycles. 
This file can be **generated automatically** from *docstrings* and/or 
*annotation* / *decorator* in auto test code.

### Sample combined testcase file with test results

- `.yaml` file

```yaml
- name: Testcase 01
  issueLinks: [TESTING-4]
  objective: Test 01 Objective
  precondition: Test 01 Precondition
  testScript:
    type: PLAIN_TEXT
    text: >
      - init x and y <br/>
      - call func add(x, y)
  testrun_status: Pass
  testrun_environment: Dev
  testrun_comment: The test has failed on some automation tool procedure
  testrun_duration: 300000 #ms
  testrun_date: "2020-12-12T14:54:00Z" 
- name: Testcase 02
  issueLinks: [TESTING-4, TESTING-5]
  objective: Test 02 Objective
  precondition: Test 02 Precondition
  priority: Normal
  status: Draft
  testScript:
    type: STEP_BY_STEP
    steps:
    - description: Step 1
      testData: <code>(x,y) = (1,3)</code>
      expectedResult: <strong>4</strong>
    - description: Step 2
      testData: <code>(x,y) = (4,5)</code>
      expectedResult: <strong>9</strong>
  testrun_status: Fail
  testrun_environment: Test1
  testrun_comment: The test has failed on some automation tool procedure
  testrun_duration: 30000 #ms
  testrun_date: "2020-12-12T14:54:00Z"
```   

- Equivalent `.json` file

```json
[
  {
    "name": "Testcase 01",
    "issueLinks": [
      "TESTING-4"
    ],
    "objective": "Test 01 Objective",
    "precondition": "Test 01 Precondition",
    "testScript": {
      "type": "PLAIN_TEXT",
      "text": "- init x and y <br/> - call func add(x, y)\n"
    },
    "testrun_status": "Pass",
    "testrun_environment": "Dev",
    "testrun_comment": "The test has failed on some automation tool procedure",
    "testrun_duration": 300000,
    "testrun_date": "2020-12-12T14:54:00Z"
  },
  {
    "name": "Testcase 02",
    "issueLinks": [
      "TESTING-4",
      "TESTING-5"
    ],
    "objective": "Test 02 Objective",
    "precondition": "Test 02 Precondition",
    "priority": "Normal",
    "status": "Draft",
    "testScript": {
      "type": "STEP_BY_STEP",
      "steps": [
        {
          "description": "Step 1",
          "testData": "<code>(x,y) = (1,3)</code>",
          "expectedResult": "<strong>4</strong>"
        },
        {
          "description": "Step 2",
          "testData": "<code>(x,y) = (4,5)</code>",
          "expectedResult": "<strong>9</strong>"
        }
      ]
    },
    "testrun_status": "Fail",
    "testrun_environment": "Test1",
    "testrun_comment": "The test has failed on some automation tool procedure",
    "testrun_duration": 30000,
    "testrun_date": "2020-12-12T14:54:00Z"
  }
]
```