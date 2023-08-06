import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

import constructs
from .. import (
    CfnResource as _CfnResource_f7d91f4b,
    CfnTag as _CfnTag_c592b05a,
    IInspectable as _IInspectable_3eb0224c,
    IResolvable as _IResolvable_6e2f5d88,
    TagManager as _TagManager_6a5badd9,
    TreeInspector as _TreeInspector_afbbf916,
)


@jsii.implements(_IInspectable_3eb0224c)
class CfnGrant(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_licensemanager.CfnGrant",
):
    """A CloudFormation ``AWS::LicenseManager::Grant``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html
    :cloudformationResource: AWS::LicenseManager::Grant
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        allowed_operations: typing.Optional[typing.List[builtins.str]] = None,
        client_token: typing.Optional[builtins.str] = None,
        filters: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnGrant.FilterProperty", _IResolvable_6e2f5d88]]]] = None,
        grant_arns: typing.Optional[typing.List[builtins.str]] = None,
        granted_operations: typing.Optional[typing.List[builtins.str]] = None,
        grantee_principal_arn: typing.Optional[builtins.str] = None,
        grant_name: typing.Optional[builtins.str] = None,
        grant_status: typing.Optional[builtins.str] = None,
        home_region: typing.Optional[builtins.str] = None,
        license_arn: typing.Optional[builtins.str] = None,
        max_results: typing.Optional[jsii.Number] = None,
        next_token: typing.Optional[builtins.str] = None,
        parent_arn: typing.Optional[builtins.str] = None,
        principals: typing.Optional[typing.List[builtins.str]] = None,
        source_version: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        status_reason: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::LicenseManager::Grant``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param allowed_operations: ``AWS::LicenseManager::Grant.AllowedOperations``.
        :param client_token: ``AWS::LicenseManager::Grant.ClientToken``.
        :param filters: ``AWS::LicenseManager::Grant.Filters``.
        :param grant_arns: ``AWS::LicenseManager::Grant.GrantArns``.
        :param granted_operations: ``AWS::LicenseManager::Grant.GrantedOperations``.
        :param grantee_principal_arn: ``AWS::LicenseManager::Grant.GranteePrincipalArn``.
        :param grant_name: ``AWS::LicenseManager::Grant.GrantName``.
        :param grant_status: ``AWS::LicenseManager::Grant.GrantStatus``.
        :param home_region: ``AWS::LicenseManager::Grant.HomeRegion``.
        :param license_arn: ``AWS::LicenseManager::Grant.LicenseArn``.
        :param max_results: ``AWS::LicenseManager::Grant.MaxResults``.
        :param next_token: ``AWS::LicenseManager::Grant.NextToken``.
        :param parent_arn: ``AWS::LicenseManager::Grant.ParentArn``.
        :param principals: ``AWS::LicenseManager::Grant.Principals``.
        :param source_version: ``AWS::LicenseManager::Grant.SourceVersion``.
        :param status: ``AWS::LicenseManager::Grant.Status``.
        :param status_reason: ``AWS::LicenseManager::Grant.StatusReason``.
        :param tags: ``AWS::LicenseManager::Grant.Tags``.
        :param version: ``AWS::LicenseManager::Grant.Version``.
        """
        props = CfnGrantProps(
            allowed_operations=allowed_operations,
            client_token=client_token,
            filters=filters,
            grant_arns=grant_arns,
            granted_operations=granted_operations,
            grantee_principal_arn=grantee_principal_arn,
            grant_name=grant_name,
            grant_status=grant_status,
            home_region=home_region,
            license_arn=license_arn,
            max_results=max_results,
            next_token=next_token,
            parent_arn=parent_arn,
            principals=principals,
            source_version=source_version,
            status=status,
            status_reason=status_reason,
            tags=tags,
            version=version,
        )

        jsii.create(CfnGrant, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrGrantArn")
    def attr_grant_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: GrantArn
        """
        return jsii.get(self, "attrGrantArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::LicenseManager::Grant.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="allowedOperations")
    def allowed_operations(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::LicenseManager::Grant.AllowedOperations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-allowedoperations
        """
        return jsii.get(self, "allowedOperations")

    @allowed_operations.setter # type: ignore
    def allowed_operations(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "allowedOperations", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clientToken")
    def client_token(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.ClientToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-clienttoken
        """
        return jsii.get(self, "clientToken")

    @client_token.setter # type: ignore
    def client_token(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clientToken", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="filters")
    def filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnGrant.FilterProperty", _IResolvable_6e2f5d88]]]]:
        """``AWS::LicenseManager::Grant.Filters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-filters
        """
        return jsii.get(self, "filters")

    @filters.setter # type: ignore
    def filters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnGrant.FilterProperty", _IResolvable_6e2f5d88]]]],
    ) -> None:
        jsii.set(self, "filters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantArns")
    def grant_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::LicenseManager::Grant.GrantArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantarns
        """
        return jsii.get(self, "grantArns")

    @grant_arns.setter # type: ignore
    def grant_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "grantArns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantedOperations")
    def granted_operations(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::LicenseManager::Grant.GrantedOperations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantedoperations
        """
        return jsii.get(self, "grantedOperations")

    @granted_operations.setter # type: ignore
    def granted_operations(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        jsii.set(self, "grantedOperations", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="granteePrincipalArn")
    def grantee_principal_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.GranteePrincipalArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-granteeprincipalarn
        """
        return jsii.get(self, "granteePrincipalArn")

    @grantee_principal_arn.setter # type: ignore
    def grantee_principal_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "granteePrincipalArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantName")
    def grant_name(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.GrantName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantname
        """
        return jsii.get(self, "grantName")

    @grant_name.setter # type: ignore
    def grant_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "grantName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="grantStatus")
    def grant_status(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.GrantStatus``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantstatus
        """
        return jsii.get(self, "grantStatus")

    @grant_status.setter # type: ignore
    def grant_status(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "grantStatus", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="homeRegion")
    def home_region(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.HomeRegion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-homeregion
        """
        return jsii.get(self, "homeRegion")

    @home_region.setter # type: ignore
    def home_region(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "homeRegion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="licenseArn")
    def license_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.LicenseArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-licensearn
        """
        return jsii.get(self, "licenseArn")

    @license_arn.setter # type: ignore
    def license_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "licenseArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxResults")
    def max_results(self) -> typing.Optional[jsii.Number]:
        """``AWS::LicenseManager::Grant.MaxResults``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-maxresults
        """
        return jsii.get(self, "maxResults")

    @max_results.setter # type: ignore
    def max_results(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxResults", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="nextToken")
    def next_token(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.NextToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-nexttoken
        """
        return jsii.get(self, "nextToken")

    @next_token.setter # type: ignore
    def next_token(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "nextToken", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="parentArn")
    def parent_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.ParentArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-parentarn
        """
        return jsii.get(self, "parentArn")

    @parent_arn.setter # type: ignore
    def parent_arn(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "parentArn", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::LicenseManager::Grant.Principals``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-principals
        """
        return jsii.get(self, "principals")

    @principals.setter # type: ignore
    def principals(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "principals", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceVersion")
    def source_version(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.SourceVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-sourceversion
        """
        return jsii.get(self, "sourceVersion")

    @source_version.setter # type: ignore
    def source_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sourceVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-status
        """
        return jsii.get(self, "status")

    @status.setter # type: ignore
    def status(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "status", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="statusReason")
    def status_reason(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.StatusReason``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-statusreason
        """
        return jsii.get(self, "statusReason")

    @status_reason.setter # type: ignore
    def status_reason(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "statusReason", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-version
        """
        return jsii.get(self, "version")

    @version.setter # type: ignore
    def version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnGrant.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "values": "values"},
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            values: typing.Union["CfnGrant.StringListProperty", _IResolvable_6e2f5d88],
        ) -> None:
            """
            :param name: ``CfnGrant.FilterProperty.Name``.
            :param values: ``CfnGrant.FilterProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-grant-filter.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "values": values,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnGrant.FilterProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-grant-filter.html#cfn-licensemanager-grant-filter-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def values(
            self,
        ) -> typing.Union["CfnGrant.StringListProperty", _IResolvable_6e2f5d88]:
            """``CfnGrant.FilterProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-grant-filter.html#cfn-licensemanager-grant-filter-values
            """
            result = self._values.get("values")
            assert result is not None, "Required property 'values' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnGrant.StringListProperty",
        jsii_struct_bases=[],
        name_mapping={"string_list": "stringList"},
    )
    class StringListProperty:
        def __init__(
            self,
            *,
            string_list: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param string_list: ``CfnGrant.StringListProperty.StringList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-grant-stringlist.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if string_list is not None:
                self._values["string_list"] = string_list

        @builtins.property
        def string_list(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnGrant.StringListProperty.StringList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-grant-stringlist.html#cfn-licensemanager-grant-stringlist-stringlist
            """
            result = self._values.get("string_list")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StringListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_licensemanager.CfnGrantProps",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_operations": "allowedOperations",
        "client_token": "clientToken",
        "filters": "filters",
        "grant_arns": "grantArns",
        "granted_operations": "grantedOperations",
        "grantee_principal_arn": "granteePrincipalArn",
        "grant_name": "grantName",
        "grant_status": "grantStatus",
        "home_region": "homeRegion",
        "license_arn": "licenseArn",
        "max_results": "maxResults",
        "next_token": "nextToken",
        "parent_arn": "parentArn",
        "principals": "principals",
        "source_version": "sourceVersion",
        "status": "status",
        "status_reason": "statusReason",
        "tags": "tags",
        "version": "version",
    },
)
class CfnGrantProps:
    def __init__(
        self,
        *,
        allowed_operations: typing.Optional[typing.List[builtins.str]] = None,
        client_token: typing.Optional[builtins.str] = None,
        filters: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union[CfnGrant.FilterProperty, _IResolvable_6e2f5d88]]]] = None,
        grant_arns: typing.Optional[typing.List[builtins.str]] = None,
        granted_operations: typing.Optional[typing.List[builtins.str]] = None,
        grantee_principal_arn: typing.Optional[builtins.str] = None,
        grant_name: typing.Optional[builtins.str] = None,
        grant_status: typing.Optional[builtins.str] = None,
        home_region: typing.Optional[builtins.str] = None,
        license_arn: typing.Optional[builtins.str] = None,
        max_results: typing.Optional[jsii.Number] = None,
        next_token: typing.Optional[builtins.str] = None,
        parent_arn: typing.Optional[builtins.str] = None,
        principals: typing.Optional[typing.List[builtins.str]] = None,
        source_version: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        status_reason: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::LicenseManager::Grant``.

        :param allowed_operations: ``AWS::LicenseManager::Grant.AllowedOperations``.
        :param client_token: ``AWS::LicenseManager::Grant.ClientToken``.
        :param filters: ``AWS::LicenseManager::Grant.Filters``.
        :param grant_arns: ``AWS::LicenseManager::Grant.GrantArns``.
        :param granted_operations: ``AWS::LicenseManager::Grant.GrantedOperations``.
        :param grantee_principal_arn: ``AWS::LicenseManager::Grant.GranteePrincipalArn``.
        :param grant_name: ``AWS::LicenseManager::Grant.GrantName``.
        :param grant_status: ``AWS::LicenseManager::Grant.GrantStatus``.
        :param home_region: ``AWS::LicenseManager::Grant.HomeRegion``.
        :param license_arn: ``AWS::LicenseManager::Grant.LicenseArn``.
        :param max_results: ``AWS::LicenseManager::Grant.MaxResults``.
        :param next_token: ``AWS::LicenseManager::Grant.NextToken``.
        :param parent_arn: ``AWS::LicenseManager::Grant.ParentArn``.
        :param principals: ``AWS::LicenseManager::Grant.Principals``.
        :param source_version: ``AWS::LicenseManager::Grant.SourceVersion``.
        :param status: ``AWS::LicenseManager::Grant.Status``.
        :param status_reason: ``AWS::LicenseManager::Grant.StatusReason``.
        :param tags: ``AWS::LicenseManager::Grant.Tags``.
        :param version: ``AWS::LicenseManager::Grant.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if allowed_operations is not None:
            self._values["allowed_operations"] = allowed_operations
        if client_token is not None:
            self._values["client_token"] = client_token
        if filters is not None:
            self._values["filters"] = filters
        if grant_arns is not None:
            self._values["grant_arns"] = grant_arns
        if granted_operations is not None:
            self._values["granted_operations"] = granted_operations
        if grantee_principal_arn is not None:
            self._values["grantee_principal_arn"] = grantee_principal_arn
        if grant_name is not None:
            self._values["grant_name"] = grant_name
        if grant_status is not None:
            self._values["grant_status"] = grant_status
        if home_region is not None:
            self._values["home_region"] = home_region
        if license_arn is not None:
            self._values["license_arn"] = license_arn
        if max_results is not None:
            self._values["max_results"] = max_results
        if next_token is not None:
            self._values["next_token"] = next_token
        if parent_arn is not None:
            self._values["parent_arn"] = parent_arn
        if principals is not None:
            self._values["principals"] = principals
        if source_version is not None:
            self._values["source_version"] = source_version
        if status is not None:
            self._values["status"] = status
        if status_reason is not None:
            self._values["status_reason"] = status_reason
        if tags is not None:
            self._values["tags"] = tags
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def allowed_operations(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::LicenseManager::Grant.AllowedOperations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-allowedoperations
        """
        result = self._values.get("allowed_operations")
        return result

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.ClientToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-clienttoken
        """
        result = self._values.get("client_token")
        return result

    @builtins.property
    def filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union[CfnGrant.FilterProperty, _IResolvable_6e2f5d88]]]]:
        """``AWS::LicenseManager::Grant.Filters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-filters
        """
        result = self._values.get("filters")
        return result

    @builtins.property
    def grant_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::LicenseManager::Grant.GrantArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantarns
        """
        result = self._values.get("grant_arns")
        return result

    @builtins.property
    def granted_operations(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::LicenseManager::Grant.GrantedOperations``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantedoperations
        """
        result = self._values.get("granted_operations")
        return result

    @builtins.property
    def grantee_principal_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.GranteePrincipalArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-granteeprincipalarn
        """
        result = self._values.get("grantee_principal_arn")
        return result

    @builtins.property
    def grant_name(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.GrantName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantname
        """
        result = self._values.get("grant_name")
        return result

    @builtins.property
    def grant_status(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.GrantStatus``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-grantstatus
        """
        result = self._values.get("grant_status")
        return result

    @builtins.property
    def home_region(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.HomeRegion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-homeregion
        """
        result = self._values.get("home_region")
        return result

    @builtins.property
    def license_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.LicenseArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-licensearn
        """
        result = self._values.get("license_arn")
        return result

    @builtins.property
    def max_results(self) -> typing.Optional[jsii.Number]:
        """``AWS::LicenseManager::Grant.MaxResults``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-maxresults
        """
        result = self._values.get("max_results")
        return result

    @builtins.property
    def next_token(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.NextToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-nexttoken
        """
        result = self._values.get("next_token")
        return result

    @builtins.property
    def parent_arn(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.ParentArn``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-parentarn
        """
        result = self._values.get("parent_arn")
        return result

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::LicenseManager::Grant.Principals``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-principals
        """
        result = self._values.get("principals")
        return result

    @builtins.property
    def source_version(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.SourceVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-sourceversion
        """
        result = self._values.get("source_version")
        return result

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-status
        """
        result = self._values.get("status")
        return result

    @builtins.property
    def status_reason(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.StatusReason``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-statusreason
        """
        result = self._values.get("status_reason")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_c592b05a]]:
        """``AWS::LicenseManager::Grant.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::Grant.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-grant.html#cfn-licensemanager-grant-version
        """
        result = self._values.get("version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGrantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_3eb0224c)
class CfnLicense(
    _CfnResource_f7d91f4b,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense",
):
    """A CloudFormation ``AWS::LicenseManager::License``.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html
    :cloudformationResource: AWS::LicenseManager::License
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        consumption_configuration: typing.Union["CfnLicense.ConsumptionConfigurationProperty", _IResolvable_6e2f5d88],
        entitlements: typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnLicense.EntitlementProperty", _IResolvable_6e2f5d88]]],
        home_region: builtins.str,
        issuer: typing.Union["CfnLicense.IssuerDataProperty", _IResolvable_6e2f5d88],
        validity: typing.Union["CfnLicense.ValidityDateFormatProperty", _IResolvable_6e2f5d88],
        beneficiary: typing.Optional[builtins.str] = None,
        client_token: typing.Optional[builtins.str] = None,
        filters: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnLicense.FilterProperty", _IResolvable_6e2f5d88]]]] = None,
        license_arns: typing.Optional[typing.List[builtins.str]] = None,
        license_metadata: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnLicense.MetadataProperty", _IResolvable_6e2f5d88]]]] = None,
        license_name: typing.Optional[builtins.str] = None,
        max_results: typing.Optional[jsii.Number] = None,
        next_token: typing.Optional[builtins.str] = None,
        product_name: typing.Optional[builtins.str] = None,
        product_sku: typing.Optional[builtins.str] = None,
        source_version: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """Create a new ``AWS::LicenseManager::License``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param consumption_configuration: ``AWS::LicenseManager::License.ConsumptionConfiguration``.
        :param entitlements: ``AWS::LicenseManager::License.Entitlements``.
        :param home_region: ``AWS::LicenseManager::License.HomeRegion``.
        :param issuer: ``AWS::LicenseManager::License.Issuer``.
        :param validity: ``AWS::LicenseManager::License.Validity``.
        :param beneficiary: ``AWS::LicenseManager::License.Beneficiary``.
        :param client_token: ``AWS::LicenseManager::License.ClientToken``.
        :param filters: ``AWS::LicenseManager::License.Filters``.
        :param license_arns: ``AWS::LicenseManager::License.LicenseArns``.
        :param license_metadata: ``AWS::LicenseManager::License.LicenseMetadata``.
        :param license_name: ``AWS::LicenseManager::License.LicenseName``.
        :param max_results: ``AWS::LicenseManager::License.MaxResults``.
        :param next_token: ``AWS::LicenseManager::License.NextToken``.
        :param product_name: ``AWS::LicenseManager::License.ProductName``.
        :param product_sku: ``AWS::LicenseManager::License.ProductSKU``.
        :param source_version: ``AWS::LicenseManager::License.SourceVersion``.
        :param status: ``AWS::LicenseManager::License.Status``.
        :param tags: ``AWS::LicenseManager::License.Tags``.
        :param version: ``AWS::LicenseManager::License.Version``.
        """
        props = CfnLicenseProps(
            consumption_configuration=consumption_configuration,
            entitlements=entitlements,
            home_region=home_region,
            issuer=issuer,
            validity=validity,
            beneficiary=beneficiary,
            client_token=client_token,
            filters=filters,
            license_arns=license_arns,
            license_metadata=license_metadata,
            license_name=license_name,
            max_results=max_results,
            next_token=next_token,
            product_name=product_name,
            product_sku=product_sku,
            source_version=source_version,
            status=status,
            tags=tags,
            version=version,
        )

        jsii.create(CfnLicense, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_afbbf916) -> None:
        """(experimental) Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty # type: ignore
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="attrLicenseArn")
    def attr_license_arn(self) -> builtins.str:
        """
        :cloudformationAttribute: LicenseArn
        """
        return jsii.get(self, "attrLicenseArn")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_6a5badd9:
        """``AWS::LicenseManager::License.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-tags
        """
        return jsii.get(self, "tags")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="consumptionConfiguration")
    def consumption_configuration(
        self,
    ) -> typing.Union["CfnLicense.ConsumptionConfigurationProperty", _IResolvable_6e2f5d88]:
        """``AWS::LicenseManager::License.ConsumptionConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-consumptionconfiguration
        """
        return jsii.get(self, "consumptionConfiguration")

    @consumption_configuration.setter # type: ignore
    def consumption_configuration(
        self,
        value: typing.Union["CfnLicense.ConsumptionConfigurationProperty", _IResolvable_6e2f5d88],
    ) -> None:
        jsii.set(self, "consumptionConfiguration", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="entitlements")
    def entitlements(
        self,
    ) -> typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnLicense.EntitlementProperty", _IResolvable_6e2f5d88]]]:
        """``AWS::LicenseManager::License.Entitlements``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-entitlements
        """
        return jsii.get(self, "entitlements")

    @entitlements.setter # type: ignore
    def entitlements(
        self,
        value: typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnLicense.EntitlementProperty", _IResolvable_6e2f5d88]]],
    ) -> None:
        jsii.set(self, "entitlements", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="homeRegion")
    def home_region(self) -> builtins.str:
        """``AWS::LicenseManager::License.HomeRegion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-homeregion
        """
        return jsii.get(self, "homeRegion")

    @home_region.setter # type: ignore
    def home_region(self, value: builtins.str) -> None:
        jsii.set(self, "homeRegion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="issuer")
    def issuer(
        self,
    ) -> typing.Union["CfnLicense.IssuerDataProperty", _IResolvable_6e2f5d88]:
        """``AWS::LicenseManager::License.Issuer``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-issuer
        """
        return jsii.get(self, "issuer")

    @issuer.setter # type: ignore
    def issuer(
        self,
        value: typing.Union["CfnLicense.IssuerDataProperty", _IResolvable_6e2f5d88],
    ) -> None:
        jsii.set(self, "issuer", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="validity")
    def validity(
        self,
    ) -> typing.Union["CfnLicense.ValidityDateFormatProperty", _IResolvable_6e2f5d88]:
        """``AWS::LicenseManager::License.Validity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-validity
        """
        return jsii.get(self, "validity")

    @validity.setter # type: ignore
    def validity(
        self,
        value: typing.Union["CfnLicense.ValidityDateFormatProperty", _IResolvable_6e2f5d88],
    ) -> None:
        jsii.set(self, "validity", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="beneficiary")
    def beneficiary(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.Beneficiary``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-beneficiary
        """
        return jsii.get(self, "beneficiary")

    @beneficiary.setter # type: ignore
    def beneficiary(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "beneficiary", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="clientToken")
    def client_token(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.ClientToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-clienttoken
        """
        return jsii.get(self, "clientToken")

    @client_token.setter # type: ignore
    def client_token(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "clientToken", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="filters")
    def filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnLicense.FilterProperty", _IResolvable_6e2f5d88]]]]:
        """``AWS::LicenseManager::License.Filters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-filters
        """
        return jsii.get(self, "filters")

    @filters.setter # type: ignore
    def filters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnLicense.FilterProperty", _IResolvable_6e2f5d88]]]],
    ) -> None:
        jsii.set(self, "filters", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="licenseArns")
    def license_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::LicenseManager::License.LicenseArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensearns
        """
        return jsii.get(self, "licenseArns")

    @license_arns.setter # type: ignore
    def license_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        jsii.set(self, "licenseArns", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="licenseMetadata")
    def license_metadata(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnLicense.MetadataProperty", _IResolvable_6e2f5d88]]]]:
        """``AWS::LicenseManager::License.LicenseMetadata``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensemetadata
        """
        return jsii.get(self, "licenseMetadata")

    @license_metadata.setter # type: ignore
    def license_metadata(
        self,
        value: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnLicense.MetadataProperty", _IResolvable_6e2f5d88]]]],
    ) -> None:
        jsii.set(self, "licenseMetadata", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="licenseName")
    def license_name(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.LicenseName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensename
        """
        return jsii.get(self, "licenseName")

    @license_name.setter # type: ignore
    def license_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "licenseName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="maxResults")
    def max_results(self) -> typing.Optional[jsii.Number]:
        """``AWS::LicenseManager::License.MaxResults``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-maxresults
        """
        return jsii.get(self, "maxResults")

    @max_results.setter # type: ignore
    def max_results(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxResults", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="nextToken")
    def next_token(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.NextToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-nexttoken
        """
        return jsii.get(self, "nextToken")

    @next_token.setter # type: ignore
    def next_token(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "nextToken", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="productName")
    def product_name(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.ProductName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productname
        """
        return jsii.get(self, "productName")

    @product_name.setter # type: ignore
    def product_name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "productName", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="productSku")
    def product_sku(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.ProductSKU``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productsku
        """
        return jsii.get(self, "productSku")

    @product_sku.setter # type: ignore
    def product_sku(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "productSku", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="sourceVersion")
    def source_version(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.SourceVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-sourceversion
        """
        return jsii.get(self, "sourceVersion")

    @source_version.setter # type: ignore
    def source_version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "sourceVersion", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-status
        """
        return jsii.get(self, "status")

    @status.setter # type: ignore
    def status(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "status", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-version
        """
        return jsii.get(self, "version")

    @version.setter # type: ignore
    def version(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense.BorrowConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "allow_early_check_in": "allowEarlyCheckIn",
            "max_time_to_live_in_minutes": "maxTimeToLiveInMinutes",
        },
    )
    class BorrowConfigurationProperty:
        def __init__(
            self,
            *,
            allow_early_check_in: typing.Union[builtins.bool, _IResolvable_6e2f5d88],
            max_time_to_live_in_minutes: jsii.Number,
        ) -> None:
            """
            :param allow_early_check_in: ``CfnLicense.BorrowConfigurationProperty.AllowEarlyCheckIn``.
            :param max_time_to_live_in_minutes: ``CfnLicense.BorrowConfigurationProperty.MaxTimeToLiveInMinutes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-borrowconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "allow_early_check_in": allow_early_check_in,
                "max_time_to_live_in_minutes": max_time_to_live_in_minutes,
            }

        @builtins.property
        def allow_early_check_in(
            self,
        ) -> typing.Union[builtins.bool, _IResolvable_6e2f5d88]:
            """``CfnLicense.BorrowConfigurationProperty.AllowEarlyCheckIn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-borrowconfiguration.html#cfn-licensemanager-license-borrowconfiguration-allowearlycheckin
            """
            result = self._values.get("allow_early_check_in")
            assert result is not None, "Required property 'allow_early_check_in' is missing"
            return result

        @builtins.property
        def max_time_to_live_in_minutes(self) -> jsii.Number:
            """``CfnLicense.BorrowConfigurationProperty.MaxTimeToLiveInMinutes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-borrowconfiguration.html#cfn-licensemanager-license-borrowconfiguration-maxtimetoliveinminutes
            """
            result = self._values.get("max_time_to_live_in_minutes")
            assert result is not None, "Required property 'max_time_to_live_in_minutes' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BorrowConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense.ConsumptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "borrow_configuration": "borrowConfiguration",
            "provisional_configuration": "provisionalConfiguration",
            "renew_type": "renewType",
        },
    )
    class ConsumptionConfigurationProperty:
        def __init__(
            self,
            *,
            borrow_configuration: typing.Optional[typing.Union["CfnLicense.BorrowConfigurationProperty", _IResolvable_6e2f5d88]] = None,
            provisional_configuration: typing.Optional[typing.Union["CfnLicense.ProvisionalConfigurationProperty", _IResolvable_6e2f5d88]] = None,
            renew_type: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param borrow_configuration: ``CfnLicense.ConsumptionConfigurationProperty.BorrowConfiguration``.
            :param provisional_configuration: ``CfnLicense.ConsumptionConfigurationProperty.ProvisionalConfiguration``.
            :param renew_type: ``CfnLicense.ConsumptionConfigurationProperty.RenewType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if borrow_configuration is not None:
                self._values["borrow_configuration"] = borrow_configuration
            if provisional_configuration is not None:
                self._values["provisional_configuration"] = provisional_configuration
            if renew_type is not None:
                self._values["renew_type"] = renew_type

        @builtins.property
        def borrow_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnLicense.BorrowConfigurationProperty", _IResolvable_6e2f5d88]]:
            """``CfnLicense.ConsumptionConfigurationProperty.BorrowConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html#cfn-licensemanager-license-consumptionconfiguration-borrowconfiguration
            """
            result = self._values.get("borrow_configuration")
            return result

        @builtins.property
        def provisional_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnLicense.ProvisionalConfigurationProperty", _IResolvable_6e2f5d88]]:
            """``CfnLicense.ConsumptionConfigurationProperty.ProvisionalConfiguration``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html#cfn-licensemanager-license-consumptionconfiguration-provisionalconfiguration
            """
            result = self._values.get("provisional_configuration")
            return result

        @builtins.property
        def renew_type(self) -> typing.Optional[builtins.str]:
            """``CfnLicense.ConsumptionConfigurationProperty.RenewType``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-consumptionconfiguration.html#cfn-licensemanager-license-consumptionconfiguration-renewtype
            """
            result = self._values.get("renew_type")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConsumptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense.EntitlementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "unit": "unit",
            "allow_check_in": "allowCheckIn",
            "checkout_rules": "checkoutRules",
            "max_count": "maxCount",
            "overage": "overage",
            "value": "value",
        },
    )
    class EntitlementProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            unit: builtins.str,
            allow_check_in: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
            checkout_rules: typing.Optional[typing.Union["CfnLicense.RuleListProperty", _IResolvable_6e2f5d88]] = None,
            max_count: typing.Optional[jsii.Number] = None,
            overage: typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param name: ``CfnLicense.EntitlementProperty.Name``.
            :param unit: ``CfnLicense.EntitlementProperty.Unit``.
            :param allow_check_in: ``CfnLicense.EntitlementProperty.AllowCheckIn``.
            :param checkout_rules: ``CfnLicense.EntitlementProperty.CheckoutRules``.
            :param max_count: ``CfnLicense.EntitlementProperty.MaxCount``.
            :param overage: ``CfnLicense.EntitlementProperty.Overage``.
            :param value: ``CfnLicense.EntitlementProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "unit": unit,
            }
            if allow_check_in is not None:
                self._values["allow_check_in"] = allow_check_in
            if checkout_rules is not None:
                self._values["checkout_rules"] = checkout_rules
            if max_count is not None:
                self._values["max_count"] = max_count
            if overage is not None:
                self._values["overage"] = overage
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnLicense.EntitlementProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def unit(self) -> builtins.str:
            """``CfnLicense.EntitlementProperty.Unit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-unit
            """
            result = self._values.get("unit")
            assert result is not None, "Required property 'unit' is missing"
            return result

        @builtins.property
        def allow_check_in(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
            """``CfnLicense.EntitlementProperty.AllowCheckIn``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-allowcheckin
            """
            result = self._values.get("allow_check_in")
            return result

        @builtins.property
        def checkout_rules(
            self,
        ) -> typing.Optional[typing.Union["CfnLicense.RuleListProperty", _IResolvable_6e2f5d88]]:
            """``CfnLicense.EntitlementProperty.CheckoutRules``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-checkoutrules
            """
            result = self._values.get("checkout_rules")
            return result

        @builtins.property
        def max_count(self) -> typing.Optional[jsii.Number]:
            """``CfnLicense.EntitlementProperty.MaxCount``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-maxcount
            """
            result = self._values.get("max_count")
            return result

        @builtins.property
        def overage(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_6e2f5d88]]:
            """``CfnLicense.EntitlementProperty.Overage``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-overage
            """
            result = self._values.get("overage")
            return result

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            """``CfnLicense.EntitlementProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-entitlement.html#cfn-licensemanager-license-entitlement-value
            """
            result = self._values.get("value")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EntitlementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "values": "values"},
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            values: typing.Union["CfnLicense.StringListProperty", _IResolvable_6e2f5d88],
        ) -> None:
            """
            :param name: ``CfnLicense.FilterProperty.Name``.
            :param values: ``CfnLicense.FilterProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-filter.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "values": values,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnLicense.FilterProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-filter.html#cfn-licensemanager-license-filter-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def values(
            self,
        ) -> typing.Union["CfnLicense.StringListProperty", _IResolvable_6e2f5d88]:
            """``CfnLicense.FilterProperty.Values``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-filter.html#cfn-licensemanager-license-filter-values
            """
            result = self._values.get("values")
            assert result is not None, "Required property 'values' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense.IssuerDataProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "sign_key": "signKey"},
    )
    class IssuerDataProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            sign_key: typing.Optional[builtins.str] = None,
        ) -> None:
            """
            :param name: ``CfnLicense.IssuerDataProperty.Name``.
            :param sign_key: ``CfnLicense.IssuerDataProperty.SignKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-issuerdata.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
            }
            if sign_key is not None:
                self._values["sign_key"] = sign_key

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnLicense.IssuerDataProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-issuerdata.html#cfn-licensemanager-license-issuerdata-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def sign_key(self) -> typing.Optional[builtins.str]:
            """``CfnLicense.IssuerDataProperty.SignKey``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-issuerdata.html#cfn-licensemanager-license-issuerdata-signkey
            """
            result = self._values.get("sign_key")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IssuerDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense.MetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class MetadataProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            """
            :param name: ``CfnLicense.MetadataProperty.Name``.
            :param value: ``CfnLicense.MetadataProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-metadata.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnLicense.MetadataProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-metadata.html#cfn-licensemanager-license-metadata-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnLicense.MetadataProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-metadata.html#cfn-licensemanager-license-metadata-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense.ProvisionalConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"max_time_to_live_in_minutes": "maxTimeToLiveInMinutes"},
    )
    class ProvisionalConfigurationProperty:
        def __init__(self, *, max_time_to_live_in_minutes: jsii.Number) -> None:
            """
            :param max_time_to_live_in_minutes: ``CfnLicense.ProvisionalConfigurationProperty.MaxTimeToLiveInMinutes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-provisionalconfiguration.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "max_time_to_live_in_minutes": max_time_to_live_in_minutes,
            }

        @builtins.property
        def max_time_to_live_in_minutes(self) -> jsii.Number:
            """``CfnLicense.ProvisionalConfigurationProperty.MaxTimeToLiveInMinutes``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-provisionalconfiguration.html#cfn-licensemanager-license-provisionalconfiguration-maxtimetoliveinminutes
            """
            result = self._values.get("max_time_to_live_in_minutes")
            assert result is not None, "Required property 'max_time_to_live_in_minutes' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProvisionalConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense.RuleListProperty",
        jsii_struct_bases=[],
        name_mapping={"rule_list": "ruleList"},
    )
    class RuleListProperty:
        def __init__(
            self,
            *,
            rule_list: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnLicense.RuleProperty", _IResolvable_6e2f5d88]]]] = None,
        ) -> None:
            """
            :param rule_list: ``CfnLicense.RuleListProperty.RuleList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-rulelist.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if rule_list is not None:
                self._values["rule_list"] = rule_list

        @builtins.property
        def rule_list(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union["CfnLicense.RuleProperty", _IResolvable_6e2f5d88]]]]:
            """``CfnLicense.RuleListProperty.RuleList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-rulelist.html#cfn-licensemanager-license-rulelist-rulelist
            """
            result = self._values.get("rule_list")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "unit": "unit", "value": "value"},
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            unit: builtins.str,
            value: builtins.str,
        ) -> None:
            """
            :param name: ``CfnLicense.RuleProperty.Name``.
            :param unit: ``CfnLicense.RuleProperty.Unit``.
            :param value: ``CfnLicense.RuleProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-rule.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "name": name,
                "unit": unit,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            """``CfnLicense.RuleProperty.Name``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-rule.html#cfn-licensemanager-license-rule-name
            """
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return result

        @builtins.property
        def unit(self) -> builtins.str:
            """``CfnLicense.RuleProperty.Unit``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-rule.html#cfn-licensemanager-license-rule-unit
            """
            result = self._values.get("unit")
            assert result is not None, "Required property 'unit' is missing"
            return result

        @builtins.property
        def value(self) -> builtins.str:
            """``CfnLicense.RuleProperty.Value``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-rule.html#cfn-licensemanager-license-rule-value
            """
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense.StringListProperty",
        jsii_struct_bases=[],
        name_mapping={"string_list": "stringList"},
    )
    class StringListProperty:
        def __init__(
            self,
            *,
            string_list: typing.Optional[typing.List[builtins.str]] = None,
        ) -> None:
            """
            :param string_list: ``CfnLicense.StringListProperty.StringList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-stringlist.html
            """
            self._values: typing.Dict[str, typing.Any] = {}
            if string_list is not None:
                self._values["string_list"] = string_list

        @builtins.property
        def string_list(self) -> typing.Optional[typing.List[builtins.str]]:
            """``CfnLicense.StringListProperty.StringList``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-stringlist.html#cfn-licensemanager-license-stringlist-stringlist
            """
            result = self._values.get("string_list")
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StringListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicense.ValidityDateFormatProperty",
        jsii_struct_bases=[],
        name_mapping={"begin": "begin", "end": "end"},
    )
    class ValidityDateFormatProperty:
        def __init__(self, *, begin: builtins.str, end: builtins.str) -> None:
            """
            :param begin: ``CfnLicense.ValidityDateFormatProperty.Begin``.
            :param end: ``CfnLicense.ValidityDateFormatProperty.End``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-validitydateformat.html
            """
            self._values: typing.Dict[str, typing.Any] = {
                "begin": begin,
                "end": end,
            }

        @builtins.property
        def begin(self) -> builtins.str:
            """``CfnLicense.ValidityDateFormatProperty.Begin``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-validitydateformat.html#cfn-licensemanager-license-validitydateformat-begin
            """
            result = self._values.get("begin")
            assert result is not None, "Required property 'begin' is missing"
            return result

        @builtins.property
        def end(self) -> builtins.str:
            """``CfnLicense.ValidityDateFormatProperty.End``.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanager-license-validitydateformat.html#cfn-licensemanager-license-validitydateformat-end
            """
            result = self._values.get("end")
            assert result is not None, "Required property 'end' is missing"
            return result

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidityDateFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_licensemanager.CfnLicenseProps",
    jsii_struct_bases=[],
    name_mapping={
        "consumption_configuration": "consumptionConfiguration",
        "entitlements": "entitlements",
        "home_region": "homeRegion",
        "issuer": "issuer",
        "validity": "validity",
        "beneficiary": "beneficiary",
        "client_token": "clientToken",
        "filters": "filters",
        "license_arns": "licenseArns",
        "license_metadata": "licenseMetadata",
        "license_name": "licenseName",
        "max_results": "maxResults",
        "next_token": "nextToken",
        "product_name": "productName",
        "product_sku": "productSku",
        "source_version": "sourceVersion",
        "status": "status",
        "tags": "tags",
        "version": "version",
    },
)
class CfnLicenseProps:
    def __init__(
        self,
        *,
        consumption_configuration: typing.Union[CfnLicense.ConsumptionConfigurationProperty, _IResolvable_6e2f5d88],
        entitlements: typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union[CfnLicense.EntitlementProperty, _IResolvable_6e2f5d88]]],
        home_region: builtins.str,
        issuer: typing.Union[CfnLicense.IssuerDataProperty, _IResolvable_6e2f5d88],
        validity: typing.Union[CfnLicense.ValidityDateFormatProperty, _IResolvable_6e2f5d88],
        beneficiary: typing.Optional[builtins.str] = None,
        client_token: typing.Optional[builtins.str] = None,
        filters: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union[CfnLicense.FilterProperty, _IResolvable_6e2f5d88]]]] = None,
        license_arns: typing.Optional[typing.List[builtins.str]] = None,
        license_metadata: typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union[CfnLicense.MetadataProperty, _IResolvable_6e2f5d88]]]] = None,
        license_name: typing.Optional[builtins.str] = None,
        max_results: typing.Optional[jsii.Number] = None,
        next_token: typing.Optional[builtins.str] = None,
        product_name: typing.Optional[builtins.str] = None,
        product_sku: typing.Optional[builtins.str] = None,
        source_version: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.List[_CfnTag_c592b05a]] = None,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        """Properties for defining a ``AWS::LicenseManager::License``.

        :param consumption_configuration: ``AWS::LicenseManager::License.ConsumptionConfiguration``.
        :param entitlements: ``AWS::LicenseManager::License.Entitlements``.
        :param home_region: ``AWS::LicenseManager::License.HomeRegion``.
        :param issuer: ``AWS::LicenseManager::License.Issuer``.
        :param validity: ``AWS::LicenseManager::License.Validity``.
        :param beneficiary: ``AWS::LicenseManager::License.Beneficiary``.
        :param client_token: ``AWS::LicenseManager::License.ClientToken``.
        :param filters: ``AWS::LicenseManager::License.Filters``.
        :param license_arns: ``AWS::LicenseManager::License.LicenseArns``.
        :param license_metadata: ``AWS::LicenseManager::License.LicenseMetadata``.
        :param license_name: ``AWS::LicenseManager::License.LicenseName``.
        :param max_results: ``AWS::LicenseManager::License.MaxResults``.
        :param next_token: ``AWS::LicenseManager::License.NextToken``.
        :param product_name: ``AWS::LicenseManager::License.ProductName``.
        :param product_sku: ``AWS::LicenseManager::License.ProductSKU``.
        :param source_version: ``AWS::LicenseManager::License.SourceVersion``.
        :param status: ``AWS::LicenseManager::License.Status``.
        :param tags: ``AWS::LicenseManager::License.Tags``.
        :param version: ``AWS::LicenseManager::License.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html
        """
        self._values: typing.Dict[str, typing.Any] = {
            "consumption_configuration": consumption_configuration,
            "entitlements": entitlements,
            "home_region": home_region,
            "issuer": issuer,
            "validity": validity,
        }
        if beneficiary is not None:
            self._values["beneficiary"] = beneficiary
        if client_token is not None:
            self._values["client_token"] = client_token
        if filters is not None:
            self._values["filters"] = filters
        if license_arns is not None:
            self._values["license_arns"] = license_arns
        if license_metadata is not None:
            self._values["license_metadata"] = license_metadata
        if license_name is not None:
            self._values["license_name"] = license_name
        if max_results is not None:
            self._values["max_results"] = max_results
        if next_token is not None:
            self._values["next_token"] = next_token
        if product_name is not None:
            self._values["product_name"] = product_name
        if product_sku is not None:
            self._values["product_sku"] = product_sku
        if source_version is not None:
            self._values["source_version"] = source_version
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def consumption_configuration(
        self,
    ) -> typing.Union[CfnLicense.ConsumptionConfigurationProperty, _IResolvable_6e2f5d88]:
        """``AWS::LicenseManager::License.ConsumptionConfiguration``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-consumptionconfiguration
        """
        result = self._values.get("consumption_configuration")
        assert result is not None, "Required property 'consumption_configuration' is missing"
        return result

    @builtins.property
    def entitlements(
        self,
    ) -> typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union[CfnLicense.EntitlementProperty, _IResolvable_6e2f5d88]]]:
        """``AWS::LicenseManager::License.Entitlements``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-entitlements
        """
        result = self._values.get("entitlements")
        assert result is not None, "Required property 'entitlements' is missing"
        return result

    @builtins.property
    def home_region(self) -> builtins.str:
        """``AWS::LicenseManager::License.HomeRegion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-homeregion
        """
        result = self._values.get("home_region")
        assert result is not None, "Required property 'home_region' is missing"
        return result

    @builtins.property
    def issuer(
        self,
    ) -> typing.Union[CfnLicense.IssuerDataProperty, _IResolvable_6e2f5d88]:
        """``AWS::LicenseManager::License.Issuer``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-issuer
        """
        result = self._values.get("issuer")
        assert result is not None, "Required property 'issuer' is missing"
        return result

    @builtins.property
    def validity(
        self,
    ) -> typing.Union[CfnLicense.ValidityDateFormatProperty, _IResolvable_6e2f5d88]:
        """``AWS::LicenseManager::License.Validity``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-validity
        """
        result = self._values.get("validity")
        assert result is not None, "Required property 'validity' is missing"
        return result

    @builtins.property
    def beneficiary(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.Beneficiary``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-beneficiary
        """
        result = self._values.get("beneficiary")
        return result

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.ClientToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-clienttoken
        """
        result = self._values.get("client_token")
        return result

    @builtins.property
    def filters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union[CfnLicense.FilterProperty, _IResolvable_6e2f5d88]]]]:
        """``AWS::LicenseManager::License.Filters``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-filters
        """
        result = self._values.get("filters")
        return result

    @builtins.property
    def license_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        """``AWS::LicenseManager::License.LicenseArns``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensearns
        """
        result = self._values.get("license_arns")
        return result

    @builtins.property
    def license_metadata(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_6e2f5d88, typing.List[typing.Union[CfnLicense.MetadataProperty, _IResolvable_6e2f5d88]]]]:
        """``AWS::LicenseManager::License.LicenseMetadata``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensemetadata
        """
        result = self._values.get("license_metadata")
        return result

    @builtins.property
    def license_name(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.LicenseName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-licensename
        """
        result = self._values.get("license_name")
        return result

    @builtins.property
    def max_results(self) -> typing.Optional[jsii.Number]:
        """``AWS::LicenseManager::License.MaxResults``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-maxresults
        """
        result = self._values.get("max_results")
        return result

    @builtins.property
    def next_token(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.NextToken``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-nexttoken
        """
        result = self._values.get("next_token")
        return result

    @builtins.property
    def product_name(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.ProductName``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productname
        """
        result = self._values.get("product_name")
        return result

    @builtins.property
    def product_sku(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.ProductSKU``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-productsku
        """
        result = self._values.get("product_sku")
        return result

    @builtins.property
    def source_version(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.SourceVersion``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-sourceversion
        """
        result = self._values.get("source_version")
        return result

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.Status``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-status
        """
        result = self._values.get("status")
        return result

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_c592b05a]]:
        """``AWS::LicenseManager::License.Tags``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-tags
        """
        result = self._values.get("tags")
        return result

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        """``AWS::LicenseManager::License.Version``.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanager-license.html#cfn-licensemanager-license-version
        """
        result = self._values.get("version")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLicenseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnGrant",
    "CfnGrantProps",
    "CfnLicense",
    "CfnLicenseProps",
]

publication.publish()
