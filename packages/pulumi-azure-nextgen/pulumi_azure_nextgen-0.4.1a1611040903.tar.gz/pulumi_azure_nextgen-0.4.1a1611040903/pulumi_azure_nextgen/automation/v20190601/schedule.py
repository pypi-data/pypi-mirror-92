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

__all__ = ['Schedule']


class Schedule(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 advanced_schedule: Optional[pulumi.Input[pulumi.InputType['AdvancedScheduleArgs']]] = None,
                 automation_account_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 expiry_time: Optional[pulumi.Input[str]] = None,
                 frequency: Optional[pulumi.Input[Union[str, 'ScheduleFrequency']]] = None,
                 interval: Optional[Any] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 schedule_name: Optional[pulumi.Input[str]] = None,
                 start_time: Optional[pulumi.Input[str]] = None,
                 time_zone: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Definition of the schedule.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['AdvancedScheduleArgs']] advanced_schedule: Gets or sets the AdvancedSchedule.
        :param pulumi.Input[str] automation_account_name: The name of the automation account.
        :param pulumi.Input[str] description: Gets or sets the description of the schedule.
        :param pulumi.Input[str] expiry_time: Gets or sets the end time of the schedule.
        :param pulumi.Input[Union[str, 'ScheduleFrequency']] frequency: Gets or sets the frequency of the schedule.
        :param Any interval: Gets or sets the interval of the schedule.
        :param pulumi.Input[str] name: Gets or sets the name of the Schedule.
        :param pulumi.Input[str] resource_group_name: Name of an Azure Resource group.
        :param pulumi.Input[str] schedule_name: The schedule name.
        :param pulumi.Input[str] start_time: Gets or sets the start time of the schedule.
        :param pulumi.Input[str] time_zone: Gets or sets the time zone of the schedule.
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

            __props__['advanced_schedule'] = advanced_schedule
            if automation_account_name is None and not opts.urn:
                raise TypeError("Missing required property 'automation_account_name'")
            __props__['automation_account_name'] = automation_account_name
            __props__['description'] = description
            __props__['expiry_time'] = expiry_time
            if frequency is None and not opts.urn:
                raise TypeError("Missing required property 'frequency'")
            __props__['frequency'] = frequency
            __props__['interval'] = interval
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            if schedule_name is None and not opts.urn:
                raise TypeError("Missing required property 'schedule_name'")
            __props__['schedule_name'] = schedule_name
            if start_time is None and not opts.urn:
                raise TypeError("Missing required property 'start_time'")
            __props__['start_time'] = start_time
            __props__['time_zone'] = time_zone
            __props__['creation_time'] = None
            __props__['expiry_time_offset_minutes'] = None
            __props__['is_enabled'] = None
            __props__['last_modified_time'] = None
            __props__['next_run'] = None
            __props__['next_run_offset_minutes'] = None
            __props__['start_time_offset_minutes'] = None
            __props__['type'] = None
        alias_opts = pulumi.ResourceOptions(aliases=[pulumi.Alias(type_="azure-nextgen:automation/latest:Schedule"), pulumi.Alias(type_="azure-nextgen:automation/v20151031:Schedule"), pulumi.Alias(type_="azure-nextgen:automation/v20200113preview:Schedule")])
        opts = pulumi.ResourceOptions.merge(opts, alias_opts)
        super(Schedule, __self__).__init__(
            'azure-nextgen:automation/v20190601:Schedule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Schedule':
        """
        Get an existing Schedule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        return Schedule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="advancedSchedule")
    def advanced_schedule(self) -> pulumi.Output[Optional['outputs.AdvancedScheduleResponse']]:
        """
        Gets or sets the advanced schedule.
        """
        return pulumi.get(self, "advanced_schedule")

    @property
    @pulumi.getter(name="creationTime")
    def creation_time(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the creation time.
        """
        return pulumi.get(self, "creation_time")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the description.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="expiryTime")
    def expiry_time(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the end time of the schedule.
        """
        return pulumi.get(self, "expiry_time")

    @property
    @pulumi.getter(name="expiryTimeOffsetMinutes")
    def expiry_time_offset_minutes(self) -> pulumi.Output[Optional[float]]:
        """
        Gets or sets the expiry time's offset in minutes.
        """
        return pulumi.get(self, "expiry_time_offset_minutes")

    @property
    @pulumi.getter
    def frequency(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the frequency of the schedule.
        """
        return pulumi.get(self, "frequency")

    @property
    @pulumi.getter
    def interval(self) -> pulumi.Output[Optional[Any]]:
        """
        Gets or sets the interval of the schedule.
        """
        return pulumi.get(self, "interval")

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Gets or sets a value indicating whether this schedule is enabled.
        """
        return pulumi.get(self, "is_enabled")

    @property
    @pulumi.getter(name="lastModifiedTime")
    def last_modified_time(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the last modified time.
        """
        return pulumi.get(self, "last_modified_time")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the resource
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nextRun")
    def next_run(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the next run time of the schedule.
        """
        return pulumi.get(self, "next_run")

    @property
    @pulumi.getter(name="nextRunOffsetMinutes")
    def next_run_offset_minutes(self) -> pulumi.Output[Optional[float]]:
        """
        Gets or sets the next run time's offset in minutes.
        """
        return pulumi.get(self, "next_run_offset_minutes")

    @property
    @pulumi.getter(name="startTime")
    def start_time(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the start time of the schedule.
        """
        return pulumi.get(self, "start_time")

    @property
    @pulumi.getter(name="startTimeOffsetMinutes")
    def start_time_offset_minutes(self) -> pulumi.Output[float]:
        """
        Gets the start time's offset in minutes.
        """
        return pulumi.get(self, "start_time_offset_minutes")

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> pulumi.Output[Optional[str]]:
        """
        Gets or sets the time zone of the schedule.
        """
        return pulumi.get(self, "time_zone")

    @property
    @pulumi.getter
    def type(self) -> pulumi.Output[str]:
        """
        The type of the resource.
        """
        return pulumi.get(self, "type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

