# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .database_account import *
from .database_account_cassandra_keyspace import *
from .database_account_cassandra_table import *
from .database_account_gremlin_database import *
from .database_account_gremlin_graph import *
from .database_account_mongo_db_collection import *
from .database_account_mongo_db_database import *
from .database_account_sql_container import *
from .database_account_sql_database import *
from .database_account_table import *
from .get_database_account import *
from .get_database_account_cassandra_keyspace import *
from .get_database_account_cassandra_table import *
from .get_database_account_gremlin_database import *
from .get_database_account_gremlin_graph import *
from .get_database_account_mongo_db_collection import *
from .get_database_account_mongo_db_database import *
from .get_database_account_sql_container import *
from .get_database_account_sql_database import *
from .get_database_account_table import *
from .list_database_account_connection_strings import *
from .list_database_account_keys import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from ... import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-nextgen:documentdb/v20150401:DatabaseAccount":
                return DatabaseAccount(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:documentdb/v20150401:DatabaseAccountCassandraKeyspace":
                return DatabaseAccountCassandraKeyspace(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:documentdb/v20150401:DatabaseAccountCassandraTable":
                return DatabaseAccountCassandraTable(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:documentdb/v20150401:DatabaseAccountGremlinDatabase":
                return DatabaseAccountGremlinDatabase(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:documentdb/v20150401:DatabaseAccountGremlinGraph":
                return DatabaseAccountGremlinGraph(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:documentdb/v20150401:DatabaseAccountMongoDBCollection":
                return DatabaseAccountMongoDBCollection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:documentdb/v20150401:DatabaseAccountMongoDBDatabase":
                return DatabaseAccountMongoDBDatabase(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:documentdb/v20150401:DatabaseAccountSqlContainer":
                return DatabaseAccountSqlContainer(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:documentdb/v20150401:DatabaseAccountSqlDatabase":
                return DatabaseAccountSqlDatabase(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:documentdb/v20150401:DatabaseAccountTable":
                return DatabaseAccountTable(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "documentdb/v20150401", _module_instance)

_register_module()
