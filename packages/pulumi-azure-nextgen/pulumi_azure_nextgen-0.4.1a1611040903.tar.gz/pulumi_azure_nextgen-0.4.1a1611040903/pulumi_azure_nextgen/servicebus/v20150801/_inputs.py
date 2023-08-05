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
    'SkuArgs',
]

@pulumi.input_type
class SkuArgs:
    def __init__(__self__, *,
                 tier: pulumi.Input[Union[str, 'SkuTier']],
                 capacity: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[Union[str, 'SkuName']]] = None):
        """
        SKU of the namespace.
        :param pulumi.Input[Union[str, 'SkuTier']] tier: The billing tier of this particular SKU.
        :param pulumi.Input[int] capacity: The specified messaging units for the tier.
        :param pulumi.Input[Union[str, 'SkuName']] name: Name of this SKU.
        """
        pulumi.set(__self__, "tier", tier)
        if capacity is not None:
            pulumi.set(__self__, "capacity", capacity)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def tier(self) -> pulumi.Input[Union[str, 'SkuTier']]:
        """
        The billing tier of this particular SKU.
        """
        return pulumi.get(self, "tier")

    @tier.setter
    def tier(self, value: pulumi.Input[Union[str, 'SkuTier']]):
        pulumi.set(self, "tier", value)

    @property
    @pulumi.getter
    def capacity(self) -> Optional[pulumi.Input[int]]:
        """
        The specified messaging units for the tier.
        """
        return pulumi.get(self, "capacity")

    @capacity.setter
    def capacity(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "capacity", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[Union[str, 'SkuName']]]:
        """
        Name of this SKU.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[Union[str, 'SkuName']]]):
        pulumi.set(self, "name", value)


