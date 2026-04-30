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
    bl_label = "Custom Display Bone"
    bl_idname = "WRYC_PT_custom_display_bone"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.bone_display_settings

        box = layout.box()
        box.label(text="Shape")
        row = box.row(align=True)
        row.menu("WRYC_MT_generate_icon_menu", icon='DOWNARROW_HLT')
        row.prop(settings, "bone_shape", expand=False, text="")
        box.prop(settings, "scale_bone_length_enable")
        box.operator("wryc.ot_custom_bone_shape")

        box = layout.box()
        box.label(text="Color")
        col = box.column(align=True)
        split = col.split(factor=0.4, align=True)
        split.label(text="Bone Color:")
        split.prop(settings, "bone_color", text="")
        split = col.split(factor=0.4, align=True)
        split.label(text="Pose Bone Color:")
        split.prop(settings, "pose_bone_color", text="")
        box.operator("wryc.ot_custom_bone_color")

        box = layout.box()
        box.label(text="Scale")
        box.prop(settings, "scale", text="Scale All")
        box.prop(settings, "scale_enable")
        if not settings.scale_enable:
            col = box.column()
            col.prop(settings, "scale_x")
            col.prop(settings, "scale_y")
            col.prop(settings, "scale_z")
        box.operator("wryc.ot_custom_bone_scale")

        box = layout.box()
        box.label(text="Translation")
        box.prop(settings, "loc_x")
        box.prop(settings, "loc_y")
        box.prop(settings, "loc_z")
        box.operator("wryc.ot_custom_bone_loc")

        box = layout.box()
        box.label(text="Rotation")
        box.prop(settings, "rot_x")
        box.prop(settings, "rot_y")
        box.prop(settings, "rot_z")
        box.operator("wryc.ot_custom_bone_rot")

        layout.operator("wryc.ot_copy_selected_bone_display_config")
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

        layout.label(text="Generate Deform Bones")
        layout.operator("wryc.ot_create_deform_bones")
        layout.operator("wryc.ot_create_manny_deform_bones")
        layout.operator("wryc.ot_connect_deform_armature")
        layout.operator("wryc.ot_set_inverse_all_child_of")

        layout.label(text="Generate Constraints")
        layout.operator("wryc.ot_create_head_controller")
        layout.operator("wryc.ot_create_spine_controller")
        layout.operator("wryc.ot_create_arm_controller")
        layout.operator("wryc.ot_create_leg_controller")
        layout.operator("wryc.ot_create_finger_controller")
        layout.operator("wryc.ot_create_manny_controller")

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

@reg_order(2)
class WRYC_PT_RetargetActions(BasePanel, bpy.types.Panel):
    bl_label = "Retarget Actions"
    bl_idname = "WRYC_PT_retarget_actions"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.bone_mapping_settings

        row = layout.row()
        row.prop(settings, "show_mappings_settings", text="", icon='TRIA_DOWN' if settings.show_mappings_settings else 'TRIA_RIGHT', emboss=False)
        row.label(text="Mapping Settings")

        if settings.show_mappings_settings:
            layout.label(text="Mapping Source/Target Settings")
            layout.prop(settings, "source_type", text="Source Type")
            if settings.source_type == 'ARMATURE':
                layout.prop(settings, "source_armature", text="Armature")
            else:
                layout.prop(settings, "source_action", text="Action")

            layout.prop(settings, "target_armature", text="Target")

            row = layout.row()
            row.enabled = settings.target_armature is not None and (
                (settings.source_type == 'ARMATURE' and settings.source_armature is not None) or
                (settings.source_type == 'ACTION' and settings.source_action is not None)
            )
            row.operator("wryc.ot_bone_mapping_generate")

            layout.separator()

            layout.label(text="Bone Mapping List")
            layout.template_list("UI_UL_list", "bone_mapping_list", settings, "mappings", settings, "active_index")
            layout.operator("wryc.ot_bone_mapping_lock", icon='LOCKED' if settings.lock_mappings else 'UNLOCKED')

            row = layout.row()
            row.enabled =  len(settings.mappings) > 0 and settings.lock_mappings == False
            row.prop(settings, "target_import")

            row = layout.row()
            row.enabled = len(settings.mappings) > 0
            row.operator("wryc.ot_bone_mapping_import", icon='IMPORT')
            row.operator("wryc.ot_bone_mapping_export", icon='EXPORT')

        layout.separator()

        layout.operator("wryc.ot_select_mapping_actions")
        layout.operator("wryc.ot_apply_mapping_to_actions")

@reg_order(3)
class WRYC_PT_RenameTool(BasePanel, bpy.types.Panel):
    bl_label = "Rename Tool"
    bl_idname = "WRYC_PT_rename_tool"

    def draw(self, context):
        layout = self.layout
        settings = context.scene.rename_tool
        layout.label(text="Replace Name")

        layout.prop(settings, "rename_target")
        layout.prop(settings, "rename_mode")

        if settings.rename_mode == 'FIND_REPLACE':
            layout.prop(settings, "find_str")
            layout.prop(settings, "replace_str")
        elif settings.rename_mode == 'SET_PREFIX_SUFFIX':
            layout.prop(settings, "prefix_str")
            layout.prop(settings, "suffix_str")
        elif settings.rename_mode == 'REMOVE_PREFIX_SUFFIX':
            layout.prop(settings, "prefix_str")
            layout.prop(settings, "suffix_str")

        layout.operator("wryc.ot_rename_tool")

#__RETARGET LIST__
class UI_UL_list(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_props, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            row.label(text=item.source)
            row.label(text=item.target)
        elif self.layout_type =='GRID':
            layout.label(text="")