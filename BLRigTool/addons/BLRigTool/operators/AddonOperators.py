import difflib
import json
from tokenize import group

import bpy
from bpy.props import FloatProperty
import math

from numpy.ma.core import shape

from ..config import __addon_name__
from ..functions import AddonFunctions
from ..functions.AddonFunctions import get_library_path, update_target_import
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

class WRYC_OT_SelectMappingActions(bpy.types.Operator):
    bl_idname = "wryc.ot_select_mapping_actions"
    bl_label = "Select Mapping Actions"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        settings = context.scene.bone_mapping_settings
        exiting_names = {a.name for a in settings.mapping_actions}
        old_states = {item.name: item.enabled for item in settings.mapping_actions}

        if bpy.data.actions:
            for action in bpy.data.actions:
                if not action.users and not action.use_fake_user:
                    continue

                if action.name not in exiting_names:
                    item = settings.mapping_actions.add()
                    item.name = action.name
                    item.enabled = old_states.get(action.name, False)

        valid_names = {a.name for a in bpy.data.actions}
        to_remove = [i for i, a in enumerate(settings.mapping_actions) if a.name not in valid_names]
        for i in reversed(to_remove):
            settings.mapping_actions.remove(i)
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        actions = context.scene.bone_mapping_settings.mapping_actions

        if not bpy.data.actions:
            layout.label(text="No actions in scene")
            return

        row = layout.row(align=True)
        row.operator("wryc.ot_enable_all_actions", text="Enable All")
        row.operator("wryc.ot_disable_all_actions", text="Disable All")

        box = layout.box()
        for entry in actions:
            box.prop(entry, "enabled", text=entry.name)

    def execute(self, context):
        settings = context.scene.bone_mapping_settings
        selected_actions = [a.name for a in settings.mapping_actions if a.enabled]
        if not selected_actions:
            self.report({'ERROR'}, "No actions selected.")
            return {'CANCELLED'}
        return {'FINISHED'}

class WRYC_OT_EnableAllActions(bpy.types.Operator):
    bl_idname = "wryc.ot_enable_all_actions"
    bl_label = "Enable All Actions"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        for entry in context.scene.bone_mapping_settings.mapping_actions:
            entry.enabled = True
        return {'FINISHED'}

class WRYC_OT_DisableAllActions(bpy.types.Operator):
    bl_idname = "wryc.ot_disable_all_actions"
    bl_label = "Disable All Actions"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        for entry in context.scene.bone_mapping_settings.mapping_actions:
            entry.enabled = False
        return {'FINISHED'}

class WRYC_OT_ApplyMappingToActions(bpy.types.Operator):
    bl_idname = "wryc.ot_apply_mapping_to_actions"
    bl_label = "Apply Mapping to Actions"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.bone_mapping_settings
        selected_actions = [a.name for a in settings.mapping_actions if a.enabled]
        bone_mappings = settings.mappings
        bone_mappings_dict = {m.source: m.target for m in bone_mappings}

        for action_name in selected_actions:
            action = bpy.data.actions.get(action_name)

            fcurve_to_modify = []

            for fcurve in action.fcurves:
                data_path = fcurve.data_path

                if 'pose.bones["' in data_path:
                    try:
                        start = data_path.find('pose.bones["') + len('pose.bones["')
                        end = data_path.find('"]', start)
                        old_bone = data_path[start:end]

                        if old_bone in bone_mappings_dict:
                            fcurve_to_modify.append((fcurve, old_bone))
                    except Exception as e:
                        print(f"Skipping {data_path}({e})")

            rename_count =0

            for fcurve, old_bone in fcurve_to_modify:
                new_bone = bone_mappings_dict[old_bone]
                new_path = fcurve.data_path.replace(f'["{old_bone}"]', f'["{new_bone}"]')
                fcurve.data_path = new_path

                group = action.groups.get(new_bone)
                if not group:
                    group = action.groups.new(name=new_bone)
                fcurve.group = group

                rename_count += 1
                print(f'renamed {old_bone} to {new_bone}')

        self.report({'INFO'}, f"Handled {len(selected_actions)} Actions" )
        return {'FINISHED'}

class WRYC_OT_BoneMappingGenerate(bpy.types.Operator):
    bl_idname = "wryc.ot_bone_mapping_generate"
    bl_label = "Create Bone List"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.bone_mapping_settings
        props.mappings.clear()

        src_names = []
        if props.source_type == 'ARMATURE' and props.source_armature:
            src_names = [b.name for b in props.source_armature.bones]
        elif props.source_type == 'ACTION' and props.source_action:
            for fc in props.source_action.fcurves:
                if "pose.bones" in fc.data_path:
                    path = fc.data_path
                    bone_name = path.split('"')[1]
                    if bone_name not in src_names:
                        src_names.append(bone_name)

        tgt_names = [b.name for b in props.target_armature.bones]

        for src_name in src_names:
            matches = difflib.get_close_matches(src_name, tgt_names, n=1, cutoff=0.3)
            if matches:
                item = props.mappings.add()
                item.source = src_name
                item.target = matches[0]

        if props.mappings:
            props.active_index = 0
            props.target_import = props.mappings[0].target
        else:
            props.active_index = -1
            props.target_import = ""

        self.report({'INFO'}, "Bone Mapping Generated")
        return {'FINISHED'}

class WRYC_OT_BoneMappingLock(bpy.types.Operator):
    bl_idname = "wryc.ot_bone_mapping_lock"
    bl_label = "Lock Mapping List"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.bone_mapping_settings
        props.lock_mappings = not props.lock_mappings
        return {'FINISHED'}

class WRYC_OT_TargetBoneImport(bpy.types.Operator):
    bl_idname = "wryc.ot_target_bone_import"
    bl_label = "Target Bone :"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.bone_mapping_settings

        if 0 <= props.active_index < len(props.mappings):
            new_target = AddonProperties.BoneMappingSettings.target_import.strip()
            if new_target:
                props.mappings[props.active_index].target = new_target
                self.report({'INFO'}, f"Mapping updated to: {new_target}")
                return {'FINISHED'}
        else:
            self.report({'WARNING'}, "Mapping not found.")
            return {'CANCELLED'}

class WRYC_OT_BoneMappingExport(bpy.types.Operator):
    bl_idname = "wryc.ot_bone_mapping_export"
    bl_label = "Export"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        props = context.scene.bone_mapping_settings
        data = [{"source": m.source, "target":m.target} for m in props.mappings]
        with open(self.filepath, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        self.report({'INFO'}, "Bone Mapping Exported")
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class WRYC_OT_BoneMappingImport(bpy.types.Operator):
    bl_idname = "wryc.ot_bone_mapping_import"
    bl_label = "Import"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        props = context.scene.bone_mapping_settings
        with open(self.filepath, "r", encoding='utf-8') as f:
            data = json.load(f)
        props.mappings.clear()
        for item in data:
            map_item = props.mappings.add()
            map_item.source = item["source", ""]
            map_item.target = item["target", ""]
        props.active_index = 0
        self.report({'INFO'}, "Bone Mapping Imported")
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
                self.report({'ERROR'}, "Please selected Mesh Object")
                return {'CANCELLED'}

            if target == 'VERTEX_GROUP':
                data_list = obj.vertex_groups

            elif target == 'SHAPE_KEY':
                if not obj.data.shape_keys:
                    continue
                data_list = obj.data.shape_keys.key_blocks
            else:
                return {'CANCELLED'}


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

    def get_Target_bone_enum(self, context):
        arm = self.target_armature
        if arm:
            return [(b.name, b.name, "") for b in arm.bones]
        return []
