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
    'OrganizationResourcePropertiesResponseOfferDetail',
    'OrganizationResourcePropertiesResponseUserDetail',
]

@pulumi.output_type
class OrganizationResourcePropertiesResponseOfferDetail(dict):
    """
    Confluent offer detail
    """
    def __init__(__self__, *,
                 id: Optional[str] = None,
                 plan_id: Optional[str] = None,
                 plan_name: Optional[str] = None,
                 publisher_id: Optional[str] = None,
                 status: Optional[str] = None,
                 term_unit: Optional[str] = None):
        """
        Confluent offer detail
        :param str id: Offer Id
        :param str plan_id: Offer Plan Id
        :param str plan_name: Offer Plan Name
        :param str publisher_id: Publisher Id
        :param str status: SaaS Offer Status
        :param str term_unit: Offer Plan Term unit
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if plan_id is not None:
            pulumi.set(__self__, "plan_id", plan_id)
        if plan_name is not None:
            pulumi.set(__self__, "plan_name", plan_name)
        if publisher_id is not None:
            pulumi.set(__self__, "publisher_id", publisher_id)
        if status is not None:
            pulumi.set(__self__, "status", status)
        if term_unit is not None:
            pulumi.set(__self__, "term_unit", term_unit)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        Offer Id
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="planId")
    def plan_id(self) -> Optional[str]:
        """
        Offer Plan Id
        """
        return pulumi.get(self, "plan_id")

    @property
    @pulumi.getter(name="planName")
    def plan_name(self) -> Optional[str]:
        """
        Offer Plan Name
        """
        return pulumi.get(self, "plan_name")

    @property
    @pulumi.getter(name="publisherId")
    def publisher_id(self) -> Optional[str]:
        """
        Publisher Id
        """
        return pulumi.get(self, "publisher_id")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        """
        SaaS Offer Status
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="termUnit")
    def term_unit(self) -> Optional[str]:
        """
        Offer Plan Term unit
        """
        return pulumi.get(self, "term_unit")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class OrganizationResourcePropertiesResponseUserDetail(dict):
    """
    Subscriber detail
    """
    def __init__(__self__, *,
                 email_address: Optional[str] = None,
                 first_name: Optional[str] = None,
                 last_name: Optional[str] = None):
        """
        Subscriber detail
        :param str email_address: Email address
        :param str first_name: First name
        :param str last_name: Last name
        """
        if email_address is not None:
            pulumi.set(__self__, "email_address", email_address)
        if first_name is not None:
            pulumi.set(__self__, "first_name", first_name)
        if last_name is not None:
            pulumi.set(__self__, "last_name", last_name)

    @property
    @pulumi.getter(name="emailAddress")
    def email_address(self) -> Optional[str]:
        """
        Email address
        """
        return pulumi.get(self, "email_address")

    @property
    @pulumi.getter(name="firstName")
    def first_name(self) -> Optional[str]:
        """
        First name
        """
        return pulumi.get(self, "first_name")

    @property
    @pulumi.getter(name="lastName")
    def last_name(self) -> Optional[str]:
        """
        Last name
        """
        return pulumi.get(self, "last_name")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


