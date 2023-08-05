# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['SavedSearch']


class SavedSearch(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 category: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 function_alias: Optional[pulumi.Input[str]] = None,
                 function_parameters: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 saved_search_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TagArgs']]]]] = None,
                 version: Optional[pulumi.Input[float]] = None,
                 workspace_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Value object for saved search results.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] category: The category of the saved search. This helps the user to find a saved search faster. 
        :param pulumi.Input[str] display_name: Saved search display name.
        :param pulumi.Input[str] etag: The ETag of the saved search.
        :param pulumi.Input[str] function_alias: The function alias if query serves as a function.
        :param pulumi.Input[str] function_parameters: The optional function parameters if query serves as a function. Value should be in the following format: 'param-name1:type1 = default_value1, param-name2:type2 = default_value2'. For more examples and proper syntax please refer to https://docs.microsoft.com/en-us/azure/kusto/query/functions/user-defined-functions.
        :param pulumi.Input[str] query: The query expression for the saved search.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
        :param pulumi.Input[str] saved_search_id: The id of the saved search.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['TagArgs']]]] tags: The tags attached to the saved search.
        :param pulumi.Input[float] version: The version number of the query language. The current version is 2 and is the default.
        :param pulumi.Input[str] workspace_name: The name of the workspace.
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

            if category is None and not opts.urn:
                raise TypeError("Missing required property 'category'")
            __props__['category'] = category
            if display_name is None and not opts.urn:
                raise TypeError("Missing required property 'display_name'")
            __props__['display_name'] = display_name
            __props__['etag'] = etag
            __props__['function_alias'] = function_alias
            __props__['function_parameters'] = function_parameters
            if query is None and not opts.urn:
                raise TypeError("Missing required property 'query'")
            __props__['query'] = query
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if saved_search_id is None and not opts.urn:
                raise TypeError("Missing required property 'saved_search_id'")
            __props__['saved_search_id'] = saved_search_id
            __props__['tags'] = tags
            __props__['version'] = version
            if workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'workspace_name'")
            __props__['workspace_name'] = workspace_name
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:operationalinsights/latest:SavedSearch"), pulumi.Alias(type_="azure-nextgen:operationalinsights/v20150320:SavedSearch"), pulumi.Alias(type_="azure-nextgen:operationalinsights/v20200801:SavedSearch")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(SavedSearch, __self__).__init__(
            'azure-nextgen:operationalinsights/v20200301preview:SavedSearch',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'SavedSearch':
        """
        Get an existing SavedSearch resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return SavedSearch(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def category(self) -> pulumi.Output[str]:
        """
        The category of the saved search. This helps the user to find a saved search faster. 
        """
        return pulumi.get(self, "category")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        Saved search display name.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[Optional[str]]:
        """
        The ETag of the saved search.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="functionAlias")
    def function_alias(self) -> pulumi.Output[Optional[str]]:
        """
        The function alias if query serves as a function.
        """
        return pulumi.get(self, "function_alias")

    @property
    @pulumi.getter(name="functionParameters")
    def function_parameters(self) -> pulumi.Output[Optional[str]]:
        """
        The optional function parameters if query serves as a function. Value should be in the following format: 'param-name1:type1 = default_value1, param-name2:type2 = default_value2'. For more examples and proper syntax please refer to https://docs.microsoft.com/en-us/azure/kusto/query/functions/user-defined-functions.
        """
        return pulumi.get(self, "function_parameters")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def query(self) -> pulumi.Output[str]:
        """
        The query expression for the saved search.
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.TagResponse']]]:
        """
        The tags attached to the saved search.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[Optional[float]]:
        """
        The version number of the query language. The current version is 2 and is the default.
        """
        return pulumi.get(self, "version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

