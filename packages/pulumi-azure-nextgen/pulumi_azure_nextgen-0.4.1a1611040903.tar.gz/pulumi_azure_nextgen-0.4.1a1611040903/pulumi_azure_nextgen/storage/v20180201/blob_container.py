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

__all__ = ['BlobContainer']


class BlobContainer(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 account_name: Optional[pulumi.Input[str]] = None,
                 container_name: Optional[pulumi.Input[str]] = None,
                 metadata: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 public_access: Optional[pulumi.Input['PublicAccess']] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Properties of the blob container, including Id, resource name, resource type, Etag.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] account_name: The name of the storage account within the specified resource group. Storage account names must be between 3 and 24 characters in length and use numbers and lower-case letters only.
        :param pulumi.Input[str] container_name: The name of the blob container within the specified storage account. Blob container names must be between 3 and 63 characters in length and use numbers, lower-case letters and dash (-) only. Every dash (-) character must be immediately preceded and followed by a letter or number.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] metadata: A name-value pair to associate with the container as metadata.
        :param pulumi.Input['PublicAccess'] public_access: Specifies whether data in the container may be accessed publicly and the level of access.
        :param pulumi.Input[str] resource_group_name: The name of the resource group within the user's subscription. The name is case insensitive.
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
            if container_name is None and not opts.urn:
                raise TypeError("Missing required property 'container_name'")
            __props__['container_name'] = container_name
            __props__['metadata'] = metadata
            __props__['public_access'] = public_access
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['etag'] = None
            __props__['has_immutability_policy'] = None
            __props__['has_legal_hold'] = None
            __props__['immutability_policy'] = None
            __props__['last_modified_time'] = None
            __props__['lease_duration'] = None
            __props__['lease_state'] = None
            __props__['lease_status'] = None
            __props__['legal_hold'] = None
            __props__['name'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:storage/latest:BlobContainer"), pulumi.Alias(type_="azure-nextgen:storage/v20180301preview:BlobContainer"), pulumi.Alias(type_="azure-nextgen:storage/v20180701:BlobContainer"), pulumi.Alias(type_="azure-nextgen:storage/v20181101:BlobContainer"), pulumi.Alias(type_="azure-nextgen:storage/v20190401:BlobContainer"), pulumi.Alias(type_="azure-nextgen:storage/v20190601:BlobContainer"), pulumi.Alias(type_="azure-nextgen:storage/v20200801preview:BlobContainer")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(BlobContainer, __self__).__init__(
            'azure-nextgen:storage/v20180201:BlobContainer',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'BlobContainer':
        """
        Get an existing BlobContainer resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return BlobContainer(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        Resource Etag.
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter(name="hasImmutabilityPolicy")
    def has_immutability_policy(self) -> pulumi.Output[bool]:
        """
        The hasImmutabilityPolicy public property is set to true by SRP if ImmutabilityPolicy has been created for this container. The hasImmutabilityPolicy public property is set to false by SRP if ImmutabilityPolicy has not been created for this container.
        """
        return pulumi.get(self, "has_immutability_policy")

    @property
    @pulumi.getter(name="hasLegalHold")
    def has_legal_hold(self) -> pulumi.Output[bool]:
        """
        The hasLegalHold public property is set to true by SRP if there are at least one existing tag. The hasLegalHold public property is set to false by SRP if all existing legal hold tags are cleared out. There can be a maximum of 1000 blob containers with hasLegalHold=true for a given account.
        """
        return pulumi.get(self, "has_legal_hold")

    @property
    @pulumi.getter(name="immutabilityPolicy")
    def immutability_policy(self) -> pulumi.Output['outputs.ImmutabilityPolicyPropertiesResponse']:
        """
        The ImmutabilityPolicy property of the container.
        """
        return pulumi.get(self, "immutability_policy")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[str]:
        """
        Returns the date and time the container was last modified.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter(name="leaseDuration")
    def lease_duration(self) -> pulumi.Output[str]:
        """
        Specifies whether the lease on a container is of infinite or fixed duration, only when the container is leased.
        """
        return pulumi.get(self, "lease_duration")

    @property
    @pulumi.getter(name="leaseState")
    def lease_state(self) -> pulumi.Output[str]:
        """
        Lease state of the container.
        """
        return pulumi.get(self, "lease_state")

    @property
    @pulumi.getter(name="leaseStatus")
    def lease_status(self) -> pulumi.Output[str]:
        """
        The lease status of the container.
        """
        return pulumi.get(self, "lease_status")

    @property
    @pulumi.getter(name="legalHold")
    def legal_hold(self) -> pulumi.Output['outputs.LegalHoldPropertiesResponse']:
        """
        The LegalHold property of the container.
        """
        return pulumi.get(self, "legal_hold")

    @property
    @pulumi.getter
    def metadata(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A name-value pair to associate with the container as metadata.
        """
        return pulumi.get(self, "metadata")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="publicAccess")
    def public_access(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies whether data in the container may be accessed publicly and the level of access.
        """
        return pulumi.get(self, "public_access")

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

