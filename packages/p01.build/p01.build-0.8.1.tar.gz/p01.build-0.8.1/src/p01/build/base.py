##############################################################################
#
# Copyright (c) 2015 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""
$Id:$
"""
__docformat__ = "reStructuredText"

import re
import base64
try:
    import configparser
except ImportError:
    import configparser as configparser
import collections
import logging
import optparse
import os.path
import pkg_resources
import subprocess
import sys
try:
    # py2
    from urlparse import urlparse
    from httplib import HTTPConnection
    from httplib import HTTPSConnection
except ImportError:
    # py3
    from urllib.parse import urlparse
    from http.client import HTTPConnection
    from http.client import HTTPSConnection
try:
    import pkg_resources._vendor.packaging.version
    packaging = pkg_resources._vendor.packaging
except ImportError:
    # fallback to naturally-installed version; allows system packagers to
    #  omit vendored packages.
    import packaging.version

logger = logging.Logger('build')
formatter = logging.Formatter('%(levelname)s - %(message)s')

BUILD_SECTION = 'build'


def parseVersion(s):
    """pkg_resources.parse_version is deprecated"""
    component_re = re.compile(r'(\d+ | [a-z]+ | \.| -)', re.VERBOSE)
    replace = {
        'pre': 'c',
        'preview': 'c',
        '-': 'final-',
        'rc': 'c',
        'dev': '@',
    }.get

    def _parse_version_parts(s):
        for part in component_re.split(s):
            part = replace(part, part)
            if not part or part == '.':
                continue
            if part[:1] in '0123456789':
                # pad for numeric comparison
                yield part.zfill(8)
            else:
                yield '*'+part

        # ensure that alpha/beta/candidate are before final
        yield '*final'

    def old_parse_version(s):
        parts = []
        for part in _parse_version_parts(s.lower()):
            if part.startswith('*'):
                # remove '-' before a prerelease tag
                if part < '*final':
                    while parts and parts[-1] == '*final-':
                        parts.pop()
                # remove trailing zeros from each series of numeric parts
                while parts and parts[-1] == '00000000':
                    parts.pop()
            parts.append(part)
        return tuple(parts)

    for part in old_parse_version(str(s)):
        yield part


def getFilePath(fName, options):
    """Apply storage path if given and not applied"""
    if options.storagePath and not fName.startswith(options.storagePath):
        fName = '%s/%s' % (options.storagePath, fName)
    return fName


def do(cmd, cwd=None, captureOutput=True):
    logger.debug('Command: ' + cmd)
    if captureOutput:
        stdout = stderr = subprocess.PIPE
    else:
        stdout = stderr = None
    p = subprocess.Popen(
        cmd, stdout=stdout, stderr=stderr,
        shell=True, cwd=cwd)
    stdout, stderr = p.communicate()
    if stdout is None:
        stdout = "See output above"
    if stderr is None:
        stderr = "See output above"
    if p.returncode != 0:
        logger.error('An error occurred while running command: %s' %cmd)
        logger.error('Error Output: \n%s' % stderr)
        sys.exit(p.returncode)
    logger.debug('Output: \n%s' % stdout)
    return stdout


class SVN(object):

    user = None
    passwd = None
    forceAuth = False

    #TODO: spaces in urls+folder names???

    def __init__(self, user=None, passwd=None, forceAuth=False,
        trustServerCert=False):
        self.user = user
        self.passwd = passwd
        self.forceAuth = forceAuth
        self.trustServerCert = trustServerCert

    def getCommand(self, command, options):
        """Replace trust server cert marker"""
        command += ' --non-interactive'
        # add authentication
        if self.user:
            command += ' --username %s --password %s' % (self.user, self.passwd)
            if self.forceAuth:
                command += ' --no-auth-cache'
        # add trusted server certificate
        if self.trustServerCert:
            command += ' --trust-server-cert'
        if options:
            command += ' %s' % options
        return command

    def info(self, url):
        command = 'svn info'
        options = '--xml %s' % url
        command = self.getCommand(command, options)
        return do(command)

    def ls(self, url):
        command = 'svn ls'
        options = '--xml %s' % url
        command = self.getCommand(command, options)
        return do(command)

    def cp(self, fromurl, tourl, comment):
        command = 'svn cp'
        options = '-m "%s" %s %s' % (comment, fromurl, tourl)
        command = self.getCommand(command, options)
        do(command)

    def co(self, url, folder):
        command = 'svn co'
        options = '%s %s' % (url, folder)
        command = self.getCommand(command, options)
        do(command)

    def ci(self, folder, comment):
        command = 'svn ci'
        options = '-m "%s" %s' % (comment, folder)
        command = self.getCommand(command, options)
        do(command)


def getInput(prompt, default, useDefaults):
    if useDefaults:
        return default
    defaultStr = ''
    if default:
        defaultStr = ' [' + default + ']'
    value = eval(input(prompt + defaultStr + ': '))
    if not value:
        return default
    return value


def uploadContent(content, filename, url, username, password,
                  offline, method, headers=None):
    if offline:
        logger.info('Offline: File `%s` not uploaded.' %filename)
        return

    logger.debug('Uploading `%s` to %s' %(filename, url))
    pieces = urlparse(url)
    Connection = HTTPConnection
    if pieces[0] == 'https':
        Connection = HTTPSConnection

    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]

    if headers is None:
        headers = {}

    headers["Authorization"] = "Basic %s" % base64string

    conn = Connection(pieces[1])
    conn.request(
        method,
        pieces[2],
        content,
        headers)

    response = conn.getresponse()
    if ((response.status != 201 and method == 'PUT')
        or response.status != 200 and method == 'POST'):
        if response.status == 400 and 'KeyError' in response.reason:
            logger.info(
                "File upload failed with Code: %i (%s). Does this file "
                "already exist?" % (response.status, response.reason))
        else:
            logger.error("Error uploading file. Code: %i (%s)" % (
                response.status, response.reason))
    else:
        logger.info("File uploaded: %s" % filename)


def uploadFile(path, url, username, password, offline, method='PUT',
               headers=None):
    filename = os.path.split(path)[-1]

    uploadContent(open(path, 'r').read(),
                  filename, url+'/'+filename,
                  username, password, offline, method, headers=headers)


def guessNextVersion(version):
    #pkg_resources.parse_version(version)
    pieces = parseVersion(version)
    newPieces = []
    for piece in pieces:
        try:
            newPieces.append(int(piece))
        except ValueError:
            break
    newPieces += [0]*(3-len(newPieces))
    newPieces[-1] += 1
    newVersion = '.'.join([str(piece) for piece in newPieces])
    logger.debug('Last Version: %s -> %s' %(version, newVersion))
    return newVersion


leading_blank_lines = re.compile(r"^(\s*\n)+")
leading_blank_lines = re.compile(r"^(\s*\n)+")


class NonDestructiveRawConfigParser(configparser.RawConfigParser):
    """Config parser preserving whitespace

    TODO: empty lines or lines with only white space get still removed
    this means p01.build is still not useable for recipe which need to
    preserve empty lines.
    """

    def __init__(self):
        configparser.RawConfigParser.__init__(self,
            dict_type=collections.OrderedDict)

    def optionxform(self, optionstr):
        return optionstr

    def _read(self, fp, fpname):
        """Fix intend in continue line handling.

        The original config parser removes starting whitespace which will
        not work for install script content or any content as option value
        which needs to preserve leading whitespace.
        """
        cursect = None                        # None, or a dictionary
        optname = None
        lineno = 0
        e = None                              # None, or an exception
        while True:
            line = fp.readline()
            if not line:
                break # EOF

            lineno = lineno + 1

            # conditions
            if line[0] in '#;':
                # skip comment
                continue
            if line.strip() == '':
                # skip empty blank line
                continue
            if line.split(None, 1)[0].lower() == 'rem' and line[0] in "rR":
                continue

            # start collecting
            if line[0].isspace() and cursect is not None and optname:
                # continuation line
                line = line.rstrip()
                cursect[optname].append(line)
            else:
                # section header or option header?
                mo = self.SECTCRE.match(line)
                if mo:
                    sectname = mo.group('header')
                    if sectname in self._sections:
                        cursect = self._sections[sectname]
                    elif sectname == configparser.DEFAULTSECT:
                        cursect = self._defaults
                    else:
                        cursect = self._dict()
                        cursect['__name__'] = sectname
                        self._sections[sectname] = cursect
                    # So sections can't start with a continuation line
                    optname = None
                elif cursect is None:
                    if not line.strip():
                        continue
                    # no section header in the file?
                    raise configparser.MissingSectionHeaderError(fpname,
                        lineno, line)
                else:
                    mo = self._optcre.match(line)
                    if mo:
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        optname = self.optionxform(optname.rstrip())
                        # This check is fine because the OPTCRE cannot
                        # match if it would set optval to None
                        if optval is not None:
                            if vi in ('=', ':') and ';' in optval:
                                # ';' is a comment delimiter only if it follows
                                # a spacing character
                                pos = optval.find(';')
                                if pos != -1 and optval[pos-1].isspace():
                                    optval = optval[:pos]
                            optval = optval.rstrip()
                            # allow empty values
                            if optval == '""':
                                optval = ''
                            cursect[optname] = [optval]
                    elif not (optname or line.strip()):
                        # skip blank line after section start
                        continue
                    else:
                        # a non-fatal parsing error occurred.  set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        if not e:
                            e = configparser.ParsingError(fpname)
                        e.append(lineno, repr(line))
        # if any parsing errors occurred, raise an exception
        if e:
            raise e

        # join the multi-line values collected while reading
        all_sections = [self._defaults]
        all_sections.extend(list(self._sections.values()))
        for options in all_sections:
            for name, val in list(options.items()):
                if isinstance(val, list):
                    options[name] = '\n'.join(val)

    def writeFile(self, fName, options):
        """Write an .ini-format representation of the configuration state.

        Enhanced support for buildout specfic "+=" key/value options e.g.
        [buildout]
        extends = foo-parts.cfg
        parts += foo

        Previous version generated parts + = foo. But this now fails since
        buildout >= 2.0

        """
        fName = getFilePath(fName, options)
        fp = open(fName, 'w')
        if self._defaults:
            fp.write("[%s]\n" % configparser.DEFAULTSECT)
            for (key, value) in list(self._defaults.items()):
                fp.write("%s = %s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in list(self._sections[section].items()):
                if key == "__name__":
                    continue
                if (value is not None) or (self._optcre == self.OPTCRE):
                    # NOTE: this supports parts += ... and prevents to split
                    # the += into "+ =" which would fail later using zc.buildout
                    if key.endswith(' +') or key.endswith(' -'):
                        key = "= ".join((key, str(value)))
                    else:
                        key = " = ".join((key, str(value)))
                fp.write("%s\n" % (key))
            fp.write("\n")


parser = optparse.OptionParser()
parser.add_option(
    "-c", "--config-file", action="store",
    dest="configFile", metavar="FILE",
    help="The file containing the configuration of the project.")

parser.add_option(
    "-q", "--quiet", action="store_true",
    dest="quiet", default=False,
    help="When specified, no messages are displayed.")

parser.add_option(
    "-v", "--verbose", action="store_true",
    dest="verbose", default=False,
    help="When specified, debug information is created.")

parser.add_option(
    "-d", "--use-defaults", action="store_true",
    dest="useDefaults", default=False,
    help="When specified, no user input is required and the defaults are used.")

parser.add_option(
    "-o", "--offline-mode", action="store_true",
    dest="offline", default=False,
    help="When set, no server commands are executed.")

parser.add_option(
    "-n", "--next-version", action="store_true",
    dest="nextVersion", default=False,
    help="When set, the system guesses the next version to generate.")

parser.add_option(
    "--force-version", action="store",
    dest="forceVersion", default="", metavar="VERSION",
    help="Force one common version through all packages and configs.")

parser.add_option(
    "--default-package-version", action="store",
    dest="defaultPackageVersion", default="", metavar="VERSION",
    help="Set a default package version for not yet released ones.")

parser.add_option(
    "--force-svnauth", action="store_true",
    dest="forceSvnAuth", default=False,
    help="Force svn authentication with svn-repos- credentials.")

parser.add_option(
    "-b", "--use-branch", action="store",
    dest="branch", metavar="BRANCH", default=None,
    help="When specified, this branch will be always used.")

parser.add_option(
    "-i", "--independent-branches", action="store_true",
    dest="independent", metavar="INDEPENDENT", default=False,
    help=("When specified, the system makes sure the last release is based "
         "on the given branch."))

parser.add_option(
    "--no-upload", action="store_true",
    dest="noUpload", default=False,
    help="When set, the generated configuration files are not uploaded.")

parser.add_option(
    "--no-branch-update", action="store_true",
    dest="noBranchUpdate", default=False,
    help=("When set, the branch is not updated with a new version after a "
         "release is created."))

parser.add_option(
    "-s", "--storage-path", action="store",
    dest="storagePath", default=None,
    help=("Generate config files in this folder"))
