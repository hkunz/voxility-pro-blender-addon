# Generated with https://github.com/BrendanParmer/NodeToPython/releases

import bpy

from voxility_pro.enums.name_constant import NameConstant

def voxelize_node_group_3_5(node_group_name, min_value, max_value, default_value):
    if node_group_name in bpy.data.node_groups:
        return bpy.data.node_groups[node_group_name]

    voxelize = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name)

    #initialize voxelize nodes
    #node Reroute.002
    reroute_002 = voxelize.nodes.new("NodeReroute")
    reroute_002.name = "Reroute.002"
    #node Mesh to Volume
    mesh_to_volume = voxelize.nodes.new("GeometryNodeMeshToVolume")
    mesh_to_volume.name = "Mesh to Volume"
    mesh_to_volume.resolution_mode = 'VOXEL_SIZE'
    #Density
    mesh_to_volume.inputs[1].default_value = 1.0
    #Voxel Amount
    mesh_to_volume.inputs[3].default_value = 64.0
    #Exterior Band Width
    mesh_to_volume.inputs[4].default_value = 0.10000000149011612
    #Interior Band Width
    mesh_to_volume.inputs[5].default_value = 0.0
    #Fill Volume
    mesh_to_volume.inputs[6].default_value = True

    #node Reroute.001
    reroute_001 = voxelize.nodes.new("NodeReroute")
    reroute_001.name = "Reroute.001"
    #node Combine XYZ
    combine_xyz = voxelize.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"

    #node Math
    math = voxelize.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'ROUND'
    math.use_clamp = False
    #Value_001
    math.inputs[1].default_value = 0.5
    #Value_002
    math.inputs[2].default_value = 0.5

    #node Math.001
    math_001 = voxelize.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'ROUND'
    math_001.use_clamp = False
    #Value_001
    math_001.inputs[1].default_value = 0.5
    #Value_002
    math_001.inputs[2].default_value = 0.5

    #node Math.002
    math_002 = voxelize.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'ROUND'
    math_002.use_clamp = False
    #Value_001
    math_002.inputs[1].default_value = 0.5
    #Value_002
    math_002.inputs[2].default_value = 0.5

    #node Vector Math.002
    vector_math_002 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'SCALE'
    #Vector_001
    vector_math_002.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Vector_002
    vector_math_002.inputs[2].default_value = (0.0, 0.0, 0.0)

    #node Group Input.001
    group_input_001 = voxelize.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    #voxelize inputs
    #input Mesh
    voxelize.inputs.new('NodeSocketGeometry', "Mesh")
    voxelize.inputs[0].attribute_domain = 'POINT'

    #input Voxel Size
    voxelize.inputs.new('NodeSocketFloat', "Voxel Size")
    voxelize.inputs[1].default_value = default_value
    voxelize.inputs[1].min_value = min_value
    voxelize.inputs[1].max_value = max_value
    voxelize.inputs[1].attribute_domain = 'POINT'

    #node Position
    position = voxelize.nodes.new("GeometryNodeInputPosition")
    position.name = "Position"

    #node Math.003
    math_003 = voxelize.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'DIVIDE'
    math_003.use_clamp = False
    #Value_001
    math_003.inputs[1].default_value = 2.0
    #Value_002
    math_003.inputs[2].default_value = 0.5

    #node Vector Math
    vector_math = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'DIVIDE'
    #Vector_002
    vector_math.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math.inputs[3].default_value = 1.0

    #node Reroute
    reroute = voxelize.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    #node Vector Math.001
    vector_math_001 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'SCALE'
    #Vector_001
    vector_math_001.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Vector_002
    vector_math_001.inputs[2].default_value = (0.0, 0.0, 0.0)

    #node Separate XYZ
    separate_xyz = voxelize.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"

    #node Volume to Mesh
    volume_to_mesh = voxelize.nodes.new("GeometryNodeVolumeToMesh")
    volume_to_mesh.name = "Volume to Mesh"
    volume_to_mesh.resolution_mode = 'GRID'
    #Voxel Size
    volume_to_mesh.inputs[1].default_value = 0.30000001192092896
    #Voxel Amount
    volume_to_mesh.inputs[2].default_value = 64.0
    #Threshold
    volume_to_mesh.inputs[3].default_value = 0.10000000149011612
    #Adaptivity
    volume_to_mesh.inputs[4].default_value = 0.0

    #node Position.001
    position_001 = voxelize.nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"

    #node Named Attribute
    named_attribute = voxelize.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.data_type = 'FLOAT_VECTOR'
    #Name
    named_attribute.inputs[0].default_value = "UVMap"

    #node Vector Math.003
    vector_math_003 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_003.name = "Vector Math.003"
    vector_math_003.operation = 'SUBTRACT'
    #Vector_002
    vector_math_003.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math_003.inputs[3].default_value = 1.0

    #node Group Input.002
    group_input_002 = voxelize.nodes.new("NodeGroupInput")
    group_input_002.name = "Group Input.002"

    #node Set Position
    set_position = voxelize.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    #Selection
    set_position.inputs[1].default_value = True
    #Offset
    set_position.inputs[3].default_value = (0.0, 0.0, 0.0)

    #node Sample Nearest Surface
    sample_nearest_surface = voxelize.nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface.name = "Sample Nearest Surface"
    sample_nearest_surface.data_type = 'FLOAT_VECTOR'
    #Value_Float
    sample_nearest_surface.inputs[1].default_value = 0.0
    #Value_Int
    sample_nearest_surface.inputs[2].default_value = 0
    #Value_Color
    sample_nearest_surface.inputs[4].default_value = (0.0, 0.0, 0.0, 0.0)
    #Value_Bool
    sample_nearest_surface.inputs[5].default_value = False

    #node Normal
    normal = voxelize.nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"

    #node Evaluate on Domain
    evaluate_on_domain = voxelize.nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain.name = "Evaluate on Domain"
    evaluate_on_domain.data_type = 'FLOAT_VECTOR'
    evaluate_on_domain.domain = 'FACE'
    #Value_Float
    evaluate_on_domain.inputs[0].default_value = 0.0
    #Value_Int
    evaluate_on_domain.inputs[1].default_value = 0
    #Value_Color
    evaluate_on_domain.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    #Value_Bool
    evaluate_on_domain.inputs[4].default_value = False

    #node Capture Attribute
    capture_attribute = voxelize.nodes.new("GeometryNodeCaptureAttribute")
    capture_attribute.name = "Capture Attribute"
    capture_attribute.data_type = 'BOOLEAN'
    capture_attribute.domain = 'POINT'
    #Value
    capture_attribute.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Value_001
    capture_attribute.inputs[2].default_value = 0.0
    #Value_002
    capture_attribute.inputs[3].default_value = (0.0, 0.0, 0.0, 0.0)
    #Value_003
    capture_attribute.inputs[4].default_value = True
    #Value_004
    capture_attribute.inputs[5].default_value = 0

    #node Set Material Index
    set_material_index = voxelize.nodes.new("GeometryNodeSetMaterialIndex")
    set_material_index.name = "Set Material Index"
    #Selection
    set_material_index.inputs[1].default_value = True

    #node Material Index
    material_index = voxelize.nodes.new("GeometryNodeInputMaterialIndex")
    material_index.name = "Material Index"

    #node Join Geometry
    join_geometry = voxelize.nodes.new("GeometryNodeJoinGeometry")
    join_geometry.name = "Join Geometry"

    #node Store Named Attribute
    store_named_attribute = voxelize.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"

    v = bpy.app.version
    store_named_attribute.data_type = 'FLOAT2' if v >= (3,5,0) else 'FLOAT_VECTOR'
    store_named_attribute.domain = 'CORNER'
    store_named_attribute_inputs = store_named_attribute.inputs

    if v >= (3,5,0):
        store_named_attribute_inputs[1].default_value = True #Selection
        store_named_attribute_inputs[2].default_value = "UVMap" #Name
        store_named_attribute_inputs[4].default_value = 0.0 #Value_Float
        store_named_attribute_inputs[5].default_value = (0.0, 0.0, 0.0, 0.0) #Value_Color
        store_named_attribute_inputs[6].default_value = False #Value_Bool
        store_named_attribute_inputs[7].default_value = 0 #Value_Int
    else:
        store_named_attribute_inputs[1].default_value = "UVMap" #Name
        store_named_attribute_inputs[3].default_value = 0.0 #Value_Float
        store_named_attribute_inputs[4].default_value = (0.0, 0.0, 0.0, 0.0) #Value_Color
        store_named_attribute_inputs[5].default_value = False #Value_Bool
        store_named_attribute_inputs[6].default_value = 0 #Value_Int

    #node Sample Nearest Surface.001
    sample_nearest_surface_001 = voxelize.nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface_001.name = "Sample Nearest Surface.001"
    sample_nearest_surface_001.data_type = 'INT'
    #Value_Float
    sample_nearest_surface_001.inputs[1].default_value = 0.0
    #Value_Vector
    sample_nearest_surface_001.inputs[3].default_value = (0.0, 0.0, 0.0)
    #Value_Color
    sample_nearest_surface_001.inputs[4].default_value = (0.0, 0.0, 0.0, 0.0)
    #Value_Bool
    sample_nearest_surface_001.inputs[5].default_value = False

    #node Delete Geometry
    delete_geometry = voxelize.nodes.new("GeometryNodeDeleteGeometry")
    delete_geometry.name = "Delete Geometry"
    delete_geometry.domain = 'POINT'
    delete_geometry.mode = 'ALL'

    #node Merge by Distance
    merge_by_distance = voxelize.nodes.new("GeometryNodeMergeByDistance")
    merge_by_distance.name = "Merge by Distance"
    merge_by_distance.mode = 'ALL'
    #Selection
    merge_by_distance.inputs[1].default_value = True
    #Distance
    merge_by_distance.inputs[2].default_value = 0.0010000000474974513

    #node Group Output
    group_output = voxelize.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    #voxelize outputs
    #output Geometry
    voxelize.outputs.new('NodeSocketGeometry', "Geometry")
    voxelize.outputs[0].attribute_domain = 'POINT'

    #node Group Input
    group_input = voxelize.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"

    #Set locations
    reroute_002.location = (-976.8480224609375, 125.14899444580078)
    mesh_to_volume.location = (-745.2174072265625, 211.2906951904297)
    reroute_001.location = (-912.9071655273438, 80.40065002441406)
    combine_xyz.location = (-699.3746337890625, -56.6837043762207)
    math.location = (-820.8148803710938, 11.86112117767334)
    math_001.location = (-820.0474243164062, -72.10088348388672)
    math_002.location = (-820.8148803710938, -155.2949981689453)
    vector_math_002.location = (-695.9293212890625, -300.3758850097656)
    group_input_001.location = (-1187.799560546875, -181.96035766601562)
    position.location = (-1187.5992431640625, -106.9603500366211)
    math_003.location = (-1064.2021484375, -200.38575744628906)
    vector_math.location = (-1064.2021484375, -65.38575744628906)
    reroute.location = (-842.562255859375, -409.3598937988281)
    vector_math_001.location = (-525.8925170898438, 51.234981536865234)
    separate_xyz.location = (-942.9451904296875, -75.49308013916016)
    volume_to_mesh.location = (-546.863525390625, 209.96153259277344)
    position_001.location = (-821.751220703125, -247.91221618652344)
    named_attribute.location = (-525.4549560546875, -84.67989349365234)
    vector_math_003.location = (-525.7860107421875, -221.54676818847656)
    group_input_002.location = (-524.3130493164062, -337.01043701171875)
    set_position.location = (-351.12689208984375, 178.91636657714844)
    sample_nearest_surface.location = (-361.0065002441406, -79.08363342285156)
    normal.location = (-821.751220703125, -308.2270202636719)
    evaluate_on_domain.location = (-182.63507080078125, 41.48637008666992)
    capture_attribute.location = (-19.29928207397461, -35.30215072631836)
    set_material_index.location = (328.9070129394531, -56.429786682128906)
    material_index.location = (-20.289609909057617, -224.03274536132812)
    join_geometry.location = (153.83200073242188, 95.92117309570312)
    store_named_attribute.location = (-22.000120162963867, 183.13987731933594)
    sample_nearest_surface_001.location = (148.21217346191406, -176.28890991210938)
    delete_geometry.location = (484.7822265625, 135.68016052246094)
    merge_by_distance.location = (643.374755859375, 145.15731811523438)
    group_output.location = (795.1829833984375, 125.6429443359375)
    group_input.location = (-1187.799560546875, 20.039649963378906)

    #Set dimensions
    reroute_002.width, reroute_002.height = 16.0, 100.0
    mesh_to_volume.width, mesh_to_volume.height = 182.27731323242188, 100.0
    reroute_001.width, reroute_001.height = 16.0, 100.0
    combine_xyz.width, combine_xyz.height = 110.64816284179688, 100.0
    math.width, math.height = 100.0, 100.0
    math_001.width, math_001.height = 100.0, 100.0
    math_002.width, math_002.height = 100.0, 100.0
    vector_math_002.width, vector_math_002.height = 100.0, 100.0
    group_input_001.width, group_input_001.height = 100.3353271484375, 100.0
    position.width, position.height = 100.0, 100.0
    math_003.width, math_003.height = 100.0, 100.0
    vector_math.width, vector_math.height = 100.0, 100.0
    reroute.width, reroute.height = 16.0, 100.0
    vector_math_001.width, vector_math_001.height = 140.0, 100.0
    separate_xyz.width, separate_xyz.height = 100.0, 100.0
    volume_to_mesh.width, volume_to_mesh.height = 172.4405975341797, 100.0
    position_001.width, position_001.height = 100.0, 100.0
    named_attribute.width, named_attribute.height = 116.661865234375, 100.0
    vector_math_003.width, vector_math_003.height = 117.21609497070312, 100.0
    group_input_002.width, group_input_002.height = 114.74972534179688, 100.0
    set_position.width, set_position.height = 140.0, 100.0
    sample_nearest_surface.width, sample_nearest_surface.height = 156.54263305664062, 100.0
    normal.width, normal.height = 100.0, 100.0
    evaluate_on_domain.width, evaluate_on_domain.height = 137.21780395507812, 100.0
    capture_attribute.width, capture_attribute.height = 140.0, 100.0
    set_material_index.width, set_material_index.height = 140.0, 100.0
    material_index.width, material_index.height = 140.0, 100.0
    join_geometry.width, join_geometry.height = 140.0, 100.0
    store_named_attribute.width, store_named_attribute.height = 152.31634521484375, 100.0
    sample_nearest_surface_001.width, sample_nearest_surface_001.height = 150.0, 100.0
    delete_geometry.width, delete_geometry.height = 140.0, 100.0
    merge_by_distance.width, merge_by_distance.height = 131.17848205566406, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    group_input.width, group_input.height = 100.3353271484375, 100.0

    #initialize voxelize links
    #store_named_attribute.Geometry -> join_geometry.Geometry
    voxelize.links.new(store_named_attribute.outputs[0], join_geometry.inputs[0])
    #capture_attribute.Geometry -> join_geometry.Geometry
    voxelize.links.new(capture_attribute.outputs[0], join_geometry.inputs[0])
    #capture_attribute.Geometry -> sample_nearest_surface_001.Mesh
    voxelize.links.new(capture_attribute.outputs[0], sample_nearest_surface_001.inputs[0])
    #separate_xyz.X -> math.Value
    voxelize.links.new(separate_xyz.outputs[0], math.inputs[0])
    #sample_nearest_surface_001.Value -> set_material_index.Material Index
    voxelize.links.new(sample_nearest_surface_001.outputs[1], set_material_index.inputs[2])
    #math.Value -> combine_xyz.X
    voxelize.links.new(math.outputs[0], combine_xyz.inputs[0])
    #vector_math_003.Vector -> sample_nearest_surface_001.Sample Position
    voxelize.links.new(vector_math_003.outputs[0], sample_nearest_surface_001.inputs[6])
    #vector_math.Vector -> separate_xyz.Vector
    voxelize.links.new(vector_math.outputs[0], separate_xyz.inputs[0])
    
    #evaluate_on_domain.Value -> store_named_attribute.Value
    store_named_attribute_inputs_value_vector_index = 3 if v >= (3,5,0) else 2
    voxelize.links.new(evaluate_on_domain.outputs[2], store_named_attribute.inputs[store_named_attribute_inputs_value_vector_index])
    #volume_to_mesh.Mesh -> set_position.Geometry
    voxelize.links.new(volume_to_mesh.outputs[0], set_position.inputs[0])
    #vector_math_003.Vector -> sample_nearest_surface.Sample Position
    voxelize.links.new(vector_math_003.outputs[0], sample_nearest_surface.inputs[6])
    #vector_math_002.Vector -> vector_math_003.Vector
    voxelize.links.new(vector_math_002.outputs[0], vector_math_003.inputs[1])
    #delete_geometry.Geometry -> merge_by_distance.Geometry
    voxelize.links.new(delete_geometry.outputs[0], merge_by_distance.inputs[0])
    #normal.Normal -> vector_math_002.Vector
    voxelize.links.new(normal.outputs[0], vector_math_002.inputs[0])
    #join_geometry.Geometry -> set_material_index.Geometry
    voxelize.links.new(join_geometry.outputs[0], set_material_index.inputs[0])
    #mesh_to_volume.Volume -> volume_to_mesh.Volume
    voxelize.links.new(mesh_to_volume.outputs[0], volume_to_mesh.inputs[0])
    #set_position.Geometry -> store_named_attribute.Geometry
    voxelize.links.new(set_position.outputs[0], store_named_attribute.inputs[0])
    #separate_xyz.Y -> math_001.Value
    voxelize.links.new(separate_xyz.outputs[1], math_001.inputs[0])
    #vector_math_001.Vector -> set_position.Position
    voxelize.links.new(vector_math_001.outputs[0], set_position.inputs[2])
    #position.Position -> vector_math.Vector
    voxelize.links.new(position.outputs[0], vector_math.inputs[0])
    #reroute.Output -> vector_math_002.Scale
    voxelize.links.new(reroute.outputs[0], vector_math_002.inputs[3])
    #math_002.Value -> combine_xyz.Z
    voxelize.links.new(math_002.outputs[0], combine_xyz.inputs[2])
    #material_index.Material Index -> sample_nearest_surface_001.Value
    voxelize.links.new(material_index.outputs[0], sample_nearest_surface_001.inputs[2])
    #separate_xyz.Z -> math_002.Value
    voxelize.links.new(separate_xyz.outputs[2], math_002.inputs[0])
    #set_material_index.Geometry -> delete_geometry.Geometry
    voxelize.links.new(set_material_index.outputs[0], delete_geometry.inputs[0])
    #sample_nearest_surface.Value -> evaluate_on_domain.Value
    voxelize.links.new(sample_nearest_surface.outputs[2], evaluate_on_domain.inputs[2])
    #capture_attribute.Attribute -> delete_geometry.Selection
    voxelize.links.new(capture_attribute.outputs[4], delete_geometry.inputs[1])
    #combine_xyz.Vector -> vector_math_001.Vector
    voxelize.links.new(combine_xyz.outputs[0], vector_math_001.inputs[0])
    #named_attribute.Attribute -> sample_nearest_surface.Value
    voxelize.links.new(named_attribute.outputs[0], sample_nearest_surface.inputs[3])
    #position_001.Position -> vector_math_003.Vector
    voxelize.links.new(position_001.outputs[0], vector_math_003.inputs[0])
    #math_001.Value -> combine_xyz.Y
    voxelize.links.new(math_001.outputs[0], combine_xyz.inputs[1])
    #reroute_002.Output -> mesh_to_volume.Mesh
    voxelize.links.new(reroute_002.outputs[0], mesh_to_volume.inputs[0])
    #merge_by_distance.Geometry -> group_output.Geometry
    voxelize.links.new(merge_by_distance.outputs[0], group_output.inputs[0])
    #reroute_001.Output -> mesh_to_volume.Voxel Size
    voxelize.links.new(reroute_001.outputs[0], mesh_to_volume.inputs[2])
    #group_input.Voxel Size -> vector_math.Vector
    voxelize.links.new(group_input.outputs[1], vector_math.inputs[1])
    #group_input_002.Mesh -> capture_attribute.Geometry
    voxelize.links.new(group_input_002.outputs[0], capture_attribute.inputs[0])
    #group_input_002.Mesh -> sample_nearest_surface.Mesh
    voxelize.links.new(group_input_002.outputs[0], sample_nearest_surface.inputs[0])
    #group_input.Voxel Size -> reroute_001.Input
    voxelize.links.new(group_input.outputs[1], reroute_001.inputs[0])
    #reroute_001.Output -> vector_math_001.Scale
    voxelize.links.new(reroute_001.outputs[0], vector_math_001.inputs[3])
    #group_input.Mesh -> reroute_002.Input
    voxelize.links.new(group_input.outputs[0], reroute_002.inputs[0])
    #group_input_001.Voxel Size -> math_003.Value
    voxelize.links.new(group_input_001.outputs[1], math_003.inputs[0])
    #math_003.Value -> reroute.Input
    voxelize.links.new(math_003.outputs[0], reroute.inputs[0])
    return voxelize

#initialize voxelizemodifier node group
def voxelizemodifier_node_group_3_5(voxelize, node_group_name, min_value, max_value, default_value):
    if node_group_name in bpy.data.node_groups:
        return bpy.data.node_groups[node_group_name]

    voxelizemodifier = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name)

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
    voxelizemodifier.inputs[1].default_value = default_value
    voxelizemodifier.inputs[1].min_value = min_value
    voxelizemodifier.inputs[1].max_value = max_value
    voxelizemodifier.inputs[1].attribute_domain = 'POINT'

    #node Group Output
    group_output_1 = voxelizemodifier.nodes.new("NodeGroupOutput")
    group_output_1.name = "Group Output"
    group_output_1.is_active_output = True
    #voxelizemodifier outputs
    #output Geometry
    voxelizemodifier.outputs.new('NodeSocketGeometry', "Geometry")
    voxelizemodifier.outputs[0].attribute_domain = 'POINT'

    #node Group
    group = voxelizemodifier.nodes.new("GeometryNodeGroup")
    group.name = "Group"
    group.node_tree = voxelize

    #Set locations
    group_input_1.location = (-319.47198486328125, -15.414009094238281)
    group_output_1.location = (200.0, 0.0)
    group.location = (-76.83906555175781, 40.01508331298828)

    #Set dimensions
    group_input_1.width, group_input_1.height = 140.0, 100.0
    group_output_1.width, group_output_1.height = 140.0, 100.0
    group.width, group.height = 197.96212768554688, 100.0

    #initialize voxelizemodifier links
    #group.Geometry -> group_output_1.Geometry
    voxelizemodifier.links.new(group.outputs[0], group_output_1.inputs[0])
    #group_input_1.Geometry -> group.Mesh
    voxelizemodifier.links.new(group_input_1.outputs[0], group.inputs[0])
    #group_input_1.Voxel Size -> group.Voxel Size
    voxelizemodifier.links.new(group_input_1.outputs[1], group.inputs[1])
    return voxelizemodifier


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

def add_modifier_blender_3_5(obj, voxelizemodifier, mod_node_group_name, default_value):
    if obj is None:
        return

    bpy.ops.object.modifier_add(type='NODES')

    vox_modifier = obj.modifiers[-1]
    vox_modifier.name = mod_node_group_name # NodesModifier.name (same name for different objects but increments if in same object multiple vox modifiers
    vox_modifier_name = vox_modifier.name
    vox_modifier.node_group = voxelizemodifier
    vox_modifier["Input_1"] = default_value
    voxelizemodifier.links.new(voxelizemodifier.nodes["Group Input"].outputs["Voxel Size"], voxelizemodifier.nodes['Group'].inputs["Voxel Size"])

def add_voxelizer_3_5(obj, min_value, max_value, default_value):
    voxelize = voxelize_node_group_3_5(NameConstant.VOXILITY_NODE_GROUP_NAME.value, min_value, max_value, default_value)
    voxelizemodifier = voxelizemodifier_node_group_3_5(voxelize, NameConstant.VOXILITY_MODIFIER_NAME.value, min_value, max_value, default_value)
    add_modifier_blender_3_5(obj, voxelizemodifier, NameConstant.VOXILITY_MODIFIER_NAME.value, default_value)
    voxelizemodifier.inputs[1].default_value = default_value
    voxelizemodifier.inputs[1].min_value = min_value
    voxelizemodifier.inputs[1].max_value = max_value

# example usage:
# add_voxelizer_3_5(bpy.context.active_object, 0, 100, 0.4)