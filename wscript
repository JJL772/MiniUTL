#! /usr/bin/env python
# encoding: utf-8
# JJL77, 2020

from waflib import Logs, Configure
import os

top = '.'


@Configure.conf
def check_pkg(conf, package, uselib_store, fragment, *k, **kw):
    errormsg = '{0} not available! Install {0} development package. Also you may need to set PKG_CONFIG_PATH environment variable'.format(package)
    confmsg = 'Checking for \'{0}\' sanity'.format(package)
    errormsg2 = '{0} isn\'t installed correctly. Make sure you installed proper development package for target architecture'.format(package)

    try:
        conf.check_cfg(package=package, args='--cflags --libs', uselib_store=uselib_store, *k, **kw )
    except conf.errors.ConfigurationError:
        conf.fatal(errormsg)

    try:
        conf.check_cxx(fragment=fragment, use=uselib_store, msg=confmsg, *k, **kw)
    except conf.errors.ConfigurationError:
        conf.fatal(errormsg2)


def options(opt):

    return

def configure(conf):
    # conf.env.CXX11_MANDATORY = False
    conf.load('fwgslib cxx11')

    if not conf.env.HAVE_CXX11:
        conf.define('MY_COMPILER_SUCKS', 1)

    nortti = {
        'msvc': ['/GR-'],
        'default': ['-fno-rtti']
    }

    conf.env.append_unique('CXXFLAGS', conf.get_flags_by_compiler(nortti, conf.env.COMPILER_CC))

    if conf.env.DEST_OS == 'android':
        conf.define('NO_STL', 1)
        conf.env.append_unique('CXXFLAGS', '-fno-exceptions')


def build(bld):
    libs = []

    # basic build: dedicated only, no dependencies
    if bld.env.DEST_OS != 'win32':
        libs += ['RT']
    else:
        libs += ['USER32']

    if bld.env.DEST_OS == 'linux':
        libs += ['RT']

    source = bld.path.ant_glob([
        '*.cpp',
    ])

    includes = [
        '.',
    ]

    bld.shlib(
        source   = source,
        target   = 'miniutl',
        features = 'cxx',
        includes = includes,
        use      = libs,
        install_path = bld.env.LIBDIR,
        subsystem = bld.env.MSVC_SUBSYSTEM
    )
