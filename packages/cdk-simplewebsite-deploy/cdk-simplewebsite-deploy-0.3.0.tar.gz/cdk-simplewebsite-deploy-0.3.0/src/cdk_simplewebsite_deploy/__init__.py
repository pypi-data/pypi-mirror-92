"""
[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)
![Build](https://github.com/SnapPetal/cdk-simplewebsite-deploy/workflows/Build/badge.svg)
![Release](https://github.com/SnapPetal/cdk-simplewebsite-deploy/workflows/Release/badge.svg?branch=main)

# cdk-simplewebsite-deploy

This is an AWS CDK Construct to simplify deploying a single-page website use CloudFront distributions.

## Installation and Usage

```console
npm i cdk-simplewebsite-deploy
```

### [CreateBasicSite](https://github.com/snappetal/cdk-simplewebsite-deploy/blob/main/API.md#cdk-cloudfront-deploy-createbasicsite)

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_simplewebsite_deploy import CreateBasicSite

class PipelineStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        CreateBasicSite(stack, "test-website",
            website_folder="./src/build",
            index_doc="index.html",
            hosted_zone="example.com",
            sub_domain="www.example.com"
        )
```

### [CreateCloudfrontSite](https://github.com/snappetal/cdk-simplewebsite-deploy/blob/main/API.md#cdk-cloudfront-deploy-createcloudfrontsite)

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.core as cdk
from cdk_simplewebsite_deploy import CreateCloudfrontSite

class PipelineStack(cdk.Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        CreateCloudfrontSite(stack, "test-website",
            website_folder="./src/dist",
            index_doc="index.html",
            hosted_zone="example.com",
            sub_domain="www.example.com"
        )
```

## License

Distributed under the [Apache-2.0](./LICENSE) license.
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

import aws_cdk.aws_cloudfront
import aws_cdk.core


class CreateBasicSite(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-simplewebsite-deploy.CreateBasicSite",
):
    """
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        hosted_zone: builtins.str,
        index_doc: builtins.str,
        website_folder: builtins.str,
        error_doc: typing.Optional[builtins.str] = None,
        price_class: typing.Optional[aws_cdk.aws_cloudfront.PriceClass] = None,
        sub_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param hosted_zone: (experimental) Hosted Zone used to create the DNS record for the website.
        :param index_doc: (experimental) The index document of the website.
        :param website_folder: (experimental) Local path to the website folder you want to deploy on S3.
        :param error_doc: (experimental) The error document of the website. Default: - No error document.
        :param price_class: (experimental) The price class determines how many edge locations CloudFront will use for your distribution. Default: PriceClass.PRICE_CLASS_100.
        :param sub_domain: (experimental) The sub-domain name you want to deploy. Default: www e.g. www.example.com.

        :stability: experimental
        """
        props = SimpleWebsiteConfiguration(
            hosted_zone=hosted_zone,
            index_doc=index_doc,
            website_folder=website_folder,
            error_doc=error_doc,
            price_class=price_class,
            sub_domain=sub_domain,
        )

        jsii.create(CreateBasicSite, self, [scope, id, props])


class CreateCloudfrontSite(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-simplewebsite-deploy.CreateCloudfrontSite",
):
    """
    :stability: experimental
    """

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        hosted_zone: builtins.str,
        index_doc: builtins.str,
        website_folder: builtins.str,
        error_doc: typing.Optional[builtins.str] = None,
        price_class: typing.Optional[aws_cdk.aws_cloudfront.PriceClass] = None,
        sub_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param hosted_zone: (experimental) Hosted Zone used to create the DNS record for the website.
        :param index_doc: (experimental) The index document of the website.
        :param website_folder: (experimental) Local path to the website folder you want to deploy on S3.
        :param error_doc: (experimental) The error document of the website. Default: - No error document.
        :param price_class: (experimental) The price class determines how many edge locations CloudFront will use for your distribution. Default: PriceClass.PRICE_CLASS_100.
        :param sub_domain: (experimental) The sub-domain name you want to deploy. Default: www e.g. www.example.com.

        :stability: experimental
        """
        props = SimpleWebsiteConfiguration(
            hosted_zone=hosted_zone,
            index_doc=index_doc,
            website_folder=website_folder,
            error_doc=error_doc,
            price_class=price_class,
            sub_domain=sub_domain,
        )

        jsii.create(CreateCloudfrontSite, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cdk-simplewebsite-deploy.SimpleWebsiteConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "hosted_zone": "hostedZone",
        "index_doc": "indexDoc",
        "website_folder": "websiteFolder",
        "error_doc": "errorDoc",
        "price_class": "priceClass",
        "sub_domain": "subDomain",
    },
)
class SimpleWebsiteConfiguration:
    def __init__(
        self,
        *,
        hosted_zone: builtins.str,
        index_doc: builtins.str,
        website_folder: builtins.str,
        error_doc: typing.Optional[builtins.str] = None,
        price_class: typing.Optional[aws_cdk.aws_cloudfront.PriceClass] = None,
        sub_domain: typing.Optional[builtins.str] = None,
    ) -> None:
        """
        :param hosted_zone: (experimental) Hosted Zone used to create the DNS record for the website.
        :param index_doc: (experimental) The index document of the website.
        :param website_folder: (experimental) Local path to the website folder you want to deploy on S3.
        :param error_doc: (experimental) The error document of the website. Default: - No error document.
        :param price_class: (experimental) The price class determines how many edge locations CloudFront will use for your distribution. Default: PriceClass.PRICE_CLASS_100.
        :param sub_domain: (experimental) The sub-domain name you want to deploy. Default: www e.g. www.example.com.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "hosted_zone": hosted_zone,
            "index_doc": index_doc,
            "website_folder": website_folder,
        }
        if error_doc is not None:
            self._values["error_doc"] = error_doc
        if price_class is not None:
            self._values["price_class"] = price_class
        if sub_domain is not None:
            self._values["sub_domain"] = sub_domain

    @builtins.property
    def hosted_zone(self) -> builtins.str:
        """(experimental) Hosted Zone used to create the DNS record for the website.

        :stability: experimental
        """
        result = self._values.get("hosted_zone")
        assert result is not None, "Required property 'hosted_zone' is missing"
        return result

    @builtins.property
    def index_doc(self) -> builtins.str:
        """(experimental) The index document of the website.

        :stability: experimental
        """
        result = self._values.get("index_doc")
        assert result is not None, "Required property 'index_doc' is missing"
        return result

    @builtins.property
    def website_folder(self) -> builtins.str:
        """(experimental) Local path to the website folder you want to deploy on S3.

        :stability: experimental
        """
        result = self._values.get("website_folder")
        assert result is not None, "Required property 'website_folder' is missing"
        return result

    @builtins.property
    def error_doc(self) -> typing.Optional[builtins.str]:
        """(experimental) The error document of the website.

        :default: - No error document.

        :stability: experimental
        """
        result = self._values.get("error_doc")
        return result

    @builtins.property
    def price_class(self) -> typing.Optional[aws_cdk.aws_cloudfront.PriceClass]:
        """(experimental) The price class determines how many edge locations CloudFront will use for your distribution.

        :default: PriceClass.PRICE_CLASS_100.

        :see: https://aws.amazon.com/cloudfront/pricing/.
        :stability: experimental
        """
        result = self._values.get("price_class")
        return result

    @builtins.property
    def sub_domain(self) -> typing.Optional[builtins.str]:
        """(experimental) The sub-domain name you want to deploy.

        :default: www  e.g. www.example.com.

        :stability: experimental
        """
        result = self._values.get("sub_domain")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SimpleWebsiteConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CreateBasicSite",
    "CreateCloudfrontSite",
    "SimpleWebsiteConfiguration",
]

publication.publish()
