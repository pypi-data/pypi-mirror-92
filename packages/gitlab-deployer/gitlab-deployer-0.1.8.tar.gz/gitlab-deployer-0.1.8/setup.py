# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deployer']

package_data = \
{'': ['*']}

install_requires = \
['Click>=7.0,<8.0', 'python-gitlab>=1.15,<2.0', 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['deployer = deployer.main:cli']}

setup_kwargs = {
    'name': 'gitlab-deployer',
    'version': '0.1.8',
    'description': 'GitLab Deployer',
    'long_description': '# GitLab deployer \xf0\x9f\x9a\x80\n\n\n## Installation\n\n```\npip install gitlab-deployer\n```\n\n## Usage \n\n```\ndeployer <command> <arguments>\n```\nCommands:\n\n```\n  deploy       - start deploy daemon \n  download     - download single artifact \n```\n\nArguments:\n\n```\ndeploy\n\nOptions:\n  --url TEXT             GitLab url\n  --private_token TEXT   GitLab private token\n  --project_id INTEGER   Project id\n  --slack_web_hook TEXT  Slack web hook api\n  --slack_channel TEXT   Slack channel (#deploy)\n  --slack_username TEXT  Slack channel\n  --deploy_script TEXT   Execute after download and unpack artifact\n                         (./deploy.sh)\n  --last_job_file TEXT   Last job file (last.txt)\n  --interval INTEGER     Pull interval (5)\n  --error_sleep INTEGER  Sleep on error (25)\n  --verbosity TEXT       Verbosity (log.level=DEBUG)\n  --ref TEXT             Git Branch\n  --web_url TEXT         HTTP GET web hook\n  --result_script TEXT   Result shell script. Execute after deployment.\n  --test_slack           Test Slack Send Info\n  --help                 Show this message and exit.\n\n\ndownload\n\nOptions:\n  --url TEXT            GitLab url\n  --private_token TEXT  GitLab private token\n  --project_id INTEGER  Project id\n  --verbosity TEXT      Verbosity (log.level=DEBUG)\n  --ref TEXT            Git Branch\n  --help                Show this message and exit.\n\n```\n\n\n\n\n## Example\n\nCommand line\n```\n\ndeployer deploy --ref master \\\n\t--slack_web_hook=https://hooks.slack.com/services/xxxxxx/yyyyyy/zzzzzzzzzzzzz \\\n\t--slack_channel="#deploy"  --slack_username="deploy-user"  --url http://gitlab.com \\\n\t--private_token=tttttttttttttt --project_id=00\n\n```\n\nsystem.d example\n\n```\n[Unit]\nDescription=Deployer Service\n\n[Service]\nExecStart=deployer deploy --ref master \\\n\t--slack_web_hook=https://hooks.slack.com/services/xxxxxx/yyyyyy/zzzzzzzzzzzzz \\\n\t--slack_channel="#deploy"  --slack_username="deploy-user"  --url http://gitlab.com \\\n\t--private_token=tttttttttttttt --project_id=00\n\n\nRestart=always\nWorkingDirectory=/myproject/\nStandardOutput=syslog\nStandardError=syslog\n\n[Install]\nWantedBy=default.target\n```\n\ndeploy.sh \n\n```\n#!/bin/bash\n\nunzip ./artifacts.zip\nmv ./simple-java-project/target/simple-java-project.jar ./\nsystemctl restart simplejavaproject\n\necho "OK"\n```\n\n## Develop\n\nUsing [poetry](https://python-poetry.org/)\n\n```\ncd ./gitlab-deployer/\npoetry install\n```\n\nRun with poetry\n```\npoetry run deployer <command> <args>\n\npoetry run deployer deploy --help\n```\n\n\nEnjoy!',
    'author': 'Dmitry Vysochin',
    'author_email': 'dmitry.vysochin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/veryevilzed/gitlab-deployer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
