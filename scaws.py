#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scaws (Simple Console for AWS) is, as the names says, a text based console for AWS
"""

import boto3
import sys
import os



__author__ = "Iván Renedo"
__copyright__ = "GPL"


# aws_services is used for list supported aws services and options by scaws
aws_services = (
    ('EC2 - Elastic Cloud Computing',
         ('Instances',
            ('List Instances',
             'Stop Instances',
             'Start Instances',
            ),
          'Images',
          'EBS - Elastic Block Store',
          'Network And Security',
          'Load Balancing',
          'Auto Scaling')),
    ('S3 - Simple Storage Service',))


def main_menu(services):
    """
    Draws the main menu
    """
    while True:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        rightoptions = [0]
        title = 'AWS Services'
        tab = "         "
        print(tab + '-' * len(title))
        print(tab + title)
        print(tab + '-' * len(title))
        option = 1
        for ser in services:
            print("[{0}] {1}".format(option, ser[0]))
            rightoptions.append(option)
            option += 1

        print("\n[0] Exit")
        chosen = input('\nChose Option->')
        # check for a correct option
        if chosen in rightoptions:
            break

    return chosen

def ec2_menu(elem):
    """
    Draws the ec2 menu
    """
    while True:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

        rightoptions = [0]
        title = 'EC2 Services'
        tab = "         "
        print(tab + '-' * len(title))
        print(tab + title)
        print(tab + '-' * len(title))
        option = 1
        for ser in elem[1]:
            print("[{0}] {1}".format(option, ser))
            rightoptions.append(option)
            option += 1

        print("\n[0] Back")
        chosen = input('\nChose Option->')
        # check for a correct option
        if chosen in rightoptions:
            break

    return chosen

def ec2(elements):
    """
    Draws the EC2 menu
    """
    ec2_menu(elements)
    if service == 0:
        return 0
    if service == 1:
        print("servicio de EC2")
    return 0

def s3(elements):
    """
    Draws the s3 menu
    """
    return 0

while True:
    service = main_menu(aws_services)

    if service == 0:
        sys.exit(0)
    if service == 1:
        ec2(aws_services[0])
    if service == 2:
        s3(aws_services[1])

