#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright © 2018 Sergiy Kolodyazhnyy <1047481448@qq.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import gi,os,json
gi.require_version('AppIndicator3', '0.1')
from gi.repository import GLib as glib
from gi.repository import AppIndicator3 
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Gio
from gi.repository.Gdk import ScrollDirection
from collections import OrderedDict

import subprocess

import menu_builder, dialogs,config_ctrl,dbus_ctrl,dock_ctrl


class DeepinDockSwitch(object):

    all_lists = OrderedDict()

    def __init__(self):
        self.app = AppIndicator3.Indicator.new(
            'dde_dock_list', "",
            AppIndicator3.IndicatorCategory.OTHER
        )

        config_file = os.path.join(os.environ["HOME"],".config/dde_dockswitch/docklists.json")

        self.app.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.make_menu()
        self.app.set_icon("drive-harddisk-symbolik")

    def run(self):
        """ Launches the indicator """
        try:
            Gtk.main()
        except KeyboardInterrupt:
            pass

    def update():
        pass

    def callback():
        pass

    def make_menu(self, *args):
        """ generates entries in the indicator"""
        global all_lists
        if hasattr(self, 'app_menu'):
            for item in self.app_menu.get_children():
                self.app_menu.remove(item)
        self.app_menu = Gtk.Menu()


        def fill_dock_and_update(ignore,fill):
             dock_ctrl.clear_dock()
             dock_ctrl.fill_dock(None,fill)
             self.make_menu()

        def clear_and_update(ignore):
             dock_ctrl.clear_dock()
             self.make_menu()
# Plank has peculiar behavior: if a program is already running, it won't move in the dock to be placed where it's supposed to be in user-defined list


        all_lists = config_ctrl.read_config_file()
        print(all_lists)
        print(dock_ctrl.get_desk_files())
        for list_label,desk_files in all_lists.items():
            if sorted(desk_files) == sorted(list(dock_ctrl.get_desk_files(onlydocked=True))):
                list_label = "\u2605 " + list_label
            item_params = { 
                "label": list_label,
                "action": fill_dock_and_update,
                "args": [desk_files]
            }
            menu_builder.add_menu_item(self.app_menu,**item_params)
         
        menu_builder.add_menu_item(self.app_menu,icon="add",label="Record Currently Docked",action=self.record_currently_docked,args=[])

        menu_builder.add_menu_item(self.app_menu,icon="trash",label="Clear dock",action=clear_and_update,args=[])
        menu_builder.build_base_menu(self.app_menu)
        self.app_menu.show_all()
        self.app.set_menu(self.app_menu)

    def record_currently_docked(self,*args):
        global all_lists
        docked_desk_files = dock_ctrl.get_desk_files(onlydocked=True)
        name = self.run_cmd(['zenity','--entry', 
                      '--text',"Name this list",
                      '--entry-text',"Default entry"]).decode().rstrip()
        if name:
            # this probably will have to be global
            all_lists = {**all_lists,name: docked_desk_files}
            config_ctrl.write_config_file(all_lists)
            self.make_menu()
        


    def run_cmd(self, cmdlist):
        """ utility: reusable function for running external commands """
        try:
            stdout = subprocess.check_output(cmdlist)
        except subprocess.CalledProcessError:
            # TODO
            pass
        else:
            if stdout:
                return stdout


        

if __name__ == '__main__':
    switch = DeepinDockSwitch()
    switch.run()
