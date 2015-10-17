#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scaws (Simple Console for AWS) is a text based console for AWS
"""


import pdb
import os
import ec2
import urwid


__author__ = "Iván Renedo"
__copyright__ = "GPL"


def draw_menu(title, menu_body, footer):
    body = [urwid.Divider()]
    for x in menu_body:
        button = urwid.Button(x[0])
        if x[0] == 'Exit':
            body.append(urwid.Divider())
        urwid.connect_signal(button, 'click', x[1])
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    main_loop.widget.body = urwid.Overlay(urwid.ListBox(urwid.SimpleFocusListWalker(body)),
                         urwid.SolidFill(u' '), align='center', width=('relative', 50),
                         valign='middle', height=('relative', 50),)
    main_loop.widget.footer = footer
    main_loop.widget.title = urwid.AttrMap(urwid.Text(title, align='center'), 'titlebar')
    main_loop.draw_screen()


def draw_result(title, body, footer):
    main_loop.widget.body = body
    main_loop.widget.title = urwid.AttrMap(urwid.Text(title, align='center'), 'titlebar')
    main_loop.widget.footer = footer
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
    if key in ['b','B']:
        menu_main(None)


def menu_main(button):

    menu_body = [
        (u'EC2 - Elastic Cloud Computing', menu_ec2),
        (u'S3 - Simple Storage Service', menu_s3),
        (u'Exit', exit_program)
        ]

    title = u'SCAWS Main Menu'

    footer = urwid.Text([u'Press (', ('quit button', u'Q'), u') to quit.'])

    draw_menu(title,menu_body, footer)


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

    footer = urwid.Text([u'Press (', ('quit button', u'Q'), u') to quit.'])

    draw_menu(title, menu_body, footer)


def ec2_instances(button):
    menu_body = [
        (u'List Instances', describe_instances),
        (u'Start Instances', exit_program),
        (u'Stop Instances', exit_program),
        (u'Back', menu_ec2)
        ]
    title = u'Instances'
    footer = urwid.Text([u'Press (', ('quit button', u'Q'), u') to quit.'])

    draw_menu(title, menu_body, footer)


def describe_instances(nil):
    instances = ec2.list_instances()
    title = u'Instances in reservation'
    for inst in instances:
        layout = urwid.Text([
            ('bold result', u'Instance ID:'), inst['InstanceId'],
        ])
        body = urwid.Overlay(urwid.Filler(layout, valign='top', top=1, bottom=1),
                         urwid.SolidFill(u' '), align='left', width=('relative', 50),
                         valign='top', height=('relative', 50),)

        footer = urwid.Text([u'Press "Enter" to continue'])

        draw_result(title, body, footer)
        input('')
    ec2_instances(None)



def menu_s3():
    pass


def init_main_menu():

    menu_body = [
        (u'EC2 - Elastic Cloud Computing', menu_ec2),
        (u'S3 - Simple Storage Service', menu_s3),
        (u'Exit', exit_program)
        ]
    title = urwid.AttrMap(urwid.Text('SCAWS Main Menu', align='center'), 'titlebar')

    footer = urwid.Text([u'Press (', ('quit button', u'Q'), u') to quit.'])

    body = [urwid.Divider()]
    for x in menu_body:
        button = urwid.Button(x[0])
        if x[0] == 'Exit' or x[0] == 'Back':
            body.append(urwid.Divider())
        urwid.connect_signal(button, 'click', x[1])
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    body = urwid.Overlay(urwid.ListBox(urwid.SimpleFocusListWalker(body)),
                         urwid.SolidFill(u' '), align='center', width=('relative', 50),
                         valign='middle', height=('relative', 50),)

    return urwid.Frame(header=title, body=body, footer=footer)

palette = [
    ('titlebar', 'black,bold', 'white'),
    ('quit button', 'dark red,bold', 'black'),
    ('bold result', 'black,bold', 'white'),
]

layout = init_main_menu()
main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)
main_loop.run()