# a test script to list discovered mistral actions
from stevedore import extension
import tripleo_common

mgr = extension.ExtensionManager(
        namespace='mistral.actions',
        invoke_on_load=False
    )
for name in mgr.names():
    print name
