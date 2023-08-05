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
    'PrivateLinkScopedResourceResponse',
]

@pulumi.output_type
class PrivateLinkScopedResourceResponse(dict):
    """
    The private link scope resource reference.
    """
    def __init__(__self__, *,
                 resource_id: Optional[str] = None,
                 scope_id: Optional[str] = None):
        """
        The private link scope resource reference.
        :param str resource_id: The full resource Id of the private link scope resource.
        :param str scope_id: The private link scope unique Identifier.
        """
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)
        if scope_id is not None:
            pulumi.set(__self__, "scope_id", scope_id)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[str]:
        """
        The full resource Id of the private link scope resource.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="scopeId")
    def scope_id(self) -> Optional[str]:
        """
        The private link scope unique Identifier.
        """
        return pulumi.get(self, "scope_id")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


