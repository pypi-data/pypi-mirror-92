from __future__ import annotations
import re
import fileinput
import sys
import os
import logging as log

from os.path import splitext, relpath
from collections import defaultdict
from colorama import Fore, Style  # type: ignore


def get_ext(filename: str):
    _, ext = splitext(filename)

    return ext


class BaseParser:
    exts: list[str]  # tuple of extensions
    path_pattern: str  # regex pattern to search for paths

    def __init__(self, dry=False, quiet=False):
        log.debug(f"init {self.__class__.__name__}")

        self.quiet = quiet
        self.dry = dry
        self.regex_path = re.compile(self.path_pattern)

    def rename(self, path: str) -> str:
        """rename path from absolute to relative"""
        if path.startswith("./"):
            return path[2:]

        if not path.startswith("/"):
            raise RuntimeError(f"{path} should be an absolute path")

        if path.startswith("//"):
            return path

        path = "." + path

        rel_path = relpath(path)

        return rel_path

    def parse_string(self, string: str, prefix: str = "") -> str:
        for match in self.regex_path.finditer(string):
            path = match.group(1)
            if not path:
                log.error(
                    f"{prefix}no path matched? (first group) full match = {match.group(0)}"
                )
                continue

            try:
                new_path = self.rename(path)
            except RuntimeError as e:
                log.debug(e)
                continue
            else:
                if not self.quiet:
                    print(
                        f"{prefix}{Fore.RED}{path} {Fore.WHITE}-> {Fore.GREEN}{new_path}",
                        file=sys.__stdout__,
                        end=Style.RESET_ALL + "\n",
                    )

            string = string.replace(path, new_path)

        return string

    def parse_file(self, filename: str):
        """parse a file to change all absolute paths to relative"""
        cwd = os.getcwd()

        with fileinput.input(filename, inplace=not self.dry) as f:
            for i, line in enumerate(f):
                rel_filename = relpath(filename, start=cwd)
                prefix = f"{Fore.CYAN}{rel_filename}:{i} "

                new_line = self.parse_string(line, prefix=prefix)

                if not self.dry:
                    print(new_line, end="")  # redirected to the new file


class ParseHTML(BaseParser):
    exts = [".html"]
    path_pattern = r'(?:href|src)="(.+?)"'


class ParseCSS(BaseParser):
    exts = [
        ".css",
        ".html",
    ]
    path_pattern = r'url\("(.+?)"\)'


class Parser:
    _parsers = (
        ParseHTML,
        ParseCSS,
    )

    parsers_map: defaultdict[str, list[BaseParser]]

    def __init__(self, dry=False, quiet=False):
        log.debug(f"init {self.__class__.__name__}")

        self.parsers_map = defaultdict(list)

        for parser in self._parsers:
            p = parser(dry=dry, quiet=quiet)

            for ext in parser.exts:
                self.parsers_map[ext].append(p)

    def _get_parsers(self, ext: str) -> list[BaseParser]:
        parsers = self.parsers_map.get(ext, [])

        if not parsers:
            log.debug(f"no parsers for extension {ext}")

        return parsers

    def parse_file(self, filename: str):
        ext = get_ext(filename)

        parsers = self._get_parsers(ext)

        for parser in parsers:
            parser.parse_file(filename)

    def parse_string(self, string: str, ext: str) -> str:
        parsers = self._get_parsers(ext)

        for parser in parsers:
            string = parser.parse_string(string)

        return string
