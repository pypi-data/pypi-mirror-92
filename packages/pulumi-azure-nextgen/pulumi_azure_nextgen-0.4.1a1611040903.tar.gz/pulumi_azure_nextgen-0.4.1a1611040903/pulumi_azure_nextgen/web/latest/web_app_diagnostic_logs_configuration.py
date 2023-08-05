# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['WebAppDiagnosticLogsConfiguration']


class WebAppDiagnosticLogsConfiguration(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_logs: Optional[pulumi.Input[pulumi.InputType['ApplicationLogsConfigArgs']]] = None,
                 detailed_error_messages: Optional[pulumi.Input[pulumi.InputType['EnabledConfigArgs']]] = None,
                 failed_requests_tracing: Optional[pulumi.Input[pulumi.InputType['EnabledConfigArgs']]] = None,
                 http_logs: Optional[pulumi.Input[pulumi.InputType['HttpLogsConfigArgs']]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Configuration of App Service site logs.
        Latest API Version: 2020-09-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ApplicationLogsConfigArgs']] application_logs: Application logs configuration.
        :param pulumi.Input[pulumi.InputType['EnabledConfigArgs']] detailed_error_messages: Detailed error messages configuration.
        :param pulumi.Input[pulumi.InputType['EnabledConfigArgs']] failed_requests_tracing: Failed requests tracing configuration.
        :param pulumi.Input[pulumi.InputType['HttpLogsConfigArgs']] http_logs: HTTP logs configuration.
        :param pulumi.Input[str] kind: Kind of resource.
        :param pulumi.Input[str] name: Name of the app.
        :param pulumi.Input[str] resource_group_name: Name of the resource group to which the resource belongs.
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

            __props__['application_logs'] = application_logs
            __props__['detailed_error_messages'] = detailed_error_messages
            __props__['failed_requests_tracing'] = failed_requests_tracing
            __props__['http_logs'] = http_logs
            __props__['kind'] = kind
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['system_data'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:web/v20150801:WebAppDiagnosticLogsConfiguration"), pulumi.Alias(type_="azure-nextgen:web/v20160801:WebAppDiagnosticLogsConfiguration"), pulumi.Alias(type_="azure-nextgen:web/v20180201:WebAppDiagnosticLogsConfiguration"), pulumi.Alias(type_="azure-nextgen:web/v20181101:WebAppDiagnosticLogsConfiguration"), pulumi.Alias(type_="azure-nextgen:web/v20190801:WebAppDiagnosticLogsConfiguration"), pulumi.Alias(type_="azure-nextgen:web/v20200601:WebAppDiagnosticLogsConfiguration"), pulumi.Alias(type_="azure-nextgen:web/v20200901:WebAppDiagnosticLogsConfiguration")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(WebAppDiagnosticLogsConfiguration, __self__).__init__(
            'azure-nextgen:web/latest:WebAppDiagnosticLogsConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'WebAppDiagnosticLogsConfiguration':
        """
        Get an existing WebAppDiagnosticLogsConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return WebAppDiagnosticLogsConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationLogs")
    def application_logs(self) -> pulumi.Output[Optional['outputs.ApplicationLogsConfigResponse']]:
        """
        Application logs configuration.
        """
        return pulumi.get(self, "application_logs")

    @property
    @pulumi.getter(name="detailedErrorMessages")
    def detailed_error_messages(self) -> pulumi.Output[Optional['outputs.EnabledConfigResponse']]:
        """
        Detailed error messages configuration.
        """
        return pulumi.get(self, "detailed_error_messages")

    @property
    @pulumi.getter(name="failedRequestsTracing")
    def failed_requests_tracing(self) -> pulumi.Output[Optional['outputs.EnabledConfigResponse']]:
        """
        Failed requests tracing configuration.
        """
        return pulumi.get(self, "failed_requests_tracing")

    @property
    @pulumi.getter(name="httpLogs")
    def http_logs(self) -> pulumi.Output[Optional['outputs.HttpLogsConfigResponse']]:
        """
        HTTP logs configuration.
        """
        return pulumi.get(self, "http_logs")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[Optional[str]]:
        """
        Kind of resource.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource Name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="systemData")
    def system_data(self) -> pulumi.Output['outputs.SystemDataResponse']:
        """
        The system metadata relating to this resource.
        """
        return pulumi.get(self, "system_data")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

