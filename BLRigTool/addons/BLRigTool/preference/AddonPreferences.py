import os
import math

import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty, FloatVectorProperty, PointerProperty
from bpy.types import PropertyGroup ,AddonPreferences
from ..functions import AddonFunctions

from ..config import __addon_name__

class BoneShapeConfig(PropertyGroup):
    show_advanced : BoolProperty(default=False)
    shape: EnumProperty(
        name="Shape",
        items=AddonFunctions.get_bone_shapes_library,
    )
    color: EnumProperty(
        name="Color",
        items=AddonFunctions.bone_color_items,
    )
    loc: FloatVectorProperty(
        name="Translation",
        size=3,
        subtype='TRANSLATION',
        default=(0.0, 0.0, 0.0)
    )
    rot: FloatVectorProperty(
        name="Rotation",
        size=3,
        subtype='EULER',
        default=(0.0, 0.0, 0.0)
    )
    scale: FloatVectorProperty(
        name="Scale",
        size=3,
        subtype='XYZ',
        default=(1.0, 1.0, 1.0)
    )
    def set(self, shape=None, color=None, loc=None, rot=None, scale=None):
        if shape is not None:
            try:
                self.shape = shape
            except TypeError:
                print(f"Warning: Shape: {shape} not found in shape library")
        if color is not None:
            self.color = color
        if loc is not None:
            self.loc = loc
        if rot is not None:
            self.rot = [math.radians(d) for d in rot]
        if scale is not None:
            if isinstance(scale, (int, float)):
                self.scale = (scale, scale, scale)
            else:
                self.scale = scale
class BonePrefix(PropertyGroup):
    # Bone Prefix
    deform_prefix: StringProperty(
        name="Deform Prefix",
        default="DEF_",
    )
    target_prefix: StringProperty(
        name="Target Prefix",
        default="TB_",
    )
    control_prefix: StringProperty(
        name="Control Prefix",
        default="CB_",
    )
    gizmo_prefix: StringProperty(
        name="Gizmo Prefix",
        default="GB_",
    )
    mechanic_prefix: StringProperty(
        name="Mechanic Prefix",
        default="MB_",
    )
    offset_prefix: StringProperty(
        name="Offset Prefix",
        default="OB_",
    )
    roll_prefix: StringProperty(
        name="Roll Prefix",
        default="ROLL_",
    )
    track_prefix: StringProperty(
        name="Track Prefix",
        default="TRACK_",
    )

class GeneralBoneDisplaySettings(PropertyGroup):
    # Bone Config Fold Enable
    show_basic: BoolProperty(default=False)
    show_offset: BoolProperty(default=False)
    show_gizmo: BoolProperty(default=False)
    show_mechanic: BoolProperty(default=False)
    show_control: BoolProperty(default=False)
    show_target: BoolProperty(default=False)
    # Basic
    root_shape: PointerProperty(type=BoneShapeConfig)
    spine_shape: PointerProperty(type=BoneShapeConfig)
    limbs_shape: PointerProperty(type=BoneShapeConfig)
    twist_shape: PointerProperty(type=BoneShapeConfig)
    finger_shape: PointerProperty(type=BoneShapeConfig)
    joint_hand_shape: PointerProperty(type=BoneShapeConfig)
    joint_foot_shape: PointerProperty(type=BoneShapeConfig)
    clavicle_shape: PointerProperty(type=BoneShapeConfig)
    metacarpal_shape: PointerProperty(type=BoneShapeConfig)
    # Offset
    offset_head_shape: PointerProperty(type=BoneShapeConfig)
    offset_foot_shape: PointerProperty(type=BoneShapeConfig)
    # Gizmo
    gizmo_shape: PointerProperty(type=BoneShapeConfig)
    gizmo_roll_shape: PointerProperty(type=BoneShapeConfig)
    # Mechanic
    mechanic_shape: PointerProperty(type=BoneShapeConfig)
    # Control
    pelvis_control_shape: PointerProperty(type=BoneShapeConfig)
    clavicle_control_shape: PointerProperty(type=BoneShapeConfig)
    head_control_shape: PointerProperty(type=BoneShapeConfig)
    foot_control_shape: PointerProperty(type=BoneShapeConfig)
    ball_control_shape: PointerProperty(type=BoneShapeConfig)
    hand_control_shape: PointerProperty(type=BoneShapeConfig)
    # Target
    target_shape: PointerProperty(type=BoneShapeConfig)
    finger_target_shape: PointerProperty(type=BoneShapeConfig)
    hand_target_shape: PointerProperty(type=BoneShapeConfig)
    foot_target_shape: PointerProperty(type=BoneShapeConfig)

    is_initialized: BoolProperty(default=False)

    def set_defaults(self, force=False):
        if self.is_initialized and not force:
            return

        #Basic
        self.root_shape.set("Root_0", "THEME04", loc=(0,0,0),rot=(90,0,0), scale=100)
        self.limbs_shape.set("Circle_0", "THEME03", loc=(0,0.15,0), rot=(90,0,0), scale=0.5)
        self.finger_shape.set("Circle_0", "THEME03", loc=(0,0.1,0), rot=(90,0,0), scale=1)
        self.twist_shape.set("Circle_0", "THEME15", loc=(0,0.05,0), rot=(90,0,0), scale=1)
        self.spine_shape.set("Roll_0", "THEME03", loc=(0,0.05,-0.1), rot=(-90,0,0), scale=2)
        self.joint_hand_shape.set("Ball_0", "THEME03", loc=(0,0,0), rot=(90,0,0), scale=1)
        self.joint_foot_shape.set("Ball_0", "THEME03", loc=(0,0,0), rot=(90,0,0), scale=0.5)
        self.clavicle_shape.set("Cube_0", "THEME03", loc=(0,0.7,0), rot=(0,0,0), scale=(0.2,0.6,0.2))
        self.metacarpal_shape.set("Cube_0", "THEME03", loc=(0,0.3,0), rot=(0,0,0), scale=(0.2,0.6,0.2))
        #Offset
        self.offset_head_shape.set("Circle_1", "THEME07", loc=(0,0.25,0), rot=(90,0,0), scale=0.3)
        self.offset_foot_shape.set("Circle_1", "THEME07", loc=(0, 0, 0), rot=(90, 45, 0), scale=1)
        #Gizmo
        self.gizmo_shape.set("Circle_1", "THEME05", loc=(0,0,0), rot=(90,0,0), scale=1)
        self.gizmo_roll_shape.set("Ball_0", "THEME05", loc=(0,0,0), rot=(0,0,0), scale=0.1)
        #Mechanic
        self.mechanic_shape.set("Circle_1", "THEME06", loc=(0,0,0), rot=(90,45,0), scale=1)
        #Control
        self.pelvis_control_shape.set("Pelvis_0", "THEME09", loc=(0,0,0), rot=(-90,0,0), scale=15)
        self.clavicle_control_shape.set("Clavicle_0", "THEME09", loc=(0,0.1,0.05), rot=(90,0,0), scale=1)
        self.head_control_shape.set("Cross_0", "THEME09", loc=(0,0.25,0), rot=(-90,0,0), scale=0.5)
        self.foot_control_shape.set("Cross_0", "THEME09", loc=(0,0.2,0), rot=(-90,0,0), scale=0.7)
        self.ball_control_shape.set("Circle_1", "THEME09", loc=(-0.02,0,0), rot=(0,90,0), scale=1)
        self.hand_control_shape.set("Paddle_0", "THEME09", loc=(0,0.03,0.01), rot=(90,0,90), scale=1.5)
        #Target
        self.target_shape.set("Ball_0", "THEME01", loc=(0,0,0), rot=(0,0,0), scale=1)
        self.finger_target_shape.set("Circle_2","THEME01", rot=(-90,0,0), scale=0.7)
        self.hand_target_shape.set("Circle_1", "THEME01", rot=(-90,0,0), scale=1.5)
        self.foot_target_shape.set("Heel_0", "THEME01", rot=(90,0,0), scale=1)

        self.is_initialized = True

class WRYC_OT_ResetGeneralDefaults(bpy.types.Operator):
    bl_idname = "wryc.reset_general_defaults"
    bl_label = "Reset General Defaults"
    bl_description = "Reset all bone shapes to original addon defaults"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        AddonFunctions.get_preferences().general.set_defaults(force=True)
        return {'FINISHED'}

class WRYCAddonPreferences(AddonPreferences):
    bl_idname = __addon_name__
    addon_file = os.path.dirname(__file__)
    prefix: PointerProperty(type=BonePrefix)
    general: PointerProperty(type=GeneralBoneDisplaySettings)

    bone_shape_folder: StringProperty(
        name="Bone Shape Folder",
        subtype='DIR_PATH',
        default=os.path.join(os.path.dirname(__file__), "..", "assets"),
    )

    def draw_shape_config(self, box, config, label_text):
        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(config, "show_advanced", text="", icon='TRIA_DOWN' if config.show_advanced else "TRIA_RIGHT", emboss=False)
        row.label(text=label_text)

        if config.show_advanced:
            row = col.column(align=True)
            row.prop(config, "shape")
            row.prop(config, "color")
            row.prop(config, "loc")
            row.prop(config, "rot")
            row.prop(config, "scale")

    #__UI__
    def draw(self, context: bpy.types.Context):
        if not self.general.is_initialized:
            self.general.set_defaults()

        layout = self.layout
        layout.prop(self, "bone_shape_folder",text="Bone Shape Folder")

        layout = self.layout
        layout.label(text="Generated Bones' Prefix")
        box = layout.box()
        box.prop(self.prefix, "deform_prefix", text="Deform")
        box.prop(self.prefix, "offset_prefix", text="Offset")
        box.prop(self.prefix, "gizmo_prefix", text="Gizmo")
        box.prop(self.prefix, "mechanic_prefix", text="Mechanic")
        box.prop(self.prefix, "control_prefix", text="Control")
        box.prop(self.prefix, "target_prefix", text="Target")
        box.prop(self.prefix, "roll_prefix", text="Roll")
        box.prop(self.prefix, "track_prefix", text="Track")

        layout = self.layout
        layout.label(text="General Bone Display Settings")
        row = layout.row()
        row.operator("wryc.reset_general_defaults")

        #Basic
        box = layout.box()
        row = box.row(align=True)
        row.prop(self.general, "show_basic", text="", icon='TRIA_DOWN' if self.general.show_basic else "TRIA_RIGHT",emboss=False)
        row.label(text="Basic")
        if self.general.show_basic:
            self.draw_shape_config(box, self.general.root_shape, "Root Bone Shape")
            self.draw_shape_config(box, self.general.limbs_shape, "Limbs Bone Shape")
            self.draw_shape_config(box, self.general.finger_shape, "Finger Bone Shape")
            self.draw_shape_config(box, self.general.twist_shape, "Twist Bone Shape")
            self.draw_shape_config(box, self.general.spine_shape, "Spine Bone Shape")
            self.draw_shape_config(box, self.general.joint_hand_shape, "Joint hand Shape")
            self.draw_shape_config(box, self.general.joint_foot_shape, "Joint foot Shape")
            self.draw_shape_config(box, self.general.clavicle_shape, "Clavicle Bone Shape")
            self.draw_shape_config(box, self.general.metacarpal_shape, "Metacarpal Bone Shape")

        #Offset
        box = layout.box()
        row = box.row(align=True)
        row.prop(self.general, "show_offset", text="", icon='TRIA_DOWN' if self.general.show_offset else "TRIA_RIGHT", emboss=False)
        row.label(text="Offset")
        if self.general.show_offset:
            self.draw_shape_config(box, self.general.offset_head_shape, "Offset Head Bone Shape")
            self.draw_shape_config(box, self.general.offset_foot_shape, "Offset Foot Bone Shape")

        #Gizmo
        box = layout.box()
        row = box.row(align=True)
        row.prop(self.general, "show_gizmo", text="", icon='TRIA_DOWN' if self.general.show_gizmo else "TRIA_RIGHT", emboss=False)
        row.label(text="Gizmo")
        if self.general.show_gizmo:
            self.draw_shape_config(box, self.general.gizmo_shape, "Gizmo Bone Shape")
            self.draw_shape_config(box, self.general.gizmo_roll_shape, "Gizmo Roll Bone Shape")

        # Mechanic
        box = layout.box()
        row = box.row(align=True)
        row.prop(self.general, "show_mechanic", text="", icon='TRIA_DOWN' if self.general.show_mechanic else "TRIA_RIGHT", emboss=False)
        row.label(text="Mechanic")
        if self.general.show_mechanic:
            self.draw_shape_config(box, self.general.mechanic_shape, "Mechanic Bone Shape")

        #Control
        box = layout.box()
        row = box.row(align=True)
        row.prop(self.general, "show_control", text="", icon='TRIA_DOWN' if self.general.show_control else "TRIA_RIGHT", emboss=False)
        row.label(text="Control")
        if self.general.show_control:
            self.draw_shape_config(box, self.general.pelvis_control_shape, "Pelvis Control Bone Shape")
            self.draw_shape_config(box, self.general.clavicle_control_shape, "Clavicle Control Bone Shape")
            self.draw_shape_config(box, self.general.head_control_shape, "Head Control Bone Shape")
            self.draw_shape_config(box, self.general.foot_control_shape, "Foot Control Bone Shape")
            self.draw_shape_config(box, self.general.ball_control_shape, "Ball Control Bone Shape")
            self.draw_shape_config(box, self.general.hand_control_shape, "Hand Control Bone Shape")

        #Target
        box = layout.box()
        row = box.row(align=True)
        row.prop(self.general, "show_target", text="", icon='TRIA_DOWN' if self.general.show_target else "TRIA_RIGHT", emboss=False)
        row.label(text="Target")

        if self.general.show_target:
            self.draw_shape_config(box, self.general.target_shape, "Target Bone Shape")
            self.draw_shape_config(box, self.general.finger_target_shape, "Finger Target Bone Shape")
            self.draw_shape_config(box, self.general.hand_target_shape, "Hand Target Bone Shape")
            self.draw_shape_config(box, self.general.foot_target_shape, "Foot Target Bone Shape")