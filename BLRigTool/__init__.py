from .addons.BLRigTool import register as addon_register, unregister as addon_unregister

bl_info = {
    "name": 'BL Rig Tool',
    "author": 'WRYC',
    "blender": (4, 0, 2),
    "version": (0, 0, 1),
    "description": 'Rig tool for Blender',
    "doc_url": '[documentation url]',
    "support": 'COMMUNITY',
    "category": 'Rigging'
}

def register():
    addon_register()

def unregister():
    addon_unregister()

    