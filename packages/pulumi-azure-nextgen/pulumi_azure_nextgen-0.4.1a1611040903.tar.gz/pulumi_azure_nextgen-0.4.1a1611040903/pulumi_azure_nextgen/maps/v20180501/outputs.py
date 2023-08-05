# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'MapsAccountPropertiesResponse',
    'SkuResponse',
]

@pulumi.output_type
class MapsAccountPropertiesResponse(dict):
    """
    Additional Map account properties
    """
    def __init__(__self__, *,
                 x_ms_client_id: Optional[str] = None):
        """
        Additional Map account properties
        :param str x_ms_client_id: A unique identifier for the maps account
        """
        if x_ms_client_id is not None:
            pulumi.set(__self__, "x_ms_client_id", x_ms_client_id)

    @property
    @pulumi.getter(name="xMsClientId")
    def x_ms_client_id(self) -> Optional[str]:
        """
        A unique identifier for the maps account
        """
        return pulumi.get(self, "x_ms_client_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class SkuResponse(dict):
    """
    The SKU of the Maps Account.
    """
    def __init__(__self__, *,
                 name: str,
                 tier: str):
        """
        The SKU of the Maps Account.
        :param str name: The name of the SKU, in standard format (such as S0).
        :param str tier: Gets the sku tier. This is based on the SKU name.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "tier", tier)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the SKU, in standard format (such as S0).
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tier(self) -> str:
        """
        Gets the sku tier. This is based on the SKU name.
        """
        return pulumi.get(self, "tier")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


