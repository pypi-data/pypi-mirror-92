# -*- coding:utf-8 -*-
__author__ = """David Scheliga"""
__email__ = "david.scheliga@gmx.de"
__version__ = "0.7b1"
__all__ = [
    "doctest_iter_print",
    "doctest_print",
    "doctest_print_list",
    "prepare_print",
    "round_collections",
    "remove_trailing_tabs",
    "remove_trailing_whitespaces",
    "remove_trailing_whitespaces_and_tabs",
    "repr_posix_path",
]

import re
import sys
from collections import namedtuple
from enum import IntFlag
from pathlib import Path
from typing import (
    Iterable,
    List,
    Generator,
    Union,
    Match,
    Any,
    Optional,
    Mapping,
    Callable,
    Sequence,
)


FIND_WHITESPACES = re.compile(r"[\s]+")
WhiteSpaceBlockPosition = namedtuple("WhiteSpaceBlockPosition", "start end")
WhiteSpaceBlockPositions = Sequence[WhiteSpaceBlockPosition]
BlockSectionPosition = namedtuple("BlockSectionPosition", "start end")
BlockSectionPositions = Iterable[BlockSectionPosition]
LINE_BREAK = "\n"


class Platforms(IntFlag):
    WINDOWS = 0
    LINUX = 1

    @classmethod
    def get_current_platform(cls):
        if sys.platform in ["win32"]:
            return Platforms.WINDOWS
        if sys.platform in ["linux"]:
            return Platforms.LINUX


_current_platform = Platforms.get_current_platform()
_REPLACE_TRAILING_WHITESPACE = re.compile(r"[\s]+$", re.MULTILINE)
_REPLACE_TRAILING_TABS = re.compile(r"[\t]+$", re.MULTILINE)
_REPLACE_TRAILING_WHITESPACE_AND_TABS = re.compile(r"[\s\t]+$", re.MULTILINE)


APath = Union[str, Path]


def remove_trailing_tabs(text: str) -> str:
    """
    Removes trailing tabs from the text.

    Args:
        text(str):
            Text from which trailing tabs should be removed.

    Returns:
        str

    Examples:
        >>> sample_text = "A sample text with\\t\\n trailing tabs.\\t\\n\\t"
        >>> remove_trailing_tabs(sample_text)
        'A sample text with\\n trailing tabs.\\n'
        >>> sample_text = "A sample text with\\t\\n\\ttrailing tabs.\\t\\nEnd.\\t"
        >>> remove_trailing_tabs(sample_text)
        'A sample text with\\n\\ttrailing tabs.\\nEnd.'

    """
    return _REPLACE_TRAILING_TABS.sub("", text)


def remove_trailing_whitespaces(text: str) -> str:
    """
    Removes trailing whitespaces from the text.

    Args:
        text(str):
            Text from which trailing whitespaces should be removed.

    Returns:
        str

    Examples:
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\n   "
        >>> remove_trailing_whitespaces(sample_text)
        'A sample text with\\n trailing whitespaces.'
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\nEnd. "
        >>> remove_trailing_whitespaces(sample_text)
        'A sample text with\\n trailing whitespaces.\\nEnd.'

    """
    return _REPLACE_TRAILING_WHITESPACE.sub("", text)


def remove_trailing_whitespaces_and_tabs(text: str) -> str:
    """
    Removes trailing tabs from the text.

    Args:
        text(str):
            Text from which trailing tabs should be removed.

    Returns:
        str

    Examples:
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\n\\t"
        >>> remove_trailing_whitespaces_and_tabs(sample_text)
        'A sample text with\\n trailing whitespaces.'
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\nEnd.\\t"
        >>> remove_trailing_whitespaces_and_tabs(sample_text)
        'A sample text with\\n trailing whitespaces.\\nEnd.'
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\n   "
        >>> remove_trailing_whitespaces(sample_text)
        'A sample text with\\n trailing whitespaces.'
        >>> sample_text = "A sample text with    \\n trailing whitespaces.   \\nEnd. "
        >>> remove_trailing_whitespaces_and_tabs(sample_text)
        'A sample text with\\n trailing whitespaces.\\nEnd.'

    """
    return _REPLACE_TRAILING_WHITESPACE_AND_TABS.sub("", text)


_ADDS_AN_IDENT_AT_SECOND_LINE = re.compile(LINE_BREAK, re.MULTILINE)


def _indent_block(paragraph: str, indent: str) -> str:
    """
    Indents a multiline paragraph.

    Args:
        paragraph(str):
            The paragraph which should be indented.

        indent(Optional[str]):
            Custom indentation.

    Returns:
        str

    Test:
        >>> print(_indent_block("a\\nparagraph", indent="--> "))
        --> a
        --> paragraph
    """
    if indent is None:
        indent = "    "
    return _ADDS_AN_IDENT_AT_SECOND_LINE.sub(LINE_BREAK + indent, indent + paragraph)


_windows_drive_letter_matcher = re.compile("^([a-z]):")


def _replace_windows_drive_letter(drive_letter_match: Match) -> str:
    """
    Replaces the windows drive letter with a forward slash encapsulation.

    Notes:
        Is used by :func:`repr_posix_path` using :func:`re.sub`.

    Args:
        drive_letter_match(Match):
            The regular expression matched drive letter.

    Returns:
        str
    """
    drive_letter = drive_letter_match.group(1)
    return "/{}".format(drive_letter)


def repr_posix_path(any_path: Union[str, Path]) -> str:
    """
    Represents the path on a Windows machine as a Posix-Path representation
    turning back slashes to forward slashes.

    Examples:
        >>> repr_posix_path("c:\\\\a\\\\path")
        '/c/a/path'
        >>> repr_posix_path(".\\\\a\\\\path")
        './a/path'
        >>> repr_posix_path(".\\\\a\\\\path")
        './a/path'

    Args:
        any_path(str, Path):
            Any type of path representation.

    Returns:
        str
    """
    busted_windows_drive_letter = _windows_drive_letter_matcher.sub(
        _replace_windows_drive_letter, str(any_path)
    )
    return str(busted_windows_drive_letter).replace("\\", "/")


def strip_base_path(base_path_to_strip: APath, path_to_show: APath) -> str:
    """
    Strips the given *base path* from the *path to show* and performing
    :func:`repr_posix_path` on the result.

    Examples:
        >>> strip_base_path("/a/root/path", "/a/root/path/some/place")
        '... /some/place'
        >>> strip_base_path("\\\\a\\\\root\\\\path", "/a/root/path/some/place")
        '... /some/place'
        >>> strip_base_path("/a/root/path", "\\\\a\\\\root\\\\path\\\\some\\\\place")
        '... /some/place'

    Args:
        base_path_to_strip:
            The base path, which should be removed from the view.

        path_to_show:
            The path which is going to be viewed.

    Returns:
        str
    """
    if _current_platform == Platforms.WINDOWS:
        path_to_show = str(path_to_show).replace("/", "\\")
        base_path_to_strip = str(base_path_to_strip).replace("/", "\\")
    elif _current_platform == Platforms.LINUX:
        path_to_show = str(path_to_show).replace("\\", "/")
        base_path_to_strip = str(base_path_to_strip).replace("\\", "/")
    stripped_path = str(path_to_show).replace(str(base_path_to_strip), "... ")
    return repr_posix_path(stripped_path)


def get_positions_of_whitespace_blocks(text: str) -> WhiteSpaceBlockPositions:
    """

    Args:
        text(str):

    Examples:
        >>> sample_text = "This is a    test string.    "
        >>> white_space_positions = get_positions_of_whitespace_blocks(sample_text)
        >>> for position in white_space_positions:
        ...     print(position)
        WhiteSpaceBlockPosition(start=4, end=5)
        WhiteSpaceBlockPosition(start=7, end=8)
        WhiteSpaceBlockPosition(start=9, end=13)
        WhiteSpaceBlockPosition(start=17, end=18)
        WhiteSpaceBlockPosition(start=25, end=29)
        >>> get_positions_of_whitespace_blocks("")
        []
        >>> sample_text = str(list(iter("abcde")))
        >>> white_space_positions = get_positions_of_whitespace_blocks(sample_text)
        >>> for position in white_space_positions:
        ...     print(position)
        WhiteSpaceBlockPosition(start=5, end=6)
        WhiteSpaceBlockPosition(start=10, end=11)
        WhiteSpaceBlockPosition(start=15, end=16)
        WhiteSpaceBlockPosition(start=20, end=21)

    Returns:
        WhiteSpaceBlockPositions
    """
    assert text is not None, "`text` cannot be None."
    return [
        WhiteSpaceBlockPosition(match.start(), match.end())
        for match in FIND_WHITESPACES.finditer(text)
    ]


def find_section_positions_at_whitespaces(
    text: str, maximum_line_width: int
) -> List[BlockSectionPosition]:
    """
    Finds the positions of sections. Whitespaces marks the used section positions.

    Args:
        text(str):
            The text in which

        maximum_line_width(int):
            The maximum linewidth.

    Returns:
        List[BlockSectionPosition]

    Examples:
        >>> sample_text = str(list(range(60)))
        >>> section_positions = find_section_positions_at_whitespaces(sample_text, 40)
        >>> for section in section_positions:
        ...     print(section)
        BlockSectionPosition(start=0, end=42)
        BlockSectionPosition(start=43, end=86)
        BlockSectionPosition(start=87, end=130)
        BlockSectionPosition(start=131, end=174)
        BlockSectionPosition(start=175, end=218)
        BlockSectionPosition(start=219, end=230)
        >>> sample_text = str(list(iter("abcde")))
        >>> section_positions = find_section_positions_at_whitespaces(sample_text, 40)
        >>> for section in section_positions:
        ...     print(section)
        BlockSectionPosition(start=0, end=25)

    .. doctest:

        >>> sample = str(['strangely_eq', 'ual_wide_ite', 'ms_are_not_s'])
        >>> section_positions = find_section_positions_at_whitespaces(sample, 36)
        >>> for section in section_positions:
        ...     print(section)
        BlockSectionPosition(start=0, end=32)
        BlockSectionPosition(start=33, end=48)
        >>> section_positions = find_section_positions_at_whitespaces(sample, 48)
        >>> for section in section_positions:
        ...     print(section)
        BlockSectionPosition(start=0, end=48)

    """
    assert isinstance(
        text, (str, bytes, bytearray)
    ), "text must be a string or byte-like."
    text_length = len(text)
    full_text_fits_in_one_line = text_length <= maximum_line_width
    if full_text_fits_in_one_line:
        return [BlockSectionPosition(0, text_length)]

    block_positions = get_positions_of_whitespace_blocks(text)
    block_sections = []
    current_line_start_position_within_text = 0
    last_line_start_within_text = 0

    last_block_position = block_positions[-1]
    breaks_into_2_lines = last_block_position.start < maximum_line_width
    if breaks_into_2_lines:
        block_sections = [BlockSectionPosition(0, last_block_position.start)]
        last_line_start_within_text = last_block_position.end
    else:
        for block_position in block_positions:
            try:
                block_start_position_within_text, end_position = block_position
            except ValueError:
                raise ValueError(
                    "A block position must be a 2 item tuple of start & end."
                )

            current_line_end_within_text = (
                block_start_position_within_text
                - current_line_start_position_within_text
            )
            found_section_with_adequate_width = (
                current_line_end_within_text >= maximum_line_width
            )
            if found_section_with_adequate_width:
                block_sections.append(
                    BlockSectionPosition(
                        start=current_line_start_position_within_text,
                        end=block_start_position_within_text,
                    )
                )
                current_line_start_position_within_text = end_position
            last_line_start_within_text = current_line_start_position_within_text

    did_found_block_sections = len(block_sections) > 0
    if did_found_block_sections:
        last_block_position = block_sections[-1][1]
        text_length = text_length
        if last_block_position < text_length:
            block_sections.append(
                BlockSectionPosition(start=last_line_start_within_text, end=text_length)
            )

    return block_sections


def iter_split_text(
    text: str, block_sections: BlockSectionPositions
) -> Generator[str, None, None]:
    """
    Splits a texts by :attribute:`BlockSectionPositions`.

    Args:
        text(str):
            Text which should be split.

        block_sections(BlockSectionPositions):
            Positions by which to split.

    Yields:
        str

    Examples:
        >>> sample_text = str(list(range(60)))
        >>> block_positions = find_section_positions_at_whitespaces(sample_text, 40)
        >>> for line in iter_split_text(sample_text, block_positions):
        ...     print(line)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
        13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
        24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
        35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
        46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56,
        57, 58, 59]
    """
    for start_position, end_position in block_sections:
        yield text[start_position:end_position]


def break_lines_at_whitespaces(text: str, maximum_line_width: int) -> str:
    """
    Breaks lines at whitespaces.

    Notes:
        Within this implementation the linewidth is not broken by block
        text elements, which exceeds the maximum line width.

    Args:
        text(str):
            Text which should be broken into lines with an maximum line width.

        maximum_line_width(int):
            The maximum line width.

    Returns:
        str

    Examples:
        >>> sample_text = str(list(range(80)))
        >>> result_as_block = break_lines_at_whitespaces(sample_text, 72)
        >>> print(result_as_block)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
        40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
        59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
        78, 79]
        >>> small_list = str(list(iter("abcdefghij")))
        >>> result_as_block = break_lines_at_whitespaces(small_list, 72)
        >>> print(result_as_block)
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    .. doctest:

        >>> sample = str(['strangely_eq', 'ual_wide_ite', 'ms_are_not_s'])
        >>> result_as_block = break_lines_at_whitespaces(sample, maximum_line_width=36)
        >>> print(result_as_block)
        ['strangely_eq', 'ual_wide_ite',
        'ms_are_not_s']
        >>> result_as_block = break_lines_at_whitespaces(sample, maximum_line_width=48)
        >>> print(result_as_block)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']

    """
    section_positions = find_section_positions_at_whitespaces(
        text=text, maximum_line_width=maximum_line_width
    )
    return LINE_BREAK.join(iter_split_text(text, block_sections=section_positions))


def _try_to_round(potentially_able_to_round: Any, digits: int) -> Any:
    """

    Args:
        potentially_able_to_round:

    Returns:

    .. doctest::

        >>> _try_to_round(1.234567, 4)
        1.2346
        >>> _try_to_round("not a number", 4)
        'not a number'
        >>> import numpy
        >>> _try_to_round(numpy.array([1.234567]), 4)
        array([1.2346])
        >>> from pandas import Series
        >>> _try_to_round(Series([1.234567]), 4)
        0    1.2346
        dtype: float64
        >>> from pandas import DataFrame
        >>> _try_to_round(DataFrame([[1.234567, "not a number"]]), 4)
                0             1
        0  1.2346  not a number
    """
    try:
        round_result = potentially_able_to_round.round(digits)
        return round_result
    except AttributeError:
        pass

    try:
        round_result = round(potentially_able_to_round, digits)
        return round_result
    except TypeError:
        return potentially_able_to_round


def round_collections(item_to_round: Any, digits: int = 3) -> Any:
    """
    Rounds items within collections (dict, list, tuple). This method also
    supports object, which implements a *round(digits)* method.

    Args:
        item_to_round(Any):
            An item with the potential to be rounded. If the item cannot be
            rounded it will be returned instead.

        digits(int):
            Remaining digits of the rounded number. Default is 3.

    Returns:
        Any

    Examples:

        >>> sample_dict = {"a_number": 1.234567, "not": "a number"}
        >>> round_collections(item_to_round=sample_dict, digits=4)
        {'a_number': 1.2346, 'not': 'a number'}
        >>> sample_list = [1.234567, "not a number"]
        >>> round_collections(item_to_round=sample_list, digits=4)
        [1.2346, 'not a number']
        >>> sample_tuple = (1.234567, "not a number")
        >>> round_collections(item_to_round=sample_tuple, digits=4)
        (1.2346, 'not a number')

        Invoking the *round(digit)* method of objects.

        >>> import numpy
        >>> sample_array = numpy.array([1.234567])
        >>> round_collections(item_to_round=sample_array, digits=4)
        array([1.2346])
        >>> from pandas import Series
        >>> sample_series = Series([1.234567])
        >>> round_collections(item_to_round=sample_series, digits=4)
        0    1.2346
        dtype: float64
        >>> from pandas import DataFrame
        >>> sample_frame = DataFrame([[1.234567, "not a number"]])
        >>> round_collections(item_to_round=sample_frame, digits=4)
                0             1
        0  1.2346  not a number

        Or just do nothing.

        >>> round_collections(item_to_round="nothing at all", digits=4)
        'nothing at all'

    """
    if isinstance(item_to_round, dict):
        round_result = {
            key: _try_to_round(item, digits) for key, item in item_to_round.items()
        }
        return round_result
    if isinstance(item_to_round, list):
        round_result = [_try_to_round(item, digits) for item in item_to_round]
        return round_result
    if isinstance(item_to_round, tuple):
        round_result = [_try_to_round(item, digits) for item in item_to_round]
        return tuple(round_result)
    return _try_to_round(potentially_able_to_round=item_to_round, digits=digits)


def doctest_print_list(object_to_print: Iterable, line_width: int = 72):
    """
    Print the content of an Iterable breaking the resulting string at whitespaces.

    Args:
        object_to_print(Any):
            The object of which a block should be printed.

        line_width(int):
            The line width on which the resulting text is broken at whitespaces.

    Examples:
        >>> sample_object = list(range(80))
        >>> doctest_print_list(sample_object)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
        21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
        40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
        59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77,
        78, 79]
        >>> small_list = list(iter("abcdefghij"))

    """
    string_representation = str(object_to_print)
    prepared_print_representation = break_lines_at_whitespaces(
        string_representation, maximum_line_width=line_width
    )
    print(prepared_print_representation)


def prepare_print(
    anything_to_print: Any,
    max_line_width: Optional[int] = 0,
    indent: Optional[str] = None,
) -> str:
    """
    Prepares anything for printing.

    Notes:
        The argument *max_line_width* will break lines a whitespaces. If the
        single text exceeds the maximum linewidth it will not be broken within
        this implementation.

    Args:
        anything_to_print(Any):
            Anything which will be converted into a string and postprocessed,
            with default methods.

        max_line_width(Optional[int]):
            Sets the maximum linewidth of the print.

        indent(str):
            Additional indentation added to the docstring.

    Returns:
       str

    Examples:
        >>> test_text = (
        ...     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed"
        ...     " do eiusmod tempor      incididunt ut labore et dolore magna"
        ...     " aliqua. Ut enim ad  minim veniam, quis nostrud exercitation"
        ...     " ullamco laboris  nisi ut  aliquip  ex ea commodo consequat."
        ... )
        >>> print(prepare_print(test_text[:84]))
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
        >>> print(prepare_print(test_text, max_line_width=60))
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
        do eiusmod tempor      incididunt ut labore et dolore magna aliqua.
        Ut enim ad  minim veniam, quis nostrud exercitation ullamco laboris
        nisi ut  aliquip  ex ea commodo consequat.
        >>> print(prepare_print(test_text, max_line_width=60, indent="    "))
            Lorem ipsum dolor sit amet, consectetur adipiscing elit,
            sed do eiusmod tempor      incididunt ut labore et dolore
            magna aliqua. Ut enim ad  minim veniam, quis nostrud exercitation
            ullamco laboris  nisi ut  aliquip  ex ea commodo consequat.
        >>> small_list = list(iter("abcdefghij"))
        >>> print(prepare_print(small_list))
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        >>> print(prepare_print(small_list, max_line_width=60))
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    .. doctest:

        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s', 'shown_here__']
        >>> doctest_print(sample, max_line_width=49)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s',
        'shown_here__']
        >>> doctest_print(sample, max_line_width=60)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s',
        'shown_here__']
        >>> doctest_print(sample, max_line_width=64)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s', 'shown_here__']

        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']
        >>> doctest_print(sample, max_line_width=36)
        ['strangely_eq', 'ual_wide_ite',
        'ms_are_not_s']
        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']
        >>> doctest_print(sample, max_line_width=48)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']

    """
    string_representation = str(anything_to_print)
    prepared_print_representation = remove_trailing_whitespaces(string_representation)
    if indent is not None:
        indent = str(indent)
        indent_count = len(indent)
    else:
        indent_count = 0
    if max_line_width > 0:
        prepared_print_representation = break_lines_at_whitespaces(
            prepared_print_representation,
            maximum_line_width=max_line_width - indent_count,
        )
    if indent is not None:
        prepared_print_representation = _indent_block(
            paragraph=prepared_print_representation, indent=indent
        )
    return prepared_print_representation


def doctest_print(
    anything_to_print: Any,
    max_line_width: Optional[int] = 0,
    indent: Optional[str] = None,
):
    """
    The general printing method for doctests.

    Notes:
        The argument *max_line_width* will break lines a whitespaces. If the
        single text exceeds the maximum linewidth it will not be broken within
        this implementation.

    Args:
        anything_to_print(Any):
            Anything which will be converted into a string and postprocessed,
            with default methods.

        max_line_width(Optional[int]):
            Sets the maximum linewidth of the print.

        indent(str):
            Additional indentation added to the docstring.

    Examples:
        >>> test_text = (
        ...     "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed"
        ...     " do eiusmod tempor      incididunt ut labore et dolore magna"
        ...     " aliqua. Ut enim ad  minim veniam, quis nostrud exercitation"
        ...     " ullamco laboris  nisi ut  aliquip  ex ea commodo consequat."
        ... )
        >>> doctest_print(test_text[:84])
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
        >>> doctest_print(test_text, max_line_width=60)
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
        do eiusmod tempor      incididunt ut labore et dolore magna aliqua.
        Ut enim ad  minim veniam, quis nostrud exercitation ullamco laboris
        nisi ut  aliquip  ex ea commodo consequat.
        >>> doctest_print(test_text, max_line_width=60, indent="    ")
            Lorem ipsum dolor sit amet, consectetur adipiscing elit,
            sed do eiusmod tempor      incididunt ut labore et dolore
            magna aliqua. Ut enim ad  minim veniam, quis nostrud exercitation
            ullamco laboris  nisi ut  aliquip  ex ea commodo consequat.
        >>> small_list = list(iter("abcdefghij"))
        >>> doctest_print(small_list)
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
        >>> doctest_print(small_list, max_line_width=60)
        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    .. doctest:

        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s', 'shown_here__']
        >>> doctest_print(sample, max_line_width=49)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s',
        'shown_here__']
        >>> doctest_print(sample, max_line_width=60)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s',
        'shown_here__']
        >>> doctest_print(sample, max_line_width=64)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s', 'shown_here__']

        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']
        >>> doctest_print(sample, max_line_width=36)
        ['strangely_eq', 'ual_wide_ite',
        'ms_are_not_s']
        >>> sample = ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']
        >>> doctest_print(sample, max_line_width=48)
        ['strangely_eq', 'ual_wide_ite', 'ms_are_not_s']

    """
    print(
        prepare_print(
            anything_to_print=anything_to_print,
            max_line_width=max_line_width,
            indent=indent,
        )
    )


def doctest_iter_print(
    iterable_to_print: Union[Mapping, Iterable],
    max_line_width: Optional[int] = 0,
    indent: Optional[str] = None,
    edits_item: Optional[Callable[[Any], Any]] = None,
):
    """
    Prints the first level of the iterable or mapping.

    Args:
        iterable_to_print(Union[Mapping, Iterable]):
            A Mapping or Iterable which first level will be iterated and printed.

        max_line_width(Optional[int]):
            Sets the maximum linewidth of the print.

        indent(Optional[str]):
            Additional indentation. The items of mappings will be indented
            additionally.

        edits_item(Callable[[Any], Any]):
            A callable which takes the 1st level item and returing the
            state, which should be printed.

    Examples:
        >>> sample_mapping = {"a": "mapping  ", "with": 3, "i": "tems  "}
        >>> doctest_iter_print(sample_mapping)
        a:
          mapping
        with:
          3
        i:
          tems
        >>> doctest_iter_print(sample_mapping, indent="..")
        ..a:
        ....mapping
        ..with:
        ....3
        ..i:
        ....tems
        >>> doctest_iter_print([1, 2, {"a": "mapping  ", "with": 3, "i": "tems  "}])
        1
        2
        {'a': 'mapping  ', 'with': 3, 'i': 'tems  '}
        >>> doctest_iter_print(["abc", "abcd", "abcde"], edits_item=lambda x: x[:3])
        abc
        abc
        abc
        >>> doctest_iter_print({"edit": 1, "item": 2}, edits_item=lambda x: x**2)
        edit:
          1
        item:
          4
        >>> sample_dict = {"first_level": {"second": "level", "a number": 1.234567}}
        >>> doctest_iter_print(sample_dict, edits_item=round_collections)
        first_level:
          {'second': 'level', 'a number': 1.235}
    """
    edit_item_before_print = edits_item is not None
    if isinstance(iterable_to_print, Mapping):
        if indent is None:
            mapping_indent = "  "
        else:
            mapping_indent = str(indent) * 2
        for key in iterable_to_print:
            item_to_print = iterable_to_print[key]
            if edit_item_before_print:
                prepared_item = edits_item(item_to_print)
            else:
                prepared_item = item_to_print
            doctest_print(
                "{}:".format(str(key)), max_line_width=max_line_width, indent=indent
            )
            doctest_print(
                prepared_item, max_line_width=max_line_width, indent=mapping_indent
            )
    elif isinstance(iterable_to_print, Iterable):
        for item_to_print in iterable_to_print:
            if edit_item_before_print:
                prepared_item = edits_item(item_to_print)
            else:
                prepared_item = item_to_print
            doctest_print(prepared_item, max_line_width=max_line_width, indent=indent)
