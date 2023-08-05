# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['DisasterRecoveryConfiguration']


class DisasterRecoveryConfiguration(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 disaster_recovery_configuration_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Represents a disaster recovery configuration.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] disaster_recovery_configuration_name: The name of the disaster recovery configuration to be created/updated.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
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

            if disaster_recovery_configuration_name is None and not opts.urn:
                raise TypeError("Missing required property 'disaster_recovery_configuration_name'")
            __props__['disaster_recovery_configuration_name'] = disaster_recovery_configuration_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__['server_name'] = server_name
            __props__['auto_failover'] = None
            __props__['failover_policy'] = None
            __props__['location'] = None
            __props__['logical_server_name'] = None
            __props__['name'] = None
            __props__['partner_logical_server_name'] = None
            __props__['partner_server_id'] = None
            __props__['role'] = None
            __props__['status'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sql/latest:DisasterRecoveryConfiguration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(DisasterRecoveryConfiguration, __self__).__init__(
            'azure-nextgen:sql/v20140401:DisasterRecoveryConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'DisasterRecoveryConfiguration':
        """
        Get an existing DisasterRecoveryConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return DisasterRecoveryConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoFailover")
    def auto_failover(self) -> pulumi.Output[str]:
        """
        Whether or not failover can be done automatically.
        """
        return pulumi.get(self, "auto_failover")

    @property
    @pulumi.getter(name="failoverPolicy")
    def failover_policy(self) -> pulumi.Output[str]:
        """
        How aggressive the automatic failover should be.
        """
        return pulumi.get(self, "failover_policy")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Location of the server that contains this disaster recovery configuration.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="logicalServerName")
    def logical_server_name(self) -> pulumi.Output[str]:
        """
        Logical name of the server.
        """
        return pulumi.get(self, "logical_server_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="partnerLogicalServerName")
    def partner_logical_server_name(self) -> pulumi.Output[str]:
        """
        Logical name of the partner server.
        """
        return pulumi.get(self, "partner_logical_server_name")

    @property
    @pulumi.getter(name="partnerServerId")
    def partner_server_id(self) -> pulumi.Output[str]:
        """
        Id of the partner server.
        """
        return pulumi.get(self, "partner_server_id")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        The role of the current server in the disaster recovery configuration.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the disaster recovery configuration.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

