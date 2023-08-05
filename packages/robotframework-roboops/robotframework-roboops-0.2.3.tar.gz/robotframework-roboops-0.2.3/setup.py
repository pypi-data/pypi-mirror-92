# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['RoboOps']

package_data = \
{'': ['*']}

install_requires = \
['robotframework>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'robotframework-roboops',
    'version': '0.2.3',
    'description': "Robot Framework's library for creating and running DevOps tasks easily and efficiently.",
    'long_description': '# robotframework-roboops\n\nRobot Framework\'s library for creating, sharing and running DevOps tasks easily and efficiently.\n\nBuilding pipelines with Robot Framework gives developers clear insight what CI/CD steps do\n(thanks to keyword based syntax). Allow them to execute pipelines easily also on their own machines\nbefore pushing to repository and waiting for CI/CD tool to take it up.\n\nThanks to nice RFWK reporting it should be easy and fast to follow pipelines and investigate issues.\n\n----\nPrimarly designed for testers/developers who use Robot Framework.\nThey often create own python libraries and must maintain them.\n\n\nBut it\'s not limited only to that - you can automate any stuff with it - with syntax you know and reports you love.\n\n# Features\n- uses robotframework for running tasks - see all the benefits of robotframework\n    - one that brings a lot of benefits are report and log files\n- keyword for running commands\n- keyword for linking artifacts into report metadata\n- any failure makes remaining tasks to fail automatically (skip)\n- others to come - raise your idea!\n\n# Installation instructions\npip install robotframework-roboops\n\n# Usage\nRoboOps is typical Robotframework library - use it as usual robot library.\n\nAs this library is mainly focused on running tasks instead of tests,\ntry to use `*** Tasks ***` instead of `*** Test Cases ***` in `.robot` files.\n\nThis repository uses RoboOps for building, testing (and in future deploying) itself.\nSee pipeline.robot to see example how to do it.\n\nThis repository uses github actions - check this out to see how to use it in CI pipeline.\n\n## Example\n```RobotFramework\n*** Settings ***\nLibrary    RoboOps\nLibrary    OperatingSystem\n\n*** Variables ***\n${atest dir}     ${CURDIR}/atest    \n&{install python env}    command=poetry install\n&{unit tests}    command=poetry run coverage run --source=RoboOps -m pytest .\n&{report coverage}    command=poetry run coverage report -m --fail-under=80\n&{generate wheel}    command=poetry build\n&{remove stale roboops package from atest env}    command=poetry remove robotframework-roboops    cwd=${atest dir}    ignore_rc=True\n&{install atest env}    command=poetry install    cwd=${atest dir}   \n&{install atest roboops package from whl}    command=poetry add ../    cwd=${atest dir}\n\n*** Tasks ***\nUnit Test Stage\n    Roboops Run Command    &{install python env}\n    Roboops Run Command    &{unit tests}\n    Create Coverage Report And Save It\n    \nBuild Package Stage\n    Roboops Run Command    &{generate wheel}\n    \nAcceptance Test Stage\n    Roboops Run Command    &{remove stale roboops package from atest env}\n    Roboops Run Command    &{install atest env}\n    Roboops Run Command    &{install atest roboops package from whl}\n    Roboops Run Command    &{run atests}\n    [Teardown]    Save Acceptance Tests Artifacts\n\n*** Keywords ***\nCreate Coverage Report And Save It\n    ${coverage}    Roboops Run Command    &{report coverage}\n    Create File    coverage.log    ${coverage.stdout.decode()}\n    Roboops Save File Artifact    coverage.log    coverage.log\n\nSave Acceptance Tests Artifacts\n    Roboops Save File Artifact    ${atest dir}/log.html    atest_log.html\n    Roboops Save File Artifact    ${atest dir}/report.html    atest_report.html\n    Roboops Save File Artifact    ${atest dir}/output.xml    atest_output.xml\n\n```\n# Running tests\nTest everything (unit tests, acceptance tests, building wheel) by running:\n```\nrobot pipeline.robot\n```\n \n## running pipeline with docker (using python 3.6)\nbuild docker image and run it:\n```\ndocker build -t roboops:latest .\ndocker run --user $(id -u):$(id -g) --rm -v "${PWD}":/code --env PYTHONPATH=. roboops:latest\n```\n\n# Security considerations\nBe aware that secrets provided in environment variables may be logged by Task (e.g. with `Log` keyword).\n\nSo don\'t provide secrets into steps where .robot file is executed for commits without any reviewers approval.\n',
    'author': 'Łukasz Sójka',
    'author_email': 'soyacz@gmail.com',
    'maintainer': 'Łukasz Sójka',
    'maintainer_email': 'soyacz@gmail.com',
    'url': 'https://github.com/soyacz/robotframework-roboops/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
