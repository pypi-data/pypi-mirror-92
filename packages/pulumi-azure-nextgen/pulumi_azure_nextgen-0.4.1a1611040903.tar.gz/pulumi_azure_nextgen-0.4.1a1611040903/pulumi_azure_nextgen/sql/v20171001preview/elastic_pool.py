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

__all__ = ['ElasticPool']


class ElasticPool(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 elastic_pool_name: Optional[pulumi.Input[str]] = None,
                 license_type: Optional[pulumi.Input[Union[str, 'ElasticPoolLicenseType']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 max_size_bytes: Optional[pulumi.Input[float]] = None,
                 per_database_settings: Optional[pulumi.Input[pulumi.InputType['ElasticPoolPerDatabaseSettingsArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 sku: Optional[pulumi.Input[pulumi.InputType['SkuArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        An elastic pool.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] elastic_pool_name: The name of the elastic pool.
        :param pulumi.Input[Union[str, 'ElasticPoolLicenseType']] license_type: The license type to apply for this elastic pool.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[float] max_size_bytes: The storage limit for the database elastic pool in bytes.
        :param pulumi.Input[pulumi.InputType['ElasticPoolPerDatabaseSettingsArgs']] per_database_settings: The per database settings for the elastic pool.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[pulumi.InputType['SkuArgs']] sku: The elastic pool SKU.
               
               The list of SKUs may vary by region and support offer. To determine the SKUs (including the SKU name, tier/edition, family, and capacity) that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API or the following command:
               
               ```azurecli
               az sql elastic-pool list-editions -l <location> -o table
               ````
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[bool] zone_redundant: Whether or not this elastic pool is zone redundant, which means the replicas of this elastic pool will be spread across multiple availability zones.
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

            if elastic_pool_name is None and not opts.urn:
                raise TypeError("Missing required property 'elastic_pool_name'")
            __props__['elastic_pool_name'] = elastic_pool_name
            __props__['license_type'] = license_type
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            __props__['max_size_bytes'] = max_size_bytes
            __props__['per_database_settings'] = per_database_settings
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__['server_name'] = server_name
            __props__['sku'] = sku
            __props__['tags'] = tags
            __props__['zone_redundant'] = zone_redundant
            __props__['creation_date'] = None
            __props__['kind'] = None
            __props__['name'] = None
            __props__['state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sql/latest:ElasticPool"), pulumi.Alias(type_="azure-nextgen:sql/v20140401:ElasticPool"), pulumi.Alias(type_="azure-nextgen:sql/v20200202preview:ElasticPool"), pulumi.Alias(type_="azure-nextgen:sql/v20200801preview:ElasticPool")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ElasticPool, __self__).__init__(
            'azure-nextgen:sql/v20171001preview:ElasticPool',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ElasticPool':
        """
        Get an existing ElasticPool resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ElasticPool(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> pulumi.Output[str]:
        """
        The creation date of the elastic pool (ISO8601 format).
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Kind of elastic pool. This is metadata used for the Azure portal experience.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter(name="licenseType")
    def license_type(self) -> pulumi.Output[Optional[str]]:
        """
        The license type to apply for this elastic pool.
        """
        return pulumi.get(self, "license_type")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maxSizeBytes")
    def max_size_bytes(self) -> pulumi.Output[Optional[float]]:
        """
        The storage limit for the database elastic pool in bytes.
        """
        return pulumi.get(self, "max_size_bytes")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="perDatabaseSettings")
    def per_database_settings(self) -> pulumi.Output[Optional['outputs.ElasticPoolPerDatabaseSettingsResponse']]:
        """
        The per database settings for the elastic pool.
        """
        return pulumi.get(self, "per_database_settings")

    @property
    @pulumi.getter
    def sku(self) -> pulumi.Output[Optional['outputs.SkuResponse']]:
        """
        The elastic pool SKU.
        
        The list of SKUs may vary by region and support offer. To determine the SKUs (including the SKU name, tier/edition, family, and capacity) that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API or the following command:
        
        ```azurecli
        az sql elastic-pool list-editions -l <location> -o table
        ````
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the elastic pool.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether or not this elastic pool is zone redundant, which means the replicas of this elastic pool will be spread across multiple availability zones.
        """
        return pulumi.get(self, "zone_redundant")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

