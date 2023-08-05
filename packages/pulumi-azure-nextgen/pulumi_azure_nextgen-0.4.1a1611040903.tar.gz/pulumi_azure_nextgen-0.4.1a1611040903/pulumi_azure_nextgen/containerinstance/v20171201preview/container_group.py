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

__all__ = ['ContainerGroup']


class ContainerGroup(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 container_group_name: Optional[pulumi.Input[str]] = None,
                 containers: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerArgs']]]]] = None,
                 image_registry_credentials: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRegistryCredentialArgs']]]]] = None,
                 ip_address: Optional[pulumi.Input[pulumi.InputType['IpAddressArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 os_type: Optional[pulumi.Input[Union[str, 'OperatingSystemTypes']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restart_policy: Optional[pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 volumes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VolumeArgs']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A container group.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] container_group_name: The name of the container group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ContainerArgs']]]] containers: The containers within the container group.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ImageRegistryCredentialArgs']]]] image_registry_credentials: The image registry credentials by which the container group is created from.
        :param pulumi.Input[pulumi.InputType['IpAddressArgs']] ip_address: The IP address type of the container group.
        :param pulumi.Input[str] location: The resource location.
        :param pulumi.Input[Union[str, 'OperatingSystemTypes']] os_type: The operating system type required by the containers in the container group.
        :param pulumi.Input[str] resource_group_name: The name of the resource group.
        :param pulumi.Input[Union[str, 'ContainerGroupRestartPolicy']] restart_policy: Restart policy for all containers within the container group. 
               - `Always` Always restart
               - `OnFailure` Restart on failure
               - `Never` Never restart
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The resource tags.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['VolumeArgs']]]] volumes: The list of volumes that can be mounted by containers in this container group.
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

            if container_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'container_group_name'")
            __props__['container_group_name'] = container_group_name
            if containers is None and not opts.urn:
                raise TypeError("Missing required property 'containers'")
            __props__['containers'] = containers
            __props__['image_registry_credentials'] = image_registry_credentials
            __props__['ip_address'] = ip_address
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            if os_type is None and not opts.urn:
                raise TypeError("Missing required property 'os_type'")
            __props__['os_type'] = os_type
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['restart_policy'] = restart_policy
            __props__['tags'] = tags
            __props__['volumes'] = volumes
            __props__['instance_view'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:containerinstance/latest:ContainerGroup"), pulumi.Alias(type_="azure-nextgen:containerinstance/v20170801preview:ContainerGroup"), pulumi.Alias(type_="azure-nextgen:containerinstance/v20171001preview:ContainerGroup"), pulumi.Alias(type_="azure-nextgen:containerinstance/v20180201preview:ContainerGroup"), pulumi.Alias(type_="azure-nextgen:containerinstance/v20180401:ContainerGroup"), pulumi.Alias(type_="azure-nextgen:containerinstance/v20180601:ContainerGroup"), pulumi.Alias(type_="azure-nextgen:containerinstance/v20180901:ContainerGroup"), pulumi.Alias(type_="azure-nextgen:containerinstance/v20181001:ContainerGroup"), pulumi.Alias(type_="azure-nextgen:containerinstance/v20191201:ContainerGroup"), pulumi.Alias(type_="azure-nextgen:containerinstance/v20201101:ContainerGroup")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ContainerGroup, __self__).__init__(
            'azure-nextgen:containerinstance/v20171201preview:ContainerGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ContainerGroup':
        """
        Get an existing ContainerGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ContainerGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def containers(self) -> pulumi.Output[Sequence['outputs.ContainerResponse']]:
        """
        The containers within the container group.
        """
        return pulumi.get(self, "containers")

    @property
    @pulumi.getter(name="imageRegistryCredentials")
    def image_registry_credentials(self) -> pulumi.Output[Optional[Sequence['outputs.ImageRegistryCredentialResponse']]]:
        """
        The image registry credentials by which the container group is created from.
        """
        return pulumi.get(self, "image_registry_credentials")

    @property
    @pulumi.getter(name="instanceView")
    def instance_view(self) -> pulumi.Output['outputs.ContainerGroupResponseInstanceView']:
        """
        The instance view of the container group. Only valid in response.
        """
        return pulumi.get(self, "instance_view")

    @property
    @pulumi.getter(name="ipAddress")
    def ip_address(self) -> pulumi.Output[Optional['outputs.IpAddressResponse']]:
        """
        The IP address type of the container group.
        """
        return pulumi.get(self, "ip_address")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="osType")
    def os_type(self) -> pulumi.Output[str]:
        """
        The operating system type required by the containers in the container group.
        """
        return pulumi.get(self, "os_type")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the container group. This only appears in the response.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="restartPolicy")
    def restart_policy(self) -> pulumi.Output[Optional[str]]:
        """
        Restart policy for all containers within the container group. 
        - `Always` Always restart
        - `OnFailure` Restart on failure
        - `Never` Never restart
        """
        return pulumi.get(self, "restart_policy")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def volumes(self) -> pulumi.Output[Optional[Sequence['outputs.VolumeResponse']]]:
        """
        The list of volumes that can be mounted by containers in this container group.
        """
        return pulumi.get(self, "volumes")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

