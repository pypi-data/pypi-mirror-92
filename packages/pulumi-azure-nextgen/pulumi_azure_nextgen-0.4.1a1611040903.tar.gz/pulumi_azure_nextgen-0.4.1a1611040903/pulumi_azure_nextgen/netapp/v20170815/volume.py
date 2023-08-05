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

__all__ = ['Volume']


class Volume(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 creation_token: Optional[pulumi.Input[str]] = None,
                 export_policy: Optional[pulumi.Input[pulumi.InputType['VolumePropertiesExportPolicyArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 pool_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 service_level: Optional[pulumi.Input[Union[str, 'ServiceLevel']]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[Any] = None,
                 usage_threshold: Optional[pulumi.Input[float]] = None,
                 volume_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Volume resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the NetApp account
        :param pulumi.Input[str] creation_token: A unique file path for the volume. Used when creating mount targets
        :param pulumi.Input[pulumi.InputType['VolumePropertiesExportPolicyArgs']] export_policy: Export policy rule
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] pool_name: The name of the capacity pool
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Union[str, 'ServiceLevel']] service_level: The service level of the file system
        :param pulumi.Input[str] subnet_id: The Azure Resource URI for a delegated subnet. Must have the delegation Microsoft.NetApp/volumes
        :param Any tags: Resource tags
        :param pulumi.Input[float] usage_threshold: Maximum storage quota allowed for a file system in bytes. This is a soft quota used for alerting only. Minimum size is 100 GiB. Upper limit is 100TiB.
        :param pulumi.Input[str] volume_name: The name of the volume
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
            if creation_token is None and not opts.urn:
                raise TypeError("Missing required property 'creation_token'")
            __props__['creation_token'] = creation_token
            __props__['export_policy'] = export_policy
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            if pool_name is None and not opts.urn:
                raise TypeError("Missing required property 'pool_name'")
            __props__['pool_name'] = pool_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if service_level is None:
                service_level = 'Premium'
            if service_level is None and not opts.urn:
                raise TypeError("Missing required property 'service_level'")
            __props__['service_level'] = service_level
            __props__['subnet_id'] = subnet_id
            __props__['tags'] = tags
            if usage_threshold is None:
                usage_threshold = 107374182400
            __props__['usage_threshold'] = usage_threshold
            if volume_name is None and not opts.urn:
                raise TypeError("Missing required property 'volume_name'")
            __props__['volume_name'] = volume_name
            __props__['file_system_id'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:netapp/latest:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20190501:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20190601:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20190701:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20190801:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20191001:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20191101:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20200201:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20200301:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20200501:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20200601:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20200701:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20200801:Volume"), pulumi.Alias(type_="azure-nextgen:netapp/v20200901:Volume")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Volume, __self__).__init__(
            'azure-nextgen:netapp/v20170815:Volume',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Volume':
        """
        Get an existing Volume resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Volume(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationToken")
    def creation_token(self) -> pulumi.Output[str]:
        """
        A unique file path for the volume. Used when creating mount targets
        """
        return pulumi.get(self, "creation_token")

    @property
    @pulumi.getter(name="exportPolicy")
    def export_policy(self) -> pulumi.Output[Optional['outputs.VolumePropertiesResponseExportPolicy']]:
        """
        Export policy rule
        """
        return pulumi.get(self, "export_policy")

    @property
    @pulumi.getter(name="fileSystemId")
    def file_system_id(self) -> pulumi.Output[str]:
        """
        Unique FileSystem Identifier.
        """
        return pulumi.get(self, "file_system_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        Azure lifecycle management
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="serviceLevel")
    def service_level(self) -> pulumi.Output[str]:
        """
        The service level of the file system
        """
        return pulumi.get(self, "service_level")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> pulumi.Output[Optional[str]]:
        """
        The Azure Resource URI for a delegated subnet. Must have the delegation Microsoft.NetApp/volumes
        """
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Any]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="usageThreshold")
    def usage_threshold(self) -> pulumi.Output[Optional[float]]:
        """
        Maximum storage quota allowed for a file system in bytes. This is a soft quota used for alerting only. Minimum size is 100 GiB. Upper limit is 100TiB.
        """
        return pulumi.get(self, "usage_threshold")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

