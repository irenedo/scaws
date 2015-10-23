#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scaws (Simple Console for AWS) is a text based console for AWS
"""


import pdb
import os
import ec2
import urwid
import termios
import sys


__author__ = "Iván Renedo"
__copyright__ = "GPL"


def getch():
    old_settings = termios.tcgetattr(0)
    new_settings = old_settings[:]
    new_settings[3] &= ~termios.ICANON
    try:
        termios.tcsetattr(0, termios.TCSANOW, new_settings)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(0, termios.TCSANOW, old_settings)
    return ch


class Menu:
    header = None
    body = None
    footer = None
    old_menu = list()


def footer_instance(started):
    if started:
            option1 = urwid.Text(u'(T): Stop Instance')
    else:
            option1 = urwid.Text(u'(S): Start Instance')
    option2 = urwid.Text(u'(Q): Quit')
    row1 = urwid.Pile([option1,option2])

    option3 = urwid.Text(u'(G): Security Groups')
    option4 = urwid.Text(u'(B): Previous menu')

    row2 = urwid.Pile([option3, option4])

    option5 = urwid.Text(u'(t): List Tags')
    option6 = urwid.Text(u'(R): Refresh Instance')

    row3 = urwid.Pile([option5, option6])
    footer = urwid.Columns([(25, row1), (25, row2), (25, row3)], min_width=30)

    footer = urwid.Pile([footer, urwid.Text(('bold result', u'Spacebar to continue'), align='center')])

    return footer


def draw_menu(m):
    body = list()
    for x in m.body:
        button = urwid.Button(x[0])
        if x[0] == 'Back' or x[0] == 'Exit':
            body.append(urwid.Divider())
        urwid.connect_signal(button, 'click', x[1])
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    main_loop.widget.body = urwid.LineBox(urwid.Overlay(urwid.ListBox(urwid.SimpleFocusListWalker(body)),
                                          urwid.SolidFill(u' '), align='center', width=('relative', 50),
                                          valign='middle', height=('relative', 50),))
    main_loop.widget.footer = urwid.Text(m.footer)
    main_loop.widget.header = urwid.AttrMap(urwid.Text(m.header, align='center'), 'titlebar')
    main_loop.draw_screen()


def draw_result(men):
    main_loop.widget.header = urwid.AttrMap(urwid.Text(men.header, align='center'), 'titlebar')
    main_loop.widget.body = urwid.LineBox(urwid.Overlay(urwid.Filler(men.body, 'top'),
                                                        urwid.SolidFill(u' '), align='center',
                                          width=('relative', 100), valign='top', height=('relative', 100)))
    main_loop.widget.footer = men.footer
    main_loop.draw_screen()


def goback(m):

    if not m.old_menu:
        exit_program(None)
    else:
        menu.header = m.old_menu[-1][0]
        menu.body = m.old_menu[-1][1]
        menu.footer = m.old_menu[-1][2]
        del menu.old_menu[-1]
        draw_menu(menu)


def menu_back(nil):
    goback(menu)


def draw_instance_in_menu(inst):
    unavailable = False
    row_width = 15
    started = False
    if inst['State']['Name'] == 'running':
        color = 'started'
        started = True
    elif inst['State']['Name'] == 'stopped':
        color = 'stopped'
        started = False
    else:
        color = 'pending'
        unavailable = True

    status = inst['State']['Name'].title()
    first_screen =[
            ('reversed', u'Instance'),  u'\n',
            ('bold result', u'Instance ID: '), inst['InstanceId'], u'\n',
            ('bold result', u'Instance Status: '), (color, status), u'\n',
            ('bold result', u'Public DNS: '), inst['PublicDnsName'], u'\n',
            ('bold result', u'Private Address: '), inst['PrivateIpAddress'], u'\n',
            ('bold result', u'Private DNS: '), inst['PrivateDnsName'], u'\n',
            ('bold result', u'Availability Zone: '), inst['Placement']['AvailabilityZone'], u'\n',
            ('bold result', u'VPC ID: '), inst['VpcId'], u'\n',
            ('bold result', u'Subnet ID: '), inst['SubnetId'], u'\n',
            ('bold result', u'Instance Type: '), inst['InstanceType'], u'\n',
            ('bold result', u'Image Id: '), inst['ImageId'], u'\n',
            ('bold result', u'IArchitecture '), inst['Architecture'], u'\n',
            ('bold result', u'Root Device Type: '), inst['RootDeviceType'], u'\n',
            ('bold result', u'EBS Optimized: '), str(inst['EbsOptimized']), u'\n',
            ('bold result', u'Key Name: '), inst['KeyName'],
    ]

    first_screen = urwid.Text(first_screen)

    second_screen = list()

    security_groups = list()
    security_groups.append([('reversed', u'Security Groups '), u'\n'])
    security_groups.append([('bold result', u'Group ID       '), ('bold result', u'Name'), u'\n'])
    for sg in inst['SecurityGroups']:
        chars = row_width - len(sg['GroupId'])
        wl = ' ' * chars
        security_groups.append([sg['GroupId'], wl, sg['GroupName'], u'\n'])
    second_screen.append((35, urwid.LineBox(urwid.Text(security_groups))))

    tags = list()
    tags.append([('reversed', u'Tags '), u'\n'])
    tags.append([('bold result', u'Name           '), ('bold result', u'Value'), u'\n'])
    for tag in inst['Tags']:
        chars = row_width - len(tag['Key'])
        wl = ' ' * chars
        tags.append([tag['Key'], wl, tag['Value'], u'\n'])
    second_screen.append((35, urwid.LineBox(urwid.Text(tags))))

    devices = list()
    devices.append([('reversed', u'Block Device Mappings '), u'\n'])
    for dev in inst['BlockDeviceMappings']:
        devices.append([('small title', dev['DeviceName']), u'\n'])
        devices.append([('bold result', u'Delete On Term: '), str(dev['Ebs']['DeleteOnTermination']), u'\n'])
        devices.append([('bold result', u'Volume ID: '), dev['Ebs']['VolumeId'], u'\n'])
        devices.append([('bold result', u'Status: '), dev['Ebs']['Status'], u'\n'])
    second_screen.append((35, urwid.LineBox(urwid.Text(devices))))

    menu.body = urwid.Pile([urwid.Columns([(60, urwid.LineBox(first_screen))], min_width=60),
                            urwid.Columns(second_screen, min_width=35)])

    menu.footer = footer_instance(started)
    draw_result(menu)

    return [started, unavailable]


def exit_program(key):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    raise urwid.ExitMainLoop()


def handle_input(key):
    if key == 'Q':
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        raise urwid.ExitMainLoop()
    elif key == 'B':
        goback(menu)
    else:
        pass


def menu_main(button):
    menu.depth = 0
    menu.old_menu = None
    menu.body = [
        (u'EC2 - Elastic Cloud Computing', menu_ec2),
        (u'S3 - Simple Storage Service <under dev>', menu_s3),
        (u'Exit', exit_program)
        ]

    menu.header = u'SCAWS Main Menu'

    menu.footer = [
        u'Press (', ('quit button', u'Q'), u') to quit.',
    ]

    draw_menu(menu)


def menu_ec2(button):
    # saves actual menu in menu.old_menu previous menus list
    menu.old_menu.append([menu.header, menu.body, menu.footer])

    menu.body = [
        (u'Instances', ec2_instances),
        (u'Images (AMIs) <under dev>', exit_program),
        (u'Elastic Bloc Store (EBS) <under dev>', exit_program),
        (u'NetWork & Security <under dev>', exit_program),
        (u'Load Balancing <under dev>', exit_program),
        (u'AutoScaling <under dev>', exit_program),
        (u'Back', menu_back )
        ]
    menu.header = u'EC2 - Elastic Cloud Computing'

    menu.footer = [
        u'Press (', ('quit button', u'Q'), u') to quit.'
    ]

    draw_menu(menu)


def ec2_instances(button):
    # saves actual menu in menu.old_menu previous menus list
    menu.old_menu.append([menu.header, menu.body, menu.footer])

    menu.body = [
        (u'List Instances', describe_instances),
        (u'Start Instances', exit_program),
        (u'Stop Instances', exit_program),
        (u'Back', menu_back )
        ]
    menu.header = u'Instances'
    menu.footer = [
        u'Press (', ('quit button', u'Q'), u') to quit.'
    ]

    draw_menu(menu)


def describe_instances(nil):
    # saves actual menu in menu.old_menu previous menus list
    menu.old_menu.append([menu.header, menu.body, menu.footer])

    ec2client = ec2.open_client()
    instances = ec2.list_instances(ec2client)
    menu.header = u'Instances in reservation'
    for inst in instances:

        started, unavailable = draw_instance_in_menu(inst)

        next_instance = False
        back = False
        while not next_instance:
            ret = getch()
            if ret == 'Q':
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')
                raise urwid.ExitMainLoop()
            elif ret == u' ':
                next_instance = True
            elif ret == 'S' and not unavailable and not started:
                ec2.start_instance(ec2client, inst['InstanceId'])
                next_instance = False
            elif ret == 'T' and not unavailable and started:
                ec2.stop_instance(ec2client, inst['InstanceId'])
                next_instance = False
            elif ret == 'B':
                back = True
                next_instance = True
            elif ret == 'R':
                inst = ec2.get_instance(ec2client, inst['InstanceId'])
                started, unavailable = draw_instance_in_menu(inst)
                next_instance = False
            elif ret == 't':
                pass
            else:
                next_instance = False

        if back:
            break

    goback(menu)


def menu_s3():
    pass


def check_auth():
    home = os.path.expanduser("~")

    credentialsf = home + u'/.aws/credentials'
    try:
        f = open(credentialsf, 'r')
        f.close()
        return True
    except FileNotFoundError:
        print(u'AWS credentials file ' + credentialsf + u'not found\n'
              u'Please, create a proper access keys from IAM and fill this file with the following format:')
        print(u'\t[default]\n '
              u'\taws_access_key_id = YOUR_ACCESS_KEY\n'
              u'\taws_secret_access_key = YOUR_SECRET_KEY\n'
              u'\tregion=PREFERRED_REGION')
        return False
    except PermissionError:
        print(u'No read permission on ' + credentialsf)
        return False


def init_menu(men):

    title = urwid.AttrMap(urwid.Text(men.header, align='center'), 'titlebar')

    footer = urwid.Text(men.footer)

    body = list()
    for x in men.body:
        button = urwid.Button(x[0])
        if x[0] == 'Exit' or x[0] == 'Back':
            body.append(urwid.Divider())
        urwid.connect_signal(button, 'click', x[1])
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    body = urwid.LineBox(urwid.Overlay(urwid.ListBox(urwid.SimpleFocusListWalker(body)),
                         urwid.SolidFill(u' '), align='center', width=('relative', 50),
                         valign='middle', height=('relative', 50),))

    return urwid.Frame(header=title, body=body, footer=footer)

palette = [
    ('titlebar', 'black,bold', 'white'),
    ('quit button', 'dark red', 'black'),
    ('bold result', 'black,bold', 'white'),
    ('stopped', 'dark red,bold', 'white'),
    ('pending', 'dark blue,bold', 'white'),
    ('started', 'dark green', 'white'),
    ('small title', 'dark blue,bold', 'white'),
    ('reversed', 'standout', '')
]
menu = Menu

menu.header = 'SCAWS Main Menu'

menu.body = [
    (u'EC2 - Elastic Cloud Computing', menu_ec2),
    (u'S3 - Simple Storage Service', menu_s3),
    (u'Exit', exit_program)
]

menu.footer = [
    u'Press (', ('quit button', u'Q'), u') to quit.',
]

if check_auth():
    layout = init_menu(menu)
    main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)
    main_loop.run()
else:
    pass
