# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'DirectPeeringType',
    'Family',
    'Kind',
    'Role',
    'SessionAddressProvider',
    'Size',
    'Tier',
    'ValidationState',
]


class DirectPeeringType(str, Enum):
    """
    The type of direct peering.
    """
    EDGE = "Edge"
    TRANSIT = "Transit"
    CDN = "Cdn"
    INTERNAL = "Internal"
    IX = "Ix"
    IX_RS = "IxRs"


class Family(str, Enum):
    """
    The family of the peering SKU.
    """
    DIRECT = "Direct"
    EXCHANGE = "Exchange"


class Kind(str, Enum):
    """
    The kind of the peering.
    """
    DIRECT = "Direct"
    EXCHANGE = "Exchange"


class Role(str, Enum):
    """
    The role of the contact.
    """
    NOC = "Noc"
    POLICY = "Policy"
    TECHNICAL = "Technical"
    SERVICE = "Service"
    ESCALATION = "Escalation"
    OTHER = "Other"


class SessionAddressProvider(str, Enum):
    """
    The field indicating if Microsoft provides session ip addresses.
    """
    MICROSOFT = "Microsoft"
    PEER = "Peer"


class Size(str, Enum):
    """
    The size of the peering SKU.
    """
    FREE = "Free"
    METERED = "Metered"
    UNLIMITED = "Unlimited"


class Tier(str, Enum):
    """
    The tier of the peering SKU.
    """
    BASIC = "Basic"
    PREMIUM = "Premium"


class ValidationState(str, Enum):
    """
    The validation state of the ASN associated with the peer.
    """
    NONE = "None"
    PENDING = "Pending"
    APPROVED = "Approved"
    FAILED = "Failed"
