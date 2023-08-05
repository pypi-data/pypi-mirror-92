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

__all__ = ['Assignment']


class Assignment(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 assignment_name: Optional[pulumi.Input[str]] = None,
                 blueprint_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 locks: Optional[pulumi.Input[pulumi.InputType['AssignmentLockSettingsArgs']]] = None,
                 parameters: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ParameterValueBaseArgs']]]]] = None,
                 resource_groups: Optional[pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ResourceGroupValueArgs']]]]] = None,
                 subscription_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Represents a Blueprint assignment.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] assignment_name: name of the assignment.
        :param pulumi.Input[str] blueprint_id: ID of the Blueprint definition resource.
        :param pulumi.Input[str] description: Multi-line explain this resource.
        :param pulumi.Input[str] display_name: One-liner string explain this resource.
        :param pulumi.Input[pulumi.InputType['ManagedServiceIdentityArgs']] identity: Managed Service Identity for this Blueprint assignment
        :param pulumi.Input[str] location: The location of this Blueprint assignment.
        :param pulumi.Input[pulumi.InputType['AssignmentLockSettingsArgs']] locks: Defines how Blueprint-managed resources will be locked.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ParameterValueBaseArgs']]]] parameters: Blueprint parameter values.
        :param pulumi.Input[Mapping[str, pulumi.Input[pulumi.InputType['ResourceGroupValueArgs']]]] resource_groups: Names and locations of resource group placeholders.
        :param pulumi.Input[str] subscription_id: azure subscriptionId, which we assign the blueprint to.
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

            if assignment_name is None and not opts.urn:
                raise TypeError("Missing required property 'assignment_name'")
            __props__['assignment_name'] = assignment_name
            __props__['blueprint_id'] = blueprint_id
            __props__['description'] = description
            __props__['display_name'] = display_name
            if identity is None and not opts.urn:
                raise TypeError("Missing required property 'identity'")
            __props__['identity'] = identity
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            __props__['locks'] = locks
            if parameters is None and not opts.urn:
                raise TypeError("Missing required property 'parameters'")
            __props__['parameters'] = parameters
            if resource_groups is None and not opts.urn:
                raise TypeError("Missing required property 'resource_groups'")
            __props__['resource_groups'] = resource_groups
            __props__['subscription_id'] = subscription_id
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['status'] = None
            __props__['type'] = None
        super(Assignment, __self__).__init__(
            'azure-nextgen:blueprint/v20171111preview:Assignment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Assignment':
        """
        Get an existing Assignment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Assignment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="blueprintId")
    def blueprint_id(self) -> pulumi.Output[Optional[str]]:
        """
        ID of the Blueprint definition resource.
        """
        return pulumi.get(self, "blueprint_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Multi-line explain this resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[Optional[str]]:
        """
        One-liner string explain this resource.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output['outputs.ManagedServiceIdentityResponse']:
        """
        Managed Service Identity for this Blueprint assignment
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of this Blueprint assignment.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def locks(self) -> pulumi.Output[Optional['outputs.AssignmentLockSettingsResponse']]:
        """
        Defines how Blueprint-managed resources will be locked.
        """
        return pulumi.get(self, "locks")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of this resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[Mapping[str, 'outputs.ParameterValueBaseResponse']]:
        """
        Blueprint parameter values.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        State of the assignment.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceGroups")
    def resource_groups(self) -> pulumi.Output[Mapping[str, 'outputs.ResourceGroupValueResponse']]:
        """
        Names and locations of resource group placeholders.
        """
        return pulumi.get(self, "resource_groups")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output['outputs.AssignmentStatusResponse']:
        """
        Status of Blueprint assignment. This field is readonly.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of this resource.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

