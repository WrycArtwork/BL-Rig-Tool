import bpy
from bpy.props import FloatProperty
import math

from numpy.ma.core import shape

from ..config import __addon_name__
from ..functions import AddonFunctions
from ..functions.AddonFunctions import get_library_path
from ..properties import AddonProperties

class WRYC_OT_GenerateShapeIcon(bpy.types.Operator):
    bl_idname = "wryc.ot_generate_shape_icon"
    bl_label = "Generate Icon"
    bl_description = "Render selected object and save as icon"
    bl_options = {'REGISTER', 'UNDO'}

    camera_distance: bpy.props.FloatProperty(
        name = "camera distance",
        default = 2,
        description = "Distance between camera and object",
    )

    camera_angle: bpy.props.EnumProperty(
        name = "camera angle",
        items = [
            ("TOP", "TOP", "Render camera look Straight from Z axis"),
            ("DIAGONAL", "DIAGONAL", "Render camera look diagonal top-down"),
        ],
        default = "TOP",
    )

    keep_generated: bpy.props.BoolProperty(
        name = "Keep generated",
        default = False,
        description = "Keep generated camera and light in scene",
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "camera_distance")
        layout.prop(self, "camera_angle")
        layout.prop(self, "keep_generated")

    def execute(self, context):
        return AddonFunctions.generate_icon(self, context, self.camera_distance, self.camera_angle, self.keep_generated)

class WRYC_OT_RemoveBoneShapeIcon(bpy.types.Operator):
    bl_idname = "wryc.ot_remove_bone_shape_icon"
    bl_label = "Remove Icon"
    bl_description = "Remove bone shape icon"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        AddonFunctions.remove_icon(self, context)
        return {'FINISHED'}

class WRYC_OT_ReloadBoneShapeIcons(bpy.types.Operator):
    bl_idname = "wryc.ot_reload_bone_icons"
    bl_label = "Reload Icons"
    bl_description = "Reload Bone Shape Icons"

    def execute(self,context):
        AddonFunctions.unload_icon_preview()
        AddonFunctions.load_icon_preview()

        context.window_manager.bone_shapes_library.bone_shape = context.window_manager.bone_shapes_library.bone_shape

        return {'FINISHED'}

class WRYC_OT_CustomBoneShape(bpy.types.Operator):
    bl_idname = "wryc.ot_custom_bone_shape"
    bl_label = "Apply Bone Shape"
    bl_description = "Apply bone shape to the selection bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}

        bones = AddonFunctions.get_selected_bones(context, self)
        if not bones:
            return {'CANCELLED'}

        shape_name = context.window_manager.bone_shapes_library.bone_shape
        if not shape_name or shape_name == "None":
            self.report({'INFO'}, "No bone shape selected")
            return {'CANCELLED'}

        blend_path = get_library_path()
        with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
            if shape_name in data_from.objects:
                data_to.objects = [shape_name]

        shape_obj = bpy.data.objects.get(shape_name)
        if not shape_obj:
            self.report({'ERROR'}, f"Object '{shape_name}' not found or cannot be loaded")
            return {'CANCELLED'}

        settings = context.scene.bone_display_settings

        for pbone in bones:
            pbone.custom_shape = shape_obj
            pbone.use_custom_shape_bone_size = settings.scale_bone_length_enable
        self.report({'INFO'}, f"Apply bone shape shape name = {shape_name}")

        return {'FINISHED'}

class WRYC_OT_CustomBoneScale(bpy.types.Operator):
    bl_idname = "wryc.ot_custom_bone_scale"
    bl_label = "Apply Scale"
    bl_description = "Apply bone scale to the selection bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}

        bones = AddonFunctions.get_selected_bones(context, self)
        if not bones:
            return {'CANCELLED'}

        self.report({'INFO'}, "Pose mode is ON, Apply bone scale")

        settings = context.scene.bone_display_settings

        if settings.scale_enable:
            scale_x = scale_y = scale_z = settings.scale
        else:
            scale_x = settings.scale_x
            scale_y = settings.scale_y
            scale_z = settings.scale_z

        for pbone in bones:
            pbone.custom_shape_scale_xyz = (scale_x, scale_y, scale_z)

        return {'FINISHED'}

class WRYC_OT_CustomBoneLoc(bpy.types.Operator):
    bl_idname = "wryc.ot_custom_bone_loc"
    bl_label = "Apply Translation"
    bl_description = "Apply bone translation to the selection bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}

        bones = AddonFunctions.get_selected_bones(context, self)
        if not bones:
            return {'CANCELLED'}

        self.report({'INFO'}, "Pose mode is ON, Apply bone Translation")

        settings = context.scene.bone_display_settings

        for pbone in bones:
            pbone.custom_shape_translation = (settings.loc_x,
                            settings.loc_y,
                            settings.loc_z)

        return {'FINISHED'}

class WRYC_OT_CustomBoneRot(bpy.types.Operator):
    bl_idname = "wryc.ot_custom_bone_rot"
    bl_label = "Apply Rotation"
    bl_description = "Apply bone Rotation to the selection bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}

        bones = AddonFunctions.get_selected_bones(context, self)
        if not bones:
            return {'CANCELLED'}

        self.report({'INFO'}, "Pose mode is ON, Apply bone Rotation")

        settings = context.scene.bone_display_settings

        for pbone in bones:
            pbone.custom_shape_rotation_euler = (math.radians(settings.rot_x),
                                    math.radians(settings.rot_y),
                                    math.radians(settings.rot_z))

        return {'FINISHED'}

class WRYC_OT_CustomDisplayBone(bpy.types.Operator):
    bl_idname = "wryc.ot_custom_display_bone"
    bl_label = "Apply All"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}

        bones = AddonFunctions.get_selected_bones(context, self)
        if not bones:
            return {'CANCELLED'}

        self.report({'INFO'}, "Pose mode is ON, Apply All")

        shape_name = context.window_manager.bone_shapes_library.bone_shape
        if not shape_name or shape_name == "None":
            self.report({'INFO'}, "No bone shape selected")
            return {'CANCELLED'}

        blend_path = get_library_path()
        with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
            if shape_name in data_from.objects:
                data_to.objects = [shape_name]

        shape_obj = bpy.data.objects.get(shape_name)
        if not shape_obj:
            self.report({'ERROR'}, f"Object '{shape_name}' not found or cannot be loaded")
            return {'CANCELLED'}

        settings = context.scene.bone_display_settings

        if settings.scale_enable:
            scale_x = scale_y = scale_z = settings.scale
        else:
            scale_x = settings.scale_x
            scale_y = settings.scale_y
            scale_z = settings.scale_z

        for pbone in bones:
            pbone.custom_shape = shape_obj
            pbone.custom_shape_scale_xyz = (scale_x, scale_y, scale_z)
            pbone.custom_shape_translation = (settings.loc_x, settings.loc_y, settings.loc_z)
            pbone.custom_shape_rotation_euler = (math.radians(settings.rot_x), math.radians(settings.rot_y),math.radians(settings.rot_z))

        return {'FINISHED'}

class WRYC_OT_RemoveConstrains(bpy.types.Operator):
    bl_idname = "wryc.ot_remove_constrains"
    bl_label = "Remove Constraints"
    bl_description = "Remove constraints"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}

        bones = AddonFunctions.get_selected_bones(context, self)
        if not bones:
            return {'CANCELLED'}

        self.report({'INFO'}, "Pose mode is ON, Remove Selected Bones Constraints")

        selected_bones = bpy.context.selected_pose_bones
        for bone in selected_bones:
            for con in list(bone.constraints):
                bone.constraints.remove(con)

        return {'FINISHED'}

class WRYC_OT_RenameTool(bpy.types.Operator):
    bl_idname = "wryc.ot_rename_tool"
    bl_label = "Apply "
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.rename_tool
        target = props.rename_target
        mode = props.rename_mode
        renamed_count = 0

        for obj in context.selected_objects:
            if obj.type != 'MESH':
                continue

            if target == 'VERTEX_GROUP':
                data_list = obj.vertex_groups

            elif target == 'SHAPE_KEY':
                if not obj.data.shape_keys:
                    continue
                data_list = obj.data.shape_keys.key_blocks
            else:
                continue

            for item in data_list:
                old_name = item.name
                new_name = old_name

                if mode == 'FIND_REPLACE':
                    if props.find_str in old_name:
                        new_name = old_name.replace(props.find_str, props.replace_str)

                elif mode == 'SET_PREFIX_SUFFIX':
                    new_name = props.prefix_str + old_name + props.suffix_str

                elif mode == 'REMOVE_PREFIX_SUFFIX':
                    if props.prefix_str and new_name.startswith(props.prefix_str):
                        new_name = new_name[len(props.prefix_str):]
                    if props.suffix_str and new_name.endswith(props.suffix_str):
                        new_name = new_name[:-len(props.suffix_str)]

                if new_name != old_name:
                    if new_name in obj.vertex_groups:
                        self.report({'WARNING'}, f"{obj.name} already exists{new_name}")
                        continue

                    item.name = new_name
                    renamed_count += 1
                    self.report({'INFO'}, f"{obj.name} has been renamed to '{new_name}'")

            self.report({'INFO'}, f"{renamed_count} vertex group names have been renamed")
            return {'FINISHED'}
