# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = ['ManagedDatabase']


class ManagedDatabase(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 catalog_collation: Optional[pulumi.Input[Union[str, 'CatalogCollationType']]] = None,
                 collation: Optional[pulumi.Input[str]] = None,
                 create_mode: Optional[pulumi.Input[Union[str, 'ManagedDatabaseCreateMode']]] = None,
                 database_name: Optional[pulumi.Input[str]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 long_term_retention_backup_resource_id: Optional[pulumi.Input[str]] = None,
                 managed_instance_name: Optional[pulumi.Input[str]] = None,
                 recoverable_database_id: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 restorable_dropped_database_id: Optional[pulumi.Input[str]] = None,
                 restore_point_in_time: Optional[pulumi.Input[str]] = None,
                 source_database_id: Optional[pulumi.Input[str]] = None,
                 storage_container_sas_token: Optional[pulumi.Input[str]] = None,
                 storage_container_uri: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A managed database resource.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Union[str, 'CatalogCollationType']] catalog_collation: Collation of the metadata catalog.
        :param pulumi.Input[str] collation: Collation of the managed database.
        :param pulumi.Input[Union[str, 'ManagedDatabaseCreateMode']] create_mode: Managed database create mode. PointInTimeRestore: Create a database by restoring a point in time backup of an existing database. SourceDatabaseName, SourceManagedInstanceName and PointInTime must be specified. RestoreExternalBackup: Create a database by restoring from external backup files. Collation, StorageContainerUri and StorageContainerSasToken must be specified. Recovery: Creates a database by restoring a geo-replicated backup. RecoverableDatabaseId must be specified as the recoverable database resource ID to restore.
        :param pulumi.Input[str] database_name: The name of the database.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] long_term_retention_backup_resource_id: The name of the Long Term Retention backup to be used for restore of this managed database.
        :param pulumi.Input[str] managed_instance_name: The name of the managed instance.
        :param pulumi.Input[str] recoverable_database_id: The resource identifier of the recoverable database associated with create operation of this database.
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] restorable_dropped_database_id: The restorable dropped database resource id to restore when creating this database.
        :param pulumi.Input[str] restore_point_in_time: Conditional. If createMode is PointInTimeRestore, this value is required. Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database.
        :param pulumi.Input[str] source_database_id: The resource identifier of the source database associated with create operation of this database.
        :param pulumi.Input[str] storage_container_sas_token: Conditional. If createMode is RestoreExternalBackup, this value is required. Specifies the storage container sas token.
        :param pulumi.Input[str] storage_container_uri: Conditional. If createMode is RestoreExternalBackup, this value is required. Specifies the uri of the storage container where backups for this restore are stored.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
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

            __props__['catalog_collation'] = catalog_collation
            __props__['collation'] = collation
            __props__['create_mode'] = create_mode
            if database_name is None and not opts.urn:
                raise TypeError("Missing required property 'database_name'")
            __props__['database_name'] = database_name
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            __props__['long_term_retention_backup_resource_id'] = long_term_retention_backup_resource_id
            if managed_instance_name is None and not opts.urn:
                raise TypeError("Missing required property 'managed_instance_name'")
            __props__['managed_instance_name'] = managed_instance_name
            __props__['recoverable_database_id'] = recoverable_database_id
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['restorable_dropped_database_id'] = restorable_dropped_database_id
            __props__['restore_point_in_time'] = restore_point_in_time
            __props__['source_database_id'] = source_database_id
            __props__['storage_container_sas_token'] = storage_container_sas_token
            __props__['storage_container_uri'] = storage_container_uri
            __props__['tags'] = tags
            __props__['creation_date'] = None
            __props__['default_secondary_location'] = None
            __props__['earliest_restore_point'] = None
            __props__['failover_group_id'] = None
            __props__['name'] = None
            __props__['status'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sql/v20180601preview:ManagedDatabase"), pulumi.Alias(type_="azure-nextgen:sql/v20190601preview:ManagedDatabase"), pulumi.Alias(type_="azure-nextgen:sql/v20200202preview:ManagedDatabase"), pulumi.Alias(type_="azure-nextgen:sql/v20200801preview:ManagedDatabase")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ManagedDatabase, __self__).__init__(
            'azure-nextgen:sql/v20170301preview:ManagedDatabase',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ManagedDatabase':
        """
        Get an existing ManagedDatabase resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ManagedDatabase(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="catalogCollation")
    def catalog_collation(self) -> pulumi.Output[Optional[str]]:
        """
        Collation of the metadata catalog.
        """
        return pulumi.get(self, "catalog_collation")

    @property
    @pulumi.getter
    def collation(self) -> pulumi.Output[Optional[str]]:
        """
        Collation of the managed database.
        """
        return pulumi.get(self, "collation")

    @property
    @pulumi.getter(name="createMode")
    def create_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Managed database create mode. PointInTimeRestore: Create a database by restoring a point in time backup of an existing database. SourceDatabaseName, SourceManagedInstanceName and PointInTime must be specified. RestoreExternalBackup: Create a database by restoring from external backup files. Collation, StorageContainerUri and StorageContainerSasToken must be specified. Recovery: Creates a database by restoring a geo-replicated backup. RecoverableDatabaseId must be specified as the recoverable database resource ID to restore.
        """
        return pulumi.get(self, "create_mode")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> pulumi.Output[str]:
        """
        Creation date of the database.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter(name="defaultSecondaryLocation")
    def default_secondary_location(self) -> pulumi.Output[str]:
        """
        Geo paired region.
        """
        return pulumi.get(self, "default_secondary_location")

    @property
    @pulumi.getter(name="earliestRestorePoint")
    def earliest_restore_point(self) -> pulumi.Output[str]:
        """
        Earliest restore point in time for point in time restore.
        """
        return pulumi.get(self, "earliest_restore_point")

    @property
    @pulumi.getter(name="failoverGroupId")
    def failover_group_id(self) -> pulumi.Output[str]:
        """
        Instance Failover Group resource identifier that this managed database belongs to.
        """
        return pulumi.get(self, "failover_group_id")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="longTermRetentionBackupResourceId")
    def long_term_retention_backup_resource_id(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the Long Term Retention backup to be used for restore of this managed database.
        """
        return pulumi.get(self, "long_term_retention_backup_resource_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="recoverableDatabaseId")
    def recoverable_database_id(self) -> pulumi.Output[Optional[str]]:
        """
        The resource identifier of the recoverable database associated with create operation of this database.
        """
        return pulumi.get(self, "recoverable_database_id")

    @property
    @pulumi.getter(name="restorableDroppedDatabaseId")
    def restorable_dropped_database_id(self) -> pulumi.Output[Optional[str]]:
        """
        The restorable dropped database resource id to restore when creating this database.
        """
        return pulumi.get(self, "restorable_dropped_database_id")

    @property
    @pulumi.getter(name="restorePointInTime")
    def restore_point_in_time(self) -> pulumi.Output[Optional[str]]:
        """
        Conditional. If createMode is PointInTimeRestore, this value is required. Specifies the point in time (ISO8601 format) of the source database that will be restored to create the new database.
        """
        return pulumi.get(self, "restore_point_in_time")

    @property
    @pulumi.getter(name="sourceDatabaseId")
    def source_database_id(self) -> pulumi.Output[Optional[str]]:
        """
        The resource identifier of the source database associated with create operation of this database.
        """
        return pulumi.get(self, "source_database_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Status of the database.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="storageContainerSasToken")
    def storage_container_sas_token(self) -> pulumi.Output[Optional[str]]:
        """
        Conditional. If createMode is RestoreExternalBackup, this value is required. Specifies the storage container sas token.
        """
        return pulumi.get(self, "storage_container_sas_token")

    @property
    @pulumi.getter(name="storageContainerUri")
    def storage_container_uri(self) -> pulumi.Output[Optional[str]]:
        """
        Conditional. If createMode is RestoreExternalBackup, this value is required. Specifies the uri of the storage container where backups for this restore are stored.
        """
        return pulumi.get(self, "storage_container_uri")

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

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

