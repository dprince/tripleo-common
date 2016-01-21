from tripleo_common.actions import base

import logging
import os
import tempfile

from oslo_concurrency import processutils
from tripleo_common.utils import tarball

LOG = logging.getLogger(__name__)


class UploadTemplates(base.TripleOAction):
    """Upload default heat templates for TripleO.

    """
    def __init__(self):
        super(UploadTemplates, self).__init__()


    def run(self):
        templates_base = '/usr/share/openstack-tripleo-heat-templates/'
        handle, temp_tarball = tempfile.mkstemp()
        os.close(handle)
        tarball.create_tarball(templates_base, temp_tarball)
        tarball.tarball_extract_to_swift_container(object_client, temp_tarball,
                                                   stack_name)

    def test(self):
        return None
