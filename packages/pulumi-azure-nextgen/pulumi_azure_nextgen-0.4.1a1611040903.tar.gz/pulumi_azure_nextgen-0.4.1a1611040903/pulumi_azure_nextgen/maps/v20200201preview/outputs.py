# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'CreatorPropertiesResponse',
    'MapsAccountPropertiesResponse',
    'PrivateAtlasPropertiesResponse',
    'SkuResponse',
    'SystemDataResponse',
]

@pulumi.output_type
class CreatorPropertiesResponse(dict):
    """
    Creator resource properties
    """
    def __init__(__self__, *,
                 provisioning_state: Optional[str] = None):
        """
        Creator resource properties
        :param str provisioning_state: The state of the resource provisioning, terminal states: Succeeded, Failed, Canceled
        """
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        The state of the resource provisioning, terminal states: Succeeded, Failed, Canceled
        """
        return pulumi.get(self, "provisioning_state")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


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
class PrivateAtlasPropertiesResponse(dict):
    """
    Private Atlas resource properties
    """
    def __init__(__self__, *,
                 provisioning_state: Optional[str] = None):
        """
        Private Atlas resource properties
        :param str provisioning_state: The state of the resource provisioning, terminal states: Succeeded, Failed, Canceled
        """
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[str]:
        """
        The state of the resource provisioning, terminal states: Succeeded, Failed, Canceled
        """
        return pulumi.get(self, "provisioning_state")

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


@pulumi.output_type
class SystemDataResponse(dict):
    """
    Metadata pertaining to creation and last modification of the resource.
    """
    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 created_by: Optional[str] = None,
                 created_by_type: Optional[str] = None,
                 last_modified_at: Optional[str] = None,
                 last_modified_by: Optional[str] = None,
                 last_modified_by_type: Optional[str] = None):
        """
        Metadata pertaining to creation and last modification of the resource.
        :param str created_at: The timestamp of resource creation (UTC).
        :param str created_by: The identity that created the resource.
        :param str created_by_type: The type of identity that created the resource.
        :param str last_modified_at: The type of identity that last modified the resource.
        :param str last_modified_by: The identity that last modified the resource.
        :param str last_modified_by_type: The type of identity that last modified the resource.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if created_by is not None:
            pulumi.set(__self__, "created_by", created_by)
        if created_by_type is not None:
            pulumi.set(__self__, "created_by_type", created_by_type)
        if last_modified_at is not None:
            pulumi.set(__self__, "last_modified_at", last_modified_at)
        if last_modified_by is not None:
            pulumi.set(__self__, "last_modified_by", last_modified_by)
        if last_modified_by_type is not None:
            pulumi.set(__self__, "last_modified_by_type", last_modified_by_type)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The timestamp of resource creation (UTC).
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> Optional[str]:
        """
        The identity that created the resource.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter(name="createdByType")
    def created_by_type(self) -> Optional[str]:
        """
        The type of identity that created the resource.
        """
        return pulumi.get(self, "created_by_type")

    @property
    @pulumi.getter(name="lastModifiedAt")
    def last_modified_at(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_at")

    @property
    @pulumi.getter(name="lastModifiedBy")
    def last_modified_by(self) -> Optional[str]:
        """
        The identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by")

    @property
    @pulumi.getter(name="lastModifiedByType")
    def last_modified_by_type(self) -> Optional[str]:
        """
        The type of identity that last modified the resource.
        """
        return pulumi.get(self, "last_modified_by_type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


