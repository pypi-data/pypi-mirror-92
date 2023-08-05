# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = ['Application']


class Application(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_group_name: Optional[pulumi.Input[str]] = None,
                 application_name: Optional[pulumi.Input[str]] = None,
                 application_type: Optional[pulumi.Input[Union[str, 'RemoteApplicationType']]] = None,
                 command_line_arguments: Optional[pulumi.Input[str]] = None,
                 command_line_setting: Optional[pulumi.Input[Union[str, 'CommandLineSetting']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 file_path: Optional[pulumi.Input[str]] = None,
                 friendly_name: Optional[pulumi.Input[str]] = None,
                 icon_index: Optional[pulumi.Input[int]] = None,
                 icon_path: Optional[pulumi.Input[str]] = None,
                 msix_package_application_id: Optional[pulumi.Input[str]] = None,
                 msix_package_family_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 show_in_portal: Optional[pulumi.Input[bool]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Schema for Application properties.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] application_group_name: The name of the application group
        :param pulumi.Input[str] application_name: The name of the application within the specified application group
        :param pulumi.Input[Union[str, 'RemoteApplicationType']] application_type: Resource Type of Application.
        :param pulumi.Input[str] command_line_arguments: Command Line Arguments for Application.
        :param pulumi.Input[Union[str, 'CommandLineSetting']] command_line_setting: Specifies whether this published application can be launched with command line arguments provided by the client, command line arguments specified at publish time, or no command line arguments at all.
        :param pulumi.Input[str] description: Description of Application.
        :param pulumi.Input[str] file_path: Specifies a path for the executable file for the application.
        :param pulumi.Input[str] friendly_name: Friendly name of Application.
        :param pulumi.Input[int] icon_index: Index of the icon.
        :param pulumi.Input[str] icon_path: Path to icon.
        :param pulumi.Input[str] msix_package_application_id: Specifies the package application Id for MSIX applications
        :param pulumi.Input[str] msix_package_family_name: Specifies the package family name for MSIX applications
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[bool] show_in_portal: Specifies whether to show the RemoteApp program in the RD Web Access server.
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

            if application_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'application_group_name'")
            __props__['application_group_name'] = application_group_name
            if application_name is None and not opts.urn:
                raise TypeError("Missing required property 'application_name'")
            __props__['application_name'] = application_name
            __props__['application_type'] = application_type
            __props__['command_line_arguments'] = command_line_arguments
            if command_line_setting is None and not opts.urn:
                raise TypeError("Missing required property 'command_line_setting'")
            __props__['command_line_setting'] = command_line_setting
            __props__['description'] = description
            __props__['file_path'] = file_path
            __props__['friendly_name'] = friendly_name
            __props__['icon_index'] = icon_index
            __props__['icon_path'] = icon_path
            __props__['msix_package_application_id'] = msix_package_application_id
            __props__['msix_package_family_name'] = msix_package_family_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['show_in_portal'] = show_in_portal
            __props__['icon_content'] = None
            __props__['icon_hash'] = None
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20190123preview:Application"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20190924preview:Application"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20191210preview:Application"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20200921preview:Application"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20201102preview:Application"), pulumi.Alias(type_="azure-nextgen:desktopvirtualization/v20201110preview:Application")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Application, __self__).__init__(
            'azure-nextgen:desktopvirtualization/v20201019preview:Application',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Application':
        """
        Get an existing Application resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Application(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationType")
    def application_type(self) -> pulumi.Output[Optional[str]]:
        """
        Resource Type of Application.
        """
        return pulumi.get(self, "application_type")

    @property
    @pulumi.getter(name="commandLineArguments")
    def command_line_arguments(self) -> pulumi.Output[Optional[str]]:
        """
        Command Line Arguments for Application.
        """
        return pulumi.get(self, "command_line_arguments")

    @property
    @pulumi.getter(name="commandLineSetting")
    def command_line_setting(self) -> pulumi.Output[str]:
        """
        Specifies whether this published application can be launched with command line arguments provided by the client, command line arguments specified at publish time, or no command line arguments at all.
        """
        return pulumi.get(self, "command_line_setting")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Description of Application.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="filePath")
    def file_path(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies a path for the executable file for the application.
        """
        return pulumi.get(self, "file_path")

    @property
    @pulumi.getter(name="friendlyName")
    def friendly_name(self) -> pulumi.Output[Optional[str]]:
        """
        Friendly name of Application.
        """
        return pulumi.get(self, "friendly_name")

    @property
    @pulumi.getter(name="iconContent")
    def icon_content(self) -> pulumi.Output[str]:
        """
        the icon a 64 bit string as a byte array.
        """
        return pulumi.get(self, "icon_content")

    @property
    @pulumi.getter(name="iconHash")
    def icon_hash(self) -> pulumi.Output[str]:
        """
        Hash of the icon.
        """
        return pulumi.get(self, "icon_hash")

    @property
    @pulumi.getter(name="iconIndex")
    def icon_index(self) -> pulumi.Output[Optional[int]]:
        """
        Index of the icon.
        """
        return pulumi.get(self, "icon_index")

    @property
    @pulumi.getter(name="iconPath")
    def icon_path(self) -> pulumi.Output[Optional[str]]:
        """
        Path to icon.
        """
        return pulumi.get(self, "icon_path")

    @property
    @pulumi.getter(name="msixPackageApplicationId")
    def msix_package_application_id(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the package application Id for MSIX applications
        """
        return pulumi.get(self, "msix_package_application_id")

    @property
    @pulumi.getter(name="msixPackageFamilyName")
    def msix_package_family_name(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the package family name for MSIX applications
        """
        return pulumi.get(self, "msix_package_family_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="showInPortal")
    def show_in_portal(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether to show the RemoteApp program in the RD Web Access server.
        """
        return pulumi.get(self, "show_in_portal")

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

