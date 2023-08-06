# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schematic',
 'schematic.manifest',
 'schematic.manifest.examples',
 'schematic.models',
 'schematic.models.examples',
 'schematic.schemas',
 'schematic.schemas.examples',
 'schematic.store',
 'schematic.store.examples',
 'schematic.utils',
 'schematic.utils.examples']

package_data = \
{'': ['*'],
 'schematic': ['etc/*', 'etc/data_models/*', 'etc/validation_schemas/*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'click-log>=0.3.2,<0.4.0',
 'click>=7.1.2,<8.0.0',
 'fastjsonschema>=2.14.5,<3.0.0',
 'google-api-python-client>=1.12.8,<2.0.0',
 'google-auth-httplib2>=0.0.4,<0.0.5',
 'google-auth-oauthlib>=0.4.2,<0.5.0',
 'graphviz>=0.16,<0.17',
 'inflection>=0.5.1,<0.6.0',
 'jsonschema>=3.2.0,<4.0.0',
 'networkx>=2.5,<3.0',
 'orderedset>=2.0.3,<3.0.0',
 'pandas>=1.2.1,<2.0.0',
 'pygsheets>=2.0.4,<3.0.0',
 'rdflib>=5.0.0,<6.0.0',
 'synapseclient>=2.2.2,<3.0.0',
 'tabletext>=0.1,<0.2']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['schematic = schematic.__main__:main']}

setup_kwargs = {
    'name': 'schematic-test',
    'version': '0.1.11',
    'description': 'Package for data model and data ingress management',
    'long_description': "# Schematic\n\n## Usage\n\n### Virtual Environment Setup\n\nPython 3 has built-in support for virtual environments (using `venv` module). Perform the following steps:\n\nAfter cloning the git repository, navigate into the `schematic` directory and run the command as below:\n\n```bash\npython[3] -m venv .venv\n```\n\n_Note: It is assumed that you are running all the below commands from the main/root (`schematic`) directory._\n\nThis creates a Python3 virtual environment (within the `root` folder/package), with its own site directories (isolated from the system site directories).\n\nTo activate the virtual environment, run:\n\n```bash\nsource .venv/bin/activate\n```\n\n_Note: You should now see the name of the virtual environment to the left of the prompt._\n\n### Install App/Package\n\nTo install the package/bundle/application:\n\n```bash\npip[3] install -e .\n```\n\nTo verify that the package has been installed (as a `pip` package), check here:\n\n```bash\npip[3] list\n```\n\nNow, your environment is ready to test the modules within the application.\n\nOnce you have finished testing the application within the virtual environment and want to deactivate it, simply run:\n\n```bash\ndeactivate\n```\n\nTo run any of the example file(s), go to your root directory and execute/run python script in the following way:\n\nLet's say you want to run the `metadata_usage` example - then do this:\n\n```bash\npython[3] examples/metadata_usage.py\n```\n\n### Configure Synapse Credentials\n\nDownload a copy of the `credentials.json` file (or the file needed for authentication using service account, called `quickstart-1560359685924-198a7114b6b5.json`) stored on Synapse, using the synapse client command line utility. The credentials file is necessary for authentication to use Google services/APIs. To do so:\n\n\n_Note: Make sure you have `download` access/permissions to the above files before running the below commands._\n\nFor `credentials.json` file:\n```bash\nsynapse get syn21088684\n```\n\nFor `quickstart-1560359685924-198a7114b6b5.json` file:\n```bash\nsynapse get syn22316486\n```\n\nFind the synapse configuration file (_`.synapseConfig`_) downloaded to the current source directory. Access it like this:\n\n```bash\nvi[m] .synapseConfig\n```\n\nOpen the config file, and under the authentication section, replace _< username >_ and _< apikey >_ with your Synapse username and API key.\n\n_Note: You can get your Synapse API key by: **logging into Synapse > Settings > Synapse API Key > Show API Key**_.\n\n----\n\n### Contribution\n\nClone a copy of the repository by executing the command as below:\n      \n```bash\ngit clone --single-branch --branch develop https://github.com/Sage-Bionetworks/schematic.git\n```\n\n1. Fork the repository.\n2. Clone the forked repository.\n3. Create a branch with a descriptive name that includes the name of the feature under development.\n4. Push your changes to that branch.\n5. PR into a branch that is developing the same feature on the `schematic` main repository.\n\nFor further reference, please consult [CONTRIBUTION.md](https://github.com/Sage-Bionetworks/schematic/blob/develop/CONTRIBUTION.md).",
    'author': 'Milen Nikolov',
    'author_email': 'milen.nikolov@sagebase.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Sage-Bionetworks/schematic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
