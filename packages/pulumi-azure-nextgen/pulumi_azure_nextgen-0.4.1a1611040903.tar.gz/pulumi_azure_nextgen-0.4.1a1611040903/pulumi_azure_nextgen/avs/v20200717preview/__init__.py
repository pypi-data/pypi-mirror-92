# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .addon import *
from .authorization import *
from .cluster import *
from .get_addon import *
from .get_authorization import *
from .get_cluster import *
from .get_global_reach_connection import *
from .get_hcx_enterprise_site import *
from .get_private_cloud import *
from .get_workload_network_dhcp import *
from .get_workload_network_dns_service import *
from .get_workload_network_dns_zone import *
from .get_workload_network_port_mirroring import *
from .get_workload_network_segment import *
from .get_workload_network_vm_group import *
from .global_reach_connection import *
from .hcx_enterprise_site import *
from .list_private_cloud_admin_credentials import *
from .private_cloud import *
from .workload_network_dhcp import *
from .workload_network_dns_service import *
from .workload_network_dns_zone import *
from .workload_network_port_mirroring import *
from .workload_network_segment import *
from .workload_network_vm_group import *
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
            if typ == "azure-nextgen:avs/v20200717preview:Addon":
                return Addon(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:avs/v20200717preview:Authorization":
                return Authorization(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:avs/v20200717preview:Cluster":
                return Cluster(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:avs/v20200717preview:GlobalReachConnection":
                return GlobalReachConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:avs/v20200717preview:HcxEnterpriseSite":
                return HcxEnterpriseSite(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:avs/v20200717preview:PrivateCloud":
                return PrivateCloud(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:avs/v20200717preview:WorkloadNetworkDhcp":
                return WorkloadNetworkDhcp(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:avs/v20200717preview:WorkloadNetworkDnsService":
                return WorkloadNetworkDnsService(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:avs/v20200717preview:WorkloadNetworkDnsZone":
                return WorkloadNetworkDnsZone(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:avs/v20200717preview:WorkloadNetworkPortMirroring":
                return WorkloadNetworkPortMirroring(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:avs/v20200717preview:WorkloadNetworkSegment":
                return WorkloadNetworkSegment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:avs/v20200717preview:WorkloadNetworkVMGroup":
                return WorkloadNetworkVMGroup(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "avs/v20200717preview", _module_instance)

_register_module()
