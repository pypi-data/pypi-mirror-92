# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .certificate import *
from .certificate_csr import *
from .get_certificate import *
from .get_certificate_csr import *
from .get_hosting_environment import *
from .get_managed_hosting_environment import *
from .get_server_farm import *
from .get_site import *
from .get_site_deployment import *
from .get_site_deployment_slot import *
from .get_site_host_name_binding import *
from .get_site_host_name_binding_slot import *
from .get_site_instance_deployment import *
from .get_site_instance_deployment_slot import *
from .get_site_logs_config import *
from .get_site_relay_service_connection import *
from .get_site_relay_service_connection_slot import *
from .get_site_slot import *
from .get_site_slot_config_names import *
from .get_site_source_control import *
from .get_site_source_control_slot import *
from .get_site_vnet_connection import *
from .get_site_vnet_connection_slot import *
from .hosting_environment import *
from .list_site_app_settings import *
from .list_site_app_settings_slot import *
from .list_site_auth_settings import *
from .list_site_auth_settings_slot import *
from .list_site_backup_configuration import *
from .list_site_backup_configuration_slot import *
from .list_site_backup_status_secrets import *
from .list_site_backup_status_secrets_slot import *
from .list_site_connection_strings import *
from .list_site_connection_strings_slot import *
from .list_site_metadata import *
from .list_site_metadata_slot import *
from .list_site_publishing_credentials import *
from .list_site_publishing_credentials_slot import *
from .managed_hosting_environment import *
from .server_farm import *
from .server_farm_route_for_vnet import *
from .site import *
from .site_deployment import *
from .site_deployment_slot import *
from .site_host_name_binding import *
from .site_host_name_binding_slot import *
from .site_instance_deployment import *
from .site_instance_deployment_slot import *
from .site_logs_config import *
from .site_relay_service_connection import *
from .site_relay_service_connection_slot import *
from .site_slot import *
from .site_slot_config_names import *
from .site_source_control import *
from .site_source_control_slot import *
from .site_vnet_connection import *
from .site_vnet_connection_slot import *
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
            if typ == "azure-nextgen:web/v20150801:Certificate":
                return Certificate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:CertificateCsr":
                return CertificateCsr(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:HostingEnvironment":
                return HostingEnvironment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:ManagedHostingEnvironment":
                return ManagedHostingEnvironment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:ServerFarm":
                return ServerFarm(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:ServerFarmRouteForVnet":
                return ServerFarmRouteForVnet(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:Site":
                return Site(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteDeployment":
                return SiteDeployment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteDeploymentSlot":
                return SiteDeploymentSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteHostNameBinding":
                return SiteHostNameBinding(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteHostNameBindingSlot":
                return SiteHostNameBindingSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteInstanceDeployment":
                return SiteInstanceDeployment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteInstanceDeploymentSlot":
                return SiteInstanceDeploymentSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteLogsConfig":
                return SiteLogsConfig(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteRelayServiceConnection":
                return SiteRelayServiceConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteRelayServiceConnectionSlot":
                return SiteRelayServiceConnectionSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteSlot":
                return SiteSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteSlotConfigNames":
                return SiteSlotConfigNames(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteSourceControl":
                return SiteSourceControl(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteSourceControlSlot":
                return SiteSourceControlSlot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteVNETConnection":
                return SiteVNETConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-nextgen:web/v20150801:SiteVNETConnectionSlot":
                return SiteVNETConnectionSlot(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-nextgen", "web/v20150801", _module_instance)

_register_module()
