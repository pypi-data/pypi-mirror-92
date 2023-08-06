# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arachnys_api_client']

package_data = \
{'': ['*']}

install_requires = \
['ipdb>=0.13.4,<0.14.0',
 'mock>=4.0.2,<5.0.0',
 'requests>=2.25.0,<3.0.0',
 'responses>=0.12.1,<0.13.0',
 'rich>=8.0.0,<9.0.0',
 'typer[all]>=0.3.2,<0.4.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.0,<2.0.0']}

entry_points = \
{'console_scripts': ['arachnys-api-client = arachnys_api_client.__main__:app']}

setup_kwargs = {
    'name': 'arachnys-api-client',
    'version': '0.2.0',
    'description': 'API client for Arachnys APIs, including Unified Search, Entity API and others',
    'long_description': '# arachnys-api-client\n\n<div align="center">\n\nAPI client for Arachnys APIs, including Unified Search, Entity API and others\n</div>\n\n## Usage\n\n```bash\npip install arachnys-api-client\n```\n\nUse the CLI:\n\n```bash\narachnys-api-client search-uss --source-ids opencorporates.company --filter \'[{"attribute_id": "arachnys.jurisdiction", "text": {"match": "GB"}},{"attribute_id": "arachnys.company_name", "text": {"match": "arachnys"}}]\'\n```\n\n## Developing\n\n1. Clone repo\n\n2. Install poetry\n\n```bash\nmake download-poetry\n```\n\n3. Initialize poetry and install `pre-commit` hooks:\n\n```bash\nmake install\n```\n\n4. Add your API credentials to your shell environment\n\n```bash\nexport ARACHNYS_PLATFORM_USER_ID=<your_user_id>\nexport ARACHNYS_PLATFORM_SECRET_ID=<your_secret_id>\nexport ARACHNYS_PLATFORM_SECRET_KEY=<your_secret_key>\nexport ARACHNYS_PLATFORM_API_BASE=<your_platform_tenant> # May not be required for all tenants\n```\n\n5. See if it works!\n\n```bash\npoetry run arachnys-api-client search-uss --source-ids opencorporates.company --filter \'[{"attribute_id": "arachnys.jurisdiction", "text": {"match": "GB"}},{"attribute_id": "arachnys.company_name", "text": {"match": "arachnys"}}]\'\n```\n\n### Makefile usage\n\n[`Makefile`](https://github.com/arachnys/arachnys-api-client/blob/master/Makefile) contains many functions for fast assembling and convenient work.\n\n<details>\n<summary>1. Download Poetry</summary>\n<p>\n\n```bash\nmake download-poetry\n```\n\n</p>\n</details>\n\n<details>\n<summary>2. Install all dependencies and pre-commit hooks</summary>\n<p>\n\n```bash\nmake install\n```\n\nIf you do not want to install pre-commit hooks, run the command with the NO_PRE_COMMIT flag:\n\n```bash\nmake install NO_PRE_COMMIT=1\n```\n\n</p>\n</details>\n\n<details>\n<summary>3. Check the security of your code</summary>\n<p>\n\n```bash\nmake check-safety\n```\n\nThis command launches a `Poetry` and `Pip` integrity check as well as identifies security issues with `Safety` and `Bandit`. By default, the build will not crash if any of the items fail. But you can set `STRICT=1` for the entire build, or you can configure strictness for each item separately.\n\n```bash\nmake check-safety STRICT=1\n```\n\nor only for `safety`:\n\n```bash\nmake check-safety SAFETY_STRICT=1\n```\n\nmultiple\n\n```bash\nmake check-safety PIP_STRICT=1 SAFETY_STRICT=1\n```\n\n> List of flags for `check-safety` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`.\n\n</p>\n</details>\n\n<details>\n<summary>4. Check the codestyle</summary>\n<p>\n\nThe command is similar to `check-safety` but to check the code style, obviously. It uses `Black`, `Darglint`, `Isort`, and `Mypy` inside.\n\n```bash\nmake check-style\n```\n\nIt may also contain the `STRICT` flag.\n\n```bash\nmake check-style STRICT=1\n```\n\n> List of flags for `check-style` (can be set to `1` or `0`): `STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.\n\n</p>\n</details>\n\n<details>\n<summary>5. Run all the codestyle formaters</summary>\n<p>\n\nCodestyle uses `pre-commit` hooks, so ensure you\'ve run `make install` before.\n\n```bash\nmake codestyle\n```\n\n</p>\n</details>\n\n<details>\n<summary>6. Run tests</summary>\n<p>\n\n```bash\nmake test\n```\n\n</p>\n</details>\n\n<details>\n<summary>7. Run all the linters</summary>\n<p>\n\n```bash\nmake lint\n```\n\nthe same as:\n\n```bash\nmake test && make check-safety && make check-style\n```\n\n> List of flags for `lint` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.\n\n</p>\n</details>\n\n<details>\n<summary>8. Build docker</summary>\n<p>\n\n```bash\nmake docker\n```\n\nwhich is equivalent to:\n\n```bash\nmake docker VERSION=latest\n```\n\nMore information [here](https://github.com/arachnys/arachnys-api-client/tree/master/docker).\n\n</p>\n</details>\n\n<details>\n<summary>9. Cleanup docker</summary>\n<p>\n\n```bash\nmake clean_docker\n```\n\nor to remove all build\n\n```bash\nmake clean\n```\n\nMore information [here](https://github.com/arachnys/arachnys-api-client/tree/master/docker).\n\n</p>\n</details>\n\n## 🛡 License\n\n[![License](https://img.shields.io/github/license/arachnys/arachnys-api-client)](https://github.com/arachnys/arachnys-api-client/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/arachnys/arachnys-api-client/blob/master/LICENSE) for more details.\n\n## 📃 Citation\n\n```\n@misc{arachnys-api-client,\n  author = {Arachnys},\n  title = {API client for Arachnys APIs, including Unified Search, Entity API and others},\n  year = {2020},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/arachnys/arachnys-api-client}}\n}\n```\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'Arachnys',
    'author_email': 'info@arachnys.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/arachnys/arachnys-api-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
