# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .file import *
from .get_file import *
from .get_project import *
from .get_service import *
from .get_service_task import *
from .get_task import *
from .project import *
from .service import *
from .service_task import *
from .task import *
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
            if typ == "azure-nextgen:datamigration/v20180715preview:File":
                return File(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:datamigration/v20180715preview:Project":
                return Project(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:datamigration/v20180715preview:Service":
                return Service(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:datamigration/v20180715preview:ServiceTask":
                return ServiceTask(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:datamigration/v20180715preview:Task":
                return Task(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "datamigration/v20180715preview", _module_instance)

_register_module()
