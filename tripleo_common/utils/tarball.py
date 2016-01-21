import logging

from oslo_concurrency import processutils

LOG = logging.getLogger(__name__)


def create_tarball(directory, filename, options='-czf'):
    """Create a tarball of a directory."""
    LOG.debug('Creating tarball of %s at location %s' % (directory, filename))
    processutils.execute('/usr/bin/tar', '-C', directory, options, filename,
                         '--exclude', '.git', '--exclude', '.tox', '.')


def tarball_extract_to_swift_container(object_client, filename, container):
    LOG.debug('Uploading filename %s to Swift container %s' % (filename,
                                                               container))
    with open(filename, 'r') as f:
        object_client.put_object(
            container=container,
            obj='',
            contents=f,
            query_string='extract-archive=tar.gz',
            headers={'X-Detect-Content-Type': 'true'}
        )
