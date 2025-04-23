import bpy

def round_node_group_3_1():
    if "Round" in bpy.data.node_groups: ### Manual Entry
        return bpy.data.node_groups["Round"] ### Manual Entry
    round = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = "Round")

    #initialize round nodes
    #node Separate XYZ.003
    separate_xyz_003 = round.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_003.name = "Separate XYZ.003"
    
    #node Math.004
    math_004 = round.nodes.new("ShaderNodeMath")
    math_004.name = "Math.004"
    math_004.operation = 'ROUND'
    math_004.use_clamp = False
    #Value_001
    math_004.inputs[1].default_value = 0.5
    #Value_002
    math_004.inputs[2].default_value = 0.5
    
    #node Math.005
    math_005 = round.nodes.new("ShaderNodeMath")
    math_005.name = "Math.005"
    math_005.operation = 'ROUND'
    math_005.use_clamp = False
    #Value_001
    math_005.inputs[1].default_value = 0.5
    #Value_002
    math_005.inputs[2].default_value = 0.5
    
    #node Math.006
    math_006 = round.nodes.new("ShaderNodeMath")
    math_006.name = "Math.006"
    math_006.operation = 'ROUND'
    math_006.use_clamp = False
    #Value_001
    math_006.inputs[1].default_value = 0.5
    #Value_002
    math_006.inputs[2].default_value = 0.5
    
    #node Combine XYZ.001
    combine_xyz_001 = round.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz_001.name = "Combine XYZ.001"
    
    #node Group Input
    group_input = round.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    #round inputs
    #input Vector
    round.inputs.new('NodeSocketVector', "Vector")
    round.inputs[0].default_value = (0.0, 0.0, 0.0)
    round.inputs[0].min_value = -10000.0
    round.inputs[0].max_value = 10000.0
    round.inputs[0].attribute_domain = 'POINT'

    #node Group Output
    group_output = round.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    #round outputs
    #output Vector
    round.outputs.new('NodeSocketVector', "Vector")
    round.outputs[0].default_value = (0.0, 0.0, 0.0)
    round.outputs[0].min_value = -3.4028234663852886e+38
    round.outputs[0].max_value = 3.4028234663852886e+38
    round.outputs[0].attribute_domain = 'POINT'

    #Set locations
    separate_xyz_003.location = (-180.0001220703125, 59.620361328125)
    math_004.location = (0.0001220703125, 60.0)
    math_005.location = (0.0001220703125, 0.0)
    math_006.location = (0.0001220703125, -60.0)
    combine_xyz_001.location = (180.0001220703125, 60.0)
    group_input.location = (-380.0001220703125, -0.0)
    group_output.location = (370.0001220703125, -0.0)
    
    #Set dimensions
    separate_xyz_003.width, separate_xyz_003.height = 140.0, 100.0
    math_004.width, math_004.height = 140.0, 100.0
    math_005.width, math_005.height = 140.0, 100.0
    math_006.width, math_006.height = 140.0, 100.0
    combine_xyz_001.width, combine_xyz_001.height = 140.0, 100.0
    group_input.width, group_input.height = 140.0, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    
    #initialize round links
    #separate_xyz_003.X -> math_004.Value
    round.links.new(separate_xyz_003.outputs[0], math_004.inputs[0])
    #separate_xyz_003.Y -> math_005.Value
    round.links.new(separate_xyz_003.outputs[1], math_005.inputs[0])
    #separate_xyz_003.Z -> math_006.Value
    round.links.new(separate_xyz_003.outputs[2], math_006.inputs[0])
    #math_004.Value -> combine_xyz_001.X
    round.links.new(math_004.outputs[0], combine_xyz_001.inputs[0])
    #math_005.Value -> combine_xyz_001.Y
    round.links.new(math_005.outputs[0], combine_xyz_001.inputs[1])
    #math_006.Value -> combine_xyz_001.Z
    round.links.new(math_006.outputs[0], combine_xyz_001.inputs[2])
    #combine_xyz_001.Vector -> group_output.Vector
    round.links.new(combine_xyz_001.outputs[0], group_output.inputs[0])
    #group_input.Vector -> separate_xyz_003.Vector
    round.links.new(group_input.outputs[0], separate_xyz_003.inputs[0])
    return round





# ========================================================================================================== ### Manual Entry
# Modification 3.1 - 1: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
import bpy ### Manual Entry
from voxelity_pro.enums.name_constant import NameConstant
from voxelity_pro.utils.voxel.voxel_utils import VoxelUtils
 ### Manual Entry
def voxelize_node_group_3_1(node_group_name, min_value, max_value, default_value): ### Manual Entry
    voxelize = VoxelUtils.get_voxelity_node_group(node_group_name) ### Manual Entry
    if voxelize: ### Manual Entry
        return voxelize ### Manual Entry
    ### Manual Entry
    voxelize = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
    voxelize[node_group_name] = 1 # add a custom id with key of the voxelity group name ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.1 - 1: END ### Manual Entry
# ========================================================================================================== ### Manual Entry





    #initialize voxelize nodes
    #node Frame.002
    frame_002 = voxelize.nodes.new("NodeFrame")
    frame_002.label = "Mesh center"
    frame_002.name = "Frame.002"
    frame_002.label_size = 20
    frame_002.shrink = True
    
    #node Frame.003
    frame_003 = voxelize.nodes.new("NodeFrame")
    frame_003.label = "Voxel amount"
    frame_003.name = "Frame.003"
    frame_003.label_size = 20
    frame_003.shrink = True
    
    #node Frame.004
    frame_004 = voxelize.nodes.new("NodeFrame")
    frame_004.label = "Delta size to mesh"
    frame_004.name = "Frame.004"
    frame_004.label_size = 20
    frame_004.shrink = True
    
    #node Frame.005
    frame_005 = voxelize.nodes.new("NodeFrame")
    frame_005.label = "Recenter to boundings"
    frame_005.name = "Frame.005"
    frame_005.label_size = 20
    frame_005.shrink = True
    
    #node Frame.006
    frame_006 = voxelize.nodes.new("NodeFrame")
    frame_006.label = "In Z keep X/Y centers and min/max Z"
    frame_006.name = "Frame.006"
    frame_006.label_size = 20
    frame_006.shrink = True
    
    #node Frame.007
    frame_007 = voxelize.nodes.new("NodeFrame")
    frame_007.label = "Instanciate the X/Y grid along Z"
    frame_007.name = "Frame.007"
    frame_007.label_size = 20
    frame_007.shrink = True
    
    #node Frame.008
    frame_008 = voxelize.nodes.new("NodeFrame")
    frame_008.label = "the point grid to instanciate"
    frame_008.name = "Frame.008"
    frame_008.label_size = 20
    frame_008.shrink = True
    
    #node Frame.010
    frame_010 = voxelize.nodes.new("NodeFrame")
    frame_010.label = "Remove points that are too far"
    frame_010.name = "Frame.010"
    frame_010.label_size = 20
    frame_010.shrink = True
    
    #node Frame.011
    frame_011 = voxelize.nodes.new("NodeFrame")
    frame_011.label = "Considering the cube half diagonal sqrt(3)/2"
    frame_011.name = "Frame.011"
    frame_011.label_size = 20
    frame_011.shrink = True
    
    #node Frame.009
    frame_009 = voxelize.nodes.new("NodeFrame")
    frame_009.label = "Capture the centers"
    frame_009.name = "Frame.009"
    frame_009.label_size = 20
    frame_009.shrink = True
    
    #node Frame.012
    frame_012 = voxelize.nodes.new("NodeFrame")
    frame_012.label = "Place voxel cubes at center"
    frame_012.name = "Frame.012"
    frame_012.label_size = 20
    frame_012.shrink = True
    
    #node Frame.013
    frame_013 = voxelize.nodes.new("NodeFrame")
    frame_013.label = "Eventually realize and merge"
    frame_013.name = "Frame.013"
    frame_013.label_size = 20
    frame_013.shrink = True
    
    #node Frame.014
    frame_014 = voxelize.nodes.new("NodeFrame")
    frame_014.label = "Inner parts deleting attempt... does not work"
    frame_014.name = "Frame.014"
    frame_014.label_size = 20
    frame_014.shrink = True
    
    #node Reroute
    reroute = voxelize.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    #node Reroute.004
    reroute_004 = voxelize.nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
    #node Reroute.005
    reroute_005 = voxelize.nodes.new("NodeReroute")
    reroute_005.name = "Reroute.005"
    #node Vector Math.007
    vector_math_007 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_007.name = "Vector Math.007"
    vector_math_007.operation = 'SCALE'
    #Vector_001
    vector_math_007.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Vector_002
    vector_math_007.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_007.inputs[3].default_value = 0.5
    
    #node Reroute.001
    reroute_001 = voxelize.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    #node Vector Math.009
    vector_math_009 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_009.name = "Vector Math.009"
    vector_math_009.operation = 'SUBTRACT'
    #Vector_002
    vector_math_009.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_009.inputs[3].default_value = 0.5
    
    #node Vector Math.002
    vector_math_002 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'SUBTRACT'
    #Vector_002
    vector_math_002.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_002.inputs[3].default_value = 1.0
    
    #node Reroute.002
    reroute_002 = voxelize.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    #node Group Input.001
    group_input_001 = voxelize.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    #voxelize inputs
    #input Mesh
    voxelize.inputs.new('NodeSocketGeometry', "Mesh")
    voxelize.inputs[0].attribute_domain = 'POINT'
    
    #input Voxel Size
    voxelize.inputs.new('NodeSocketFloat', "Voxel Size")





# ========================================================================================================== ### Manual Entry
# Modification 3.1 - 2: Assign default_value, min_value, max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
    voxelize.inputs[1].default_value = default_value ### Manual Entry
    voxelize.inputs[1].min_value = min_value ### Manual Entry
    voxelize.inputs[1].max_value = max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.1 - 2: END ### Manual Entry
# ========================================================================================================== ### Manual Entry





    voxelize.inputs[1].attribute_domain = 'POINT'

    #node Reroute.003
    reroute_003 = voxelize.nodes.new("NodeReroute")
    reroute_003.name = "Reroute.003"
    #node Reroute.006
    reroute_006 = voxelize.nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    #node Bounding Box
    bounding_box = voxelize.nodes.new("GeometryNodeBoundBox")
    bounding_box.name = "Bounding Box"
    
    #node Group Input.003
    group_input_003 = voxelize.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    
    #node Vector Math.006
    vector_math_006 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_006.name = "Vector Math.006"
    vector_math_006.operation = 'SUBTRACT'
    #Vector_002
    vector_math_006.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_006.inputs[3].default_value = 1.0
    
    #node Separate XYZ.001
    separate_xyz_001 = voxelize.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_001.name = "Separate XYZ.001"
    
    #node Mesh Line
    mesh_line = voxelize.nodes.new("GeometryNodeMeshLine")
    mesh_line.name = "Mesh Line"
    mesh_line.count_mode = 'TOTAL'
    mesh_line.mode = 'END_POINTS'
    #Resolution
    mesh_line.inputs[1].default_value = 1.0
    
    #node Separate XYZ.002
    separate_xyz_002 = voxelize.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz_002.name = "Separate XYZ.002"
    
    #node Vector Math.010
    vector_math_010 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_010.name = "Vector Math.010"
    vector_math_010.operation = 'SUBTRACT'
    #Vector_002
    vector_math_010.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_010.inputs[3].default_value = 1.0
    
    #node Vector Math.003
    vector_math_003 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.operation = 'DIVIDE'
    #Vector_002
    vector_math_003.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_003.inputs[3].default_value = 1.0
    
    #node Vector Math.004
    vector_math_004 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_004.name = "Vector Math.004"
    vector_math_004.operation = 'ADD'
    #Vector_002
    vector_math_004.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_004.inputs[3].default_value = 1.0
    
    #node Vector Math.005
    vector_math_005 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_005.name = "Vector Math.005"
    vector_math_005.operation = 'SCALE'
    #Vector_001
    vector_math_005.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Vector_002
    vector_math_005.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_005.inputs[3].default_value = 0.5
    
    #node Vector Math.017
    vector_math_017 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_017.name = "Vector Math.017"
    vector_math_017.operation = 'ADD'
    #Vector_002
    vector_math_017.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_017.inputs[3].default_value = 1.0
    
    #node Vector Math.018
    vector_math_018 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_018.name = "Vector Math.018"
    vector_math_018.operation = 'ADD'
    #Vector_002
    vector_math_018.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_018.inputs[3].default_value = 1.0
    
    #node Group Input.004
    group_input_004 = voxelize.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    
    #node Reroute.008
    reroute_008 = voxelize.nodes.new("NodeReroute")
    reroute_008.name = "Reroute.008"
    #node Vector Math.008
    vector_math_008 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_008.name = "Vector Math.008"
    vector_math_008.operation = 'ADD'
    #Vector_002
    vector_math_008.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_008.inputs[3].default_value = 0.5
    
    #node Vector Math.013
    vector_math_013 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_013.name = "Vector Math.013"
    vector_math_013.operation = 'MULTIPLY'
    #Vector_001
    vector_math_013.inputs[1].default_value = (0.0, 0.0, 1.0)
    #Vector_002
    vector_math_013.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_013.inputs[3].default_value = 0.5
    
    #node Vector Math.011
    vector_math_011 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_011.name = "Vector Math.011"
    vector_math_011.operation = 'SCALE'
    #Vector_001
    vector_math_011.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Vector_002
    vector_math_011.inputs[2].default_value = (0.0, 0.0, 0.0)
    
    #node Group
    group = voxelize.nodes.new("GeometryNodeGroup")
    group.name = "Group"
    group.node_tree = round_node_group_3_1()
    
    #node Vector Math.014
    vector_math_014 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_014.name = "Vector Math.014"
    vector_math_014.operation = 'SUBTRACT'
    #Vector_001
    vector_math_014.inputs[1].default_value = (1.0, 1.0, 1.0)
    #Vector_002
    vector_math_014.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_014.inputs[3].default_value = 0.5
    
    #node Reroute.007
    reroute_007 = voxelize.nodes.new("NodeReroute")
    reroute_007.name = "Reroute.007"
    #node Vector Math.012
    vector_math_012 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_012.name = "Vector Math.012"
    vector_math_012.operation = 'MULTIPLY'
    #Vector_001
    vector_math_012.inputs[1].default_value = (0.0, 0.0, 1.0)
    #Vector_002
    vector_math_012.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_012.inputs[3].default_value = 0.5
    
    #node Vector Math.016
    vector_math_016 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_016.name = "Vector Math.016"
    vector_math_016.operation = 'MULTIPLY'
    #Vector_001
    vector_math_016.inputs[1].default_value = (1.0, 1.0, 0.0)
    #Vector_002
    vector_math_016.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_016.inputs[3].default_value = 1.0
    
    #node Grid
    grid = voxelize.nodes.new("GeometryNodeMeshGrid")
    grid.name = "Grid"
    
    #node Delete Geometry.005
    delete_geometry_005 = voxelize.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_005.name = "Delete Geometry.005"
    delete_geometry_005.domain = 'EDGE'
    delete_geometry_005.mode = 'EDGE_FACE'
    #Selection
    delete_geometry_005.inputs[1].default_value = True
    
    #node Delete Geometry.002
    delete_geometry_002 = voxelize.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry_002.name = "Delete Geometry.002"
    delete_geometry_002.domain = 'POINT'






    if bpy.app.version >= (3,2,0):
        delete_geometry_002.mode = 'ALL'







    #node Group Input.011
    group_input_011 = voxelize.nodes.new("NodeGroupInput")
    group_input_011.name = "Group Input.011"
    
    #node Cube.002
    cube_002 = voxelize.nodes.new("GeometryNodeMeshCube")
    cube_002.name = "Cube.002"
    #Vertices X
    cube_002.inputs[1].default_value = 2
    #Vertices Y
    cube_002.inputs[2].default_value = 2
    #Vertices Z
    cube_002.inputs[3].default_value = 2
    
    #node Instance on Points.003
    instance_on_points_003 = voxelize.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points_003.name = "Instance on Points.003"
    #Selection
    instance_on_points_003.inputs[1].default_value = True
    #Pick Instance
    instance_on_points_003.inputs[3].default_value = False
    #Instance Index
    instance_on_points_003.inputs[4].default_value = 0
    #Rotation
    instance_on_points_003.inputs[5].default_value = (0.0, 0.0, 0.0)
    #Scale
    instance_on_points_003.inputs[6].default_value = (1.0, 1.0, 1.0)
    
    #node Realize Instances.002
    realize_instances_002 = voxelize.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_002.name = "Realize Instances.002"






    if bpy.app.version >= (3,1,0):
        realize_instances_002.legacy_behavior = False
    






    #node Realize Instances.001
    realize_instances_001 = voxelize.nodes.new("GeometryNodeRealizeInstances")
    realize_instances_001.name = "Realize Instances.001"






    if bpy.app.version >= (3,1,0):
        realize_instances_001.legacy_behavior = False







    #node Instance on Points
    instance_on_points = voxelize.nodes.new("GeometryNodeInstanceOnPoints")
    instance_on_points.name = "Instance on Points"
    #Selection
    instance_on_points.inputs[1].default_value = True
    #Pick Instance
    instance_on_points.inputs[3].default_value = False
    #Instance Index
    instance_on_points.inputs[4].default_value = 0
    #Rotation
    instance_on_points.inputs[5].default_value = (0.0, 0.0, 0.0)
    #Scale
    instance_on_points.inputs[6].default_value = (1.0, 1.0, 1.0)
    
    #node Geometry Proximity.001
    geometry_proximity_001 = voxelize.nodes.new("GeometryNodeProximity")
    geometry_proximity_001.name = "Geometry Proximity.001"
    geometry_proximity_001.target_element = 'FACES'
    
    #node Group Input.009
    group_input_009 = voxelize.nodes.new("NodeGroupInput")
    group_input_009.name = "Group Input.009"
    
    #node Compare.001
    compare_001 = voxelize.nodes.new("FunctionNodeCompare")
    compare_001.name = "Compare.001"
    compare_001.data_type = 'FLOAT'
    compare_001.mode = 'ELEMENT'
    compare_001.operation = 'GREATER_THAN'
    #A_INT
    compare_001.inputs[2].default_value = 0
    #B_INT
    compare_001.inputs[3].default_value = 0
    #A_VEC3
    compare_001.inputs[4].default_value = (0.0, 0.0, 0.0)
    #B_VEC3
    compare_001.inputs[5].default_value = (0.0, 0.0, 0.0)
    #A_COL
    compare_001.inputs[6].default_value = (0.0, 0.0, 0.0, 0.0)
    #B_COL
    compare_001.inputs[7].default_value = (0.0, 0.0, 0.0, 0.0)
    #A_STR
    compare_001.inputs[8].default_value = ""
    #B_STR
    compare_001.inputs[9].default_value = ""
    #C
    compare_001.inputs[10].default_value = 0.8999999761581421
    #Angle
    compare_001.inputs[11].default_value = 0.08726649731397629
    #Epsilon
    compare_001.inputs[12].default_value = 0.0010000000474974513
    
    #node Position.003
    position_003 = voxelize.nodes.new("GeometryNodeInputPosition")
    position_003.name = "Position.003"
    
    #node Group Input.010
    group_input_010 = voxelize.nodes.new("NodeGroupInput")
    group_input_010.name = "Group Input.010"
    
    #node Position.001
    position_001 = voxelize.nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    
    #node Math.004
    math_004_1 = voxelize.nodes.new("ShaderNodeMath")
    math_004_1.name = "Math.004"
    math_004_1.operation = 'MULTIPLY'
    math_004_1.use_clamp = False
    #Value_001
    math_004_1.inputs[1].default_value = 0.8660253882408142
    #Value_002
    math_004_1.inputs[2].default_value = 0.5
    
    #node Capture Attribute
    capture_attribute = voxelize.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.data_type = 'FLOAT_VECTOR'
    capture_attribute.domain = 'POINT'
    #Value_001
    capture_attribute.inputs[2].default_value = 0.0
    #Value_002
    capture_attribute.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    #Value_003
    capture_attribute.inputs[4].default_value = False
    #Value_004
    capture_attribute.inputs[5].default_value = 0
    
    #node Group Output
    group_output_1 = voxelize.nodes.new("NodeGroupOutput")
    group_output_1.name = "Group Output"
    group_output_1.is_active_output = True
    #voxelize outputs
    #output Geometry
    voxelize.outputs.new('NodeSocketGeometry', "Geometry")
    voxelize.outputs[0].attribute_domain = 'POINT'
    
    
    
    #node Reroute.010
    reroute_010 = voxelize.nodes.new("NodeReroute")
    reroute_010.name = "Reroute.010"
    #node Vector Math.020
    vector_math_020 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_020.name = "Vector Math.020"
    vector_math_020.operation = 'DOT_PRODUCT'
    #Vector_002
    vector_math_020.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_020.inputs[3].default_value = 1.0
    
    #node Compare
    compare = voxelize.nodes.new("FunctionNodeCompare")
    compare.name = "Compare"
    compare.data_type = 'FLOAT'
    compare.mode = 'ELEMENT'
    compare.operation = 'GREATER_THAN'
    #B
    compare.inputs[1].default_value = 0.0
    #A_INT
    compare.inputs[2].default_value = 0
    #B_INT
    compare.inputs[3].default_value = 0
    #A_VEC3
    compare.inputs[4].default_value = (0.0, 0.0, 0.0)
    #B_VEC3
    compare.inputs[5].default_value = (0.0, 0.0, 0.0)
    #A_COL
    compare.inputs[6].default_value = (0.0, 0.0, 0.0, 0.0)
    #B_COL
    compare.inputs[7].default_value = (0.0, 0.0, 0.0, 0.0)
    #A_STR
    compare.inputs[8].default_value = ""
    #B_STR
    compare.inputs[9].default_value = ""
    #C
    compare.inputs[10].default_value = 0.8999999761581421
    #Angle
    compare.inputs[11].default_value = 0.08726649731397629
    #Epsilon
    compare.inputs[12].default_value = 0.0010000000474974513
    
    #node Boolean Math
    boolean_math = voxelize.nodes.new("FunctionNodeBooleanMath")
    boolean_math.name = "Boolean Math"
    boolean_math.operation = 'AND'
    
    #node Vector Math.015
    vector_math_015 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_015.name = "Vector Math.015"
    vector_math_015.operation = 'SUBTRACT'
    #Vector_002
    vector_math_015.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_015.inputs[3].default_value = 1.0
    
    #node Reroute.009
    reroute_009 = voxelize.nodes.new("NodeReroute")
    reroute_009.name = "Reroute.009"
    #node Vector Math.019
    vector_math_019 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_019.name = "Vector Math.019"
    vector_math_019.operation = 'NORMALIZE'
    #Vector_001
    vector_math_019.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Vector_002
    vector_math_019.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_019.inputs[3].default_value = 1.0
    
    #node Vector Math.021
    vector_math_021 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_021.name = "Vector Math.021"
    vector_math_021.operation = 'SCALE'
    #Vector_001
    vector_math_021.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Vector_002
    vector_math_021.inputs[2].default_value = (0.0, 0.0, 0.0)
    
    #node Position.004
    position_004 = voxelize.nodes.new("GeometryNodeInputPosition")
    position_004.name = "Position.004"
    
    #node Vector Math.022
    vector_math_022 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_022.name = "Vector Math.022"
    vector_math_022.operation = 'ADD'
    #Vector_002
    vector_math_022.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_022.inputs[3].default_value = 1.0
    
    #node Position.002
    position_002 = voxelize.nodes.new("GeometryNodeInputPosition")
    position_002.name = "Position.002"
    
    #node Raycast
    raycast = voxelize.nodes.new("GeometryNodeRaycast")
    raycast.name = "Raycast"
    raycast.data_type = 'FLOAT'
    raycast.mapping = 'INTERPOLATED'
    #Attribute
    raycast.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Attribute_001
    raycast.inputs[2].default_value = 0.0
    #Attribute_002
    raycast.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    #Attribute_003
    raycast.inputs[4].default_value = False
    #Attribute_004
    raycast.inputs[5].default_value = 0
    #Ray Length
    raycast.inputs[8].default_value = 100.0
    
    #node Group Input.002
    group_input_002 = voxelize.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"
    
    #node Group Input.005
    group_input_005 = voxelize.nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    
    #node Math.003
    math_003 = voxelize.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'MULTIPLY_ADD'
    math_003.use_clamp = False
    #Value_001
    math_003.inputs[1].default_value = 1.7320507764816284
    
    #node Compare.002
    compare_002 = voxelize.nodes.new("FunctionNodeCompare")
    compare_002.name = "Compare.002"
    compare_002.data_type = 'FLOAT'
    compare_002.mode = 'ELEMENT'
    compare_002.operation = 'LESS_THAN'
    #A_INT
    compare_002.inputs[2].default_value = 0
    #B_INT
    compare_002.inputs[3].default_value = 0
    #A_VEC3
    compare_002.inputs[4].default_value = (0.0, 0.0, 0.0)
    #B_VEC3
    compare_002.inputs[5].default_value = (0.0, 0.0, 0.0)
    #A_COL
    compare_002.inputs[6].default_value = (0.0, 0.0, 0.0, 0.0)
    #B_COL
    compare_002.inputs[7].default_value = (0.0, 0.0, 0.0, 0.0)
    #A_STR
    compare_002.inputs[8].default_value = ""
    #B_STR
    compare_002.inputs[9].default_value = ""
    #C
    compare_002.inputs[10].default_value = 0.8999999761581421
    #Angle
    compare_002.inputs[11].default_value = 0.08726649731397629
    #Epsilon
    compare_002.inputs[12].default_value = 0.0010000000474974513
    
    #node Boolean Math.001
    boolean_math_001 = voxelize.nodes.new("FunctionNodeBooleanMath")
    boolean_math_001.name = "Boolean Math.001"
    boolean_math_001.operation = 'AND'
    
    #node Math.005
    math_005_1 = voxelize.nodes.new("ShaderNodeMath")
    math_005_1.name = "Math.005"
    math_005_1.operation = 'MULTIPLY'
    math_005_1.use_clamp = False
    #Value_001
    math_005_1.inputs[1].default_value = -1.0
    #Value_002
    math_005_1.inputs[2].default_value = 0.5
    
    #node Math.006
    math_006_1 = voxelize.nodes.new("ShaderNodeMath")
    math_006_1.name = "Math.006"
    math_006_1.operation = 'MULTIPLY'
    math_006_1.use_clamp = False
    #Value_001
    math_006_1.inputs[1].default_value = 2.0
    #Value_002
    math_006_1.inputs[2].default_value = 0.5
    
    #node Merge by Distance.002
    merge_by_distance_002 = voxelize.nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance_002.name = "Merge by Distance.002"





    if bpy.app.version >= (3,2,0):
        merge_by_distance_002.mode = 'ALL'







    #Selection
    merge_by_distance_002.inputs[1].default_value = True
    #Distance
    merge_by_distance_002.inputs[2].default_value = 0.0010000000474974513
    
    #node Value
    value = voxelize.nodes.new("ShaderNodeValue")
    value.name = "Value"
    
    value.outputs[0].default_value = 9.999999747378752e-05
    #Set parents
    reroute_010.parent = frame_014
    vector_math_020.parent = frame_014
    compare.parent = frame_014
    boolean_math.parent = frame_014
    vector_math_015.parent = frame_014
    reroute_009.parent = frame_014
    vector_math_019.parent = frame_014
    vector_math_021.parent = frame_014
    position_004.parent = frame_014
    vector_math_022.parent = frame_014
    position_002.parent = frame_014
    raycast.parent = frame_014
    group_input_002.parent = frame_014
    group_input_005.parent = frame_014
    math_003.parent = frame_014
    compare_002.parent = frame_014
    boolean_math_001.parent = frame_014
    math_005_1.parent = frame_014
    math_006_1.parent = frame_014
    value.parent = frame_014
    
    #Set locations
    frame_002.location = (-1435.37255859375, 1390.767822265625)
    frame_003.location = (-1253.57763671875, 1049.769287109375)
    frame_004.location = (-707.0185546875, 1040.0)
    frame_005.location = (-261.1684265136719, 1040.0)
    frame_006.location = (-99.99951171875, 1564.0345458984375)
    frame_007.location = (370.64453125, 1480.0)
    frame_008.location = (360.0000305175781, 1180.0)
    frame_010.location = (1140.0, 1160.0)
    frame_011.location = (1040.0, 880.0)
    frame_009.location = (980.0, 1460.0)
    frame_012.location = (1720.0, 1460.0)
    frame_013.location = (2080.0, 1460.0)
    frame_014.location = (-30.0, 10.0)
    reroute.location = (-842.562255859375, -409.3598937988281)
    reroute_004.location = (-400.0, 660.0)
    reroute_005.location = (-400.0, 700.0)
    vector_math_007.location = (-440.0, 940.0)
    reroute_001.location = (-680.0, 760.0)
    vector_math_009.location = (-259.9998779296875, 940.0)
    vector_math_002.location = (-1540.0, 940.0)
    reroute_002.location = (-1340.0, 760.0)
    group_input_001.location = (-1880.0, 940.0)
    reroute_003.location = (-1520.0, 660.0)
    reroute_006.location = (-1520.0, 700.0)
    bounding_box.location = (-1740.0, 940.0)
    group_input_003.location = (-1500.0, 1060.0)
    vector_math_006.location = (-620.0, 940.0)
    separate_xyz_001.location = (99.99993896484375, 1080.0)
    mesh_line.location = (280.0, 1360.0)
    separate_xyz_002.location = (100.0, 940.0)
    vector_math_010.location = (-80.0, 940.0)
    vector_math_003.location = (-1340.0, 940.0)
    vector_math_004.location = (-1520.0006103515625, 1284.9425048828125)
    vector_math_005.location = (-1340.0, 1280.0)
    vector_math_017.location = (100.0, 1460.0)
    vector_math_018.location = (100.0, 1300.0)
    group_input_004.location = (-959.99951171875, 1174.649658203125)
    reroute_008.location = (40.0, 1080.0)
    vector_math_008.location = (-259.9998779296875, 780.0)
    vector_math_013.location = (-80.0, 1260.0)
    vector_math_011.location = (-800.0, 940.0)
    group.location = (-1160.0, 940.0)
    vector_math_014.location = (-980.0, 940.0)
    reroute_007.location = (-800.0, 1080.0)
    vector_math_012.location = (-79.99993896484375, 1400.0)
    vector_math_016.location = (-260.0, 1400.0)
    grid.location = (280.0, 1080.0)
    delete_geometry_005.location = (460.0, 1080.0)
    delete_geometry_002.location = (1420.0, 1360.0)
    group_input_011.location = (1480.0, 1160.0)
    cube_002.location = (1620.0, 1160.0)
    instance_on_points_003.location = (1820.0, 1360.0)
    realize_instances_002.location = (2000.0, 1360.0)
    realize_instances_001.location = (900.0, 1360.0)
    instance_on_points.location = (660.0, 1360.0)
    geometry_proximity_001.location = (1080.0, 1060.0)
    group_input_009.location = (940.0, 1060.0)
    compare_001.location = (1260.0, 1060.0)
    position_003.location = (900.0, 920.0)
    group_input_010.location = (940.0, 780.0)
    position_001.location = (900.0, 1240.0)
    math_004_1.location = (1080.0, 780.0)
    capture_attribute.location = (1080.0, 1360.0)
    group_output_1.location = (2360.0, 1380.0)
    reroute_010.location = (2030.0, 1530.0)
    vector_math_020.location = (2310.0, 1790.0)
    compare.location = (2490.0, 1790.0)
    boolean_math.location = (2870.0, 1970.0)
    vector_math_015.location = (1450.0, 1650.0)
    reroute_009.location = (2170.0, 1530.0)
    vector_math_019.location = (1630.0, 1650.0)
    vector_math_021.location = (1630.0, 1810.0)
    position_004.location = (1630.0, 1890.0)
    vector_math_022.location = (1810.0, 1810.0)
    position_002.location = (1130.0, 1650.0)
    raycast.location = (2030.0, 1990.0)
    group_input_002.location = (1630.0, 2010.0)
    group_input_005.location = (2029.99951171875, 2142.015869140625)
    math_003.location = (2230.0, 2130.0)
    compare_002.location = (2490.0, 1990.0)
    boolean_math_001.location = (2690.0, 1950.0)
    math_005_1.location = (1450.0, 2110.0)
    math_006_1.location = (1670.0, 2210.0)
    merge_by_distance_002.location = (2180.0, 1360.0)
    value.location = (1249.99951171875, 2107.372802734375)
    
    #Set dimensions
    frame_002.width, frame_002.height = 319.25537109375, 41.501953125
    frame_003.width, frame_003.height = 332.10015869140625, 44.8072509765625
    frame_004.width, frame_004.height = 320.4057312011719, 44.80718994140625
    frame_005.width, frame_005.height = 496.77972412109375, 44.80718994140625
    frame_006.width, frame_006.height = 496.77972412109375, 44.80712890625
    frame_007.width, frame_007.height = 318.06884765625, 44.80712890625
    frame_008.width, frame_008.height = 318.0688171386719, 44.80712890625
    frame_010.width, frame_010.height = 318.06884765625, 44.80712890625
    frame_011.width, frame_011.height = 566.617431640625, 44.80712890625
    frame_009.width, frame_009.height = 318.06884765625, 44.80712890625
    frame_012.width, frame_012.height = 318.06884765625, 44.80712890625
    frame_013.width, frame_013.height = 318.06884765625, 44.80712890625
    frame_014.width, frame_014.height = 1940.0, 751.0
    reroute.width, reroute.height = 16.0, 100.0
    reroute_004.width, reroute_004.height = 16.0, 100.0
    reroute_005.width, reroute_005.height = 16.0, 100.0
    vector_math_007.width, vector_math_007.height = 140.0, 100.0
    reroute_001.width, reroute_001.height = 16.0, 100.0
    vector_math_009.width, vector_math_009.height = 140.0, 100.0
    vector_math_002.width, vector_math_002.height = 140.0, 100.0
    reroute_002.width, reroute_002.height = 16.0, 100.0
    group_input_001.width, group_input_001.height = 100.3353271484375, 100.0
    reroute_003.width, reroute_003.height = 16.0, 100.0
    reroute_006.width, reroute_006.height = 16.0, 100.0
    bounding_box.width, bounding_box.height = 140.0, 100.0
    group_input_003.width, group_input_003.height = 100.3353271484375, 100.0
    vector_math_006.width, vector_math_006.height = 140.0, 100.0
    separate_xyz_001.width, separate_xyz_001.height = 140.0, 100.0
    mesh_line.width, mesh_line.height = 140.0, 100.0
    separate_xyz_002.width, separate_xyz_002.height = 140.0, 100.0
    vector_math_010.width, vector_math_010.height = 140.0, 100.0
    vector_math_003.width, vector_math_003.height = 140.0, 100.0
    vector_math_004.width, vector_math_004.height = 140.0, 100.0
    vector_math_005.width, vector_math_005.height = 140.0, 100.0
    vector_math_017.width, vector_math_017.height = 140.0, 100.0
    vector_math_018.width, vector_math_018.height = 140.0, 100.0
    group_input_004.width, group_input_004.height = 100.3353271484375, 100.0
    reroute_008.width, reroute_008.height = 16.0, 100.0
    vector_math_008.width, vector_math_008.height = 140.0, 100.0
    vector_math_013.width, vector_math_013.height = 140.0, 100.0
    vector_math_011.width, vector_math_011.height = 140.0, 100.0
    group.width, group.height = 140.0, 100.0
    vector_math_014.width, vector_math_014.height = 140.0, 100.0
    reroute_007.width, reroute_007.height = 16.0, 100.0
    vector_math_012.width, vector_math_012.height = 140.0, 100.0
    vector_math_016.width, vector_math_016.height = 140.0, 100.0
    grid.width, grid.height = 140.0, 100.0
    delete_geometry_005.width, delete_geometry_005.height = 140.0, 100.0
    delete_geometry_002.width, delete_geometry_002.height = 140.0, 100.0
    group_input_011.width, group_input_011.height = 100.3353271484375, 100.0
    cube_002.width, cube_002.height = 140.0, 100.0
    instance_on_points_003.width, instance_on_points_003.height = 140.0, 100.0
    realize_instances_002.width, realize_instances_002.height = 140.0, 100.0
    realize_instances_001.width, realize_instances_001.height = 140.0, 100.0
    instance_on_points.width, instance_on_points.height = 140.0, 100.0
    geometry_proximity_001.width, geometry_proximity_001.height = 140.0, 100.0
    group_input_009.width, group_input_009.height = 100.3353271484375, 100.0
    compare_001.width, compare_001.height = 140.0, 100.0
    position_003.width, position_003.height = 140.0, 100.0
    group_input_010.width, group_input_010.height = 100.3353271484375, 100.0
    position_001.width, position_001.height = 140.0, 100.0
    math_004_1.width, math_004_1.height = 140.0, 100.0
    capture_attribute.width, capture_attribute.height = 140.0, 100.0
    group_output_1.width, group_output_1.height = 140.0, 100.0
    reroute_010.width, reroute_010.height = 16.0, 100.0
    vector_math_020.width, vector_math_020.height = 140.0, 100.0
    compare.width, compare.height = 140.0, 100.0
    boolean_math.width, boolean_math.height = 140.0, 100.0
    vector_math_015.width, vector_math_015.height = 140.0, 100.0
    reroute_009.width, reroute_009.height = 16.0, 100.0
    vector_math_019.width, vector_math_019.height = 140.0, 100.0
    vector_math_021.width, vector_math_021.height = 140.0, 100.0
    position_004.width, position_004.height = 140.0, 100.0
    vector_math_022.width, vector_math_022.height = 140.0, 100.0
    position_002.width, position_002.height = 140.0, 100.0
    raycast.width, raycast.height = 150.0, 100.0
    group_input_002.width, group_input_002.height = 140.0, 100.0
    group_input_005.width, group_input_005.height = 140.0, 100.0
    math_003.width, math_003.height = 140.0, 100.0
    compare_002.width, compare_002.height = 140.0, 100.0
    boolean_math_001.width, boolean_math_001.height = 140.0, 100.0
    math_005_1.width, math_005_1.height = 140.0, 100.0
    math_006_1.width, math_006_1.height = 140.0, 100.0
    merge_by_distance_002.width, merge_by_distance_002.height = 140.0, 100.0
    value.width, value.height = 140.0, 100.0
    
    #initialize voxelize links
    #group_input_001.Mesh -> bounding_box.Geometry
    voxelize.links.new(group_input_001.outputs[0], bounding_box.inputs[0])
    #bounding_box.Max -> vector_math_002.Vector
    voxelize.links.new(bounding_box.outputs[2], vector_math_002.inputs[0])
    #bounding_box.Min -> vector_math_002.Vector
    voxelize.links.new(bounding_box.outputs[1], vector_math_002.inputs[1])
    #vector_math_002.Vector -> vector_math_003.Vector
    voxelize.links.new(vector_math_002.outputs[0], vector_math_003.inputs[0])
    #mesh_line.Mesh -> instance_on_points.Points
    voxelize.links.new(mesh_line.outputs[0], instance_on_points.inputs[0])
    #delete_geometry_005.Geometry -> instance_on_points.Instance
    voxelize.links.new(delete_geometry_005.outputs[0], instance_on_points.inputs[2])
    #vector_math_011.Vector -> vector_math_006.Vector
    voxelize.links.new(vector_math_011.outputs[0], vector_math_006.inputs[0])
    #reroute_001.Output -> vector_math_006.Vector
    voxelize.links.new(reroute_001.outputs[0], vector_math_006.inputs[1])
    #group_input_003.Voxel Size -> vector_math_003.Vector
    voxelize.links.new(group_input_003.outputs[1], vector_math_003.inputs[1])
    #reroute_002.Output -> reroute_001.Input
    voxelize.links.new(reroute_002.outputs[0], reroute_001.inputs[0])
    #vector_math_002.Vector -> reroute_002.Input
    voxelize.links.new(vector_math_002.outputs[0], reroute_002.inputs[0])
    #vector_math_006.Vector -> vector_math_007.Vector
    voxelize.links.new(vector_math_006.outputs[0], vector_math_007.inputs[0])
    #bounding_box.Max -> reroute_003.Input
    voxelize.links.new(bounding_box.outputs[2], reroute_003.inputs[0])
    #reroute_003.Output -> reroute_004.Input
    voxelize.links.new(reroute_003.outputs[0], reroute_004.inputs[0])
    #vector_math_007.Vector -> vector_math_009.Vector
    voxelize.links.new(vector_math_007.outputs[0], vector_math_009.inputs[1])
    #reroute_005.Output -> vector_math_009.Vector
    voxelize.links.new(reroute_005.outputs[0], vector_math_009.inputs[0])
    #reroute_006.Output -> reroute_005.Input
    voxelize.links.new(reroute_006.outputs[0], reroute_005.inputs[0])
    #bounding_box.Min -> reroute_006.Input
    voxelize.links.new(bounding_box.outputs[1], reroute_006.inputs[0])
    #separate_xyz_001.X -> grid.Vertices X
    voxelize.links.new(separate_xyz_001.outputs[0], grid.inputs[2])
    #separate_xyz_001.Y -> grid.Vertices Y
    voxelize.links.new(separate_xyz_001.outputs[1], grid.inputs[3])
    #vector_math_008.Vector -> vector_math_010.Vector
    voxelize.links.new(vector_math_008.outputs[0], vector_math_010.inputs[0])
    #vector_math_009.Vector -> vector_math_010.Vector
    voxelize.links.new(vector_math_009.outputs[0], vector_math_010.inputs[1])
    #separate_xyz_002.X -> grid.Size X
    voxelize.links.new(separate_xyz_002.outputs[0], grid.inputs[0])
    #separate_xyz_002.Y -> grid.Size Y
    voxelize.links.new(separate_xyz_002.outputs[1], grid.inputs[1])
    #group_input_004.Voxel Size -> vector_math_011.Scale
    voxelize.links.new(group_input_004.outputs[1], vector_math_011.inputs[3])
    #separate_xyz_001.Z -> mesh_line.Count
    voxelize.links.new(separate_xyz_001.outputs[2], mesh_line.inputs[0])
    #reroute_008.Output -> separate_xyz_001.Vector
    voxelize.links.new(reroute_008.outputs[0], separate_xyz_001.inputs[0])
    #vector_math_009.Vector -> vector_math_012.Vector
    voxelize.links.new(vector_math_009.outputs[0], vector_math_012.inputs[0])
    #vector_math_008.Vector -> vector_math_013.Vector
    voxelize.links.new(vector_math_008.outputs[0], vector_math_013.inputs[0])
    #vector_math_003.Vector -> group.Vector
    voxelize.links.new(vector_math_003.outputs[0], group.inputs[0])
    #bounding_box.Max -> vector_math_004.Vector
    voxelize.links.new(bounding_box.outputs[2], vector_math_004.inputs[1])
    #bounding_box.Min -> vector_math_004.Vector
    voxelize.links.new(bounding_box.outputs[1], vector_math_004.inputs[0])
    #vector_math_004.Vector -> vector_math_005.Vector
    voxelize.links.new(vector_math_004.outputs[0], vector_math_005.inputs[0])
    #vector_math_005.Vector -> vector_math_016.Vector
    voxelize.links.new(vector_math_005.outputs[0], vector_math_016.inputs[0])
    #vector_math_012.Vector -> vector_math_017.Vector
    voxelize.links.new(vector_math_012.outputs[0], vector_math_017.inputs[0])
    #vector_math_017.Vector -> mesh_line.Start Location
    voxelize.links.new(vector_math_017.outputs[0], mesh_line.inputs[2])
    #vector_math_016.Vector -> vector_math_017.Vector
    voxelize.links.new(vector_math_016.outputs[0], vector_math_017.inputs[1])
    #vector_math_016.Vector -> vector_math_018.Vector
    voxelize.links.new(vector_math_016.outputs[0], vector_math_018.inputs[1])
    #vector_math_013.Vector -> vector_math_018.Vector
    voxelize.links.new(vector_math_013.outputs[0], vector_math_018.inputs[0])
    #vector_math_018.Vector -> mesh_line.Offset
    voxelize.links.new(vector_math_018.outputs[0], mesh_line.inputs[3])
    #group.Vector -> reroute_007.Input
    voxelize.links.new(group.outputs[0], reroute_007.inputs[0])
    #reroute_004.Output -> vector_math_008.Vector
    voxelize.links.new(reroute_004.outputs[0], vector_math_008.inputs[0])
    #vector_math_007.Vector -> vector_math_008.Vector
    voxelize.links.new(vector_math_007.outputs[0], vector_math_008.inputs[1])
    #vector_math_010.Vector -> separate_xyz_002.Vector
    voxelize.links.new(vector_math_010.outputs[0], separate_xyz_002.inputs[0])
    #group.Vector -> vector_math_014.Vector
    voxelize.links.new(group.outputs[0], vector_math_014.inputs[0])
    #vector_math_014.Vector -> vector_math_011.Vector
    voxelize.links.new(vector_math_014.outputs[0], vector_math_011.inputs[0])
    #reroute_007.Output -> reroute_008.Input
    voxelize.links.new(reroute_007.outputs[0], reroute_008.inputs[0])
    #instance_on_points.Instances -> realize_instances_001.Geometry
    voxelize.links.new(instance_on_points.outputs[0], realize_instances_001.inputs[0])
    #group_input_009.Mesh -> geometry_proximity_001.Target
    voxelize.links.new(group_input_009.outputs[0], geometry_proximity_001.inputs[0])
    #position_003.Position -> geometry_proximity_001.Source Position
    voxelize.links.new(position_003.outputs[0], geometry_proximity_001.inputs[1])
    #compare_001.Result -> delete_geometry_002.Selection
    voxelize.links.new(compare_001.outputs[0], delete_geometry_002.inputs[1])
    #geometry_proximity_001.Distance -> compare_001.A
    voxelize.links.new(geometry_proximity_001.outputs[1], compare_001.inputs[0])
    #group_input_010.Voxel Size -> math_004_1.Value
    voxelize.links.new(group_input_010.outputs[1], math_004_1.inputs[0])
    #math_004_1.Value -> compare_001.B
    voxelize.links.new(math_004_1.outputs[0], compare_001.inputs[1])
    #capture_attribute.Geometry -> delete_geometry_002.Geometry
    voxelize.links.new(capture_attribute.outputs[0], delete_geometry_002.inputs[0])
    #group_input_011.Voxel Size -> cube_002.Size
    voxelize.links.new(group_input_011.outputs[1], cube_002.inputs[0])
    #cube_002.Mesh -> instance_on_points_003.Instance
    voxelize.links.new(cube_002.outputs[0], instance_on_points_003.inputs[2])
    #delete_geometry_002.Geometry -> instance_on_points_003.Points
    voxelize.links.new(delete_geometry_002.outputs[0], instance_on_points_003.inputs[0])
    #instance_on_points_003.Instances -> realize_instances_002.Geometry
    voxelize.links.new(instance_on_points_003.outputs[0], realize_instances_002.inputs[0])
    #merge_by_distance_002.Geometry -> group_output_1.Geometry
    voxelize.links.new(merge_by_distance_002.outputs[0], group_output_1.inputs[0])
    #realize_instances_001.Geometry -> capture_attribute.Geometry
    voxelize.links.new(realize_instances_001.outputs[0], capture_attribute.inputs[0])
    #position_001.Position -> capture_attribute.Value
    voxelize.links.new(position_001.outputs[0], capture_attribute.inputs[1])
    #grid.Mesh -> delete_geometry_005.Geometry
    voxelize.links.new(grid.outputs[0], delete_geometry_005.inputs[0])
    #realize_instances_002.Geometry -> merge_by_distance_002.Geometry
    voxelize.links.new(realize_instances_002.outputs[0], merge_by_distance_002.inputs[0])
    #group_input_002.Mesh -> raycast.Target Geometry
    voxelize.links.new(group_input_002.outputs[0], raycast.inputs[0])
    #vector_math_015.Vector -> vector_math_019.Vector
    voxelize.links.new(vector_math_015.outputs[0], vector_math_019.inputs[0])
    #boolean_math_001.Boolean -> boolean_math.Boolean
    voxelize.links.new(boolean_math_001.outputs[0], boolean_math.inputs[0])
    #raycast.Hit Normal -> vector_math_020.Vector
    voxelize.links.new(raycast.outputs[2], vector_math_020.inputs[0])
    #reroute_010.Output -> reroute_009.Input
    voxelize.links.new(reroute_010.outputs[0], reroute_009.inputs[0])
    #vector_math_019.Vector -> reroute_010.Input
    voxelize.links.new(vector_math_019.outputs[0], reroute_010.inputs[0])
    #vector_math_020.Value -> compare.A
    voxelize.links.new(vector_math_020.outputs[1], compare.inputs[0])
    #compare.Result -> boolean_math.Boolean
    voxelize.links.new(compare.outputs[0], boolean_math.inputs[1])
    #capture_attribute.Attribute -> vector_math_015.Vector
    voxelize.links.new(capture_attribute.outputs[1], vector_math_015.inputs[0])
    #position_002.Position -> vector_math_015.Vector
    voxelize.links.new(position_002.outputs[0], vector_math_015.inputs[1])
    #vector_math_019.Vector -> raycast.Ray Direction
    voxelize.links.new(vector_math_019.outputs[0], raycast.inputs[7])
    #reroute_009.Output -> vector_math_020.Vector
    voxelize.links.new(reroute_009.outputs[0], vector_math_020.inputs[1])
    #vector_math_019.Vector -> vector_math_021.Vector
    voxelize.links.new(vector_math_019.outputs[0], vector_math_021.inputs[0])
    #position_004.Position -> vector_math_022.Vector
    voxelize.links.new(position_004.outputs[0], vector_math_022.inputs[0])
    #vector_math_021.Vector -> vector_math_022.Vector
    voxelize.links.new(vector_math_021.outputs[0], vector_math_022.inputs[1])
    #vector_math_022.Vector -> raycast.Source Position
    voxelize.links.new(vector_math_022.outputs[0], raycast.inputs[6])
    #raycast.Is Hit -> boolean_math_001.Boolean
    voxelize.links.new(raycast.outputs[0], boolean_math_001.inputs[0])
    #raycast.Hit Distance -> compare_002.A
    voxelize.links.new(raycast.outputs[3], compare_002.inputs[0])
    #group_input_005.Voxel Size -> math_003.Value
    voxelize.links.new(group_input_005.outputs[1], math_003.inputs[0])
    #math_003.Value -> compare_002.B
    voxelize.links.new(math_003.outputs[0], compare_002.inputs[1])
    #compare_002.Result -> boolean_math_001.Boolean
    voxelize.links.new(compare_002.outputs[0], boolean_math_001.inputs[1])
    #value.Value -> math_005_1.Value
    voxelize.links.new(value.outputs[0], math_005_1.inputs[0])
    #math_005_1.Value -> vector_math_021.Scale
    voxelize.links.new(math_005_1.outputs[0], vector_math_021.inputs[3])
    #value.Value -> math_006_1.Value
    voxelize.links.new(value.outputs[0], math_006_1.inputs[0])
    #math_006_1.Value -> math_003.Value
    voxelize.links.new(math_006_1.outputs[0], math_003.inputs[2])
    return voxelize





# ========================================================================================================== ### Manual Entry
# Modification 3.1 - 3: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
def voxelizemodifier_node_group_3_1(voxelize, node_group_name, min_value, max_value, default_value): ### Manual Entry
    voxelizemodifier = VoxelUtils.get_voxelity_node_group(node_group_name) ### Manual Entry
    if voxelizemodifier: ### Manual Entry
        return voxelizemodifier ### Manual Entry
    ### Manual Entry
    voxelizemodifier = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
    voxelizemodifier[node_group_name] = 1 # add a custom id with key of the voxelity modifier group name ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3.1 - 3: END ### Manual Entry
# ========================================================================================================== ### Manual Entry






    #initialize voxelizemodifier nodes
    #node Group Input
    group_input_1 = voxelizemodifier.nodes.new("NodeGroupInput")
    group_input_1.name = "Group Input"
    #voxelizemodifier inputs
    #input Geometry
    voxelizemodifier.inputs.new('NodeSocketGeometry', "Geometry")
    voxelizemodifier.inputs[0].attribute_domain = 'POINT'
    
    #input Voxel Size
    voxelizemodifier.inputs.new('NodeSocketFloat', "Voxel Size")





# ========================================================================================================== ### Manual Entry
# Modification 3.1 - 4: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
    voxelizemodifier.inputs[1].default_value = default_value
    voxelizemodifier.inputs[1].min_value = min_value
    voxelizemodifier.inputs[1].max_value = max_value
# ========================================================================================================== ### Manual Entry
# Modification 3.1 - 4: END ### Manual Entry
# ========================================================================================================== ### Manual Entry





    voxelizemodifier.inputs[1].attribute_domain = 'POINT'

    #node Group Output
    group_output_2 = voxelizemodifier.nodes.new("NodeGroupOutput")
    group_output_2.name = "Group Output"
    group_output_2.is_active_output = True
    #voxelizemodifier outputs
    #output Geometry
    voxelizemodifier.outputs.new('NodeSocketGeometry', "Geometry")
    voxelizemodifier.outputs[0].attribute_domain = 'POINT'

    #node Group
    group_1 = voxelizemodifier.nodes.new("GeometryNodeGroup")
    group_1.name = "Group"
    group_1.node_tree = voxelize

    #Set locations
    group_input_1.location = (-249.22732543945312, -30.26141357421875)
    group_output_2.location = (238.68157958984375, 24.64019775390625)
    group_1.location = (-68.0223388671875, 25.491729736328125)
    
    #Set dimensions
    group_input_1.width, group_input_1.height = 140.0, 100.0
    group_output_2.width, group_output_2.height = 140.0, 100.0
    group_1.width, group_1.height = 260.95867919921875, 100.0
    
    #initialize voxelizemodifier links
    #group_1.Geometry -> group_output_2.Geometry
    voxelizemodifier.links.new(group_1.outputs[0], group_output_2.inputs[0])
    #group_input_1.Geometry -> group_1.Mesh
    voxelizemodifier.links.new(group_input_1.outputs[0], group_1.inputs[0])
    #group_input_1.Voxel Size -> group_1.Voxel Size
    voxelizemodifier.links.new(group_input_1.outputs[1], group_1.inputs[1])
    return voxelizemodifier


# ========================================================================================================== ### Manual Entry
# Modification 5: Add initialization code ### Manual Entry
# ========================================================================================================== ### Manual Entry

def get_currently_added_modifier(obj):
    for m in reversed(obj.modifiers):
        if m.type == 'NODES':
            return m
    return None

def get_associated_nodegroup(node_group_name):
    for ng in bpy.data.node_groups:
        if ng.name == node_group_name:
            return ng
    return None

def add_modifier_blender_3_1(obj, voxelizemodifier, mod_node_group_name, default_value):
    if obj is None:
        return
    vox_modifier = obj.modifiers.new(mod_node_group_name, 'NODES')
    vox_modifier.name = mod_node_group_name # NodesModifier.name (same name for different objects but increments if in same object multiple vox modifiers
    vox_modifier_name = vox_modifier.name
    vox_modifier.node_group = voxelizemodifier
    vox_modifier["Input_1"] = default_value
    #vox_modifier["Input_2"] = "UVMap" if not obj.data.uv_layers else obj.data.uv_layers[0].name
    #vox_modifier["Input_3"] = "Col" if not obj.data.color_attributes else obj.data.color_attributes[0].name
    #voxelizemodifier.links.new(voxelizemodifier.nodes["Group Input"].outputs["Voxel Size"], voxelizemodifier.nodes['Group'].inputs["Voxel Size"])

def add_voxelizer_3_1(obj, min_value, max_value, default_value):
    round = round_node_group_3_1()
    voxelize = voxelize_node_group_3_1(NameConstant.VOXILITY_NODE_GROUP_NAME.value, min_value, max_value, default_value)
    voxelizemodifier = voxelizemodifier_node_group_3_1(voxelize, NameConstant.VOXILITY_MODIFIER_NAME.value, min_value, max_value, default_value)
    add_modifier_blender_3_1(obj, voxelizemodifier, NameConstant.VOXILITY_MODIFIER_NAME.value, default_value)

# example usage:
# add_voxelizer_3_1(bpy.context.active_object, 0, 100, 0.4)