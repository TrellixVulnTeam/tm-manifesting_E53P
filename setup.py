#!/usr/bin/python3 -tt
import argparse
import os
import json
import shlex
import shutil
import subprocess
import sys

from pdb import set_trace

from utils import utils

build_config = None


def set_python_lib():
    """
        Create a symlink to manifesting source code to:
    /usr/local/lib/python3.4/dist-packages/tmms so that user could import
    manifeseting libraries as follows: import tmms.unittests
    """
    path_to_lib = sorted(sys.path)[-1]
    for path in sorted(sys.path):           # find a python3/dist-packages
        if 'python3/dist-packages' in path: # path in the python environment
            path_to_lib = path + '/tmms'    # use it to construct symlink
            break                           # break on first occurance.
    manifesting_path = os.path.realpath(__file__)
    manifesting_path = os.path.dirname(manifesting_path)    # setup script must be in top of tree
    print(' - Creating a symlink from [%s] to [%s]' % (manifesting_path, path_to_lib))
    os.symlink(manifesting_path, path_to_lib)


def _create_env(fields, ignore_list=[]):
    """
        Create folder tree based of the list of fileds passed, that must comply
    with config/build_config/ structure. This function dependent on build_config/
    module and its  variables naming convention.

    :param 'fields': [list] variable names that determines path values of the
                    manifesting entities.
    :param 'ignore_list': [list] of fields to ignore, e.g. GOLDEN_IMAGE
    """
    print(' ---- Creating manifest and tftp environment ---- ')
    for field in fields:
        if field in ignore_list:
            continue
        path = build_config.settings[field]

        print(' - ' + path)
        create_folder(path)


def create_folder(path):
    """ A simple wrapper around os.makedirs that skip existed folders. """
    try:
        if not os.path.isdir(path):
            os.makedirs(path)
    except OSError:
        raise RuntimeError('Failed to create %s' % (path))


def install_packages():
    """
        Install packages required by manifesting service.
    """
    pkg_list = ['vmdebootstrap', 'python3',
                'python3-flask', 'python3-requests',
                'python3-debian', 'tm-librarian']
    cmd = 'apt install -y %s' % (' '.join(pkg_list))
    cmd = shlex.split(cmd)
    try:
        subprocess.call(cmd)
    except subprocess.CalledProcessError:
        raise RuntimeError('Error occured during the install of packages.')


def main(args):
    """
        Run all the functions needed to setup tm-manifesting environment:
    - set PYTHONPATH using .pth file that have a path to the manifesting/ source code.
    - create folders for manifesting server and manifesting tftp based of the config file
    - run make_grub_cfg.py script to create grub config files in the tftp folder
    - run generate_golden_image.py script to generate golden image
    """
    assert os.geteuid() == 0, 'This script requires root permissions'
    install_packages()

    config_path = os.path.realpath(args['config'])

    set_python_lib()

    from configs import build_config as BC
    global build_config
    build_config = BC
    build_config.make_config(config_path)

    print()
    fields = build_config._manifest_env
    _create_env(fields, ['GOLDEN_IMAGE'])
    golden_img_dir = os.path.dirname(build_config.settings['GOLDEN_IMAGE'])
    create_folder(golden_img_dir)

    print()

    fields = build_config._tftp_env
    _create_env(fields)
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Setup arguments that should not\
                                    be changed, unless you know what you doing.')
    parser.add_argument('-c', '--config',
                        help='A config.py file to be used by manifesting server.',
                        default='./manifest_config.py')

    parser.add_argument('-C', '--tmconfig',
                        help='A config file that stores nodes topology.',
                        default='configs/hpetmconfig.py')

    args, _ = parser.parse_known_args()
    try:
        main(vars(args))
    except RuntimeError as err:
        raise SystemExit('Setup failed: %s' % err)
    except Exception as err:
        raise SystemExit('Setup failed! Something bad happened: %s' % err)
