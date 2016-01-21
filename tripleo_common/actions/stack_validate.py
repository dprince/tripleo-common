from tripleo_common.actions import templates

import logging

LOG = logging.getLogger(__name__)


class StackValidate(templates.ProcessTemplates):
    """Create a heat stack using the given parameters.

    :param container: Swift container where templates reside. Defaults
        to 'overcloud'.
    :param template: Relative path to the main template. Defaults to
        'overcloud.yaml'.
    :param environments: Relative path to any active environment files.
    """
    def __init__(self, container='overcloud', template='overcloud.yaml',
                 environments=[{'path':
                               'overcloud-resource-registry-puppet.yaml'}]):
        super(StackValidate, self).__init__(container, template, environments)

    def run(self):

        data = super(StackValidate, self).run()
        data['show_nested'] = True
        orchestration_client = self._get_orchestration_client()
        return orchestration_client.stacks.validate(**data)
