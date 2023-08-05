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
    'AppServiceCertificateArgs',
    'CertificateDetailsArgs',
    'CertificateOrderCertificateArgs',
]

@pulumi.input_type
class AppServiceCertificateArgs:
    def __init__(__self__, *,
                 key_vault_id: Optional[pulumi.Input[str]] = None,
                 key_vault_secret_name: Optional[pulumi.Input[str]] = None):
        """
        Key Vault container for a certificate that is purchased through Azure.
        :param pulumi.Input[str] key_vault_id: Key Vault resource Id.
        :param pulumi.Input[str] key_vault_secret_name: Key Vault secret name.
        """
        if key_vault_id is not None:
            pulumi.set(__self__, "key_vault_id", key_vault_id)
        if key_vault_secret_name is not None:
            pulumi.set(__self__, "key_vault_secret_name", key_vault_secret_name)

    @property
    @pulumi.getter(name="keyVaultId")
    def key_vault_id(self) -> Optional[pulumi.Input[str]]:
        """
        Key Vault resource Id.
        """
        return pulumi.get(self, "key_vault_id")

    @key_vault_id.setter
    def key_vault_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_id", value)

    @property
    @pulumi.getter(name="keyVaultSecretName")
    def key_vault_secret_name(self) -> Optional[pulumi.Input[str]]:
        """
        Key Vault secret name.
        """
        return pulumi.get(self, "key_vault_secret_name")

    @key_vault_secret_name.setter
    def key_vault_secret_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_secret_name", value)


@pulumi.input_type
class CertificateDetailsArgs:
    def __init__(__self__, *,
                 location: pulumi.Input[str],
                 id: Optional[pulumi.Input[str]] = None,
                 issuer: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 not_after: Optional[pulumi.Input[str]] = None,
                 not_before: Optional[pulumi.Input[str]] = None,
                 raw_data: Optional[pulumi.Input[str]] = None,
                 serial_number: Optional[pulumi.Input[str]] = None,
                 signature_algorithm: Optional[pulumi.Input[str]] = None,
                 subject: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 thumbprint: Optional[pulumi.Input[str]] = None,
                 type: Optional[pulumi.Input[str]] = None,
                 version: Optional[pulumi.Input[int]] = None):
        """
        Certificate Details
        :param pulumi.Input[str] location: Resource Location
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[str] issuer: Issuer
        :param pulumi.Input[str] kind: Kind of resource
        :param pulumi.Input[str] name: Resource Name
        :param pulumi.Input[str] not_after: Valid to
        :param pulumi.Input[str] not_before: Valid from
        :param pulumi.Input[str] raw_data: Raw certificate data
        :param pulumi.Input[str] serial_number: Serial Number
        :param pulumi.Input[str] signature_algorithm: Signature Algorithm
        :param pulumi.Input[str] subject: Subject
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] thumbprint: Thumbprint
        :param pulumi.Input[str] type: Resource type
        :param pulumi.Input[int] version: Version
        """
        pulumi.set(__self__, "location", location)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if issuer is not None:
            pulumi.set(__self__, "issuer", issuer)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if not_after is not None:
            pulumi.set(__self__, "not_after", not_after)
        if not_before is not None:
            pulumi.set(__self__, "not_before", not_before)
        if raw_data is not None:
            pulumi.set(__self__, "raw_data", raw_data)
        if serial_number is not None:
            pulumi.set(__self__, "serial_number", serial_number)
        if signature_algorithm is not None:
            pulumi.set(__self__, "signature_algorithm", signature_algorithm)
        if subject is not None:
            pulumi.set(__self__, "subject", subject)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if thumbprint is not None:
            pulumi.set(__self__, "thumbprint", thumbprint)
        if type is not None:
            pulumi.set(__self__, "type", type)
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def issuer(self) -> Optional[pulumi.Input[str]]:
        """
        Issuer
        """
        return pulumi.get(self, "issuer")

    @issuer.setter
    def issuer(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "issuer", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="notAfter")
    def not_after(self) -> Optional[pulumi.Input[str]]:
        """
        Valid to
        """
        return pulumi.get(self, "not_after")

    @not_after.setter
    def not_after(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "not_after", value)

    @property
    @pulumi.getter(name="notBefore")
    def not_before(self) -> Optional[pulumi.Input[str]]:
        """
        Valid from
        """
        return pulumi.get(self, "not_before")

    @not_before.setter
    def not_before(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "not_before", value)

    @property
    @pulumi.getter(name="rawData")
    def raw_data(self) -> Optional[pulumi.Input[str]]:
        """
        Raw certificate data
        """
        return pulumi.get(self, "raw_data")

    @raw_data.setter
    def raw_data(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "raw_data", value)

    @property
    @pulumi.getter(name="serialNumber")
    def serial_number(self) -> Optional[pulumi.Input[str]]:
        """
        Serial Number
        """
        return pulumi.get(self, "serial_number")

    @serial_number.setter
    def serial_number(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "serial_number", value)

    @property
    @pulumi.getter(name="signatureAlgorithm")
    def signature_algorithm(self) -> Optional[pulumi.Input[str]]:
        """
        Signature Algorithm
        """
        return pulumi.get(self, "signature_algorithm")

    @signature_algorithm.setter
    def signature_algorithm(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "signature_algorithm", value)

    @property
    @pulumi.getter
    def subject(self) -> Optional[pulumi.Input[str]]:
        """
        Subject
        """
        return pulumi.get(self, "subject")

    @subject.setter
    def subject(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subject", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def thumbprint(self) -> Optional[pulumi.Input[str]]:
        """
        Thumbprint
        """
        return pulumi.get(self, "thumbprint")

    @thumbprint.setter
    def thumbprint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "thumbprint", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[int]]:
        """
        Version
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class CertificateOrderCertificateArgs:
    def __init__(__self__, *,
                 location: pulumi.Input[str],
                 id: Optional[pulumi.Input[str]] = None,
                 key_vault_id: Optional[pulumi.Input[str]] = None,
                 key_vault_secret_name: Optional[pulumi.Input[str]] = None,
                 kind: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 provisioning_state: Optional[pulumi.Input['KeyVaultSecretStatus']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        Class representing the Key Vault container for certificate purchased through Azure
        :param pulumi.Input[str] location: Resource Location
        :param pulumi.Input[str] id: Resource Id
        :param pulumi.Input[str] key_vault_id: Key Vault Csm resource Id
        :param pulumi.Input[str] key_vault_secret_name: Key Vault secret name
        :param pulumi.Input[str] kind: Kind of resource
        :param pulumi.Input[str] name: Resource Name
        :param pulumi.Input['KeyVaultSecretStatus'] provisioning_state: Status of the Key Vault secret
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags
        :param pulumi.Input[str] type: Resource type
        """
        pulumi.set(__self__, "location", location)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if key_vault_id is not None:
            pulumi.set(__self__, "key_vault_id", key_vault_id)
        if key_vault_secret_name is not None:
            pulumi.set(__self__, "key_vault_secret_name", key_vault_secret_name)
        if kind is not None:
            pulumi.set(__self__, "kind", kind)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if provisioning_state is not None:
            pulumi.set(__self__, "provisioning_state", provisioning_state)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def location(self) -> pulumi.Input[str]:
        """
        Resource Location
        """
        return pulumi.get(self, "location")

    @location.setter
    def location(self, value: pulumi.Input[str]):
        pulumi.set(self, "location", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Id
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="keyVaultId")
    def key_vault_id(self) -> Optional[pulumi.Input[str]]:
        """
        Key Vault Csm resource Id
        """
        return pulumi.get(self, "key_vault_id")

    @key_vault_id.setter
    def key_vault_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_id", value)

    @property
    @pulumi.getter(name="keyVaultSecretName")
    def key_vault_secret_name(self) -> Optional[pulumi.Input[str]]:
        """
        Key Vault secret name
        """
        return pulumi.get(self, "key_vault_secret_name")

    @key_vault_secret_name.setter
    def key_vault_secret_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_vault_secret_name", value)

    @property
    @pulumi.getter
    def kind(self) -> Optional[pulumi.Input[str]]:
        """
        Kind of resource
        """
        return pulumi.get(self, "kind")

    @kind.setter
    def kind(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kind", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Resource Name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="provisioningState")
    def provisioning_state(self) -> Optional[pulumi.Input['KeyVaultSecretStatus']]:
        """
        Status of the Key Vault secret
        """
        return pulumi.get(self, "provisioning_state")

    @provisioning_state.setter
    def provisioning_state(self, value: Optional[pulumi.Input['KeyVaultSecretStatus']]):
        pulumi.set(self, "provisioning_state", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Resource tags
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        Resource type
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


