# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .availability_set import *
from .get_availability_set import *
from .get_image import *
from .get_log_analytic_export_request_rate_by_interval import *
from .get_log_analytic_export_throttled_requests import *
from .get_proximity_placement_group import *
from .get_virtual_machine import *
from .get_virtual_machine_extension import *
from .get_virtual_machine_scale_set import *
from .get_virtual_machine_scale_set_extension import *
from .get_virtual_machine_scale_set_vm import *
from .image import *
from .proximity_placement_group import *
from .virtual_machine import *
from .virtual_machine_extension import *
from .virtual_machine_scale_set import *
from .virtual_machine_scale_set_extension import *
from .virtual_machine_scale_set_vm import *
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
            if typ == "azure-nextgen:compute/v20181001:AvailabilitySet":
                return AvailabilitySet(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20181001:Image":
                return Image(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20181001:ProximityPlacementGroup":
                return ProximityPlacementGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20181001:VirtualMachine":
                return VirtualMachine(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20181001:VirtualMachineExtension":
                return VirtualMachineExtension(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20181001:VirtualMachineScaleSet":
                return VirtualMachineScaleSet(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20181001:VirtualMachineScaleSetExtension":
                return VirtualMachineScaleSetExtension(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20181001:VirtualMachineScaleSetVM":
                return VirtualMachineScaleSetVM(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "compute/v20181001", _module_instance)

_register_module()
