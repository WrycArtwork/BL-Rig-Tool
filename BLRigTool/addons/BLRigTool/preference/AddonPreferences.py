import os

import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty
from bpy.types import AddonPreferences

from ..config import __addon_name__


class WRYCAddonPreferences(AddonPreferences):
    # this must match the add-on name (the folder name of the unzipped file)
    bl_idname = __addon_name__

    # https://docs.blender.org/api/current/bpy.props.html
    # The name can't be dynamically translated during blender programming running as they are defined
    # when the class is registered, i.e. we need to restart blender for the property name to be correctly translated.
    addon_file = os.path.dirname(__file__)
    default_assets_path = os.path.join(addon_file, "..", "assets")

    filepath: StringProperty(
        name="Assets Folder",
        default=default_assets_path,
        subtype='DIR_PATH',
    )

    def draw(self, context: bpy.types.Context):
        layout = self.layout
        layout.label(text="Add-on Preferences View")
        layout.prop(self, "filepath")
