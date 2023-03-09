import os

import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_certificatemanager as acm,
    aws_route53 as r53,
    aws_route53_targets as targets,
    aws_cloudfront as cfront,
    aws_cloudfront_origins as origins,
)
from constructs import Construct

HOSTED_ZONE_ID   = os.environ['hosted_zone_id']
HOSTED_ZONE_NAME = os.environ['hosted_zone_name']
DOMAIN_NAME      = os.environ['domain_name']

class WackoToolsInfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Import R53 Hosted Zone
        hosted_zone = r53.HostedZone.from_hosted_zone_attributes(self, "HostedZone",
                                                                 hosted_zone_id=HOSTED_ZONE_ID,
                                                                 zone_name=HOSTED_ZONE_NAME)

        # S3 bucket to host the static website content
        bucket = s3.Bucket(self, DOMAIN_NAME,
                           block_public_access=s3.BlockPublicAccess.BLOCK_ALL, 
                           versioned=True,
                           removal_policy=cdk.RemovalPolicy.DESTROY,
                           auto_delete_objects=True)
        
        # ACM Certificate for SSL on CloudFront
        # certificate = acm.Certificate(self, "SiteCertificate",
        #                               domain_name=DOMAIN_NAME,
        #                               validation=acm.CertificateValidation.from_dns(hosted_zone))

        # Deprecated method, using this because it supports creating cross-region certificates
        # https://github.com/aws/aws-cdk/issues/9274
        # Cert must be deployed in "us-east-1" as CloudFront resource requires cert to be here.
        certificate = acm.DnsValidatedCertificate(self, "SiteCertificate",
                                                  domain_name=DOMAIN_NAME,
                                                  hosted_zone=hosted_zone,
                                                  validation=acm.CertificateValidation.from_dns(hosted_zone),
                                                  region="us-east-1")


        # CloudFront Distribution
        distribution = cfront.Distribution(self, "Distribution",
                                           default_behavior=cfront.BehaviorOptions(
                                                origin=origins.S3Origin(bucket),
                                                compress=True,
                                                viewer_protocol_policy=cfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                allowed_methods=cfront.AllowedMethods.ALLOW_GET_HEAD,
                                                cache_policy=cfront.CachePolicy.CACHING_OPTIMIZED),
                                            certificate=certificate,
                                            domain_names=[DOMAIN_NAME],
                                            default_root_object="index.html")

        # Alias Record 
        record = r53.ARecord(self, "AliasRecord",
                             zone=hosted_zone,
                             record_name=DOMAIN_NAME,
                             target=r53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)))
