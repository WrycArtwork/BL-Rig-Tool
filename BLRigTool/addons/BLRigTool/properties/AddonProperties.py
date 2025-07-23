import bpy
from bpy.props import EnumProperty, BoolProperty, FloatProperty, StringProperty, PointerProperty, CollectionProperty, IntProperty
from bpy.types import PropertyGroup
from ..functions import AddonFunctions

class BoneShapesLibrary(PropertyGroup):

    bone_shape: EnumProperty(
        name="Bone Shape",
        items=AddonFunctions.get_bone_shapes_library
    )

class BoneDisplaySettings(PropertyGroup):

    scale_bone_length_enable: BoolProperty(
        name="Enable Scale Bone Length",
        default=True
    )

    scale_enable: BoolProperty(
        name="Enable Apply Scale All",
        default=True
    )

    scale: FloatProperty(name="Scale All", default=1.0)
    scale_x: FloatProperty(name="Scale x", default=1.0)
    scale_y: FloatProperty(name="Scale y", default=1.0)
    scale_z: FloatProperty(name="Scale z", default=1.0)
    loc_x: FloatProperty(name="Translate X", default=0.0)
    loc_y: FloatProperty(name="Translate Y", default=0.0)
    loc_z: FloatProperty(name="Translate Z", default=0.0)
    rot_x: FloatProperty(name="Rotate X", default=0.0)
    rot_y: FloatProperty(name="Rotate Y", default=0.0)
    rot_z: FloatProperty(name="Rotate Z", default=0.0)

class RenameTool(PropertyGroup):

    rename_target: EnumProperty(
        name="Target",
        items=[
            ('VERTEX_GROUP', "Vertex Group", "Vertex Group"),
            ('SHAPE_KEY', "Shape key", "Shape key"),
        ],
        default='VERTEX_GROUP',
    )

    rename_mode: EnumProperty(
        name="Rename Mode",
        items=[
            ('FIND_REPLACE', "Find/Replace", "Search and replace"),
            ('SET_PREFIX_SUFFIX', "Set Prefix Suffix", "Set Prefix/Suffix"),
            ('REMOVE_PREFIX_SUFFIX', "Remove Prefix/Suffix", "Remove Prefix/Suffix"),
        ],
        default='FIND_REPLACE',
    )
    find_str: StringProperty(name="Find", default="")
    replace_str: StringProperty(name="Replace", default="")
    prefix_str: StringProperty(name="Prefix", default="")
    suffix_str: StringProperty(name="Suffix", default="")