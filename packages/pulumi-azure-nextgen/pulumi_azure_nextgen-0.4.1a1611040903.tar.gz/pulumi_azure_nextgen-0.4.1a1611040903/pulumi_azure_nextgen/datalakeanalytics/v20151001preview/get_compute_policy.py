# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'GetComputePolicyResult',
    'AwaitableGetComputePolicyResult',
    'get_compute_policy',
]

@pulumi.output_type
class GetComputePolicyResult:
    """
    Data Lake Analytics compute policy information.
    """
    def __init__(__self__, id=None, max_degree_of_parallelism_per_job=None, min_priority_per_job=None, name=None, object_id=None, object_type=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if max_degree_of_parallelism_per_job and not isinstance(max_degree_of_parallelism_per_job, int):
            raise TypeError("Expected argument 'max_degree_of_parallelism_per_job' to be a int")
        pulumi.set(__self__, "max_degree_of_parallelism_per_job", max_degree_of_parallelism_per_job)
        if min_priority_per_job and not isinstance(min_priority_per_job, int):
            raise TypeError("Expected argument 'min_priority_per_job' to be a int")
        pulumi.set(__self__, "min_priority_per_job", min_priority_per_job)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if object_id and not isinstance(object_id, str):
            raise TypeError("Expected argument 'object_id' to be a str")
        pulumi.set(__self__, "object_id", object_id)
        if object_type and not isinstance(object_type, str):
            raise TypeError("Expected argument 'object_type' to be a str")
        pulumi.set(__self__, "object_type", object_type)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource identifier.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="maxDegreeOfParallelismPerJob")
    def max_degree_of_parallelism_per_job(self) -> int:
        """
        The maximum degree of parallelism per job this user can use to submit jobs.
        """
        return pulumi.get(self, "max_degree_of_parallelism_per_job")

    @property
    @pulumi.getter(name="minPriorityPerJob")
    def min_priority_per_job(self) -> int:
        """
        The minimum priority per job this user can use to submit jobs.
        """
        return pulumi.get(self, "min_priority_per_job")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> str:
        """
        The AAD object identifier for the entity to create a policy for.
        """
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter(name="objectType")
    def object_type(self) -> str:
        """
        The type of AAD object the object identifier refers to.
        """
        return pulumi.get(self, "object_type")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The resource type.
        """
        return pulumi.get(self, "type")


class AwaitableGetComputePolicyResult(GetComputePolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetComputePolicyResult(
            id=self.id,
            max_degree_of_parallelism_per_job=self.max_degree_of_parallelism_per_job,
            min_priority_per_job=self.min_priority_per_job,
            name=self.name,
            object_id=self.object_id,
            object_type=self.object_type,
            type=self.type)


def get_compute_policy(account_name: Optional[str] = None,
                       compute_policy_name: Optional[str] = None,
                       resource_group_name: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetComputePolicyResult:
    """
    Use this data source to access information about an existing resource.

    :param str account_name: The name of the Data Lake Analytics account.
    :param str compute_policy_name: The name of the compute policy to retrieve.
    :param str resource_group_name: The name of the Azure resource group.
    """
    __args__ = dict()
    __args__['accountName'] = account_name
    __args__['computePolicyName'] = compute_policy_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:datalakeanalytics/v20151001preview:getComputePolicy', __args__, opts=opts, typ=GetComputePolicyResult).value

    return AwaitableGetComputePolicyResult(
        id=__ret__.id,
        max_degree_of_parallelism_per_job=__ret__.max_degree_of_parallelism_per_job,
        min_priority_per_job=__ret__.min_priority_per_job,
        name=__ret__.name,
        object_id=__ret__.object_id,
        object_type=__ret__.object_type,
        type=__ret__.type)
