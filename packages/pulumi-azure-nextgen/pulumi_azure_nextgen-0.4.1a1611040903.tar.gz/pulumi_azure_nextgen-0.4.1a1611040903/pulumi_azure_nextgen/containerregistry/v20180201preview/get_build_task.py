# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs

__all__ = [
    'GetBuildTaskResult',
    'AwaitableGetBuildTaskResult',
    'get_build_task',
]

@pulumi.output_type
class GetBuildTaskResult:
    """
    The build task that has the resource properties and all build items. The build task will have all information to schedule a build against it.
    """
    def __init__(__self__, alias=None, creation_date=None, id=None, location=None, name=None, platform=None, provisioning_state=None, source_repository=None, status=None, tags=None, timeout=None, type=None):
        if alias and not isinstance(alias, str):
            raise TypeError("Expected argument 'alias' to be a str")
        pulumi.set(__self__, "alias", alias)
        if creation_date and not isinstance(creation_date, str):
            raise TypeError("Expected argument 'creation_date' to be a str")
        pulumi.set(__self__, "creation_date", creation_date)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if platform and not isinstance(platform, dict):
            raise TypeError("Expected argument 'platform' to be a dict")
        pulumi.set(__self__, "platform", platform)
        if provisioning_state and not isinstance(provisioning_state, str):
            raise TypeError("Expected argument 'provisioning_state' to be a str")
        pulumi.set(__self__, "provisioning_state", provisioning_state)
        if source_repository and not isinstance(source_repository, dict):
            raise TypeError("Expected argument 'source_repository' to be a dict")
        pulumi.set(__self__, "source_repository", source_repository)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if timeout and not isinstance(timeout, int):
            raise TypeError("Expected argument 'timeout' to be a int")
        pulumi.set(__self__, "timeout", timeout)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def alias(self) -> str:
        """
        The alternative updatable name for a build task.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter(name="creationDate")
    def creation_date(self) -> str:
        """
        The creation date of build task.
        """
        return pulumi.get(self, "creation_date")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The resource ID.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The location of the resource. This cannot be changed after the resource is created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def platform(self) -> 'outputs.PlatformPropertiesResponse':
        """
        The platform properties against which the build has to happen.
        """
        return pulumi.get(self, "platform")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> str:
        """
        The provisioning state of the build task.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="sourceRepository")
    def source_repository(self) -> 'outputs.SourceRepositoryPropertiesResponse':
        """
        The properties that describes the source(code) for the build task.
        """
        return pulumi.get(self, "source_repository")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        The current status of build task.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, str]]:
        """
        The tags of the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def timeout(self) -> Optional[int]:
        """
        Build timeout in seconds.
        """
        return pulumi.get(self, "timeout")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")


class AwaitableGetBuildTaskResult(GetBuildTaskResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetBuildTaskResult(
            alias=self.alias,
            creation_date=self.creation_date,
            id=self.id,
            location=self.location,
            name=self.name,
            platform=self.platform,
            provisioning_state=self.provisioning_state,
            source_repository=self.source_repository,
            status=self.status,
            tags=self.tags,
            timeout=self.timeout,
            type=self.type)


def get_build_task(build_task_name: Optional[str] = None,
                   registry_name: Optional[str] = None,
                   resource_group_name: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetBuildTaskResult:
    """
    Use this data source to access information about an existing resource.

    :param str build_task_name: The name of the container registry build task.
    :param str registry_name: The name of the container registry.
    :param str resource_group_name: The name of the resource group to which the container registry belongs.
    """
    __args__ = dict()
    __args__['buildTaskName'] = build_task_name
    __args__['registryName'] = registry_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:containerregistry/v20180201preview:getBuildTask', __args__, opts=opts, typ=GetBuildTaskResult).value

    return AwaitableGetBuildTaskResult(
        alias=__ret__.alias,
        creation_date=__ret__.creation_date,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        platform=__ret__.platform,
        provisioning_state=__ret__.provisioning_state,
        source_repository=__ret__.source_repository,
        status=__ret__.status,
        tags=__ret__.tags,
        timeout=__ret__.timeout,
        type=__ret__.type)
