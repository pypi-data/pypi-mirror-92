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

import datetime
import bs4
import configparser
import io
import base64
import logging
import md5
import pkg_resources
import re
import sys
import shutil
import os
try:
    # py2
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import HTTPError
except ImportError:
    # py3
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import HTTPError

try:
    import pkg_resources._vendor.packaging.version
    packaging = pkg_resources._vendor.packaging
except ImportError:
    # fallback to naturally-installed version; allows system packagers to
    #  omit vendored packages.
    import packaging.version

from p01.build import base
from p01.build import package

logger = base.logger

is_win32 = sys.platform == 'win32'


def findProjectVersions(project, config, options, uploadType):
    if options.offline:
        logger.info('Offline: Skip looking for project versions.')
        return []

    VERSION = re.compile(project+r'-(\d+\.\d+(\.\d+){0,2})')

    if uploadType == 'local':
        dest = os.path.join(config.get(base.BUILD_SECTION, 'buildout-server'),
                            project)

        versions = []
        for root, dirs, files in os.walk(dest):
            for fname in files:
                m = VERSION.search(fname)
                if m:
                    versions.append(m.group(1))
    else:
        url = config.get(base.BUILD_SECTION, 'buildout-server') + project + '/'
        logger.debug('Package Index: ' + url)
        req = Request(url)

        username = config.get(base.BUILD_SECTION, 'buildout-server-username')
        password = config.get(base.BUILD_SECTION, 'buildout-server-password')
        base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
        req.add_header("Authorization", "Basic %s" % base64string)

        try:
            soup = bs4.BeautifulSoup(urlopen(req).read(), "html.parser")
        except HTTPError as err:
            logger.error("There was an error accessing %s: %s" % (url, err))
            return []

        versions = []
        for tag in soup('a'):
            cntnt = str(tag.contents[0]) # str: re does not like non-strings
            m = VERSION.search(cntnt)
            if m:
                versions.append(m.group(1))

    return sorted(versions, key=lambda x: packaging.version.Version(x))


def getDependentConfigFiles(baseFolder, infile, addSelf=True, outfile=None,
                            hashes=None, options=None):
    # go and read all cfg files that are required by the master
    # to collect them all
    # if they have a path, modify according to that the the files are flat
    # on the server

    # baseFolder and infile might be "out of sync", because
    # we process cfg files that are already modified compared to the templates
    # in that case we want to read/write the modified file, but look for
    # the others in the template_path

    if hashes is not None:
        justname = os.path.split(infile)[-1]
        if justname not in hashes:
            hash = md5.new(open(infile, 'rb').read()).hexdigest()
            hashes[justname] = hash

    config = base.NonDestructiveRawConfigParser()
    config.read(infile)

    dependents = set()
    if addSelf:
        dependents.add(infile)

    try:
        extends = config.get('buildout', 'extends')
    except configparser.NoSectionError:
        return dependents
    except configparser.NoOptionError:
        return dependents

    extendParts = extends.split()
    hasPath = False
    for part in extendParts:
        if '/' in part or '\\' in part:
            hasPath = True

        # extends filenames are always relative to the actual file
        fullname = os.path.join(baseFolder, part)

        if is_win32:
            #most buildouts use / but win32 uses \
            fullname = fullname.replace('/', '\\')

        if not os.path.exists(fullname):
            logger.error("FATAL: %s not found, but is referenced by %s" % (
                fullname, infile))
            sys.exit(0)

        dependents.update(getDependentConfigFiles(os.path.dirname(fullname),
            fullname, hashes=hashes, options=options))

    if hasPath:
        #we need to clean relative path from extends as on the server
        #everything is flat
        extendParts = [os.path.split(part)[-1] for part in extendParts]
        extends = '\n  '.join(extendParts)

        config.set('buildout', 'extends', extends)

        if outfile:
            #if the config is created by ourselves
            # config.write(open(outfile, 'w'))
            config.writeFile(outfile, options)
        else:
            #this is a referenced config, don't modify the original
            fName = os.path.split(infile)[-1]
            # config.write(open(fName, 'w'))
            config.writeFile(fName, options)

            if addSelf:
                #adjust dependents
                dependents.remove(infile)
                dependents.add(fName)

    return dependents


def addHashes(dependencies, hashes, rename=True, options=None):
    # add hashes to files

    rdep = []
    for fname in dependencies:
        modified = False
        justname = os.path.split(fname)[-1]

        config = base.NonDestructiveRawConfigParser()
        config.read(fname)

        try:
            # 1. modify file contents
            extends = config.get('buildout', 'extends')
            for oldname, hash in list(hashes.items()):
                parts = os.path.splitext(oldname)
                newname = "%s-%s%s" % (parts[0], hash, parts[1])

                if oldname in extends:
                    extends = extends.replace(oldname, newname)
                    modified = True

            if modified:
                config.set('buildout', 'extends', extends)
        except configparser.NoSectionError:
            pass
        except configparser.NoOptionError:
            pass

        # 2. rename/copy files
        newname = justname
        if rename:
            try:
                hash = hashes[justname]
                parts = os.path.splitext(justname)
                newname = "%s-%s%s" % (parts[0], hash, parts[1])
                modified = True
            except KeyError:
                pass

        if modified:
            #RawConfigParser fools us... next time it does I'll do
            #plain replace on the file contents
            # config.write(open(newname, 'w'))
            config.writeFile(newname, options)
            rdep.append(newname)
        else:
            rdep.append(fname)

    return rdep


def build(configFile, options):
    # save the time we started
    now = datetime.datetime.now()

    # Read the configuration file.
    logger.info('Loading configuration file: ' + configFile)
    config = base.NonDestructiveRawConfigParser()
    config.read(configFile)

    # Create the project config parser
    logger.info('Creating Project Configuration')
    projectParser = base.NonDestructiveRawConfigParser()
    template_path = None
    if config.has_option(base.BUILD_SECTION, 'template'):
        template = config.get(base.BUILD_SECTION, 'template')
        logger.info('Loading Project Configuration Template: ' + template)
        projectParser.read([template])
        template_path = os.path.abspath(template)

    if not projectParser.has_section('versions'):
        projectParser.add_section('versions')

    # Determine all versions of the important packages
    pkgversions = {}
    pkginfos = {}
    for pkg in config.get(base.BUILD_SECTION, 'packages').split():
        customPath = None
        if ':' in pkg:
            pkg, customPath = pkg.split(':')
        builder = package.PackageBuilder(pkg, options)

        version = builder.runCLI(configFile, askToCreateRelease=True,
                                 forceSvnAuth = options.forceSvnAuth)

        pkgversions[pkg] = version
        pkginfos[pkg] = (builder.branchUrl, builder.branchRevision)
        projectParser.set('versions', pkg, version)

    # Get upload type
    try:
        uploadType = config.get(base.BUILD_SECTION, 'buildout-upload-type')
    except configparser.NoOptionError:
        uploadType = "webdav"

    # Stop if no buildout-server given
    try:
        config.get(base.BUILD_SECTION, 'buildout-server')
    except configparser.NoOptionError:
        logger.info('No buildout-server specified in the cfg, STOPPING')
        logger.info('Selected package versions:\n%s' % (
            '\n'.join('%s = %s' % (pkg, version)
                      for pkg, version in list(pkgversions.items()))) )
        return

    # Write the new configuration file to disk
    projectName = config.get(base.BUILD_SECTION, 'name')
    defaultVersion = configVersion = config.get(base.BUILD_SECTION, 'version')
    projectVersions = findProjectVersions(projectName, config,
                                          options, uploadType)

    # Determine new project version
    if projectVersions:
        defaultVersion = projectVersions[-1]
    if options.nextVersion or configVersion == '+':
        defaultVersion = base.guessNextVersion(defaultVersion)
    if options.forceVersion:
        if options.forceVersion in projectVersions:
            logger.error('Forced version %s already exists' % \
                options.forceVersion)
        else:
            defaultVersion = options.forceVersion
    projectVersion = base.getInput(
        'Project Version', defaultVersion, options.useDefaults)

    # Write out the new project config -- the pinned versions
    simpleProjectFilename = '%s-%s.cfg' %(projectName, projectVersion)
    projectConfigFilename = base.getFilePath(simpleProjectFilename, options)
    logger.info('Writing project configuration file: ' + projectConfigFilename)
    # projectParser.write(open(projectConfigFilename, 'w'))
    projectParser.writeFile(projectConfigFilename, options)

    filesToUpload = [simpleProjectFilename]

    try:
        hashConfigFiles = config.getboolean(base.BUILD_SECTION,
                                            'hash-config-files')
    except configparser.NoOptionError:
        hashConfigFiles = False

    # Process config files, check for dependent config files
    # we should make sure that they are on the server
    # by design only the projectConfigFilename will have variable dependencies
    if template_path:
        if hashConfigFiles:
            hashes = {}
        else:
            hashes = None

        dependencies = getDependentConfigFiles(os.path.dirname(template_path),
            projectConfigFilename, addSelf=False, outfile=projectConfigFilename,
            hashes=hashes, options=options)

        if hashConfigFiles:
            dependencies = addHashes(dependencies, hashes, options=options)
            #fix main config too
            addHashes([projectConfigFilename], hashes, rename=False,
                options=options)

        filesToUpload.extend(dependencies)

    # Dump package repo infos
    # do it here, projectConfigFilename might be rewritten by
    # getDependentConfigFiles
    projectFile = open(projectConfigFilename, 'a')
    projectFile.write('\n')
    projectFile.write('# package SVN infos:\n')
    for pkg, pkginfo in list(pkginfos.items()):
        projectFile.writelines(
            ('# %s\n' % pkg,
             '#   svn URL:%s\n' % pkginfo[0],
             '#   svn repo revision:%s\n' % pkginfo[1][0],
             '#   svn last change revision:%s\n' % pkginfo[1][1],
            ))
        logger.info('SVN info: %s: %s %s %s', pkg, pkginfo[0],
                    pkginfo[1][0], pkginfo[1][1])
    projectFile.close()

    # Create deployment configurations
    # first define a parser for load addition variable (vars) section somewhere
    # in your templates chain.
    varsParser = base.NonDestructiveRawConfigParser()
    # make sure we use the right (tempalte inheritation) order
    varsParser.read(reversed(filesToUpload))

    for section in config.sections():
        if section == base.BUILD_SECTION:
            continue
        logger.info('Building deployment configuration: %s', section)
        template_path = config.get(section, 'template')
        logger.info('Loading deploy template file: %s', template_path)
        with open(template_path, 'r') as f:
            template = f.read()
        vars = dict([(name, value)
                     for name, value in config.items(section)
                     if name != 'template'])

        # apply additional vars defined in release template section if a
        # section name is defined as vars argument
        # or keep the vars argument as is if there is no section. This is
        # usefull if someone uses the vars attribute as argument (BBB)
        vName = vars.get('vars')
        if varsParser.has_section(vName):
            # apply vars from given section as additional vars
            for name, value in varsParser.items(vName):
                if name not in vars:
                    # but only if not overriden in deployment config
                    vars[name] = value

        # apply defaults
        vars['project-name'] = projectName
        vars['project-version'] = projectVersion
        vars['instance-name'] = section

        # add current time
        vars['current-datetime'] = now.isoformat()
        vars['current-date'] = now.date().isoformat()
        vars['current-time'] = now.time().isoformat()

        # not required anymore since we use input as is,
        # see: NonDestructiveRawConfigParser for more info
        ##handle multi-line items, ConfigParser removes leading spaces
        ##we need to add some back otherwise it will be a parsing error
        #for k, v in vars.items():
        #    if '\n' in v:
        #        #add a 2 space indent
        #        vars[k] = v.replace('\n', '\n  ')

        try:
            deployConfigText = template % vars
        except KeyError as e:
            logger.error(
                "The project variant %s template %s is missing the %r "
                "argument" % (section, template_path, e.message))
            sys.exit(0)
        except Exception as e:
            logger.error(
                "The project variant %s template %s probably provides unquoted "
                "attributes. Make sure all %% get prefixed ith an additonal %% "
                "(error: %r)" % (section, template_path, e.message))
            sys.exit(0)
        deployConfigFilename = '%s-%s-%s.cfg' %(
            config.get(base.BUILD_SECTION, 'name'), section, projectVersion)
        deployConfigFilename = base.getFilePath(deployConfigFilename, options)
        deployConfig = base.NonDestructiveRawConfigParser()
        deployConfig.readfp(io.StringIO(deployConfigText))
        deployConfig.set('buildout', 'extends', simpleProjectFilename)
        logger.info('Writing deployment file: ' + deployConfigFilename)
        # deployConfig.write(open(deployConfigFilename, 'w'))
        deployConfig.writeFile(deployConfigFilename, options)
        filesToUpload.append(deployConfigFilename)

    # Upload the files
    if uploadType == 'local':
        #no upload, just copy to destination
        dest = os.path.join(config.get(base.BUILD_SECTION, 'buildout-server'),
                            projectName)
        if not os.path.exists(dest):
            os.makedirs(dest)
        for filename in filesToUpload:
            fName = base.getFilePath(filename, options)
            justfname = os.path.split(fName)[-1]
            shutil.copyfile(fName, os.path.join(dest, justfname))
    elif uploadType == 'webdav':
        if not options.offline and not options.noUpload:
            for filename in filesToUpload:
                fName = base.getFilePath(filename, options)
                base.uploadFile(
                    fName,
                    config.get(
                        base.BUILD_SECTION, 'buildout-server')+'/'+projectName,
                    config.get(base.BUILD_SECTION, 'buildout-server-username'),
                    config.get(base.BUILD_SECTION, 'buildout-server-password'),
                    options.offline)
    elif uploadType == 'mypypi':
        if not options.offline and not options.noUpload:
            server = config.get(base.BUILD_SECTION, 'buildout-server')
            if not server.endswith('/'):
                server += '/'
            url = (server + projectName + '/upload')
            boundary = "--------------GHSKFJDLGDS7543FJKLFHRE75642756743254"
            headers={"Content-Type":
                "multipart/form-data; boundary=%s; charset=utf-8" % boundary}
            for filename in filesToUpload:
                fName = base.getFilePath(filename, options)
                justfname = os.path.split(fName)[-1]
                #being lazy here with the construction of the multipart form data
                content = """--%s
Content-Disposition: form-data; name="content";filename="%s"

%s
--%s--
""" % (boundary, justfname, open(fName, 'r').read(), boundary)

                base.uploadContent(
                    content, fName, url,
                    config.get(base.BUILD_SECTION, 'buildout-server-username'),
                    config.get(base.BUILD_SECTION, 'buildout-server-password'),
                    options.offline, method='POST', headers=headers)


def main(args=None):
    # Make sure we get the arguments.
    if args is None:
        args = sys.argv[1:]
    if not args:
        args = ['-h']

    # Set up logger handler
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(base.formatter)
    logger.addHandler(handler)

    # Parse arguments
    options, args = base.parser.parse_args(args)

    logger.setLevel(logging.INFO)
    if options.verbose:
        logger.setLevel(logging.DEBUG)
    if options.quiet:
        logger.setLevel(logging.FATAL)

    try:
        build(options.configFile, options)
    except KeyboardInterrupt:
        logger.info("Quitting")
        sys.exit(0)

    # Remove the handler again.
    logger.removeHandler(handler)

    # Exit cleanly.
    sys.exit(0)
