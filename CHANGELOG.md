# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.1b4] - 2017-09-05
### Added
- [a6a9c6d]: Added Dockerfile & dev reqs
- [dad0bd8]: Added Market
- [2f1ba0d]: Added Travis CI & Coveralls
- [7ef1461]: Added virtualdisplay
- [3dab378]: Added BrowserException
- [4d9e3d6]: Added logger

### Changed
- [78a5a9a]: Included logger in setup

### Removed
- [95ca894]: Removed datetime from records

### Fixed
A lot of minor fixies, these are the mayor ones:

- [412f29f]: Fixed prefs bug
- [ce71903]: Fixed **addPrefs** and **clearPrefs** bugs.

## [0.1b3] - 2017-08-28
### Added
- [abdde90]: Added virtual browser (and fixed).
- [07f19ad]: Added sentiment to **addPrefs**.

### Changed
- [b17e6df]: Launch browser function on its own _"self.launch()"_.

## [0.1b2] - 2017-08-27
### Added
- [cbf449a]: Added sentiment to **checkStocks**.

### Fixed
- [64f78e4]: Adjusted price in **checkStocks** _(now without swap)_.

### Deprecated
- [64f78e4]: Date in movements.

## [0.1b1] - 2017-08-24
### Fixed
- Fixed finally **checkStocks**.

## [0.1a2] - 2017-08-23
### Fixed
- Fixed partially **checkStocks**.

### Added
- New function **addPrefs**.
- New function **clearPrefs**.

## [0.1a1] - 2017-08-20
### Added
- New function **checkStocks**.

## 0.1a0 - 2017-08-19
Initial version.

[Unreleased]: https://github.com/federico123579/Trading212-API/compare/v0.1b3...HEAD
[0.1b3]: https://github.com/federico123579/Trading212-API/compare/v0.1b2...v0.1b3
[0.1b2]: https://github.com/federico123579/Trading212-API/compare/v0.1b1...v0.1b2
[0.1b1]: https://github.com/federico123579/Trading212-API/compare/v0.1a2...v0.1b1
[0.1a2]: https://github.com/federico123579/Trading212-API/compare/v0.1a1...v0.1a2
[0.1a1]: https://github.com/federico123579/Trading212-API/compare/v0.1a0...v0.1a1

[2f1ba0d]: https://github.com/federico123579/Trading212-API/commit/2f1ba0d
[78a5a9a]: https://github.com/federico123579/Trading212-API/commit/78a5a9a
[7ef1461]: https://github.com/federico123579/Trading212-API/commit/7ef1461
[412f29f]: https://github.com/federico123579/Trading212-API/commit/412f29f
[a6a9c6d]: https://github.com/federico123579/Trading212-API/commit/a6a9c6d
[dad0bd8]: https://github.com/federico123579/Trading212-API/commit/dad0bd8
[95ca894]: https://github.com/federico123579/Trading212-API/commit/95ca894
[3dab378]: https://github.com/federico123579/Trading212-API/commit/e25a600
[4d9e3d6]: https://github.com/federico123579/Trading212-API/commit/4d9e3d6
[abdde90]: https://github.com/federico123579/Trading212-API/commit/abdde90
[ce71903]: https://github.com/federico123579/Trading212-API/commit/ce71903
[07f19ad]: https://github.com/federico123579/Trading212-API/commit/07f19ad
[b17e6df]: https://github.com/federico123579/Trading212-API/commit/b17e6df
[cbf449a]: https://github.com/federico123579/Trading212-API/commit/cbf449a
[64f78e4]: https://github.com/federico123579/Trading212-API/commit/64f78e4
