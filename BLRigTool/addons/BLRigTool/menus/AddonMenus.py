import bpy
from ..operators import AddonOperators
from bpy.types import Menu



class WRYC_MT_GenerateIconMenu(Menu):
    bl_idname = "WRYC_MT_generate_icon_menu"
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        layout.operator("wryc.ot_generate_shape_icon", icon="ADD", text="Generate Icon for selected object")
        layout.operator("wryc.ot_remove_bone_shape_icon", icon="REMOVE", text="Remove Icon")
        layout.operator("wryc.ot_reload_bone_icons", icon="FILE_REFRESH", text="Reload Bone Shape Icons")

