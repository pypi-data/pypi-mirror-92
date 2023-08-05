# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = [
    'AKSArgs',
    'AKSPropertiesArgs',
    'BatchAIArgs',
    'BatchAIPropertiesArgs',
    'DataFactoryArgs',
    'HDInsightArgs',
    'HDInsightPropertiesArgs',
    'IdentityArgs',
    'ScaleSettingsArgs',
    'SslConfigurationArgs',
    'VirtualMachineArgs',
    'VirtualMachinePropertiesArgs',
    'VirtualMachineSshCredentialsArgs',
]

@pulumi.input_type
class AKSArgs:
    def __init__(__self__, *,
                 compute_type: pulumi.Input[str],
                 compute_location: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['AKSPropertiesArgs']] = None,
                 resource_id: Optional[pulumi.Input[str]] = None):
        """
        A Machine Learning compute based on AKS.
        :param pulumi.Input[str] compute_type: The type of compute
               Expected value is 'AKS'.
        :param pulumi.Input[str] compute_location: Location for the underlying compute
        :param pulumi.Input[str] description: The description of the Machine Learning compute.
        :param pulumi.Input['AKSPropertiesArgs'] properties: AKS properties
        :param pulumi.Input[str] resource_id: ARM resource id of the compute
        """
        pulumi.set(__self__, "compute_type", 'AKS')
        if compute_location is not None:
            pulumi.set(__self__, "compute_location", compute_location)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="computeType")
    def compute_type(self) -> pulumi.Input[str]:
        """
        The type of compute
        Expected value is 'AKS'.
        """
        return pulumi.get(self, "compute_type")

    @compute_type.setter
    def compute_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "compute_type", value)

    @property
    @pulumi.getter(name="computeLocation")
    def compute_location(self) -> Optional[pulumi.Input[str]]:
        """
        Location for the underlying compute
        """
        return pulumi.get(self, "compute_location")

    @compute_location.setter
    def compute_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compute_location", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Machine Learning compute.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['AKSPropertiesArgs']]:
        """
        AKS properties
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['AKSPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        ARM resource id of the compute
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)


@pulumi.input_type
class AKSPropertiesArgs:
    def __init__(__self__, *,
                 agent_count: Optional[pulumi.Input[int]] = None,
                 agent_vm_size: Optional[pulumi.Input[str]] = None,
                 cluster_fqdn: Optional[pulumi.Input[str]] = None,
                 ssl_configuration: Optional[pulumi.Input['SslConfigurationArgs']] = None):
        """
        AKS properties
        :param pulumi.Input[int] agent_count: Number of agents
        :param pulumi.Input[str] agent_vm_size: Agent virtual machine size
        :param pulumi.Input[str] cluster_fqdn: Cluster full qualified domain name
        :param pulumi.Input['SslConfigurationArgs'] ssl_configuration: SSL configuration
        """
        if agent_count is not None:
            pulumi.set(__self__, "agent_count", agent_count)
        if agent_vm_size is not None:
            pulumi.set(__self__, "agent_vm_size", agent_vm_size)
        if cluster_fqdn is not None:
            pulumi.set(__self__, "cluster_fqdn", cluster_fqdn)
        if ssl_configuration is not None:
            pulumi.set(__self__, "ssl_configuration", ssl_configuration)

    @property
    @pulumi.getter(name="agentCount")
    def agent_count(self) -> Optional[pulumi.Input[int]]:
        """
        Number of agents
        """
        return pulumi.get(self, "agent_count")

    @agent_count.setter
    def agent_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "agent_count", value)

    @property
    @pulumi.getter(name="agentVMSize")
    def agent_vm_size(self) -> Optional[pulumi.Input[str]]:
        """
        Agent virtual machine size
        """
        return pulumi.get(self, "agent_vm_size")

    @agent_vm_size.setter
    def agent_vm_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "agent_vm_size", value)

    @property
    @pulumi.getter(name="clusterFqdn")
    def cluster_fqdn(self) -> Optional[pulumi.Input[str]]:
        """
        Cluster full qualified domain name
        """
        return pulumi.get(self, "cluster_fqdn")

    @cluster_fqdn.setter
    def cluster_fqdn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_fqdn", value)

    @property
    @pulumi.getter(name="sslConfiguration")
    def ssl_configuration(self) -> Optional[pulumi.Input['SslConfigurationArgs']]:
        """
        SSL configuration
        """
        return pulumi.get(self, "ssl_configuration")

    @ssl_configuration.setter
    def ssl_configuration(self, value: Optional[pulumi.Input['SslConfigurationArgs']]):
        pulumi.set(self, "ssl_configuration", value)


@pulumi.input_type
class BatchAIArgs:
    def __init__(__self__, *,
                 compute_type: pulumi.Input[str],
                 compute_location: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['BatchAIPropertiesArgs']] = None,
                 resource_id: Optional[pulumi.Input[str]] = None):
        """
        A Machine Learning compute based on Azure BatchAI.
        :param pulumi.Input[str] compute_type: The type of compute
               Expected value is 'BatchAI'.
        :param pulumi.Input[str] compute_location: Location for the underlying compute
        :param pulumi.Input[str] description: The description of the Machine Learning compute.
        :param pulumi.Input['BatchAIPropertiesArgs'] properties: BatchAI properties
        :param pulumi.Input[str] resource_id: ARM resource id of the compute
        """
        pulumi.set(__self__, "compute_type", 'BatchAI')
        if compute_location is not None:
            pulumi.set(__self__, "compute_location", compute_location)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="computeType")
    def compute_type(self) -> pulumi.Input[str]:
        """
        The type of compute
        Expected value is 'BatchAI'.
        """
        return pulumi.get(self, "compute_type")

    @compute_type.setter
    def compute_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "compute_type", value)

    @property
    @pulumi.getter(name="computeLocation")
    def compute_location(self) -> Optional[pulumi.Input[str]]:
        """
        Location for the underlying compute
        """
        return pulumi.get(self, "compute_location")

    @compute_location.setter
    def compute_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compute_location", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Machine Learning compute.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['BatchAIPropertiesArgs']]:
        """
        BatchAI properties
        """
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['BatchAIPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        ARM resource id of the compute
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)


@pulumi.input_type
class BatchAIPropertiesArgs:
    def __init__(__self__, *,
                 scale_settings: Optional[pulumi.Input['ScaleSettingsArgs']] = None,
                 vm_priority: Optional[pulumi.Input[str]] = None,
                 vm_size: Optional[pulumi.Input[str]] = None):
        """
        BatchAI properties
        :param pulumi.Input['ScaleSettingsArgs'] scale_settings: Scale settings for BatchAI
        :param pulumi.Input[str] vm_priority: Virtual Machine priority
        :param pulumi.Input[str] vm_size: Virtual Machine Size
        """
        if scale_settings is not None:
            pulumi.set(__self__, "scale_settings", scale_settings)
        if vm_priority is not None:
            pulumi.set(__self__, "vm_priority", vm_priority)
        if vm_size is not None:
            pulumi.set(__self__, "vm_size", vm_size)

    @property
    @pulumi.getter(name="scaleSettings")
    def scale_settings(self) -> Optional[pulumi.Input['ScaleSettingsArgs']]:
        """
        Scale settings for BatchAI
        """
        return pulumi.get(self, "scale_settings")

    @scale_settings.setter
    def scale_settings(self, value: Optional[pulumi.Input['ScaleSettingsArgs']]):
        pulumi.set(self, "scale_settings", value)

    @property
    @pulumi.getter(name="vmPriority")
    def vm_priority(self) -> Optional[pulumi.Input[str]]:
        """
        Virtual Machine priority
        """
        return pulumi.get(self, "vm_priority")

    @vm_priority.setter
    def vm_priority(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vm_priority", value)

    @property
    @pulumi.getter(name="vmSize")
    def vm_size(self) -> Optional[pulumi.Input[str]]:
        """
        Virtual Machine Size
        """
        return pulumi.get(self, "vm_size")

    @vm_size.setter
    def vm_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "vm_size", value)


@pulumi.input_type
class DataFactoryArgs:
    def __init__(__self__, *,
                 compute_type: pulumi.Input[str],
                 compute_location: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None):
        """
        A DataFactory compute.
        :param pulumi.Input[str] compute_type: The type of compute
               Expected value is 'DataFactory'.
        :param pulumi.Input[str] compute_location: Location for the underlying compute
        :param pulumi.Input[str] description: The description of the Machine Learning compute.
        :param pulumi.Input[str] resource_id: ARM resource id of the compute
        """
        pulumi.set(__self__, "compute_type", 'DataFactory')
        if compute_location is not None:
            pulumi.set(__self__, "compute_location", compute_location)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="computeType")
    def compute_type(self) -> pulumi.Input[str]:
        """
        The type of compute
        Expected value is 'DataFactory'.
        """
        return pulumi.get(self, "compute_type")

    @compute_type.setter
    def compute_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "compute_type", value)

    @property
    @pulumi.getter(name="computeLocation")
    def compute_location(self) -> Optional[pulumi.Input[str]]:
        """
        Location for the underlying compute
        """
        return pulumi.get(self, "compute_location")

    @compute_location.setter
    def compute_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compute_location", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Machine Learning compute.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        ARM resource id of the compute
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)


@pulumi.input_type
class HDInsightArgs:
    def __init__(__self__, *,
                 compute_type: pulumi.Input[str],
                 compute_location: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['HDInsightPropertiesArgs']] = None,
                 resource_id: Optional[pulumi.Input[str]] = None):
        """
        A HDInsight compute.
        :param pulumi.Input[str] compute_type: The type of compute
               Expected value is 'HDInsight'.
        :param pulumi.Input[str] compute_location: Location for the underlying compute
        :param pulumi.Input[str] description: The description of the Machine Learning compute.
        :param pulumi.Input[str] resource_id: ARM resource id of the compute
        """
        pulumi.set(__self__, "compute_type", 'HDInsight')
        if compute_location is not None:
            pulumi.set(__self__, "compute_location", compute_location)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="computeType")
    def compute_type(self) -> pulumi.Input[str]:
        """
        The type of compute
        Expected value is 'HDInsight'.
        """
        return pulumi.get(self, "compute_type")

    @compute_type.setter
    def compute_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "compute_type", value)

    @property
    @pulumi.getter(name="computeLocation")
    def compute_location(self) -> Optional[pulumi.Input[str]]:
        """
        Location for the underlying compute
        """
        return pulumi.get(self, "compute_location")

    @compute_location.setter
    def compute_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compute_location", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Machine Learning compute.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['HDInsightPropertiesArgs']]:
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['HDInsightPropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        ARM resource id of the compute
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)


@pulumi.input_type
class HDInsightPropertiesArgs:
    def __init__(__self__, *,
                 address: Optional[pulumi.Input[str]] = None,
                 administrator_account: Optional[pulumi.Input['VirtualMachineSshCredentialsArgs']] = None,
                 ssh_port: Optional[pulumi.Input[int]] = None):
        """
        :param pulumi.Input[str] address: Public IP address of the master node of the cluster.
        :param pulumi.Input['VirtualMachineSshCredentialsArgs'] administrator_account: Admin credentials for master node of the cluster
        :param pulumi.Input[int] ssh_port: Port open for ssh connections on the master node of the cluster.
        """
        if address is not None:
            pulumi.set(__self__, "address", address)
        if administrator_account is not None:
            pulumi.set(__self__, "administrator_account", administrator_account)
        if ssh_port is not None:
            pulumi.set(__self__, "ssh_port", ssh_port)

    @property
    @pulumi.getter
    def address(self) -> Optional[pulumi.Input[str]]:
        """
        Public IP address of the master node of the cluster.
        """
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter(name="administratorAccount")
    def administrator_account(self) -> Optional[pulumi.Input['VirtualMachineSshCredentialsArgs']]:
        """
        Admin credentials for master node of the cluster
        """
        return pulumi.get(self, "administrator_account")

    @administrator_account.setter
    def administrator_account(self, value: Optional[pulumi.Input['VirtualMachineSshCredentialsArgs']]):
        pulumi.set(self, "administrator_account", value)

    @property
    @pulumi.getter(name="sshPort")
    def ssh_port(self) -> Optional[pulumi.Input[int]]:
        """
        Port open for ssh connections on the master node of the cluster.
        """
        return pulumi.get(self, "ssh_port")

    @ssh_port.setter
    def ssh_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ssh_port", value)


@pulumi.input_type
class IdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input['ResourceIdentityType']] = None):
        """
        Identity for the resource.
        :param pulumi.Input['ResourceIdentityType'] type: The identity type.
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['ResourceIdentityType']]:
        """
        The identity type.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['ResourceIdentityType']]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class ScaleSettingsArgs:
    def __init__(__self__, *,
                 auto_scale_enabled: Optional[pulumi.Input[bool]] = None,
                 max_node_count: Optional[pulumi.Input[int]] = None,
                 min_node_count: Optional[pulumi.Input[int]] = None):
        """
        scale settings for BatchAI Compute
        :param pulumi.Input[bool] auto_scale_enabled: Enable or disable auto scale
        :param pulumi.Input[int] max_node_count: Max number of nodes to use
        :param pulumi.Input[int] min_node_count: Min number of nodes to use
        """
        if auto_scale_enabled is not None:
            pulumi.set(__self__, "auto_scale_enabled", auto_scale_enabled)
        if max_node_count is not None:
            pulumi.set(__self__, "max_node_count", max_node_count)
        if min_node_count is not None:
            pulumi.set(__self__, "min_node_count", min_node_count)

    @property
    @pulumi.getter(name="autoScaleEnabled")
    def auto_scale_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable or disable auto scale
        """
        return pulumi.get(self, "auto_scale_enabled")

    @auto_scale_enabled.setter
    def auto_scale_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_scale_enabled", value)

    @property
    @pulumi.getter(name="maxNodeCount")
    def max_node_count(self) -> Optional[pulumi.Input[int]]:
        """
        Max number of nodes to use
        """
        return pulumi.get(self, "max_node_count")

    @max_node_count.setter
    def max_node_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_node_count", value)

    @property
    @pulumi.getter(name="minNodeCount")
    def min_node_count(self) -> Optional[pulumi.Input[int]]:
        """
        Min number of nodes to use
        """
        return pulumi.get(self, "min_node_count")

    @min_node_count.setter
    def min_node_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "min_node_count", value)


@pulumi.input_type
class SslConfigurationArgs:
    def __init__(__self__, *,
                 cert: Optional[pulumi.Input[str]] = None,
                 cname: Optional[pulumi.Input[str]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        The SSL configuration for scoring
        :param pulumi.Input[str] cert: Cert data
        :param pulumi.Input[str] cname: CNAME of the cert
        :param pulumi.Input[str] key: Key data
        :param pulumi.Input[str] status: Enable or disable SSL for scoring
        """
        if cert is not None:
            pulumi.set(__self__, "cert", cert)
        if cname is not None:
            pulumi.set(__self__, "cname", cname)
        if key is not None:
            pulumi.set(__self__, "key", key)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter
    def cert(self) -> Optional[pulumi.Input[str]]:
        """
        Cert data
        """
        return pulumi.get(self, "cert")

    @cert.setter
    def cert(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cert", value)

    @property
    @pulumi.getter
    def cname(self) -> Optional[pulumi.Input[str]]:
        """
        CNAME of the cert
        """
        return pulumi.get(self, "cname")

    @cname.setter
    def cname(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cname", value)

    @property
    @pulumi.getter
    def key(self) -> Optional[pulumi.Input[str]]:
        """
        Key data
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        Enable or disable SSL for scoring
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


@pulumi.input_type
class VirtualMachineArgs:
    def __init__(__self__, *,
                 compute_type: pulumi.Input[str],
                 compute_location: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input['VirtualMachinePropertiesArgs']] = None,
                 resource_id: Optional[pulumi.Input[str]] = None):
        """
        A Machine Learning compute based on Azure Virtual Machines.
        :param pulumi.Input[str] compute_type: The type of compute
               Expected value is 'VirtualMachine'.
        :param pulumi.Input[str] compute_location: Location for the underlying compute
        :param pulumi.Input[str] description: The description of the Machine Learning compute.
        :param pulumi.Input[str] resource_id: ARM resource id of the compute
        """
        pulumi.set(__self__, "compute_type", 'VirtualMachine')
        if compute_location is not None:
            pulumi.set(__self__, "compute_location", compute_location)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if properties is not None:
            pulumi.set(__self__, "properties", properties)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="computeType")
    def compute_type(self) -> pulumi.Input[str]:
        """
        The type of compute
        Expected value is 'VirtualMachine'.
        """
        return pulumi.get(self, "compute_type")

    @compute_type.setter
    def compute_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "compute_type", value)

    @property
    @pulumi.getter(name="computeLocation")
    def compute_location(self) -> Optional[pulumi.Input[str]]:
        """
        Location for the underlying compute
        """
        return pulumi.get(self, "compute_location")

    @compute_location.setter
    def compute_location(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "compute_location", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the Machine Learning compute.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def properties(self) -> Optional[pulumi.Input['VirtualMachinePropertiesArgs']]:
        return pulumi.get(self, "properties")

    @properties.setter
    def properties(self, value: Optional[pulumi.Input['VirtualMachinePropertiesArgs']]):
        pulumi.set(self, "properties", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        ARM resource id of the compute
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)


@pulumi.input_type
class VirtualMachinePropertiesArgs:
    def __init__(__self__, *,
                 address: Optional[pulumi.Input[str]] = None,
                 administrator_account: Optional[pulumi.Input['VirtualMachineSshCredentialsArgs']] = None,
                 ssh_port: Optional[pulumi.Input[int]] = None,
                 virtual_machine_size: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] address: Public IP address of the virtual machine.
        :param pulumi.Input['VirtualMachineSshCredentialsArgs'] administrator_account: Admin credentials for virtual machine
        :param pulumi.Input[int] ssh_port: Port open for ssh connections.
        :param pulumi.Input[str] virtual_machine_size: Virtual Machine size
        """
        if address is not None:
            pulumi.set(__self__, "address", address)
        if administrator_account is not None:
            pulumi.set(__self__, "administrator_account", administrator_account)
        if ssh_port is not None:
            pulumi.set(__self__, "ssh_port", ssh_port)
        if virtual_machine_size is not None:
            pulumi.set(__self__, "virtual_machine_size", virtual_machine_size)

    @property
    @pulumi.getter
    def address(self) -> Optional[pulumi.Input[str]]:
        """
        Public IP address of the virtual machine.
        """
        return pulumi.get(self, "address")

    @address.setter
    def address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "address", value)

    @property
    @pulumi.getter(name="administratorAccount")
    def administrator_account(self) -> Optional[pulumi.Input['VirtualMachineSshCredentialsArgs']]:
        """
        Admin credentials for virtual machine
        """
        return pulumi.get(self, "administrator_account")

    @administrator_account.setter
    def administrator_account(self, value: Optional[pulumi.Input['VirtualMachineSshCredentialsArgs']]):
        pulumi.set(self, "administrator_account", value)

    @property
    @pulumi.getter(name="sshPort")
    def ssh_port(self) -> Optional[pulumi.Input[int]]:
        """
        Port open for ssh connections.
        """
        return pulumi.get(self, "ssh_port")

    @ssh_port.setter
    def ssh_port(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ssh_port", value)

    @property
    @pulumi.getter(name="virtualMachineSize")
    def virtual_machine_size(self) -> Optional[pulumi.Input[str]]:
        """
        Virtual Machine size
        """
        return pulumi.get(self, "virtual_machine_size")

    @virtual_machine_size.setter
    def virtual_machine_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "virtual_machine_size", value)


@pulumi.input_type
class VirtualMachineSshCredentialsArgs:
    def __init__(__self__, *,
                 password: Optional[pulumi.Input[str]] = None,
                 private_key_data: Optional[pulumi.Input[str]] = None,
                 public_key_data: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Admin credentials for virtual machine
        :param pulumi.Input[str] password: Password of admin account
        :param pulumi.Input[str] private_key_data: Private key data
        :param pulumi.Input[str] public_key_data: Public key data
        :param pulumi.Input[str] username: Username of admin account
        """
        if password is not None:
            pulumi.set(__self__, "password", password)
        if private_key_data is not None:
            pulumi.set(__self__, "private_key_data", private_key_data)
        if public_key_data is not None:
            pulumi.set(__self__, "public_key_data", public_key_data)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        Password of admin account
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="privateKeyData")
    def private_key_data(self) -> Optional[pulumi.Input[str]]:
        """
        Private key data
        """
        return pulumi.get(self, "private_key_data")

    @private_key_data.setter
    def private_key_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_key_data", value)

    @property
    @pulumi.getter(name="publicKeyData")
    def public_key_data(self) -> Optional[pulumi.Input[str]]:
        """
        Public key data
        """
        return pulumi.get(self, "public_key_data")

    @public_key_data.setter
    def public_key_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_key_data", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        """
        Username of admin account
        """
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


