"""
[![NPM version](https://badge.fury.io/js/cdk-ec2spot.svg)](https://badge.fury.io/js/cdk-ec2spot)
[![PyPI version](https://badge.fury.io/py/cdk-ec2spot.svg)](https://badge.fury.io/py/cdk-ec2spot)
![Release](https://github.com/pahud/cdk-ec2spot/workflows/Release/badge.svg)

# `cdk-ec2spot`

CDK construct library that allows you to create EC2 Spot instances with AWS AutoScaling Group or SpotFleet

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk_ec2spot as ec2spot

# create a ec2spot provider
provider = ec2spot.Provider(stack, "Provider")

# import or create a vpc
vpc = provider.get_or_create_vpc(stack)

# create an AutoScalingGroup with Launch Template for spot instances
provider.create_auto_scaling_group("SpotASG",
    vpc=vpc,
    default_capacity_size=2,
    instance_type=ec2.InstanceType("m5.large")
)
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_autoscaling
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.core


@jsii.data_type(
    jsii_type="cdk-ec2spot.AutoScalingGroupOptions",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "default_capacity_size": "defaultCapacitySize",
        "instance_profile": "instanceProfile",
        "instance_type": "instanceType",
        "machine_image": "machineImage",
        "spot_options": "spotOptions",
        "user_data": "userData",
    },
)
class AutoScalingGroupOptions:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        default_capacity_size: typing.Optional[jsii.Number] = None,
        instance_profile: typing.Optional[aws_cdk.aws_iam.CfnInstanceProfile] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        machine_image: typing.Optional[aws_cdk.aws_ec2.IMachineImage] = None,
        spot_options: typing.Optional["SpotOptions"] = None,
        user_data: typing.Optional[aws_cdk.aws_ec2.UserData] = None,
    ) -> None:
        """
        :param vpc: The vpc for the AutoScalingGroup.
        :param default_capacity_size: default capacity size for the Auto Scaling Group. Default: 1
        :param instance_profile: 
        :param instance_type: 
        :param machine_image: 
        :param spot_options: 
        :param user_data: 
        """
        if isinstance(spot_options, dict):
            spot_options = SpotOptions(**spot_options)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if default_capacity_size is not None:
            self._values["default_capacity_size"] = default_capacity_size
        if instance_profile is not None:
            self._values["instance_profile"] = instance_profile
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if machine_image is not None:
            self._values["machine_image"] = machine_image
        if spot_options is not None:
            self._values["spot_options"] = spot_options
        if user_data is not None:
            self._values["user_data"] = user_data

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The vpc for the AutoScalingGroup."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def default_capacity_size(self) -> typing.Optional[jsii.Number]:
        """default capacity size for the Auto Scaling Group.

        :default: 1
        """
        result = self._values.get("default_capacity_size")
        return result

    @builtins.property
    def instance_profile(self) -> typing.Optional[aws_cdk.aws_iam.CfnInstanceProfile]:
        result = self._values.get("instance_profile")
        return result

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        result = self._values.get("instance_type")
        return result

    @builtins.property
    def machine_image(self) -> typing.Optional[aws_cdk.aws_ec2.IMachineImage]:
        result = self._values.get("machine_image")
        return result

    @builtins.property
    def spot_options(self) -> typing.Optional["SpotOptions"]:
        result = self._values.get("spot_options")
        return result

    @builtins.property
    def user_data(self) -> typing.Optional[aws_cdk.aws_ec2.UserData]:
        result = self._values.get("user_data")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoScalingGroupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-ec2spot.BlockDurationMinutes")
class BlockDurationMinutes(enum.Enum):
    ONE_HOUR = "ONE_HOUR"
    TWO_HOURS = "TWO_HOURS"
    THREE_HOURS = "THREE_HOURS"
    FOUR_HOURS = "FOUR_HOURS"
    FIVE_HOURS = "FIVE_HOURS"
    SIX_HOURS = "SIX_HOURS"


@jsii.enum(jsii_type="cdk-ec2spot.InstanceInterruptionBehavior")
class InstanceInterruptionBehavior(enum.Enum):
    HIBERNATE = "HIBERNATE"
    STOP = "STOP"
    TERMINATE = "TERMINATE"


class Provider(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-ec2spot.Provider",
):
    def __init__(self, scope: aws_cdk.core.Construct, id: builtins.str) -> None:
        """
        :param scope: -
        :param id: -
        """
        jsii.create(Provider, self, [scope, id])

    @jsii.member(jsii_name="createAutoScalingGroup")
    def create_auto_scaling_group(
        self,
        id: builtins.str,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        default_capacity_size: typing.Optional[jsii.Number] = None,
        instance_profile: typing.Optional[aws_cdk.aws_iam.CfnInstanceProfile] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        machine_image: typing.Optional[aws_cdk.aws_ec2.IMachineImage] = None,
        spot_options: typing.Optional["SpotOptions"] = None,
        user_data: typing.Optional[aws_cdk.aws_ec2.UserData] = None,
    ) -> aws_cdk.aws_autoscaling.AutoScalingGroup:
        """
        :param id: -
        :param vpc: The vpc for the AutoScalingGroup.
        :param default_capacity_size: default capacity size for the Auto Scaling Group. Default: 1
        :param instance_profile: 
        :param instance_type: 
        :param machine_image: 
        :param spot_options: 
        :param user_data: 
        """
        options = AutoScalingGroupOptions(
            vpc=vpc,
            default_capacity_size=default_capacity_size,
            instance_profile=instance_profile,
            instance_type=instance_type,
            machine_image=machine_image,
            spot_options=spot_options,
            user_data=user_data,
        )

        return jsii.invoke(self, "createAutoScalingGroup", [id, options])

    @jsii.member(jsii_name="getOrCreateVpc")
    def get_or_create_vpc(self, scope: aws_cdk.core.Construct) -> aws_cdk.aws_ec2.IVpc:
        """
        :param scope: -
        """
        return jsii.invoke(self, "getOrCreateVpc", [scope])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="amazonLinuxAmiImageId")
    def amazon_linux_ami_image_id(self) -> builtins.str:
        return jsii.get(self, "amazonLinuxAmiImageId")


@jsii.enum(jsii_type="cdk-ec2spot.SpotInstanceType")
class SpotInstanceType(enum.Enum):
    ONE_TIME = "ONE_TIME"
    PERSISTENT = "PERSISTENT"


@jsii.data_type(
    jsii_type="cdk-ec2spot.SpotOptions",
    jsii_struct_bases=[],
    name_mapping={
        "block_duration_minutes": "blockDurationMinutes",
        "instance_interruption_behavior": "instanceInterruptionBehavior",
        "max_price": "maxPrice",
        "spot_instance_type": "spotInstanceType",
        "valid_until": "validUntil",
    },
)
class SpotOptions:
    def __init__(
        self,
        *,
        block_duration_minutes: typing.Optional[BlockDurationMinutes] = None,
        instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
        max_price: typing.Optional[builtins.str] = None,
        spot_instance_type: typing.Optional[SpotInstanceType] = None,
        valid_until: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param block_duration_minutes: 
        :param instance_interruption_behavior: 
        :param max_price: 
        :param spot_instance_type: 
        :param valid_until: 
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if block_duration_minutes is not None:
            self._values["block_duration_minutes"] = block_duration_minutes
        if instance_interruption_behavior is not None:
            self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if max_price is not None:
            self._values["max_price"] = max_price
        if spot_instance_type is not None:
            self._values["spot_instance_type"] = spot_instance_type
        if valid_until is not None:
            self._values["valid_until"] = valid_until

    @builtins.property
    def block_duration_minutes(self) -> typing.Optional[BlockDurationMinutes]:
        result = self._values.get("block_duration_minutes")
        return result

    @builtins.property
    def instance_interruption_behavior(
        self,
    ) -> typing.Optional[InstanceInterruptionBehavior]:
        result = self._values.get("instance_interruption_behavior")
        return result

    @builtins.property
    def max_price(self) -> typing.Optional[builtins.str]:
        result = self._values.get("max_price")
        return result

    @builtins.property
    def spot_instance_type(self) -> typing.Optional[SpotInstanceType]:
        result = self._values.get("spot_instance_type")
        return result

    @builtins.property
    def valid_until(self) -> typing.Optional[builtins.str]:
        result = self._values.get("valid_until")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpotOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AutoScalingGroupOptions",
    "BlockDurationMinutes",
    "InstanceInterruptionBehavior",
    "Provider",
    "SpotInstanceType",
    "SpotOptions",
]

publication.publish()
