# Changelog
This changelog is inspired by [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## 0.7b0 [2021-01-20]
### Added
- function *prepare_print* returning the string representation before the print.

## 0.6b7 [2021-01-20]
### Fixed
- Wrong sting replacement using bumpversion.
- Missing dependencies in tox.

## 0.6b1
### Added
- Testing via travis-ci and tox
- Code coverage via coveralls.io

### Changed
- Layout of setup.py to setup.cfg
- Added badges to readme.

## 0.6b0 [2020-12-28]
### Added
- Helper method *round_collections* for rounding items using the 
  *edit_item* argument or *doctest_iter_print*.

## 0.5b2 [2020-12-18]
### Fixed
- Text was not printed correctly if it span over 2 lines.

## 0.5b1 [2020-12-01]
### Fixed
- Text was not printed correctly, if it was within a single line smaller than 
  *max_line_width*.

## 0.5b0 [2020-11-27]
### Added
- Argument 'item_edit' allows a preliminary editing of each first level item
  before printing.

## 0.4a0.post1 [2020-11-21]
### Added
- Argument `indent` supports indentation in `doctest_print`
- Function `doctest_iter_print` iterates through the first level of an Iterable or
  Mapping.

## 0.3a0 [unreleased]
### Changed
- Renamed `doctest_print` to `doctest_print_list`
- Changed behavior of former `doctest_print` to an overall printing method.
- Added optional argument 'max_line_width' to `doctest_print`.

## 0.0b2 [unreleased]
### Added
- method *remove_trailing_whitespaces* removes trailing whitespaces from a
  multiline text.
- method *repr_posix_path* and *strip_base_path*

## 0.0a1 [unreleased]
- initialized *doctestprinter*