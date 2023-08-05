# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .account import *
from .compute_policy import *
from .firewall_rule import *
from .get_account import *
from .get_compute_policy import *
from .get_firewall_rule import *
from .list_account_sas_tokens import *
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
            if typ == "azure-nextgen:datalakeanalytics/v20151001preview:Account":
                return Account(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:datalakeanalytics/v20151001preview:ComputePolicy":
                return ComputePolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:datalakeanalytics/v20151001preview:FirewallRule":
                return FirewallRule(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "datalakeanalytics/v20151001preview", _module_instance)

_register_module()
