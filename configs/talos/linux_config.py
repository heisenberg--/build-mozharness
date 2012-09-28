import os
import socket

PYTHON = '/tools/buildbot/bin/python'
VENV_PATH = '/home/cltbld/talos-slave/test/build/venv'

config = {
    "log_name": "talos",
    "buildbot_json_path": "buildprops.json",
    "installer_path": "installer.exe",
    "virtualenv_path": VENV_PATH,
    "pypi_url": "http://puppetagain.pub.build.mozilla.org/data/python/packages/",
    "find_links": ["http://puppetagain.pub.build.mozilla.org/data/python/packages/"],
    "use_talos_json": True,
    "exes": {
        'python': PYTHON,
        'virtualenv': [PYTHON, '/tools/misc-python/virtualenv.py'],
    },
    "title": os.uname()[1].lower().split('.')[0],
    "results_url": "http://graphs.mozilla.org/server/collect.cgi",
    "default_actions": [
        "clobber",
        "read-buildbot-config",
        "pull",
        "download-and-extract",
        "create-virtualenv",
        "install",
        "generate-config",
        "run-tests",
    ],
    "repos": [{"repo": "http://hg.mozilla.org/build/tools",}],
    "python_webserver": False,
    "webroot": '/home/cltbld/talos-slave/talos-data',
    "populate_webroot": True,
}
