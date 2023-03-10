
# Wacko's Tools Website Infrastructure

This is a CDK Infrastructure to create a static website using S3 and CloudFront to serve the website.

## Architecture
![](https://raw.githubusercontent.com/SabeerBakir/wacko-tools-infra/ef3621fd04cc523056e01b62ff288615731b6a5b/S3_Static_Hosted_Site.svg)

## CDK Project Instructions

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

Set Environment Variables:
```bash
# Domain name (website name)
domain_name="<domain_name>"

# Hosted Zone ID 
# https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-working-with.html
hosted_zone_id="<hosted_zone_id>"

# Hosted Zone Name
hosted_zone_name="<hosted_zone_name>"
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
