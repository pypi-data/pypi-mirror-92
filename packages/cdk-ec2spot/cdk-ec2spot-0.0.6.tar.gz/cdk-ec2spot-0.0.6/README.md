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
