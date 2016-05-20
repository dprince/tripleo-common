# Copyright 2016 Red Hat, Inc.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import logging

from tripleo_common.actions import base
from tripleo_common.utils import nodes

LOG = logging.getLogger(__name__)


class RegisterNodesAction(base.TripleOAction):

    def __init__(self, service_host, nodes_json, remove=False,
                 kernel_name=None, ramdisk_name=None):
        super(RegisterNodesAction, self).__init__()
        self.service_host = service_host
        self.nodes_json = nodes_json
        self.remove = remove
        self.kernel_name = kernel_name
        self.ramdisk_name = ramdisk_name

    def run(self):
        baremetal_client = self._get_baremetal_client()
        image_client = self._get_image_client()

        return nodes.register_all_nodes(
            self.service_host,
            self.nodes_json,
            client=baremetal_client,
            remove=self.remove,
            glance_client=image_client,
            kernel_name=self.kernel_name,
            ramdisk_name=self.ramdisk_name)
