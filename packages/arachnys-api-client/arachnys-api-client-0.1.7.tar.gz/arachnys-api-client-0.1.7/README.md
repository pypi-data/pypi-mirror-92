# arachnys-api-client

<div align="center">

API client for Arachnys APIs, including Unified Search, Entity API and others
</div>

## Usage

```bash
pip install arachnys-api-client
```

Use the CLI:

```bash
arachnys-api-client search-uss --source-ids opencorporates.company --filter '[{"attribute_id": "arachnys.jurisdiction", "text": {"match": "GB"}},{"attribute_id": "arachnys.company_name", "text": {"match": "arachnys"}}]'
```

## Developing

1. Clone repo

2. Install poetry

```bash
make download-poetry
```

3. Initialize poetry and install `pre-commit` hooks:

```bash
make install
```

4. Add your API credentials to your shell environment

```bash
export ARACHNYS_PLATFORM_USER_ID=<your_user_id>
export ARACHNYS_PLATFORM_SECRET_ID=<your_secret_id>
export ARACHNYS_PLATFORM_SECRET_KEY=<your_secret_key>
export ARACHNYS_PLATFORM_API_BASE=<your_platform_tenant> # May not be required for all tenants
```

5. See if it works!

```bash
poetry run arachnys-api-client search-uss --source-ids opencorporates.company --filter '[{"attribute_id": "arachnys.jurisdiction", "text": {"match": "GB"}},{"attribute_id": "arachnys.company_name", "text": {"match": "arachnys"}}]'
```

### Makefile usage

[`Makefile`](https://github.com/arachnys/arachnys-api-client/blob/master/Makefile) contains many functions for fast assembling and convenient work.

<details>
<summary>1. Download Poetry</summary>
<p>

```bash
make download-poetry
```

</p>
</details>

<details>
<summary>2. Install all dependencies and pre-commit hooks</summary>
<p>

```bash
make install
```

If you do not want to install pre-commit hooks, run the command with the NO_PRE_COMMIT flag:

```bash
make install NO_PRE_COMMIT=1
```

</p>
</details>

<details>
<summary>3. Check the security of your code</summary>
<p>

```bash
make check-safety
```

This command launches a `Poetry` and `Pip` integrity check as well as identifies security issues with `Safety` and `Bandit`. By default, the build will not crash if any of the items fail. But you can set `STRICT=1` for the entire build, or you can configure strictness for each item separately.

```bash
make check-safety STRICT=1
```

or only for `safety`:

```bash
make check-safety SAFETY_STRICT=1
```

multiple

```bash
make check-safety PIP_STRICT=1 SAFETY_STRICT=1
```

> List of flags for `check-safety` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`.

</p>
</details>

<details>
<summary>4. Check the codestyle</summary>
<p>

The command is similar to `check-safety` but to check the code style, obviously. It uses `Black`, `Darglint`, `Isort`, and `Mypy` inside.

```bash
make check-style
```

It may also contain the `STRICT` flag.

```bash
make check-style STRICT=1
```

> List of flags for `check-style` (can be set to `1` or `0`): `STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.

</p>
</details>

<details>
<summary>5. Run all the codestyle formaters</summary>
<p>

Codestyle uses `pre-commit` hooks, so ensure you've run `make install` before.

```bash
make codestyle
```

</p>
</details>

<details>
<summary>6. Run tests</summary>
<p>

```bash
make test
```

</p>
</details>

<details>
<summary>7. Run all the linters</summary>
<p>

```bash
make lint
```

the same as:

```bash
make test && make check-safety && make check-style
```

> List of flags for `lint` (can be set to `1` or `0`): `STRICT`, `POETRY_STRICT`, `PIP_STRICT`, `SAFETY_STRICT`, `BANDIT_STRICT`, `BLACK_STRICT`, `DARGLINT_STRICT`, `ISORT_STRICT`, `MYPY_STRICT`.

</p>
</details>

<details>
<summary>8. Build docker</summary>
<p>

```bash
make docker
```

which is equivalent to:

```bash
make docker VERSION=latest
```

More information [here](https://github.com/arachnys/arachnys-api-client/tree/master/docker).

</p>
</details>

<details>
<summary>9. Cleanup docker</summary>
<p>

```bash
make clean_docker
```

or to remove all build

```bash
make clean
```

More information [here](https://github.com/arachnys/arachnys-api-client/tree/master/docker).

</p>
</details>

## 🛡 License

[![License](https://img.shields.io/github/license/arachnys/arachnys-api-client)](https://github.com/arachnys/arachnys-api-client/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/arachnys/arachnys-api-client/blob/master/LICENSE) for more details.

## 📃 Citation

```
@misc{arachnys-api-client,
  author = {Arachnys},
  title = {API client for Arachnys APIs, including Unified Search, Entity API and others},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/arachnys/arachnys-api-client}}
}
```

## Credits

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).
