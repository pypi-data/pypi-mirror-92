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

__all__ = ['Share']


class Share(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 access_protocol: Optional[pulumi.Input[Union[str, 'ShareAccessProtocol']]] = None,
                 azure_container_info: Optional[pulumi.Input[pulumi.InputType['AzureContainerInfoArgs']]] = None,
                 client_access_rights: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClientAccessRightArgs']]]]] = None,
                 data_policy: Optional[pulumi.Input[Union[str, 'DataPolicy']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 device_name: Optional[pulumi.Input[str]] = None,
                 monitoring_status: Optional[pulumi.Input[Union[str, 'MonitoringStatus']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 refresh_details: Optional[pulumi.Input[pulumi.InputType['RefreshDetailsArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 share_status: Optional[pulumi.Input[Union[str, 'ShareStatus']]] = None,
                 user_access_rights: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserAccessRightArgs']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Represents a share on the  Data Box Edge/Gateway device.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'ShareAccessProtocol']] access_protocol: Access protocol to be used by the share.
        :param pulumi.Input[pulumi.InputType['AzureContainerInfoArgs']] azure_container_info: Azure container mapping for the share.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClientAccessRightArgs']]]] client_access_rights: List of IP addresses and corresponding access rights on the share(required for NFS protocol).
        :param pulumi.Input[Union[str, 'DataPolicy']] data_policy: Data policy of the share.
        :param pulumi.Input[str] description: Description for the share.
        :param pulumi.Input[str] device_name: The device name.
        :param pulumi.Input[Union[str, 'MonitoringStatus']] monitoring_status: Current monitoring status of the share.
        :param pulumi.Input[str] name: The share name.
        :param pulumi.Input[pulumi.InputType['RefreshDetailsArgs']] refresh_details: Details of the refresh job on this share.
        :param pulumi.Input[str] resource_group_name: The resource group name.
        :param pulumi.Input[Union[str, 'ShareStatus']] share_status: Current status of the share.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserAccessRightArgs']]]] user_access_rights: Mapping of users and corresponding access rights on the share (required for SMB protocol).
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

            if access_protocol is None and not opts.urn:
                raise TypeError("Missing required property 'access_protocol'")
            __props__['access_protocol'] = access_protocol
            __props__['azure_container_info'] = azure_container_info
            __props__['client_access_rights'] = client_access_rights
            __props__['data_policy'] = data_policy
            __props__['description'] = description
            if device_name is None and not opts.urn:
                raise TypeError("Missing required property 'device_name'")
            __props__['device_name'] = device_name
            if monitoring_status is None and not opts.urn:
                raise TypeError("Missing required property 'monitoring_status'")
            __props__['monitoring_status'] = monitoring_status
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            __props__['refresh_details'] = refresh_details
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if share_status is None and not opts.urn:
                raise TypeError("Missing required property 'share_status'")
            __props__['share_status'] = share_status
            __props__['user_access_rights'] = user_access_rights
            __props__['share_mappings'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:databoxedge/latest:Share"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20190301:Share"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20190701:Share"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200501preview:Share"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200901:Share"), pulumi.Alias(type_="azure-nextgen:databoxedge/v20200901preview:Share")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Share, __self__).__init__(
            'azure-nextgen:databoxedge/v20190801:Share',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Share':
        """
        Get an existing Share resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Share(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="accessProtocol")
    def access_protocol(self) -> pulumi.Output[str]:
        """
        Access protocol to be used by the share.
        """
        return pulumi.get(self, "access_protocol")

    @property
    @pulumi.getter(name="azureContainerInfo")
    def azure_container_info(self) -> pulumi.Output[Optional['outputs.AzureContainerInfoResponse']]:
        """
        Azure container mapping for the share.
        """
        return pulumi.get(self, "azure_container_info")

    @property
    @pulumi.getter(name="clientAccessRights")
    def client_access_rights(self) -> pulumi.Output[Optional[Sequence['outputs.ClientAccessRightResponse']]]:
        """
        List of IP addresses and corresponding access rights on the share(required for NFS protocol).
        """
        return pulumi.get(self, "client_access_rights")

    @property
    @pulumi.getter(name="dataPolicy")
    def data_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Data policy of the share.
        """
        return pulumi.get(self, "data_policy")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description for the share.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="monitoringStatus")
    def monitoring_status(self) -> pulumi.Output[str]:
        """
        Current monitoring status of the share.
        """
        return pulumi.get(self, "monitoring_status")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The object name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="refreshDetails")
    def refresh_details(self) -> pulumi.Output[Optional['outputs.RefreshDetailsResponse']]:
        """
        Details of the refresh job on this share.
        """
        return pulumi.get(self, "refresh_details")

    @property
    @pulumi.getter(name="shareMappings")
    def share_mappings(self) -> pulumi.Output[Sequence['outputs.MountPointMapResponse']]:
        """
        Share mount point to the role.
        """
        return pulumi.get(self, "share_mappings")

    @property
    @pulumi.getter(name="shareStatus")
    def share_status(self) -> pulumi.Output[str]:
        """
        Current status of the share.
        """
        return pulumi.get(self, "share_status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The hierarchical type of the object.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="userAccessRights")
    def user_access_rights(self) -> pulumi.Output[Optional[Sequence['outputs.UserAccessRightResponse']]]:
        """
        Mapping of users and corresponding access rights on the share (required for SMB protocol).
        """
        return pulumi.get(self, "user_access_rights")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

