# functions for interfacing with dbus
import dbus
def call_dbus_method(bus_type, obj, path, interface, method, arg):
    """ calls dbus method on specific interface"""
    if bus_type == "session":
        bus = dbus.SessionBus()
    if bus_type == "system":
        bus = dbus.SystemBus()
    proxy = bus.get_object(obj, path)
    method = proxy.get_dbus_method(method, interface)
    if arg:
        return method(*arg)
    else:
        return method()

def get_dbus_property(bus_type, obj, path, iface, prop):
    """ reads properties defined on specific dbus interface"""
    if bus_type == "session":
        bus = dbus.SessionBus()
    if bus_type == "system":
        bus = dbus.SystemBus()
    proxy = bus.get_object(obj, path)
    aux = 'org.freedesktop.DBus.Properties'
    props_iface = dbus.Interface(proxy, aux)
    props = props_iface.Get(iface, prop)
    return props

