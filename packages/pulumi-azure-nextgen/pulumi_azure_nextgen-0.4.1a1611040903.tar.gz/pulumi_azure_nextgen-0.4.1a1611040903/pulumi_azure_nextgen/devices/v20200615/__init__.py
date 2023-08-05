# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .certificate import *
from .get_certificate import *
from .get_iot_hub_resource import *
from .get_iot_hub_resource_event_hub_consumer_group import *
from .get_private_endpoint_connection import *
from .iot_hub_resource import *
from .iot_hub_resource_event_hub_consumer_group import *
from .list_iot_hub_resource_keys import *
from .list_iot_hub_resource_keys_for_key_name import *
from .private_endpoint_connection import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from ... import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-nextgen:devices/v20200615:Certificate":
                return Certificate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:devices/v20200615:IotHubResource":
                return IotHubResource(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:devices/v20200615:IotHubResourceEventHubConsumerGroup":
                return IotHubResourceEventHubConsumerGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:devices/v20200615:PrivateEndpointConnection":
                return PrivateEndpointConnection(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "devices/v20200615", _module_instance)

_register_module()
