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

__all__ = ['StorageAccountCredential']


class StorageAccountCredential(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_key: Optional[pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']]] = None,
                 account_type: Optional[pulumi.Input[Union[str, 'AccountType']]] = None,
                 alias: Optional[pulumi.Input[str]] = None,
                 blob_domain_name: Optional[pulumi.Input[str]] = None,
                 connection_string: Optional[pulumi.Input[str]] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 ssl_status: Optional[pulumi.Input[Union[str, 'SSLStatus']]] = None,
                 storage_account_id: Optional[pulumi.Input[str]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The storage account credential.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AsymmetricEncryptedSecretArgs']] account_key: Encrypted storage key.
        :param pulumi.Input[Union[str, 'AccountType']] account_type: Type of storage accessed on the storage account.
        :param pulumi.Input[str] alias: Alias for the storage account.
        :param pulumi.Input[str] blob_domain_name: Blob end point for private clouds.
        :param pulumi.Input[str] connection_string: Connection string for the storage account. Use this string if username and account key are not specified.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[str] name: The storage account credential name.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'SSLStatus']] ssl_status: Signifies whether SSL needs to be enabled or not.
        :param pulumi.Input[str] storage_account_id: Id of the storage account.
        :param pulumi.Input[str] user_name: Username for the storage account.
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

            __props__['account_key'] = account_key
            if account_type is None and not opts.urn:
                raise TypeError("Missing required property 'account_type'")
            __props__['account_type'] = account_type
            if alias is None and not opts.urn:
                raise TypeError("Missing required property 'alias'")
            __props__['alias'] = alias
            __props__['blob_domain_name'] = blob_domain_name
            __props__['connection_string'] = connection_string
            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__['device_name'] = device_name
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if ssl_status is None and not opts.urn:
                raise TypeError("Missing required property 'ssl_status'")
            __props__['ssl_status'] = ssl_status
            __props__['storage_account_id'] = storage_account_id
            __props__['user_name'] = user_name
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:databoxedge/latest:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20190301:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20190801:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200501preview:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200901:StorageAccountCredential"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200901preview:StorageAccountCredential")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(StorageAccountCredential, __self__).__init__(
            'azure-nextgen:databoxedge/v20190701:StorageAccountCredential',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'StorageAccountCredential':
        """
        Get an existing StorageAccountCredential resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return StorageAccountCredential(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accountKey")
    def account_key(self) -> pulumi.Output[Optional['outputs.AsymmetricEncryptedSecretResponse']]:
        """
        Encrypted storage key.
        """
        return pulumi.get(self, "account_key")

    @property
    @pulumi.getter(name="accountType")
    def account_type(self) -> pulumi.Output[str]:
        """
        Type of storage accessed on the storage account.
        """
        return pulumi.get(self, "account_type")

    @property
    @pulumi.getter
    def alias(self) -> pulumi.Output[str]:
        """
        Alias for the storage account.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter(name="blobDomainName")
    def blob_domain_name(self) -> pulumi.Output[Optional[str]]:
        """
        Blob end point for private clouds.
        """
        return pulumi.get(self, "blob_domain_name")

    @property
    @pulumi.getter(name="connectionString")
    def connection_string(self) -> pulumi.Output[Optional[str]]:
        """
        Connection string for the storage account. Use this string if username and account key are not specified.
        """
        return pulumi.get(self, "connection_string")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sslStatus")
    def ssl_status(self) -> pulumi.Output[str]:
        """
        Signifies whether SSL needs to be enabled or not.
        """
        return pulumi.get(self, "ssl_status")

    @property
    @pulumi.getter(name="storageAccountId")
    def storage_account_id(self) -> pulumi.Output[Optional[str]]:
        """
        Id of the storage account.
        """
        return pulumi.get(self, "storage_account_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Output[Optional[str]]:
        """
        Username for the storage account.
        """
        return pulumi.get(self, "user_name")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

