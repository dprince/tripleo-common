import abc

from heatclient.v1 import client as heatclient
from swiftclient import client as swift_client

from mistral import context
from mistral.actions import base
from mistral.utils.openstack import keystone as keystone_utils

import logging
import json

LOG = logging.getLogger(__name__)

class TripleOAction(base.Action):

    def _get_object_client(self):
        ctx = context.ctx()

        LOG.debug("Swift action security context: %s" % ctx)

        swift_endpoint = keystone_utils.get_endpoint_for_project('swift')

        kwargs = {
            'preauthurl': swift_endpoint.url % {'tenant_id': ctx.project_id},
            'preauthtoken': ctx.auth_token
        }

        return swift_client.Connection(**kwargs)

    def _get_orchestration_client(self):
        ctx = context.ctx()

        LOG.debug("Heat action security context: %s" % ctx)

        heat_endpoint = keystone_utils.get_endpoint_for_project('heat')

        endpoint_url = keystone_utils.format_url(
            heat_endpoint.url,
            {'tenant_id': ctx.project_id}
        )

        return heatclient.Client(
            endpoint_url,
            region_name=heat_endpoint.region,
            token=ctx.auth_token,
            username=ctx.user_name
        )

    def _get_endpoint(self, service_name=None, service_type=None,
                      interface='internalURL'):
        ctx = context.ctx()
        for entry in json.loads(ctx.service_catalog):
            if (entry['type'] == service_type and
                    entry['name'] == service_name):
                return entry['endpoints'][0]['internalURL']
        return None
