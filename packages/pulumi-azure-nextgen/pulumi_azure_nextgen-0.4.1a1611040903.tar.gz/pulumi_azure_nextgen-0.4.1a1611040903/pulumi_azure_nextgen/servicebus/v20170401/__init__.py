# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .disaster_recovery_config import *
from .get_disaster_recovery_config import *
from .get_migration_config import *
from .get_namespace import *
from .get_namespace_authorization_rule import *
from .get_namespace_network_rule_set import *
from .get_queue import *
from .get_queue_authorization_rule import *
from .get_rule import *
from .get_subscription import *
from .get_topic import *
from .get_topic_authorization_rule import *
from .list_disaster_recovery_config_keys import *
from .list_namespace_keys import *
from .migration_config import *
from .namespace import *
from .namespace_authorization_rule import *
from .namespace_network_rule_set import *
from .queue import *
from .queue_authorization_rule import *
from .rule import *
from .subscription import *
from .topic import *
from .topic_authorization_rule import *
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
            if typ == "azure-nextgen:servicebus/v20170401:DisasterRecoveryConfig":
                return DisasterRecoveryConfig(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:servicebus/v20170401:MigrationConfig":
                return MigrationConfig(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:servicebus/v20170401:Namespace":
                return Namespace(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:servicebus/v20170401:NamespaceAuthorizationRule":
                return NamespaceAuthorizationRule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:servicebus/v20170401:NamespaceNetworkRuleSet":
                return NamespaceNetworkRuleSet(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:servicebus/v20170401:Queue":
                return Queue(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:servicebus/v20170401:QueueAuthorizationRule":
                return QueueAuthorizationRule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:servicebus/v20170401:Rule":
                return Rule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:servicebus/v20170401:Subscription":
                return Subscription(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:servicebus/v20170401:Topic":
                return Topic(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:servicebus/v20170401:TopicAuthorizationRule":
                return TopicAuthorizationRule(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "servicebus/v20170401", _module_instance)

_register_module()
