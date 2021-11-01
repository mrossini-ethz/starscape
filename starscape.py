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

#######################################################################################

def hide_node_outputs(node):
    for socket in node.outputs:
        if not socket.is_linked:
            socket.hide = True

# Set material
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
material_output = nodes.new("ShaderNodeOutputMaterial")
material_output.location = (0, 0)

# Add an Emission Shader node
emission = nodes.new('ShaderNodeEmission')
emission.location = (-200, 0)
node_tree.links.new(material_output.inputs["Surface"], emission.outputs["Emission"])

# Add a math node for multiplication with light path
math_lightpath = nodes.new("ShaderNodeMath")
math_lightpath.operation = "MULTIPLY"
math_lightpath.location = (-400, 0)
light_path = nodes.new("ShaderNodeLightPath")
light_path.location = (-600, 100)
node_tree.links.new(math_lightpath.inputs[0], light_path.outputs["Is Camera Ray"])
node_tree.links.new(emission.inputs["Strength"], math_lightpath.outputs[0])
hide_node_outputs(light_path)

# Add a math node to control the intensity
math_intensity = nodes.new("ShaderNodeMath")
math_intensity.operation = "MULTIPLY"
math_intensity.inputs[1].default_value = 15 # <<<<<<<<<<<<<<<<<<<<<<<<<<<< FXIME
math_intensity.location = (-600, 0)
node_tree.links.new(math_lightpath.inputs[1], math_intensity.outputs[0])

# Add a node group for random intensity
group = bpy.data.node_groups.new("Random Intensity", "ShaderNodeTree")
group_inputs = group.nodes.new("NodeGroupInput")
group.inputs.new('NodeSocketFloat', "Random")
group_inputs.location = (0, 0)
group_outputs = group.nodes.new("NodeGroupOutput")
group.outputs.new("NodeSocketFloat", "Intensity")
group_outputs.location = (1200, 0)

# Add a math node to prepare random input
math_inp_fact = group.nodes.new("ShaderNodeMath")
math_inp_fact.operation = "MULTIPLY"
math_inp_fact.inputs[1].default_value = 9100
math_inp_fact.location = (200, 0)
group.links.new(math_inp_fact.inputs[0], group_inputs.outputs[0])

# Add a math node to prepare input
math_pre_div = group.nodes.new("ShaderNodeMath")
math_pre_div.operation = "DIVIDE"
math_pre_div.inputs[1].default_value = 3.56
math_pre_div.location = (400, 0)
group.links.new(math_pre_div.inputs[0], math_inp_fact.outputs[0])

# Add a math node to convert visual magnitude
math_mag_log = group.nodes.new("ShaderNodeMath")
math_mag_log.operation = "LOGARITHM"
math_mag_log.inputs[1].default_value = math.e
math_mag_log.location = (600, 0)
group.links.new(math_mag_log.inputs[0], math_pre_div.outputs[0])

# Add a math node to convert visual magnitude
math_mag_div = group.nodes.new("ShaderNodeMath")
math_mag_div.operation = "DIVIDE"
math_mag_div.inputs[1].default_value = -1.21
math_mag_div.location = (800, 0)
group.links.new(math_mag_div.inputs[0], math_mag_log.outputs[0])

# Add a math node to convert visual magnitude
math_mag_power = group.nodes.new("ShaderNodeMath")
math_mag_power.operation = "POWER"
math_mag_power.inputs[0].default_value = 2.512
math_mag_power.location = (1000, 0)
group.links.new(math_mag_power.inputs[1], math_mag_div.outputs[0])
group.links.new(group_outputs.inputs[0], math_mag_power.outputs[0])

random_magnitude = nodes.new("ShaderNodeGroup")
random_magnitude.node_tree = group
random_magnitude.location = (-800, 0)
node_tree.links.new(math_intensity.inputs[0], random_magnitude.outputs["Intensity"])

group = bpy.data.node_groups.new("Random Splitter", "ShaderNodeTree")
group_inputs = group.nodes.new("NodeGroupInput")
group.inputs.new('NodeSocketFloat', "Random")
group_inputs.location = (0, 0)
group_outputs = group.nodes.new("NodeGroupOutput")
group.outputs.new("NodeSocketFloat", "Random 1")
group.outputs.new("NodeSocketFloat", "Random 2")
group_outputs.location = (600, 0)
group.links.new(group_outputs.inputs["Random 1"], group_inputs.outputs["Random"])

math_rsplit_mult = group.nodes.new("ShaderNodeMath")
math_rsplit_mult.operation = "MULTIPLY"
math_rsplit_mult.inputs[1].default_value = 1000
math_rsplit_mult.location = (200, -100)
group.links.new(math_rsplit_mult.inputs[0], group_inputs.outputs["Random"])

math_rsplit_mod = group.nodes.new("ShaderNodeMath")
math_rsplit_mod.operation = "MODULO"
math_rsplit_mod.inputs[1].default_value = 1
math_rsplit_mod.location = (400, -100)
group.links.new(math_rsplit_mod.inputs[0], math_rsplit_mult.outputs[0])
group.links.new(group_outputs.inputs["Random 2"], math_rsplit_mod.outputs[0])

random_splitter = nodes.new("ShaderNodeGroup")
random_splitter.node_tree = group
random_splitter.location = (-1000, 0)
node_tree.links.new(random_magnitude.inputs["Random"], random_splitter.outputs["Random 1"])

geometry_input = nodes.new("ShaderNodeObjectInfo")
geometry_input.location = (-1200, 0)
node_tree.links.new(random_splitter.inputs["Random"], geometry_input.outputs["Random"])
hide_node_outputs(geometry_input)

group = bpy.data.node_groups.new("Random Star Color", "ShaderNodeTree")
group_inputs = group.nodes.new("NodeGroupInput")
group.inputs.new('NodeSocketFloat', "Random")
group_inputs.location = (0, 0)
group_outputs = group.nodes.new("NodeGroupOutput")
group.outputs.new("NodeSocketColor", "Color")
group_outputs.location = (800, 0)

math_kelvin_width = group.nodes.new("ShaderNodeMath")
math_kelvin_width.operation = "MULTIPLY"
math_kelvin_width.inputs[1].default_value = 17000
math_kelvin_width.location = (200, 0)
group.links.new(math_kelvin_width.inputs[0], group_inputs.outputs["Random"])

math_kelvin_offset = group.nodes.new("ShaderNodeMath")
math_kelvin_offset.operation = "ADD"
math_kelvin_offset.inputs[1].default_value = 3000
math_kelvin_offset.location = (400, 0)
group.links.new(math_kelvin_offset.inputs[0], math_kelvin_width.outputs[0])

blackbody = group.nodes.new("ShaderNodeBlackbody")
blackbody.location = (600, 0)
group.links.new(blackbody.inputs["Temperature"], math_kelvin_offset.outputs[0])
group.links.new(group_outputs.inputs["Color"], blackbody.outputs["Color"])

random_color = nodes.new("ShaderNodeGroup")
random_color.node_tree = group
random_color.location = (-600, -200)
node_tree.links.new(random_color.inputs["Random"], random_splitter.outputs["Random 2"])
node_tree.links.new(emission.inputs["Color"], random_color.outputs["Color"])

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