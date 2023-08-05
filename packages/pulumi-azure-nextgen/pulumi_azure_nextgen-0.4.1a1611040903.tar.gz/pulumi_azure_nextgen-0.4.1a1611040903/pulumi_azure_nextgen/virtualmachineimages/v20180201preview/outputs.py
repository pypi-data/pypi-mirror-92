# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'ImageTemplateIsoSourceResponse',
    'ImageTemplateLastRunStatusResponse',
    'ImageTemplateManagedImageDistributorResponse',
    'ImageTemplatePlatformImageSourceResponse',
    'ImageTemplateSharedImageDistributorResponse',
    'ImageTemplateShellCustomizerResponse',
    'ProvisioningErrorResponse',
]

@pulumi.output_type
class ImageTemplateIsoSourceResponse(dict):
    """
    Describes an image source that is an installation ISO. Currently only supports Red Hat Enterprise Linux 7.2-7.5 ISO's.
    """
    def __init__(__self__, *,
                 sha256_checksum: str,
                 source_uri: str,
                 type: str):
        """
        Describes an image source that is an installation ISO. Currently only supports Red Hat Enterprise Linux 7.2-7.5 ISO's.
        :param str sha256_checksum: SHA256 Checksum of the ISO image.
        :param str source_uri: URL to get the ISO image. This URL has to be accessible to the resource provider at the time of the imageTemplate creation.
        :param str type: Specifies the type of source image you want to start with.
               Expected value is 'ISO'.
        """
        pulumi.set(__self__, "sha256_checksum", sha256_checksum)
        pulumi.set(__self__, "source_uri", source_uri)
        pulumi.set(__self__, "type", 'ISO')

    @property
    @pulumi.getter(name="sha256Checksum")
    def sha256_checksum(self) -> str:
        """
        SHA256 Checksum of the ISO image.
        """
        return pulumi.get(self, "sha256_checksum")

    @property
    @pulumi.getter(name="sourceURI")
    def source_uri(self) -> str:
        """
        URL to get the ISO image. This URL has to be accessible to the resource provider at the time of the imageTemplate creation.
        """
        return pulumi.get(self, "source_uri")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the type of source image you want to start with.
        Expected value is 'ISO'.
        """
        return pulumi.get(self, "type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ImageTemplateLastRunStatusResponse(dict):
    def __init__(__self__, *,
                 end_time: Optional[str] = None,
                 message: Optional[str] = None,
                 run_state: Optional[str] = None,
                 run_sub_state: Optional[str] = None,
                 start_time: Optional[str] = None):
        """
        :param str end_time: End time of the last run (UTC)
        :param str message: Verbose information about the last run state
        :param str run_state: State of the last run
        :param str run_sub_state: Sub state of the last run
        :param str start_time: Start time of the last run (UTC)
        """
        if end_time is not None:
            pulumi.set(__self__, "end_time", end_time)
        if message is not None:
            pulumi.set(__self__, "message", message)
        if run_state is not None:
            pulumi.set(__self__, "run_state", run_state)
        if run_sub_state is not None:
            pulumi.set(__self__, "run_sub_state", run_sub_state)
        if start_time is not None:
            pulumi.set(__self__, "start_time", start_time)

    @property
    @pulumi.getter(name="endTime")
    def end_time(self) -> Optional[str]:
        """
        End time of the last run (UTC)
        """
        return pulumi.get(self, "end_time")

    @property
    @pulumi.getter
    def message(self) -> Optional[str]:
        """
        Verbose information about the last run state
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter(name="runState")
    def run_state(self) -> Optional[str]:
        """
        State of the last run
        """
        return pulumi.get(self, "run_state")

    @property
    @pulumi.getter(name="runSubState")
    def run_sub_state(self) -> Optional[str]:
        """
        Sub state of the last run
        """
        return pulumi.get(self, "run_sub_state")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> Optional[str]:
        """
        Start time of the last run (UTC)
        """
        return pulumi.get(self, "start_time")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ImageTemplateManagedImageDistributorResponse(dict):
    """
    Distribute as a Managed Disk Image.
    """
    def __init__(__self__, *,
                 image_id: str,
                 location: str,
                 run_output_name: str,
                 type: str,
                 artifact_tags: Optional[Mapping[str, str]] = None):
        """
        Distribute as a Managed Disk Image.
        :param str image_id: Resource Id of the Managed Disk Image
        :param str location: Azure location for the image, should match if image already exists
        :param str run_output_name: The name to be used for the associated RunOutput.
        :param str type: Type of distribution.
               Expected value is 'managedImage'.
        :param Mapping[str, str] artifact_tags: Tags that will be applied to the artifact once it has been created/updated by the distributor.
        """
        pulumi.set(__self__, "image_id", image_id)
        pulumi.set(__self__, "location", location)
        pulumi.set(__self__, "run_output_name", run_output_name)
        pulumi.set(__self__, "type", 'managedImage')
        if artifact_tags is not None:
            pulumi.set(__self__, "artifact_tags", artifact_tags)

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> str:
        """
        Resource Id of the Managed Disk Image
        """
        return pulumi.get(self, "image_id")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        Azure location for the image, should match if image already exists
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="runOutputName")
    def run_output_name(self) -> str:
        """
        The name to be used for the associated RunOutput.
        """
        return pulumi.get(self, "run_output_name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of distribution.
        Expected value is 'managedImage'.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="artifactTags")
    def artifact_tags(self) -> Optional[Mapping[str, str]]:
        """
        Tags that will be applied to the artifact once it has been created/updated by the distributor.
        """
        return pulumi.get(self, "artifact_tags")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ImageTemplatePlatformImageSourceResponse(dict):
    """
    Describes an image source from [Azure Gallery Images](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachineimages).
    """
    def __init__(__self__, *,
                 type: str,
                 offer: Optional[str] = None,
                 publisher: Optional[str] = None,
                 sku: Optional[str] = None,
                 version: Optional[str] = None):
        """
        Describes an image source from [Azure Gallery Images](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachineimages).
        :param str type: Specifies the type of source image you want to start with.
               Expected value is 'PlatformImage'.
        :param str offer: Image offer from the [Azure Gallery Images](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachineimages).
        :param str publisher: Image Publisher in [Azure Gallery Images](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachineimages).
        :param str sku: Image sku from the [Azure Gallery Images](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachineimages).
        :param str version: Image version from the [Azure Gallery Images](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachineimages).
        """
        pulumi.set(__self__, "type", 'PlatformImage')
        if offer is not None:
            pulumi.set(__self__, "offer", offer)
        if publisher is not None:
            pulumi.set(__self__, "publisher", publisher)
        if sku is not None:
            pulumi.set(__self__, "sku", sku)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Specifies the type of source image you want to start with.
        Expected value is 'PlatformImage'.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def offer(self) -> Optional[str]:
        """
        Image offer from the [Azure Gallery Images](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachineimages).
        """
        return pulumi.get(self, "offer")

    @property
    @pulumi.getter
    def publisher(self) -> Optional[str]:
        """
        Image Publisher in [Azure Gallery Images](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachineimages).
        """
        return pulumi.get(self, "publisher")

    @property
    @pulumi.getter
    def sku(self) -> Optional[str]:
        """
        Image sku from the [Azure Gallery Images](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachineimages).
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def version(self) -> Optional[str]:
        """
        Image version from the [Azure Gallery Images](https://docs.microsoft.com/en-us/rest/api/compute/virtualmachineimages).
        """
        return pulumi.get(self, "version")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ImageTemplateSharedImageDistributorResponse(dict):
    """
    Distribute via Shared Image Gallery.
    """
    def __init__(__self__, *,
                 gallery_image_id: str,
                 replication_regions: Sequence[str],
                 run_output_name: str,
                 type: str,
                 artifact_tags: Optional[Mapping[str, str]] = None):
        """
        Distribute via Shared Image Gallery.
        :param str gallery_image_id: Resource Id of the Shared Image Gallery image
        :param str run_output_name: The name to be used for the associated RunOutput.
        :param str type: Type of distribution.
               Expected value is 'sharedImage'.
        :param Mapping[str, str] artifact_tags: Tags that will be applied to the artifact once it has been created/updated by the distributor.
        """
        pulumi.set(__self__, "gallery_image_id", gallery_image_id)
        pulumi.set(__self__, "replication_regions", replication_regions)
        pulumi.set(__self__, "run_output_name", run_output_name)
        pulumi.set(__self__, "type", 'sharedImage')
        if artifact_tags is not None:
            pulumi.set(__self__, "artifact_tags", artifact_tags)

    @property
    @pulumi.getter(name="galleryImageId")
    def gallery_image_id(self) -> str:
        """
        Resource Id of the Shared Image Gallery image
        """
        return pulumi.get(self, "gallery_image_id")

    @property
    @pulumi.getter(name="replicationRegions")
    def replication_regions(self) -> Sequence[str]:
        return pulumi.get(self, "replication_regions")

    @property
    @pulumi.getter(name="runOutputName")
    def run_output_name(self) -> str:
        """
        The name to be used for the associated RunOutput.
        """
        return pulumi.get(self, "run_output_name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        Type of distribution.
        Expected value is 'sharedImage'.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="artifactTags")
    def artifact_tags(self) -> Optional[Mapping[str, str]]:
        """
        Tags that will be applied to the artifact once it has been created/updated by the distributor.
        """
        return pulumi.get(self, "artifact_tags")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ImageTemplateShellCustomizerResponse(dict):
    """
    Runs a shell script during the customization phase
    """
    def __init__(__self__, *,
                 type: str,
                 name: Optional[str] = None,
                 script: Optional[str] = None):
        """
        Runs a shell script during the customization phase
        :param str type: The type of customization tool you want to use on the Image. For example, "shell" can be shellCustomizer
               Expected value is 'shell'.
        :param str name: Friendly Name to provide context on what this customization step does
        :param str script: The shell script to be run for customizing. It can be a github link, SAS URI for Azure Storage, etc
        """
        pulumi.set(__self__, "type", 'shell')
        if name is not None:
            pulumi.set(__self__, "name", name)
        if script is not None:
            pulumi.set(__self__, "script", script)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of customization tool you want to use on the Image. For example, "shell" can be shellCustomizer
        Expected value is 'shell'.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        Friendly Name to provide context on what this customization step does
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def script(self) -> Optional[str]:
        """
        The shell script to be run for customizing. It can be a github link, SAS URI for Azure Storage, etc
        """
        return pulumi.get(self, "script")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class ProvisioningErrorResponse(dict):
    def __init__(__self__, *,
                 message: Optional[str] = None,
                 provisioning_error_code: Optional[str] = None):
        """
        :param str message: Verbose error message about the provisioning failure
        :param str provisioning_error_code: Error code of the provisioning failure
        """
        if message is not None:
            pulumi.set(__self__, "message", message)
        if provisioning_error_code is not None:
            pulumi.set(__self__, "provisioning_error_code", provisioning_error_code)

    @property
    @pulumi.getter
    def message(self) -> Optional[str]:
        """
        Verbose error message about the provisioning failure
        """
        return pulumi.get(self, "message")

    @property
    @pulumi.getter(name="provisioningErrorCode")
    def provisioning_error_code(self) -> Optional[str]:
        """
        Error code of the provisioning failure
        """
        return pulumi.get(self, "provisioning_error_code")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


