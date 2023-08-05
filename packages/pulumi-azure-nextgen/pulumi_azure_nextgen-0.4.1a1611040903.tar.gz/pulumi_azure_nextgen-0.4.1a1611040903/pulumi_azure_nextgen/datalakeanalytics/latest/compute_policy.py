# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from ._enums import *

__all__ = ['ComputePolicy']


class ComputePolicy(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 compute_policy_name: Optional[pulumi.Input[str]] = None,
                 max_degree_of_parallelism_per_job: Optional[pulumi.Input[int]] = None,
                 min_priority_per_job: Optional[pulumi.Input[int]] = None,
                 object_id: Optional[pulumi.Input[str]] = None,
                 object_type: Optional[pulumi.Input[Union[str, 'AADObjectType']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Data Lake Analytics compute policy information.
        Latest API Version: 2016-11-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the Data Lake Analytics account.
        :param pulumi.Input[str] compute_policy_name: The name of the compute policy to create or update.
        :param pulumi.Input[int] max_degree_of_parallelism_per_job: The maximum degree of parallelism per job this user can use to submit jobs. This property, the min priority per job property, or both must be passed.
        :param pulumi.Input[int] min_priority_per_job: The minimum priority per job this user can use to submit jobs. This property, the max degree of parallelism per job property, or both must be passed.
        :param pulumi.Input[str] object_id: The AAD object identifier for the entity to create a policy for.
        :param pulumi.Input[Union[str, 'AADObjectType']] object_type: The type of AAD object the object identifier refers to.
        :param pulumi.Input[str] resource_group_name: The name of the Azure resource group.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            if account_name is None and not opts.urn:
                raise TypeError("Missing required property 'account_name'")
            __props__['account_name'] = account_name
            if compute_policy_name is None and not opts.urn:
                raise TypeError("Missing required property 'compute_policy_name'")
            __props__['compute_policy_name'] = compute_policy_name
            __props__['max_degree_of_parallelism_per_job'] = max_degree_of_parallelism_per_job
            __props__['min_priority_per_job'] = min_priority_per_job
            if object_id is None and not opts.urn:
                raise TypeError("Missing required property 'object_id'")
            __props__['object_id'] = object_id
            if object_type is None and not opts.urn:
                raise TypeError("Missing required property 'object_type'")
            __props__['object_type'] = object_type
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:datalakeanalytics/v20151001preview:ComputePolicy"), pulumi.Alias(type_="azure-nextgen:datalakeanalytics/v20161101:ComputePolicy")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(ComputePolicy, __self__).__init__(
            'azure-nextgen:datalakeanalytics/latest:ComputePolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'ComputePolicy':
        """
        Get an existing ComputePolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return ComputePolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="maxDegreeOfParallelismPerJob")
    def max_degree_of_parallelism_per_job(self) -> pulumi.Output[int]:
        """
        The maximum degree of parallelism per job this user can use to submit jobs.
        """
        return pulumi.get(self, "max_degree_of_parallelism_per_job")

    @property
    @pulumi.getter(name="minPriorityPerJob")
    def min_priority_per_job(self) -> pulumi.Output[int]:
        """
        The minimum priority per job this user can use to submit jobs.
        """
        return pulumi.get(self, "min_priority_per_job")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="objectId")
    def object_id(self) -> pulumi.Output[str]:
        """
        The AAD object identifier for the entity to create a policy for.
        """
        return pulumi.get(self, "object_id")

    @property
    @pulumi.getter(name="objectType")
    def object_type(self) -> pulumi.Output[str]:
        """
        The type of AAD object the object identifier refers to.
        """
        return pulumi.get(self, "object_type")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

