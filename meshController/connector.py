import mmapi;
from mmRemote import *;
import mm;
import socket_util;
from socket_names import *;
import os;


# [RMS] in the following code, we use a few global names/strings:
#       * socket_names.ConnectorPath() is the path to the connector
#       * socket_names.ConnectorName() is what we rename the connector object to
#       * socket_names.SocketName() is what we assume the socket object is named
#

# [RMS] this function imports the socket connector and positions it such that it is offset half its height
#   from the centroid of the current selection. 
def import_connector(do_accept,connectorName):
    # initialize connection
    remote = mmRemote();
    remote.connect();
    setConnectorPath(connectorName)
    # find center of current selection, and then shoot ray from below this point, straight upwards, and
    # hope that it hits outer shell
    centroid = mm.get_face_selection_centroid(remote)
    sel_ctr = centroid
    (bFound, selFrame) = mm.find_ray_hit(remote, mm.addv3(sel_ctr, (0,-10,0)), (0,1,0)  )

    # exit out of selection tool
    mm.clear_face_selection(remote)

    # import part we want to position at selection
    cwd = os.getcwd()
    socketPath = os.path.join(cwd,'socket',connectorName)
    new_objs = mm.append_objects_from_file(remote, socketPath);

    # rename part
    mm.set_object_name(remote, new_objs[0], ConnectorName() )

    # select new part
    mm.select_objects(remote, new_objs)

    # get bbox of part, so that we can put origin at bottom of cylinder if desired (assume file authored that way)
    (min,max) = mm.get_selected_bounding_box(remote)
    partTop = ( (min[0]+max[0])/2, max[1], (min[2]+max[2])/2 )
    partCenter =  ( (min[0]+max[0])/2, (min[1]+max[1])/2, (min[2]+max[2])/2 )
    partH = max[1]-min[1]

    # RMS HACK BECAUSE OF UNITS STUPID
    plane_cut_setback = partH * 0.5

    # start transform tool
    mm.begin_tool(remote, "transform")
    cur_origin = mm.get_toolparam(remote, "origin")
    dy = 0.5*partH

    # [RMS] currently assuming that leg is oriented wrt axis, so we keep connector vertical
    # compute and apply rotation
    #rotation = mm.make_matrix_from_axes(selFrame.x, mm.negv3(selFrame.z), selFrame.y )
    #mm.set_toolparam(remote, "rotation", rotation )

    # translate origin of part to frame origin
    translate = mm.subv3( selFrame.origin, cur_origin )
    # shift along frame Z to place bottom of part on surface (ie at frame origin)
    translate = mm.addv3( translate, mm.mulv3s( selFrame.z, dy ) )
    mm.set_toolparam(remote, "translation", translate )

    # accept xform
    if do_accept:
        mm.accept_tool(remote)

    remote.shutdown()


# [RMS] cut the outer shell of the socket at a vertical offset from the Connector
def connector_plane_cut(do_accept):
    remote = mmRemote();
    remote.connect();

    # accept outstanding tools, if there are any
    mm.accept_tool(remote)

    # get bbox of connector
    mm.select_object_by_name(remote, ConnectorName() )
    (min,max) = mm.get_selected_bounding_box(remote)
    partCenter =  ( (min[0]+max[0])/2, (min[1]+max[1])/2, (min[2]+max[2])/2 )
    partH = max[1]-min[1]

    mm.select_object_by_name(remote, SocketName() )

    # shoot ray upwards to hit exterior of socket, and then get facegroup of outer shell
    (bounds_min, bounds_max) = mm.get_selected_bounding_box(remote)
    bounds_ctr = mm.mulvs(mm.addv3(bounds_min, bounds_max), 0.5)
    mm.begin_tool(remote, "select")
    mm.select_hit_triangle(remote, mm.addv3(bounds_ctr, (0,-10,0)), (0,1,0) )
    groups = mm.list_selected_groups(remote)

    # select outer shell facegroup and start plane cut
    mm.select_facegroups(remote, groups)
    mm.begin_tool(remote, "planeCut")

    # position cutting plane at offset from part
    mm.set_toolparam(remote, "fillType", 0)
    #planeNormal = (0,1,0)
    #mm.set_toolparam(remote, "normal", planeNormal )
    planeOrigin = max
    planeOrigin = mm.addv3( planeOrigin, mm.mulv3s(planeNormal, 0.5*partH) )
    mm.set_toolparam(remote, "origin", planeOrigin)

    if do_accept:
        mm.accept_tool(remote)

    remote.shutdown()


# [RMS] Combine the open shells of the socket and connector, then Join them, then expand a few rings and Smooth the result
def connector_join():
    remote = mmRemote();
    remote.connect();

    # accept outstanding tools, if there are any
    mm.accept_tool(remote)

    [found,id1] = mm.find_object_by_name(remote,SocketName())
    [found,id2] = mm.find_object_by_name(remote,ConnectorName())
    mm.select_objects(remote,[id1,id2])



    # combine part with socket
    mm.begin_tool(remote, "combine")

    # select-all and do join # [TODO] support select-boundary-loops in API
    mm.select_all(remote)
    mm.begin_tool(remote, "join")
    mm.accept_tool(remote)

    # [RMS] this block will clean up holes, but requires ability to save & restore selection!
    #   [TODO] we can do this now, because we can read back facegroup after createFaceGroup...
    if False:
        # save selection
        mm.begin_tool(remote, "createFaceGroup")
        mm.clear_face_selection(remote)

        # do repair pass, in case join created holes (happens!)
        mm.begin_tool(remote, "inspector")
        mm.tool_utility_command(remote, "repairAll")

        # [TODO] restore selection


    # expand selection a few times, then remesh
    if True:
        for x in range(0,8):
            mm.selection_utility_command(remote, "expandByOneRing")

        mm.begin_tool(remote, "remesh")
        mm.accept_tool(remote)
        mm.begin_tool(remote, "smooth")
        mm.set_toolparam(remote, "scale", 500.0)
        mm.accept_tool(remote)

    mm.clear_face_selection(remote)

    remote.shutdown()