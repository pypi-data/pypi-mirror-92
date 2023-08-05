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

__all__ = ['Database']


class Database(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 collation: Optional[pulumi.Input[str]] = None,
                 create_mode: Optional[pulumi.Input[Union[str, 'CreateMode']]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 edition: Optional[pulumi.Input[Union[str, 'DatabaseEdition']]] = None,
                 elastic_pool_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 max_size_bytes: Optional[pulumi.Input[str]] = None,
                 read_scale: Optional[pulumi.Input[Union[str, 'ReadScale']]] = None,
                 recovery_services_recovery_point_resource_id: Optional[pulumi.Input[str]] = None,
                 requested_service_objective_id: Optional[pulumi.Input[str]] = None,
                 requested_service_objective_name: Optional[pulumi.Input[Union[str, 'ServiceObjectiveName']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restore_point_in_time: Optional[pulumi.Input[str]] = None,
                 sample_name: Optional[pulumi.Input[Union[str, 'SampleName']]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 source_database_deletion_date: Optional[pulumi.Input[str]] = None,
                 source_database_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 zone_redundant: Optional[pulumi.Input[bool]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Represents a database.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] collation: The collation of the database. If createMode is not Default, this value is ignored.
        :param pulumi.Input[Union[str, 'CreateMode']] create_mode: Specifies the mode of database creation.
               
               Default: regular database creation.
               
               Copy: creates a database as a copy of an existing database. sourceDatabaseId must be specified as the resource ID of the source database.
               
               OnlineSecondary/NonReadableSecondary: creates a database as a (readable or nonreadable) secondary replica of an existing database. sourceDatabaseId must be specified as the resource ID of the existing primary database.
               
               PointInTimeRestore: Creates a database by restoring a point in time backup of an existing database. sourceDatabaseId must be specified as the resource ID of the existing database, and restorePointInTime must be specified.
               
               Recovery: Creates a database by restoring a geo-replicated backup. sourceDatabaseId must be specified as the recoverable database resource ID to restore.
               
               Restore: Creates a database by restoring a backup of a deleted database. sourceDatabaseId must be specified. If sourceDatabaseId is the database's original resource ID, then sourceDatabaseDeletionDate must be specified. Otherwise sourceDatabaseId must be the restorable dropped database resource ID and sourceDatabaseDeletionDate is ignored. restorePointInTime may also be specified to restore from an earlier point in time.
               
               RestoreLongTermRetentionBackup: Creates a database by restoring from a long term retention vault. recoveryServicesRecoveryPointResourceId must be specified as the recovery point resource ID.
               
               Copy, NonReadableSecondary, OnlineSecondary and RestoreLongTermRetentionBackup are not supported for DataWarehouse edition.
        :param pulumi.Input[str] database_name: The name of the database to be operated on (updated or created).
        :param pulumi.Input[Union[str, 'DatabaseEdition']] edition: The edition of the database. The DatabaseEditions enumeration contains all the valid editions. If createMode is NonReadableSecondary or OnlineSecondary, this value is ignored.
               
               The list of SKUs may vary by region and support offer. To determine the SKUs (including the SKU name, tier/edition, family, and capacity) that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API or one of the following commands:
               
               ```azurecli
               az sql db list-editions -l <location> -o table
               ````
               
               ```powershell
               Get-AzSqlServerServiceObjective -Location <location>
               ````
        :param pulumi.Input[str] elastic_pool_name: The name of the elastic pool the database is in. If elasticPoolName and requestedServiceObjectiveName are both updated, the value of requestedServiceObjectiveName is ignored. Not supported for DataWarehouse edition.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] max_size_bytes: The max size of the database expressed in bytes. If createMode is not Default, this value is ignored. To see possible values, query the capabilities API (/subscriptions/{subscriptionId}/providers/Microsoft.Sql/locations/{locationID}/capabilities) referred to by operationId: "Capabilities_ListByLocation."
        :param pulumi.Input[Union[str, 'ReadScale']] read_scale: Conditional. If the database is a geo-secondary, readScale indicates whether read-only connections are allowed to this database or not. Not supported for DataWarehouse edition.
        :param pulumi.Input[str] recovery_services_recovery_point_resource_id: Conditional. If createMode is RestoreLongTermRetentionBackup, then this value is required. Specifies the resource ID of the recovery point to restore from.
        :param pulumi.Input[str] requested_service_objective_id: The configured service level objective ID of the database. This is the service level objective that is in the process of being applied to the database. Once successfully updated, it will match the value of currentServiceObjectiveId property. If requestedServiceObjectiveId and requestedServiceObjectiveName are both updated, the value of requestedServiceObjectiveId overrides the value of requestedServiceObjectiveName.
               
               The list of SKUs may vary by region and support offer. To determine the service objective ids that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API.
        :param pulumi.Input[Union[str, 'ServiceObjectiveName']] requested_service_objective_name: The name of the configured service level objective of the database. This is the service level objective that is in the process of being applied to the database. Once successfully updated, it will match the value of serviceLevelObjective property. 
               
               The list of SKUs may vary by region and support offer. To determine the SKUs (including the SKU name, tier/edition, family, and capacity) that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API or one of the following commands:
               
               ```azurecli
               az sql db list-editions -l <location> -o table
               ````
               
               ```powershell
               Get-AzSqlServerServiceObjective -Location <location>
               ````
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] restore_point_in_time: Conditional. If createMode is PointInTimeRestore, this value is required. If createMode is Restore, this value is optional. Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database. Must be greater than or equal to the source database's earliestRestoreDate value.
        :param pulumi.Input[Union[str, 'SampleName']] sample_name: Indicates the name of the sample schema to apply when creating this database. If createMode is not Default, this value is ignored. Not supported for DataWarehouse edition.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[str] source_database_deletion_date: Conditional. If createMode is Restore and sourceDatabaseId is the deleted database's original resource id when it existed (as opposed to its current restorable dropped database id), then this value is required. Specifies the time that the database was deleted.
        :param pulumi.Input[str] source_database_id: Conditional. If createMode is Copy, NonReadableSecondary, OnlineSecondary, PointInTimeRestore, Recovery, or Restore, then this value is required. Specifies the resource ID of the source database. If createMode is NonReadableSecondary or OnlineSecondary, the name of the source database must be the same as the new database being created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[bool] zone_redundant: Whether or not this database is zone redundant, which means the replicas of this database will be spread across multiple availability zones.
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

            __props__['collation'] = collation
            __props__['create_mode'] = create_mode
            if database_name is None and not opts.urn:
                raise TypeError("Missing required property 'database_name'")
            __props__['database_name'] = database_name
            __props__['edition'] = edition
            __props__['elastic_pool_name'] = elastic_pool_name
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            __props__['max_size_bytes'] = max_size_bytes
            __props__['read_scale'] = read_scale
            __props__['recovery_services_recovery_point_resource_id'] = recovery_services_recovery_point_resource_id
            __props__['requested_service_objective_id'] = requested_service_objective_id
            __props__['requested_service_objective_name'] = requested_service_objective_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['restore_point_in_time'] = restore_point_in_time
            __props__['sample_name'] = sample_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__['server_name'] = server_name
            __props__['source_database_deletion_date'] = source_database_deletion_date
            __props__['source_database_id'] = source_database_id
            __props__['tags'] = tags
            __props__['zone_redundant'] = zone_redundant
            __props__['containment_state'] = None
            __props__['creation_date'] = None
            __props__['current_service_objective_id'] = None
            __props__['database_id'] = None
            __props__['default_secondary_location'] = None
            __props__['earliest_restore_date'] = None
            __props__['failover_group_id'] = None
            __props__['kind'] = None
            __props__['name'] = None
            __props__['recommended_index'] = None
            __props__['service_level_objective'] = None
            __props__['service_tier_advisors'] = None
            __props__['status'] = None
            __props__['transparent_data_encryption'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sql/latest:Database"), pulumi.Alias(type_="azure-nextgen:sql/v20170301preview:Database"), pulumi.Alias(type_="azure-nextgen:sql/v20171001preview:Database"), pulumi.Alias(type_="azure-nextgen:sql/v20190601preview:Database"), pulumi.Alias(type_="azure-nextgen:sql/v20200202preview:Database"), pulumi.Alias(type_="azure-nextgen:sql/v20200801preview:Database")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Database, __self__).__init__(
            'azure-nextgen:sql/v20140401:Database',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Database':
        """
        Get an existing Database resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Database(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def collation(self) -> pulumi.Output[Optional[str]]:
        """
        The collation of the database. If createMode is not Default, this value is ignored.
        """
        return pulumi.get(self, "collation")

    @property
    @pulumi.getter(name="containmentState")
    def containment_state(self) -> pulumi.Output[float]:
        """
        The containment state of the database.
        """
        return pulumi.get(self, "containment_state")

    @property
    @pulumi.getter(name="createMode")
    def create_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the mode of database creation.

        Default: regular database creation.

        Copy: creates a database as a copy of an existing database. sourceDatabaseId must be specified as the resource ID of the source database.

        OnlineSecondary/NonReadableSecondary: creates a database as a (readable or nonreadable) secondary replica of an existing database. sourceDatabaseId must be specified as the resource ID of the existing primary database.

        PointInTimeRestore: Creates a database by restoring a point in time backup of an existing database. sourceDatabaseId must be specified as the resource ID of the existing database, and restorePointInTime must be specified.

        Recovery: Creates a database by restoring a geo-replicated backup. sourceDatabaseId must be specified as the recoverable database resource ID to restore.

        Restore: Creates a database by restoring a backup of a deleted database. sourceDatabaseId must be specified. If sourceDatabaseId is the database's original resource ID, then sourceDatabaseDeletionDate must be specified. Otherwise sourceDatabaseId must be the restorable dropped database resource ID and sourceDatabaseDeletionDate is ignored. restorePointInTime may also be specified to restore from an earlier point in time.

        RestoreLongTermRetentionBackup: Creates a database by restoring from a long term retention vault. recoveryServicesRecoveryPointResourceId must be specified as the recovery point resource ID.

        Copy, NonReadableSecondary, OnlineSecondary and RestoreLongTermRetentionBackup are not supported for DataWarehouse edition.
        """
        return pulumi.get(self, "create_mode")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> pulumi.Output[str]:
        """
        The creation date of the database (ISO8601 format).
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="currentServiceObjectiveId")
    def current_service_objective_id(self) -> pulumi.Output[str]:
        """
        The current service level objective ID of the database. This is the ID of the service level objective that is currently active.
        """
        return pulumi.get(self, "current_service_objective_id")

    @property
    @pulumi.getter(name="databaseId")
    def database_id(self) -> pulumi.Output[str]:
        """
        The ID of the database.
        """
        return pulumi.get(self, "database_id")

    @property
    @pulumi.getter(name="defaultSecondaryLocation")
    def default_secondary_location(self) -> pulumi.Output[str]:
        """
        The default secondary region for this database.
        """
        return pulumi.get(self, "default_secondary_location")

    @property
    @pulumi.getter(name="earliestRestoreDate")
    def earliest_restore_date(self) -> pulumi.Output[str]:
        """
        This records the earliest start date and time that restore is available for this database (ISO8601 format).
        """
        return pulumi.get(self, "earliest_restore_date")

    @property
    @pulumi.getter
    def edition(self) -> pulumi.Output[Optional[str]]:
        """
        The edition of the database. The DatabaseEditions enumeration contains all the valid editions. If createMode is NonReadableSecondary or OnlineSecondary, this value is ignored.
        
        The list of SKUs may vary by region and support offer. To determine the SKUs (including the SKU name, tier/edition, family, and capacity) that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API or one of the following commands:
        
        ```azurecli
        az sql db list-editions -l <location> -o table
        ````
        
        ```powershell
        Get-AzSqlServerServiceObjective -Location <location>
        ````
        """
        return pulumi.get(self, "edition")

    @property
    @pulumi.getter(name="elasticPoolName")
    def elastic_pool_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the elastic pool the database is in. If elasticPoolName and requestedServiceObjectiveName are both updated, the value of requestedServiceObjectiveName is ignored. Not supported for DataWarehouse edition.
        """
        return pulumi.get(self, "elastic_pool_name")

    @property
    @pulumi.getter(name="failoverGroupId")
    def failover_group_id(self) -> pulumi.Output[str]:
        """
        The resource identifier of the failover group containing this database.
        """
        return pulumi.get(self, "failover_group_id")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Kind of database.  This is metadata used for the Azure portal experience.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maxSizeBytes")
    def max_size_bytes(self) -> pulumi.Output[Optional[str]]:
        """
        The max size of the database expressed in bytes. If createMode is not Default, this value is ignored. To see possible values, query the capabilities API (/subscriptions/{subscriptionId}/providers/Microsoft.Sql/locations/{locationID}/capabilities) referred to by operationId: "Capabilities_ListByLocation."
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
    @pulumi.getter(name="readScale")
    def read_scale(self) -> pulumi.Output[Optional[str]]:
        """
        Conditional. If the database is a geo-secondary, readScale indicates whether read-only connections are allowed to this database or not. Not supported for DataWarehouse edition.
        """
        return pulumi.get(self, "read_scale")

    @property
    @pulumi.getter(name="recommendedIndex")
    def recommended_index(self) -> pulumi.Output[Sequence['outputs.RecommendedIndexResponse']]:
        """
        The recommended indices for this database.
        """
        return pulumi.get(self, "recommended_index")

    @property
    @pulumi.getter(name="recoveryServicesRecoveryPointResourceId")
    def recovery_services_recovery_point_resource_id(self) -> pulumi.Output[Optional[str]]:
        """
        Conditional. If createMode is RestoreLongTermRetentionBackup, then this value is required. Specifies the resource ID of the recovery point to restore from.
        """
        return pulumi.get(self, "recovery_services_recovery_point_resource_id")

    @property
    @pulumi.getter(name="requestedServiceObjectiveId")
    def requested_service_objective_id(self) -> pulumi.Output[Optional[str]]:
        """
        The configured service level objective ID of the database. This is the service level objective that is in the process of being applied to the database. Once successfully updated, it will match the value of currentServiceObjectiveId property. If requestedServiceObjectiveId and requestedServiceObjectiveName are both updated, the value of requestedServiceObjectiveId overrides the value of requestedServiceObjectiveName.
        
        The list of SKUs may vary by region and support offer. To determine the service objective ids that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API.
        """
        return pulumi.get(self, "requested_service_objective_id")

    @property
    @pulumi.getter(name="requestedServiceObjectiveName")
    def requested_service_objective_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the configured service level objective of the database. This is the service level objective that is in the process of being applied to the database. Once successfully updated, it will match the value of serviceLevelObjective property. 
        
        The list of SKUs may vary by region and support offer. To determine the SKUs (including the SKU name, tier/edition, family, and capacity) that are available to your subscription in an Azure region, use the `Capabilities_ListByLocation` REST API or one of the following commands:
        
        ```azurecli
        az sql db list-editions -l <location> -o table
        ````
        
        ```powershell
        Get-AzSqlServerServiceObjective -Location <location>
        ````
        """
        return pulumi.get(self, "requested_service_objective_name")

    @property
    @pulumi.getter(name="restorePointInTime")
    def restore_point_in_time(self) -> pulumi.Output[Optional[str]]:
        """
        Conditional. If createMode is PointInTimeRestore, this value is required. If createMode is Restore, this value is optional. Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database. Must be greater than or equal to the source database's earliestRestoreDate value.
        """
        return pulumi.get(self, "restore_point_in_time")

    @property
    @pulumi.getter(name="sampleName")
    def sample_name(self) -> pulumi.Output[Optional[str]]:
        """
        Indicates the name of the sample schema to apply when creating this database. If createMode is not Default, this value is ignored. Not supported for DataWarehouse edition.
        """
        return pulumi.get(self, "sample_name")

    @property
    @pulumi.getter(name="serviceLevelObjective")
    def service_level_objective(self) -> pulumi.Output[str]:
        """
        The current service level objective of the database.
        """
        return pulumi.get(self, "service_level_objective")

    @property
    @pulumi.getter(name="serviceTierAdvisors")
    def service_tier_advisors(self) -> pulumi.Output[Sequence['outputs.ServiceTierAdvisorResponse']]:
        """
        The list of service tier advisors for this database. Expanded property
        """
        return pulumi.get(self, "service_tier_advisors")

    @property
    @pulumi.getter(name="sourceDatabaseDeletionDate")
    def source_database_deletion_date(self) -> pulumi.Output[Optional[str]]:
        """
        Conditional. If createMode is Restore and sourceDatabaseId is the deleted database's original resource id when it existed (as opposed to its current restorable dropped database id), then this value is required. Specifies the time that the database was deleted.
        """
        return pulumi.get(self, "source_database_deletion_date")

    @property
    @pulumi.getter(name="sourceDatabaseId")
    def source_database_id(self) -> pulumi.Output[Optional[str]]:
        """
        Conditional. If createMode is Copy, NonReadableSecondary, OnlineSecondary, PointInTimeRestore, Recovery, or Restore, then this value is required. Specifies the resource ID of the source database. If createMode is NonReadableSecondary or OnlineSecondary, the name of the source database must be the same as the new database being created.
        """
        return pulumi.get(self, "source_database_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The status of the database.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="transparentDataEncryption")
    def transparent_data_encryption(self) -> pulumi.Output[Sequence['outputs.TransparentDataEncryptionResponse']]:
        """
        The transparent data encryption info for this database.
        """
        return pulumi.get(self, "transparent_data_encryption")

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
        Whether or not this database is zone redundant, which means the replicas of this database will be spread across multiple availability zones.
        """
        return pulumi.get(self, "zone_redundant")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

