import bpy
from ....common.types.framework import reg_order


class BasePanel(object):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BL Rig Tool"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True


@reg_order(0)
class WRYC_PT_CustomDisplayBone(BasePanel, bpy.types.Panel):
    bl_label = "Custom Display Shape"
    bl_idname = "WRYC_PT_custom_display_bone"

    def draw(self, context):

        layout = self.layout
        row = layout.row(align=True)
        row.menu("WRYC_MT_generate_icon_menu", icon='DOWNARROW_HLT')
        row.prop(context.window_manager.bone_shapes_library, "bone_shape", expand=False, text="")

        settings = context.scene.bone_display_settings

        layout.prop(settings, "scale_bone_length_enable")
        layout.operator("wryc.ot_custom_bone_shape")

        layout.label(text="Scale")
        layout.prop(settings, "scale", text="Scale All")
        layout.prop(settings, "scale_enable")
        if not settings.scale_enable:
            col = layout.column()
            col.prop(settings, "scale_x")
            col.prop(settings, "scale_y")
            col.prop(settings, "scale_z")
        layout.operator("wryc.ot_custom_bone_scale")

        layout.label(text="Translation")
        layout.prop(settings, "loc_x")
        layout.prop(settings, "loc_y")
        layout.prop(settings, "loc_z")
        layout.operator("wryc.ot_custom_bone_loc")


        layout.label(text="Rotation")
        layout.prop(settings, "rot_x")
        layout.prop(settings, "rot_y")
        layout.prop(settings, "rot_z")
        layout.operator("wryc.ot_custom_bone_rot")

        layout.operator("wryc.ot_custom_display_bone", icon = 'BONE_DATA')

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

@reg_order(1)
class WRYC_PT_GenerateConstraint(BasePanel, bpy.types.Panel):
    bl_label = "Generate Constraint"
    bl_idname = "WRYC_PT_generate_constraint"

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        layout.label(text="Remove Constraints")
        layout.operator("wryc.ot_remove_constrains")

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

@reg_order(2)
class WRYC_PT_RenameTool(BasePanel, bpy.types.Panel):
    bl_label = "Rename Tool"
    bl_idname = "WRYC_PT_vertex_group_tools"

    def draw(self, context):
        props = context.scene.rename_tool
        layout = self.layout
        layout.label(text="Replace Name")

        layout.prop(props, "rename_target")
        layout.prop(props, "rename_mode")

        if props.rename_mode == 'FIND_REPLACE':
            layout.prop(props, "find_str")
            layout.prop(props, "replace_str")
        elif props.rename_mode == 'SET_PREFIX_SUFFIX':
            layout.prop(props, "prefix_str")
            layout.prop(props, "suffix_str")
        elif props.rename_mode == 'REMOVE_PREFIX_SUFFIX':
            layout.prop(props, "prefix_str")
            layout.prop(props, "suffix_str")

        layout.operator("wryc.ot_rename_tool")


