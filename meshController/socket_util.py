import mmapi;
from mmRemote import *;
import mm;


def selectObjectByName(remote, name):
    (found, objid) = mm.find_object_by_name(remote, name)
    if found:
        mm.select_objects(remote, [objid])
    return found


def selectObjectsByName(remote, name_list):
    objects = []
    for name in name_list:
        (found, objid) = mm.find_object_by_name(remote, name)
        if found:
            objects.append(objid)
    mm.select_objects(remote, objects)

