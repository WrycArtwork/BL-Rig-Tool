import bpy

from .config import __addon_name__
from .functions.AddonFunctions import load_icon_preview
from .i18n.dictionary import dictionary
from .properties.AddonProperties import BoneDisplaySettings, BoneShapesLibrary, RenameTool
from ...common.class_loader import auto_load
from ...common.class_loader.auto_load import add_properties, remove_properties
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary

bl_info = {
    "name": "BL Rig Tool",
    "author": "WRYC",
    "blender": (4, 0, 2),
    "version": (0, 0, 1),
    "description": "Rig tool for Blender",
    "doc_url": "[documentation url]",
    "support": "COMMUNITY",
    "category": "Rigging"
}

_addon_properties = {
     bpy.types.Scene: {
         "bone_display_settings": bpy.props.PointerProperty(type=BoneDisplaySettings),
         "rename_tool": bpy.props.PointerProperty(type=RenameTool),
     },
     bpy.types.WindowManager: {
         "bone_shapes_library": bpy.props.PointerProperty(type=BoneShapesLibrary),
     }
 }

def register():
    # Register classes
    auto_load.init()
    auto_load.register()
    add_properties(_addon_properties)

    bpy.app.handlers.load_post.append(load_icon_preview())

    # Internationalization
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)

    print("{} addon is installed.".format(__addon_name__))


def unregister():
    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    # unRegister classes
    auto_load.unregister()
    remove_properties(_addon_properties)
    print("{} addon is uninstalled.".format(__addon_name__))
