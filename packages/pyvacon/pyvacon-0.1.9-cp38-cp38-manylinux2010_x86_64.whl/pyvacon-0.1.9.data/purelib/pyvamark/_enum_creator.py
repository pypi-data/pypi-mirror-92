import enum

# needed so that enum can be converted to integer
# this is required by the "in" typemap which converts a c++ enum value
# to a Python enum value
def _get_index(obj):
    return obj.value

# The swig interface creates a set of enum constants of the form _<Enum>_Value
# This function creates a Python enum (subclass of enum.Enum) containing all values
def create_enum(name, all_vars):
    prefix = '_' + name + '_'
    prefixlen = len(prefix)
    kv = {k[prefixlen:] : v for k,v in all_vars.items() if k.startswith(prefix)}
    cls = enum.Enum(name, kv)
    setattr(cls, '__index__', _get_index)
    return cls
