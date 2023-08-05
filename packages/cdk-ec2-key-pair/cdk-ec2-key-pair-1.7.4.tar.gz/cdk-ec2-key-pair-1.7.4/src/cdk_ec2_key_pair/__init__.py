"""
# CDK EC2 Key Pair

[![Source](https://img.shields.io/badge/Source-GitHub-blue?logo=github)](https://github.com/udondan/cdk-ec2-key-pair)
[![Test](https://github.com/udondan/cdk-ec2-key-pair/workflows/Test/badge.svg)](https://github.com/udondan/cdk-ec2-key-pair/actions?query=workflow%3ATest)
[![GitHub](https://img.shields.io/github/license/udondan/cdk-ec2-key-pair)](https://github.com/udondan/cdk-ec2-key-pair/blob/master/LICENSE)
[![Docs](https://img.shields.io/badge/awscdk.io-cdk--ec2--key--pair-orange)](https://awscdk.io/packages/cdk-ec2-key-pair@1.7.4)

[![npm package](https://img.shields.io/npm/v/cdk-ec2-key-pair?color=brightgreen)](https://www.npmjs.com/package/cdk-ec2-key-pair)
[![PyPI package](https://img.shields.io/pypi/v/cdk-ec2-key-pair?color=brightgreen)](https://pypi.org/project/cdk-ec2-key-pair/)
[![NuGet package](https://img.shields.io/nuget/v/CDK.EC2.KeyPair?color=brightgreen)](https://www.nuget.org/packages/CDK.EC2.KeyPair/)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
[![npm](https://img.shields.io/npm/dt/cdk-ec2-key-pair?label=npm&color=blueviolet)](https://www.npmjs.com/package/cdk-ec2-key-pair)
[![PyPI](https://img.shields.io/pypi/dm/cdk-ec2-key-pair?label=pypi&color=blueviolet)](https://pypi.org/project/cdk-ec2-key-pair/)
[![NuGet](https://img.shields.io/nuget/dt/CDK.EC2.KeyPair?label=nuget&color=blueviolet)](https://www.nuget.org/packages/CDK.EC2.KeyPair/)

[AWS CDK](https://aws.amazon.com/cdk/) L3 construct for managing [EC2 Key Pairs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html).

CloudFormation doesn't directly support creation of EC2 Key Pairs. This construct provides an easy interface for creating Key Pairs through a [custom CloudFormation resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html). The private key is stored in [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/).

## Installation

This package has peer dependencies, which need to be installed along in the expected version.

For TypeScript/NodeJS, add these to your `dependencies` in `package.json`:

* cdk-ec2-key-pair
* @aws-cdk/aws-cloudformation
* @aws-cdk/aws-ec2
* @aws-cdk/aws-iam
* @aws-cdk/aws-kms
* @aws-cdk/aws-lambda

For Python, add these to your `requirements.txt`:

* cdk-ec2-key-pair
* aws-cdk.aws-cloudformation
* aws-cdk.aws-ec2
* aws-cdk.aws-iam
* aws-cdk.aws-kms
* aws-cdk.aws-lambda

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
import aws_cdk.aws_ec2 as ec2
from cdk_ec2_key_pair import KeyPair

# Create the Key Pair
key = KeyPair(self, "A-Key-Pair",
    name="a-key-pair",
    description="This is a Key Pair"
)

# Grant read access to the private key to a role or user
key.grant_read(some_role)

# Use Key Pair on an EC2 instance
ec2.Instance(self, "An-Instance", {
    "key_name": key.name
})
```

The private key will be stored in AWS Secrets Manager. The secret name by default is prefixed with `ec2-private-key/`, so in this example it will be saved as `ec2-private-key/a-key-pair`.

To download the private key via AWS cli you can run:

```bash
aws secretsmanager get-secret-value \
  --secret-id ec2-private-key/a-key-pair \
  --query SecretString \
  --output text
```

## Roadmap

* Name should be optional
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

import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.core


@jsii.enum(jsii_type="cdk-ec2-key-pair.KeyLength")
class KeyLength(enum.Enum):
    L2048 = "L2048"
    L4096 = "L4096"


@jsii.implements(aws_cdk.core.ITaggable)
class KeyPair(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-ec2-key-pair.KeyPair",
):
    """An EC2 Key Pair."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        key_length: typing.Optional[KeyLength] = None,
        kms: typing.Optional[aws_cdk.aws_kms.Key] = None,
        remove_private_key_after_days: typing.Optional[jsii.Number] = None,
        resource_prefix: typing.Optional[builtins.str] = None,
        secret_prefix: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        account: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        """Defines a new EC2 Key Pair.

        The private key will be stored in AWS Secrets Manager

        :param scope: -
        :param id: -
        :param name: Name of the Key Pair. In AWS Secrets Manager the key will be prefixed with ``ec2-private-key/``. The name can be up to 255 characters long. Valid characters include _, -, a-z, A-Z, and 0-9.
        :param description: The description for the key in AWS Secrets Manager. Default: - ''
        :param key_length: Number of bits in the key. Valid options are 2048 and 4096 Default: - 2048
        :param kms: The KMS key to use to encrypt the private key with. This needs to be a key created in the same stack. You cannot use a key imported via ARN. Default: - ``alias/aws/secretsmanager``
        :param remove_private_key_after_days: When the resource is destroyed, after how many days the private key in the AWS Secrets Manager should be deleted. Valid values are 0 and 7 to 30 Default: 0
        :param resource_prefix: A prefix for all resource names. By default all resources are prefixed with the stack name to avoid collisions with other stacks. This might cause problems when you work with long stack names and can be overridden through this parameter. Default: Name of the stack
        :param secret_prefix: Prefix for the secret in AWS Secrets Manager. Default: ``ec2-private-key/``
        :param tags: Tags that will be applied to the private key in the AWS Secrets Manager. EC2 Key Pairs themselves don't support tags Default: - None
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        """
        props = KeyPairProps(
            name=name,
            description=description,
            key_length=key_length,
            kms=kms,
            remove_private_key_after_days=remove_private_key_after_days,
            resource_prefix=resource_prefix,
            secret_prefix=secret_prefix,
            tags=tags,
            account=account,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(KeyPair, self, [scope, id, props])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants read access to the private key in AWS Secrets Manager.

        :param grantee: -
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        """ARN of the private key in AWS Secrets Manager."""
        return jsii.get(self, "arn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> aws_cdk.aws_lambda.IFunction:
        """The lambda function that is created."""
        return jsii.get(self, "lambda")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        """Name of the Key Pair."""
        return jsii.get(self, "name")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return jsii.get(self, "prefix")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.core.TagManager:
        """Resource tags."""
        return jsii.get(self, "tags")


@jsii.data_type(
    jsii_type="cdk-ec2-key-pair.KeyPairProps",
    jsii_struct_bases=[aws_cdk.core.ResourceProps],
    name_mapping={
        "account": "account",
        "physical_name": "physicalName",
        "region": "region",
        "name": "name",
        "description": "description",
        "key_length": "keyLength",
        "kms": "kms",
        "remove_private_key_after_days": "removePrivateKeyAfterDays",
        "resource_prefix": "resourcePrefix",
        "secret_prefix": "secretPrefix",
        "tags": "tags",
    },
)
class KeyPairProps(aws_cdk.core.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        key_length: typing.Optional[KeyLength] = None,
        kms: typing.Optional[aws_cdk.aws_kms.Key] = None,
        remove_private_key_after_days: typing.Optional[jsii.Number] = None,
        resource_prefix: typing.Optional[builtins.str] = None,
        secret_prefix: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        """Definition of EC2 Key Pair.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param name: Name of the Key Pair. In AWS Secrets Manager the key will be prefixed with ``ec2-private-key/``. The name can be up to 255 characters long. Valid characters include _, -, a-z, A-Z, and 0-9.
        :param description: The description for the key in AWS Secrets Manager. Default: - ''
        :param key_length: Number of bits in the key. Valid options are 2048 and 4096 Default: - 2048
        :param kms: The KMS key to use to encrypt the private key with. This needs to be a key created in the same stack. You cannot use a key imported via ARN. Default: - ``alias/aws/secretsmanager``
        :param remove_private_key_after_days: When the resource is destroyed, after how many days the private key in the AWS Secrets Manager should be deleted. Valid values are 0 and 7 to 30 Default: 0
        :param resource_prefix: A prefix for all resource names. By default all resources are prefixed with the stack name to avoid collisions with other stacks. This might cause problems when you work with long stack names and can be overridden through this parameter. Default: Name of the stack
        :param secret_prefix: Prefix for the secret in AWS Secrets Manager. Default: ``ec2-private-key/``
        :param tags: Tags that will be applied to the private key in the AWS Secrets Manager. EC2 Key Pairs themselves don't support tags Default: - None
        """
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
        }
        if account is not None:
            self._values["account"] = account
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if description is not None:
            self._values["description"] = description
        if key_length is not None:
            self._values["key_length"] = key_length
        if kms is not None:
            self._values["kms"] = kms
        if remove_private_key_after_days is not None:
            self._values["remove_private_key_after_days"] = remove_private_key_after_days
        if resource_prefix is not None:
            self._values["resource_prefix"] = resource_prefix
        if secret_prefix is not None:
            self._values["secret_prefix"] = secret_prefix
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        """The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        """
        result = self._values.get("account")
        return result

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        """The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        """
        result = self._values.get("physical_name")
        return result

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        """The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        """
        result = self._values.get("region")
        return result

    @builtins.property
    def name(self) -> builtins.str:
        """Name of the Key Pair.

        In AWS Secrets Manager the key will be prefixed with ``ec2-private-key/``.

        The name can be up to 255 characters long. Valid characters include _, -, a-z, A-Z, and 0-9.
        """
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return result

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        """The description for the key in AWS Secrets Manager.

        :default: - ''
        """
        result = self._values.get("description")
        return result

    @builtins.property
    def key_length(self) -> typing.Optional[KeyLength]:
        """Number of bits in the key.

        Valid options are 2048 and 4096

        :default: - 2048
        """
        result = self._values.get("key_length")
        return result

    @builtins.property
    def kms(self) -> typing.Optional[aws_cdk.aws_kms.Key]:
        """The KMS key to use to encrypt the private key with.

        This needs to be a key created in the same stack. You cannot use a key imported via ARN.

        :default: - ``alias/aws/secretsmanager``
        """
        result = self._values.get("kms")
        return result

    @builtins.property
    def remove_private_key_after_days(self) -> typing.Optional[jsii.Number]:
        """When the resource is destroyed, after how many days the private key in the AWS Secrets Manager should be deleted.

        Valid values are 0 and 7 to 30

        :default: 0
        """
        result = self._values.get("remove_private_key_after_days")
        return result

    @builtins.property
    def resource_prefix(self) -> typing.Optional[builtins.str]:
        """A prefix for all resource names.

        By default all resources are prefixed with the stack name to avoid collisions with other stacks. This might cause problems when you work with long stack names and can be overridden through this parameter.

        :default: Name of the stack
        """
        result = self._values.get("resource_prefix")
        return result

    @builtins.property
    def secret_prefix(self) -> typing.Optional[builtins.str]:
        """Prefix for the secret in AWS Secrets Manager.

        :default: ``ec2-private-key/``
        """
        result = self._values.get("secret_prefix")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        """Tags that will be applied to the private key in the AWS Secrets Manager.

        EC2 Key Pairs themselves don't support tags

        :default: - None
        """
        result = self._values.get("tags")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyPairProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "KeyLength",
    "KeyPair",
    "KeyPairProps",
]

publication.publish()
