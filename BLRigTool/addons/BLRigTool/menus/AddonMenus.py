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

class WRYC_MT_AddUE5Manny(Menu):
    bl_idname = "WRYC_MT_add_ue5_manny_menu"
    bl_label = "Add UE5 Manny (Simple)"

    def draw(self, context):
        layout = self.layout
        layout.operator("wryc.ot_add_ue5_manny", icon="ARMATURE_DATA", text="Only Bones").import_mesh = False
        layout.operator("wryc.ot_add_ue5_manny", icon="OUTLINER_OB_ARMATURE", text="With Mesh").import_mesh = True