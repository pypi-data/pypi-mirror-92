# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = ['NotebookWorkspace']


class NotebookWorkspace(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 notebook_workspace_name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        A notebook workspace resource

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: Cosmos DB database account name.
        :param pulumi.Input[str] notebook_workspace_name: The name of the notebook workspace resource.
        :param pulumi.Input[str] resource_group_name: The name of the resource group. The name is case insensitive.
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
            if notebook_workspace_name is None and not opts.urn:
                raise TypeError("Missing required property 'notebook_workspace_name'")
            __props__['notebook_workspace_name'] = notebook_workspace_name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['name'] = None
            __props__['notebook_server_endpoint'] = None
            __props__['status'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:documentdb/latest:NotebookWorkspace"), pulumi.Alias(type_="azure-nextgen:documentdb/v20191212:NotebookWorkspace"), pulumi.Alias(type_="azure-nextgen:documentdb/v20200301:NotebookWorkspace"), pulumi.Alias(type_="azure-nextgen:documentdb/v20200401:NotebookWorkspace"), pulumi.Alias(type_="azure-nextgen:documentdb/v20200601preview:NotebookWorkspace"), pulumi.Alias(type_="azure-nextgen:documentdb/v20200901:NotebookWorkspace")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(NotebookWorkspace, __self__).__init__(
            'azure-nextgen:documentdb/v20190801:NotebookWorkspace',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'NotebookWorkspace':
        """
        Get an existing NotebookWorkspace resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return NotebookWorkspace(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the database account.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="notebookServerEndpoint")
    def notebook_server_endpoint(self) -> pulumi.Output[str]:
        """
        Specifies the endpoint of Notebook server.
        """
        return pulumi.get(self, "notebook_server_endpoint")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        Status of the notebook workspace. Possible values are: Creating, Online, Deleting, Failed, Updating.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of Azure resource.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

