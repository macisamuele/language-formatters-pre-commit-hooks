Changelog
=========

2.10.0 (2023-05-29)
------------------

- Add `--indent` and `--trailing-commas` arguments for `pretty-format-toml` - [PR #160](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/143) - [@maresb](https://github.com/maresb) thanks for your contribution

2.9.0 (2023-05-13)
------------------

- Update GoogleJavaFormatter to 1.17.0
- Update KTLint to 0.49.1
- Bug fix pretty-format-yaml
  Sequecence item indentation should condider offset as part of the indentation, [#154 (comment)](https://github.com/macisamuele/language-formatters-pre-commit-hooks/issues/154#issuecomment-1546778156) has more details.
  Thanks [@datalogics-kam](https://github.com/datalogics-kam) and [@fmigneault](https://github.com/fmigneault) for reporting the issue and helping me identify the underlying root cause.

2.8.0 (2023-03-17)
------------------

- Update GoogleJavaFormatter to 1.16.0

2.7.0 (2023-02-18)
------------------

- Add support for customisable offset in `pretty-format-yaml` - [PR #143](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/143)
- Update KTLint to 0.48.2

2.6.0 (2023-01-20)
------------------

- Fix `pretty-format-toml` to be compatible with latest `toml-sort` libraries - Thanks [@liblaf](https://github.com/liblaf) and [@stewartHutchins](https://github.com/stewartHutchins) for the support on having toml prettification working again
  The fix has been carried over multiple PRs ([PR #134](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/134), [PR #136](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/136) and [PR #137](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/137)).
- Internal build fix (failures caused by `tox` major release) - [PR #141](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/141), inspired from [PR #135](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/135) - Thanks [@malmans2](https://github.com/malmans2) for the support
- Update KTlint to 0.48.1 - [PR #140](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/140) - Thanks [@detouched](https://github.com/detouched) for the upgrade

2.5.0 (2022-12-05)
------------------

- Lift JDK 16+ restriction - [PR #123](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/123) - [@harti2006](https://github.com/harti2006) thanks for your contribution
- Update KTlint to 0.47.1 - [PR #125](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/125)
- pretty_format_rust does no longer use explicit rust versions - [PR #126](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/126)

2.4.0 (2022-07-01)
------------------

- Update GoogleJavaFormatter to 1.15.0
- Update KTlint to 0.45.1
- Ensure Python 3.10 support and drop Python3.6 guaranteed support - [PR #114](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/114) / [PR #115](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/115)
- Updated prettifier library for INI files (from `configobj` to `config_formatter`) to provide more deterministic output and proper comments handling - [PR #113](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/113) - [@Delgan](https://github.com/Delgan) thanks for your contribution
- `pretty-format-yaml` allows customization of max line length - [PR #104](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/104)
- More explicit error messages in case of prettifier failires - [PR #116](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/116)
- Use explicit encoding within INI prettifier - [PR #102](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/102) - [@hbre](https://github.com/hbre) thanks for your contribution

2.3.0 (2022-02-17)
------------------

- Update GoogleJavaFormatter to 1.14.0
- Update KTlint to 0.44.0
- Use explicit encoding within YAML prettifier - [PR #92](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/92) - [@passionsfrucht](https://github.com/passionsfrucht) thanks for your contribution

2.2.0 (2021-08-08)
------------------

- Make download of external artifacts resilient to systems with temporary directory on different disk partitions - [@psmit](https://github.com/psmit) and [@kbalston](https://github.com/kbalston) thanks for your contribution
- Make usage of Google Java Formatter compatible with JDK16+ - [@ostrya](https://github.com/ostrya) thanks for your contribution
- Update GoogleJavaFormatter to 1.11.0
- Bump KTlint to 0.42.1
- Misc github workflow updates (testing on Python 3.9, better tracking of tool versions tested, etc.)
- Improved error message in case of Google Java Formatter and KTLint not supported Java Version

ℹ: `pretty-format-java` now supports Java 16+
⚠: `pretty-format-kotlin` supports Java up to Java 15

2.1.0 (2021-05-28)
------------------

- Bump KTlint to 0.40.0
- Update GoogleJavaFormatter to 1.10.0

2.0.0 (2021-01-16)
------------------

- Preserve comments in while formatting `ini` files. [PR #45](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/45) - [@Skylion007](https://github.com/Skylion007) thanks for your contribution
- Preserve comments in while formatting `toml` files. [PR #46](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/46) - [@Skylion007](https://github.com/Skylion007) thanks for your contribution
- ⚠ Drop Python2 support. [PR #48](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/48)
- Update KTLint to 0.40.0

1.6.1 (2020-10-31)
-----------------

- Internal fix of downloaded files path. [PR #43](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/43)

1.6.0 (2020-10-24)
------------------

- Update KTLint to 0.39.0
- Update GoogleJavaFormatter to 1.9
- Run `pretty-format-java` serially to prevent multiple-downloads of the same Java artifact. [PR #23](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/23) - [@ineiti](https://github.com/ineiti) thanks for your contribution
- Internal update of download logic to reduce race coditions while download big artifacts from network. [PR #24](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/24)
- Bump min `pre-commit` supported version. [PR #27](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/27)
- Allow `pretty-format-java` to modify the Google Java Formatter to use (`--google-java-formatter-version` CLI argument). [PR #30](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/30)
- Allow `pretty-format-kotlin` to modify the KTLint to use (`--ktlint-version` CLI argument). [PR #30](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/30)
- Enhance security in commands execution (prevent shell-injection). [PR #38](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/38)

1.5.0 (2020-06-16)
------------------

- Add `--preserve-quotes` argument into `pretty-format-yaml`. [PR #16](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/16) - [@vbisserie](https://github.com/vbisserie) thanks for your contribution

1.4.2 (2020-06-09)
------------------

- Update KTLint to 0.37.1

1.4.1 (2020-06-03)
------------------

- Update KTLint to 0.37.0

1.4.0 (2020-05-20)
------------------

- Improve handling of multi-document YAML files. [PR #3](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/3) - [@dan-cohn](https://github.com/dan-cohn) thanks for your contribution
- `pretty-format-java` does default to Google style. Add `--aosp` argument for Android Open Source Project style. [PR #8](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/8) - [@ChenAndrew](https://github.com/ChenAndrew) thanks for your contribution.
- Update GoogleJavaFormatter to 1.8

1.3.2 (2020-01-25)
------------------

- Definitive packaging fix

1.3.1 (2020-01-24)
------------------

- Update Packaging informations

:warning: This version **broke module retrieval** (:disappointed:) while improving quality of PyPi uploaded information. You're recommended to use a more recent version of the library.

1.3.0 (2020-01-24)
------------------

- Update KTLint to 0.36.0
- Enhange `pretty-format-yaml` to deal with YAML files containing primitive types only - [PR #1](https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/1) - [@dan-cohn](https://github.com/dan-cohn) thanks for your contribution

1.2.5 (2019-11-22)
------------------

- Update KTLint to 0.35.0

1.2.4 (2019-07-19)
------------------

- Update KTLint to 0.34.0 and fix KTLint GitHub link

1.2.3 (2019-02-14)
------------------

- Update Google Java Formatter to 1.7 and KTlint to 0.30.0

1.2.2 (2018-11-20)
------------------

- pretty-format-rust fails if ``cargo fmt`` fails

1.2.1 (2018-11-20)
------------------

- no-diff release

1.2.0 (2018-11-20)
------------------

- Bump KTlint to 0.29.0
- Remove duplicated filenames from command execution

1.1.3 (2018-09-02)
------------------

- Last fix to cargo invocations to use the environmentally defined toolchain

1.1.2 (2018-09-02)
------------------

- Bump KTlint to 0.27.0

1.1.1 (2018-09-02)
------------------

- Ensure that generated files end with a new line
- Allow rust toolchain customization via `RUST_TOOLCHAIN` environment variable

1.1.0 (2018-07-29)
------------------

- Add pretty formatters for INI, Rust and TOML files

1.0.1 (2018-07-20)
------------------

- Improve detection of modified files from kotlin formatter

1.0.0 (2018-07-20)
------------------

- Initial release: added pretty formatters for Golang, Java, Kotlin and YAML
