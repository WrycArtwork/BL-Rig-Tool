import difflib
import json
import os

import bpy
import math
import mathutils

from ..functions import AddonFunctions
from ..properties import AddonProperties
from ..utils import AddonUtils

#__CUSTOM DISPLAY SHAPE__
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
        name = "Keep generated camera & light",
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
        context.scene.bone_display_settings.bone_shape = context.scene.bone_display_settings.bone_shape

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

        shape_name = context.scene.bone_display_settings.bone_shape
        if not shape_name or shape_name == "None":
            self.report({'INFO'}, "No bone shape selected")
            return {'CANCELLED'}

        blend_path = AddonFunctions.get_library_path()
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

        self.report({'INFO'}, f"Success apply bone shape.")
        return {'FINISHED'}

class WRYC_OT_CustomBoneColor(bpy.types.Operator):
    bl_idname = "wryc.ot_custom_bone_color"
    bl_label = "Apply Color"
    bl_description = "Apply bone color to the selection bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}

        bones = AddonFunctions.get_selected_bones(context, self)
        if not bones:
            return {'CANCELLED'}

        armature = context.active_object

        settings = context.scene.bone_display_settings

        for pbone in bones:
            armature.data.bones[pbone.name].color.palette = settings.bone_color
            armature.pose.bones[pbone.name].color.palette = settings.pose_bone_color

        self.report({'INFO'}, "Success apply bone color")
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

        settings = context.scene.bone_display_settings

        if settings.scale_enable:
            scale_x = scale_y = scale_z = settings.scale
        else:
            scale_x = settings.scale_x
            scale_y = settings.scale_y
            scale_z = settings.scale_z

        for pbone in bones:
            pbone.custom_shape_scale_xyz = (scale_x, scale_y, scale_z)

        self.report({'INFO'}, "Success apply bone scale")
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

        settings = context.scene.bone_display_settings

        for pbone in bones:
            pbone.custom_shape_translation = (settings.loc_x,
                            settings.loc_y,
                            settings.loc_z)

        self.report({'INFO'}, "Success apply bone Translation")
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

        settings = context.scene.bone_display_settings

        for pbone in bones:
            pbone.custom_shape_rotation_euler = (math.radians(settings.rot_x),
                                    math.radians(settings.rot_y),
                                    math.radians(settings.rot_z))

        self.report({'INFO'}, "Success apply bone Rotation")
        return {'FINISHED'}

class WRYC_OT_CopySelectedBoneDisplayConfig(bpy.types.Operator):
    bl_idname = "wryc.ot_copy_selected_bone_display_config"
    bl_label = "Copy From Selected"
    bl_description = "Copy bone display config from selected bone."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}

        bones = AddonFunctions.get_selected_bones(context, self)
        if not bones:
            return {'CANCELLED'}

        settings = context.scene.bone_display_settings
        pbone = bones[0]
        armature = context.active_object

        if pbone.custom_shape:
            settings.bone_shape = pbone.custom_shape.name

        settings.scale_bone_length_enable = pbone.use_custom_shape_bone_size

        settings.bone_color = armature.data.bones[pbone.name].color.palette
        settings.pose_bone_color = armature.pose.bones[pbone.name].color.palette

        settings.loc_x = pbone.custom_shape_translation.x
        settings.loc_y = pbone.custom_shape_translation.y
        settings.loc_z = pbone.custom_shape_translation.z

        rot = pbone.custom_shape_rotation_euler
        settings.rot_x = math.degrees(rot.x)
        settings.rot_y = math.degrees(rot.y)
        settings.rot_z = math.degrees(rot.z)

        scale = pbone.custom_shape_scale_xyz
        if scale.x == scale.y == scale.z:
            settings.scale_enable = True
            settings.scale = scale.x
        else:
            settings.scale_enable = False
            settings.scale_x = scale.x
            settings.scale_y = scale.y
            settings.scale_z = scale.z

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

        shape_name = context.scene.bone_display_settings.bone_shape
        if not shape_name or shape_name == "None":
            self.report({'INFO'}, "No bone shape selected")
            return {'CANCELLED'}

        blend_path = AddonFunctions.get_library_path()
        with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
            if shape_name in data_from.objects:
                data_to.objects = [shape_name]

        settings = context.scene.bone_display_settings
        armature = context.active_object

        shape_obj = bpy.data.objects.get(shape_name)
        if not shape_obj:
            self.report({'ERROR'}, f"Object '{shape_name}' not found or cannot be loaded")
            return {'CANCELLED'}

        if settings.scale_enable:
            scale_x = scale_y = scale_z = settings.scale
        else:
            scale_x = settings.scale_x
            scale_y = settings.scale_y
            scale_z = settings.scale_z

        for pbone in bones:
            armature.data.bones[pbone.name].color.palette = settings.bone_color
            armature.pose.bones[pbone.name].color.palette = settings.pose_bone_color
            pbone.custom_shape = shape_obj
            pbone.use_custom_shape_bone_size = settings.scale_bone_length_enable
            pbone.custom_shape_scale_xyz = (scale_x, scale_y, scale_z)
            pbone.custom_shape_translation = (settings.loc_x, settings.loc_y, settings.loc_z)
            pbone.custom_shape_rotation_euler = (math.radians(settings.rot_x), math.radians(settings.rot_y),math.radians(settings.rot_z))

        self.report({'INFO'}, "Success apply All")
        return {'FINISHED'}

#__GENERATE CONSTRAINTS__
class WRYC_OT_ConnectDeformArmature(bpy.types.Operator):
    bl_idname = "wryc.ot_connect_deform_armature"
    bl_label = "Connect Deform Armature"
    bl_description = "Create deform bones from source armature and bind to target armature."
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        if context.mode != 'OBJECT':
            self.report({'ERROR'}, "Please into Object mode")
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        settings = context.scene.deform_settings

        layout = self.layout
        layout.label(text="Connect Deform Armature")
        layout.prop_search(settings, "src_obj", context.scene, "objects", text="Source Armature")
        layout.prop_search(settings, "tgt_obj", context.scene, "objects", text="Target Armature")

    def execute(self, context):
        settings = context.scene.deform_settings
        pref = AddonFunctions.get_preferences()

        def_obj = settings.src_obj
        tgt_obj = settings.tgt_obj
        def_arm = def_obj.data
        tgt_arm = tgt_obj.data

        if not def_obj or not tgt_obj:
            self.report({'ERROR'}, "Please select both armatures.")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='OBJECT')
        context.view_layer.objects.active = tgt_obj
        bpy.ops.object.mode_set(mode='EDIT')

        if "Deform Bones" not in tgt_arm.collections:
            tgt_arm.collections.new("Deform Bones")
        deform_col = tgt_arm.collections["Deform Bones"]

        def_bones = []

        for src_bone in def_arm.bones:
            src_name = src_bone.name
            def_name = f"{pref.deform_prefix}{src_name}"

            if src_name not in tgt_arm.bones:
                continue

            tgt_bone = tgt_arm.bones[src_name]

            if def_name in tgt_arm.edit_bones:
                def_bone = tgt_arm.edit_bones[def_name]
            else:
                def_bone = tgt_arm.edit_bones.new(name=def_name)

            def_bone.head = src_bone.head_local
            def_bone.tail = src_bone.tail_local
            def_bone.matrix = src_bone.matrix_local

            def_bone.use_deform = False
            def_bone.use_connect = False

            deform_col.assign(def_bone)
            def_bones.append(src_name)

        for src_bone in def_arm.bones:
            src_name = src_bone.name
            def_name = f"{pref.deform_prefix}{src_name}"

            if def_name not in tgt_arm.edit_bones:
                continue

            def_bone = tgt_arm.edit_bones[def_name]

            if src_bone.parent:
                parent_name = src_bone.parent.name
                def_parent_name = f"{pref.deform_prefix}{parent_name}"

                if def_parent_name in tgt_arm.edit_bones:
                    def_bone.parent = tgt_arm.edit_bones[def_parent_name]

        bpy.ops.object.mode_set(mode='POSE')

        for tgt_name in def_bones:
            def_name = f"{pref.deform_prefix}{tgt_name}"

            if tgt_name not in tgt_obj.pose.bones:
                continue
            if def_name not in tgt_obj.pose.bones:
                continue

            def_pb = tgt_obj.pose.bones[def_name]

            if def_pb:
                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", 'LIMIT_LOCATION')
                con.max_x = con.max_y = con.max_z = con.min_x = con.min_y = con.min_z = 0
                con.use_max_x = con.use_max_y = con.use_max_z = con.use_min_x = con.use_min_y = con.use_min_z = True
                con.owner_space = 'LOCAL_WITH_PARENT'
                con.influence = 1.0

                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", 'LIMIT_ROTATION')
                con.max_x = con.max_y = con.max_z = con.min_x = con.min_y = con.min_z = 0
                con.use_limit_x = con.use_limit_y = con.use_limit_z = True
                con.owner_space = 'LOCAL_WITH_PARENT'
                con.influence = 1.0

                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", 'LIMIT_SCALE')
                con.max_x = con.max_y = con.max_z = con.min_x = con.min_y = con.min_z = 1
                con.use_max_x = con.use_max_y = con.use_max_z = con.use_min_x = con.use_min_y = con.use_min_z = True
                con.owner_space = 'LOCAL_WITH_PARENT'
                con.influence = 1.0

                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", "CHILD_OF")
                con.target = tgt_obj
                con.subtarget = tgt_name

        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Deform Bones generated and connected.")
        return {'FINISHED'}

class WRYC_OT_CreateDeformBones(bpy.types.Operator):
    bl_idname = "wryc.ot_create_deform_bones"
    bl_label = "Generate Deform"
    bl_description = "Generate virtual deform bones form active armature"
    bl_options = {'REGISTER', 'UNDO'}

    is_switch_direction: bpy.props.BoolProperty(name="Switch Bones Direction",default=True)
    switch_direction: bpy.props.EnumProperty(
        name="Switch Direction",
        items=[
            ('X', "X", "X"),
            ('-X', "-X", "-X"),
            ('Z', "Z", "Z"),
            ('-Z', "-Z", "-Z"),
        ],
        default='Z'
    )
    switch_angle: bpy.props.FloatProperty(name="Switch Angle",default=90)
    def_coll_name: bpy.props.StringProperty(name="Collection Name",default="Deform Bones")

    def invoke(self, context, event):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if obj and obj.type == 'ARMATURE':
            layout.prop(self, "is_switch_direction", text="Switch Bones Direction")
            if self.is_switch_direction:
                col = layout.column(align=True)
                split = col.split(factor=0.5)
                split.label(text="Switch Direction:")
                split.prop(self, "switch_direction", text="")
                layout.prop(self, "switch_angle", text="Switch Angle")
            col = layout.column(align=True)
            split = col.split(factor=0.5)
            split.label(text="Deform Collection Name:")
            split.prop(self, "def_coll_name", text="")
        else:
            layout.label(text="Select an Armature", icon="ERROR")

    def execute(self, context):
        pref = AddonFunctions.get_preferences()
        obj = context.object
        arm = obj.data

        selected_bones = AddonFunctions.get_selected_bones(context, self)
        if not selected_bones:
            return {'CANCELLED'}

        selected_names = {pb.name for pb in selected_bones}

        if self.def_coll_name not in arm.collections:
            def_collection = arm.collections.new(self.def_coll_name)
        else:
            def_collection = arm.collections[self.def_coll_name]

        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = arm.edit_bones

        bone_map = {}

        for orig_bone in arm.bones:
            if orig_bone.name not in selected_names:
                continue

            if not orig_bone.use_deform:
                continue

            eb = edit_bones.get(orig_bone.name)
            if not eb:
                self.report({'ERROR'}, f"Can not find bone for {orig_bone.name}")
                continue

            def_name = pref.deform_prefix + orig_bone.name
            new_bone = edit_bones.new(def_name)

            new_bone.head = eb.head.copy()
            new_bone.tail = eb.tail.copy()
            new_bone.roll = eb.roll

            if self.is_switch_direction:
                if self.switch_direction == 'X':
                    axis_local = mathutils.Vector((1, 0, 0))
                elif self.switch_direction == '-X':
                    axis_local = mathutils.Vector((-1, 0, 0))
                elif self.switch_direction == 'Z':
                    axis_local = mathutils.Vector((0, 0, 1))
                elif self.switch_direction == '-Z':
                    axis_local = mathutils.Vector((0, 0, -1))

                axis_world = new_bone.matrix.to_3x3() @ axis_local
                axis_world.normalize()

                vec = new_bone.tail - new_bone.head

                angle_radians = math.radians(self.switch_angle)
                rotate = mathutils.Matrix.Rotation(angle_radians, 4, axis_world)

                new_bone.tail = new_bone.head + rotate @ vec

            new_bone.use_deform = False
            new_bone.use_connect = False

            def_collection.assign(new_bone)

            bone_map[orig_bone.name] = def_name

        for orig_name, def_name in bone_map.items():
            orig_bone = arm.bones[orig_name]
            def_bone = edit_bones[def_name]

            if orig_bone.parent and orig_bone.parent.name in bone_map:
                def_bone.parent = edit_bones[bone_map[orig_bone.parent.name]]
            else:
                def_bone.parent = None

        bpy.ops.object.mode_set(mode='POSE')

        for orig_name, def_name in bone_map.items():
            def_pb = obj.pose.bones.get(def_name)

            if def_pb:
                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", 'LIMIT_LOCATION')
                con.max_x = con.max_y = con.max_z = con.min_x = con.min_y = con.min_z = 0
                con.use_max_x = con.use_max_y = con.use_max_z = con.use_min_x = con.use_min_y = con.use_min_z = True
                con.owner_space = 'LOCAL_WITH_PARENT'
                con.influence = 1.0

                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", 'LIMIT_ROTATION')
                con.max_x = con.max_y = con.max_z = con.min_x = con.min_y = con.min_z = 0
                con.use_limit_x = con.use_limit_y = con.use_limit_z = True
                con.owner_space = 'LOCAL_WITH_PARENT'
                con.influence = 1.0

                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", 'LIMIT_SCALE')
                con.max_x = con.max_y = con.max_z = con.min_x = con.min_y = con.min_z = 1
                con.use_max_x = con.use_max_y = con.use_max_z = con.use_min_x = con.use_min_y = con.use_min_z = True
                con.owner_space = 'LOCAL_WITH_PARENT'
                con.influence = 1.0

                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", 'CHILD_OF')
                con.target = obj
                con.subtarget = orig_name
                obj.data.bones.active = obj.data.bones[def_name]
                bpy.ops.constraint.childof_set_inverse(constraint=con.name, owner='BONE')

        self.report({'INFO'}, f"Generated deform bones.")
        return {'FINISHED'}

class WRYC_OT_CreateMannyDeformBones(bpy.types.Operator):
    bl_idname = "wryc.ot_create_manny_deform_bones"
    bl_label = "UE5 Manny Deform"
    bl_options = {'REGISTER', 'UNDO'}

    def_coll_name: bpy.props.StringProperty(default="Deform Bones", name="Deform Collection Name")
    def_body_coll_name:bpy.props.StringProperty(default="Deform(Body)", name="Deform Body Collection Name")

    def execute(self, context):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}
        prefix = AddonFunctions.get_preferences().prefix.deform_prefix
        obj = context.active_object
        arm = obj.data

        def_coll = AddonFunctions.get_or_create_collection(arm, self.def_coll_name)
        def_body_coll = AddonFunctions.get_or_create_collection(arm, self.def_body_coll_name)

        def_body_coll.parent = def_coll

        spine_mapping = {'X': '-Z', 'Y': 'X', 'Z': '-Y'}
        left_hand_right_leg_mapping = {'X': '-Y', 'Y': 'X', 'Z': 'Z'}
        left_hand_wrist_mapping = {'X': 'Z', 'Y': 'X', 'Z': 'Y'}
        right_hand_left_leg_mapping = {'X': '-Y', 'Y': '-X', 'Z': '-Z'}
        right_hand_wrist_mapping = {'X': 'Z', 'Y': '-X', 'Z': '-Y'}
        left_toe_mapping = {'X': 'Y', 'Y': 'X', 'Z': '-Z'}
        right_toe_mapping = {'X': 'Y', 'Y': '-X', 'Z': 'Z'}

        bone_configs = [
            # Spine
            ("root", "root", spine_mapping, 'head'),
            ("pelvis", "pelvis", spine_mapping, 'head'),
            ("spine_01", "spine_01", spine_mapping, 'head'),
            ("spine_02", "spine_02", spine_mapping, 'head'),
            ("spine_03", "spine_03", spine_mapping, 'head'),
            ("spine_04", "spine_04", spine_mapping, 'head'),
            ("spine_05", "spine_05", spine_mapping, 'head'),
            ("neck_01", "neck_01", spine_mapping, 'head'),
            ("neck_02", "neck_02", spine_mapping, 'head'),
            ("head", "head", spine_mapping, 'head'),
            # Left Arm
            ("clavicle_l", "clavicle_l", left_hand_right_leg_mapping, 'head'),
            ("upperarm_l", "upperarm_l", left_hand_right_leg_mapping, 'head'),
            ("lowerarm_l", "lowerarm_l", left_hand_right_leg_mapping, 'head'),
            ("upperarm_twist_01_l", "upperarm_twist_01_l", left_hand_right_leg_mapping, 'tail'),
            ("upperarm_twist_02_l", "upperarm_twist_02_l", left_hand_right_leg_mapping, 'tail'),
            ("lowerarm_twist_01_l", "lowerarm_twist_01_l", left_hand_wrist_mapping, 'tail'),
            ("lowerarm_twist_02_l", "lowerarm_twist_02_l", left_hand_wrist_mapping, 'tail'),
            # Left Hand
            ("hand_l", "hand_l", left_hand_right_leg_mapping, 'head'),
            ("thumb_01_l", "thumb_01_l", left_hand_right_leg_mapping, 'head'),
            ("thumb_02_l", "thumb_02_l", left_hand_right_leg_mapping, 'head'),
            ("thumb_03_l", "thumb_03_l", left_hand_right_leg_mapping, 'head'),
            ("index_metacarpal_l", "index_metacarpal_l", left_hand_right_leg_mapping, 'head'),
            ("index_01_l", "index_01_l", left_hand_right_leg_mapping, 'head'),
            ("index_02_l", "index_02_l", left_hand_right_leg_mapping, 'head'),
            ("index_03_l", "index_03_l", left_hand_right_leg_mapping, 'head'),
            ("middle_metacarpal_l", "middle_metacarpal_l", left_hand_right_leg_mapping, 'head'),
            ("middle_01_l", "middle_01_l", left_hand_right_leg_mapping, 'head'),
            ("middle_02_l", "middle_02_l", left_hand_right_leg_mapping, 'head'),
            ("middle_03_l", "middle_03_l", left_hand_right_leg_mapping, 'head'),
            ("ring_metacarpal_l", "ring_metacarpal_l", left_hand_right_leg_mapping, 'head'),
            ("ring_01_l", "ring_01_l", left_hand_right_leg_mapping, 'head'),
            ("ring_02_l", "ring_01_l", left_hand_right_leg_mapping, 'head'),
            ("ring_03_l", "ring_03_l", left_hand_right_leg_mapping, 'head'),
            ("pinky_metacarpal_l", "pinky_metacarpal_l", left_hand_right_leg_mapping, 'head'),
            ("pinky_01_l", "pinky_01_l", left_hand_right_leg_mapping, 'head'),
            ("pinky_02_l", "pinky_02_l", left_hand_right_leg_mapping, 'head'),
            ("pinky_03_l", "pinky_03_l", left_hand_right_leg_mapping, 'head'),
            # Right Arm
            ("clavicle_r", "clavicle_r", right_hand_left_leg_mapping, 'head'),
            ("upperarm_r", "upperarm_r", right_hand_left_leg_mapping, 'head'),
            ("lowerarm_r", "lowerarm_r", right_hand_left_leg_mapping, 'head'),
            ("upperarm_twist_01_r", "upperarm_twist_01_r", right_hand_left_leg_mapping, 'tail'),
            ("upperarm_twist_02_r", "upperarm_twist_02_r", right_hand_left_leg_mapping, 'tail'),
            ("lowerarm_twist_01_r", "lowerarm_twist_01_r", right_hand_wrist_mapping, 'tail'),
            ("lowerarm_twist_02_r", "lowerarm_twist_02_r", right_hand_wrist_mapping, 'tail'),
            # Right Hand
            ("hand_r", "hand_r", right_hand_left_leg_mapping, 'head'),
            ("thumb_01_r", "thumb_01_r", right_hand_left_leg_mapping, 'head'),
            ("thumb_02_r", "thumb_02_r", right_hand_left_leg_mapping, 'head'),
            ("thumb_03_r", "thumb_03_r", right_hand_left_leg_mapping, 'head'),
            ("index_metacarpal_r", "index_metacarpal_r", right_hand_left_leg_mapping, 'head'),
            ("index_01_r", "index_01_r", right_hand_left_leg_mapping, 'head'),
            ("index_02_r", "index_02_r", right_hand_left_leg_mapping, 'head'),
            ("index_03_r", "index_03_r", right_hand_left_leg_mapping, 'head'),
            ("middle_metacarpal_r", "middle_metacarpal_r", right_hand_left_leg_mapping, 'head'),
            ("middle_01_r", "middle_01_r", right_hand_left_leg_mapping, 'head'),
            ("middle_02_r", "middle_02_r", right_hand_left_leg_mapping, 'head'),
            ("middle_03_r", "middle_03_r", right_hand_left_leg_mapping, 'head'),
            ("ring_metacarpal_r", "ring_metacarpal_r", right_hand_left_leg_mapping, 'head'),
            ("ring_01_r", "ring_01_r", right_hand_left_leg_mapping, 'head'),
            ("ring_02_r", "ring_02_r", right_hand_left_leg_mapping, 'head'),
            ("ring_03_r", "ring_03_r", right_hand_left_leg_mapping, 'head'),
            ("pinky_metacarpal_r", "pinky_metacarpal_r", right_hand_left_leg_mapping, 'head'),
            ("pinky_01_r", "pinky_01_r", right_hand_left_leg_mapping, 'head'),
            ("pinky_02_r", "pinky_02_r", right_hand_left_leg_mapping, 'head'),
            ("pinky_03_r", "pinky_03_r", right_hand_left_leg_mapping, 'head'),
            # Left Leg
            ("thigh_l", "thigh_l", right_hand_left_leg_mapping, 'head'),
            ("calf_l", "calf_l", right_hand_left_leg_mapping, 'head'),
            ("thigh_twist_01_l", "thigh_twist_01_l", right_hand_left_leg_mapping, 'tail'),
            ("thigh_twist_02_l", "thigh_twist_02_l", right_hand_left_leg_mapping, 'tail'),
            ("calf_twist_01_l", "calf_twist_01_l", right_hand_left_leg_mapping, 'tail'),
            ("calf_twist_02_l", "calf_twist_02_l", right_hand_left_leg_mapping, 'tail'),
            # Left Foot
            ("foot_l", "calf_l", right_hand_left_leg_mapping, 'tail'),
            ("ball_l", "ball_l", left_toe_mapping, 'head'),
            # Right Leg
            ("thigh_r", "thigh_r", left_hand_right_leg_mapping, 'head'),
            ("calf_r", "calf_r", left_hand_right_leg_mapping, 'head'),
            ("thigh_twist_01_r", "thigh_twist_01_r", left_hand_right_leg_mapping, 'tail'),
            ("thigh_twist_02_r", "thigh_twist_02_r", left_hand_right_leg_mapping, 'tail'),
            ("calf_twist_01_r", "calf_twist_01_r", left_hand_right_leg_mapping, 'tail'),
            ("calf_twist_02_r", "calf_twist_02_r", left_hand_right_leg_mapping, 'tail'),
            # Right Foot
            ("foot_r", "calf_r", left_hand_right_leg_mapping, 'tail'),
            ("ball_r", "ball_r", right_toe_mapping, 'head'),
        ]

        bone_map = {}

        try:
            bpy.ops.object.mode_set(mode='EDIT')
            mirror_mode = arm.use_mirror_x
            arm.use_mirror_x = False

            for target_name, matrix_name, mapping, relation in bone_configs:
                    if target_name not in obj.pose.bones or matrix_name not in obj.pose.bones:
                        continue

                    target_pb = obj.pose.bones[target_name]
                    matrix_pb = obj.pose.bones[matrix_name]
                    def_name = f"{prefix}{target_name}"
                    parent_name = f"{prefix}{target_pb.parent.name}" if target_pb.parent else ""

                    new_bone = AddonFunctions.create_deform_bone(obj, target_pb, matrix_pb, def_name, mapping, relation, parent_name)
                    nb = arm.edit_bones.get(new_bone)
                    def_body_coll.assign(nb)
                    bone_map[target_name] = new_bone

        finally:
            arm.use_mirror_x = mirror_mode

        bpy.ops.object.mode_set(mode='POSE')

        for orig_name, def_name in bone_map.items():
            def_pb = obj.pose.bones.get(def_name)

            if def_pb:
                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", 'LIMIT_LOCATION')
                con.max_x = con.max_y = con.max_z = con.min_x = con.min_y = con.min_z = 0
                con.use_max_x = con.use_max_y = con.use_max_z = con.use_min_x = con.use_min_y = con.use_min_z = True
                con.owner_space = 'LOCAL_WITH_PARENT'
                con.influence = 1.0

                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", 'LIMIT_ROTATION')
                con.max_x = con.max_y = con.max_z = con.min_x = con.min_y = con.min_z = 0
                con.use_limit_x = con.use_limit_y = con.use_limit_z = True
                con.owner_space = 'LOCAL_WITH_PARENT'
                con.influence = 1.0

                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", 'LIMIT_SCALE')
                con.max_x = con.max_y = con.max_z = con.min_x = con.min_y = con.min_z = 1
                con.use_max_x = con.use_max_y = con.use_max_z = con.use_min_x = con.use_min_y = con.use_min_z = True
                con.owner_space = 'LOCAL_WITH_PARENT'
                con.influence = 1.0

                con = AddonFunctions.get_or_create_constraint(def_pb, "DEFORM - ", 'CHILD_OF')
                con.target = obj
                con.subtarget = orig_name
                con.use_location_x = con.use_location_y = con.use_location_z = True
                con.use_rotation_x = con.use_rotation_y = con.use_rotation_z = True
                con.use_scale_x = con.use_scale_y = con.use_scale_z = True
                con.influence = 1.0

                obj.data.bones.active = obj.data.bones[def_name]
                bpy.ops.constraint.childof_set_inverse(constraint=con.name, owner='BONE')

        self.report({'INFO'}, "Generated UE5 Manny deform bones.")
        return {'FINISHED'}

class WRYC_OT_SetInverseAllChildOf(bpy.types.Operator):
    bl_idname = "wryc.ot_set_inverse_all_child_of"
    bl_label = "Set Inverse All"
    bl_description = "Set Inverse to all child of constraint in selected bones"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}

        selected_bones = AddonFunctions.get_selected_bones(context, self)
        if not selected_bones:
            return {'CANCELLED'}

        obj = bpy.context.object

        bpy.ops.pose.select_all(action='DESELECT')

        for pb in selected_bones:
            cons = [c for c in pb.constraints if c.type == 'CHILD_OF' and c.target]
            if not cons:
                continue

            for con in cons:
                AddonFunctions.apply_child_of_inverse(context, obj, pb, con)

        self.report({'INFO'}, "Pose mode is ON, Set Inverse All")
        return {'FINISHED'}

class WRYC_OT_RemoveConstrains(bpy.types.Operator):
    bl_idname = "wryc.ot_remove_constrains"
    bl_label = "Remove Constraints"
    bl_description = "Remove seleted bones constraints"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}

        selected_bones = AddonFunctions.get_selected_bones(context, self)
        if not selected_bones:
            return {'CANCELLED'}

        for pb in selected_bones:
            for con in list(pb.constraints):
                pb.constraints.remove(con)

        self.report({'INFO'}, "Pose mode is ON, Remove Selected Bones Constraints")
        return {'FINISHED'}

class WRYC_OT_CreateSpineController(bpy.types.Operator):
    bl_idname = "wryc.ot_create_spine_controller"
    bl_label = "Spine"
    bl_description = "Generate Spine Controller"
    bl_options = {'REGISTER', 'UNDO'}

    head: bpy.props.StringProperty(name="Head Bone")
    chest: bpy.props.StringProperty(name="Chest Bone")
    pelvis: bpy.props.StringProperty(name="Pelvis Bone")

    def invoke(self, context, event):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj and obj.type == 'ARMATURE':
            layout.label(text="Basic Bone")
            layout.prop_search(self, "head", obj.data, "bones", text="Head")
            layout.prop_search(self, "chest", obj.data, "bones", text="Chest")
            layout.prop_search(self, "pelvis", obj.data, "bones", text="Pelvis")
        else:
            layout.label(text="Select an Armature", icon="ERROR")

    def execute(self, context):
        obj = context.object
        pref = AddonFunctions.get_preferences()

        if not self.head or not self.chest or not self.pelvis:
            self.report({'ERROR'}, f"Please select bones")
            return {'CANCELLED'}

        head_pb = obj.pose.bones.get(self.head)
        chest_pb = obj.pose.bones.get(self.chest)
        pelvis_pb = obj.pose.bones.get(self.pelvis)

        if not head_pb or not chest_pb or not pelvis_pb:
            self.report({'ERROR'}, f"Bone not found")
            return {'CANCELLED'}

        neck_pb = chest_pb.children[0]

        #Collect chain: pelvis -> chain
        pre_neck_chain = []
        pb = neck_pb
        while pb:
            pre_neck_chain.append(pb)
            if pb.name == pelvis_pb.name:
                break
            pb = pb.parent
        pre_neck_chain.reverse()

        spline_chain_count = len(pre_neck_chain)

        full_chain = []
        pb = head_pb
        while pb:
            full_chain.append(pb)
            if pb.name == self.pelvis:
                break
            pb = pb.parent
        full_chain.reverse()

        full_chain_names = [b.name for b in full_chain]

        # Generate Pelvis Control Bone
        control_pelvis = AddonFunctions.ensure_target(
            obj,
            self.pelvis,
            f"{pref.prefix.control_prefix}{self.pelvis}",
            "pelvis_control_shape",
            "",
            False,
            mode="DEFAULT"
        )

        #Generate Target Bones
        unit = chest_pb.length / 0.12
        offset = obj.matrix_world.inverted().to_3x3() @ (mathutils.Vector((0, unit * 0.3, 0)))

        target_pelvis = AddonFunctions.ensure_target(
            obj,
            self.pelvis,
            f"{pref.prefix.target_prefix}{self.pelvis}",
            "target_shape",
            parent_bone="",
            use_connect=False,
            position=offset,
            length=unit * 0.05,
            mode="CHAIN_TARGET"
        )
        target_chest = AddonFunctions.ensure_target(
            obj,
            self.chest,
            f"{pref.prefix.target_prefix}{self.chest}",
            "target_shape",
            parent_bone="",
            use_connect=False,
            position=offset,
            length=unit * 0.05,
            mode="CHAIN_TARGET"
        )
        target_head = AddonFunctions.ensure_target(
            obj,
            self.head,
            f"{pref.prefix.target_prefix}{self.head}",
            "target_shape",
            parent_bone="",
            use_connect=False,
            position=offset,
            length=unit * 0.05,
            mode="CHAIN_TARGET"
        )

        #Generate Gizmo Bones
        prev_gizmo_name = None
        for bone_name in full_chain_names:
            gizmo_name = f"{pref.prefix.gizmo_prefix}{bone_name}"
            AddonFunctions.ensure_target(
                obj,
                bone_name,
                gizmo_name,
                "gizmo_shape",
                parent_bone=prev_gizmo_name if prev_gizmo_name else "",
                use_connect=prev_gizmo_name is not None,
                position=offset,
                mode="CHAIN_GIZMO"
            )
            gizmo_bone = obj.pose.bones.get(gizmo_name)
            gizmo_bone.bone.inherit_scale = 'ALIGNED'
            prev_gizmo_name = gizmo_name

        #Generate Curve
        curve_name = f"{obj.name} Spine Curve"
        if curve_name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[curve_name], do_unlink=True)

        curve_data = bpy.data.curves.new(curve_name, type='CURVE')
        curve_data.dimensions = '3D'
        spline = curve_data.splines.new('NURBS')
        spline.points.add(2)
        spline.use_endpoint_u = True

        for i, (pt, pos) in enumerate(zip(spline.points, [target_pelvis.head, target_chest.head, target_head.head])):
            pt.co = (*pos, 1.0)
            pt.weight = 1.0

        curve_obj = bpy.data.objects.new(curve_name, curve_data)
        if obj.users_collection:
            target_collection = obj.users_collection[0]
        else:
            target_collection = context.scene.collection
        target_collection.objects.link(curve_obj)
        curve_obj.parent = obj
        context.view_layer.update()

        hook_targets = [
            (target_pelvis.name, 0),
            (target_chest.name, 1),
            (target_head.name, 2),
        ]

        bpy.context.view_layer.objects.active = curve_obj
        curve_obj.select_set(True)

        for bone_name, index in hook_targets:
            mod = curve_obj.modifiers.new(name=f"{bone_name} - Hook", type='HOOK')
            mod.object = obj
            mod.subtarget = bone_name
            mod.vertex_indices_set([index])

        curve_obj.parent = obj

        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.mode_set(mode='POSE')

        #Constraints
        con = AddonFunctions.get_or_create_constraint(control_pelvis, "TARGET - ", 'COPY_LOCATION')
        con.target = obj
        con.subtarget = target_pelvis.name
        con.use_x = con.use_y = con.use_z = True
        con.use_offset = True
        con.target_space = 'LOCAL'
        con.owner_space = 'LOCAL'
        con.influence = 1

        con = AddonFunctions.get_or_create_constraint(control_pelvis, "GIZMO - ", 'COPY_ROTATION')
        con.target = obj
        con.subtarget = f"{pref.prefix.gizmo_prefix}{pelvis_pb.name}"
        con.use_x = con.use_y = con.use_z = True
        con.target_space = 'LOCAL'
        con.owner_space = 'LOCAL'
        con.mix_mode = 'BEFORE'
        con.influence = 1

        con = AddonFunctions.get_or_create_constraint(pelvis_pb, "CONTROL - ", 'COPY_LOCATION')
        con.target = obj
        con.subtarget = control_pelvis.name
        con.use_x = con.use_y = con.use_z = True
        con.use_offset = False
        con.target_space = 'LOCAL'
        con.owner_space = 'LOCAL'
        con.influence = 1

        con = AddonFunctions.get_or_create_constraint(pelvis_pb, "CONTROL - ", 'COPY_ROTATION')
        con.target = obj
        con.subtarget = control_pelvis.name
        con.use_x = con.use_y = con.use_z = True
        con.target_space = 'LOCAL'
        con.owner_space = 'LOCAL'
        con.mix_mode = 'REPLACE'
        con.influence = 1

        for pb in full_chain[1:]:
            con = AddonFunctions.get_or_create_constraint(pb, "GIZMO - ", 'COPY_ROTATION')
            con.target = obj
            con.subtarget = f"{pref.prefix.gizmo_prefix}{pb.name}"
            con.use_x = con.use_y = con.use_z = True
            con.target_space = 'LOCAL'
            con.owner_space = 'LOCAL'
            con.mix_mode = 'BEFORE'
            con.influence = 0.5

        gizmo_neck = obj.pose.bones.get(f"{pref.prefix.gizmo_prefix}{neck_pb.name}")
        con = AddonFunctions.get_or_create_constraint(gizmo_neck, "", 'SPLINE_IK')
        con.target = curve_obj
        con.chain_count = spline_chain_count
        con.use_curve_radius = True
        con.y_scale_mode = 'FIT_CURVE'

        self.report({'INFO'}, f"Generated Controller for SPINE")
        return {'FINISHED'}

class WRYC_OT_CreateHeadController(bpy.types.Operator):
    bl_idname = "wryc.ot_create_head_controller"
    bl_label = "Head"
    bl_description = "Generate Head Controller"
    bl_options = {'REGISTER', 'UNDO'}

    head: bpy.props.StringProperty(name="Head Bone")
    chest: bpy.props.StringProperty(name="Chest Bone")

    def invoke(self, context, event):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj and obj.type == 'ARMATURE':
            layout.label(text="Basic Bone")
            layout.prop_search(self, "head", obj.data, "bones", text="Head")
            layout.prop_search(self, "chest", obj.data, "bones", text="Chest")
        else:
            layout.label(text="Select an Armature", icon="ERROR")
            
    def execute(self, context):
        obj = context.object
        pref = AddonFunctions.get_preferences()

        if not self.head or not self.chest:
            self.report({'ERROR'}, f"Please Select Bones")
            return {'CANCELLED'}

        head_pb = obj.pose.bones.get(self.head)
        chest_pb = obj.pose.bones.get(self.chest)

        if not head_pb or not chest_pb:
            self.report({'ERROR'}, f"Bone not found")
            return {'CANCELLED'}

        chain = []
        pb = head_pb
        while pb:
            chain.append(pb)
            if pb.name == chest_pb.name:
                break
            pb = pb.parent
        chain.reverse()

        chain_length = len(chain)
        chain_names = [b.name for b in chain]

        gt_prefix = f"{pref.prefix.gizmo_prefix}{pref.prefix.track_prefix}"
        mt_prefix = f"{pref.prefix.mechanic_prefix}{pref.prefix.track_prefix}"

        unit = chest_pb.child.length/0.05

        offset_head = AddonFunctions.ensure_target(
            obj,
            head_pb,
            f"{pref.prefix.offset_prefix}{pref.prefix.track_prefix}{head_pb.name}",
            'offset_head_shape',
            chest_pb.child.name,
            False,
            length=unit * 0.3,
            mode='HEAD_TRACK',
        )

        for i, bone_name in enumerate(chain_names):
            gt_name = f"{gt_prefix}{bone_name}"
            gt_pb = AddonFunctions.ensure_target(
                obj,
                bone_name,
                gt_name,
                'gizmo_shape',
                chain_names[i - 1] if i > 0 else f"{chest_pb.parent.name}",
                False,
                mode='DEFAULT'
            )
            if gt_pb:
                gt_pb.bone.inherit_scale = 'ALIGNED'

        prev_mt_name = chain_names[0]
        for bone_name in chain_names:
            mt_name = f"{mt_prefix}{bone_name}"
            AddonFunctions.ensure_target(
                obj,
                bone_name,
                mt_name,
                'mechanic_shape',
                parent_bone=offset_head.name if bone_name == head_pb.name else chest_pb.parent.name if bone_name == chest_pb.name else prev_mt_name,
                use_connect=False,
                mode='DEFAULT'
            )
            prev_mt_name = mt_name

        control_head = AddonFunctions.ensure_target(
            obj,
            head_pb,
            f"{pref.prefix.control_prefix}{pref.prefix.track_prefix}{head_pb.name}",
            'head_control_shape',
            f"{pref.prefix.mechanic_prefix}{pref.prefix.track_prefix}{head_pb.parent.name}",
            False,
            length=unit * 0.3,
            mode='HEAD_TRACK',
        )
        target_head = AddonFunctions.ensure_target(
            obj,
            head_pb,
            f"{pref.prefix.target_prefix}{pref.prefix.track_prefix}{head_pb.name}",
            'target_shape',
            "",
            length=unit * 0.1,
            mode='HEAD_TARGET',
            ref_name=control_head.name
        )

        bpy.ops.object.mode_set(mode='POSE')

        #Constraints
        con = AddonFunctions.get_or_create_constraint(offset_head, 'TRACK - ', 'IK')
        con.target = obj
        con.subtarget = target_head.name
        con.chain_count = 1
        con.use_tail = True
        con.use_stretch = False
        con.use_location = True
        con.use_rotation = False
        con.weight = 1.0
        con.influence = 1.0

        con = AddonFunctions.get_or_create_constraint(offset_head, 'TRACK - ', 'COPY_ROTATION')
        con.target = obj
        con.subtarget = control_head.name
        con.use_x = con.use_y = con.use_z = True
        con.target_space = 'LOCAL'
        con.owner_space = 'LOCAL'
        con.mix_mode = 'AFTER'
        con.influence = 1.0

        con = AddonFunctions.get_or_create_constraint(control_head, 'TRACK - ', 'IK')
        con.target = obj
        con.subtarget = target_head.name
        con.chain_count = chain_length + 1
        con.use_tail = True
        con.use_stretch = True
        con.use_location = True
        con.use_rotation = False
        con.weight = 1.0
        con.influence = 1.0

        con = AddonFunctions.get_or_create_constraint(control_head, 'LOCK X - ', 'LOCKED_TRACK')
        con.target = obj
        con.subtarget = target_head.name
        con.track_axis = 'TRACK_Y'
        con.lock_axis = 'LOCK_X'
        con.influence = 0.5

        con = AddonFunctions.get_or_create_constraint(control_head, 'LOCK Z - ', 'LOCKED_TRACK')
        con.target = obj
        con.subtarget = target_head.name
        con.track_axis = 'TRACK_Y'
        con.lock_axis = 'LOCK_Z'
        con.influence = 0.5


        gt_bones = [obj.pose.bones.get(f"{gt_prefix}{bone_name}") for bone_name in chain_names]
        mt_bones = [obj.pose.bones.get(f"{mt_prefix}{bone_name}") for bone_name in chain_names]

        for i in range(chain_length):
            bone = chain[i]
            gt_bone = gt_bones[i]
            mt_bone = mt_bones[i]

            is_head = (i == chain_length - 1)

            con = AddonFunctions.get_or_create_constraint(gt_bone, 'TRACK - ', 'IK')
            con.target = obj
            if is_head:
                con.subtarget = mt_bone.name
                con.use_location = False
                con.use_rotation = True
            else:
                next_mt_bone = mt_bones[i + 1]
                con.subtarget = control_head.name if i == (chain_length - 2) else next_mt_bone.name
                con.use_location = True
                con.use_rotation = False

            con.chain_count = 1
            con.use_tail = True
            con.use_stretch = False
            con.weight = 1.0
            con.orient_weight = 1.0
            con.influence = 1.0

            con = AddonFunctions.get_or_create_constraint(gt_bone, 'TRACK - ', 'COPY_ROTATION')
            con.target = obj
            con.subtarget = mt_bone.name
            con.use_x = con.use_z = False
            con.use_y = True
            con.target_space = 'LOCAL'
            con.owner_space = 'LOCAL'
            con.mix_mode = 'AFTER'
            con.influence = 1.0

            con = AddonFunctions.get_or_create_constraint(bone, 'TRACK - ', 'COPY_ROTATION')
            con.target = obj
            con.subtarget = gt_bone.name
            con.use_x = con.use_y = con.use_z = True
            con.target_space = 'LOCAL'
            con.owner_space = 'LOCAL'
            con.mix_mode = 'AFTER'
            if is_head:
                con.influence = 1.0
            else:
                con.influence = 0.5

        self.report({'INFO'}, f"Generated Controller for Head")
        return {'FINISHED'}

class WRYC_OT_CreateArmController(bpy.types.Operator):
    bl_idname = "wryc.ot_create_arm_controller"
    bl_label = "Arm"
    bl_description = "Generate Arm Controller"
    bl_options = {'REGISTER', 'UNDO'}

    hand: bpy.props.StringProperty(name="Hand Bone")
    arm_length: bpy.props.IntProperty(name="Arm Length", default=2, min=2)

    def invoke(self, context, event):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj and obj.type == 'ARMATURE':
            layout.label(text="Basic Bone")
            layout.prop_search(self, "hand", obj.data, "bones", text="Hand")
            layout.prop(self, "arm_length")
        else:
            layout.label(text="Select an Armature", icon="ERROR")

    def execute(self, context):
        obj = context.object
        pref = AddonFunctions.get_preferences()

        if not self.hand:
            self.report({'ERROR'}, f"Please select the hand bone")
            return {'CANCELLED'}

        chain = []
        pb = obj.pose.bones.get(self.hand)
        if not pb:
            self.report({'ERROR'}, f"Hand Bone {self.hand} not found")
            return {'CANCELLED'}

        chain.append(pb)
        while pb.parent and len(chain) <self.arm_length + 1:
            pb = pb.parent
            chain.append(pb)

        if len(chain) < self.arm_length + 1:
            self.report({'ERROR'}, f"Arm Length {self.arm_length} is too short")
            return {'CANCELLED'}

        hand_pb = chain[0]
        lower_pb = chain[1]
        upper_pb = chain[-1]

        hand_name = hand_pb.name
        lower_name = lower_pb.name
        upper_name = upper_pb.name

        unit = upper_pb.length/0.28

        bpy.ops.object.mode_set(mode='EDIT')

        target_wrist = AddonFunctions.ensure_target(
            obj,
            hand_name,
            f"{pref.prefix.target_prefix}{hand_name}",
            "hand_target_shape",
            "",
            False,
        )
        pole_pos = AddonFunctions.compute_pole_position(
            obj,
            upper_name,
            lower_name,
            hand_name,
        )
        target_elbow = AddonFunctions.ensure_target(
            obj,
            upper_name,
            f"{pref.prefix.target_prefix}{upper_name}",
            "target_shape",
            parent_bone="",
            position=pole_pos,
            length=unit * 0.1,
            mode="POLE_TARGET",
        )

        bpy.ops.object.mode_set(mode='POSE')

        pole_angle = AddonFunctions.compute_pole_angle(
            obj,
            upper_name,
            hand_name,
            pole_pos,
        )

        con = AddonFunctions.get_or_create_constraint(lower_pb, "ARM - ", 'IK')
        con.target = obj
        con.subtarget = target_wrist.name
        con.pole_target = obj
        con.pole_subtarget = target_elbow.name
        con.pole_angle = pole_angle
        con.chain_count = self.arm_length
        con.use_tail = True
        con.use_stretch = False
        con.weight = 1.0
        con.influence = 1.0

        con = AddonFunctions.get_or_create_constraint(hand_pb, "TARGET - ", 'COPY_ROTATION')
        con.target = obj
        con.subtarget = target_wrist.name
        con.use_x = con.use_y = con.use_z = True
        con.target_space = 'WORLD'
        con.owner_space = 'WORLD'
        con.mix_mode = 'REPLACE'
        con.influence = 1.0

        self.report({'INFO'}, f"Generated Controller for Arm")
        return {'FINISHED'}

class WRYC_OT_CreateFingerController(bpy.types.Operator):
    bl_idname = "wryc.ot_create_finger_controller"
    bl_label = "Finger"
    bl_description = "Create finger controller"
    bl_options = {'REGISTER', 'UNDO'}

    root_bone: bpy.props.StringProperty(name="Root Bone")

    def invoke(self, context, event):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if obj and obj.type == 'ARMATURE':
            layout.label(text="Basic Bone")
            layout.prop_search(self, "root_bone", obj.data, "bones", text="Root Bone")

        else:
            layout.label(text="Select an Armature", icon="ERROR")

    def execute(self, context):
        pref = AddonFunctions.get_preferences()
        obj = context.object

        if not self.root_bone:
            self.report({'ERROR'}, "Please select the first bone in the finger chain")
            return {'CANCELLED'}

        root_name = self.root_bone
        parent_name = obj.pose.bones.get(root_name).parent.name

        target = AddonFunctions.ensure_target(
            obj,
            root_name,
            f"{pref.prefix.target_prefix}{root_name}",
            "finger_target_shape",
            parent_name,
            False,
        )

        bpy.ops.object.mode_set(mode='POSE')

        chain = AddonFunctions.collect_bone_chain(obj.pose.bones[root_name])

        for pb in chain:
            con = AddonFunctions.get_or_create_constraint(
                pb,
                "FINGER - ",
                "COPY_ROTATION"
            )
            con.target = obj
            con.subtarget = target.name
            con.target_space = 'LOCAL'
            con.owner_space = 'LOCAL'
            con.mix_mode = 'BEFORE'

        self.report({'INFO'}, f"Generate Constraint For Finger")
        return {'FINISHED'}

class WRYC_OT_CreateLegController(bpy.types.Operator):
    bl_idname = "wryc.ot_create_leg_controller"
    bl_label = "Leg"
    bl_description = "Generate Leg Controller"
    bl_options = {'REGISTER', 'UNDO'}

    is_create_toe: bpy.props.BoolProperty(name="Is Create Toe" ,default=True)

    foot: bpy.props.StringProperty(name="Foot Bone")
    toe: bpy.props.StringProperty(name="Toe Bone")
    leg_length: bpy.props.IntProperty(name="Leg Length", default=2, min=2)

    def invoke(self, context, event):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj and obj.type == 'ARMATURE':
            layout.prop(self, "is_create_toe")
            layout.label(text="Basic Bone")
            layout.prop_search(self, "foot", obj.data, "bones", text="Foot")
            if self.is_create_toe:
                layout.prop_search(self, "toe", obj.data, "bones", text="Toe")
            layout.prop(self, "leg_length")
        else:
            layout.label(text="Select an Armature", icon="ERROR")

    def execute(self, context):
        obj = context.object
        pref = AddonFunctions.get_preferences()

        if not self.foot:
            self.report({'ERROR'}, f"Please select the foot bone")
            return {'CANCELLED'}

        if self.is_create_toe:
            if not self.toe:
                self.report({'ERROR'}, f"Please select the toe bone")
                return {'CANCELLED'}

        chain = []
        pb = obj.pose.bones.get(self.foot)
        if not pb:
            self.report({'ERROR'}, f"Foot Bone {self.foot} not found")
            return {'CANCELLED'}

        chain.append(pb)
        while pb.parent and len(chain) < self.leg_length + 1:
            pb = pb.parent
            chain.append(pb)

        if len(chain) < self.leg_length + 1:
            self.report({'ERROR'}, f"Leg Length {self.leg_length} is too short")
            return {'CANCELLED'}

        foot_pb = chain[0]
        calf_pb = chain[1]
        thigh_pb = chain[-1]

        foot_name = foot_pb.name
        calf_name = calf_pb.name
        thigh_name = thigh_pb.name

        unit = thigh_pb.length/0.4

        if self.is_create_toe:
            toe_name = self.toe
            toe = obj.pose.bones.get(toe_name)

        root_name = ""
        for b in obj.pose.bones:
            if "root" in b.name:
                root_name = b.name
                break

        pole_pos = AddonFunctions.compute_pole_position(
            obj,
            thigh_name,
            calf_name,
            foot_name,
        )
        target_knee = AddonFunctions.ensure_target(
            obj,
            thigh_name,
            f"{pref.prefix.target_prefix}{thigh_name}",
            "target_shape",
            parent_bone="",
            position=pole_pos,
            mode="POLE_TARGET",
        )
        offset_ankle = AddonFunctions.ensure_target(
            obj,
            calf_name,
            f"{pref.prefix.offset_prefix}{foot_name}",
            "offset_foot_shape",
            calf_name,
            True,
            mode="FOOT_TO_FLOOR",
        )

        target_foot = AddonFunctions.ensure_target(
            obj,
            offset_ankle,
            f"{pref.prefix.target_prefix}{foot_name}",
            "foot_target_shape",
            "",
            False,
            length=unit * 0.1,
            mode="FOOT_UNDER_FLOOR",
        )

        if target_foot.name == "TB_foot_l":
            target_foot.custom_shape_rotation_euler[1] *= -1

        if self.is_create_toe:
            roll_toe = AddonFunctions.ensure_target(
                obj,
                toe_name,
                f"{pref.prefix.gizmo_prefix}{pref.prefix.roll_prefix}{toe_name}",
                "gizmo_roll_shape",
                target_foot.name,
                False,
                length=unit * 0.1,
                mode="BALL_ROLL"
            )

            roll_foot = AddonFunctions.ensure_target(
                obj,
                offset_ankle,
                f"{pref.prefix.gizmo_prefix}{pref.prefix.roll_prefix}{foot_name}",
                "gizmo_roll_shape",
                roll_toe.name,
                False,
                length=unit * 0.1,
                mode="FOOT_ROLL",
                ref_name = roll_toe.name
            )

            roll_control = AddonFunctions.ensure_target(
                obj,
                calf_name,
                f"{pref.prefix.control_prefix}{foot_name}",
                "foot_control_shape",
                target_foot.name,
                False,
                length=unit * 0.2,
                mode="FOOT_CONTROL",
                ref_name=roll_toe.name
            )

            toe_control = AddonFunctions.ensure_target(
                obj,
                toe_name,
                f"{pref.prefix.control_prefix}{toe_name}",
                "ball_control_shape",
                foot_name,
                False,
                mode="DEFAULT",
            )

        gizmo_ankle = AddonFunctions.ensure_target(
            obj,
            calf_name,
            f"{pref.prefix.gizmo_prefix}{foot_name}",
            "gizmo_shape",
            parent_bone = roll_foot.name if self.is_create_toe else "",
            use_connect= False,
            mode="FOOT_TO_FLOOR"
        )

        pole_angle = AddonFunctions.compute_pole_angle(
            obj,
            thigh_name,
            foot_name,
            pole_pos,
        )

        con = AddonFunctions.get_or_create_constraint(calf_pb, "LEG - ", 'IK')
        con.target = obj
        con.subtarget = gizmo_ankle.name
        con.pole_target = obj
        con.pole_subtarget = target_knee.name
        con.pole_angle = pole_angle
        con.chain_count = self.leg_length
        con.use_tail = True
        con.use_stretch = False
        con.weight = 1.0
        con.influence = 1.0

        con = AddonFunctions.get_or_create_constraint(foot_pb, "OFFSET - ", 'COPY_TRANSFORMS')
        con.target = obj
        con.subtarget = offset_ankle.name
        con.target_space = 'LOCAL_OWNER_ORIENT'
        con.owner_space = 'LOCAL_WITH_PARENT'
        con.mix_mode = 'AFTER_FULL'
        con.influence = 1.0

        con = AddonFunctions.get_or_create_constraint(offset_ankle, "TARGET - ", 'COPY_ROTATION')
        con.target = obj
        con.subtarget = gizmo_ankle.name
        con.use_x = con.use_y = con.use_z = True
        con.target_space = 'WORLD'
        con.owner_space = 'WORLD'
        con.mix_mode = 'REPLACE'
        con.influence = 1.0

        con = AddonFunctions.get_or_create_constraint(target_foot, "", 'FLOOR')
        con.target = obj
        con.subtarget = root_name
        con.floor_location = 'FLOOR_Z'
        con.target_space = 'WORLD'
        con.owner_space = 'WORLD'

        if self.is_create_toe:
            roll_axis, axis_is_positive = AddonFunctions.detect_roll_axis(obj, toe_name)

            if axis_is_positive:
                toe_min, toe_max = math.radians(0), math.radians(45)
                foot_min, foot_max = math.radians(-45), math.radians(0)
            else:
                toe_min, toe_max = math.radians(-45), math.radians(0)
                foot_min, foot_max = math.radians(0), math.radians(45)

            con = AddonFunctions.get_or_create_constraint(roll_toe, "ROLL - ", 'COPY_ROTATION')
            con.target = obj
            con.subtarget = roll_control.name
            con.use_x = con.use_y = con.use_z = True
            con.target_space = 'LOCAL'
            con.owner_space = 'LOCAL'
            con.mix_mode = 'REPLACE'
            con.influence = 1.0

            con = AddonFunctions.get_or_create_constraint(roll_toe, "ROLL - ", 'LIMIT_ROTATION')
            con.use_limit_x = con.use_limit_y = con.use_limit_z = True
            setattr(con, f"min_{roll_axis}", toe_min)
            setattr(con, f"max_{roll_axis}", toe_max)
            con.use_transform_limit = True
            con.use_legacy_behavior = True
            con.owner_space = 'LOCAL'
            con.influence = 1.0

            con = AddonFunctions.get_or_create_constraint(roll_foot, "ROLL - ", 'COPY_ROTATION')
            con.target = obj
            con.subtarget = roll_control.name
            con.use_x = con.use_y = con.use_z = False
            setattr(con, f"use_{roll_axis}", True)
            con.target_space = 'LOCAL'
            con.owner_space = 'LOCAL'
            con.mix_mode = 'REPLACE'
            con.influence = 1.0

            con = AddonFunctions.get_or_create_constraint(roll_foot, "ROLL - ", 'LIMIT_ROTATION')
            con.use_limit_x = con.use_limit_y = con.use_limit_z = True
            setattr(con, f"min_{roll_axis}", foot_min)
            setattr(con, f"max_{roll_axis}", foot_max)
            con.use_transform_limit = True
            con.use_legacy_behavior = True
            con.owner_space = 'LOCAL'
            con.influence = 1.0

            con = AddonFunctions.get_or_create_constraint(roll_control, "ROLL - ", 'LIMIT_ROTATION')
            con.use_limit_x = con.use_limit_y = con.use_limit_z = True
            con.min_x = con.min_y = con.min_z = math.radians(-45)
            con.max_x = con.max_y = con.max_z = math.radians(45)
            con.use_transform_limit = True
            con.use_legacy_behavior = True
            con.owner_space = 'LOCAL'
            con.influence = 1.0

            con = AddonFunctions.get_or_create_constraint(toe_control, "ROLL - ", 'COPY_ROTATION')
            con.target = obj
            con.subtarget = roll_toe.name
            setattr(con, f"use_{roll_axis}", True)
            setattr(con, f"invert_{roll_axis}", True)
            con.mix_mode = 'AFTER'
            con.target_space = 'LOCAL'
            con.owner_space = 'LOCAL'
            con.influence = 1.0

            con = AddonFunctions.get_or_create_constraint(toe, "", 'COPY_ROTATION')
            con.target = obj
            con.subtarget = toe_control.name
            con.use_x = con.use_x = con.use_y = con.use_z = True
            con.target_space = 'LOCAL'
            con.owner_space = 'LOCAL'
            con.mix_mode = 'REPLACE'
            con.influence = 1.0

        self.report({'INFO'}, f"Generated Controller for LEG")
        return {'FINISHED'}

class WRYC_OT_CreateMannyController(bpy.types.Operator):
    bl_idname = "wryc.ot_create_manny_controller"
    bl_label = "UE5 Manny"
    bl_options = {'REGISTER', 'UNDO'}

    driver_coll_name: bpy.props.StringProperty(default="Driver", name="Driver Collection name")
    target_coll_name: bpy.props.StringProperty(default="Target Bones", name="Target Collection name")
    control_coll_name: bpy.props.StringProperty(default="Control Bones", name="Control Collection name")
    gizmo_coll_name: bpy.props.StringProperty(default="Gizmo Bones", name="Gizmo Collection name")
    mechanic_coll_name: bpy.props.StringProperty(default="Mechanic Bones", name="Mechanic Collection name")
    offset_coll_name: bpy.props.StringProperty(default="Offset Bones", name="Offset Collection name")


    def execute(self, context):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}
        obj = context.active_object
        arm = obj.data
        pref = AddonFunctions.get_preferences()

        driver_coll = AddonFunctions.get_or_create_collection(arm, self.driver_coll_name)
        target_coll = AddonFunctions.get_or_create_collection(arm, self.target_coll_name)
        control_coll = AddonFunctions.get_or_create_collection(arm, self.control_coll_name)
        gizmo_coll = AddonFunctions.get_or_create_collection(arm, self.gizmo_coll_name)
        mechanic_coll = AddonFunctions.get_or_create_collection(arm, self.mechanic_coll_name)
        offset_coll = AddonFunctions.get_or_create_collection(arm, self.offset_coll_name)

        for coll in (target_coll, control_coll, gizmo_coll, mechanic_coll, offset_coll):
            coll.parent = driver_coll

        basic_bone_names = [
            "root",
            "pelvis",
            "spine_01", "spine_02", "spine_03", "spine_04", "spine_05",
            "neck_01", "neck_02", "head",
            "clavicle_l", "upperarm_l", "lowerarm_l", "hand_l",
            "upperarm_twist_01_l", "upperarm_twist_02_l", "lowerarm_twist_02_l", "lowerarm_twist_01_l",
            "thumb_01_l", "thumb_02_l", "thumb_03_l",
            "index_metacarpal_l", "index_01_l", "index_02_l", "index_03_l",
            "middle_metacarpal_l", "middle_01_l", "middle_02_l", "middle_03_l",
            "ring_metacarpal_l", "ring_01_l", "ring_02_l", "ring_03_l",
            "pinky_metacarpal_l", "pinky_01_l", "pinky_02_l", "pinky_03_l",
            "thigh_l", "calf_l", "foot_l", "ball_l",
            "thigh_twist_01_l", "thigh_twist_02_l", "calf_twist_02_l", "calf_twist_01_l",
            "clavicle_r", "upperarm_r", "lowerarm_r", "hand_r",
            "upperarm_twist_01_r", "upperarm_twist_02_r", "lowerarm_twist_02_r", "lowerarm_twist_01_r",
            "thumb_01_r", "thumb_02_r", "thumb_03_r",
            "index_metacarpal_r", "index_01_r", "index_02_r", "index_03_r",
            "middle_metacarpal_r", "middle_01_r", "middle_02_r", "middle_03_r",
            "ring_metacarpal_r", "ring_01_r", "ring_02_r", "ring_03_r",
            "pinky_metacarpal_r", "pinky_01_r", "pinky_02_r", "pinky_03_r",
            "thigh_r", "calf_r", "foot_r", "ball_r",
            "thigh_twist_01_r", "thigh_twist_02_r", "calf_twist_02_r", "calf_twist_01_r",
        ]

        for bone_name in basic_bone_names:
            pb = obj.pose.bones.get(bone_name)
            if not pb:
                continue

            shape_config = None
            mirror_mode = arm.use_mirror_x
            arm.use_mirror_x = False

            if pb.name == "root":
                shape_config = "root_shape"
            elif "spine" in pb.name or pb.name in ["pelvis", "neck_01", "neck_02", "head"]:
                shape_config = "spine_shape"
            elif pb.name in ["upperarm_l", "lowerarm_l", "upperarm_r", "lowerarm_r", \
                    "thigh_l", "calf_l", "thigh_r", "calf_r"]:
                shape_config = "limbs_shape"
            elif "twist" in pb.name:
                shape_config = "twist_shape"
                pb.lock_ik_x = True
                pb.lock_ik_z = True
            elif any(keyword in pb.name for keyword in ["thumb", "index", "middle", "ring", "pinky"]):
                if "metacarpal" in pb.name.lower():
                    shape_config = "metacarpal_shape"
                else:
                    shape_config = "finger_shape"
            elif pb.name in ["hand_l", "hand_r"]:
                shape_config = "joint_hand_shape"
            elif pb.name in ["foot_l", "ball_l", "foot_r", "ball_r"]:
                shape_config = "joint_foot_shape"
            elif pb.name in ["clavicle_l", "clavicle_r"]:
                shape_config = "clavicle_shape"

            if shape_config and pb.custom_shape is None:
                AddonFunctions.apply_bone_shape_settings(pb, shape_config, obj)

        bpy.ops.wryc.ot_create_spine_controller('EXEC_DEFAULT',
            head="head", chest="spine_05", pelvis="pelvis")
        bpy.ops.wryc.ot_create_head_controller('EXEC_DEFAULT',
            head="head", chest="spine_05")
        bpy.ops.wryc.ot_create_arm_controller('EXEC_DEFAULT',
            hand="hand_l", arm_length=2)
        bpy.ops.wryc.ot_create_arm_controller('EXEC_DEFAULT',
            hand="hand_r", arm_length=2)
        bpy.ops.wryc.ot_create_leg_controller('EXEC_DEFAULT',
            foot="foot_l", toe="ball_l", leg_length=2, is_create_toe=True)
        bpy.ops.wryc.ot_create_leg_controller('EXEC_DEFAULT',
            foot="foot_r", toe="ball_r", leg_length=2, is_create_toe=True)

        finger_prefixes = ["thumb", "index", "middle", "ring", "pinky"]
        sides = ["_l", "_r"]

        for side in sides:
            for root in finger_prefixes:
                finger_bone_name = f"{root}_01{side}"
                if finger_bone_name in obj.pose.bones:
                    bpy.ops.wryc.ot_create_finger_controller('EXEC_DEFAULT', root_bone = finger_bone_name)

        for side in sides:
            control_meta = AddonFunctions.ensure_target(
                obj,
                f"pinky_metacarpal{side}",
                f"{pref.prefix.control_prefix}pinky_metacarpal{side}",
                "hand_control_shape",
                f"hand{side}",
                False,
            )
            for name in finger_prefixes[2:]:
                pb = obj.pose.bones.get(f"{name}_metacarpal{side}")
                con = AddonFunctions.get_or_create_constraint(pb,"METACARPAL", 'COPY_ROTATION')
                con.target = obj
                con.subtarget = control_meta.name
                con.use_x = con.use_y = con.use_z = True
                con.mix_mode = 'BEFORE'
                con.target_space = 'LOCAL'
                con.owner_space = 'LOCAL'
                if name == finger_prefixes[2]:
                    con.influence = 0.1
                elif name == finger_prefixes[3]:
                    con.influence = 0.5
                elif name == finger_prefixes[4]:
                    con.influence = 1.0

        arm.use_mirror_x = mirror_mode

        bpy.ops.object.mode_set(mode='POSE')
        for pb in obj.pose.bones:
            if pb.name.startswith(pref.prefix.target_prefix):
                target_coll.assign(pb.bone)
            elif pb.name.startswith(pref.prefix.control_prefix):
                control_coll.assign(pb.bone)
            elif pb.name.startswith(pref.prefix.gizmo_prefix):
                gizmo_coll.assign(pb.bone)
            elif pb.name.startswith(pref.prefix.mechanic_prefix):
                mechanic_coll.assign(pb.bone)
            elif pb.name.startswith(pref.prefix.offset_prefix):
                offset_coll.assign(pb.bone)

        self.report({'INFO'}, "Generated UE5 Manny controllers")
        return {'FINISHED'}

#__RETARGET ACTIONS__
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
                if action.name not in exiting_names:
                    item = settings.mapping_actions.add()
                    item.name = action.name
                    item.enabled = old_states.get(action.name, False)

        valid_names = {a.name for a in bpy.data.actions}
        to_remove = [i for i, a in enumerate(settings.mapping_actions) if a.name not in valid_names]
        for i in reversed(to_remove):
            settings.mapping_actions.remove(i)

        AddonFunctions.sort_actions(settings.mapping_actions)
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        actions = context.scene.bone_mapping_settings.mapping_actions

        if not bpy.data.actions:
            layout.label(text="No actions in scene")
            return

        row = layout.row(align=True)
        row.operator("wryc.ot_enable_all_mapping_actions", text="Enable All")
        row.operator("wryc.ot_disable_all_mapping_actions", text="Disable All")

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

class WRYC_OT_EnableAllMappingActions(bpy.types.Operator):
    bl_idname = "wryc.ot_enable_all_mapping_actions"
    bl_label = "Enable All Actions"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        for entry in context.scene.bone_mapping_settings.mapping_actions:
            entry.enabled = True
        return {'FINISHED'}

class WRYC_OT_DisableAllMappingActions(bpy.types.Operator):
    bl_idname = "wryc.ot_disable_all_mapping_actions"
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
            rename_count = 0

            for fcurve_coll in AddonUtils.Compat.get_fcurve_collection(action):
                fcurve_to_modify = []

                for fcurve in fcurve_coll:
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

                for fcurve, old_bone in fcurve_to_modify:
                    new_bone = bone_mappings_dict[old_bone]

                    if new_bone == "" or new_bone is None :
                        fcurve_coll.remove(fcurve)
                    else:
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

    filepath: bpy.props.StringProperty(
        subtype='FILE_PATH',
        default="bone_mapping.json",
    )
    filename_ext = ".json"

    def execute(self, context):
        props = context.scene.bone_mapping_settings
        data = [{"source": m.source, "target":m.target} for m in props.mappings]

        if not self.filepath.lower().endswith(".json"):
            self.filepath += ".json"

        with open(self.filepath, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        props.set_last_path(self.filepath)

        self.report({'INFO'}, "Bone Mapping Exported")
        return {'FINISHED'}

    def invoke(self, context, event):
        props = context.scene.bone_mapping_settings
        self.filepath = props.get_last_path()
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class WRYC_OT_BoneMappingImport(bpy.types.Operator):
    bl_idname = "wryc.ot_bone_mapping_import"
    bl_label = "Import"

    filepath: bpy.props.StringProperty(subtype='FILE_PATH')

    def execute(self, context):
        if not self.filepath.lower().endswith(".json"):
            self.report({'ERROR'}, "Only .json file can be supported")
            return {'CANCELLED'}

        props = context.scene.bone_mapping_settings

        with open(self.filepath, "r", encoding='utf-8') as f:
            data = json.load(f)

        props.mappings.clear()
        for item in data:
            map_item = props.mappings.add()
            map_item.source = item.get("source", "")
            map_item.target = item.get("target", "")

        props.active_index = 0
        self.report({'INFO'}, "Bone Mapping Imported")
        return {'FINISHED'}

    def invoke(self, context, event):
        props = context.scene.bone_mapping_settings
        self.filepath = props.get_last_path()
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#__RENAME TOOL__
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

#__Add Manny__
class WRYC_OT_AddUE5Manny(bpy.types.Operator):
    bl_idname = "wryc.ot_add_ue5_manny"
    bl_label = "UE5 Manny (Simple)"
    bl_options = {'REGISTER', 'UNDO'}

    import_mesh: bpy.props.BoolProperty(
        name="Include Mesh",
        default=False
    )

    def execute(self, context):
        path = AddonFunctions.get_preferences().assets_folder
        manny_file= os.path.join(path, "SKM_Manny.blend")
        target_names = ["SKM_Manny_Simple", "root"]
        if self.import_mesh:
            target_names.append("SKM_Manny_Simple_LOD0")

        with bpy.data.libraries.load(manny_file) as (data_from, data_to):
            data_to.objects = [name for name in data_from.objects if name in target_names]

        new_empty = None
        new_arm = None
        new_mesh = None

        for obj in data_to.objects:
            context.collection.objects.link(obj)

            if "SKM_Manny_Simple" in obj.name:
                new_empty = obj
            elif "root" in obj.name:
                new_arm = obj
            elif "SKM_Manny_Simple_LOD0" in obj.name:
                new_mesh = obj

            if new_empty and new_arm:
                new_arm.parent = new_empty

            if new_mesh and new_arm:
                new_mesh.parent = new_arm

        self.report({'INFO'}, "UE Manny Imported")
        return {'FINISHED'}

