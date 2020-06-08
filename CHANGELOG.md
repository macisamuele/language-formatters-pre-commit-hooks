Changelog
=========

1.4.2 (2020-06-09)
------------------
- Update KTLint to 0.37.1

1.4.1 (2020-06-03)
------------------
- Update KTLint to 0.37.0

1.4.0 (2020-05-20)
------------------
- Improve handling of multi-document YAML files. PR #3 - [@dan-cohn](https://github.com/dan-cohn) thanks for your contribution
- `pretty-format-java` does default to Google style. Add `--aosp` argument for Android Open Source Project style. PR #8 - [@ChenAndrew](https://github.com/ChenAndrew) thanks for your contribution.
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
- Enhange `pretty-format-yaml` to deal with YAML files containing primitive types only - PR #1 - [@dan-cohn](https://github.com/dan-cohn) thanks for your contribution

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
