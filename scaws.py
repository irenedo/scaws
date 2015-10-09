#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
scaws (Simple Console for AWS) is, as the names says, a text based console for AWS
"""

import boto3
import sys, os


__author__ = "Iván Renedo"
__copyright__ = "GPL"


# aws_services is used for list supported aws services by scaws
aws_services = (('EC2', 'Elastic Cloud Computing'), ('S3', 'Simple Storage Service'))


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
        for service in services:
            print("[{0}] {1} - {2}".format(option, service[0], service[1]))
            rightoptions.append(option)
            option += 1

        print("\n[0] Exit")
        chosen = input('\nChose Option->')
        if chosen in rightoptions:
            break

    return chosen

def ec2():
    """
    Draws the EC2 menu
    """
    print('ec2')
    return 0

def s3():
    """
    Draws the s3 menu
    """
    return 0

while True:
    service = main_menu(aws_services)

    if service == 0:
        sys.exit(0)
    if service == 1:
        ec2()
    if service == 2:
        s3()

