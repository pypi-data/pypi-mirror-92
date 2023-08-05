# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kfp_deployer']

package_data = \
{'': ['*']}

install_requires = \
['kfp>=1.3.0,<2.0.0', 'pytz>=2020.5,<2021.0']

entry_points = \
{'console_scripts': ['kfp-deploy = kfp_deployer.main:main']}

setup_kwargs = {
    'name': 'kfp-deployer',
    'version': '0.1.0',
    'description': 'Deploy the KFP ML Pipeline from CLI.',
    'long_description': '# kfp-deployer\n\nDeploy your ml-pipeline with `kfp-deploy` from cli.\n\n## How to use\n\n`kfp-deploy https://your-kubeflow-host/ "pipeline-name" ./pipeline_file.yaml`\n\nfor more detail, see `kfp-deploy -h`.\n\n## what the difference from `kfp pipeline upload`?\n\n\nKubeflow Pipelines requires the all pipelines must have unique names. \nOtherwise you have to use `update the version` instead of `upload the pipeline`.\nFurthermore, you have to use unique name when uploading the new version of pipeline.\n\nThis command does everything required in the upload process for you. \nThis command will communicate with kfp host and automatically determine \nwhether update or upload is required and perform it.\nFurthermore, the version string is automatically generated based on the upload timestamp.\n',
    'author': 'Karno',
    'author_email': 'karnoroid@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/reproio/kfp-deployer',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
