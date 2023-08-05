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

__all__ = ['ManagementPolicy']


class ManagementPolicy(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 management_policy_name: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[pulumi.InputType['ManagementPolicySchemaArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The Get Storage Account ManagementPolicies operation response.
        Latest API Version: 2019-06-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        :param pulumi.Input[str] management_policy_name: The name of the Storage Account Management Policy. It should always be 'default'
        :param pulumi.Input[pulumi.InputType['ManagementPolicySchemaArgs']] policy: The Storage Account ManagementPolicy, in JSON format. See more details in: https://docs.microsoft.com/en-us/azure/storage/common/storage-lifecycle-managment-concepts.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
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

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__['account_name'] = account_name
            if management_policy_name is None and not opts.urn:
                raise TypeError("Missing required property 'management_policy_name'")
            __props__['management_policy_name'] = management_policy_name
            if policy is None and not opts.urn:
                raise TypeError("Missing required property 'policy'")
            __props__['policy'] = policy
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['last_modified_time'] = None
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storage/v20180301preview:ManagementPolicy"), pulumi.Alias(type_="azure-nextgen:storage/v20181101:ManagementPolicy"), pulumi.Alias(type_="azure-nextgen:storage/v20190401:ManagementPolicy"), pulumi.Alias(type_="azure-nextgen:storage/v20190601:ManagementPolicy"), pulumi.Alias(type_="azure-nextgen:storage/v20200801preview:ManagementPolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagementPolicy, __self__).__init__(
            'azure-nextgen:storage/latest:ManagementPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ManagementPolicy':
        """
        Get an existing ManagementPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ManagementPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[str]:
        """
        Returns the date and time the ManagementPolicies was last modified.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output['outputs.ManagementPolicySchemaResponse']:
        """
        The Storage Account ManagementPolicy, in JSON format. See more details in: https://docs.microsoft.com/en-us/azure/storage/common/storage-lifecycle-managment-concepts.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

