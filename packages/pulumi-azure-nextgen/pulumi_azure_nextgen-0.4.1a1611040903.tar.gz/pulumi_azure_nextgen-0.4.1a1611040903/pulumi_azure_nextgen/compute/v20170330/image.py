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

__all__ = ['Image']


class Image(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 image_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 source_virtual_machine: Optional[pulumi.Input[pulumi.InputType['SubResourceArgs']]] = None,
                 storage_profile: Optional[pulumi.Input[pulumi.InputType['ImageStorageProfileArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The source user image virtual hard disk. The virtual hard disk will be copied before being attached to the virtual machine. If SourceImage is provided, the destination virtual hard drive must not exist.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] image_name: The name of the image.
        :param pulumi.Input[str] location: Resource location
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[pulumi.InputType['SubResourceArgs']] source_virtual_machine: The source virtual machine from which Image is created.
        :param pulumi.Input[pulumi.InputType['ImageStorageProfileArgs']] storage_profile: Specifies the storage settings for the virtual machine disks.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
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

            if image_name is None and not opts.urn:
                raise TypeError("Missing required property 'image_name'")
            __props__['image_name'] = image_name
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['source_virtual_machine'] = source_virtual_machine
            __props__['storage_profile'] = storage_profile
            __props__['tags'] = tags
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:compute/latest:Image"), pulumi.Alias(type_="azure-nextgen:compute/v20160430preview:Image"), pulumi.Alias(type_="azure-nextgen:compute/v20171201:Image"), pulumi.Alias(type_="azure-nextgen:compute/v20180401:Image"), pulumi.Alias(type_="azure-nextgen:compute/v20180601:Image"), pulumi.Alias(type_="azure-nextgen:compute/v20181001:Image"), pulumi.Alias(type_="azure-nextgen:compute/v20190301:Image"), pulumi.Alias(type_="azure-nextgen:compute/v20190701:Image"), pulumi.Alias(type_="azure-nextgen:compute/v20191201:Image"), pulumi.Alias(type_="azure-nextgen:compute/v20200601:Image")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Image, __self__).__init__(
            'azure-nextgen:compute/v20170330:Image',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Image':
        """
        Get an existing Image resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Image(resource_name, opts=opts, __props__=__props__)

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
        The provisioning state.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="sourceVirtualMachine")
    def source_virtual_machine(self) -> pulumi.Output[Optional['outputs.SubResourceResponse']]:
        """
        The source virtual machine from which Image is created.
        """
        return pulumi.get(self, "source_virtual_machine")

    @property
    @pulumi.getter(name="storageProfile")
    def storage_profile(self) -> pulumi.Output[Optional['outputs.ImageStorageProfileResponse']]:
        """
        Specifies the storage settings for the virtual machine disks.
        """
        return pulumi.get(self, "storage_profile")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
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

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

