# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = ['ExpressRouteCircuitAuthorization']


class ExpressRouteCircuitAuthorization(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 authorization_key: Optional[pulumi.Input[str]] = None,
                 authorization_name: Optional[pulumi.Input[str]] = None,
                 authorization_use_status: Optional[pulumi.Input[Union[str, 'AuthorizationUseStatus']]] = None,
                 circuit_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Authorization in an ExpressRouteCircuit resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] authorization_key: The authorization key.
        :param pulumi.Input[str] authorization_name: The name of the authorization.
        :param pulumi.Input[Union[str, 'AuthorizationUseStatus']] authorization_use_status: The authorization use status.
        :param pulumi.Input[str] circuit_name: The name of the express route circuit.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] provisioning_state: Gets the provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
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

            __props__['authorization_key'] = authorization_key
            if authorization_name is None and not opts.urn:
                raise TypeError("Missing required property 'authorization_name'")
            __props__['authorization_name'] = authorization_name
            __props__['authorization_use_status'] = authorization_use_status
            if circuit_name is None and not opts.urn:
                raise TypeError("Missing required property 'circuit_name'")
            __props__['circuit_name'] = circuit_name
            __props__['id'] = id
            __props__['name'] = name
            __props__['provisioning_state'] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['etag'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/latest:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20150501preview:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20150615:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20160330:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20160601:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20160901:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20161201:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20170301:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20170601:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20170801:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20170901:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20171001:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20171101:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20180101:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20180201:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20180401:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20180601:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20180701:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20180801:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20181001:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20181101:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20181201:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20190201:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20190601:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20190701:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20190801:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20190901:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20191101:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20191201:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20200301:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20200401:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20200501:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20200601:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20200701:ExpressRouteCircuitAuthorization"), pulumi.Alias(type_="azure-nextgen:network/v20200801:ExpressRouteCircuitAuthorization")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ExpressRouteCircuitAuthorization, __self__).__init__(
            'azure-nextgen:network/v20190401:ExpressRouteCircuitAuthorization',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ExpressRouteCircuitAuthorization':
        """
        Get an existing ExpressRouteCircuitAuthorization resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ExpressRouteCircuitAuthorization(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="authorizationKey")
    def authorization_key(self) -> pulumi.Output[Optional[str]]:
        """
        The authorization key.
        """
        return pulumi.get(self, "authorization_key")

    @property
    @pulumi.getter(name="authorizationUseStatus")
    def authorization_use_status(self) -> pulumi.Output[Optional[str]]:
        """
        The authorization use status.
        """
        return pulumi.get(self, "authorization_use_status")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        Gets name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        Gets the provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
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

