from tripleo_common.actions import base

import logging
import os
import tempfile
import json

from oslo_concurrency import processutils
from heatclient.common import template_utils
from mistral import context
import requests

LOG = logging.getLogger(__name__)


class ProcessTemplates(base.TripleOAction):
    """Process templates and environment files.

    :param container: Swift container where templates reside. Defaults
        to 'overcloud'.
    :param template: Relative path to the main template. Defaults to
        'overcloud.yaml'.
    :param environments: Relative path to any active environment files.
    """
    def __init__(self, container='overcloud', template='overcloud.yaml',
                 environments=[{'path':
                               'overcloud-resource-registry-puppet.yaml'}]):
        super(ProcessTemplates, self).__init__()
        self.container = container
        self.template = template
        self.environments = environments

    def run(self):

        swift_base_url = self._get_endpoint(service_name='swift',
                                            service_type='object-store')

        template_object = os.path.join(swift_base_url, self.container,
                                       self.template)

        env_paths = []
        temp_files = []
        LOG.debug('Template: %s' % self.template)
        LOG.debug('Environments: %s' % self.environments)
        for env in self.environments:
            if env.get('path'):
                env_paths.append(os.path.join(swift_base_url, self.container,
                                              env['path']))
            elif env.get('data'):
                handle, env_temp_file = tempfile.mkstemp()
                with open(env_temp_file, 'w') as temp_file:
                    temp_file.write(json.dumps(env['data']))
                    os.close(handle)
                temp_files.append(env_temp_file)
                env_paths.append(env_temp_file)

        def _env_path_is_object(env_path):
            if env_path in temp_files:
                LOG.debug('_env_path_is_object %s: False' % env_path)
                return False
            else:
                LOG.debug('_env_path_is_object %s: True' % env_path)
                return True

        token = context.ctx().auth_token

        def _object_request(method, url, token=token):
            return requests.request(method, url,
                                    headers={'X-Auth-Token': token}).content

        template_files, template = template_utils.get_template_contents(
            template_object=template_object,
            object_request=_object_request)

        env_files, env = (
            template_utils.process_multiple_environments_and_files(
                env_paths=env_paths,
                env_path_is_object=_env_path_is_object,
                object_request=_object_request))

        # cleanup any local temp files
        for f in temp_files:
            os.remove(f)

        files = dict(list(template_files.items()) + list(env_files.items()))

        return {
            'stack_name': 'overcloud',
            'template': template,
            'environment': env,
            'files': files
        }

    def test(self):
        return None
