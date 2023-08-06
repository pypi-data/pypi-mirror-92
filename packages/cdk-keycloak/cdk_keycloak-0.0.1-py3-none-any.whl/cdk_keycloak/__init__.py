"""
[![NPM version](https://badge.fury.io/js/cdk-keycloak.svg)](https://badge.fury.io/js/cdk-keycloak)
[![PyPI version](https://badge.fury.io/py/cdk-keycloak.svg)](https://badge.fury.io/py/cdk-keycloak)
![Release](https://github.com/pahud/cdk-keycloak/workflows/Release/badge.svg)

# `cdk-keycloak`

CDK construct library that allows you to create KeyCloak service on AWS in TypeScript or Python

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_keycloak import KeyCloak

app = cdk.App()

env = {
    "region": process.env.CDK_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

stack = cdk.Stack(app, "keycloak-demo", env=env)
KeyCloak(stack, "KeyCloak")
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

import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_rds
import aws_cdk.aws_secretsmanager
import aws_cdk.core


class ContainerService(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-keycloak.ContainerService",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        db_host: builtins.str,
        db_secret: aws_cdk.aws_secretsmanager.ISecret,
        db_user: builtins.str,
        keycloak_secret: aws_cdk.aws_secretsmanager.ISecret,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param db_host: 
        :param db_secret: 
        :param db_user: 
        :param keycloak_secret: 
        :param vpc: 
        """
        props = ContainerServiceProps(
            db_host=db_host,
            db_secret=db_secret,
            db_user=db_user,
            keycloak_secret=keycloak_secret,
            vpc=vpc,
        )

        jsii.create(ContainerService, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        return jsii.get(self, "service")


@jsii.data_type(
    jsii_type="cdk-keycloak.ContainerServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_host": "dbHost",
        "db_secret": "dbSecret",
        "db_user": "dbUser",
        "keycloak_secret": "keycloakSecret",
        "vpc": "vpc",
    },
)
class ContainerServiceProps:
    def __init__(
        self,
        *,
        db_host: builtins.str,
        db_secret: aws_cdk.aws_secretsmanager.ISecret,
        db_user: builtins.str,
        keycloak_secret: aws_cdk.aws_secretsmanager.ISecret,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> None:
        """
        :param db_host: 
        :param db_secret: 
        :param db_user: 
        :param keycloak_secret: 
        :param vpc: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "db_host": db_host,
            "db_secret": db_secret,
            "db_user": db_user,
            "keycloak_secret": keycloak_secret,
            "vpc": vpc,
        }

    @builtins.property
    def db_host(self) -> builtins.str:
        result = self._values.get("db_host")
        assert result is not None, "Required property 'db_host' is missing"
        return result

    @builtins.property
    def db_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        result = self._values.get("db_secret")
        assert result is not None, "Required property 'db_secret' is missing"
        return result

    @builtins.property
    def db_user(self) -> builtins.str:
        result = self._values.get("db_user")
        assert result is not None, "Required property 'db_user' is missing"
        return result

    @builtins.property
    def keycloak_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        result = self._values.get("keycloak_secret")
        assert result is not None, "Required property 'keycloak_secret' is missing"
        return result

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Database(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-keycloak.Database",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        database_username: typing.Optional[builtins.str] = None,
        engine: typing.Optional[aws_cdk.aws_rds.IClusterEngine] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: 
        :param database_username: database user name. Default: admin
        :param engine: 
        :param instance_type: 
        """
        props = DatabaseProps(
            vpc=vpc,
            database_username=database_username,
            engine=engine,
            instance_type=instance_type,
        )

        jsii.create(Database, self, [scope, id, props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterEndpointHostname")
    def cluster_endpoint_hostname(self) -> builtins.str:
        return jsii.get(self, "clusterEndpointHostname")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        return jsii.get(self, "clusterIdentifier")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clusterReadEndpointHostname")
    def cluster_read_endpoint_hostname(self) -> builtins.str:
        return jsii.get(self, "clusterReadEndpointHostname")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="databaseUsername")
    def database_username(self) -> builtins.str:
        return jsii.get(self, "databaseUsername")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="dbcluster")
    def dbcluster(self) -> aws_cdk.aws_rds.DatabaseCluster:
        return jsii.get(self, "dbcluster")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="secret")
    def secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        return jsii.get(self, "secret")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return jsii.get(self, "vpc")


@jsii.data_type(
    jsii_type="cdk-keycloak.DatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "database_username": "databaseUsername",
        "engine": "engine",
        "instance_type": "instanceType",
    },
)
class DatabaseProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        database_username: typing.Optional[builtins.str] = None,
        engine: typing.Optional[aws_cdk.aws_rds.IClusterEngine] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
    ) -> None:
        """
        :param vpc: 
        :param database_username: database user name. Default: admin
        :param engine: 
        :param instance_type: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if database_username is not None:
            self._values["database_username"] = database_username
        if engine is not None:
            self._values["engine"] = engine
        if instance_type is not None:
            self._values["instance_type"] = instance_type

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return result

    @builtins.property
    def database_username(self) -> typing.Optional[builtins.str]:
        """database user name.

        :default: admin
        """
        result = self._values.get("database_username")
        return result

    @builtins.property
    def engine(self) -> typing.Optional[aws_cdk.aws_rds.IClusterEngine]:
        result = self._values.get("engine")
        return result

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        result = self._values.get("instance_type")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-keycloak.KeyCloadProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc"},
)
class KeyCloadProps:
    def __init__(self, *, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None) -> None:
        """
        :param vpc: 
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyCloadProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyCloak(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-keycloak.KeyCloak",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: 
        """
        props = KeyCloadProps(vpc=vpc)

        jsii.create(KeyCloak, self, [scope, id, props])

    @jsii.member(jsii_name="addDatabase")
    def add_database(self) -> Database:
        return jsii.invoke(self, "addDatabase", [])

    @jsii.member(jsii_name="addKeyCloakContainerService")
    def add_key_cloak_container_service(
        self,
        *,
        db_host: builtins.str,
        db_secret: aws_cdk.aws_secretsmanager.ISecret,
        db_user: builtins.str,
        keycloak_secret: aws_cdk.aws_secretsmanager.ISecret,
        vpc: aws_cdk.aws_ec2.IVpc,
    ) -> ContainerService:
        """
        :param db_host: 
        :param db_secret: 
        :param db_user: 
        :param keycloak_secret: 
        :param vpc: 
        """
        props = ContainerServiceProps(
            db_host=db_host,
            db_secret=db_secret,
            db_user=db_user,
            keycloak_secret=keycloak_secret,
            vpc=vpc,
        )

        return jsii.invoke(self, "addKeyCloakContainerService", [props])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return jsii.get(self, "vpc")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="db")
    def db(self) -> typing.Optional[Database]:
        return jsii.get(self, "db")


__all__ = [
    "ContainerService",
    "ContainerServiceProps",
    "Database",
    "DatabaseProps",
    "KeyCloadProps",
    "KeyCloak",
]

publication.publish()
