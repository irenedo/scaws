# scaws
Simple Console for AWS: Text based console for AWS. This is a personal project for python and AWS learning and not developed for production environments.

Dependencies:
	- python3 
	- boto3
	- urwid

Boto3 configuration:

	* Create a new file under home directory named .aws/credentials
	* Create a new default profile using credentials generated from IAM

		[default]
		aws_access_key_id = YOUR_ACCESS_KEY
		aws_secret_access_key = YOUR_SECRET_KEY
		region=PREFERRED_REGION

Right now scaws only works with an unique region, so the last line it's required

