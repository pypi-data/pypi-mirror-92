"""
[![NPM version](https://badge.fury.io/js/cdk-eksdistro.svg)](https://badge.fury.io/js/cdk-eksdistro)
[![PyPI version](https://badge.fury.io/py/cdk-eksdistro.svg)](https://badge.fury.io/py/cdk-eksdistro)
![Release](https://github.com/pahud/cdk-eksdistro/workflows/Release/badge.svg)

# `cdk-eksdistro`

CDK construct library that allows you to create [Amazon EKS Distro](https://distro.eks.amazonaws.com/) on Amaozn EC2 instance(s).

# How it works

Under the hood, `cdk-eksdistro` creates an Amazon Auto Scaling Group with single Amazon EC2 instance running Ubuntu Linux LTS `20.04` and installs the [eks snap](https://snapcraft.io/eks) from the `UserData`.

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
imoprtClusterfrom"cdk-eksdistro"

app = cdk.App()

env = {
    "region": process.env.CDK_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

stack = cdk.Stack(app, "eksdistro-stack", env=env)

Cluster(stack, "Cluster")
```

## Spot Instance

To create Amazon EC2 Spot instance instead of on-demand, use the `spot` property:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Cluster(stack, "Cluster", spot=True)
```

# Validate the cluster

By default, the `Cluster` construct creates a single-node EKS-D cluster on AWS EC2 with the latest Ubuntu Linux LTS AMI. To validate the cluster, open the EC2 console, select the instance and click the **Connect** button and select **session manager**.

Run the following commands to execute `kubectl` in the cluster.

![](https://pbs.twimg.com/media/EsEgnhoVoAIHnkr?format=jpg&name=4096x4096)

# Reference

* https://aws.amazon.com/blogs/opensource/introducing-amazon-eks-distro/
* https://ubuntu.com/blog/install-amazon-eks-distro-anywhere
* https://microk8s.io/
* https://snapcraft.io/microk8s
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

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.core


@jsii.data_type(
    jsii_type="cdk-eksdistro.AutoScalingGroupOptions",
    jsii_struct_bases=[],
    name_mapping={
        "launch_template": "launchTemplate",
        "vpc": "vpc",
        "default_capacity_size": "defaultCapacitySize",
    },
)
class AutoScalingGroupOptions:
    def __init__(
        self,
        *,
        launch_template: "LaunchTemplateOptions",
        vpc: aws_cdk.aws_ec2.IVpc,
        default_capacity_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param launch_template: Launch template options for the AutoScalingGroup.
        :param vpc: The vpc for the AutoScalingGroup.
        :param default_capacity_size: default capacity size for the Auto Scaling Group. Default: 1
        """
        if isinstance(launch_template, dict):
            launch_template = LaunchTemplateOptions(**launch_template)
        self._values: typing.Dict[str, typing.Any] = {
            "launch_template": launch_template,
            "vpc": vpc,
        }
        if default_capacity_size is not None:
            self._values["default_capacity_size"] = default_capacity_size

    @builtins.property
    def launch_template(self) -> "LaunchTemplateOptions":
        """Launch template options for the AutoScalingGroup."""
        result = self._values.get("launch_template")
        assert result is not None, "Required property 'launch_template' is missing"
        return result

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

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoScalingGroupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-eksdistro.BlockDurationMinutes")
class BlockDurationMinutes(enum.Enum):
    ONE_HOUR = "ONE_HOUR"
    TWO_HOURS = "TWO_HOURS"
    THREE_HOURS = "THREE_HOURS"
    FOUR_HOURS = "FOUR_HOURS"
    FIVE_HOURS = "FIVE_HOURS"
    SIX_HOURS = "SIX_HOURS"


class Cluster(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eksdistro.Cluster",
):
    """Represents the EKS-D cluster."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        capacity_size: typing.Optional[jsii.Number] = None,
        default_instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        machine_image: typing.Optional[aws_cdk.aws_ec2.IMachineImage] = None,
        output_ami_id: typing.Optional[builtins.bool] = None,
        spot: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param capacity_size: number of instances. Default: 1
        :param default_instance_type: The default EC2 instance type. Default: t3.large
        :param machine_image: AMI for the EKS-D instance node. Default: - The latest AMI from ubuntu-focal-20.04-amd64-server
        :param output_ami_id: Print AMI ID in the output. Default: - true
        :param spot: Create EC2 spot instnce for the cluster node. Default: - false
        :param vpc: VPC for the cluster. Default: - get or create a VPC
        """
        props = ClusterProps(
            capacity_size=capacity_size,
            default_instance_type=default_instance_type,
            machine_image=machine_image,
            output_ami_id=output_ami_id,
            spot=spot,
            vpc=vpc,
        )

        jsii.create(Cluster, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-eksdistro.ClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity_size": "capacitySize",
        "default_instance_type": "defaultInstanceType",
        "machine_image": "machineImage",
        "output_ami_id": "outputAmiId",
        "spot": "spot",
        "vpc": "vpc",
    },
)
class ClusterProps:
    def __init__(
        self,
        *,
        capacity_size: typing.Optional[jsii.Number] = None,
        default_instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        machine_image: typing.Optional[aws_cdk.aws_ec2.IMachineImage] = None,
        output_ami_id: typing.Optional[builtins.bool] = None,
        spot: typing.Optional[builtins.bool] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """Construct properties for the EKS-D cluster.

        :param capacity_size: number of instances. Default: 1
        :param default_instance_type: The default EC2 instance type. Default: t3.large
        :param machine_image: AMI for the EKS-D instance node. Default: - The latest AMI from ubuntu-focal-20.04-amd64-server
        :param output_ami_id: Print AMI ID in the output. Default: - true
        :param spot: Create EC2 spot instnce for the cluster node. Default: - false
        :param vpc: VPC for the cluster. Default: - get or create a VPC
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if capacity_size is not None:
            self._values["capacity_size"] = capacity_size
        if default_instance_type is not None:
            self._values["default_instance_type"] = default_instance_type
        if machine_image is not None:
            self._values["machine_image"] = machine_image
        if output_ami_id is not None:
            self._values["output_ami_id"] = output_ami_id
        if spot is not None:
            self._values["spot"] = spot
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def capacity_size(self) -> typing.Optional[jsii.Number]:
        """number of instances.

        :default: 1
        """
        result = self._values.get("capacity_size")
        return result

    @builtins.property
    def default_instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """The default EC2 instance type.

        :default: t3.large
        """
        result = self._values.get("default_instance_type")
        return result

    @builtins.property
    def machine_image(self) -> typing.Optional[aws_cdk.aws_ec2.IMachineImage]:
        """AMI for the EKS-D instance node.

        :default: - The latest AMI from ubuntu-focal-20.04-amd64-server
        """
        result = self._values.get("machine_image")
        return result

    @builtins.property
    def output_ami_id(self) -> typing.Optional[builtins.bool]:
        """Print AMI ID in the output.

        :default: - true
        """
        result = self._values.get("output_ami_id")
        return result

    @builtins.property
    def spot(self) -> typing.Optional[builtins.bool]:
        """Create EC2 spot instnce for the cluster node.

        :default: - false
        """
        result = self._values.get("spot")
        return result

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC for the cluster.

        :default: - get or create a VPC
        """
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-eksdistro.InstanceInterruptionBehavior")
class InstanceInterruptionBehavior(enum.Enum):
    HIBERNATE = "HIBERNATE"
    STOP = "STOP"
    TERMINATE = "TERMINATE"


@jsii.data_type(
    jsii_type="cdk-eksdistro.LaunchTemplateOptions",
    jsii_struct_bases=[],
    name_mapping={
        "instance_type": "instanceType",
        "machine_image": "machineImage",
        "user_data": "userData",
        "instance_profile": "instanceProfile",
        "spot_options": "spotOptions",
    },
)
class LaunchTemplateOptions:
    def __init__(
        self,
        *,
        instance_type: aws_cdk.aws_ec2.InstanceType,
        machine_image: aws_cdk.aws_ec2.IMachineImage,
        user_data: aws_cdk.aws_ec2.UserData,
        instance_profile: typing.Optional[aws_cdk.aws_iam.CfnInstanceProfile] = None,
        spot_options: typing.Optional["SpotOptions"] = None,
    ) -> None:
        """
        :param instance_type: 
        :param machine_image: 
        :param user_data: 
        :param instance_profile: 
        :param spot_options: 
        """
        if isinstance(spot_options, dict):
            spot_options = SpotOptions(**spot_options)
        self._values: typing.Dict[str, typing.Any] = {
            "instance_type": instance_type,
            "machine_image": machine_image,
            "user_data": user_data,
        }
        if instance_profile is not None:
            self._values["instance_profile"] = instance_profile
        if spot_options is not None:
            self._values["spot_options"] = spot_options

    @builtins.property
    def instance_type(self) -> aws_cdk.aws_ec2.InstanceType:
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return result

    @builtins.property
    def machine_image(self) -> aws_cdk.aws_ec2.IMachineImage:
        result = self._values.get("machine_image")
        assert result is not None, "Required property 'machine_image' is missing"
        return result

    @builtins.property
    def user_data(self) -> aws_cdk.aws_ec2.UserData:
        result = self._values.get("user_data")
        assert result is not None, "Required property 'user_data' is missing"
        return result

    @builtins.property
    def instance_profile(self) -> typing.Optional[aws_cdk.aws_iam.CfnInstanceProfile]:
        result = self._values.get("instance_profile")
        return result

    @builtins.property
    def spot_options(self) -> typing.Optional["SpotOptions"]:
        result = self._values.get("spot_options")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LaunchTemplateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-eksdistro.SpotInstanceType")
class SpotInstanceType(enum.Enum):
    ONE_TIME = "ONE_TIME"
    PERSISTENT = "PERSISTENT"


@jsii.data_type(
    jsii_type="cdk-eksdistro.SpotOptions",
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


class UbumtuAmiProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-eksdistro.UbumtuAmiProvider",
):
    """The AMI provider to get the latest Ubuntu Linux AMI."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        user_data: aws_cdk.aws_ec2.UserData,
    ) -> None:
        """
        :param scope: -
        :param user_data: -
        """
        jsii.create(UbumtuAmiProvider, self, [scope, user_data])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="amiId")
    def ami_id(self) -> aws_cdk.aws_ec2.IMachineImage:
        return jsii.get(self, "amiId")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="scope")
    def scope(self) -> aws_cdk.core.Construct:
        return jsii.get(self, "scope")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="userData")
    def user_data(self) -> aws_cdk.aws_ec2.UserData:
        return jsii.get(self, "userData")


__all__ = [
    "AutoScalingGroupOptions",
    "BlockDurationMinutes",
    "Cluster",
    "ClusterProps",
    "InstanceInterruptionBehavior",
    "LaunchTemplateOptions",
    "SpotInstanceType",
    "SpotOptions",
    "UbumtuAmiProvider",
]

publication.publish()
