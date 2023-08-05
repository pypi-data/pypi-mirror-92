# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['PrivateEndpointConnection']


class PrivateEndpointConnection(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 group_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 parent_name: Optional[pulumi.Input[str]] = None,
                 parent_type: Optional[pulumi.Input[str]] = None,
                 private_endpoint: Optional[pulumi.Input[pulumi.InputType['PrivateEndpointArgs']]] = None,
                 private_endpoint_connection_name: Optional[pulumi.Input[str]] = None,
                 private_link_service_connection_state: Optional[pulumi.Input[pulumi.InputType['ConnectionStateArgs']]] = None,
                 provisioning_state: Optional[pulumi.Input[Union[str, 'ResourceProvisioningState']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Latest API Version: 2020-06-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] group_ids: GroupIds from the private link service resource.
        :param pulumi.Input[str] parent_name: The name of the parent resource (namely, either, the topic name or domain name).
        :param pulumi.Input[str] parent_type: The type of the parent resource. This can be either \'topics\' or \'domains\'.
        :param pulumi.Input[pulumi.InputType['PrivateEndpointArgs']] private_endpoint: The Private Endpoint resource for this Connection.
        :param pulumi.Input[str] private_endpoint_connection_name: The name of the private endpoint connection connection.
        :param pulumi.Input[pulumi.InputType['ConnectionStateArgs']] private_link_service_connection_state: Details about the state of the connection.
        :param pulumi.Input[Union[str, 'ResourceProvisioningState']] provisioning_state: Provisioning state of the Private Endpoint Connection.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['group_ids'] = group_ids
            if parent_name is None and not opts.urn:
                raise TypeError("Missing required property 'parent_name'")
            __props__['parent_name'] = parent_name
            if parent_type is None and not opts.urn:
                raise TypeError("Missing required property 'parent_type'")
            __props__['parent_type'] = parent_type
            __props__['private_endpoint'] = private_endpoint
            if private_endpoint_connection_name is None and not opts.urn:
                raise TypeError("Missing required property 'private_endpoint_connection_name'")
            __props__['private_endpoint_connection_name'] = private_endpoint_connection_name
            __props__['private_link_service_connection_state'] = private_link_service_connection_state
            __props__['provisioning_state'] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:eventgrid/v20200401preview:PrivateEndpointConnection"), pulumi.Alias(type_="azure-nextgen:eventgrid/v20200601:PrivateEndpointConnection")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(PrivateEndpointConnection, __self__).__init__(
            'azure-nextgen:eventgrid/latest:PrivateEndpointConnection',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'PrivateEndpointConnection':
        """
        Get an existing PrivateEndpointConnection resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return PrivateEndpointConnection(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="groupIds")
    def group_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        GroupIds from the private link service resource.
        """
        return pulumi.get(self, "group_ids")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateEndpoint")
    def private_endpoint(self) -> pulumi.Output[Optional['outputs.PrivateEndpointResponse']]:
        """
        The Private Endpoint resource for this Connection.
        """
        return pulumi.get(self, "private_endpoint")

    @property
    @pulumi.getter(name="privateLinkServiceConnectionState")
    def private_link_service_connection_state(self) -> pulumi.Output[Optional['outputs.ConnectionStateResponse']]:
        """
        Details about the state of the connection.
        """
        return pulumi.get(self, "private_link_service_connection_state")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Provisioning state of the Private Endpoint Connection.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the resource.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

