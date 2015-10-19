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


def draw_menu(titl, menu_body, footer):
    body = [urwid.Divider()]
    for x in menu_body:
        button = urwid.Button(x[0])
        if x[0] == 'Exit':
            body.append(urwid.Divider())
        urwid.connect_signal(button, 'click', x[1])
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    main_loop.widget.body = urwid.LineBox(urwid.Overlay(urwid.ListBox(urwid.SimpleFocusListWalker(body)),
                                          urwid.SolidFill(u' '), align='center', width=('relative', 50),
                                          valign='middle', height=('relative', 50),))
    main_loop.widget.footer = urwid.Text(footer)
    main_loop.widget.header = urwid.AttrMap(urwid.Text(titl, align='center'), 'titlebar')
    main_loop.draw_screen()


def draw_result(titl, body, footer):
    main_loop.widget.header = urwid.AttrMap(urwid.Text(titl, align='center'), 'titlebar')
    main_loop.widget.body = urwid.LineBox(urwid.Overlay(urwid.Filler(urwid.Text(body)),
                                                        urwid.SolidFill(u' '), align='center',
                                          width=('relative', 50), valign='middle', height=('relative', 50)))
    main_loop.widget.footer = urwid.Text(footer)
    main_loop.draw_screen()


def exit_program(key):
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    raise urwid.ExitMainLoop()


def handle_input(key):
    if key in ['Q', 'q']:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
        raise urwid.ExitMainLoop()
    if key in ['b', 'B']:
        menu_main(None)


def menu_main(button):

    menu_body = [
        (u'EC2 - Elastic Cloud Computing', menu_ec2),
        (u'S3 - Simple Storage Service', menu_s3),
        (u'Exit', exit_program)
        ]

    title = u'SCAWS Main Menu'

    footer = [
        u'Press (', ('quit button', u'Q'), u') to quit.'
    ]

    draw_menu(title, menu_body, footer)


def menu_ec2(button):

    menu_body = [
        (u'Instances', ec2_instances),
        (u'Images (AMIs)', exit_program),
        (u'Elastic Bloc Store (EBS)', exit_program),
        (u'NetWork & Security', exit_program),
        (u'Load Balancing', exit_program),
        (u'AutoScaling', exit_program),
        (u'Back', menu_main)
        ]
    title = u'EC2 - Elastic Cloud Computing'

    footer = [
        u'Press (', ('quit button', u'Q'), u') to quit.'
    ]

    draw_menu(title, menu_body, footer)


def ec2_instances(button):
    menu_body = [
        (u'List Instances', describe_instances),
        (u'Start Instances', exit_program),
        (u'Stop Instances', exit_program),
        (u'Back', menu_ec2)
        ]
    title = u'Instances'
    footer = [
        u'Press (', ('quit button', u'Q'), u') to quit.'
    ]

    draw_menu(title, menu_body, footer)


def describe_instances(nil):
    instances = ec2.list_instances()
    title = u'Instances in reservation'

    for inst in instances:
        if inst['State']['Name'] != 'stopped':
            status = 'Started'
            color = 'started'

        else:
            status = 'Stopped'
            color = 'stopped'

        body = [
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

        footer = [
            u'Press (', ('quit button', u'Q'), u') to quit. \n',
            'Press any key to continue...'
        ]

        draw_result(title, body, footer)
        ret = getch()

        if ret in ['Q', 'q']:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
            raise urwid.ExitMainLoop()

    ec2_instances(None)


def menu_s3():
    pass


def init_menu(title, menu_body, footer):

    title = urwid.AttrMap(urwid.Text(title, align='center'), 'titlebar')

    footer = urwid.Text(footer)

    body = [urwid.Divider()]
    for x in menu_body:
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

title = 'SCAWS Main Menu'

menu_body = [
    (u'EC2 - Elastic Cloud Computing', menu_ec2),
    (u'S3 - Simple Storage Service', menu_s3),
    (u'Exit', exit_program)
]

footer = [
    u'Press (', ('quit button', u'Q'), u') to quit.\n',
    u'Press (', ('help', u'H'), u') for help.'
]

layout = init_menu(title, menu_body, footer)

main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)
main_loop.run()