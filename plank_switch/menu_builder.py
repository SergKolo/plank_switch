from gi.repository import Gtk
from collections import OrderedDict
import os,json
import dialogs

def add_menu_item(menu_obj, type=Gtk.MenuItem,
                  icon=None, label="HelloWorld", action=None, args=[]):
    """ dynamic function that can add menu items depending on
        the item type and other arguments"""
    #print(label,type,action)

    menu_item = None
    if type is Gtk.ImageMenuItem and label:
        menu_item = Gtk.ImageMenuItem.new_with_label(label)
        menu_item.set_always_show_image(True)
        if '/' in icon:
            icon = Gtk.Image.new_from_file(icon)
        else:
            icon = Gtk.Image.new_from_icon_name(icon, 48)
        menu_item.set_image(icon)
    elif type is Gtk.ImageMenuItem and not label:
        menu_item = Gtk.ImageMenuItem()
        menu_item.set_always_show_image(True)
        if '/' in icon:
            icon = Gtk.Image.new_from_file(icon)
        else:
            icon = Gtk.Image.new_from_icon_name(icon, 16)
        menu_item.set_image(icon)
    elif type is Gtk.MenuItem:
        menu_item = Gtk.MenuItem(label)
    elif type is Gtk.SeparatorMenuItem:
        menu_item = Gtk.SeparatorMenuItem()
    if action:
        menu_item.connect('activate', action, *args)
    menu_obj.append(menu_item)
    menu_obj.show()


def build_base_menu(menu_obj):
    with open(os.path.join(os.path.dirname(__file__),'base_menu.json') ) as menu_file:
         base_menu = json.load(menu_file,object_pairs_hook=OrderedDict)
         for key,val in base_menu.items():
             val["type"] = eval(val["type"])
             if val["type"] is Gtk.SeparatorMenuItem:
                 print("Is Separator")
                 add_menu_item(menu_obj,type=Gtk.SeparatorMenuItem)
                 continue
             val["action"] = eval("self" + val["action"]) if val["action"].startswith(".")else  eval(val["action"])
             add_menu_item(menu_obj,label=key,**val,args=[None])
