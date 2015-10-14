# -*- coding: utf-8 -*-
import os
import boto3 as aws

"""
EC2 related functions
"""


def instances():
    """
    Instances Menu
    """

    while True:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        tab = "         "

        title = "[[  Instances  ]]"
        print(tab + '-' * len(title))
        print(tab + title)
        print(tab + '-' * len(title))
        print("")
        print("[1] :: List Instances")

        print("\n[0] Back")

        # check for a correct option
        try:
            chosen = input('\nChose Option->')
            # check for a correct option
            if chosen in range(2):
                if chosen == 0:
                    break
                elif chosen == 1:
                    list_instances()
        except SyntaxError:
            # non common characters  -> redraw menu
            pass
        except NameError:
            # non numerical option -> redraw menu
            pass
    return 0


def list_instances():
    """
    List instances in aws account
    :return: nothing
    """
    ec2 = aws.client('ec2')
    reservations = ec2.describe_instances()
    inst = [res['Instances'][0] for res in reservations['Reservations']]
    for inst in inst:
        print("InstanceId : {0}".format(inst['InstanceId']))
    wait = input("Press any key to continue")