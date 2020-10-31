# Language Formatters Pre Commit Hooks

[![Github Actions CI](https://github.com/macisamuele/language-formatters-pre-commit-hooks/workflows/Build/badge.svg)](https://github.com/macisamuele/language-formatters-pre-commit-hooks/actions)
[![Coverage](https://img.shields.io/codecov/c/github/macisamuele/language-formatters-pre-commit-hooks/master.svg)](https://codecov.io/gh/macisamuele/language-formatters-pre-commit-hooks)
[![PyPi version](https://img.shields.io/pypi/v/language-formatters-pre-commit-hooks.svg)](https://pypi.python.org/pypi/language-formatters-pre-commit-hooks/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/language-formatters-pre-commit-hooks.svg)](https://pypi.python.org/pypi/language-formatters-pre-commit-hooks/)

## About

This package provides utilities for ensuring that your code is nicely formatted by using [`pre-commit`](https://pre-commit.com/) hooks

## List of pretty-format hooks

* `pretty-format-golang`
* `pretty-format-ini`
* `pretty-format-java`
* `pretty-format-kotlin`
* `pretty-format-rust`
* `pretty-format-toml`
* `pretty-format-yaml`

⚠: the list above could be out-of-sync respect the exposed pre-commit hooks.

Please refer to [`.pre-commit-hooks.yaml`](.pre-commit-hooks.yaml) for a more updated list.

## Example Usage

Add a similar snippet into your `.pre-commit-config.yaml` file

```yaml

- repo: https://github.com/macisamuele/language-formatters-pre-commit-hooks
  rev: ${LATEST_SHA_OR_VERSION}
  hooks:
  - id: pretty-format-java
    args: [--autofix]
  - id: pretty-format-kotlin
    args: [--autofix]
  - id: pretty-format-yaml
    args: [--autofix, --indent, '2']
```

## Development

This tool uses tox as main tool to build virtual environments.

To get started will be enough to run `make development`.

If you have [`aactivator`](https://github.com/Yelp/aactivator) installed this step will happen automatically.

### Contributing

Contributions are _always_ welcome.

1. [Fork the project](http://github.com/macisamuele/language-formatters-pre-commit-hooks/fork)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Add your modifications
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## FAQ

### How to deal with multiple Java versions?

This might be relevant for `pretty-format-java` and `pretty-format-kotlin` hooks.
The hooks depends on having `java` on version **11** or greater installed on your machine.

As you're working with _compiled-to-JVM_ languages, we assume that you have `java` installed on your system. You might not have the minimum required version installed.

To work-around such scenario you have 2 approaches available:

1. Have multiple `java` versions installed on your system and ensure that while running the pre-commit hooks JRE 11+ is available on your `PATH` variable (ie. `PATH=${JRE_11_PATH}:${PATH} pre-commit run`).

2. Work around the issue by using [`docker`](https://www.docker.com/).
    ⚠: This approach has been tested (at the time of writing) on Linux and MacOS.

    The latter approach should be preferred if you cannot install an additional JRE version on your system or if doing is unfeasible (e.g. on a CI system). Please note you need to have `docker` installed on your system.

    Add the following `Dockerfile` on your repository root (same directory where `.pre-commit-config.yaml` is stored)

    ```Dockerfile
    FROM python:3.7-alpine

    # Install JRE-11 as we will run pre-commit hooks that depends an Java 11+
    RUN apk add --no-cache openjdk11-jre

    ENV PRE_COMMIT_HOME /pre-commit-docker-cache
    ENV PRE_COMMIT_LANGUAGE_FORMATTERS_VERSION ${version of the library to install}

    RUN set -x \
        && pip install --no-cache-dir language-formatters-pre-commit-hooks==${PRE_COMMIT_LANGUAGE_FORMATTERS_VERSION} \

        # Run pre-commit-hook to ensure that jars are downloaded and stored in the docker image
        # Run the hooks that you're planning to run within docker.
        # This reduces premission issues as well has makes all the run fast as the lazy-dependencies are pre-fetched
        && pretty-format-java  \

        # Update permissions as hooks will be run as your host-system user (your username) but the image is built as root
        && chmod a+r ${PRE_COMMIT_HOME}/*
    ```

    and the following hook into your `.pre-commit-config.yaml` file

    ```yaml
    repos:
    - repo: local
      hooks:
      - id: pretty-format-java-in-docker    # Useful to eventually SKIP pre-commit hooks
        name: pretty-format-java-in-docker  # This is required, put something sensible
        language: docker                    # Self explanatory
        entry: pretty-format-java           # Hook that you want to run in docker
        args: [...]                         # Arguments that would would pass to the hook (as if it was local)
        files: ^.*\.java$                   # File filter has to be added ;)
    ```

    By doing the following, the selected hook (`pretty-format-java` in the example) will be executed within the docker container.

    Side note: We're not embedding the Dockerfile in the repository as this is more a workaround to support whom cannot of installing a more recent Java version on the library-user system and as such we are not planning to fully support this other than giving possible solutions (Java 11+ was released in September, 2018).

## License

`language-formatters-pre-commit-hooks` is licensed with [`Apache License version 2.0`](http://www.apache.org/licenses/LICENSE-2.0.html).
