"""EditorConfig file parser

Based on code from ConfigParser.py file distributed with Python 2.6.

Licensed under PSF License (see LICENSE.PSF file).

Changes to original ConfigParser:

- Special characters can be used in section names
- Octothorpe can be used for comments (not just at beginning of line)
- Only track INI options in sections that match target filename
- Stop parsing files with when ``root = true`` is found
- Add EditorConfigFile

"""

import posixpath
import re
from codecs import open
from collections import OrderedDict
from os import sep
from os.path import dirname, exists, normpath

from toolconfig_core.ecpy.compat import u
from toolconfig_core.ecpy.exceptions import ParsingError
from toolconfig_core.ecpy.fnmatch import fnmatch


__all__ = ["ParsingError", "EditorConfigParser"]

MAX_SECTION_LENGTH = 4096
MAX_PROPERTY_LENGTH= 50
MAX_VALUE_LENGTH = 255


class EditorConfigParser(object):

    """Parser for EditorConfig-style configuration files

    Based on RawConfigParser from ConfigParser.py in Python 2.6.
    """

    # Regular expressions for parsing section headers and options.
    # Allow ``]`` and escaped ``;`` and ``#`` characters in section headers
    SECTCRE = re.compile(
        r"""

        \s *                                # Optional whitespace
        \[                                  # Opening square brace

        (?P<header>                         # One or more characters excluding
            ( [^\#;] | \\\# | \\; ) +       # unescaped # and ; characters
        )

        \]                                  # Closing square brace

        """, re.VERBOSE
    )
    # Regular expression for parsing option name/values.
    # Allow any amount of whitespaces, followed by separator
    # (either ``:`` or ``=``), followed by any amount of whitespace and then
    # any characters to eol
    OPTCRE = re.compile(
        r"""

        \s *                                # Optional whitespace
        (?P<option>                         # One or more characters excluding
            [^:=\s]                         # : a = characters (and first
            [^:=] *                         # must not be whitespace)
        )
        \s *                                # Optional whitespace
        (?P<vi>
            [:=]                            # Single = or : character
        )
        \s *                                # Optional whitespace
        (?P<value>
            . *                             # One or more characters
        )
        $

        """, re.VERBOSE
    )

    def __init__(self, filename):
        self.filename = filename
        self.options = OrderedDict()
        self.root_file = False

    def matches_filename(self, config_filename, glob):
        """Return True if section glob matches filename"""
        config_dirname = normpath(dirname(config_filename)).replace(sep, '/')
        glob = glob.replace("\\#", "#")
        glob = glob.replace("\\;", ";")
        if '/' in glob:
            if glob.find('/') == 0:
                glob = glob[1:]
            glob = posixpath.join(config_dirname, glob)
        else:
            glob = posixpath.join('**/', glob)
        return fnmatch(self.filename, glob)

    def read(self, ec_filename):
        """Read and parse single EditorConfig file"""
        try:
            fp = open(ec_filename, encoding='utf-8')
        except IOError:
            return
        self._read(fp, ec_filename)
        fp.close()

    def _read(self, fp, fpname):
        """Parse a sectioned setup file.

        The sections in setup file contains a title line at the top,
        indicated by a name in square brackets (`[]'), plus key/value
        options lines, indicated by `name: value' format lines.
        Continuations are represented by an embedded newline then
        leading whitespace.  Blank lines, lines beginning with a '#',
        and just about everything else are ignored.
        """
        in_section = False
        matching_section = False
        optname = None
        lineno = 0
        e = None                                  # None, or an exception
        while True:
            line = fp.readline()
            if not line:
                break
            if lineno == 0 and line.startswith(u('\ufeff')):
                line = line[1:]  # Strip UTF-8 BOM
            lineno = lineno + 1
            # comment or blank line?
            if line.strip() == '' or line[0] in '#;':
                continue
            # a section header or option header?
            else:
                # is it a section header?
                mo = self.SECTCRE.match(line)
                if mo:
                    sectname = mo.group('header')
                    if len(sectname) > MAX_SECTION_LENGTH:
                        continue
                    in_section = True
                    matching_section = self.matches_filename(fpname, sectname)
                    # So sections can't start with a continuation line
                    optname = None
                # an option line?
                else:
                    mo = self.OPTCRE.match(line)
                    if mo:
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        if ';' in optval or '#' in optval:
                            # ';' and '#' are comment delimiters only if
                            # preceeded by a spacing character
                            m = re.search('(.*?) [;#]', optval)
                            if m:
                                optval = m.group(1)
                        optval = optval.strip()
                        # allow empty values
                        if optval == '""':
                            optval = ''
                        optname = self.optionxform(optname.rstrip())
                        if (len(optname) > MAX_PROPERTY_LENGTH or
                            len(optval) > MAX_VALUE_LENGTH):
                            continue
                        if not in_section and optname == 'root':
                            self.root_file = (optval.lower() == 'true')
                        if matching_section:
                            self.options[optname] = optval
                    else:
                        # a non-fatal parsing error occurred.  set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        if not e:
                            e = ParsingError(fpname)
                        e.append(lineno, repr(line))
        # if any parsing errors occurred, raise an exception
        if e:
            raise e

    def optionxform(self, optionstr):
        return optionstr.lower()

class EditorConfigFile(EditorConfigParser):
    """A .editorconfig file.

    Args:
        ec_filename: The full path to the EditorConfig file to read

    Raises:
        OSError: if the file doesn't exist
    """

    def __init__(self, ec_filename):
        placeholder_filename = "\0"
        super().__init__(placeholder_filename)
        self.file_exists = False
        self.ec_filename = ec_filename

        self.read(ec_filename)

    def _read(self, *args):
        """Record the fact that the file exists.

        Do this here so that, after a settings_for() call, we know
        for sure whether the file existed at read time.
        """
        super()._read(*args)
        self.file_exists = True

    def read(self, ec_filename):
        """Read the file, throwing if it's absent.

        Raises:
            OSError: if the EC file doesn't exist
        """
        self.ec_filename = ec_filename
        super().read(ec_filename)
        if not self.file_exists:
            raise OSError(f"File {ec_filename} doesn't exist")

    def settings_for(self, target_path):
        """Return the settings for target_path, which may or may not exist.

        Args:
            target_path (str): Absolute path

        Raises:
            OSError: If the EditorConfig file passed to __init__() does not exist.
        """
        self.filename = target_path

        # Reset before reading --- start fresh with each call.
        self.options = OrderedDict()
        self.root_file = False
        self.file_exists = False

        self.read(self.ec_filename)

        return self.options
