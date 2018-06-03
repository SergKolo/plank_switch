import os
from gi.repository import Gtk

def show_about(*args):
    print(args)
    builder = Gtk.Builder()
    builder.add_from_file(os.path.join( 
            os.path.dirname(__file__),
            'about_dialog.glade'  ) )
    #print([ i.get_children() for i in builder.get_objects() ])

    # might be better to get children of the 
    # ButtonBox and actually connect Close button
    # to a signal handler
    
    w = builder.get_object("about_dialog")
    response = w.run()
    w.destroy()
