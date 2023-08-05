# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'StorageAccountPropertiesArgs',
]

@pulumi.input_type
class StorageAccountPropertiesArgs:
    def __init__(__self__, *,
                 access_key: pulumi.Input[str],
                 name: pulumi.Input[str]):
        """
        The properties of a storage account for a container registry.
        :param pulumi.Input[str] access_key: The access key to the storage account.
        :param pulumi.Input[str] name: The name of the storage account.
        """
        pulumi.set(__self__, "access_key", access_key)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="accessKey")
    def access_key(self) -> pulumi.Input[str]:
        """
        The access key to the storage account.
        """
        return pulumi.get(self, "access_key")

    @access_key.setter
    def access_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "access_key", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the storage account.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


