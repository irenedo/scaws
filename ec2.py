# -*- coding: utf-8 -*-
import boto3 as aws

"""
EC2 related functions
"""


def open_client():
    return aws.client('ec2')


def list_instances(ec2):
    reservations = ec2.describe_instances()

    inst = [res['Instances'][0] for res in reservations['Reservations']]

    return inst


def start_instance(ec2, instid):

    ret = ec2.start_instances(InstanceIds = [instid])

    return ret


def stop_instance(ec2, instid):

    ret = ec2.stop_instances(InstanceIds = [instid])

    return ret


def get_instance(ec2, instid):
    ret = ec2.describe_instances(InstanceIds = [instid])

    return ret['Reservations'][0]['Instances'][0]