import bpy

from .config import __addon_name__
from .functions.AddonFunctions import load_icon_preview, get_preferences
from .i18n.dictionary import dictionary
from .properties.AddonProperties import BoneDisplaySettings, RenameTool, BoneMappingSettings, \
    DeformSettings
from ...common.class_loader import auto_load
from ...common.class_loader.auto_load import add_properties, remove_properties
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary

bl_info = {
    "name": "BL Rig Tool",
    "author": "WRYC",
    "blender": (4, 0, 2),
    "version": (0, 0, 7),
    "description": "Rig tool for Blender. include Custom Display Shape, Generate Constraint, Retarget Action, Rename Tool.",
    "doc_url": "https://github.com/WrycArtwork/BL-Rig-Tool",
    "category": "Rigging"
}

_addon_properties = {
     bpy.types.Scene: {
         "bone_display_settings": bpy.props.PointerProperty(type=BoneDisplaySettings),
         "rename_tool": bpy.props.PointerProperty(type=RenameTool),
         "bone_mapping_settings": bpy.props.PointerProperty(type=BoneMappingSettings),
         "deform_settings": bpy.props.PointerProperty(type=DeformSettings),
     },
 }


def init_pref_defaults():
    try:
        pref = get_preferences()
        if not pref.general.is_initialized:
            pref.general.set_defaults()
    except Exception:
        pass

def ue5_manny_add(self, context):
    print("UE5 Manny Add")
    layout = self.layout
    layout.separator()
    layout.menu("WRYC_MT_add_ue5_manny_menu", icon="ARMATURE_DATA")

def register():
    # Register classes
    auto_load.init()
    auto_load.register()
    add_properties(_addon_properties)
    #Load bone Shape Icon
    if load_icon_preview() not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(load_icon_preview())
    # Internationalization
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)
    #Register ue5 manny add menu
    bpy.types.VIEW3D_MT_armature_add.append(ue5_manny_add)
    #Register basic shape configs in preference
    bpy.app.timers.register(init_pref_defaults, first_interval=0.1)

    print("{} addon is installed.".format(__addon_name__))

def unregister():
    #Remove bone Shape Icon
    bpy.app.handlers.load_post.remove(load_icon_preview())
    # Remove ue5 manny add menu
    bpy.types.VIEW3D_MT_armature_add.remove(ue5_manny_add)
    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    # unRegister classes
    auto_load.unregister()
    remove_properties(_addon_properties)
    print("{} addon is uninstalled.".format(__addon_name__))