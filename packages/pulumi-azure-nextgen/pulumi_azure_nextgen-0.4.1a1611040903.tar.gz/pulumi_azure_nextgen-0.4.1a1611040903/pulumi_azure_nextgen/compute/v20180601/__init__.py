# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .availability_set import *
from .disk import *
from .gallery import *
from .gallery_image import *
from .gallery_image_version import *
from .get_availability_set import *
from .get_disk import *
from .get_gallery import *
from .get_gallery_image import *
from .get_gallery_image_version import *
from .get_image import *
from .get_log_analytic_export_request_rate_by_interval import *
from .get_log_analytic_export_throttled_requests import *
from .get_proximity_placement_group import *
from .get_snapshot import *
from .get_virtual_machine import *
from .get_virtual_machine_extension import *
from .get_virtual_machine_scale_set import *
from .get_virtual_machine_scale_set_extension import *
from .get_virtual_machine_scale_set_vm import *
from .image import *
from .proximity_placement_group import *
from .snapshot import *
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
            if typ == "azure-nextgen:compute/v20180601:AvailabilitySet":
                return AvailabilitySet(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:Disk":
                return Disk(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:Gallery":
                return Gallery(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:GalleryImage":
                return GalleryImage(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:GalleryImageVersion":
                return GalleryImageVersion(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:Image":
                return Image(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:ProximityPlacementGroup":
                return ProximityPlacementGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:Snapshot":
                return Snapshot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:VirtualMachine":
                return VirtualMachine(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:VirtualMachineExtension":
                return VirtualMachineExtension(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:VirtualMachineScaleSet":
                return VirtualMachineScaleSet(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:VirtualMachineScaleSetExtension":
                return VirtualMachineScaleSetExtension(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:compute/v20180601:VirtualMachineScaleSetVM":
                return VirtualMachineScaleSetVM(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "compute/v20180601", _module_instance)

_register_module()
