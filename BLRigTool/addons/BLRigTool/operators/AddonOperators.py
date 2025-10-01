import difflib
import json
import os
from itertools import chain
from re import search, split

import bpy
import math

from bpy_extras.io_utils import ExportHelper

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

#__GENERATE CONSTRAINTS__
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

#__RENAME TOOL__
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

#__EXPORT TOOL__
class WRYC_OT_ExportToUnreal(bpy.types.Operator, ExportHelper):
    bl_idname = "wryc.ot_export_to_unreal"
    bl_label = "BL Export to Unreal"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout

        settings = context.scene.export_to_unreal

        box_mesh = layout.box()
        box_mesh.label(text="Mesh/Armature")
        box_mesh.prop(settings, "mesh_path", text="Mesh Path:")
        row = box_mesh.row(align=True)
        '''row.prop(settings, "is_export_mesh", text="Export Mesh")'''
        row.prop(settings, "apply_modifiers", text="Apply Modifiers")
        box_mesh.prop(settings, "skeletal_prefix", text="Skeletal Prefix:")
        '''box_mesh.prop(settings, "static_prefix", text="Static Prefix:")'''

        box_action = layout.box()
        box_action.label(text="Action")
        box_action.prop(settings, "action_path", text="Action Path")
        box_action.prop(settings, "export_type", text="Export Type")
        row = box_action.row(align=True)
        row.prop(settings, "is_add_start_end", text="Add Start/End Keyframes")
        box_action.prop(settings, "action_prefix", text="Action Prefix:")

        box_advanced = layout.box()
        box_advanced.label(text="Advanced Settings")
        row = box_advanced.row()
        row.prop(settings, "only_deform", text="Only Deform Bones")
        row.prop(settings, "add_leaf", text="Add Leaf Bones")

        row = box_advanced.row()
        col = row.column(align=True)
        split = col.split(factor=0.7, align=True)
        split.label(text="Primary Bone Axis")
        split.prop(settings, "primary_bone_axis", text="")
        split = col.split(factor=0.7, align=True)
        split.label(text="Secondary Bone Axis")
        split.prop(settings, "secondary_bone_axis", text="")

        col = row.column(align=True)
        split = col.split(factor=0.7, align=True)
        split.label(text="FBX Axis Forward")
        split.prop(settings, "axis_forward", text="")
        split = col.split(factor=0.7, align=True)
        split.label(text="FBX Axis Up")
        split.prop(settings, "axis_up", text="")

    def execute(self, context):
        settings = context.scene.export_to_unreal

        armatures = [obj for obj in context.selected_objects if obj.type == 'ARMATURE']
        if not armatures:
            self.report({'ERROR'}, "No armature selected")
            return {'CANCELLED'}

        meshs = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if settings.mesh_path.strip() and settings.is_export_mesh and not meshs:
            self.report({'ERROR'}, "No mesh selected")
            return {'CANCELLED'}

        arm = armatures[0]
        armature_name = arm.name

        selected_objects = context.selected_objects[:]
        active_obj = context.view_layer.objects.active

        original_name = arm.name
        original_action = arm.animation_data.action if arm.animation_data else None

        try:
            bpy.context.view_layer.objects.active = arm
            arm.name = "Armature"
            if arm.data.users > 1:
                arm.data = arm.data.copy()

            bpy.ops.object.mode_set(mode='EDIT')
            edit_bones = arm.data.edit_bones

            if "root" not in edit_bones:
                root = edit_bones.new("root")
                root.head = (0, 0, 0)
                root.tail = (0, 0.1, 0)
                for b in edit_bones:
                    if b.name != "root" and b.parent is None:
                        b.parent = root
            else:
                root = edit_bones["root"]
                root.head = (0, 0, 0)
            bpy.ops.object.mode_set(mode='OBJECT')

            arm.scale *= 100.0
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            for action in bpy.data.actions:
                for fcurve in action.fcurves:
                    if fcurve.data_path.endswith('location'):
                        for kp in fcurve.keyframe_points:
                            kp.co.y *= 100
                            kp.handle_left.y *= 100
                            kp.handle_right.y *= 100

            bpy.ops.object.select_all(action='DESELECT')
            arm.select_set(True)
            for mesh in meshs:
                mesh.select_set(True)

            bpy.context.view_layer.objects.active = arm

            # Mesh/Armature
            if settings.mesh_path.strip():
                export_dir = bpy.path.abspath(settings.mesh_path)
                sk_file_name = settings.skeletal_prefix + armature_name
                export_file = os.path.join(export_dir, sk_file_name + ".fbx")

                AddonFunctions.do_export(
                    context, filepath=export_file, object_type={'ARMATURE', 'MESH'},scale=0.01, bake_anim=False
                )
                self.report({'INFO'}, f"Mesh/Armature Exported Successfully")

            #Action
            if settings.action_path.strip():
                bpy.ops.object.select_all(action='DESELECT')
                arm.select_set(True)
                bpy.context.view_layer.objects.active = arm

                if settings.export_type == "SELECTED":
                    action = arm.animation_data.action if arm.animation_data else None
                    if not action:
                        self.report({'ERROR'}, "No active action in selected armature")
                    else:

                        export_name = settings.action_prefix + action.name
                        act_file = bpy.path.abspath(
                            settings.action_path + "/" +  export_name + ".fbx"
                        )
                        arm.animation_data.action = action
                        AddonFunctions.do_export(
                            context, filepath=act_file, object_type={'ARMATURE'}, scale=0.01, bake_anim=True, bake_all=False
                        )

                        self.report({'INFO'}, f"Exported selected action successfully: {act_file}")
    
                elif settings.export_type == "BATCH":
                    for action in bpy.data.actions:
                        if not action:
                            continue

                        export_name = settings.action_prefix + action.name
                        act_file = bpy.path.abspath(
                               settings.action_path + "/" + export_name + ".fbx"
                        )
                        arm.animation_data.action = action
                        AddonFunctions.do_export(
                            context, filepath=act_file, object_type={'ARMATURE'}, scale=0.01,bake_anim=True,bake_all=False
                        )

                    self.report({'INFO'}, f"Exported action by batch successfully")
    
                elif settings.export_type == "ALL":
                    blend_name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
                    export_file = os.path.join(bpy.path.abspath(settings.action_path), blend_name + ".fbx")
                    if bpy.data.actions:
                        arm.animation_data.action = bpy.data.actions[0]

                    AddonFunctions.do_export(
                        context, filepath=export_file, object_type={'ARMATURE'}, scale=0.01, bake_anim=True,bake_all=True
                    )
                    self.report({'INFO'}, f"Exported all action successfully")

                else:
                    self.report({'INFO'}, "Action path is empty, skip action export")

        finally:
            bpy.context.view_layer.objects.active = arm
            if arm.data.users > 1:
                arm.data = arm.data.copy()
            arm.name = original_name

            arm.scale *= 0.01
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            for action in bpy.data.actions:
                for fcurve in action.fcurves:
                    if fcurve.data_path.endswith('location'):
                        for kp in fcurve.keyframe_points:
                            kp.co.y /= 100
                            kp.handle_left.y /= 100
                            kp.handle_right.y /= 100

            if original_action:
                arm.animation_data.action = original_action

            bpy.ops.object.select_all(action='DESELECT')
            for obj in selected_objects:
                obj.select_set(True)
            if active_obj:
                context.view_layer.objects.active = active_obj

        return {'FINISHED'}