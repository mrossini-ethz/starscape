import bpy

class StarscapePanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Starscape"
    bl_idname = "OBJECT_PT_starscape"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "world"

    def draw(self, context):
        props = bpy.context.scene.starscape_properties

        layout = self.layout
        layout.operator("world.starscape")
