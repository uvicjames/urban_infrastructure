from scripting import *

"""
Python script for use in ESRI CityEngine. This script will allow a user to export the block/lot 
geometry from a CityEngine scene to an XML file. Note the coordinate system: the y axis is vertical.

Instructions: 
1) copy this file to the CityEngine 'scripts' folder for your project.
2) open a scene, double click on the script, and then select 'run script'.

If you are exporting building/street geometry from the same scene, you may wish to center the
exported geometry at the origin. Use the 'export model->Autodesk OBJ' wizard and select the 
'center geometry' option. Copy the offsets to the script below in order to ensure that the 
exported building/street geometry matches the output of this script.
"""


# CityEngine instance object, required for all queries.
ce = CE() 

# Offsets to match building meshes. 
x_offset = 42.452; 
z_offset = -45.093 

# Name of the output file.
filename = 'blocks.xml' 

# Counter for generating unique lot IDs.
lot_id_counter = 0 

@noUIupdate    
def get_vertex_list_as_string(vertex_list):
    output = ''
    # Walk the vertex list and apply transforms. (x_1, y_1, z_1, x_2, y_2, z_2, ...)
    for i in range(0, len(vertex_list)):
        value = vertex_list[i]
        if i % 3 == 0:
            value = value + x_offset
        elif i % 3 == 2:
            value = value + z_offset
        output = output + str(value) + ' '
    return output
    
@noUIupdate
def output_lot(lot, index, file):
    global lot_id_counter
    
    file.write('\t\t\t<lot sub_id="{}" id="{}" oid="{}" '.format(
             index,  # 'sub_id' is the lot index within the block
             lot_id_counter, # 'id' is the index within the scene.
             ce.getOID(lot))) # 'oid' is the CityEngine OID.
             
    vertex_string = get_vertex_list_as_string(ce.getVertices(lot))
    file.write('polygon="' + vertex_string + '"/>\n')
    lot_id_counter = lot_id_counter + 1

@noUIupdate 
def output_lots(lots, file):
    file.write('\t\t<lots count="{}">\n'.format(len(lots)))
    
    for j in range(0, len(lots)):
        output_lot(lots[j], j, file)
        
    file.write('\t\t</lots>\n')

@noUIupdate
def output_block(block, file, block_id):
    # Output 'id' (primary identifier) and CityEngine internal OID.
    file.write('\t<block id="{}" oid="{}" '.format(str(block_id), ce.getOID(block)))
        
    # Polygon information for block shape. All blocks have a shape.
    vertex_string = get_vertex_list_as_string(ce.getVertices(block))
    file.write('polygon="' + vertex_string + '">\n')
        
    # Output lot data if present. Not all blocks have lot data.
    lots = ce.getObjectsFrom(block, ce.isShape)
    if len(lots) != 0:
        output_lots(lots, file)
            
    file.write('\t</block>\n')
    file.flush()

@noUIupdate
def output_scene():
    filepath = ce.toFSPath(filename)
    file = open(filepath, 'w')
    blocks = ce.getObjectsFrom(ce.scene, ce.isBlock)
    
    # Root XML element.
    file.write('<blocks count="{}">\n'.format(str(len(blocks))))
    
    for i in range(0, len(blocks)):
        output_block(blocks[i], file, i)
        
    file.write('</blocks>\n');
    file.close()
