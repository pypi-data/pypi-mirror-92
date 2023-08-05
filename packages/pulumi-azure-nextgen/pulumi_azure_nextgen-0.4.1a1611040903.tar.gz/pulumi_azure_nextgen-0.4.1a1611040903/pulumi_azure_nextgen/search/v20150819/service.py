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

__all__ = ['Service']


class Service(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hosting_mode: Optional[pulumi.Input['HostingMode']] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['IdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 partition_count: Optional[pulumi.Input[int]] = None,
                 replica_count: Optional[pulumi.Input[int]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 search_service_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Describes an Azure Cognitive Search service and its current state.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input['HostingMode'] hosting_mode: Applicable only for the standard3 SKU. You can set this property to enable up to 3 high density partitions that allow up to 1000 indexes, which is much higher than the maximum indexes allowed for any other SKU. For the standard3 SKU, the value is either 'default' or 'highDensity'. For all other SKUs, this value must be 'default'.
        :param pulumi.Input[pulumi.InputType['IdentityArgs']] identity: The identity of the resource.
        :param pulumi.Input[str] location: The geographic location of the resource. This must be one of the supported and registered Azure Geo Regions (for example, West US, East US, Southeast Asia, and so forth). This property is required when creating a new resource.
        :param pulumi.Input[int] partition_count: The number of partitions in the Search service; if specified, it can be 1, 2, 3, 4, 6, or 12. Values greater than 1 are only valid for standard SKUs. For 'standard3' services with hostingMode set to 'highDensity', the allowed values are between 1 and 3.
        :param pulumi.Input[int] replica_count: The number of replicas in the Search service. If specified, it must be a value between 1 and 12 inclusive for standard SKUs or between 1 and 3 inclusive for basic SKU.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the current subscription. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] search_service_name: The name of the Azure Cognitive Search service to create or update. Search service names must only contain lowercase letters, digits or dashes, cannot use dash as the first two or last one characters, cannot contain consecutive dashes, and must be between 2 and 60 characters in length. Search service names must be globally unique since they are part of the service URI (https://<name>.search.windows.net). You cannot change the service name after the service is created.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The SKU of the Search Service, which determines price tier and capacity limits. This property is required when creating a new Search Service.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Tags to help categorize the resource in the Azure portal.
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

            if hosting_mode is None:
                hosting_mode = 'default'
            __props__['hosting_mode'] = hosting_mode
            __props__['identity'] = identity
            __props__['location'] = location
            if partition_count is None:
                partition_count = 1
            __props__['partition_count'] = partition_count
            if replica_count is None:
                replica_count = 1
            __props__['replica_count'] = replica_count
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if search_service_name is None and not opts.urn:
                raise TypeError("Missing required property 'search_service_name'")
            __props__['search_service_name'] = search_service_name
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['status'] = None
            __props__['status_details'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:search/latest:Service"), pulumi.Alias(type_="azure-nextgen:search/v20191001preview:Service"), pulumi.Alias(type_="azure-nextgen:search/v20200313:Service"), pulumi.Alias(type_="azure-nextgen:search/v20200801:Service"), pulumi.Alias(type_="azure-nextgen:search/v20200801preview:Service")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Service, __self__).__init__(
            'azure-nextgen:search/v20150819:Service',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Service':
        """
        Get an existing Service resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Service(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="hostingMode")
    def hosting_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Applicable only for the standard3 SKU. You can set this property to enable up to 3 high density partitions that allow up to 1000 indexes, which is much higher than the maximum indexes allowed for any other SKU. For the standard3 SKU, the value is either 'default' or 'highDensity'. For all other SKUs, this value must be 'default'.
        """
        return pulumi.get(self, "hosting_mode")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.IdentityResponse']]:
        """
        The identity of the resource.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[Optional[str]]:
        """
        The geographic location of the resource. This must be one of the supported and registered Azure Geo Regions (for example, West US, East US, Southeast Asia, and so forth). This property is required when creating a new resource.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="partitionCount")
    def partition_count(self) -> pulumi.Output[Optional[int]]:
        """
        The number of partitions in the Search service; if specified, it can be 1, 2, 3, 4, 6, or 12. Values greater than 1 are only valid for standard SKUs. For 'standard3' services with hostingMode set to 'highDensity', the allowed values are between 1 and 3.
        """
        return pulumi.get(self, "partition_count")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The state of the last provisioning operation performed on the Search service. Provisioning is an intermediate state that occurs while service capacity is being established. After capacity is set up, provisioningState changes to either 'succeeded' or 'failed'. Client applications can poll provisioning status (the recommended polling interval is from 30 seconds to one minute) by using the Get Search Service operation to see when an operation is completed. If you are using the free service, this value tends to come back as 'succeeded' directly in the call to Create Search service. This is because the free service uses capacity that is already set up.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="replicaCount")
    def replica_count(self) -> pulumi.Output[Optional[int]]:
        """
        The number of replicas in the Search service. If specified, it must be a value between 1 and 12 inclusive for standard SKUs or between 1 and 3 inclusive for basic SKU.
        """
        return pulumi.get(self, "replica_count")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The SKU of the Search Service, which determines price tier and capacity limits. This property is required when creating a new Search Service.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the Search service. Possible values include: 'running': The Search service is running and no provisioning operations are underway. 'provisioning': The Search service is being provisioned or scaled up or down. 'deleting': The Search service is being deleted. 'degraded': The Search service is degraded. This can occur when the underlying search units are not healthy. The Search service is most likely operational, but performance might be slow and some requests might be dropped. 'disabled': The Search service is disabled. In this state, the service will reject all API requests. 'error': The Search service is in an error state. If your service is in the degraded, disabled, or error states, it means the Azure Cognitive Search team is actively investigating the underlying issue. Dedicated services in these states are still chargeable based on the number of search units provisioned.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="statusDetails")
    def status_details(self) -> pulumi.Output[str]:
        """
        The details of the Search service status.
        """
        return pulumi.get(self, "status_details")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Tags to help categorize the resource in the Azure portal.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

