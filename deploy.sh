rm -Rf /usr/lib/python2.7/site-packages/tripleo_common*
python setup.py install
systemctl restart openstack-mistral-executor
systemctl restart openstack-mistral-engine
systemctl restart openstack-mistral-api
# this loads the actions via entrypoints (puppet already runs this)
mistral-db-manage populate
# make sure the new actions got loaded
mistral action-list | grep tripleo
