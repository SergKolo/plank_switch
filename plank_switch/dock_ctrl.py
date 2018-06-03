# functions responsible for Deepin dock control
import dbus_ctrl

dock_obj = [ "session", "net.launchpad.plank", 
                "/net/launchpad/plank/dock1", "net.launchpad.plank.Items"]

def get_desk_files(onlydocked=True):
    """ Obtains .desktop files of entries currently on the dock.
        Defaults to returning only those that are pinned to dock.
        If onlydocked=False, all entries on the dock (including 
        running but not pinned entries) get returned"""
    desk_files = []
    global dock_obj    
    desk_files = list( dbus_ctrl.call_dbus_method(*dock_obj,"GetPersistentApplications",[]))
    if not onlydocked :
        desk_files = desk_files + list(dbus_ctrl.call_dbus_method(*dock_obj,"GetTransientApplications",[]))
    return desk_files

def clear_dock(*args):
    """  Undocks all entries. Running appications will still 
         appear but won't be pinned"""
    global dock_obj
    for desk_file in get_desk_files():
        dbus_ctrl.call_dbus_method(*dock_obj,"Remove",[desk_file])

def fill_dock(desk_files):
    """ Fills the dock with Entries as provided by desk_files list,
        in the order they appear on the list"""
    global dock_obj
    for index,desk_file in enumerate(desk_files):
        dbus_ctrl.call_dbus_method(*dock_obj,"Add",[desk_file])
