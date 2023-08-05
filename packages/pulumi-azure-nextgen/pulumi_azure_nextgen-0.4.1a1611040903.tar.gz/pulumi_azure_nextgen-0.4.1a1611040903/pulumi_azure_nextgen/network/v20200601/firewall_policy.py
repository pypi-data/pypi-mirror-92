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

__all__ = ['FirewallPolicy']


class FirewallPolicy(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 base_policy: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 dns_settings: Optional[pulumi.Input[pulumi.InputType['DnsSettingsArgs']]] = None,
                 firewall_policy_name: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 threat_intel_mode: Optional[pulumi.Input[Union[str, 'AzureFirewallThreatIntelMode']]] = None,
                 threat_intel_whitelist: Optional[pulumi.Input[pulumi.InputType['FirewallPolicyThreatIntelWhitelistArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        FirewallPolicy Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] base_policy: The parent firewall policy from which rules are inherited.
        :param pulumi.Input[pulumi.InputType['DnsSettingsArgs']] dns_settings: DNS Proxy Settings definition.
        :param pulumi.Input[str] firewall_policy_name: The name of the Firewall Policy.
        :param pulumi.Input[str] id: Resource ID.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[Union[str, 'AzureFirewallThreatIntelMode']] threat_intel_mode: The operation mode for Threat Intelligence.
        :param pulumi.Input[pulumi.InputType['FirewallPolicyThreatIntelWhitelistArgs']] threat_intel_whitelist: ThreatIntel Whitelist for Firewall Policy.
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

            __props__['base_policy'] = base_policy
            __props__['dns_settings'] = dns_settings
            if firewall_policy_name is None and not opts.urn:
                raise TypeError("Missing required property 'firewall_policy_name'")
            __props__['firewall_policy_name'] = firewall_policy_name
            __props__['id'] = id
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            __props__['threat_intel_mode'] = threat_intel_mode
            __props__['threat_intel_whitelist'] = threat_intel_whitelist
            __props__['child_policies'] = None
            __props__['etag'] = None
            __props__['firewalls'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['rule_collection_groups'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:network/latest:FirewallPolicy"), pulumi.Alias(type_="azure-nextgen:network/v20190601:FirewallPolicy"), pulumi.Alias(type_="azure-nextgen:network/v20190701:FirewallPolicy"), pulumi.Alias(type_="azure-nextgen:network/v20190801:FirewallPolicy"), pulumi.Alias(type_="azure-nextgen:network/v20190901:FirewallPolicy"), pulumi.Alias(type_="azure-nextgen:network/v20191101:FirewallPolicy"), pulumi.Alias(type_="azure-nextgen:network/v20191201:FirewallPolicy"), pulumi.Alias(type_="azure-nextgen:network/v20200301:FirewallPolicy"), pulumi.Alias(type_="azure-nextgen:network/v20200401:FirewallPolicy"), pulumi.Alias(type_="azure-nextgen:network/v20200501:FirewallPolicy"), pulumi.Alias(type_="azure-nextgen:network/v20200701:FirewallPolicy"), pulumi.Alias(type_="azure-nextgen:network/v20200801:FirewallPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(FirewallPolicy, __self__).__init__(
            'azure-nextgen:network/v20200601:FirewallPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'FirewallPolicy':
        """
        Get an existing FirewallPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return FirewallPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="basePolicy")
    def base_policy(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The parent firewall policy from which rules are inherited.
        """
        return pulumi.get(self, "base_policy")

    @property
    @pulumi.getter(name="childPolicies")
    def child_policies(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        List of references to Child Firewall Policies.
        """
        return pulumi.get(self, "child_policies")

    @property
    @pulumi.getter(name="dnsSettings")
    def dns_settings(self) -> pulumi.Output[Optional['outputs.DnsSettingsResponse']]:
        """
        DNS Proxy Settings definition.
        """
        return pulumi.get(self, "dns_settings")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        A unique read-only string that changes whenever the resource is updated.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def firewalls(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        List of references to Azure Firewalls that this Firewall Policy is associated with.
        """
        return pulumi.get(self, "firewalls")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the firewall policy resource.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="ruleCollectionGroups")
    def rule_collection_groups(self) -> pulumi.Output[Sequence['outputs.SubResourceResponse']]:
        """
        List of references to FirewallPolicyRuleCollectionGroups.
        """
        return pulumi.get(self, "rule_collection_groups")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="threatIntelMode")
    def threat_intel_mode(self) -> pulumi.Output[Optional[str]]:
        """
        The operation mode for Threat Intelligence.
        """
        return pulumi.get(self, "threat_intel_mode")

    @property
    @pulumi.getter(name="threatIntelWhitelist")
    def threat_intel_whitelist(self) -> pulumi.Output[Optional['outputs.FirewallPolicyThreatIntelWhitelistResponse']]:
        """
        ThreatIntel Whitelist for Firewall Policy.
        """
        return pulumi.get(self, "threat_intel_whitelist")

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

