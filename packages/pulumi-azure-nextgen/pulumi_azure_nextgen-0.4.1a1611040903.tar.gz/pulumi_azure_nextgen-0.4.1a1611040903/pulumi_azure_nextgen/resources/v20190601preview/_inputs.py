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
    'TemplateSpecTemplateArtifactArgs',
]

@pulumi.input_type
class TemplateSpecTemplateArtifactArgs:
    def __init__(__self__, *,
                 kind: pulumi.Input[str],
                 path: pulumi.Input[str],
                 template: Any):
        """
        Represents a Template Spec artifact containing an embedded Azure Resource Manager template.
        :param pulumi.Input[str] kind: The kind of artifact.
               Expected value is 'template'.
        :param pulumi.Input[str] path: A filesystem safe relative path of the artifact.
        :param Any template: The Azure Resource Manager template.
        """
        pulumi.set(__self__, "kind", 'template')
        pulumi.set(__self__, "path", path)
        pulumi.set(__self__, "template", template)

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Input[str]:
        """
        The kind of artifact.
        Expected value is 'template'.
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: pulumi.Input[str]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def path(self) -> pulumi.Input[str]:
        """
        A filesystem safe relative path of the artifact.
        """
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: pulumi.Input[str]):
        pulumi.set(self, "path", value)

    @property
    @pulumi.getter
    def template(self) -> Any:
        """
        The Azure Resource Manager template.
        """
        return pulumi.get(self, "template")

    @template.setter
    def template(self, value: Any):
        pulumi.set(self, "template", value)


