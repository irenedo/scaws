# -*- coding: utf-8 -*-
import os
import urwid
import boto3 as aws

"""
EC2 related functions
"""


def list_instances():

    ec2 = aws.client('ec2')
    reservations = ec2.describe_instances()

    inst = [res['Instances'][0] for res in reservations['Reservations']]

    return inst



