# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .assessment import *
from .get_assessment import *
from .get_group import *
from .get_hyper_v_collector import *
from .get_project import *
from .get_v_mware_collector import *
from .group import *
from .hyper_v_collector import *
from .project import *
from .v_mware_collector import *
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
            if typ == "azure-nextgen:migrate/latest:Assessment":
                return Assessment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:migrate/latest:Group":
                return Group(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:migrate/latest:HyperVCollector":
                return HyperVCollector(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:migrate/latest:Project":
                return Project(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:migrate/latest:VMwareCollector":
                return VMwareCollector(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "migrate/latest", _module_instance)

_register_module()
