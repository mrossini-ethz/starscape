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
        layout.prop(props, "random_seed")
        layout.prop(props, "star_density")
        layout.prop(props, "star_intensity")
        layout.prop(props, "hemisphere")
        layout.prop(props, "camera_lock")
        layout.prop(props, "clear_world_bg")
        layout.operator("world.starscape")
