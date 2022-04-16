# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [1.3.1] - 2021-11-15
### Changed
* Limit document status update wait time to 60 seconds, and log wait times.


## [1.3.0] - 2021-11-15
Note: the PyPI package for 1.3.0 included changes from 1.3.1, so it has been yanked. 
### Added
* Add glossary support for document translation.
* Add proxy support.
### Fixed
* Fix issues with parallelized tests by changing how test glossaries are created and deleted.


## [1.2.1] - 2021-10-19
### Added
* Add support for Python 3.10.
### Fixed
* Fix bug that caused User-Agent header to be omitted from HTTP requests. 
* Fix glossary name prefix used in unit-tests to match git repository name.
* Add workaround for possible issue in datetime.strptime in Python 3.6.


## [1.2.0] - 2021-10-07
### Added
* Add `Translator.get_glossary_languages()` to query language pairs supported for glossaries.
* Add constants for all supported languages codes, for example: `Language.GERMAN`.
### Changed
* Internal language caching and client-side checking of language codes are removed. 
### Deprecated
* Some optional arguments related to language caching are now deprecated, and will be removed in a future version:
  * `Translator()`: the `skip_language_check` argument 
  * `Translator.get_source_languages()` and `Translator.get_target_languages()`: the `skip_cache` argument 
### Fixed
* Fix HTTP request retries for document uploads.


## [1.1.3] - 2021-09-27
### Changed
* Loosen requirement for requests to 2.0 or higher.


## [1.1.2] - 2021-09-21
### Changed
* Improve request exception messages and include exception stacktraces.
* Update unit tests for server error message changes.


## [1.1.1] - 2021-09-13
### Fixed
* Fix typing.List issue on Python 3.6.
* Add workaround for datetime.strptime bug in Python 3.6.


## [1.1.0] - 2021-09-13
### Added
* Add security policy.
* Add support for glossary API functions.
### Fixed
* README and comments improvements, type hints and other minor fixes.  


## [1.0.1] - 2021-08-13
### Added
* Add explicit copyright notice to all source files.
### Fixed
* Force response encoding to UTF-8 to avoid issues with older versions of requests package.


## [1.0.0] - 2021-08-12
### Changed
* All API calls use Authorization header instead of auth_key parameter.


## [0.4.1] - 2021-08-10
### Changed
* Minor updates to pyproject.toml and README.md.


## [0.4.0] - 2021-08-05
Version increased to avoid conflicts with old packages on PyPI. 


## [0.3.0] - 2021-08-05
### Added
* Package uploaded to PyPI. Thanks to [Adrian Freund](mailto:mail@freundtech.com) for transferring the deepl package
  name.
* Clarify minimum version of requests module to 2.18.


## [0.2.0] - 2021-07-28
### Changed
* Improve exception hierarchy.
* Translator() server_url argument works with and without trailing slash.
* Translator.translate_text() accepts a single text argument, which may be a list or other iterable.
### Fixed
* Fix examples in readme to match function interface changes.


## [0.1.0] - 2021-07-26
Initial version.


[1.3.1]: https://github.com/DeepLcom/deepl-python/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/DeepLcom/deepl-python/compare/v1.2.1...v1.3.0
[1.2.1]: https://github.com/DeepLcom/deepl-python/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/DeepLcom/deepl-python/compare/v1.1.3...v1.2.0
[1.1.3]: https://github.com/DeepLcom/deepl-python/compare/v1.1.2...v1.1.3
[1.1.2]: https://github.com/DeepLcom/deepl-python/compare/v1.1.1...v1.1.2
[1.1.1]: https://github.com/DeepLcom/deepl-python/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/DeepLcom/deepl-python/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/DeepLcom/deepl-python/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/DeepLcom/deepl-python/compare/v0.4.1...v1.0.0
[0.4.1]: https://github.com/DeepLcom/deepl-python/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/DeepLcom/deepl-python/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/DeepLcom/deepl-python/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/DeepLcom/deepl-python/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/DeepLcom/deepl-python/releases/tag/v0.1.0
