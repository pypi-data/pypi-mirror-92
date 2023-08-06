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

import bs4
import base64
import logging
import optparse
import pkg_resources
import re
import sys
import os.path
try:
    # py2
    from urlparse import urlparse
    from urllib2 import urlopen
    from urllib2 import Request
except ImportError:
    # py3
    from urllib.parse import urlparse
    from urllib.request import urlopen
    from urllib.request import Request
try:
    import pkg_resources._vendor.packaging.version
    packaging = pkg_resources._vendor.packaging
except ImportError:
    # fallback to naturally-installed version; allows system packagers to
    #  omit vendored packages.
    import packaging.version

from p01.build import base

logger = base.logger

is_win32 = sys.platform == 'win32'


class Installer(object):
    """Installer used at installing server"""

    def __init__(self, options):
        self.options = options

    def getProjects(self):
        logger.debug('Package Index: ' + self.options.url)
        req = Request(self.options.url)

        if self.options.username:
            base64string = base64.encodestring(
                '%s:%s' % (self.options.username, self.options.password))[:-1]
            req.add_header("Authorization", "Basic %s" % base64string)

        soup = bs4.BeautifulSoup(urlopen(req).read(), "html.parser")
        projects = [tag.get('href').replace('/', '')
                    for tag in soup('a')
                    if tag.parent.name == 'td' and tag.get('href') != '/']
        projects = sorted(projects)
        logger.debug('Found projects: %s' %' '.join(projects))
        return projects

    def getVariants(self, project):
        logger.debug('Package Index: ' + self.options.url)
        if not self.options.url.endswith('/'):
            self.options.url += '/'
        req = Request(self.options.url + project)

        if self.options.username:
            base64string = base64.encodestring(
                '%s:%s' % (self.options.username, self.options.password))[:-1]
            req.add_header("Authorization", "Basic %s" % base64string)

        soup = bs4.BeautifulSoup(urlopen(req).read(), "html.parser")
        variants = []
        for tag in soup('a'):
            text = tag.contents[0]
            if not text.startswith(project):
                continue
            if len(text.split('-')) != 3:
                continue
            variant = text.split('-')[1]
            if variant in variants:
                continue
            variants.append(variant)
        variants = sorted(variants)
        logger.debug('Found variants: %s' %' '.join(variants))
        return variants

    def getVersions(self, project, variant):
        logger.debug('Package Index: ' + self.options.url)
        req = Request(self.options.url + project)

        if self.options.username:
            base64string = base64.encodestring(
                '%s:%s' % (self.options.username, self.options.password))[:-1]
            req.add_header("Authorization", "Basic %s" % base64string)

        soup = bs4.BeautifulSoup(urlopen(req).read(), "html.parser")
        versions = []
        for tag in soup('a'):
            text = tag.contents[0]
            if not text:
                continue
            text = str(text)
            if not text.startswith(project+'-'+variant):
                continue
            version = text.split('-')[-1][:-4]
            if version in versions:
                continue
            versions.append(version)
        versions = sorted(
            versions, key=lambda x: packaging.version.Version(x))
        logger.debug('Found versions: %s' %' '.join(versions))
        return versions

    def runCLI(self):
        # 1. Get the project to be installed.
        project = self.options.project
        if project is None:
            projects = self.getProjects()
            print('Projects')
            for name in projects:
                print('  * ' + name)
            project = base.getInput('Project', projects[0], False)
        # 2. Get the variant of the project.
        variant = self.options.variant
        if variant is None:
            variants = self.getVariants(project)
            print('Variants')
            for name in variants:
                print('  * ' + name)
            if not variants:
                logger.error(
                    "No variants found, this script only works with variants.")
                sys.exit(0)
            variant = base.getInput('Variant', variants[0], False)
        # 3. Get the version of the project.
        version = self.options.version
        if version is None:
            versions = self.getVersions(project, variant)
            if len(versions) == 0:
                print("Sorry, but there have not been any", project, variant, "releases yet.")
                sys.exit(0)
            if self.options.latest:
                version = versions[-1]
            else:
                print('Versions')
                for name in versions:
                    print('  * ' + name)
                version = base.getInput('Version', versions[-1], False)
        # 4. Install the package
        url = self.options.url

        if self.options.username:
            #add username and password if present so that buildout can access
            #the URL without prompting
            parts = urlparse(url)
            url = '%s://%s:%s@%s' % (parts[0], self.options.username,
                                     self.options.password, ''.join(parts[1:]))

        options = []
        if self.options.verbose:
            options.append('-vv')

        if self.options.overrideDir:
            overrideDir = self.options.overrideDir
            #make it absolute if it's not
            #buildout does not like relative, buildbot cannot do absolute
            if is_win32:
                isAbs = overrideDir[0].lower().isalpha() and overrideDir[1]==':'
                if not isAbs:
                    overrideDir = os.path.abspath(overrideDir)
            else:
                isAbs = overrideDir.startswith('/')
                if not isAbs:
                    overrideDir = os.path.abspath(overrideDir)

            options.append('buildout:directory=%s' % overrideDir)

        cfgFile = '%s%s/%s-%s-%s.cfg' % (url, project, project, variant, version)

        base.do('%s -t %s %s -c %s' %(
                self.options.buildout,
                self.options.timeout,
                ' '.join(options),
                cfgFile),
                captureOutput=False)


parser = optparse.OptionParser()
parser.add_option(
    "-u", "--url", action="store",
    dest="url", metavar="URL",
    help="The base URL at which the releases can be found.")

parser.add_option(
    "-p", "--project", action="store",
    dest="project", metavar="PROJECT",
    help="The name of the project to be installed.")

parser.add_option(
    "-V", "--variant", action="store",
    dest="variant", metavar="VARIANT",
    help="The variant of the project to be installed.")

parser.add_option(
    "-v", "--version", action="store",
    dest="version", metavar="VERSION",
    help="The version of the project to be installed.")

parser.add_option(
    "--directory", action="store",
    dest="overrideDir", metavar="FOLDER", default=None,
    help="Override installation target folder")

parser.add_option(
    "-l", "--latest", action="store_true",
    dest="latest", default=False,
    help="When specified, the latest version will be chosen.")

parser.add_option(
    "--username", action="store",
    dest="username", metavar="USER", default=None,
    help="The username needed to access the site.")

parser.add_option(
    "--password", action="store",
    dest="password", metavar="PASSWORD",
    help="The password needed to access the site.")

parser.add_option(
    "-b", "--buildout-path", action="store",
    dest="buildout", metavar="PATH", default="buildout",
    help="The path to the buildout executable.")

parser.add_option(
    "--quiet", action="store_true",
    dest="quiet", default=False,
    help="When specified, no messages are displayed.")

parser.add_option(
    "--verbose", action="store_true",
    dest="verbose", default=False,
    help="When specified, debug information is created.")

parser.add_option(
    "--timeout", action="store", type="int", default=2,
    dest="timeout", metavar="TIMEOUT",
    help="Socket timeout passed on to buildout.")


def main(args=None):
    # Make sure we get the arguments.
    if args is None:
        args = sys.argv[1:]
    if not args:
        args = ['-h']

    # Set up logger handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(base.formatter)
    logger.addHandler(handler)

    # Parse arguments
    options, args = parser.parse_args(args)

    logger.setLevel(logging.INFO)
    if options.verbose:
        logger.setLevel(logging.DEBUG)
    if options.quiet:
        logger.setLevel(logging.FATAL)

    installer = Installer(options)

    try:
        installer.runCLI()
    except KeyboardInterrupt:
        logger.info("Quitting")
        sys.exit(0)

    # Remove the handler again.
    logger.removeHandler(handler)

    # Exit cleanly.
    sys.exit(0)
