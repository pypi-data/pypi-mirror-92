# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odoo_backup_db_cli', 'odoo_backup_db_cli.protocols']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata==1.7.0',
 'pysftp>=0.2.9,<0.3.0',
 'python-dateutil>=2.8,<3.0',
 'yaspin>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['odoo-backup-db-cli = odoo_backup_db_cli.cli:main',
                     'poetry = poetry.console:run']}

setup_kwargs = {
    'name': 'odoo-backup-db-cli',
    'version': '1.0.0',
    'description': 'Tool to create full backup of odoo database',
    'long_description': '# odoo-backup-db-cli\n\n[![Build Status](https://github.com/ventor-tech/odoo-backup-db-cli/workflows/test/badge.svg?branch=main&event=push)](https://github.com/ventor-tech/odoo-backup-db-cli/actions?query=workflow%3Atest)\n[![Python Version](https://img.shields.io/pypi/pyversions/odoo-backup-db-cli.svg)](https://pypi.org/project/odoo-backup-db-cli/)\n[![Documentation Status](https://readthedocs.org/projects/odoo-backup-db-cli/badge/?version=latest)](https://odoo-backup-db-cli.readthedocs.io/en/latest/?badge=latest)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nTool to create full backup of odoo database\n\n## Features\n\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n- Add yours!\n\n## Installation\n\n```bash\npip install odoo-backup-db-cli\n```\n\n## Example creating cron\n\nLet\'s say you want to create cron each minute create backup and you have a conda environment.\nThen you need:\n\n1. Copy snippet appended by Anaconda in `~/.bashrc` (at the end of the file) to a separate file `~/.bashrc_conda`\n\n    As of Anaconda 2020.02 installation, the snippet reads as follows:\n\n    ```bash\n    # >>> conda initialize >>>\n    # !! Contents within this block are managed by \'conda init\' !!\n    __conda_setup="$(\'/home/USERNAME/anaconda3/bin/conda\' \'shell.bash\' \'hook\' 2> /dev/null)"\n    if [ $? -eq 0 ]; then\n        eval "$__conda_setup"\n    else\n        if [ -f "/home/USERNAME/anaconda3/etc/profile.d/conda.sh" ]; then\n            . "/home/USERNAME/anaconda3/etc/profile.d/conda.sh"\n        else\n            export PATH="/home/USERNAME/anaconda3/bin:$PATH"\n        fi\n    fi\n    unset __conda_setup\n    # <<< conda initialize <<<\n    ```\n\n    Make sure that:\n\n    - The path `/home/USERNAME/anaconda3/` is correct.\n    - The user running the cronjob has read permissions for `~/.bashrc_conda` (and no other user can write to this file).\n\n2. In `crontab -e` add lines to run cronjobs on `bash` and to source `~/.bashrc_conda`\n\n    Run `crontab -e` and insert the following before the cronjob:\n\n    ```bash\n    SHELL=/bin/bash\n    BASH_ENV=~/.bashrc_conda\n    ```\n\n3. In `crontab -e` include at beginning of the cronjob `conda activate my_env;` as in example\n\n    Example of entry for a script that would execute at noon 12:30 each day on the Python interpreter within the conda environment:\n\n    ```bash\n    30 12 * * * conda activate my_env; odoo-backup-db-cli create-backup production_local_with_filestore; conda deactivate\n    ```\n\nAnd that\'s it.\n\nYou may want to check from time to time that the snippet in `~/.bashrc_conda` is up to date in case conda updates its snippet in `~/.bashrc`.\n\n## License\n\n[agpl3](https://github.com/ventor-tech/odoo-backup-db-cli/blob/master/LICENSE)\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [88c80f5d17a6f4bc41dbc5473db4f5ffd2b3068f](https://github.com/wemake-services/wemake-python-package/tree/88c80f5d17a6f4bc41dbc5473db4f5ffd2b3068f). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/88c80f5d17a6f4bc41dbc5473db4f5ffd2b3068f...master) since then.\n',
    'author': 'VentorTech OU',
    'author_email': 'hello@ventor.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ventor-tech/odoo-backup-db-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
