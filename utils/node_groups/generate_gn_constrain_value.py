import bpy

def voxilityconstraininput_node_group(node_group_name):

	for node_group in bpy.data.node_groups[:]:
		if node_group.name == node_group_name:
			return node_group

	voxilityconstraininput = bpy.data.node_groups.new(type = 'GeometryNodeTree', name = node_group_name)

	contrainvaluegroupoutput = voxilityconstraininput.nodes.new("NodeGroupOutput")
	contrainvaluegroupoutput.name = "ContrainValueGroupOutput"
	contrainvaluegroupoutput.is_active_output = True

	v = bpy.app.version
	if v >= (4,0,0):
		# Output Socket for the Output value or the constrained value based on input value
		value_socket = voxilityconstraininput.interface.new_socket(name = "Value", in_out='OUTPUT', socket_type = 'NodeSocketFloat')
		value_socket.subtype = 'NONE'
		value_socket.default_value = 0.0
		value_socket.min_value = -3.4e+38
		value_socket.max_value = 3.4e+38
		value_socket.attribute_domain = 'POINT'

		# Input Socket for the Value to check and constrain
		value_socket_1 = voxilityconstraininput.interface.new_socket(name = "Value", in_out='INPUT', socket_type = 'NodeSocketFloat')
		value_socket_1.subtype = 'NONE'
		value_socket_1.default_value = 0.5
		value_socket_1.min_value = -100000.0
		value_socket_1.max_value = 100000.0
		value_socket_1.attribute_domain = 'POINT'

		# Input Socket for the Min allowable value to constrain the input value to
		min_socket = voxilityconstraininput.interface.new_socket(name = "Min", in_out='INPUT', socket_type = 'NodeSocketFloat')
		min_socket.subtype = 'NONE'
		min_socket.default_value = 0.01
		min_socket.min_value = -100000.0
		min_socket.max_value = 100000.0
		min_socket.attribute_domain = 'POINT'

		# Input Socket for the Max allowable value to constrain the input value to
		max_socket = voxilityconstraininput.interface.new_socket(name = "Max", in_out='INPUT', socket_type = 'NodeSocketFloat')
		max_socket.subtype = 'NONE'
		max_socket.default_value = 100.0
		max_socket.min_value = -100000.0
		max_socket.max_value = 100000.0
		max_socket.attribute_domain = 'POINT'

		# Input Socket for the number of decimals or precision for the contrained output of the input value
		decimals_socket = voxilityconstraininput.interface.new_socket(name = "Decimals", in_out='INPUT', socket_type = 'NodeSocketInt')
		decimals_socket.subtype = 'NONE'
		decimals_socket.default_value = 2
		decimals_socket.min_value = 0
		decimals_socket.max_value = 10
		decimals_socket.attribute_domain = 'POINT'
	else:
		# Output Socket for the Output value or the constrained value based on input value
		voxilityconstraininput.outputs.new('NodeSocketFloat', "Value")
		voxilityconstraininput.outputs[0].default_value = 0.0
		voxilityconstraininput.outputs[0].min_value = -3.4028234663852886e+38
		voxilityconstraininput.outputs[0].max_value = 3.4028234663852886e+38
		voxilityconstraininput.outputs[0].attribute_domain = 'POINT'

		# Input Socket for the Value to check and constrain
		voxilityconstraininput.inputs.new('NodeSocketFloat', "Value")
		voxilityconstraininput.inputs[0].default_value = 0.5
		voxilityconstraininput.inputs[0].min_value = -100000.0
		voxilityconstraininput.inputs[0].max_value = 100000.0
		voxilityconstraininput.inputs[0].attribute_domain = 'POINT'

		# Input Socket for the Min allowable value to constrain the input value to
		voxilityconstraininput.inputs.new('NodeSocketFloat', "Min")
		voxilityconstraininput.inputs[1].default_value = 0.009999999776482582
		voxilityconstraininput.inputs[1].min_value = -100000.0
		voxilityconstraininput.inputs[1].max_value = 100000.0
		voxilityconstraininput.inputs[1].attribute_domain = 'POINT'

		# Input Socket for the Max allowable value to constrain the input value to
		voxilityconstraininput.inputs.new('NodeSocketFloat', "Max")
		voxilityconstraininput.inputs[2].default_value = 100.0
		voxilityconstraininput.inputs[2].min_value = -100000.0
		voxilityconstraininput.inputs[2].max_value = 100000.0
		voxilityconstraininput.inputs[2].attribute_domain = 'POINT'

		# Input Socket for the number of decimals or precision for the contrained output of the input value
		voxilityconstraininput.inputs.new('NodeSocketInt', "Decimals")
		voxilityconstraininput.inputs[3].default_value = 2
		voxilityconstraininput.inputs[3].min_value = 0
		voxilityconstraininput.inputs[3].max_value = 10
		voxilityconstraininput.inputs[3].attribute_domain = 'POINT'

	#node ContrainValueDivide
	contrainvaluedivide = voxilityconstraininput.nodes.new("ShaderNodeMath")
	contrainvaluedivide.name = "ContrainValueDivide"
	contrainvaluedivide.operation = 'DIVIDE'
	contrainvaluedivide.use_clamp = False
	contrainvaluedivide.inputs[2].default_value = 0.5

	#node ContrainValueRound
	contrainvalueround = voxilityconstraininput.nodes.new("ShaderNodeMath")
	contrainvalueround.name = "ContrainValueRound"
	contrainvalueround.operation = 'ROUND'
	contrainvalueround.use_clamp = False
	contrainvalueround.inputs[1].default_value = 100.0
	contrainvalueround.inputs[2].default_value = 0.5

	#node ContrainValueMultiply
	contrainvaluemultiply = voxilityconstraininput.nodes.new("ShaderNodeMath")
	contrainvaluemultiply.name = "ContrainValueMultiply"
	contrainvaluemultiply.operation = 'MULTIPLY'
	contrainvaluemultiply.use_clamp = False
	contrainvaluemultiply.inputs[2].default_value = 0.5

	#node ContrainValueMathMin
	contrainvaluemathmin = voxilityconstraininput.nodes.new("ShaderNodeMath")
	contrainvaluemathmin.name = "ContrainValueMathMin"
	contrainvaluemathmin.operation = 'MINIMUM'
	contrainvaluemathmin.use_clamp = False
	contrainvaluemathmin.inputs[2].default_value = 0.5

	#node ContrainValuePow
	contrainvaluepow = voxilityconstraininput.nodes.new("ShaderNodeMath")
	contrainvaluepow.name = "ContrainValuePow"
	contrainvaluepow.operation = 'POWER'
	contrainvaluepow.use_clamp = False
	contrainvaluepow.inputs[0].default_value = 10.0
	contrainvaluepow.inputs[2].default_value = 0.5

	#node ContrainValueMathMax
	contrainvaluemathmax = voxilityconstraininput.nodes.new("ShaderNodeMath")
	contrainvaluemathmax.name = "ContrainValueMathMax"
	contrainvaluemathmax.operation = 'MAXIMUM'
	contrainvaluemathmax.use_clamp = False
	contrainvaluemathmax.inputs[2].default_value = 0.5

	#node ContrainValueGroupInput
	contrainvaluegroupinput = voxilityconstraininput.nodes.new("NodeGroupInput")
	contrainvaluegroupinput.name = "ContrainValueGroupInput"

	#Set locations
	contrainvaluegroupoutput.location = (827.0339965820312, 59.57916259765625)
	contrainvaluedivide.location = (654.565673828125, 45.23163986206055)
	contrainvalueround.location = (485.45068359375, 62.66097640991211)
	contrainvaluemultiply.location = (324.52337646484375, 22.05120277404785)
	contrainvaluemathmin.location = (160.0699005126953, 23.98297119140625)
	contrainvaluepow.location = (160.0699005126953, -145.01702880859375)
	contrainvaluemathmax.location = (-21.669620513916016, 139.99407958984375)
	contrainvaluegroupinput.location = (-249.78366088867188, 25.69511604309082)

	#Set dimensions
	contrainvaluegroupoutput.width, contrainvaluegroupoutput.height = 140.0, 100.0
	contrainvaluedivide.width, contrainvaluedivide.height = 140.0, 100.0
	contrainvalueround.width, contrainvalueround.height = 140.0, 100.0
	contrainvaluemultiply.width, contrainvaluemultiply.height = 140.0, 100.0
	contrainvaluemathmin.width, contrainvaluemathmin.height = 140.0, 100.0
	contrainvaluepow.width, contrainvaluepow.height = 140.0, 100.0
	contrainvaluemathmax.width, contrainvaluemathmax.height = 140.0, 100.0
	contrainvaluegroupinput.width, contrainvaluegroupinput.height = 140.0, 100.0

	voxilityconstraininput.links.new(contrainvaluegroupinput.outputs[0], contrainvaluemathmax.inputs[0])
	voxilityconstraininput.links.new(contrainvaluegroupinput.outputs[1], contrainvaluemathmax.inputs[1])
	voxilityconstraininput.links.new(contrainvaluegroupinput.outputs[2], contrainvaluemathmin.inputs[1])
	voxilityconstraininput.links.new(contrainvaluemathmax.outputs[0], contrainvaluemathmin.inputs[0])
	voxilityconstraininput.links.new(contrainvaluemathmin.outputs[0], contrainvaluemultiply.inputs[0])
	voxilityconstraininput.links.new(contrainvalueround.outputs[0], contrainvaluedivide.inputs[0])
	voxilityconstraininput.links.new(contrainvaluemultiply.outputs[0], contrainvalueround.inputs[0])
	voxilityconstraininput.links.new(contrainvaluepow.outputs[0], contrainvaluemultiply.inputs[1])
	voxilityconstraininput.links.new(contrainvaluegroupinput.outputs[3], contrainvaluepow.inputs[1])
	voxilityconstraininput.links.new(contrainvaluepow.outputs[0], contrainvaluedivide.inputs[1])
	voxilityconstraininput.links.new(contrainvaluedivide.outputs[0], contrainvaluegroupoutput.inputs[0])
	return voxilityconstraininput

#voxilityconstraininput = voxilityconstraininput_node_group()
