import difflib
import json
import os
from _ast import operator
from itertools import chain
from re import search, split

import bpy
import math
import mathutils

from bpy_extras.io_utils import ExportHelper
from setuptools.command.rotate import rotate

from ..config import __addon_name__
from ..functions import AddonFunctions
from ..properties import AddonProperties
from ..preference import AddonPreferences

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

        blend_path = AddonFunctions.get_library_path()
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

            src_dir = src_bone.tail_local - src_bone.head_local
            length = src_dir.length
            if length == 0:
                continue

            src_dir_normalized = src_dir.normalized()

            tgt_head_world = tgt_obj.matrix_world @ tgt_bone.head_local
            tgt_head_local = tgt_obj.matrix_world.inverted() @ tgt_head_world

            def_bone.head = tgt_head_local
            def_bone.tail = tgt_head_local + src_dir_normalized * length

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

            p_def = tgt_obj.pose.bones[def_name]

            if "DEFORM - CHILD_OF" in p_def.constraints:
                continue


            con = AddonFunctions.get_or_create_constraint(p_def, "DEFORM - ", "CHILD_OF")
            con.target = tgt_obj
            con.subtarget = tgt_name
            AddonFunctions.apply_child_of_inverse(context, tgt_obj, p_def, con)

        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Deform Bones generated and connected.")
        return {'FINISHED'}

class WRYC_OT_CreateDeformBones(bpy.types.Operator):
    bl_idname = "wryc.ot_create_deform_bones"
    bl_label = "Generate Deform Bones"
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
    def_collection_name: bpy.props.StringProperty(name="Collection Name",default="Deform Bones")

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
            split.prop(self, "def_collection_name", text="")
        else:
            layout.label(text="Select an Armature", icon="ERROR")

    def execute(self, context):
        pref = AddonFunctions.get_preferences()
        obj = context.object
        arm_data = obj.data

        selected_bones = AddonFunctions.get_selected_bones(context, self)
        if not selected_bones:
            return {'CANCELLED'}

        selected_names = {pb.name for pb in selected_bones}

        if self.def_collection_name not in arm_data.collections:
            def_collection = arm_data.collections.new(self.def_collection_name)
        else:
            def_collection = arm_data.collections[self.def_collection_name]

        bpy.ops.object.mode_set(mode='EDIT')
        edit_bones = arm_data.edit_bones

        bone_map = {}

        for orig_bone in arm_data.bones:
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
            orig_bone = arm_data.bones[orig_name]
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

class WRYC_OT_CreateFingerController(bpy.types.Operator):
    bl_idname = "wryc.ot_create_finger_controller"
    bl_label = "Finger"
    bl_description = "Create finger controller"
    bl_options = {'REGISTER', 'UNDO'}

    root_bone: bpy.props.StringProperty(name="Root Bone")
    target_bone: bpy.props.StringProperty(name="Target Bone")


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

            layout.label(text="Control Bone")
            layout.prop_search(self, "target_bone", obj.data, "bones", text="TB Bone")

            sub = layout.row()
            sub.enabled = False
            sub.label(text="If not select Control Bone, will generate new Control Bone")

            row = layout.row()
            row.enabled = bool(not self.target_bone)
            row.prop(context.window_manager.bone_shapes_library, "finger_bone_shape", expand=False, text="Target Bone Shape")
        else:
            layout.label(text="Select an Armature", icon="ERROR")

    def execute(self, context):
        pref = AddonFunctions.get_preferences()
        obj = context.object

        if not self.root_bone:
            self.report({'ERROR'}, "Please select the first bone in the finger chain")
            return {'CANCELLED'}

        root_name = self.root_bone

        raw_target_name = self.target_bone.strip() if self.target_bone else f"{pref.target_prefix} + {root_name}"
        target_name = AddonFunctions.ensure_target(
            obj,
            root_name,
            raw_target_name,
            context.window_manager.bone_shapes_library.finger_bone_shape,
            None,
            False,
        )

        chain = AddonFunctions.collect_bone_chain(obj.pose.bones[root_name])

        for pb in chain:
            con = AddonFunctions.get_or_create_constraint(
                pb,
                "FINGER - ",
                "COPY_ROTATION"
            )
            con.target = obj
            con.subtarget = target_name
            con.target_space = 'LOCAL'
            con.owner_space = 'LOCAL'
            con.mix_mode = 'BEFORE'

        self.report({'INFO'}, f"Generate Constraint For Finger")
        return {'FINISHED'}

class WRYC_OT_CreateArmController(bpy.types.Operator):
    bl_idname = "wryc.ot_create_arm_controller"
    bl_label = "Arm"
    bl_description = "Generate Arm Controller"
    bl_options = {'REGISTER', 'UNDO'}

    hand: bpy.props.StringProperty(name="Hand Bone")
    arm_length: bpy.props.IntProperty(name="Arm Length", default=2, min=2)

    target_elbow: bpy.props.StringProperty(name="TB Elbow")
    target_wrist: bpy.props.StringProperty(name="TB Wrist")
    pole_direction: bpy.props.EnumProperty(
        name="Pole Direction",
        items=[
            ("X+", "+X", "Positive X axis"),
            ("X-", "-X", "Negative X axis"),
            ("Y+", "+Y", "Positive Y axis"),
            ("Y-", "-Y", "Negative Y axis"),
            ("Z+", "+Z", "Positive Z axis"),
            ("Z-", "-Z", "Negative Z axis")
        ],
        default="X+"
    )

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

            layout.label(text="Control Bone")
            layout.prop_search(self, "target_elbow", obj.data, "bones", text="Elbow")
            layout.prop_search(self, "target_wrist", obj.data, "bones", text="Wrist")

            sub = layout.row()
            sub.enabled = False
            sub.label(text="If not select Control Bone, will generate new Control Bone")

            layout.prop(self, "pole_direction")

            row = layout.row()
            row.enabled = bool(not self.target_elbow)
            layout.prop(context.window_manager.bone_shapes_library, "arm_elbow_shape", expand=False, text="Elbow Shape")

            row = layout.row()
            row.enabled = bool(not self.target_wrist)
            layout.prop(context.window_manager.bone_shapes_library, "arm_hand_shape", expand=False, text="Hand Shape")
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

        raw_target_wrist = self.target_wrist.strip() if self.target_wrist else f"{pref.target_prefix} +{hand_name}"
        target_wrist = AddonFunctions.ensure_target(
            obj,
            hand_name,
            raw_target_wrist,
            context.window_manager.bone_shapes_library.arm_hand_shape,
            "",
            False,
        )

        if not self.target_elbow.strip():
            pole_pos = AddonFunctions.compute_pole_position(
                obj,
                upper_name,
                lower_name,
                hand_name,
                direction=self.pole_direction,
            )
            target_elbow = AddonFunctions.ensure_target(
                obj,
                upper_name,
                f"{pref.target_prefix} + {upper_name}",
                context.window_manager.bone_shapes_library.arm_elbow_shape,
                parent_name="",
                position=pole_pos,
            )
        else:
            raw_target_elbow = self.target_elbow.strip()
            target_elbow = AddonFunctions.ensure_target(
                obj,
                upper_name,
                raw_target_elbow,
                parent_name="",
                use_connect=False,
            )
        pole_pos = obj.matrix_world @ target_elbow.head
        pole_angle = AddonFunctions.compute_pole_angle(
            obj,
            upper_name,
            hand_name,
            pole_pos,
        )

        wrist_name = target_wrist.name
        elbow_name = target_elbow.name

        con = AddonFunctions.get_or_create_constraint(lower_pb, "ARM - ", 'IK')
        con.target = obj
        con.subtarget = wrist_name
        con.pole_target = obj
        con.pole_subtarget = elbow_name
        if not self.target_elbow.strip():
            con.pole_angle = pole_angle
        else:
            con.pole_angle = 0.0
        con.chain_count = self.arm_length
        con.use_tail = True
        con.use_stretch = False
        con.weight = 1.0
        con.influence = 1.0

        con = AddonFunctions.get_or_create_constraint(hand_pb, "TARGET - ", 'COPY_ROTATION')
        con.target = obj
        con.subtarget = wrist_name
        con.use_x = con.use_y = con.use_z = True
        con.target_space = 'WORLD'
        con.owner_space = 'WORLD'
        con.mix_mode = 'REPLACE'
        con.influence = 1.0

        self.report({'INFO'}, f"Generated Controller for Arm")
        return {'FINISHED'}

class WRYC_OT_CreateLegController(bpy.types.Operator):
    bl_idname = "wryc.ot_create_leg_controller"
    bl_label = "Leg"
    bl_description = "Generate Leg Controller"
    bl_options = {'REGISTER', 'UNDO'}

    foot: bpy.props.StringProperty(name="Foot Bone")
    leg_length: bpy.props.IntProperty(name="Leg Length", default=2, min=2)

    target_knee: bpy.props.StringProperty(name="TB Knee")
    target_ankle: bpy.props.StringProperty(name="GB Ankle")
    offset_ankle: bpy.props.StringProperty(name="OB Ankle")

    pole_direction: bpy.props.EnumProperty(
        name="Pole Direction",
        items=[
            ("X+", "+X", "Positive X axis"),
            ("X-", "-X", "Negative X axis"),
            ("Y+", "+Y", "Positive Y axis"),
            ("Y-", "-Y", "Negative Y axis"),
            ("Z+", "+Z", "Positive Z axis"),
            ("Z-", "-Z", "Negative Z axis")
        ],
        default="X+"
    )

    def invoke(self, context, event):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj and obj.type == 'ARMATURE':
            layout.label(text="Basic Bone")
            layout.prop_search(self, "foot", obj.data, "bones", text="Foot")
            layout.prop(self, "leg_length")

            layout.label(text="Control Bone")
            layout.prop_search(self, "target_knee", obj.data, "bones", text="Knee")
            layout.prop_search(self, "target_ankle", obj.data, "bones", text="Ankle")
            layout.prop_search(self, "offset_ankle", obj.data, "bones", text="Offset Ankle")

            sub = layout.row()
            sub.enabled = False
            sub.label(text="If not select Control Bone, will generate new Control Bone")

            layout.prop(self, "pole_direction")

            row = layout.row()
            row.enabled = bool(not self.target_knee)
            layout.prop(context.window_manager.bone_shapes_library, "leg_knee_shape", expand=False, text="Knee Shape")

            row = layout.row()
            row.enabled = bool(not self.target_ankle)
            layout.prop(context.window_manager.bone_shapes_library, "leg_ankle_shape", expand=False, text="Ankle Shape")

            row = layout.row()
            row.enabled = bool(not self.offset_ankle)
            layout.prop(context.window_manager.bone_shapes_library, "leg_offset_shape", expand=False, text="Ankle Offset Shape")
        else:
            layout.label(text="Select an Armature", icon="ERROR")

    def execute(self, context):
        obj = context.object
        pref = AddonFunctions.get_preferences()

        if not self.foot:
            self.report({'ERROR'}, f"Please select the foot bone")
            return {'CANCELLED'}

        chain = []
        pb = obj.pose.bones.get(self.foot)
        if not pb:
            self.report({'ERROR'}, f"Hand Bone {self.foot} not found")
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

        raw_offset_ankle = self.offset_ankle.strip() if self.offset_ankle else f"{pref.offset_prefix} + {foot_name}"
        offset_ankle = AddonFunctions.ensure_foot_ob_bone(
            obj,
            calf_name,
            raw_offset_ankle,
            context.window_manager.bone_shapes_library.leg_offset_shape,
        )
        offset_name = offset_ankle.name

        raw_target_ankle = self.target_ankle.strip() if self.target_ankle else f"{pref.gizmo_prefix} + {foot_name}"
        target_ankle = AddonFunctions.ensure_target(
            obj,
            offset_ankle,
            raw_target_ankle,
            context.window_manager.bone_shapes_library.leg_ankle_shape,
            "",
            False,
        )
        ankle_name = target_ankle.name

        if not self.target_knee.strip():
            pole_pos = AddonFunctions.compute_pole_position(
                obj,
                thigh_name,
                calf_name,
                foot_name,
                direction=self.pole_direction,
            )
            target_knee = AddonFunctions.ensure_target(
                obj,
                thigh_name,
                f"{pref.target_prefix} + {thigh_name}",
                parent_name="",
                position=pole_pos,
            )
        else:
            raw_target_knee = self.target_knee.strip()
            target_knee = AddonFunctions.ensure_target(
                obj,
                thigh_name,
                raw_target_knee,
                context.window_manager.bone_shapes_library.arm_knee_shape,
                "",
                use_connect=False,
            )
        knee_name = target_knee.name


        pole_pos = obj.matrix_world @ target_knee.head
        pole_angle = AddonFunctions.compute_pole_angle(
            obj,
            thigh_name,
            calf_name,
            pole_pos,
        )

        con = AddonFunctions.get_or_create_constraint(calf_pb, "LEG - ", 'IK')
        con.target = obj
        con.subtarget = ankle_name
        con.pole_target = obj
        con.pole_subtarget = knee_name
        if not self.target_knee.strip():
            con.pole_angle = pole_angle
        else:
            con.pole_angle = 0.0
        con.chain_count = self.leg_length
        con.use_tail = True
        con.use_stretch = False
        con.weight = 1.0
        con.influence = 1.0

        con = AddonFunctions.get_or_create_constraint(foot_pb, "OFFSET - ", 'COPY_TRANSFORMS')
        con.target = obj
        con.subtarget = offset_name
        con.target_space = 'LOCAL_OWNER_ORIENT'
        con.owner_space = 'LOCAL_WITH_PARENT'
        con.mix_mode = 'AFTER_FULL'
        con.influence = 1.0

        con = AddonFunctions.get_or_create_constraint(offset_ankle, "TARGET - ", 'COPY_ROTATION')
        con.target = obj
        con.subtarget = ankle_name
        con.use_x = con.use_y = con.use_z = True
        con.target_space = 'WORLD'
        con.owner_space = 'WORLD'
        con.mix_mode = 'REPLACE'
        con.influence = 1.0

        self.report({'INFO'}, f"Generated Controller for LEG")
        return {'FINISHED'}

'''class WRYC_OT_CreateFootController(bpy.types.Operator):
    bl_idname = "wryc.ot_create_foot_controller"
    bl_label = "Foot"
    bl_description = "Create foot controller"
    bl_options = {'REGISTER', 'UNDO'}

    foot = bpy.props.StringProperty(name="Foot Bone")
    ball = bpy.props.StringProperty(name="Ball Bone")

    target_ankle = bpy.props.StringProperty(name="Target Ankle")
    target_heel = bpy.props.StringProperty(name="Target Foot")
    target_ball = bpy.props.StringProperty(name="Target Ball")
    target_roll = bpy.props.StringProperty(name="Target Roll")

    def invoke(self, context, event):
        if not AddonFunctions.check_pose_mode(context, self):
            return {'CANCELLED'}
        return context.window_manager.invoke_props_dialog(self, width=300)

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj and obj.type == 'ARMATURE':
            layout.label(text="Basic Bone")
            layout.prop_search(self, "foot", obj.data, "bones", text="Foot")
            layout.prop_search(self, "ball", obj.data, "bones", text="Ball")

            layout.label(text="Control Bone")
            layout.prop_search(self, "target_ankle", obj.data, "bones", text="GB Ankle")
            layout.prop_search(self, "target_heel", obj.data, "bones", text="TB Heel")
            layout.prop_search(self, "target_ball", obj.data, "bones", text="CB Ball")
            layout.prop_search(self, "target_roll", obj.data, "bones", text="CB Roll")

            sub = layout.row()
            sub.enabled = False
            sub.label(text="If not select Control Bone, will generate new Control Bone")

            row = layout.row()
            row.enabled = bool(not self.target_ankle)
            layout.prop(context.window_manager.bone_shapes_library, "foot_ankle_shape", expand=False, text="Ankle Shape")

            row = layout.row()
            row.enabled = bool(not self.target_heel)
            layout.prop(context.window_manager.bone_shapes_library, "foot_heel_shape", expand=False, text="Heel Shape")

            row = layout.row()
            row.enabled = bool(not self.target_ball)
            layout.prop(context.window_manager.bone_shapes_library, "foot_ball_shape", expand=False, text="Ball Shape")

            row = layout.row()
            row.enabled = bool(not self.target_roll)
            layout.prop(context.window_manager.bone_shapes_library, "foot_roll_shape", expand=False, text="Roll Shape")
        else:
            layout.label(text="Select an Armature", icon="ERROR")

    def execute(self, context):'''

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

                if new_bone == "" or new_bone is None :
                    action.fcurves.remove(fcurve)
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