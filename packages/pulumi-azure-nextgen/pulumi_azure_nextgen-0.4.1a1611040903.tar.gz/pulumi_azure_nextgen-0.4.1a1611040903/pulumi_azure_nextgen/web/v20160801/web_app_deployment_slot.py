# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['WebAppDeploymentSlot']


class WebAppDeploymentSlot(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 active: Optional[pulumi.Input[bool]] = None,
                 author: Optional[pulumi.Input[str]] = None,
                 author_email: Optional[pulumi.Input[str]] = None,
                 deployer: Optional[pulumi.Input[str]] = None,
                 details: Optional[pulumi.Input[str]] = None,
                 end_time: Optional[pulumi.Input[str]] = None,
                 id: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 slot: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[int]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        User credentials used for publishing activity.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] active: True if deployment is currently active, false if completed and null if not started.
        :param pulumi.Input[str] author: Who authored the deployment.
        :param pulumi.Input[str] author_email: Author email.
        :param pulumi.Input[str] deployer: Who performed the deployment.
        :param pulumi.Input[str] details: Details on deployment.
        :param pulumi.Input[str] end_time: End time.
        :param pulumi.Input[str] id: Identifier for deployment.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] message: Details about deployment status.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
        :param pulumi.Input[str] slot: Name of the deployment slot. If a slot is not specified, the API creates a deployment for the production slot.
        :param pulumi.Input[str] start_time: Start time.
        :param pulumi.Input[int] status: Deployment status.
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

            __props__['active'] = active
            __props__['author'] = author
            __props__['author_email'] = author_email
            __props__['deployer'] = deployer
            __props__['details'] = details
            __props__['end_time'] = end_time
            if id is None and not opts.urn:
                raise TypeError("Missing required property 'id'")
            __props__['id'] = id
            __props__['kind'] = kind
            __props__['message'] = message
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if slot is None and not opts.urn:
                raise TypeError("Missing required property 'slot'")
            __props__['slot'] = slot
            __props__['start_time'] = start_time
            __props__['status'] = status
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web/latest:WebAppDeploymentSlot"), pulumi.Alias(type_="azure-nextgen:web/v20150801:WebAppDeploymentSlot"), pulumi.Alias(type_="azure-nextgen:web/v20180201:WebAppDeploymentSlot"), pulumi.Alias(type_="azure-nextgen:web/v20181101:WebAppDeploymentSlot"), pulumi.Alias(type_="azure-nextgen:web/v20190801:WebAppDeploymentSlot"), pulumi.Alias(type_="azure-nextgen:web/v20200601:WebAppDeploymentSlot"), pulumi.Alias(type_="azure-nextgen:web/v20200901:WebAppDeploymentSlot")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppDeploymentSlot, __self__).__init__(
            'azure-nextgen:web/v20160801:WebAppDeploymentSlot',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppDeploymentSlot':
        """
        Get an existing WebAppDeploymentSlot resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return WebAppDeploymentSlot(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def active(self) -> pulumi.Output[Optional[bool]]:
        """
        True if deployment is currently active, false if completed and null if not started.
        """
        return pulumi.get(self, "active")

    @property
    @pulumi.getter
    def author(self) -> pulumi.Output[Optional[str]]:
        """
        Who authored the deployment.
        """
        return pulumi.get(self, "author")

    @property
    @pulumi.getter(name="authorEmail")
    def author_email(self) -> pulumi.Output[Optional[str]]:
        """
        Author email.
        """
        return pulumi.get(self, "author_email")

    @property
    @pulumi.getter
    def deployer(self) -> pulumi.Output[Optional[str]]:
        """
        Who performed the deployment.
        """
        return pulumi.get(self, "deployer")

    @property
    @pulumi.getter
    def details(self) -> pulumi.Output[Optional[str]]:
        """
        Details on deployment.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> pulumi.Output[Optional[str]]:
        """
        End time.
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def message(self) -> pulumi.Output[Optional[str]]:
        """
        Details about deployment status.
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[Optional[str]]:
        """
        Start time.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[Optional[int]]:
        """
        Deployment status.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

