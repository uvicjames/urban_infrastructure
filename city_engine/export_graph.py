from scripting import *

# get a CityEngine instance
ce = CE()

# Offsets to match CityEngine mesh export for buildings. Set manually.
xOffset = 42.452
zOffset = -45.093

# Global variables.
vertex_dictionary = {}
processed_vertices = []
processed_edges = []
filename = "street_network.xml"


# get list of vertices
# for each vertex
#   assign new ID
#   load coordinates 
#   put in map
# for each edge
#   get incident vertices
#   add edge data structure using simple ID
# output all information.

class Vertex:
    def __init__(self, ID):
        self.ID = ID
        
class Edge:
    def __init__(self, ID):
        self.ID = ID

def process_vertices():
    node_list = ce.getObjectsFrom(ce.scene(), ce.isGraphNode)
    counter = 0
    for node in node_list:
        temp_vertex = Vertex(counter)
        float_array = ce.getVertices(node)
        temp_vertex.x = float_array[0]
        temp_vertex.y = float_array[1]
        temp_vertex.z = float_array[2]
        temp_vertex.OID = ce.getOID(node)
        vertex_dictionary[temp_vertex.OID] = temp_vertex.ID
        processed_vertices.append(temp_vertex)
        counter = counter + 1
    print('Processed vertex data')
        
def process_edges():
    segment_list = ce.getObjectsFrom(ce.scene(), ce.isGraphSegment)
    counter = 0
    for segment in segment_list:
        vertices = ce.getObjectsFrom(segment, ce.isGraphNode)
        v = vertices[0]
        w = vertices[1]
        vOID = ce.getOID(v)
        wOID = ce.getOID(w)
        vID = vertex_dictionary.get(vOID)
        wID = vertex_dictionary.get(wOID)
        temp_edge = Edge(counter)
        temp_edge.OID = ce.getOID(segment)
        temp_edge.vOID = vOID
        temp_edge.wOID = wOID
        temp_edge.vID = vID
        temp_edge.wID = wID
        temp_edge.lanes = ce.getAttribute(segment, '/ce/street/streetWidth')
        processed_edges.append(temp_edge)
        counter = counter +1
    print('Processed edge data')

def output_vertex(vertex, file):
    if vertex is None:
        return
    
    file.write('\t\t<vertex id="{}" oid="{}"  x="{}"  y="{}"  z="{}" />\n'.format(
        vertex.ID, vertex.OID, vertex.x + xOffset, vertex.y, vertex.z + zOffset))


def output_edge(edge, file):
    if edge is None:
        return
    file.write('\t\t<edge id="{}" oid="{}" start_id="{}" end_id="{}" lanes="{}" />\n'.format(
            edge.ID, edge.OID, edge.vID, edge.wID, edge.lanes))


def output_vertices(file):
    
    file.write('\t<vertexlist count="{}">\n'.format(len(processed_vertices)))

    for vertex in processed_vertices:
        output_vertex(vertex, file)
        
    file.write('\t</vertexlist>\n')
    

def output_edges(file):
    
    file.write('\t<edgelist count="{}">\n'.format(len(processed_edges)))
    
    for edge in processed_edges:
        output_edge(edge, file)
    
    file.write('\t</edgelist>\n')


def output_graph(file):
    process_vertices()
    process_edges()
    
    file.write('<graph>\n')
    output_vertices(file)
    output_edges(file)
    file.write('</graph>\n')   


if __name__ == '__main__':
    filepath = ce.toFSPath(filename)
    file = open(filepath, 'w')

    output_graph(file)
    
    file.close()
