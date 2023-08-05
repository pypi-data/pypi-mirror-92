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

__all__ = ['Job']


class Job(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 delivery_info: Optional[pulumi.Input[pulumi.InputType['JobDeliveryInfoArgs']]] = None,
                 delivery_type: Optional[pulumi.Input[Union[str, 'JobDeliveryType']]] = None,
                 details: Optional[pulumi.Input[Union[pulumi.InputType['DataBoxDiskJobDetailsArgs'], pulumi.InputType['DataBoxHeavyJobDetailsArgs'], pulumi.InputType['DataBoxJobDetailsArgs']]]] = None,
                 job_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Job Resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['JobDeliveryInfoArgs']] delivery_info: Delivery Info of Job.
        :param pulumi.Input[Union[str, 'JobDeliveryType']] delivery_type: Delivery type of Job.
        :param pulumi.Input[Union[pulumi.InputType['DataBoxDiskJobDetailsArgs'], pulumi.InputType['DataBoxHeavyJobDetailsArgs'], pulumi.InputType['DataBoxJobDetailsArgs']]] details: Details of a job run. This field will only be sent for expand details filter.
        :param pulumi.Input[str] job_name: The name of the job Resource within the specified resource group. job names must be between 3 and 24 characters in length and use any alphanumeric and underscore only
        :param pulumi.Input[str] location: The location of the resource. This will be one of the supported and registered Azure Regions (e.g. West US, East US, Southeast Asia, etc.). The region of a resource cannot be changed once it is created, but if an identical region is specified on update the request will succeed.
        :param pulumi.Input[str] resource_group_name: The Resource Group Name
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The sku type.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: The list of key value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups).
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

            __props__['delivery_info'] = delivery_info
            __props__['delivery_type'] = delivery_type
            __props__['details'] = details
            if job_name is None and not opts.urn:
                raise TypeError("Missing required property 'job_name'")
            __props__['job_name'] = job_name
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if sku is None and not opts.urn:
                raise TypeError("Missing required property 'sku'")
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['cancellation_reason'] = None
            __props__['error'] = None
            __props__['is_cancellable'] = None
            __props__['is_cancellable_without_fee'] = None
            __props__['is_deletable'] = None
            __props__['is_shipping_address_editable'] = None
            __props__['name'] = None
            __props__['start_time'] = None
            __props__['status'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:databox/latest:Job"), pulumi.Alias(type_="azure-nextgen:databox/v20180101:Job"), pulumi.Alias(type_="azure-nextgen:databox/v20200401:Job"), pulumi.Alias(type_="azure-nextgen:databox/v20201101:Job")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Job, __self__).__init__(
            'azure-nextgen:databox/v20190901:Job',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Job':
        """
        Get an existing Job resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Job(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cancellationReason")
    def cancellation_reason(self) -> pulumi.Output[str]:
        """
        Reason for cancellation.
        """
        return pulumi.get(self, "cancellation_reason")

    @property
    @pulumi.getter(name="deliveryInfo")
    def delivery_info(self) -> pulumi.Output[Optional['outputs.JobDeliveryInfoResponse']]:
        """
        Delivery Info of Job.
        """
        return pulumi.get(self, "delivery_info")

    @property
    @pulumi.getter(name="deliveryType")
    def delivery_type(self) -> pulumi.Output[Optional[str]]:
        """
        Delivery type of Job.
        """
        return pulumi.get(self, "delivery_type")

    @property
    @pulumi.getter
    def details(self) -> pulumi.Output[Optional[Any]]:
        """
        Details of a job run. This field will only be sent for expand details filter.
        """
        return pulumi.get(self, "details")

    @property
    @pulumi.getter
    def error(self) -> pulumi.Output['outputs.ErrorResponse']:
        """
        Top level error for the job.
        """
        return pulumi.get(self, "error")

    @property
    @pulumi.getter(name="isCancellable")
    def is_cancellable(self) -> pulumi.Output[bool]:
        """
        Describes whether the job is cancellable or not.
        """
        return pulumi.get(self, "is_cancellable")

    @property
    @pulumi.getter(name="isCancellableWithoutFee")
    def is_cancellable_without_fee(self) -> pulumi.Output[bool]:
        """
        Flag to indicate cancellation of scheduled job.
        """
        return pulumi.get(self, "is_cancellable_without_fee")

    @property
    @pulumi.getter(name="isDeletable")
    def is_deletable(self) -> pulumi.Output[bool]:
        """
        Describes whether the job is deletable or not.
        """
        return pulumi.get(self, "is_deletable")

    @property
    @pulumi.getter(name="isShippingAddressEditable")
    def is_shipping_address_editable(self) -> pulumi.Output[bool]:
        """
        Describes whether the shipping address is editable or not.
        """
        return pulumi.get(self, "is_shipping_address_editable")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        The location of the resource. This will be one of the supported and registered Azure Regions (e.g. West US, East US, Southeast Asia, etc.). The region of a resource cannot be changed once it is created, but if an identical region is specified on update the request will succeed.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Name of the object.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output['outputs.SkuResponse']:
        """
        The sku type.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[str]:
        """
        Time at which the job was started in UTC ISO 8601 format.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Name of the stage which is in progress.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        The list of key value pairs that describe the resource. These tags can be used in viewing and grouping this resource (across resource groups).
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Type of the object.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

