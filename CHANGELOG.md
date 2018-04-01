# Changelog
All notable changes to this project will be documented in this file.

## [1.11]  - 26 Oct 2017<br>
### Fixed
- php://filter attack did not work as expected, returning even not base64 contents.

## [1.13]  - 1 Apr 2018<br>
### Fixed
- requests now are allowed to any websites, even those with self-signed certificates
### Added
- set the default file containing paths to test to "pathtotest.txt" (used if the user leaves the input blank)
