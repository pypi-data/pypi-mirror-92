# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union
from ... import _utilities, _tables
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['Server']


class Server(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 administrator_login: Optional[pulumi.Input[str]] = None,
                 administrator_login_password: Optional[pulumi.Input[str]] = None,
                 identity: Optional[pulumi.Input[pulumi.InputType['ResourceIdentityArgs']]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 minimal_tls_version: Optional[pulumi.Input[str]] = None,
                 public_network_access: Optional[pulumi.Input[Union[str, 'ServerPublicNetworkAccess']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 server_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 version: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        An Azure SQL Database server.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] administrator_login: Administrator username for the server. Once created it cannot be changed.
        :param pulumi.Input[str] administrator_login_password: The administrator login password (required for server creation).
        :param pulumi.Input[pulumi.InputType['ResourceIdentityArgs']] identity: The Azure Active Directory identity of the server.
        :param pulumi.Input[str] location: Resource location.
        :param pulumi.Input[str] minimal_tls_version: Minimal TLS version. Allowed values: '1.0', '1.1', '1.2'
        :param pulumi.Input[Union[str, 'ServerPublicNetworkAccess']] public_network_access: Whether or not public endpoint access is allowed for this server.  Value is optional but if passed in, must be 'Enabled' or 'Disabled'
        :param pulumi.Input[str] resource_group_name: The name of the resource group that contains the resource. You can obtain this value from the Azure Resource Manager API or the portal.
        :param pulumi.Input[str] server_name: The name of the server.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Resource tags.
        :param pulumi.Input[str] version: The version of the server.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['administrator_login'] = administrator_login
            __props__['administrator_login_password'] = administrator_login_password
            __props__['identity'] = identity
            if location is None and not opts.urn:
                raise TypeError("Missing required property 'location'")
            __props__['location'] = location
            __props__['minimal_tls_version'] = minimal_tls_version
            __props__['public_network_access'] = public_network_access
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if server_name is None and not opts.urn:
                raise TypeError("Missing required property 'server_name'")
            __props__['server_name'] = server_name
            __props__['tags'] = tags
            __props__['version'] = version
            __props__['fully_qualified_domain_name'] = None
            __props__['kind'] = None
            __props__['name'] = None
            __props__['private_endpoint_connections'] = None
            __props__['state'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:sql/latest:Server"), pulumi.Alias(type_="azure-nextgen:sql/v20140401:Server"), pulumi.Alias(type_="azure-nextgen:sql/v20150501preview:Server"), pulumi.Alias(type_="azure-nextgen:sql/v20200202preview:Server"), pulumi.Alias(type_="azure-nextgen:sql/v20200801preview:Server")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Server, __self__).__init__(
            'azure-nextgen:sql/v20190601preview:Server',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Server':
        """
        Get an existing Server resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Server(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="administratorLogin")
    def administrator_login(self) -> pulumi.Output[Optional[str]]:
        """
        Administrator username for the server. Once created it cannot be changed.
        """
        return pulumi.get(self, "administrator_login")

    @property
    @pulumi.getter(name="administratorLoginPassword")
    def administrator_login_password(self) -> pulumi.Output[Optional[str]]:
        """
        The administrator login password (required for server creation).
        """
        return pulumi.get(self, "administrator_login_password")

    @property
    @pulumi.getter(name="fullyQualifiedDomainName")
    def fully_qualified_domain_name(self) -> pulumi.Output[str]:
        """
        The fully qualified domain name of the server.
        """
        return pulumi.get(self, "fully_qualified_domain_name")

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[Optional['outputs.ResourceIdentityResponse']]:
        """
        The Azure Active Directory identity of the server.
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter
    def kind(self) -> pulumi.Output[str]:
        """
        Kind of sql server. This is metadata used for the Azure portal experience.
        """
        return pulumi.get(self, "kind")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Resource location.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="minimalTlsVersion")
    def minimal_tls_version(self) -> pulumi.Output[Optional[str]]:
        """
        Minimal TLS version. Allowed values: '1.0', '1.1', '1.2'
        """
        return pulumi.get(self, "minimal_tls_version")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Resource name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="privateEndpointConnections")
    def private_endpoint_connections(self) -> pulumi.Output[Sequence['outputs.ServerPrivateEndpointConnectionResponse']]:
        """
        List of private endpoint connections on a server
        """
        return pulumi.get(self, "private_endpoint_connections")

    @property
    @pulumi.getter(name="publicNetworkAccess")
    def public_network_access(self) -> pulumi.Output[Optional[str]]:
        """
        Whether or not public endpoint access is allowed for this server.  Value is optional but if passed in, must be 'Enabled' or 'Disabled'
        """
        return pulumi.get(self, "public_network_access")

    @property
    @pulumi.getter
    def state(self) -> pulumi.Output[str]:
        """
        The state of the server.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Resource tags.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        Resource type.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def version(self) -> pulumi.Output[Optional[str]]:
        """
        The version of the server.
        """
        return pulumi.get(self, "version")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

