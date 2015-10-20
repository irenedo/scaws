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
            option1 = urwid.Text(u'(s): Stop Instance')
    else:
            option1 = urwid.Text(u'(S): Start Instance')
    option2 = urwid.Text(u'(Q): Quit')
    row1 = urwid.Pile([option1,option2])

    option3 = urwid.Text(u'(G): List Security Groups')
    option4 = urwid.Text(u'(B): Back to previous menu')

    row2 = urwid.Pile([option3, option4])

    option5 = urwid.Text(u'(T): List Tags')
    option6 = urwid.Text(u'(R): Refresh Instance')

    row3 = urwid.Pile([option5, option6])

    footer = urwid.Columns([row1, row2, row3])

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
    main_loop.widget.body = urwid.LineBox(urwid.Overlay(urwid.Filler(urwid.Text(men.body)),
                                                        urwid.SolidFill(u' '), align='center',
                                          width=('relative', 50), valign='middle', height=('relative', 50)))
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
    if key == 'B':
        goback(menu)


def menu_main(button):
    menu.depth = 0
    menu.old_menu = None
    menu.body = [
        (u'EC2 - Elastic Cloud Computing', menu_ec2),
        (u'S3 - Simple Storage Service', menu_s3),
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
        (u'Images (AMIs)', exit_program),
        (u'Elastic Bloc Store (EBS)', exit_program),
        (u'NetWork & Security', exit_program),
        (u'Load Balancing', exit_program),
        (u'AutoScaling', exit_program),
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

    unavailable = False
    started = False
    color = ''
    status = ''
    for inst in instances:

        if inst['State']['Name'] == 'running':
            status = 'Started'
            color = 'started'
            started = True
        elif inst['State']['Name'] == 'stopped':
            status = 'Stopped'
            color = 'stopped'
            started = False
        else:
            unavailable = True

        menu.body = [
            ('bold result', u'Instance ID: '), inst['InstanceId'], '\n',
            ('bold result', u'Instance Status: '), (color, status), '\n',
            ('bold result', u'PublicDnsName: '), inst['PublicDnsName'], '\n',
            ('bold result', u'Private Address: '), inst['PrivateIpAddress'], '\n',
            ('bold result', u'Availability Zone: '), inst['Placement']['AvailabilityZone'], '\n',
            ('bold result', u'VPC ID: '), inst['VpcId'], '\n',
            ('bold result', u'Instance Type: '), inst['InstanceType'], '\n',
            ('bold result', u'Image Id: '), inst['ImageId'], '\n',
            ('bold result', u'Key Name: '), inst['KeyName'], '\n'
        ]

        menu.footer = footer_instance(started)

        draw_result(menu)
        allowed_key = False
        back = False
        while not allowed_key:
            ret = getch()
            if ret == 'Q':
                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')
                raise urwid.ExitMainLoop()
            elif ret == u' ':
                allowed_key = True
            elif ret == 'S' and not unavailable and not started:
                ec2.start_instance(ec2client, inst['InstanceId'])
                allowed_key = False
            elif ret == 's' and not unavailable and started:
                ec2.stop_instance(ec2client, inst['InstanceId'])
                allowed_key = False
            elif ret == 'B':
                back = True
                allowed_key = True
            elif ret == 'R':
                inst = ec2.get_instance(ec2client,inst['InstanceId'])
                if inst['State']['Name'] == 'running':
                    status = 'Started'
                    color = 'started'
                    started = True
                elif inst['State']['Name'] == 'stopped':
                    status = 'Stopped'
                    color = 'stopped'
                    started = False
                else:
                    unavailable = True

                menu.body = [
                    ('bold result', u'Instance ID: '), inst['InstanceId'], '\n',
                    ('bold result', u'Instance Status: '), (color, status), '\n',
                    ('bold result', u'PublicDnsName: '), inst['PublicDnsName'], '\n',
                    ('bold result', u'Private Address: '), inst['PrivateIpAddress'], '\n',
                    ('bold result', u'Availability Zone: '), inst['Placement']['AvailabilityZone'], '\n',
                    ('bold result', u'VPC ID: '), inst['VpcId'], '\n',
                    ('bold result', u'Instance Type: '), inst['InstanceType'], '\n',
                    ('bold result', u'Image Id: '), inst['ImageId'], '\n',
                    ('bold result', u'Key Name: '), inst['KeyName'], '\n'
                ]

                menu.footer = footer_instance(started)
                allowed_key = True
            else:
                allowed_key = False

        if back:
            break

    goback(menu)


def menu_s3():
    pass


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
    ('started', 'dark green', 'white'),
    ('help', 'dark blue', 'white')
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

layout = init_menu(menu)

main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)
main_loop.run()