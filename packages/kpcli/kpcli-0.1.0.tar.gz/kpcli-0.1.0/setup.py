# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kpcli']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.3.0,<21.0.0',
 'pykeepass>=3.2.1,<4.0.0',
 'pyperclip>=1.8.1,<2.0.0',
 'tableformatter>=0.1.5,<0.2.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['kpcli = kpcli.kp:app']}

setup_kwargs = {
    'name': 'kpcli',
    'version': '0.1.0',
    'description': 'A simple command line tool to interact with KeePassX databases',
    'long_description': '# kpcli\n\nA simple command line tool to interact with KeePassX databases.\n\n[KeePassX](https://www.keepassx.org/) is a cross platform password management application.\nIt is available as a GUI application for MacOSX, Linux and Windows and as an Android app (KeePassDroid), \nmaking it useful to manage passwords across multiple devices.\n\n### Features\n- View details: list groups and entries, get details for a single entry\n- Add new entries and change passwords from the commandline\n- Resolve conflicts: users may choose to keep their KeePassX database in a central location\nsuch as Dropbox or other synchronisation software.  This results in "conflicting copies" being generated if \na opens and updates the database from more than one device.  **kpcli** avoids these conflicts, and also provides \na utility to compare conflicting copies and identify where the conflicts lie.\n\n## Installation\n\nUsing pip:\n\n```pip install kpcli```\n\nFrom source:\n\n```\ngit clone https://github.com/rebkwok/kpcli.git\ncd kpcli\npoetry install\n```\n\n## Configuration\n\n**kpcli** will look for database configuration first in a config.ini file, and if \none is not found, in environment variables.\n\n**NOTE:** \nAT YOUR OWN RISK! `KEEPASSDB_PASSWORD` can be set in the config.ini file or as an environment variable if you really want to.\nNot advised unless you implement some method of encrypting and retrieving it before passing to **kpcli**.  If no `KEEPASSDB_PASSWORD`\nis found, **kpcli** will prompt for it.\n\n### Config file \n\nCreate a config file at $(HOME)/.kp/config.ini, with at least a default profile, and your\ndatabase location and credentials:\n```\n[default]\nKEEPASSDB=/Users/me/mypassworddb.kdbx\n```\n\nIf your database uses a key file, provide that location too:\n```\n[default]\nKEEPASSDB=/path/to/mypassworddb.kdbx\nKEYPASSDB_KEYFILE=/path/to/mykeyfile.key\n```\n\nMore than one profile can be set for multiple databases, and switched with the `-p` flag\n```\n[default]\nKEEPASSDB=/path/to/db.kdbx\nKEYPASSDB_KEYFILE=/path/to/mykeyfile.key\n\n[work]\nKEEPASSDB=/path/to/workdb.kdbx\n```\n\n### Environment Variables\nIf no config.ini file exists, **kpcli** will attempt to find config in the environment variables \n`KEEPASSDB`, `KEYPASSDB_KEYFILE` and `KEEPASSDB_PASSWORD` (falling back to a prompt for the password).\n\n\n### Usage Examples ###\n\nList groups and entries\n```console\n$kpcli ls\n\nDatabase: /path/to/db.kdbx\n================================================================================\nGroups\n================================================================================\nRoot\nInternet\nCommunications\n...\n\n$kpcli ls --group comm --entries\nDatabase: /path/to/db.kdbx\n================================================================================\nCommunications\n================================================================================\nmy email\nwork email\n...\n```\n\nList groups in the database from the "work" profile:\n```console\n$kpcli --profile work ls\nDatabase: /path/to/workdb.kdbx\n================================================================================\nGroups\n================================================================================\nRoot\nWork\n...\n```\n\nGet an entry  \nBy group and entry title, separated with /.  Note partial matches are allowed.  \nIf multiple matching entries are found, all will be listed.\n```console\n$kpcli get comm/email\nDatabase: /path/to/db.kdbx\n================================================================================\nCommunications/my email\n================================================================================\nname: Communications/my email\nusername: my@email.com\npassword: **********\nURL:\nNotes: This is my main email address\n```\n\nCopy an attribute (default password) from an entry to the clipboard  \nIf multiple entries match, kpcli prompts for a selection.\n```console\n$kpcli cp comm/email\nEntry: Communications/my email\npassword copied to clipboard\n\n$kpcli cp comm/email username\nEntry: Communications/my email\nusername copied to clipboard\n```\n\nAdd an entry\n```console\n$kpcli add\n```\n**kpcli** will prompt for required fields.\n\n\nChange a password\n```console\n$kpcli change-password comm/email\n```\n**kpcli** will prompt for new password.\n\n\nFor more detailed usage, use `--help` with any kpcli command listed below.\n\n**Usage**:\n\n```console\n$ kpcli [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n* `-p, --profile TEXT`: Specify config profile to use  [default: default]\n* `--loglevel TEXT`: [default: INFO]\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n\n**Commands**:\n\n* `ls`: List groups and entries\n* `get`: Fetch details for a single entry\n* `cp`: Copy entry attribute to clipboard\n* `add`: Add a new entry\n* `change-password`: Change entry password\n* `compare`: Compare potentially conflicting copies of a KeePassX Database and report conflicts\n\n\n\n\n',
    'author': 'Becky Smith',
    'author_email': 'rebkwok@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
