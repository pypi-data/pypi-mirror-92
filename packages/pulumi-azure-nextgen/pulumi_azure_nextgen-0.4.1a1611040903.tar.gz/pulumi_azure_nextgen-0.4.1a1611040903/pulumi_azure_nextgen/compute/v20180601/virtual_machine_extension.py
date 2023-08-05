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

__all__ = ['VirtualMachineExtension']


class VirtualMachineExtension(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_upgrade_minor_version: Optional[pulumi.Input[bool]] = None,
                 force_update_tag: Optional[pulumi.Input[str]] = None,
                 instance_view: Optional[pulumi.Input[pulumi.InputType['VirtualMachineExtensionInstanceViewArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 protected_settings: Optional[Any] = None,
                 publisher: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 settings: Optional[Any] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 type_handler_version: Optional[pulumi.Input[str]] = None,
                 vm_extension_name: Optional[pulumi.Input[str]] = None,
                 vm_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Describes a Virtual Machine Extension.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_upgrade_minor_version: Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true.
        :param pulumi.Input[str] force_update_tag: How the extension handler should be forced to update even if the extension configuration has not changed.
        :param pulumi.Input[pulumi.InputType['VirtualMachineExtensionInstanceViewArgs']] instance_view: The virtual machine extension instance view.
        :param pulumi.Input[str] location: Resource location
        :param Any protected_settings: The extension can contain either protectedSettings or protectedSettingsFromKeyVault or no protected settings at all.
        :param pulumi.Input[str] publisher: The name of the extension handler publisher.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param Any settings: Json formatted public settings for the extension.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] type: Specifies the type of the extension; an example is "CustomScriptExtension".
        :param pulumi.Input[str] type_handler_version: Specifies the version of the script handler.
        :param pulumi.Input[str] vm_extension_name: The name of the virtual machine extension.
        :param pulumi.Input[str] vm_name: The name of the virtual machine where the extension should be created or updated.
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

            __props__['auto_upgrade_minor_version'] = auto_upgrade_minor_version
            __props__['force_update_tag'] = force_update_tag
            __props__['instance_view'] = instance_view
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            __props__['protected_settings'] = protected_settings
            __props__['publisher'] = publisher
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['settings'] = settings
            __props__['tags'] = tags
            __props__['type'] = type
            __props__['type_handler_version'] = type_handler_version
            if vm_extension_name is None and not opts.urn:
                raise TypeError("Missing required property 'vm_extension_name'")
            __props__['vm_extension_name'] = vm_extension_name
            if vm_name is None and not opts.urn:
                raise TypeError("Missing required property 'vm_name'")
            __props__['vm_name'] = vm_name
            __props__['name'] = None
            __props__['provisioning_state'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:compute/latest:VirtualMachineExtension"), pulumi.Alias(type_="azure-nextgen:compute/v20150615:VirtualMachineExtension"), pulumi.Alias(type_="azure-nextgen:compute/v20160330:VirtualMachineExtension"), pulumi.Alias(type_="azure-nextgen:compute/v20160430preview:VirtualMachineExtension"), pulumi.Alias(type_="azure-nextgen:compute/v20170330:VirtualMachineExtension"), pulumi.Alias(type_="azure-nextgen:compute/v20171201:VirtualMachineExtension"), pulumi.Alias(type_="azure-nextgen:compute/v20180401:VirtualMachineExtension"), pulumi.Alias(type_="azure-nextgen:compute/v20181001:VirtualMachineExtension"), pulumi.Alias(type_="azure-nextgen:compute/v20190301:VirtualMachineExtension"), pulumi.Alias(type_="azure-nextgen:compute/v20190701:VirtualMachineExtension"), pulumi.Alias(type_="azure-nextgen:compute/v20191201:VirtualMachineExtension"), pulumi.Alias(type_="azure-nextgen:compute/v20200601:VirtualMachineExtension")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(VirtualMachineExtension, __self__).__init__(
            'azure-nextgen:compute/v20180601:VirtualMachineExtension',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VirtualMachineExtension':
        """
        Get an existing VirtualMachineExtension resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return VirtualMachineExtension(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="autoUpgradeMinorVersion")
    def auto_upgrade_minor_version(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether the extension should use a newer minor version if one is available at deployment time. Once deployed, however, the extension will not upgrade minor versions unless redeployed, even with this property set to true.
        """
        return pulumi.get(self, "auto_upgrade_minor_version")

    @property
    @pulumi.getter(name="forceUpdateTag")
    def force_update_tag(self) -> pulumi.Output[Optional[str]]:
        """
        How the extension handler should be forced to update even if the extension configuration has not changed.
        """
        return pulumi.get(self, "force_update_tag")

    @property
    @pulumi.getter(name="instanceView")
    def instance_view(self) -> pulumi.Output[Optional['outputs.VirtualMachineExtensionInstanceViewResponse']]:
        """
        The virtual machine extension instance view.
        """
        return pulumi.get(self, "instance_view")

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
    @pulumi.getter(name="protectedSettings")
    def protected_settings(self) -> pulumi.Output[Optional[Any]]:
        """
        The extension can contain either protectedSettings or protectedSettingsFromKeyVault or no protected settings at all.
        """
        return pulumi.get(self, "protected_settings")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state, which only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter
    def publisher(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the extension handler publisher.
        """
        return pulumi.get(self, "publisher")

    @property
    @pulumi.getter
    def settings(self) -> pulumi.Output[Optional[Any]]:
        """
        Json formatted public settings for the extension.
        """
        return pulumi.get(self, "settings")

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

    @property
    @pulumi.getter(name="typeHandlerVersion")
    def type_handler_version(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the version of the script handler.
        """
        return pulumi.get(self, "type_handler_version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

