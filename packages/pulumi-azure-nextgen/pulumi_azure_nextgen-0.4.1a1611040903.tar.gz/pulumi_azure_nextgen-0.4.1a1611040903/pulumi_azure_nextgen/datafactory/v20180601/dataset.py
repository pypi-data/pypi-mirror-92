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

__all__ = ['Dataset']


class Dataset(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 dataset_name: Optional[pulumi.Input[str]] = None,
                 factory_name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[Union[pulumi.InputType['AmazonMWSObjectDatasetArgs'], pulumi.InputType['AmazonRedshiftTableDatasetArgs'], pulumi.InputType['AmazonS3DatasetArgs'], pulumi.InputType['AvroDatasetArgs'], pulumi.InputType['AzureBlobDatasetArgs'], pulumi.InputType['AzureBlobFSDatasetArgs'], pulumi.InputType['AzureDataExplorerTableDatasetArgs'], pulumi.InputType['AzureDataLakeStoreDatasetArgs'], pulumi.InputType['AzureDatabricksDeltaLakeDatasetArgs'], pulumi.InputType['AzureMariaDBTableDatasetArgs'], pulumi.InputType['AzureMySqlTableDatasetArgs'], pulumi.InputType['AzurePostgreSqlTableDatasetArgs'], pulumi.InputType['AzureSearchIndexDatasetArgs'], pulumi.InputType['AzureSqlDWTableDatasetArgs'], pulumi.InputType['AzureSqlMITableDatasetArgs'], pulumi.InputType['AzureSqlTableDatasetArgs'], pulumi.InputType['AzureTableDatasetArgs'], pulumi.InputType['BinaryDatasetArgs'], pulumi.InputType['CassandraTableDatasetArgs'], pulumi.InputType['CommonDataServiceForAppsEntityDatasetArgs'], pulumi.InputType['ConcurObjectDatasetArgs'], pulumi.InputType['CosmosDbMongoDbApiCollectionDatasetArgs'], pulumi.InputType['CosmosDbSqlApiCollectionDatasetArgs'], pulumi.InputType['CouchbaseTableDatasetArgs'], pulumi.InputType['CustomDatasetArgs'], pulumi.InputType['Db2TableDatasetArgs'], pulumi.InputType['DelimitedTextDatasetArgs'], pulumi.InputType['DocumentDbCollectionDatasetArgs'], pulumi.InputType['DrillTableDatasetArgs'], pulumi.InputType['DynamicsAXResourceDatasetArgs'], pulumi.InputType['DynamicsCrmEntityDatasetArgs'], pulumi.InputType['DynamicsEntityDatasetArgs'], pulumi.InputType['EloquaObjectDatasetArgs'], pulumi.InputType['ExcelDatasetArgs'], pulumi.InputType['FileShareDatasetArgs'], pulumi.InputType['GoogleAdWordsObjectDatasetArgs'], pulumi.InputType['GoogleBigQueryObjectDatasetArgs'], pulumi.InputType['GreenplumTableDatasetArgs'], pulumi.InputType['HBaseObjectDatasetArgs'], pulumi.InputType['HiveObjectDatasetArgs'], pulumi.InputType['HttpDatasetArgs'], pulumi.InputType['HubspotObjectDatasetArgs'], pulumi.InputType['ImpalaObjectDatasetArgs'], pulumi.InputType['InformixTableDatasetArgs'], pulumi.InputType['JiraObjectDatasetArgs'], pulumi.InputType['JsonDatasetArgs'], pulumi.InputType['MagentoObjectDatasetArgs'], pulumi.InputType['MariaDBTableDatasetArgs'], pulumi.InputType['MarketoObjectDatasetArgs'], pulumi.InputType['MicrosoftAccessTableDatasetArgs'], pulumi.InputType['MongoDbAtlasCollectionDatasetArgs'], pulumi.InputType['MongoDbCollectionDatasetArgs'], pulumi.InputType['MongoDbV2CollectionDatasetArgs'], pulumi.InputType['MySqlTableDatasetArgs'], pulumi.InputType['NetezzaTableDatasetArgs'], pulumi.InputType['ODataResourceDatasetArgs'], pulumi.InputType['OdbcTableDatasetArgs'], pulumi.InputType['Office365DatasetArgs'], pulumi.InputType['OracleServiceCloudObjectDatasetArgs'], pulumi.InputType['OracleTableDatasetArgs'], pulumi.InputType['OrcDatasetArgs'], pulumi.InputType['ParquetDatasetArgs'], pulumi.InputType['PaypalObjectDatasetArgs'], pulumi.InputType['PhoenixObjectDatasetArgs'], pulumi.InputType['PostgreSqlTableDatasetArgs'], pulumi.InputType['PrestoObjectDatasetArgs'], pulumi.InputType['QuickBooksObjectDatasetArgs'], pulumi.InputType['RelationalTableDatasetArgs'], pulumi.InputType['ResponsysObjectDatasetArgs'], pulumi.InputType['RestResourceDatasetArgs'], pulumi.InputType['SalesforceMarketingCloudObjectDatasetArgs'], pulumi.InputType['SalesforceObjectDatasetArgs'], pulumi.InputType['SalesforceServiceCloudObjectDatasetArgs'], pulumi.InputType['SapBwCubeDatasetArgs'], pulumi.InputType['SapCloudForCustomerResourceDatasetArgs'], pulumi.InputType['SapEccResourceDatasetArgs'], pulumi.InputType['SapHanaTableDatasetArgs'], pulumi.InputType['SapOpenHubTableDatasetArgs'], pulumi.InputType['SapTableResourceDatasetArgs'], pulumi.InputType['ServiceNowObjectDatasetArgs'], pulumi.InputType['SharePointOnlineListResourceDatasetArgs'], pulumi.InputType['ShopifyObjectDatasetArgs'], pulumi.InputType['SnowflakeDatasetArgs'], pulumi.InputType['SparkObjectDatasetArgs'], pulumi.InputType['SqlServerTableDatasetArgs'], pulumi.InputType['SquareObjectDatasetArgs'], pulumi.InputType['SybaseTableDatasetArgs'], pulumi.InputType['TeradataTableDatasetArgs'], pulumi.InputType['VerticaTableDatasetArgs'], pulumi.InputType['WebTableDatasetArgs'], pulumi.InputType['XeroObjectDatasetArgs'], pulumi.InputType['XmlDatasetArgs'], pulumi.InputType['ZohoObjectDatasetArgs']]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Dataset resource type.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] dataset_name: The dataset name.
        :param pulumi.Input[str] factory_name: The factory name.
        :param pulumi.Input[Union[pulumi.InputType['AmazonMWSObjectDatasetArgs'], pulumi.InputType['AmazonRedshiftTableDatasetArgs'], pulumi.InputType['AmazonS3DatasetArgs'], pulumi.InputType['AvroDatasetArgs'], pulumi.InputType['AzureBlobDatasetArgs'], pulumi.InputType['AzureBlobFSDatasetArgs'], pulumi.InputType['AzureDataExplorerTableDatasetArgs'], pulumi.InputType['AzureDataLakeStoreDatasetArgs'], pulumi.InputType['AzureDatabricksDeltaLakeDatasetArgs'], pulumi.InputType['AzureMariaDBTableDatasetArgs'], pulumi.InputType['AzureMySqlTableDatasetArgs'], pulumi.InputType['AzurePostgreSqlTableDatasetArgs'], pulumi.InputType['AzureSearchIndexDatasetArgs'], pulumi.InputType['AzureSqlDWTableDatasetArgs'], pulumi.InputType['AzureSqlMITableDatasetArgs'], pulumi.InputType['AzureSqlTableDatasetArgs'], pulumi.InputType['AzureTableDatasetArgs'], pulumi.InputType['BinaryDatasetArgs'], pulumi.InputType['CassandraTableDatasetArgs'], pulumi.InputType['CommonDataServiceForAppsEntityDatasetArgs'], pulumi.InputType['ConcurObjectDatasetArgs'], pulumi.InputType['CosmosDbMongoDbApiCollectionDatasetArgs'], pulumi.InputType['CosmosDbSqlApiCollectionDatasetArgs'], pulumi.InputType['CouchbaseTableDatasetArgs'], pulumi.InputType['CustomDatasetArgs'], pulumi.InputType['Db2TableDatasetArgs'], pulumi.InputType['DelimitedTextDatasetArgs'], pulumi.InputType['DocumentDbCollectionDatasetArgs'], pulumi.InputType['DrillTableDatasetArgs'], pulumi.InputType['DynamicsAXResourceDatasetArgs'], pulumi.InputType['DynamicsCrmEntityDatasetArgs'], pulumi.InputType['DynamicsEntityDatasetArgs'], pulumi.InputType['EloquaObjectDatasetArgs'], pulumi.InputType['ExcelDatasetArgs'], pulumi.InputType['FileShareDatasetArgs'], pulumi.InputType['GoogleAdWordsObjectDatasetArgs'], pulumi.InputType['GoogleBigQueryObjectDatasetArgs'], pulumi.InputType['GreenplumTableDatasetArgs'], pulumi.InputType['HBaseObjectDatasetArgs'], pulumi.InputType['HiveObjectDatasetArgs'], pulumi.InputType['HttpDatasetArgs'], pulumi.InputType['HubspotObjectDatasetArgs'], pulumi.InputType['ImpalaObjectDatasetArgs'], pulumi.InputType['InformixTableDatasetArgs'], pulumi.InputType['JiraObjectDatasetArgs'], pulumi.InputType['JsonDatasetArgs'], pulumi.InputType['MagentoObjectDatasetArgs'], pulumi.InputType['MariaDBTableDatasetArgs'], pulumi.InputType['MarketoObjectDatasetArgs'], pulumi.InputType['MicrosoftAccessTableDatasetArgs'], pulumi.InputType['MongoDbAtlasCollectionDatasetArgs'], pulumi.InputType['MongoDbCollectionDatasetArgs'], pulumi.InputType['MongoDbV2CollectionDatasetArgs'], pulumi.InputType['MySqlTableDatasetArgs'], pulumi.InputType['NetezzaTableDatasetArgs'], pulumi.InputType['ODataResourceDatasetArgs'], pulumi.InputType['OdbcTableDatasetArgs'], pulumi.InputType['Office365DatasetArgs'], pulumi.InputType['OracleServiceCloudObjectDatasetArgs'], pulumi.InputType['OracleTableDatasetArgs'], pulumi.InputType['OrcDatasetArgs'], pulumi.InputType['ParquetDatasetArgs'], pulumi.InputType['PaypalObjectDatasetArgs'], pulumi.InputType['PhoenixObjectDatasetArgs'], pulumi.InputType['PostgreSqlTableDatasetArgs'], pulumi.InputType['PrestoObjectDatasetArgs'], pulumi.InputType['QuickBooksObjectDatasetArgs'], pulumi.InputType['RelationalTableDatasetArgs'], pulumi.InputType['ResponsysObjectDatasetArgs'], pulumi.InputType['RestResourceDatasetArgs'], pulumi.InputType['SalesforceMarketingCloudObjectDatasetArgs'], pulumi.InputType['SalesforceObjectDatasetArgs'], pulumi.InputType['SalesforceServiceCloudObjectDatasetArgs'], pulumi.InputType['SapBwCubeDatasetArgs'], pulumi.InputType['SapCloudForCustomerResourceDatasetArgs'], pulumi.InputType['SapEccResourceDatasetArgs'], pulumi.InputType['SapHanaTableDatasetArgs'], pulumi.InputType['SapOpenHubTableDatasetArgs'], pulumi.InputType['SapTableResourceDatasetArgs'], pulumi.InputType['ServiceNowObjectDatasetArgs'], pulumi.InputType['SharePointOnlineListResourceDatasetArgs'], pulumi.InputType['ShopifyObjectDatasetArgs'], pulumi.InputType['SnowflakeDatasetArgs'], pulumi.InputType['SparkObjectDatasetArgs'], pulumi.InputType['SqlServerTableDatasetArgs'], pulumi.InputType['SquareObjectDatasetArgs'], pulumi.InputType['SybaseTableDatasetArgs'], pulumi.InputType['TeradataTableDatasetArgs'], pulumi.InputType['VerticaTableDatasetArgs'], pulumi.InputType['WebTableDatasetArgs'], pulumi.InputType['XeroObjectDatasetArgs'], pulumi.InputType['XmlDatasetArgs'], pulumi.InputType['ZohoObjectDatasetArgs']]] properties: Dataset properties.
        :param pulumi.Input[str] resource_group_name: The resource group name.
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

            if dataset_name is None and not opts.urn:
                raise TypeError("Missing required property 'dataset_name'")
            __props__['dataset_name'] = dataset_name
            if factory_name is None and not opts.urn:
                raise TypeError("Missing required property 'factory_name'")
            __props__['factory_name'] = factory_name
            if properties is None and not opts.urn:
                raise TypeError("Missing required property 'properties'")
            __props__['properties'] = properties
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['etag'] = None
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:datafactory/latest:Dataset"), pulumi.Alias(type_="azure-nextgen:datafactory/v20170901preview:Dataset")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Dataset, __self__).__init__(
            'azure-nextgen:datafactory/v20180601:Dataset',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Dataset':
        """
        Get an existing Dataset resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Dataset(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Etag identifies change in the resource.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Any]:
        """
        Dataset properties.
        """
        return pulumi.get(self, "properties")

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

