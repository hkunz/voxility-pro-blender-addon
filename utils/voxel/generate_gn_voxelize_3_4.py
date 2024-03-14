# Generated with https://github.com/BrendanParmer/NodeToPython/releases

# ========================================================================================================== ### Manual Entry
# Modification 1: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
import bpy ### Manual Entry
from voxility_pro.enums.name_constant import NameConstant ### Manual Entry
 ### Manual Entry
def voxelize_node_group_3_4(node_group_name, min_value, max_value, default_value): ### Manual Entry
    if node_group_name in bpy.data.node_groups: ### Manual Entry
        return bpy.data.node_groups[node_group_name] ### Manual Entry
    ### Manual Entry
    voxelize = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 1: END ### Manual Entry
# ========================================================================================================== ### Manual Entry

    #initialize voxelize nodes
    #node Separate XYZ
    separate_xyz = voxelize.nodes.new("ShaderNodeSeparateXYZ")
    separate_xyz.name = "Separate XYZ"
    
    #node Group Input
    group_input = voxelize.nodes.new("NodeGroupInput")
    group_input.name = "Group Input"
    #voxelize inputs
    #input Mesh
    voxelize.inputs.new('NodeSocketGeometry', "Mesh")
    voxelize.inputs[0].attribute_domain = 'POINT'
    
    #input Voxel Size
    voxelize.inputs.new('NodeSocketFloat', "Voxel Size")





# ========================================================================================================== ### Manual Entry
# Modification 2: Assign default_value, min_value, max_value within voxelize_node_group ### Manual Entry
# ========================================================================================================== ### Manual Entry
    voxelize.inputs[1].default_value = default_value ### Manual Entry
    voxelize.inputs[1].min_value = min_value ### Manual Entry
    voxelize.inputs[1].max_value = max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 2: END ### Manual Entry
# ========================================================================================================== ### Manual Entry
    




    voxelize.inputs[1].attribute_domain = 'POINT'
    
    #input UV Map
    voxelize.inputs.new('NodeSocketString', "UV Map")
    voxelize.inputs[2].attribute_domain = 'POINT'
    
    #input Vertex Colors
    voxelize.inputs.new('NodeSocketString', "Vertex Colors")
    voxelize.inputs[3].attribute_domain = 'POINT'
    
    
    group_input.outputs[2].hide = True
    group_input.outputs[3].hide = True
    group_input.outputs[4].hide = True
    
    #node Vector Math
    vector_math = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math.name = "Vector Math"
    vector_math.operation = 'DIVIDE'
    #Vector_002
    vector_math.inputs[2].default_value = (0.0, 0.0, 0.0)
    #Scale
    vector_math.inputs[3].default_value = 1.0
    
    #node Math.003
    math_003 = voxelize.nodes.new("ShaderNodeMath")
    math_003.name = "Math.003"
    math_003.operation = 'DIVIDE'
    math_003.use_clamp = False
    #Value_001
    math_003.inputs[1].default_value = 2.0
    #Value_002
    math_003.inputs[2].default_value = 0.5
    
    #node Position
    position = voxelize.nodes.new("GeometryNodeInputPosition")
    position.name = "Position"
    
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
    
    #node Vector Math.001
    vector_math_001 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_001.name = "Vector Math.001"
    vector_math_001.operation = 'SCALE'
    #Vector_001
    vector_math_001.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Vector_002
    vector_math_001.inputs[2].default_value = (0.0, 0.0, 0.0)
    
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
    group_input_002.outputs[1].hide = True
    group_input_002.outputs[2].hide = True
    group_input_002.outputs[3].hide = True
    group_input_002.outputs[4].hide = True
    
    #node Sample Nearest Surface.002
    sample_nearest_surface_002 = voxelize.nodes.new("GeometryNodeSampleNearestSurface")
    sample_nearest_surface_002.name = "Sample Nearest Surface.002"
    sample_nearest_surface_002.data_type = 'FLOAT_COLOR'
    #Value_Float
    sample_nearest_surface_002.inputs[1].default_value = 0.0
    #Value_Int
    sample_nearest_surface_002.inputs[2].default_value = 0
    #Value_Bool
    sample_nearest_surface_002.inputs[5].default_value = False
    
    #node Evaluate on Domain.001
    evaluate_on_domain_001 = voxelize.nodes.new("GeometryNodeFieldOnDomain")
    evaluate_on_domain_001.name = "Evaluate on Domain.001"
    evaluate_on_domain_001.data_type = 'FLOAT_COLOR'
    evaluate_on_domain_001.domain = 'FACE'
    #Value_Float
    evaluate_on_domain_001.inputs[0].default_value = 0.0
    #Value_Int
    evaluate_on_domain_001.inputs[1].default_value = 0
    #Value_Bool
    evaluate_on_domain_001.inputs[4].default_value = False
    
    #node Set Position
    set_position = voxelize.nodes.new("GeometryNodeSetPosition")
    set_position.name = "Set Position"
    #Selection
    set_position.inputs[1].default_value = True
    #Offset
    set_position.inputs[3].default_value = (0.0, 0.0, 0.0)
    
    #node Store Named Attribute
    store_named_attribute = voxelize.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute.name = "Store Named Attribute"





# ========================================================================================================== ### Manual Entry
# Modification 3: Use FLOAT2 if 3.5+ else FLOAT_VECTOR ### Manual Entry
# ========================================================================================================== ### Manual Entry
    v = bpy.app.version ### Manual Entry
    store_named_attribute.domain = 'CORNER' ### Manual Entry
    store_named_attribute_inputs = store_named_attribute.inputs ### Manual Entry
    ### Manual Entry
    if v >= (3,5,0): ### Manual Entry
        store_named_attribute.data_type = 'FLOAT2' ### Manual Entry
        store_named_attribute_inputs[1].default_value = True #Selection ### Manual Entry
        store_named_attribute_inputs[2].default_value = "UVMap" #Name ### Manual Entry
        store_named_attribute_inputs[4].default_value = 0.0 #Value_Float ### Manual Entry
        store_named_attribute_inputs[5].default_value = (0.0, 0.0, 0.0, 0.0) #Value_Color ### Manual Entry
        store_named_attribute_inputs[6].default_value = False #Value_Bool ### Manual Entry
        store_named_attribute_inputs[7].default_value = 0 #Value_Int ### Manual Entry
    else: ### Manual Entry
        store_named_attribute.data_type = 'FLOAT_VECTOR' ### Manual Entry
        store_named_attribute_inputs[1].default_value = "UVMap" #Name ### Manual Entry
        store_named_attribute_inputs[3].default_value = 0.0 #Value_Float ### Manual Entry
        store_named_attribute_inputs[4].default_value = (0.0, 0.0, 0.0, 0.0) #Value_Color ### Manual Entry
        store_named_attribute_inputs[5].default_value = False #Value_Bool ### Manual Entry
        store_named_attribute_inputs[6].default_value = 0 #Value_Int ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 3: END ### Manual Entry
# ========================================================================================================== ### Manual Entry





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
    
    #node Material Index
    material_index = voxelize.nodes.new("GeometryNodeInputMaterialIndex")
    material_index.name = "Material Index"
    
    #node Group Input.005
    group_input_005 = voxelize.nodes.new("NodeGroupInput")
    group_input_005.name = "Group Input.005"
    group_input_005.outputs[0].hide = True
    group_input_005.outputs[1].hide = True
    group_input_005.outputs[2].hide = True
    group_input_005.outputs[4].hide = True
    
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
    
    #node Store Named Attribute.001
    store_named_attribute_001 = voxelize.nodes.new("GeometryNodeStoreNamedAttribute")
    store_named_attribute_001.name = "Store Named Attribute.001"
    store_named_attribute_001.data_type = 'FLOAT_COLOR'
    store_named_attribute_001.domain = 'CORNER'






# ========================================================================================================== ### Manual Entry
# Modification 4: StoreNamedAttributeNode has changed in 3.5 ### Manual Entry
# ========================================================================================================== ### Manual Entry
    if v >= (3,5,0): ### Manual Entry
        store_named_attribute_001.inputs[1].default_value = True #Selection ### Manual Entry
        store_named_attribute_001.inputs[3].default_value = (0.0, 0.0, 0.0) #Value_Vector ### Manual Entry
        store_named_attribute_001.inputs[6].default_value = False #Value Bool ### Manual Entry
        store_named_attribute_001.inputs[7].default_value = 0 #Value Int ### Manual Entry
    else: ### Manual Entry
        store_named_attribute_001.inputs[3].default_value = 0.0 #Value_Float ### Manual Entry
        store_named_attribute_001.inputs[5].default_value = False #Value_Bool ### Manual Entry
        store_named_attribute_001.inputs[6].default_value = 0 #Value_Int ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 4: StoreNamedAttributeNode has changed in 3.5 ### Manual Entry
# ========================================================================================================== ### Manual Entry






    #node Join Geometry.001
    join_geometry_001 = voxelize.nodes.new("GeometryNodeJoinGeometry")
    join_geometry_001.name = "Join Geometry.001"
    
    #node Set Material Index
    set_material_index = voxelize.nodes.new("GeometryNodeSetMaterialIndex")
    set_material_index.name = "Set Material Index"
    #Selection
    set_material_index.inputs[1].default_value = True
    
    #node Reroute.004
    reroute_004 = voxelize.nodes.new("NodeReroute")
    reroute_004.name = "Reroute.004"
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
    
    
    
    #node Group Input.006
    group_input_006 = voxelize.nodes.new("NodeGroupInput")
    group_input_006.name = "Group Input.006"
    group_input_006.outputs[1].hide = True
    group_input_006.outputs[2].hide = True
    group_input_006.outputs[3].hide = True
    group_input_006.outputs[4].hide = True
    
    #node Group Input.004
    group_input_004 = voxelize.nodes.new("NodeGroupInput")
    group_input_004.name = "Group Input.004"
    group_input_004.outputs[0].hide = True
    group_input_004.outputs[1].hide = True
    group_input_004.outputs[3].hide = True
    group_input_004.outputs[4].hide = True

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
    
    #node Group Input.007
    group_input_007 = voxelize.nodes.new("NodeGroupInput")
    group_input_007.name = "Group Input.007"
    group_input_007.outputs[0].hide = True
    group_input_007.outputs[2].hide = True
    group_input_007.outputs[3].hide = True
    group_input_007.outputs[4].hide = True
    
    #node Combine XYZ
    combine_xyz = voxelize.nodes.new("ShaderNodeCombineXYZ")
    combine_xyz.name = "Combine XYZ"
    
    #node Group Input.003
    group_input_003 = voxelize.nodes.new("NodeGroupInput")
    group_input_003.name = "Group Input.003"
    group_input_003.outputs[0].hide = True
    group_input_003.outputs[1].hide = True
    group_input_003.outputs[3].hide = True
    group_input_003.outputs[4].hide = True
    
    #node Position.001
    position_001 = voxelize.nodes.new("GeometryNodeInputPosition")
    position_001.name = "Position.001"
    
    #node Vector Math.002
    vector_math_002 = voxelize.nodes.new("ShaderNodeVectorMath")
    vector_math_002.name = "Vector Math.002"
    vector_math_002.operation = 'SCALE'
    #Vector_001
    vector_math_002.inputs[1].default_value = (0.0, 0.0, 0.0)
    #Vector_002
    vector_math_002.inputs[2].default_value = (0.0, 0.0, 0.0)
    
    #node Math
    math = voxelize.nodes.new("ShaderNodeMath")
    math.name = "Math"
    math.operation = 'ROUND'
    math.use_clamp = False
    #Value_001
    math.inputs[1].default_value = 0.5
    #Value_002
    math.inputs[2].default_value = 0.5
    
    #node Math.002
    math_002 = voxelize.nodes.new("ShaderNodeMath")
    math_002.name = "Math.002"
    math_002.operation = 'ROUND'
    math_002.use_clamp = False
    #Value_001
    math_002.inputs[1].default_value = 0.5
    #Value_002
    math_002.inputs[2].default_value = 0.5
    
    #node Reroute.006
    reroute_006 = voxelize.nodes.new("NodeReroute")
    reroute_006.name = "Reroute.006"
    #node Reroute
    reroute = voxelize.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    #node Normal
    normal = voxelize.nodes.new("GeometryNodeInputNormal")
    normal.name = "Normal"
    
    #node Group Input.001
    group_input_001 = voxelize.nodes.new("NodeGroupInput")
    group_input_001.name = "Group Input.001"
    group_input_001.outputs[0].hide = True
    group_input_001.outputs[1].hide = True
    group_input_001.outputs[2].hide = True
    group_input_001.outputs[4].hide = True
    
    #node Named Attribute.001
    named_attribute_001 = voxelize.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute_001.name = "Named Attribute.001"
    named_attribute_001.data_type = 'FLOAT_COLOR'
    
    #node Named Attribute
    named_attribute = voxelize.nodes.new("GeometryNodeInputNamedAttribute")
    named_attribute.name = "Named Attribute"
    named_attribute.data_type = 'FLOAT_VECTOR'
    
    #node Math.001
    math_001 = voxelize.nodes.new("ShaderNodeMath")
    math_001.name = "Math.001"
    math_001.operation = 'ROUND'
    math_001.use_clamp = False
    #Value_001
    math_001.inputs[1].default_value = 0.5
    #Value_002
    math_001.inputs[2].default_value = 0.5
    
    
    #Set locations
    separate_xyz.location = (-942.9451904296875, -75.49308013916016)
    group_input.location = (-1199.1243896484375, 0.4726755917072296)
    vector_math.location = (-1064.2021484375, -99.32075500488281)
    math_003.location = (-1064.2021484375, -234.3207550048828)
    position.location = (-1198.924072265625, -151.33131408691406)
    volume_to_mesh.location = (-546.863525390625, 209.96153259277344)
    vector_math_001.location = (-550.3804321289062, 51.234981536865234)
    vector_math_003.location = (-550.2739868164062, -221.54676818847656)
    group_input_002.location = (-548.801025390625, -361.6170959472656)
    sample_nearest_surface_002.location = (-365.6252746582031, -395.0259704589844)
    evaluate_on_domain_001.location = (-190.3221893310547, -396.1815185546875)
    set_position.location = (-381.73687744140625, 178.91636657714844)
    store_named_attribute.location = (-63.93571853637695, 177.4740447998047)
    capture_attribute.location = (-56.58012008666992, -36.664119720458984)
    sample_nearest_surface.location = (-391.6164855957031, -58.722633361816406)
    material_index.location = (-68.06128692626953, -290.96160888671875)
    group_input_005.location = (-30.275577545166016, -354.1745300292969)
    sample_nearest_surface_001.location = (116.29338073730469, -130.26129150390625)
    store_named_attribute_001.location = (113.43736267089844, -300.1981506347656)
    join_geometry_001.location = (286.4576721191406, -50.69439697265625)
    set_material_index.location = (411.99151611328125, -62.28020477294922)
    reroute_004.location = (171.43771362304688, -34.686737060546875)
    delete_geometry.location = (558.0912475585938, 94.8803939819336)
    merge_by_distance.location = (558.4078369140625, -59.447059631347656)
    group_output.location = (559.9868774414062, -212.2124481201172)
    group_input_006.location = (-203.52774047851562, -7.253007888793945)
    group_input_004.location = (-194.91915893554688, 57.143165588378906)
    evaluate_on_domain.location = (-216.94618225097656, -76.75315856933594)
    mesh_to_volume.location = (-745.2174072265625, 211.2906951904297)
    group_input_007.location = (-693.215576171875, -18.198217391967773)
    combine_xyz.location = (-699.3746337890625, -83.56336212158203)
    group_input_003.location = (-693.215576171875, -212.79969787597656)
    position_001.location = (-693.0152587890625, -276.32415771484375)
    vector_math_002.location = (-693.0152587890625, -342.7977600097656)
    math.location = (-820.8148803710938, -13.157085418701172)
    math_002.location = (-820.8148803710938, -286.232421875)
    reroute_006.location = (-742.1619262695312, -428.2528076171875)
    reroute.location = (-858.4794921875, -428.2528076171875)
    normal.location = (-820.8148803710938, -454.6971130371094)
    group_input_001.location = (-821.01513671875, -518.1253662109375)
    named_attribute_001.location = (-572.817138671875, -453.9988098144531)
    named_attribute.location = (-549.94287109375, -104.93040466308594)
    math_001.location = (-820.8148803710938, -148.58486938476562)
    
    #Set dimensions
    separate_xyz.width, separate_xyz.height = 100.0, 100.0
    group_input.width, group_input.height = 100.3353271484375, 100.0
    vector_math.width, vector_math.height = 100.0, 100.0
    math_003.width, math_003.height = 100.0, 100.0
    position.width, position.height = 100.0, 100.0
    volume_to_mesh.width, volume_to_mesh.height = 138.1574249267578, 100.0
    vector_math_001.width, vector_math_001.height = 140.0, 100.0
    vector_math_003.width, vector_math_003.height = 117.21609497070312, 100.0
    group_input_002.width, group_input_002.height = 114.74972534179688, 100.0
    sample_nearest_surface_002.width, sample_nearest_surface_002.height = 156.54263305664062, 100.0
    evaluate_on_domain_001.width, evaluate_on_domain_001.height = 137.21780395507812, 100.0
    set_position.width, set_position.height = 140.0, 100.0
    store_named_attribute.width, store_named_attribute.height = 152.31634521484375, 100.0
    capture_attribute.width, capture_attribute.height = 140.0, 100.0
    sample_nearest_surface.width, sample_nearest_surface.height = 156.54263305664062, 100.0
    material_index.width, material_index.height = 140.0, 100.0
    group_input_005.width, group_input_005.height = 100.3353271484375, 100.0
    sample_nearest_surface_001.width, sample_nearest_surface_001.height = 150.0, 100.0
    store_named_attribute_001.width, store_named_attribute_001.height = 152.31634521484375, 100.0
    join_geometry_001.width, join_geometry_001.height = 109.61866760253906, 100.0
    set_material_index.width, set_material_index.height = 129.5236358642578, 100.0
    reroute_004.width, reroute_004.height = 16.0, 100.0
    delete_geometry.width, delete_geometry.height = 140.0, 100.0
    merge_by_distance.width, merge_by_distance.height = 139.46994018554688, 100.0
    group_output.width, group_output.height = 140.0, 100.0
    group_input_006.width, group_input_006.height = 114.74972534179688, 100.0
    group_input_004.width, group_input_004.height = 100.3353271484375, 100.0
    evaluate_on_domain.width, evaluate_on_domain.height = 137.21780395507812, 100.0
    mesh_to_volume.width, mesh_to_volume.height = 182.27731323242188, 100.0
    group_input_007.width, group_input_007.height = 100.3353271484375, 100.0
    combine_xyz.width, combine_xyz.height = 110.64816284179688, 100.0
    group_input_003.width, group_input_003.height = 100.3353271484375, 100.0
    position_001.width, position_001.height = 100.0, 100.0
    vector_math_002.width, vector_math_002.height = 100.0, 100.0
    math.width, math.height = 100.0, 100.0
    math_002.width, math_002.height = 100.0, 100.0
    reroute_006.width, reroute_006.height = 16.0, 100.0
    reroute.width, reroute.height = 16.0, 100.0
    normal.width, normal.height = 100.0, 100.0
    group_input_001.width, group_input_001.height = 100.3353271484375, 100.0
    named_attribute_001.width, named_attribute_001.height = 159.23309326171875, 100.0
    named_attribute.width, named_attribute.height = 116.661865234375, 100.0
    math_001.width, math_001.height = 100.0, 100.0
    
    #initialize voxelize links
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





# ========================================================================================================== ### Manual Entry
# Modification 5: Index is shifted from 2 to 3 in the creating noodle link process (search voxelize.links.new)
# ========================================================================================================== ### Manual Entry
    iiiii = 3 if v >= (3,5,0) else 2 ### Manual Entry
    voxelize.links.new(evaluate_on_domain.outputs[2], store_named_attribute.inputs[iiiii]) ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 5: END ### Manual Entry
# ========================================================================================================== ### Manual Entry






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
    #join_geometry_001.Geometry -> set_material_index.Geometry
    voxelize.links.new(join_geometry_001.outputs[0], set_material_index.inputs[0])
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
    #combine_xyz.Vector -> vector_math_001.Vector
    voxelize.links.new(combine_xyz.outputs[0], vector_math_001.inputs[0])
    #named_attribute.Attribute -> sample_nearest_surface.Value
    voxelize.links.new(named_attribute.outputs[0], sample_nearest_surface.inputs[3])
    #position_001.Position -> vector_math_003.Vector
    voxelize.links.new(position_001.outputs[0], vector_math_003.inputs[0])
    #math_001.Value -> combine_xyz.Y
    voxelize.links.new(math_001.outputs[0], combine_xyz.inputs[1])
    #group_input.Mesh -> mesh_to_volume.Mesh
    voxelize.links.new(group_input.outputs[0], mesh_to_volume.inputs[0])
    #merge_by_distance.Geometry -> group_output.Geometry
    voxelize.links.new(merge_by_distance.outputs[0], group_output.inputs[0])
    #group_input.Voxel Size -> mesh_to_volume.Voxel Size
    voxelize.links.new(group_input.outputs[1], mesh_to_volume.inputs[2])
    #group_input.Voxel Size -> vector_math.Vector
    voxelize.links.new(group_input.outputs[1], vector_math.inputs[1])
    #group_input_002.Mesh -> sample_nearest_surface.Mesh
    voxelize.links.new(group_input_002.outputs[0], sample_nearest_surface.inputs[0])
    #math_003.Value -> reroute.Input
    voxelize.links.new(math_003.outputs[0], reroute.inputs[0])
    #named_attribute_001.Attribute -> sample_nearest_surface_002.Value
    voxelize.links.new(named_attribute_001.outputs[2], sample_nearest_surface_002.inputs[3])
    #named_attribute_001.Attribute -> sample_nearest_surface_002.Value
    voxelize.links.new(named_attribute_001.outputs[2], sample_nearest_surface_002.inputs[4])
    #vector_math_003.Vector -> sample_nearest_surface_002.Sample Position
    voxelize.links.new(vector_math_003.outputs[0], sample_nearest_surface_002.inputs[6])
    #group_input_002.Mesh -> sample_nearest_surface_002.Mesh
    voxelize.links.new(group_input_002.outputs[0], sample_nearest_surface_002.inputs[0])
    #sample_nearest_surface_002.Value -> evaluate_on_domain_001.Value
    voxelize.links.new(sample_nearest_surface_002.outputs[3], evaluate_on_domain_001.inputs[2])
    #evaluate_on_domain_001.Value -> store_named_attribute_001.Value
    #voxelize.links.new(evaluate_on_domain_001.outputs[3], store_named_attribute_001.inputs[2]) #manually deleted its in the below Modification 6
    #evaluate_on_domain_001.Value -> store_named_attribute_001.Value
    voxelize.links.new(evaluate_on_domain_001.outputs[3], store_named_attribute_001.inputs[4])
    #sample_nearest_surface_002.Value -> evaluate_on_domain_001.Value
    voxelize.links.new(sample_nearest_surface_002.outputs[3], evaluate_on_domain_001.inputs[3])
    #store_named_attribute_001.Geometry -> join_geometry_001.Geometry
    voxelize.links.new(store_named_attribute_001.outputs[0], join_geometry_001.inputs[0])
    #capture_attribute.Geometry -> join_geometry_001.Geometry
    voxelize.links.new(capture_attribute.outputs[0], join_geometry_001.inputs[0])
    #store_named_attribute.Geometry -> store_named_attribute_001.Geometry
    voxelize.links.new(store_named_attribute.outputs[0], store_named_attribute_001.inputs[0])
    #group_input_001.Vertex Colors -> named_attribute_001.Name
    voxelize.links.new(group_input_001.outputs[3], named_attribute_001.inputs[0])
    #group_input_003.UV Map -> named_attribute.Name
    voxelize.links.new(group_input_003.outputs[2], named_attribute.inputs[0])





# ========================================================================================================== ### Manual Entry
# Modification 6: Index is shifted in the creating noodle link process ### Manual Entry
# ========================================================================================================== ### Manual Entry
    if v >= (3,5,0): ### Manual Entry
        voxelize.links.new(group_input_004.outputs[2], store_named_attribute.inputs[2]) ### Manual Entry
        voxelize.links.new(evaluate_on_domain_001.outputs[3], store_named_attribute_001.inputs[5]) ### Manual Entry
        voxelize.links.new(group_input_005.outputs[3], store_named_attribute_001.inputs[2]) ### Manual Entry
    else: ### Manual Entry
        voxelize.links.new(evaluate_on_domain_001.outputs[3], store_named_attribute_001.inputs[2]) ### Manual Entry
        voxelize.links.new(group_input_004.outputs[2], store_named_attribute.inputs[1]) ### Manual Entry
        voxelize.links.new(group_input_005.outputs[3], store_named_attribute_001.inputs[1]) ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 6: Index is shifted in the creating noodle link process ### Manual Entry
# ========================================================================================================== ### Manual Entry




    #group_input.Voxel Size -> math_003.Value
    voxelize.links.new(group_input.outputs[1], math_003.inputs[0])
    #capture_attribute.Attribute -> reroute_004.Input
    voxelize.links.new(capture_attribute.outputs[4], reroute_004.inputs[0])
    #reroute_004.Output -> delete_geometry.Selection
    voxelize.links.new(reroute_004.outputs[0], delete_geometry.inputs[1])
    #group_input_006.Mesh -> capture_attribute.Geometry
    voxelize.links.new(group_input_006.outputs[0], capture_attribute.inputs[0])
    #reroute.Output -> reroute_006.Input
    voxelize.links.new(reroute.outputs[0], reroute_006.inputs[0])
    #reroute_006.Output -> vector_math_002.Scale
    voxelize.links.new(reroute_006.outputs[0], vector_math_002.inputs[3])
    #group_input_007.Voxel Size -> vector_math_001.Scale
    voxelize.links.new(group_input_007.outputs[1], vector_math_001.inputs[3])

    return voxelize





# ========================================================================================================== ### Manual Entry
# Modification 7: Function name change and parameters modification ### Manual Entry
# ========================================================================================================== ### Manual Entry
def voxelizemodifier_node_group_3_4(voxelize, node_group_name, min_value, max_value, default_value): ### Manual Entry
    if node_group_name in bpy.data.node_groups: ### Manual Entry
        return bpy.data.node_groups[node_group_name] ### Manual Entry
    ### Manual Entry
    voxelizemodifier = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name) ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 7: END ### Manual Entry
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
# Modification 8: Assign default_value, min_value, max_value within voxelizemodifier_node_group ### Manual Entry
# ========================================================================================================== ### Manual Entry
    voxelizemodifier.inputs[1].default_value = default_value ### Manual Entry
    voxelizemodifier.inputs[1].min_value = min_value ### Manual Entry
    voxelizemodifier.inputs[1].max_value = max_value ### Manual Entry
# ========================================================================================================== ### Manual Entry
# Modification 8: END ### Manual Entry
# ========================================================================================================== ### Manual Entry





    voxelizemodifier.inputs[1].attribute_domain = 'POINT'
    
    #input UV Map
    voxelizemodifier.inputs.new('NodeSocketString', "UV Map")
    voxelizemodifier.inputs[2].attribute_domain = 'POINT'
    
    #input Vertex Colors
    voxelizemodifier.inputs.new('NodeSocketString', "Vertex Colors")
    voxelizemodifier.inputs[3].attribute_domain = 'POINT'
    
    #node Group Output
    group_output_1 = voxelizemodifier.nodes.new("NodeGroupOutput")
    group_output_1.name = "Group Output"
    group_output_1.is_active_output = True
    #voxelizemodifier outputs
    #output Geometry
    voxelizemodifier.outputs.new('NodeSocketGeometry', "Geometry")
    voxelizemodifier.outputs[0].attribute_domain = 'POINT'

    #node Group.001
    group_001 = voxelizemodifier.nodes.new("GeometryNodeGroup")
    group_001.name = "Group.001"
    group_001.node_tree = voxelize

    #Set locations
    group_input_1.location = (561.7833862304688, -199.3120880126953)
    group_output_1.location = (1135.4541015625, -143.74620056152344)
    group_001.location = (776.3731079101562, -143.63876342773438)
    
    #Set dimensions
    group_input_1.width, group_input_1.height = 140.0, 100.0
    group_output_1.width, group_output_1.height = 140.0, 100.0
    group_001.width, group_001.height = 296.51495361328125, 100.0
    
    #initialize voxelizemodifier links
    #group_001.Geometry -> group_output_1.Geometry
    voxelizemodifier.links.new(group_001.outputs[0], group_output_1.inputs[0])
    #group_input_1.Geometry -> group_001.Mesh
    voxelizemodifier.links.new(group_input_1.outputs[0], group_001.inputs[0])
    #group_input_1.Vertex Colors -> group_001.Vertex Colors
    voxelizemodifier.links.new(group_input_1.outputs[3], group_001.inputs[3])
    #group_input_1.UV Map -> group_001.UV Map
    voxelizemodifier.links.new(group_input_1.outputs[2], group_001.inputs[2])
    #group_input_1.Voxel Size -> group_001.Voxel Size
    voxelizemodifier.links.new(group_input_1.outputs[1], group_001.inputs[1])
    return voxelizemodifier





# ========================================================================================================== ### Manual Entry
# Modification 7: Add initialization code ### Manual Entry
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

def add_modifier_blender_3_4(obj, voxelizemodifier, mod_node_group_name, default_value):
    if obj is None:
        return

    v = bpy.app.version
    bpy.ops.object.modifier_add(type='NODES')

    vox_modifier = obj.modifiers[-1]
    vox_modifier.name = mod_node_group_name # NodesModifier.name (same name for different objects but increments if in same object multiple vox modifiers
    vox_modifier_name = vox_modifier.name
    vox_modifier.node_group = voxelizemodifier
    vox_modifier["Input_1"] = default_value
    vox_modifier["Input_2"] = "UVMap" if not obj.data.uv_layers else obj.data.uv_layers[0].name
    vox_modifier["Input_3"] = ("Col" if v <= (3,4,0) else "Attribute") if not obj.data.color_attributes else obj.data.color_attributes[0].name
    #voxelizemodifier.links.new(voxelizemodifier.nodes["Group Input"].outputs["Voxel Size"], voxelizemodifier.nodes['Group'].inputs["Voxel Size"])

def add_voxelizer_3_4(obj, min_value, max_value, default_value):
    voxelize = voxelize_node_group_3_4(NameConstant.VOXILITY_NODE_GROUP_NAME.value, min_value, max_value, default_value)
    voxelizemodifier = voxelizemodifier_node_group_3_4(voxelize, NameConstant.VOXILITY_MODIFIER_NAME.value, min_value, max_value, default_value)
    add_modifier_blender_3_4(obj, voxelizemodifier, NameConstant.VOXILITY_MODIFIER_NAME.value, default_value)

# example usage:
# add_voxelizer_3_4(bpy.context.active_object, 0, 100, 0.4)