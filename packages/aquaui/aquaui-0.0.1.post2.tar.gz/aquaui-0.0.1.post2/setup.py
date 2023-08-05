# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aquaui', 'aquaui.notification', 'aquaui.types']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aquaui',
    'version': '0.0.1.post2',
    'description': 'Native Mac OS UI elements with python',
    'long_description': '<h1 align="center">\n  <img src="https://raw.githubusercontent.com/ninest/aquaui/master/assets/icon.svg" width=155>\n  <br>\n  aquaui\n</h1>\n\n<p align="center">\nDisplay native dialogs, alerts, notifications, color pickers, and more with Python\n</p>\n\n<p align="center">\n  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/ninest/aquaui/Run%20tests?style=flat-square">\n\n  <a href="https://pypi.org/project/aquaui/">\n    <img src="https://img.shields.io/pypi/v/aquaui?color=blue&style=flat-square" alt="Version" />\n  </a>\n  <a href="https://pypi.org/project/aquaui/">\n    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/aquaui?color=red&style=flat-square" />\n  </a>\n\n  <img src="https://img.shields.io/github/license/ninest/aquaui?style=flat-square" alt="MIT" />\n\n  <a href="https://www.buymeacoffee.com/ninest">\n    <img src="https://img.shields.io/badge/Donate-Buy%20Me%20A%20Coffee-orange.svg?style=flat-square" alt="Buy Me A Coffee">\n  </a>\n</p>\n\n**💥 This library is still a work in progress.**\n\n## Useful links\n\n- [Documentation](https://github.com/ninest/aquaui/tree/master/docs)\n- [Examples](https://github.com/ninest/aquaui#examples)\n- [Discussions](https://github.com/ninest/aquaui/discussions)\n\n## Features\n\n- [x] Display dialogs\n  - [x] Dialog prompts\n  - [x] Icon support\n- [x] Alerts\n- [x] Choice dialogs\n- [ ] Notifications\n  - [x] Customize title, subtitle, and informational text\n  - [x] Customize icon\n  - [x] Schedulable\n  - [ ] Callbacks (button pressed, reply text) – [relevant stackoverflow answer](https://stackoverflow.com/a/62248246/8677167)\n  - [x] Fallback (AppleScript) notifications\n- [ ] Color picker\n- [ ] File/folder picker\n\n## Documentation\n\n[**Find the documentation in the `docs/` folder**](https://github.com/ninest/aquaui/tree/master/docs)\n\n## Examples\n\nSee the `examples/` directory. Feel free to make a pull request to add more examples.\n\n**Show a dialog with the buttons "Go" (default) and "No" (to cancel) with the caution icon:**\n\n```py\nfrom aquaui import Dialog, Buttons, Icon\n\nbuttons = Buttons(["Go", "No"], default_button="Go", cancel_button="No")\nresult = Dialog("Hello!").with_buttons(buttons).with_icon(Icon.CAUTION).show()\n```\n\n**Execute functions based on the button clicked:**\n\n```py\nfrom aquaui import Dialog, Buttons\n\nbutton_one = "One"\nbutton_two = "Two"\nbuttons = Buttons([button_one, button_two])\n\nresult = Dialog("Press a button").with_buttons(buttons).show()\n\nif result.button_returned == button_one:\n  print("Button One was pressed")\nelif result.button_returned == button_two:\n  print("Button Two was pressed")\n```\n\n**Display a choice dialog with the options "Netflix" and "Prime Video"**\n\n```py\nfrom aquaui import Choice\n\nprovider = Choice("Choose the streaming platform").with_choices(["Netflix", "Prime Video"]).show()\nprint(provider)\n```\n\nIf this example interests you, check out my other library [Flixpy](https://github.com/ninest/flixpy).\n\n**Display a notification:**\n\nWarning: please read the [documentation](./docs/3-notification.md) before using notifications. There are additional dependencies to install.\n\n```py\nfrom aquaui.notification.native_notification import Notification\n\nnotification = (\n    Notification("Hello!")\n    .with_subtitle("This is the subtitle!")\n    .with_informative_text("Isn\'t this informative?")\n    .with_identity_image("assets/folder.png")  # the image on the right of the notification\n    .send()\n)\n```\n\n**Schedule a notification:**\n\n```py\nfrom aquaui.notification.native_notification import Notification\n\nnotification = Notification("Your pizza is here!").with_delay(15).send()\n# 15 seconds delay\n```\n\n## Build setup\n\nClone or fork the repository, then run\n\n```bash\npoetry shell\n\npoetry install\npre-commit install\n```\n\nMake changes, then run tests with\n\n```bash\npytest tests\n```\n\nEnsure that all tests pass.\n\n<details>\n<summary>\nRecommended editor settings\n</summary>\n\n```json\n{\n  "python.formatting.provider": "black",\n  "editor.formatOnSave": true,\n  "[python]": {\n    "editor.insertSpaces": true,\n    "editor.detectIndentation": false,\n    "editor.tabSize": 4\n  },\n  "python.linting.enabled": true,\n  "python.linting.flake8Enabled": true,\n  "python.linting.pylintEnabled": false,\n  "python.pythonPath": "/Users/yourusername/.../aquaui-UIHDsdfS-py3.7"\n}\n```\n\n</details>\n\n## License\n\nMIT\n',
    'author': 'ninest',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ninest/aquaui/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
