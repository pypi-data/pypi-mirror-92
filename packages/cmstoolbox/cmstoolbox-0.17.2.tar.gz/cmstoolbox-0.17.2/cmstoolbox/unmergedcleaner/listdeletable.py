#! /usr/bin/env python

# pylint: disable=redefined-builtin, anomalous-backslash-in-string, too-complex, global-statement, redefined-outer-name, invalid-name, import-error

"""
This script is located as :file:`SiteAdminToolkit/unmerged-cleaner/ListDeletable.py`.
After cloning the repository, it can immediately be run by::

    cd SiteAdminToolkit/unmerged-cleaner
    ./ListDeletable.py

It depends on the ``configtools.py`` module too, so it must be run from
the ``unmerged-cleaner`` directory or the directory must be added to your ``$PYTHONPATH``.
It is used to list directories that can be removed and stores this list in a simple text file.
The directories listed are in PFN format.

.. _listdel-config-ref:

Configuration
+++++++++++++

The first time you run :file:`ListDeletable.py`, the file :file:`config.py`
will be generated by the :ref:`unmerged-config-ref-ref`.
This will attempt to determine the site it is being run at through the hostname of the node
and set **SITE_NAME** accordingly.
However, you should check the default values since there are other values that can be changed.
In particular, the **STORAGE_TYPE** may affect whether or not the script runs optimally at the site.
The various configuration options inside ``config.py`` are listed below.

%s

.. _listdel-running-ref:

Running
+++++++

After creating and checking the :file:`config.py`, the ``ListDeletable.py`` script can be run again
to write a list of directory or file PFNs that can be removed.
We expect most site admins to have tools to correctly remove those directories.
However, available tools for removing directories or files in this list are given under
:ref:`unmerged-delete-ref`.

.. _listdel-optim-ref:

Potential Optimization
++++++++++++++++++++++

This script was originally developed on a Hadoop system and unit tested on POSIX.
There are three different functions that interact with the file system which could potentially
be broken or unoptimized for other types of file systems.
These functions are :py:func:`list_folder`, :py:func:`get_file_size`,
:py:func:`do_delete`, and :py:func:`get_mtime`.
Anyone who wants to contribute optimized versions of these functions,
depending on the value of :py:data:`config.STORAGE_TYPE`
(as it is called from within ``ListDeletable.py``)
is welcome to make pull requests.

:authors: Christoph Wissing <christoph.wissing@desy.de> \n
          Max Goncharov <maxi@mit.edu> \n
          Daniel Abercrombie <dabercro@mit.edu>
"""

from __future__ import print_function

import json
import os
import sys
import time
import datetime
import subprocess
import shutil
import logging
from bisect import bisect_left
from optparse import OptionParser

from ..webtools import get_json

from . import configtools


LOG = logging.getLogger(__name__)


if __name__ == '__main__':
    PARSER = OptionParser('Usage: ./%prog [options]\n\n'
                          '  This script can list and delete directories over the course of\n'
                          '  multiple runs. The first time is it run, it generates a file,\n'
                          '  config.py. Edit config.py so that it points to the correct LFN and\n'
                          '  PFN names, along with targets the proper storage type. The second\n'
                          '  time it runs, this script creates a list of directories to delete.\n'
                          '  These directories can then be deleted with this script by passing\n'
                          '  the --delete flag.\n\n'
                          ' See http://cms-comp-ops-tools.readthedocs.io/en/latest/'
                          'siteadmintoolkit.html#module-ListDeletable for more details.')

    PARSER.add_option('--delete', action='store_true', dest='do_delete',
                      help=('This flag cause the script to operate in deletion mode. '
                            'The script has to create the deletion file before this mode '
                            'can be activated so that the site admin can take a look by '
                            'hand at the deletion list.'))

    (OPTS, ARGS) = PARSER.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s')


config = None

def set_config(path=None, key=None):
    """
    Sets the configuration up.
    This can either be from a static JSON file, or a dynamic module.
    The module must lie in the sys.path and be named config.py.
    This function only does anything the first time it's called.

    :param str path: Path to JSON file. If None (default),
                     loads the first module found called config,
                     or generates a module in the working directory and quits.
    :param str key: The key to search for the unmerged cleaner configuration.
                    This allows nesting inside other configuration files.
    """

    global config

    if config is None:
        if path:
            from . import _config as config # pylint: disable = import-outside-toplevel

            with open(path, 'r') as infile:
                fileconfig = json.load(infile)
            if key:
                fileconfig = fileconfig[key]

            # Now overwrite the defaults
            for variable, value in fileconfig.iteritems():
                setattr(config, variable, value)

        else:
            try:
                import config               # pylint: disable = import-outside-toplevel

            except ImportError:
                print('Generating default configuration...')
                configtools.generate_default_config()

                print('\nConfiguration created at config.py.')
                print('Please correct the default values to match your site')
                print('and run this script again.')
                sys.exit()


class SuspiciousConditions(Exception):
    """
    An exception for catching anticipated configuration an tool problems.
    """
    pass


class DataNode(object):
    """
    An object that holds other DataNodes inside of it.
    If a single DataNode is removable, then all nodes under it are removable too.
    Removability is determined by the list of protected directories and the directory age.
    """

    def __init__(self, path_name):
        """
        Initializes the DataNode.
        :param str path_name: is the path to the directory that defines this DataNode
        """
        self.path_name = path_name
        self.sub_nodes = []
        self.can_vanish = None
        self.latest = 0
        self.nsubnodes = 0
        self.nsubfiles = 0
        self.size = 0

    def fill(self):
        """
        Fills this DataNode's sub_node member with all DataNodes made by subdirectories.
        Recursively builds the full tree.
        """

        lfn_path_name = os.path.join(config.LFN_TO_CLEAN, self.path_name)

        # If protected, cannot delete this DataNode, and stop filling
        if bi_search(ALL_LENGTHS, len(lfn_path_name)) and \
                bi_search(PROTECTED_LIST, lfn_path_name):
            self.can_vanish = False

        else:
            full_path_name = os.path.join(config.UNMERGED_DIR_LOCATION, self.path_name)

            # Here we invoke method that might not work on all storage systems
            # Check list_folder()

            dirs = list_folder(full_path_name, 'subdirs')
            all_files = list_folder(full_path_name, 'files')

            for subdir in dirs:
                sub_node = DataNode(os.path.join(self.path_name, subdir))
                sub_node.fill()
                self.sub_nodes.append(sub_node)

            # Get the latest modification start for all files
            for file_name in all_files:
                modtime = get_mtime(full_path_name + '/' + file_name)
                self.size = self.size + get_file_size(full_path_name + '/' + file_name)
                if modtime > self.latest:
                    self.latest = modtime

            self.can_vanish = True

            for sub_node in self.sub_nodes:
                # Add one to include the subnode in the loop
                self.nsubnodes += sub_node.nsubnodes + 1
                self.nsubfiles += sub_node.nsubfiles
                self.size += sub_node.size

                if not sub_node.can_vanish:
                    self.can_vanish = False

                if sub_node.latest > self.latest:
                    self.latest = sub_node.latest

            self.nsubfiles += len(all_files)

            if self.nsubnodes == 0 and self.nsubfiles == 0:
                # Check that this time function works for your system as well
                self.latest = get_mtime(full_path_name)

            if (NOW - self.latest) < config.MIN_AGE or lfn_path_name in PROTECTED_UPPER_DIRS:
                self.can_vanish = False

    def traverse_tree(self, list_to_del):
        """
        Searches the tree for directories that can be deleted
        and appends them to a list of directories to delete.

        :param list list_to_del: is a list of directories that
                                can be deleted by a cleaner.
        """

        if self.can_vanish:
            list_to_del.append(self)
        else:
            for sub_node in self.sub_nodes:
                sub_node.traverse_tree(list_to_del)


def bi_search(thelist, item):
    """Performs a binary search

    :param list thelist: is the list to search
    :param item: is the item to determine if it's in *thelist* or not
    :type item: int or str
    :returns: whether or not *item* is in *thelist*
    :rtype: bool
    """

    # Check that the list has non-zero length and
    # if the bisected result is equal to the search term
    if thelist:
        index = bisect_left(thelist, item)
        if index != len(thelist) and thelist[index] == item:
            return True

    # If not returned True, then the item is not in the list
    return False


def list_folder(name, opt):
    """
    Lists the directories or files in a parent directory.

    .. Note::

       This can potentially be optimized for different filesystems.

    :param str name: is the name of the directory to list.
    :param str opt: determines what to list inside the directory.
                    If 'subdirs', then only directories are listed.
                    If any other value, only files inside directory
                    *name* are listed.
    :returns: a list of directories or files in a directory.
    :rtype: list
    """

    # This is where the call is made depending on what
    # file system the site is running, should add more as we go on
    if opt == 'subdirs':
        # Return list of directories
        the_filter = os.path.isdir
    else:
        # Return list of files
        the_filter = os.path.isfile

    return [listing for listing in os.listdir(name) if
            the_filter(os.path.join(name, listing))]


def get_mtime(name):
    """
    Get the modification time for a directory or file.

    .. Note::

       This can potentially be optimized for different filesystems.

    :param str name: Name of directory or file
    :returns: Modification time
    :rtype: int
    """

    return os.stat(name).st_mtime


def get_file_size(name):
    """
    Get the size of a file.

    .. Note::

       This can potentially be optimized for different filesystems.
       There's no real use for this function though besides reporting back the user,
       so go ahead and return 0 or something if you want to.

    :param str name: Name of file
    :returns: File size, in bytes
    :rtype: int
    """

    return os.stat(name).st_size


def get_protected():
    """
    :returns: the protected directory LFNs.
    :rtype: list
    :raises SuspiciousConditions: If the protected LFN list can't be downloaded.
    """

    response = get_json('cmsweb.cern.ch', '/wmstatsserver/data/protectedlfns',
                        use_cert=True)

    protected = response.get('result')

    if protected is None:
        raise SuspiciousConditions('Could not protected list')

    return protected


def lfn_to_pfn(lfn):
    """
    :param str lfn: is the LFN of a file
    :returns: the PFN
    :rtype: str
    """

    pfn = lfn.replace(config.LFN_TO_CLEAN, config.UNMERGED_DIR_LOCATION)
    return pfn


def hadoop_delete(directory, mount_point='/mnt/hadoop'):
    """
    Does the deletion for Hadoop sites.

    :param str directory: The directory name for hdfs to delete.
                          This is not exactly the same as the LFN or PFN.
    :param str mount_point: The location of the hadoop mount point.
    """

    # Check if path is still there in case checksum is actually in a different place
    # than we are expecting at the moment.
    if os.path.exists(os.path.normpath(os.path.sep.join([mount_point, directory]))):
        command = 'hdfs dfs -rm -r %s' % directory
        LOG.info('Will do: %s', command)
        time.sleep(config.SLEEP_TIME)
        os.system(command)


def dcache_delete(directory):
    """
    Does the deletion for dCache sites.

    :param str directory: The directory name for dCache to delete
    """
    LOG.error('Not implimented yet. %s has not been deleted.', directory)
    LOG.error('Try posix or editing dcache_delete() in ListDeletable.py')


def do_delete():
    """
    Does the deletion for a site based on the deletion file contents.
    If the deletion file does not exist a message is printed to the user
    and the script exits.

    .. Note::

       This can potentially be optimized for different filesystems.

    .. Warning::

       **For Hadoop sites:**
       Currently, we assume your Hadoop instance is mounted at `/mnt/hadoop`
       and the checksums are located under `/mnt/hadoop/cksums`.
       If this is not the case, the cksums will not be deleted.
       Your LFN will still be properly propagated to delete
       the unmerged files themselves.
    """

    if not os.path.isfile(config.DELETION_FILE):
        LOG.error('Deletion file %s has not been created yet.', config.DELETION_FILE)
        sys.exit()

    if config.WHICH_LIST != 'directories':
        LOG.info('-' * 40)
        LOG.info('Deleting individual files.')
        LOG.info('Your sleep time is set to %s seconds.', config.SLEEP_TIME)
        LOG.info('To change it, edit your config.py.')
        LOG.info('-' * 40)

    with open(config.DELETION_FILE, 'r') as deletions:
        for deleted in deletions.readlines():
            deleting = deleted.strip('\n')

            # Do a check of the directory names. End process if something is wrong.
            if '/unmerged/' not in deleting:
                LOG.error('Something is either wrong with your deletions file or')
                LOG.error('ListDetetable.do_delete().')
                LOG.error('Your deletions file is at %s', config.DELETION_FILE)
                LOG.error('Refusing to continue.')
                sys.exit()

            if config.WHICH_LIST == 'directories':

                if config.STORAGE_TYPE == 'hadoop':
                    # Hadoop stores also a directory with checksums
                    hadoop_delete(deleting.replace('/mnt/hadoop', '/cksums'))
                    # Delete the unmerged directory
                    hadoop_delete(deleting.replace('/mnt/hadoop', ''))

                elif config.STORAGE_TYPE == 'dcache':
                    dcache_delete(deleting)

                else:
                    # The default, 'posix', goes here
                    LOG.warning('About to delete %s', deleting)
                    time.sleep(config.SLEEP_TIME)
                    shutil.rmtree(deleting)

            else:
                if os.path.isfile(deleting):
                    LOG.warning('About to delete %s', deleting)
                    time.sleep(config.SLEEP_TIME)
                    os.remove(deleting)


def get_unmerged_files():
    """
    :returns: the old files' PFNs in the unmerged directory
    :rtype: list
    """

    find_cmd = 'find {0} -type f -not -newermt \'-{1} seconds\' -print'.format(
        config.UNMERGED_DIR_LOCATION, config.MIN_AGE)

    LOG.info('About to run:')
    LOG.info(find_cmd)

    out = subprocess.Popen(find_cmd, shell=True, stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, _ = out.communicate()
    return stdout.decode().split()


def get_unmerged_files_hadoop():
    """
    :returns: the old files' PFNs in the unmerged directory
    :rtype: list
    """

    older_than_timestamp = int(time.time()) - config.MIN_AGE
    hdfs_cmd = "hdfs dfs -ls -R {0} | grep -v '^d' | sed '1d;s/  */ /g' | cut -d\  -f6-8".format(
        config.LFN_TO_CLEAN)

    LOG.info('About to run:')
    LOG.info(hdfs_cmd)

    out = subprocess.Popen(hdfs_cmd, shell=True, stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, _ = out.communicate()
    all_files = stdout.decode().split("\n")
    unmerged_files = []
    for file_line in all_files:
        tmp_line = file_line.split()
        if not tmp_line:
            continue
        file_date = "%s %s" % (tmp_line[0], tmp_line[1])
        file_date = int(
            time.mktime(
                datetime.datetime.strptime(
                    file_date, "%Y-%m-%d %H:%M").timetuple()))

        if file_date < older_than_timestamp:
            unmerged_files.append(file_line[2])
    return unmerged_files


def filter_protected(unmerged_files, protected):
    """
    Lists unprotected files

    :param list unmerged_files: the list of files to check and delete, if unprotected.
    :param list protected: the list of protected LFNs.
    :raises SuspiciousConditions: If the beginning of the file name does not match the
                                  configured location of ``/store/unmerged``
                                  or if there is a partial match with a protected LFN
    """

    LOG.info('Got %i deletion candidates', len(unmerged_files))
    LOG.info('Have %i protected dirs', len(protected))
    LOG.info('Have %i avoided dirs', len(config.DIRS_TO_AVOID))
    n_protect = 0
    n_delete = 0
    output = []

    # Double check this
    if not protected:
        raise SuspiciousConditions(
            '\nNo directories are protected.\n'
            'Check https://cmst2.web.cern.ch/cmst2/unified/listProtectedLFN.txt')

    # Speed up by comparing two sorted lists
    protected.sort()
    unmerged_files.sort()

    iter_protect = iter(protected)
    get_next = iter_protect.next \
        if 'next' in dir(iter_protect) else \
        iter_protect.__next__

    pfn = lfn_to_pfn(get_next())      # We should never have 0 protected here

    for unmerged_file in unmerged_files:
        if not unmerged_file.startswith(config.UNMERGED_DIR_LOCATION):
            raise SuspiciousConditions(
                '\nFile %s\nis not in your configured unmerged location:\n%s' %
                (unmerged_file, config.UNMERGED_DIR_LOCATION))

        protect = False
        while pfn < unmerged_file:

            if unmerged_file.startswith(pfn):
                protect = True
                break

            try:
                pfn = lfn_to_pfn(get_next())
            except StopIteration:
                pfn = 'None'  # Paths start with '/', so this never satisfies pfn < unmerged_file
                break

            if not pfn.startswith(config.UNMERGED_DIR_LOCATION):
                raise SuspiciousConditions(
                    '\nDirectory %s\nis not in your configured unmerged location:\n%s' %
                    (pfn, config.UNMERGED_DIR_LOCATION))

        if not protect:
            for root_dir in config.DIRS_TO_AVOID:
                if os.path.join(config.UNMERGED_DIR_LOCATION, root_dir) in unmerged_file:
                    protect = True
                    break

        if not protect:
            output.append(unmerged_file)
            n_delete += 1
        else:
            n_protect += 1

    with open(config.DELETION_FILE, 'w') as deletions:
        deletions.write('\n'.join(output))

    LOG.info('Number to delete: %i', n_delete)
    LOG.info('Number protected/avoided: %i', n_protect)


def main():
    """
    Does the full listing for the site given in the :file:`config.py` file.
    """

    # Do the old behavior if not set yet
    set_config()

    # Perform some checks of configuration file
    if not config.UNMERGED_DIR_LOCATION.endswith('/unmerged'):
        raise SuspiciousConditions(
            '\n\'/unmerged\' not at the end of your PFN path: %s\n'
            'This tool replaces the \'/store/unmerged\' part of the LFN with your PFN path.\n'
            '(So it will expect \'/store/unmerged/protected/dir\' at \'%s\')\n'
            'If that is intended, please modify the beginning of this script\'s main() function.'
            % (config.UNMERGED_DIR_LOCATION, lfn_to_pfn('/store/unmerged/protected/dir')))

    # Expect protected LFN list from Unified
    if not PROTECTED_LIST:
        raise SuspiciousConditions(
            '\nNo directories are protected.\n'
            'Check https://cmst2.web.cern.ch/cmst2/unified/listProtectedLFN.txt')

    # Start checks
    if config.WHICH_LIST == 'files':
        unmerged_files = get_unmerged_files_hadoop() \
            if config.STORAGE_TYPE == 'hadoop' else \
            get_unmerged_files()

        filter_protected(unmerged_files, PROTECTED_LIST)

    elif config.WHICH_LIST == 'directories':
        for directory in PROTECTED_LIST:
            parent = os.path.dirname(directory)
            while parent and parent != '/':
                PROTECTED_UPPER_DIRS.add(parent)
                parent = os.path.dirname(parent)

        LOG.info("Some statistics about what is going to be deleted")
        LOG.info("# Folders  Total    Total  DiskSize  FolderName")
        LOG.info("#          Folders  Files  [GB]                ")

        # Get the location of the PFN and the subdirectories there

        dirs = [subdir for subdir in list_folder(config.UNMERGED_DIR_LOCATION, 'subdirs') \
                    if subdir not in config.DIRS_TO_AVOID]

        dirs_to_delete = []

        tot_upper_dirs = 0
        tot_dirs = 0
        tot_files = 0
        tot_site = 0

        for subdir in dirs:
            top_node = DataNode(subdir)
            top_node.fill()

            list_to_del = []
            top_node.traverse_tree(list_to_del)

            if not list_to_del:
                continue

            num_todelete_dirs = 0   # Number of directories to be deleted
            num_todelete_files = 0  # Number of files to be deleted
            todelete_size = 0       # Amount of space to be deleted (in GB, eventually)

            for item in list_to_del:
                num_todelete_dirs += item.nsubnodes
                num_todelete_files += item.nsubfiles
                todelete_size += item.size

            todelete_size /= (1024 * 1024 * 1024)
            LOG.info("  %-8d %-8d %-6d %-9d %-s",
                     len(list_to_del), num_todelete_dirs, num_todelete_files,
                     todelete_size, subdir)

            tot_upper_dirs += len(list_to_del)
            tot_dirs += num_todelete_dirs
            tot_files += num_todelete_files
            tot_site += todelete_size

            dirs_to_delete.extend(list_to_del)

        LOG.info("-" * 30)
        LOG.info("  %-8d %-8d %-6d %-9d TOTALS", tot_upper_dirs, tot_dirs, tot_files, tot_site)

        deletion_dir = os.path.dirname(config.DELETION_FILE)
        if not os.path.exists(deletion_dir):
            os.makedirs(deletion_dir)

        with open(config.DELETION_FILE, 'w') as del_file:
            del_file.write(
                '\n'.join(
                    [os.path.join(config.UNMERGED_DIR_LOCATION, item.path_name) \
                         for item in dirs_to_delete]
                    ) + '\n')

    else:
        LOG.error('The WHICH_LIST parameter in config.py is not valid.')


# Generate documentation for the options in the configuration file.
__doc__ %= '\n'.join(['- **%s** - %s' % (var, configtools.DOCS[var].replace('\n', ' '))
                      for var in configtools.VAR_ORDER])

NOW = int(time.time())


if __name__ == '__main__':

    if OPTS.do_delete:
        do_delete()

    else:
        # The list of protected directories to not delete
        PROTECTED_LIST = get_protected()
        PROTECTED_LIST.sort()
        PROTECTED_UPPER_DIRS = set()

        # The lengths of these protected directories for optimization
        ALL_LENGTHS = list(set(len(protected) for protected in PROTECTED_LIST))
        ALL_LENGTHS.sort()

        main()

else:

    # Some empty lists that we'll populate for tests.

    PROTECTED_LIST = []
    ALL_LENGTHS = []
