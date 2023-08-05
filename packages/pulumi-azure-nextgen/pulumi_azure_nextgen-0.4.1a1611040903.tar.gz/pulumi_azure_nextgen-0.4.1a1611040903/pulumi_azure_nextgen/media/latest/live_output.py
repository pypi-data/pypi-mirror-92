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

__all__ = ['LiveOutput']


class LiveOutput(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 archive_window_length: Optional[pulumi.Input[str]] = None,
                 asset_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 hls: Optional[pulumi.Input[pulumi.InputType['HlsArgs']]] = None,
                 live_event_name: Optional[pulumi.Input[str]] = None,
                 live_output_name: Optional[pulumi.Input[str]] = None,
                 manifest_name: Optional[pulumi.Input[str]] = None,
                 output_snap_time: Optional[pulumi.Input[float]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        The Live Output.
        Latest API Version: 2020-05-01.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The Media Services account name.
        :param pulumi.Input[str] archive_window_length: ISO 8601 time between 1 minute to 25 hours to indicate the maximum content length that can be archived in the asset for this live output. This also sets the maximum content length for the rewind window. For example, use PT1H30M to indicate 1 hour and 30 minutes of archive window.
        :param pulumi.Input[str] asset_name: The asset that the live output will write to.
        :param pulumi.Input[str] description: The description of the live output.
        :param pulumi.Input[pulumi.InputType['HlsArgs']] hls: HTTP Live Streaming (HLS) packing setting for the live output.
        :param pulumi.Input[str] live_event_name: The name of the live event, maximum length is 32.
        :param pulumi.Input[str] live_output_name: The name of the live output.
        :param pulumi.Input[str] manifest_name: The manifest file name. If not provided, the service will generate one automatically.
        :param pulumi.Input[float] output_snap_time: The initial timestamp that the live output will start at, any content before this value will not be archived.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the Azure subscription.
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
            if archive_window_length is None and not opts.urn:
                raise TypeError("Missing required property 'archive_window_length'")
            __props__['archive_window_length'] = archive_window_length
            if asset_name is None and not opts.urn:
                raise TypeError("Missing required property 'asset_name'")
            __props__['asset_name'] = asset_name
            __props__['description'] = description
            __props__['hls'] = hls
            if live_event_name is None and not opts.urn:
                raise TypeError("Missing required property 'live_event_name'")
            __props__['live_event_name'] = live_event_name
            if live_output_name is None and not opts.urn:
                raise TypeError("Missing required property 'live_output_name'")
            __props__['live_output_name'] = live_output_name
            __props__['manifest_name'] = manifest_name
            __props__['output_snap_time'] = output_snap_time
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['created'] = None
            __props__['last_modified'] = None
            __props__['name'] = None
            __props__['provisioning_state'] = None
            __props__['resource_state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:media/v20180330preview:LiveOutput"), pulumi.Alias(type_="azure-nextgen:media/v20180601preview:LiveOutput"), pulumi.Alias(type_="azure-nextgen:media/v20180701:LiveOutput"), pulumi.Alias(type_="azure-nextgen:media/v20190501preview:LiveOutput"), pulumi.Alias(type_="azure-nextgen:media/v20200501:LiveOutput")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(LiveOutput, __self__).__init__(
            'azure-nextgen:media/latest:LiveOutput',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'LiveOutput':
        """
        Get an existing LiveOutput resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return LiveOutput(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="archiveWindowLength")
    def archive_window_length(self) -> pulumi.Output[str]:
        """
        ISO 8601 time between 1 minute to 25 hours to indicate the maximum content length that can be archived in the asset for this live output. This also sets the maximum content length for the rewind window. For example, use PT1H30M to indicate 1 hour and 30 minutes of archive window.
        """
        return pulumi.get(self, "archive_window_length")

    @property
    @pulumi.getter(name="assetName")
    def asset_name(self) -> pulumi.Output[str]:
        """
        The asset that the live output will write to.
        """
        return pulumi.get(self, "asset_name")

    @property
    @pulumi.getter
    def created(self) -> pulumi.Output[str]:
        """
        The creation time the live output.
        """
        return pulumi.get(self, "created")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the live output.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def hls(self) -> pulumi.Output[Optional['outputs.HlsResponse']]:
        """
        HTTP Live Streaming (HLS) packing setting for the live output.
        """
        return pulumi.get(self, "hls")

    @property
    @pulumi.getter(name="lastModified")
    def last_modified(self) -> pulumi.Output[str]:
        """
        The time the live output was last modified.
        """
        return pulumi.get(self, "last_modified")

    @property
    @pulumi.getter(name="manifestName")
    def manifest_name(self) -> pulumi.Output[Optional[str]]:
        """
        The manifest file name. If not provided, the service will generate one automatically.
        """
        return pulumi.get(self, "manifest_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="outputSnapTime")
    def output_snap_time(self) -> pulumi.Output[Optional[float]]:
        """
        The initial timestamp that the live output will start at, any content before this value will not be archived.
        """
        return pulumi.get(self, "output_snap_time")

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> pulumi.Output[str]:
        """
        The provisioning state of the live output.
        """
        return pulumi.get(self, "provisioning_state")

    @property
    @pulumi.getter(name="resourceState")
    def resource_state(self) -> pulumi.Output[str]:
        """
        The resource state of the live output.
        """
        return pulumi.get(self, "resource_state")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource. E.g. "Microsoft.Compute/virtualMachines" or "Microsoft.Storage/storageAccounts"
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

