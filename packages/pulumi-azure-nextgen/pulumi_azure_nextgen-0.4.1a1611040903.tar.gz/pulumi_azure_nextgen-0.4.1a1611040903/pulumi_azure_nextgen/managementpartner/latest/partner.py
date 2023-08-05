# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['Partner']


class Partner(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 partner_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        this is the management partner operations response
        Latest API Version: 2018-02-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] partner_id: Id of the Partner
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

            if partner_id is None and not opts.urn:
                raise TypeError("Missing required property 'partner_id'")
            __props__['partner_id'] = partner_id
            __props__['created_time'] = None
            __props__['etag'] = None
            __props__['name'] = None
            __props__['object_id'] = None
            __props__['partner_name'] = None
            __props__['tenant_id'] = None
            __props__['type'] = None
            __props__['updated_time'] = None
            __props__['version'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:managementpartner/v20180201:Partner")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Partner, __self__).__init__(
            'azure-nextgen:managementpartner/latest:Partner',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Partner':
        """
        Get an existing Partner resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Partner(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="createdTime")
    def created_time(self) -> pulumi.Output[Optional[str]]:
        """
        This is the DateTime when the partner was created.
        """
        return pulumi.get(self, "created_time")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[int]]:
        """
        Type of the partner
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the partner
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> pulumi.Output[Optional[str]]:
        """
        This is the object id.
        """
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter(name="partnerId")
    def partner_id(self) -> pulumi.Output[Optional[str]]:
        """
        This is the partner id
        """
        return pulumi.get(self, "partner_id")

    @property
    @pulumi.getter(name="partnerName")
    def partner_name(self) -> pulumi.Output[Optional[str]]:
        """
        This is the partner name
        """
        return pulumi.get(self, "partner_name")

    @property
    @pulumi.getter(name="tenantId")
    def tenant_id(self) -> pulumi.Output[Optional[str]]:
        """
        This is the tenant id.
        """
        return pulumi.get(self, "tenant_id")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of resource. "Microsoft.ManagementPartner/partners"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="updatedTime")
    def updated_time(self) -> pulumi.Output[Optional[str]]:
        """
        This is the DateTime when the partner was updated.
        """
        return pulumi.get(self, "updated_time")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[Optional[int]]:
        """
        This is the version.
        """
        return pulumi.get(self, "version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

