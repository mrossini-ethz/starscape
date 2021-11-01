import bpy

class StarscapeProperties(bpy.types.PropertyGroup):
    seed: bpy.props.FloatProperty(name="Seed", default=0)
