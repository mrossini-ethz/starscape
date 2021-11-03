import bpy

class StarscapeProperties(bpy.types.PropertyGroup):
    random_seed: bpy.props.IntProperty(name="Random Seed", default=0, min=0, description="Initial value for the random number generator that determines the random outcome of the starscape generation.")
    star_density: bpy.props.FloatProperty(name="Star Density", default=1.0, min=0.0, max=10.0, description="Density of stars relative to near-earth conditions.")
    star_intensity: bpy.props.FloatProperty(name="Star Intensity", default=1.0, min=0.0, description="Brightness of the rendered stars.")
    hemisphere: bpy.props.BoolProperty(name="Hemisphere", default=False, description="Generate only stars above the horizon.")
    camera_lock: bpy.props.BoolProperty(name="Lock To Camera", default=True, description="Locks the starscape object to the camera.")
