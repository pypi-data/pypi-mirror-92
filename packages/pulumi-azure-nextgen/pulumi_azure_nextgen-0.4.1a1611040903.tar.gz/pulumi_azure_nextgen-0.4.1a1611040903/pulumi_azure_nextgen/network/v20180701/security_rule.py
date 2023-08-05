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

__all__ = ['SecurityRule']


class SecurityRule(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access: Optional[pulumi.Input[Union[str, 'SecurityRuleAccess']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 destination_address_prefix: Optional[pulumi.Input[str]] = None,
                 destination_address_prefixes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 destination_application_security_groups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationSecurityGroupArgs']]]]] = None,
                 destination_port_range: Optional[pulumi.Input[str]] = None,
                 destination_port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 direction: Optional[pulumi.Input[Union[str, 'SecurityRuleDirection']]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 network_security_group_name: Optional[pulumi.Input[str]] = None,
                 priority: Optional[pulumi.Input[int]] = None,
                 protocol: Optional[pulumi.Input[Union[str, 'SecurityRuleProtocol']]] = None,
                 provisioning_state: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 security_rule_name: Optional[pulumi.Input[str]] = None,
                 source_address_prefix: Optional[pulumi.Input[str]] = None,
                 source_address_prefixes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 source_application_security_groups: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationSecurityGroupArgs']]]]] = None,
                 source_port_range: Optional[pulumi.Input[str]] = None,
                 source_port_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Network security rule.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'SecurityRuleAccess']] access: The network traffic is allowed or denied. Possible values are: 'Allow' and 'Deny'.
        :param pulumi.Input[str] description: A description for this rule. Restricted to 140 chars.
        :param pulumi.Input[str] destination_address_prefix: The destination address prefix. CIDR or destination IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] destination_address_prefixes: The destination address prefixes. CIDR or destination IP ranges.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationSecurityGroupArgs']]]] destination_application_security_groups: The application security group specified as destination.
        :param pulumi.Input[str] destination_port_range: The destination port or range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] destination_port_ranges: The destination port ranges.
        :param pulumi.Input[Union[str, 'SecurityRuleDirection']] direction: The direction of the rule. The direction specifies if rule will be evaluated on incoming or outgoing traffic. Possible values are: 'Inbound' and 'Outbound'.
        :param pulumi.Input[str] etag: A unique read-only string that changes whenever the resource is updated.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] name: The name of the resource that is unique within a resource group. This name can be used to access the resource.
        :param pulumi.Input[str] network_security_group_name: The name of the network security group.
        :param pulumi.Input[int] priority: The priority of the rule. The value can be between 100 and 4096. The priority number must be unique for each rule in the collection. The lower the priority number, the higher the priority of the rule.
        :param pulumi.Input[Union[str, 'SecurityRuleProtocol']] protocol: Network protocol this rule applies to. Possible values are 'Tcp', 'Udp', and '*'.
        :param pulumi.Input[str] provisioning_state: The provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[str] security_rule_name: The name of the security rule.
        :param pulumi.Input[str] source_address_prefix: The CIDR or source IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. If this is an ingress rule, specifies where network traffic originates from. 
        :param pulumi.Input[Sequence[pulumi.Input[str]]] source_address_prefixes: The CIDR or source IP ranges.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ApplicationSecurityGroupArgs']]]] source_application_security_groups: The application security group specified as source.
        :param pulumi.Input[str] source_port_range: The source port or range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] source_port_ranges: The source port ranges.
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

            if access is None and not opts.urn:
                raise TypeError("Missing required property 'access'")
            __props__['access'] = access
            __props__['description'] = description
            __props__['destination_address_prefix'] = destination_address_prefix
            __props__['destination_address_prefixes'] = destination_address_prefixes
            __props__['destination_application_security_groups'] = destination_application_security_groups
            __props__['destination_port_range'] = destination_port_range
            __props__['destination_port_ranges'] = destination_port_ranges
            if direction is None and not opts.urn:
                raise TypeError("Missing required property 'direction'")
            __props__['direction'] = direction
            __props__['etag'] = etag
            __props__['id'] = id
            __props__['name'] = name
            if network_security_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'network_security_group_name'")
            __props__['network_security_group_name'] = network_security_group_name
            __props__['priority'] = priority
            if protocol is None and not opts.urn:
                raise TypeError("Missing required property 'protocol'")
            __props__['protocol'] = protocol
            __props__['provisioning_state'] = provisioning_state
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if security_rule_name is None and not opts.urn:
                raise TypeError("Missing required property 'security_rule_name'")
            __props__['security_rule_name'] = security_rule_name
            __props__['source_address_prefix'] = source_address_prefix
            __props__['source_address_prefixes'] = source_address_prefixes
            __props__['source_application_security_groups'] = source_application_security_groups
            __props__['source_port_range'] = source_port_range
            __props__['source_port_ranges'] = source_port_ranges
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/latest:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20150501preview:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20150615:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20160330:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20160601:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20160901:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20161201:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20170301:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20170601:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20170801:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20170901:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20171001:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20171101:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20180101:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20180201:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20180401:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20180601:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20180801:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20181001:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20181101:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20181201:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20190201:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20190401:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20190601:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20190701:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20190801:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20190901:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20191101:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20191201:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20200301:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20200401:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20200501:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20200601:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20200701:SecurityRule"), pulumi.Alias(type_="azure-nextgen:network/v20200801:SecurityRule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SecurityRule, __self__).__init__(
            'azure-nextgen:network/v20180701:SecurityRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SecurityRule':
        """
        Get an existing SecurityRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return SecurityRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def access(self) -> pulumi.Output[str]:
        """
        The network traffic is allowed or denied. Possible values are: 'Allow' and 'Deny'.
        """
        return pulumi.get(self, "access")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        A description for this rule. Restricted to 140 chars.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="destinationAddressPrefix")
    def destination_address_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        The destination address prefix. CIDR or destination IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used.
        """
        return pulumi.get(self, "destination_address_prefix")

    @property
    @pulumi.getter(name="destinationAddressPrefixes")
    def destination_address_prefixes(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The destination address prefixes. CIDR or destination IP ranges.
        """
        return pulumi.get(self, "destination_address_prefixes")

    @property
    @pulumi.getter(name="destinationApplicationSecurityGroups")
    def destination_application_security_groups(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationSecurityGroupResponse']]]:
        """
        The application security group specified as destination.
        """
        return pulumi.get(self, "destination_application_security_groups")

    @property
    @pulumi.getter(name="destinationPortRange")
    def destination_port_range(self) -> pulumi.Output[Optional[str]]:
        """
        The destination port or range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        """
        return pulumi.get(self, "destination_port_range")

    @property
    @pulumi.getter(name="destinationPortRanges")
    def destination_port_ranges(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The destination port ranges.
        """
        return pulumi.get(self, "destination_port_ranges")

    @property
    @pulumi.getter
    def direction(self) -> pulumi.Output[str]:
        """
        The direction of the rule. The direction specifies if rule will be evaluated on incoming or outgoing traffic. Possible values are: 'Inbound' and 'Outbound'.
        """
        return pulumi.get(self, "direction")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the resource that is unique within a resource group. This name can be used to access the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def priority(self) -> pulumi.Output[Optional[int]]:
        """
        The priority of the rule. The value can be between 100 and 4096. The priority number must be unique for each rule in the collection. The lower the priority number, the higher the priority of the rule.
        """
        return pulumi.get(self, "priority")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[str]:
        """
        Network protocol this rule applies to. Possible values are 'Tcp', 'Udp', and '*'.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[Optional[str]]:
        """
        The provisioning state of the public IP resource. Possible values are: 'Updating', 'Deleting', and 'Failed'.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="sourceAddressPrefix")
    def source_address_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        The CIDR or source IP range. Asterisk '*' can also be used to match all source IPs. Default tags such as 'VirtualNetwork', 'AzureLoadBalancer' and 'Internet' can also be used. If this is an ingress rule, specifies where network traffic originates from. 
        """
        return pulumi.get(self, "source_address_prefix")

    @property
    @pulumi.getter(name="sourceAddressPrefixes")
    def source_address_prefixes(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The CIDR or source IP ranges.
        """
        return pulumi.get(self, "source_address_prefixes")

    @property
    @pulumi.getter(name="sourceApplicationSecurityGroups")
    def source_application_security_groups(self) -> pulumi.Output[Optional[Sequence['outputs.ApplicationSecurityGroupResponse']]]:
        """
        The application security group specified as source.
        """
        return pulumi.get(self, "source_application_security_groups")

    @property
    @pulumi.getter(name="sourcePortRange")
    def source_port_range(self) -> pulumi.Output[Optional[str]]:
        """
        The source port or range. Integer or range between 0 and 65535. Asterisk '*' can also be used to match all ports.
        """
        return pulumi.get(self, "source_port_range")

    @property
    @pulumi.getter(name="sourcePortRanges")
    def source_port_ranges(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The source port ranges.
        """
        return pulumi.get(self, "source_port_ranges")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

