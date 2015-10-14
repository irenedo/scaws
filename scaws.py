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


def menu_button(caption, callback):

    button = urwid.Button(caption)
    urwid.connect_signal(button, 'click', callback)
    return urwid.AttrMap(button, None, focus_map='reversed')


def sub_menu(caption, choices):
    contents = menu(caption, choices)

    def open_menu(button):
        return top.open_box(contents)
    return menu_button([caption, u'...'], open_menu)


def menu(title, choices):
    body = [urwid.Text(('banner',title), align='center'), urwid.Divider()]
    body.extend(choices)
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))


def item_chosen(button):
    response = urwid.Text([u'You chose ', button.label, u'\n'])
    done = menu_button(u'Ok', exit_program)
    top.open_box(urwid.Filler(urwid.Pile([response, done])))


def exit_program(button):
    raise urwid.ExitMainLoop()


def divider():
    return urwid.Divider()


class boxes(urwid.WidgetPlaceholder):
    max_box_levels = 5

    def __init__(self, box):
        super(boxes, self).__init__(urwid.SolidFill(u' '))
        self.box_level = 0
        self.open_box(box)

    def open_box(self, box):
        self.original_widget = urwid.Overlay(urwid.LineBox(box),
            self.original_widget,
            align='center', width=('relative', 80),
            valign='middle', height=('relative', 80),
            min_width=24, min_height=8)
        self.box_level += 1

    def keypress(self, size, key):
        if key == 'esc' and self.box_level > 1:
            self.original_widget = self.original_widget[0]
            self.box_level -= 1
        else:
            return super(boxes, self).keypress(size, key)


def item_back(button):
    top.original_widget = top.original_widget[0]
    top.box_level -= 1


"""
MAIN
"""


menu_top = menu(u'[[  SCAWS Main Menu  ]]', [
    sub_menu(u'EC2 - Elastic Cloud Computing', [
        sub_menu(u'Instances', [
            menu_button(u'Describe Instances', item_chosen),
            divider(),
            menu_button(u'Back', item_back),
        ]),
        sub_menu(u'Images (AMIs)', [
            divider(),
            menu_button(u'Back', item_chosen),
        ]),
        sub_menu(u'Elastic Bloc Store (EBS)', [
            divider(),
            menu_button(u'Back', item_back),
        ]),
        sub_menu(u'NetWork & Security', [
            divider(),
            menu_button(u'Back', item_chosen),
        ]),
        sub_menu(u'Load Balancing', [
            divider(),
            menu_button(u'Back', item_back)
        ]),
        sub_menu(u'AutoScaling', [
            divider(),
            menu_button(u'Back', item_chosen),
        ]),
        divider(),
        menu_button(u'Back', item_back)
    ]),
    sub_menu(u'S3 - Simple Storage Service', [
        sub_menu(u'Preferences', [
            menu_button(u'Appearance', item_chosen),
        ]),
        menu_button(u'Lock Screen', item_chosen),
    ]),
    divider(),
    menu_button(u'Exit', exit_program)
])

top = boxes(menu_top)
urwid.MainLoop(top, palette=[('banner', 'white', 'black'), ('reversed', 'standout', '')]).run()


if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')
