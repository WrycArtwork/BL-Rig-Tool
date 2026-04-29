from .addons.BLRigTool import register as addon_register, unregister as addon_unregister

bl_info = {
    "name": 'BL Rig Tool',
    "author": 'WRYC',
    "blender": (4, 0, 2),
    "version": (0, 0, 6),
    "description": 'Rig tool for Blender. include Custom Display Shape, Generate Constraint(Exp), Rename Tool, Export to Unreal',
    "doc_url": 'https://github.com/WrycArtwork/BL-Rig-Tool',
    "category": 'Rigging'
}

def register():
    addon_register()

def unregister():
    addon_unregister()

    