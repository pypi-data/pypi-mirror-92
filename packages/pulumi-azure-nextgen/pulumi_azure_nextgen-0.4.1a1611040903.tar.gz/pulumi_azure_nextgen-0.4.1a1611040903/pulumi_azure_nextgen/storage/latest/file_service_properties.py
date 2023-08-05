# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['FileServiceProperties']


class FileServiceProperties(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 cors: Optional[pulumi.Input[pulumi.InputType['CorsRulesArgs']]] = None,
                 file_services_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 share_delete_retention_policy: Optional[pulumi.Input[pulumi.InputType['DeleteRetentionPolicyArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The properties of File services in storage account.
        Latest API Version: 2019-06-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        :param pulumi.Input[pulumi.InputType['CorsRulesArgs']] cors: Specifies CORS rules for the File service. You can include up to five CorsRule elements in the request. If no CorsRule elements are included in the request body, all CORS rules will be deleted, and CORS will be disabled for the File service.
        :param pulumi.Input[str] file_services_name: The name of the file Service within the specified storage account. File Service Name must be "default"
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
        :param pulumi.Input[pulumi.InputType['DeleteRetentionPolicyArgs']] share_delete_retention_policy: The file service properties for share soft delete.
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
            __props__['cors'] = cors
            if file_services_name is None and not opts.urn:
                raise TypeError("Missing required property 'file_services_name'")
            __props__['file_services_name'] = file_services_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['share_delete_retention_policy'] = share_delete_retention_policy
            __props__['name'] = None
            __props__['sku'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storage/v20190401:FileServiceProperties"), pulumi.Alias(type_="azure-nextgen:storage/v20190601:FileServiceProperties"), pulumi.Alias(type_="azure-nextgen:storage/v20200801preview:FileServiceProperties")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(FileServiceProperties, __self__).__init__(
            'azure-nextgen:storage/latest:FileServiceProperties',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'FileServiceProperties':
        """
        Get an existing FileServiceProperties resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return FileServiceProperties(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def cors(self) -> pulumi.Output[Optional['outputs.CorsRulesResponse']]:
        """
        Specifies CORS rules for the File service. You can include up to five CorsRule elements in the request. If no CorsRule elements are included in the request body, all CORS rules will be deleted, and CORS will be disabled for the File service.
        """
        return pulumi.get(self, "cors")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="shareDeleteRetentionPolicy")
    def share_delete_retention_policy(self) -> pulumi.Output[Optional['outputs.DeleteRetentionPolicyResponse']]:
        """
        The file service properties for share soft delete.
        """
        return pulumi.get(self, "share_delete_retention_policy")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output['outputs.SkuResponse']:
        """
        Sku name and tier.
        """
        return pulumi.get(self, "sku")

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

