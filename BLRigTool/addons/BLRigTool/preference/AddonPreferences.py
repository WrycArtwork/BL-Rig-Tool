import os

import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import AddonPreferences

from ..config import __addon_name__

class WRYCAddonPreferences(AddonPreferences):
    # this must match the add-on name (the folder name of the unzipped file)
    bl_idname = __addon_name__
    addon_file = os.path.dirname(__file__)

    bone_shape_folder: StringProperty(
        name="Bone Shape Folder",
        subtype='DIR_PATH',
        default=os.path.join(os.path.dirname(__file__), "..", "assets"),
    )

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

    offset_prefix: StringProperty(
        name="Offset Prefix",
        default="OB_",
    )

    #__UI__
    def draw(self, context: bpy.types.Context):
        layout = self.layout
        layout.prop(self, "bone_shape_folder",text="Bone Shape Folder")

        layout = self.layout
        layout.label(text="Generated bones' prefix")
        layout.prop(self, "deform_prefix",text="Deform")
        layout.prop(self, "target_prefix", text="Target:")
        layout.prop(self, "control_prefix", text="Control:")
        layout.prop(self, "gizmo_prefix", text="Gizmo:")
        layout.prop(self, "offset_prefix", text="Offset:")
