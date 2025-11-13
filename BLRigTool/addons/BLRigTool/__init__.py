import bpy

from .config import __addon_name__
from .functions.AddonFunctions import load_icon_preview
from .i18n.dictionary import dictionary
from .properties.AddonProperties import BoneDisplaySettings, BoneShapesLibrary, RenameTool, BoneMappingSettings, \
    ExportToUnreal
from ...common.class_loader import auto_load
from ...common.class_loader.auto_load import add_properties, remove_properties
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary

bl_info = {
    "name": "BL Rig Tool",
    "author": "WRYC",
    "blender": (4, 0, 2),
    "version": (0, 0, 4),
    "description": "Rig tool for Blender. include Custom Display Shape, Generate Constraint(Exp), Rename Tool, Export to Unreal",
    "doc_url": "https://github.com/WrycArtwork/BL-Rig-Tool",
    "category": "Rigging"
}

_addon_properties = {
     bpy.types.Scene: {
         "bone_display_settings": bpy.props.PointerProperty(type=BoneDisplaySettings),
         "rename_tool": bpy.props.PointerProperty(type=RenameTool),
         "bone_mapping_settings": bpy.props.PointerProperty(type=BoneMappingSettings),
         "export_to_unreal": bpy.props.PointerProperty(type=ExportToUnreal),
     },
     bpy.types.WindowManager: {
         "bone_shapes_library": bpy.props.PointerProperty(type=BoneShapesLibrary),
     }
 }

def menu_func_export_ue(self, context):
    self.layout.operator("wryc.ot_export_to_unreal", text="BL Export to Unreal")

def register():
    # Register classes
    auto_load.init()
    auto_load.register()
    add_properties(_addon_properties)
    #Load bone Shape Icon
    bpy.app.handlers.load_post.append(load_icon_preview())
    #ExportToUnreal
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export_ue)
    # Internationalization
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)

    print("{} addon is installed.".format(__addon_name__))


def unregister():
    # ExportToUnreal
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export_ue)
    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    # unRegister classes
    auto_load.unregister()
    remove_properties(_addon_properties)
    print("{} addon is uninstalled.".format(__addon_name__))
