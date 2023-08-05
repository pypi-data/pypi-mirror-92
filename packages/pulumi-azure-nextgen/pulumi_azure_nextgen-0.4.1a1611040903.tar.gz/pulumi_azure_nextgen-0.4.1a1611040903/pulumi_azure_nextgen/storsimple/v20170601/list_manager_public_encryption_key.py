# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables

__all__ = [
    'ListManagerPublicEncryptionKeyResult',
    'AwaitableListManagerPublicEncryptionKeyResult',
    'list_manager_public_encryption_key',
]

@pulumi.output_type
class ListManagerPublicEncryptionKeyResult:
    """
    Represents the secrets encrypted using Symmetric Encryption Key.
    """
    def __init__(__self__, encryption_algorithm=None, value=None, value_certificate_thumbprint=None):
        if encryption_algorithm and not isinstance(encryption_algorithm, str):
            raise TypeError("Expected argument 'encryption_algorithm' to be a str")
        pulumi.set(__self__, "encryption_algorithm", encryption_algorithm)
        if value and not isinstance(value, str):
            raise TypeError("Expected argument 'value' to be a str")
        pulumi.set(__self__, "value", value)
        if value_certificate_thumbprint and not isinstance(value_certificate_thumbprint, str):
            raise TypeError("Expected argument 'value_certificate_thumbprint' to be a str")
        pulumi.set(__self__, "value_certificate_thumbprint", value_certificate_thumbprint)

    @property
    @pulumi.getter(name="encryptionAlgorithm")
    def encryption_algorithm(self) -> str:
        """
        The algorithm used to encrypt the "Value".
        """
        return pulumi.get(self, "encryption_algorithm")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the secret itself. If the secret is in plaintext or null then EncryptionAlgorithm will be none.
        """
        return pulumi.get(self, "value")

    @property
    @pulumi.getter(name="valueCertificateThumbprint")
    def value_certificate_thumbprint(self) -> Optional[str]:
        """
        The thumbprint of the cert that was used to encrypt "Value".
        """
        return pulumi.get(self, "value_certificate_thumbprint")


class AwaitableListManagerPublicEncryptionKeyResult(ListManagerPublicEncryptionKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return ListManagerPublicEncryptionKeyResult(
            encryption_algorithm=self.encryption_algorithm,
            value=self.value,
            value_certificate_thumbprint=self.value_certificate_thumbprint)


def list_manager_public_encryption_key(manager_name: Optional[str] = None,
                                       resource_group_name: Optional[str] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableListManagerPublicEncryptionKeyResult:
    """
    Use this data source to access information about an existing resource.

    :param str manager_name: The manager name
    :param str resource_group_name: The resource group name
    """
    __args__ = dict()
    __args__['managerName'] = manager_name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-nextgen:storsimple/v20170601:listManagerPublicEncryptionKey', __args__, opts=opts, typ=ListManagerPublicEncryptionKeyResult).value

    return AwaitableListManagerPublicEncryptionKeyResult(
        encryption_algorithm=__ret__.encryption_algorithm,
        value=__ret__.value,
        value_certificate_thumbprint=__ret__.value_certificate_thumbprint)
