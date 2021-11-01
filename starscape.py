import bpy
import sys
import math
import random
import mathutils

def random_spherical_coordinates():
    phi = random.random() * 2 * math.pi
    theta = math.asin(2 * random.random() - 1)
    return phi, theta

def spherical_to_cartesian_coordinates(radius, phi, theta):
    x = radius * math.cos(phi) * math.cos(theta)
    y = radius * math.sin(phi) * math.cos(theta)
    z = radius * math.sin(theta)
    return x, y, z

# Get the scene camera
camera = bpy.context.scene.camera
if not camera or camera.data.type != "PERSP":
    sys.exit(1)

# Create stars positions (mesh data consisting only of vertices, radius = 1)
vertices = []
for i in range(100000):
    # Generate a random location at random across the sky
    phi, theta = random_spherical_coordinates()
    x, y, z = spherical_to_cartesian_coordinates(1, phi, theta)
    vertices.append((x, y, z))

# Create a new mesh
mesh = bpy.data.meshes.new("stars_mesh")
# Add the mesh to a new object
obj = bpy.data.objects.new("stars", mesh)
# Set the mesh to the star data
mesh.from_pydata(vertices, [], [])

# Set vertex normals
for v in mesh.vertices:
    v.normal = v.co

# Add a star template
# Usa a triangle, because it uses the least amount of vertices and faces
vertices = []
s = 0.0002
q = s * math.sqrt(3)
vertices.append((+0, 0, +2 * s))
vertices.append((-q, 0, -1 * s))
vertices.append((+q, 0, -1 * s))
mesh = bpy.data.meshes.new("star_template_mesh")
obj2 = bpy.data.objects.new("star_template", mesh)
mesh.from_pydata(vertices, [(0, 1), (0, 2), (1, 2)], [(0, 1, 2)])

### Material ###############################################################################

def hide_node_outputs(node):
    for socket in node.outputs:
        if not socket.is_linked:
            socket.hide = True

def make_node(nodes, node_type, x, y):
    node = nodes.new(node_type)
    node.location = (x, y)
    return node

def make_group_node(nodes, group, x, y):
    node = nodes.new("ShaderNodeGroup")
    node.node_tree = group
    node.location = (x, y)
    return node

def make_math_node(nodes, function, x, y, default_1 = 0.5, default_2 = 0.5):
    node = nodes.new("ShaderNodeMath")
    node.operation = function
    node.location = (x, y)
    node.inputs[0].default_value = default_1
    node.inputs[1].default_value = default_2
    return node

def connect_nodes(tree, *args):
    if len(args) < 4 or (len(args) - 4) % 3 != 0:
        raise Exception("Invalid number of arguments!")

    # Make n links
    n = (len(args) - 1) // 3
    print(n)
    for i in range(n):
        node_a = args[3 * i]
        node_b = args[3 * (i + 1)]
        output = args[3 * i + 1]
        input = args[3 * i + 2]
        tree.links.new(node_b.inputs[input], node_a.outputs[output])

# Create the new material "Star Shader"
shader = bpy.data.materials["Star Shader"]
if not shader:
    shader = bpy.data.materials.new("Star Shader")

# Use nodes
shader.use_nodes = True
node_tree = shader.node_tree
nodes = node_tree.nodes
nodes.clear()

# Add Material Output node
material_output = make_node(nodes, "ShaderNodeOutputMaterial", 0, 0)

# Add an Emission Shader node
emission = make_node(nodes, 'ShaderNodeEmission', -200, 0)

# Add a math node for multiplication with light path
math_lightpath = make_math_node(nodes, "MULTIPLY", -400, 0)
light_path = make_node(nodes, "ShaderNodeLightPath", -600, 100)
connect_nodes(node_tree, light_path, "Is Camera Ray", 0, math_lightpath)

# Add a math node to control the intensity
math_intensity = make_math_node(nodes, "MULTIPLY", -600, 0, default_2 = 15)

# Add a node group for random intensity
group = bpy.data.node_groups.new("Random Intensity", "ShaderNodeTree")
group_inputs = group.nodes.new("NodeGroupInput")
group.inputs.new('NodeSocketFloat', "Random")
group_inputs.location = (0, 0)
group_outputs = group.nodes.new("NodeGroupOutput")
group.outputs.new("NodeSocketFloat", "Intensity")
group_outputs.location = (1200, 0)
# Add a math node to prepare random input
math_inp_fact = make_math_node(group.nodes, "MULTIPLY", 200, 0, default_2 = 9100)
# Add a math node to prepare input
math_pre_div = make_math_node(group.nodes, "DIVIDE", 400, 0, default_2 = 3.56)
# Add a math node to convert visual magnitude
math_mag_log = make_math_node(group.nodes, "LOGARITHM", 600, 0, default_2 = math.e)
# Add a math node to convert visual magnitude
math_mag_div = make_math_node(group.nodes, "DIVIDE", 800, 0, default_2 = -1.21)
# Add a math node to convert visual magnitude
math_mag_power = make_math_node(group.nodes, "POWER", 1000, 0, default_1 = 2.512)
# Connect nodes
connect_nodes(group, group_inputs, "Random",
    0, math_inp_fact, 0,
    0, math_pre_div, 0,
    0, math_mag_log, 0,
    0, math_mag_div, 0,
    1, math_mag_power, 0,
    "Intensity", group_outputs)
# Add group
random_magnitude = make_group_node(nodes, group, -800, 0)

# Make node group to split single random value into two
group = bpy.data.node_groups.new("Random Splitter", "ShaderNodeTree")
group_inputs = group.nodes.new("NodeGroupInput")
group.inputs.new('NodeSocketFloat', "Random")
group_inputs.location = (0, 0)
group_outputs = group.nodes.new("NodeGroupOutput")
group.outputs.new("NodeSocketFloat", "Random 1")
group.outputs.new("NodeSocketFloat", "Random 2")
group_outputs.location = (600, 0)
# Multiplication by large factor
math_rsplit_mult = make_math_node(group.nodes, "MULTIPLY", 200, -100, default_2 = 1000)
# Use only decimals
math_rsplit_mod = make_math_node(group.nodes, "MODULO", 400, -100, default_2 = 1)
# Connect nodes
connect_nodes(group, group_inputs, "Random", "Random 1", group_outputs)
connect_nodes(group, group_inputs, "Random",
    0, math_rsplit_mult, 0,
    0, math_rsplit_mod, 0,
    "Random 2", group_outputs)
# Add group
random_splitter = make_group_node(nodes, group, -1000, 0)

# Add geometry input node
geometry_input = make_node(nodes, "ShaderNodeObjectInfo", -1200, 0)

# Connect main node chain
connect_nodes(node_tree, geometry_input, "Random",
    "Random", random_splitter, "Random 1",
    "Random", random_magnitude, "Intensity",
    0, math_intensity, 0,
    1, math_lightpath, 0,
    "Strength", emission, "Emission",
    "Surface", material_output)
hide_node_outputs(light_path)
hide_node_outputs(geometry_input)

# Make node group for star color
group = bpy.data.node_groups.new("Random Star Color", "ShaderNodeTree")
group_inputs = group.nodes.new("NodeGroupInput")
group.inputs.new('NodeSocketFloat', "Random")
group_inputs.location = (0, 0)
group_outputs = group.nodes.new("NodeGroupOutput")
group.outputs.new("NodeSocketColor", "Color")
group_outputs.location = (800, 0)
# Color temperature width
math_kelvin_width = make_math_node(group.nodes, "MULTIPLY", 200, 0, default_2 = 17000)
# Color temperature offset
math_kelvin_offset = make_math_node(group.nodes, "ADD", 400, 0, default_2 = 3000)
# Blackbody color
blackbody = make_node(group.nodes, "ShaderNodeBlackbody", 600, 0)
# Connect nodes
connect_nodes(group, group_inputs, "Random",
    0, math_kelvin_width, 0,
    0, math_kelvin_offset, 0,
    "Temperature", blackbody, "Color",
    "Color", group_outputs)
# Add group
random_color = make_group_node(nodes, group, -600, -200)

# Connect color chain
connect_nodes(node_tree, random_splitter, "Random 2",
    "Random", random_color, "Color",
    "Color", emission)

# Set material
obj2.active_material = bpy.data.materials["Star Shader"]

#######################################################################################

# Add location constraint
# This keeps the stars fixed relatve to the camera
constraint = obj.constraints.new(type="COPY_LOCATION")
constraint.target = obj_camera = camera

# Add driver to object scale for the stars
# This makes the stars be as far away while still visible
fcurves = obj.driver_add("scale")
for fcurve in fcurves:
    # Add a variable for the camera focal length
    var = fcurve.driver.variables.new()
    var.name = "s"
    var.type = "SINGLE_PROP"
    target = var.targets[0]
    target.id_type = "CAMERA"
    target.id = camera.data.id_data
    target.data_path = "clip_end"

    # Set the driver expression
    fcurve.driver.expression = "0.9 * s"

# Add driver to object scale for the template
# This keeps the star size independent from focal length and render resolution
fcurves = obj2.driver_add("scale")
for fcurve in fcurves:
    # Add a variable for the camera focal length
    var = fcurve.driver.variables.new()
    var.name = "f"
    var.type = "SINGLE_PROP"
    target = var.targets[0]
    target.id_type = "CAMERA"
    target.id = camera.data.id_data
    target.data_path = "lens"

    # Add a variable for the render width
    var = fcurve.driver.variables.new()
    var.name = "x"
    var.type = "SINGLE_PROP"
    target = var.targets[0]
    target.id_type = "SCENE"
    target.id = bpy.context.scene.id_data
    target.data_path = "render.resolution_x"

    # Add a variable for the render height
    var = fcurve.driver.variables.new()
    var.name = "y"
    var.type = "SINGLE_PROP"
    target = var.targets[0]
    target.id_type = "SCENE"
    target.id = bpy.context.scene.id_data
    target.data_path = "render.resolution_y"

    # Add a variable for the resolution percentage
    var = fcurve.driver.variables.new()
    var.name = "p"
    var.type = "SINGLE_PROP"
    target = var.targets[0]
    target.id_type = "SCENE"
    target.id = bpy.context.scene.id_data
    target.data_path = "render.resolution_percentage"

    # Set the driver expression
    fcurve.driver.expression = "50 / f * 2202.907 / max(x, y) / p * 100"

# Set object relationship
obj2.parent = obj
obj.instance_type = "VERTS"
obj.use_instance_vertices_rotation = True
#obj.show_instancer_for_viewport = False
obj.show_instancer_for_render = False

# Hide the template
obj2.hide_viewport = True
#obj2.hide_render = True

# Add the object
bpy.context.collection.objects.link(obj)
bpy.context.collection.objects.link(obj2)
