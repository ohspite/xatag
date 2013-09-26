import xattr
from helpers import listify
import tag

XATTR_PREFIX = 'org.xatag.tags'
XATTR_FIELD_SEPARATOR = ';'

def is_xatag_xattr_key(name):
    """Check if name starts with XATTR_PREFIX."""
    return name.startswith('user.' + XATTR_PREFIX) or name.startswith(XATTR_PREFIX)

def xatag_to_xattr_key(tag_or_key):
    """Add XATTR_PREFIX to the given string or to the tag's key."""
    try:
        key = tag_or_key.key
    except AttributeError:
        key = tag_or_key
    key = tag.format_tag_key(key)
    if key == '' or key == 'tags':
        return 'user.' + XATTR_PREFIX
    else: 
        return 'user.' + XATTR_PREFIX + '.' + key

def xattr_to_xatag_key(key):
    """Remove XATTR_PREFIX from the given string."""
    key = tag.format_tag_key(key)
    key = key.replace('user.' + XATTR_PREFIX, '')
    key = key.replace(XATTR_PREFIX, '')
    if key != '' and key[0] == '.': key = key[1:]
    return key

def read_tag_keys(fname):
    """Return a list of the xatag keys of the xattr fields in fname in the xatag namespace."""
    attributes = xattr.xattr(fname)
    return [xattr_to_xatag_key(k) for k in attributes if is_xatag_xattr_key(k)]

def xattr_value_to_list(tag_string):
    """Split the value of a tag xattr and return a list of tag values."""
    return [tag.format_tag_value(x) for x in tag_string.split(XATTR_FIELD_SEPARATOR)
            if tag.format_tag_value(x) != '']

def list_to_xattr_value(tag_list):
    """Return a xattr value that represents the tags in tag_list."""
    return XATTR_FIELD_SEPARATOR.join(sorted(tag.format_tag_value(x) for x in tag_list))

# TODO: optionally print when the tag wasn't there to begin with.  it's
# especially important if you mean
#    -d genre:
# but type
#    -d genre
def remove_tag_values_from_xattr_value(xattr_value, tag_values, complement=False):
    """Remove the values in tag_values from the xattr formatted value."""
    tag_values = listify(tag_values)
    current_values = xattr_value_to_list(xattr_value)
    tag_values_set = set(tag_values)
    if complement:
        if '' in tag_values_set:
            values = current_values
        else:
            values = [value for value in current_values if value in tag_values_set]
    else:
        values = [value for value in current_values if value not in tag_values_set] 
    return list_to_xattr_value(values)

def add_tag_values_to_xattr_value(xattr_value, values_to_add):
    """Add the values in values_to_remove from the xattr formatted value."""
    values_to_add = listify(values_to_add)
    current_values = xattr_value_to_list(xattr_value)
    values = current_values + [value for value in values_to_add if value not in set(current_values)]
    return list_to_xattr_value(values)

def read_tags_as_dict(fname):
    """Return a dict of the xattr fields in fname in the xatag namespace."""
    attributes = xattr.xattr(fname)
    # no sense in reading the value if the key isn't going to be chosen
    return {xattr_to_xatag_key(k): xattr_value_to_list(attributes[k])
            for k in attributes if is_xatag_xattr_key(k)}


