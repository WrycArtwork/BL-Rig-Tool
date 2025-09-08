import bpy
from bpy.props import EnumProperty, BoolProperty, FloatProperty, StringProperty, PointerProperty, CollectionProperty, IntProperty
from bpy.types import PropertyGroup
from ..functions import AddonFunctions

#__CUSTOM DISPLAY SHAPE__
class BoneShapesLibrary(PropertyGroup):

    bone_shape: EnumProperty(
        name="Bone Shape",
        items=AddonFunctions.get_bone_shapes_library
    )

    finger_bone_shape: EnumProperty(
        name="Finger Bone Shape",
        items=AddonFunctions.get_bone_shapes_library,
    )

    arm_elbow_shape: EnumProperty(
        name="Arm Elbow Shape",
        items=AddonFunctions.get_bone_shapes_library,
    )

    arm_hand_shape: EnumProperty(
        name="Arm Hand Shape",
        items=AddonFunctions.get_bone_shapes_library,
    )

    leg_knee_shape: EnumProperty(
        name="Leg Knee Shape",
        items=AddonFunctions.get_bone_shapes_library,
    )

    leg_ankle_shape: EnumProperty(
        name="Leg Foot Shape",
        items=AddonFunctions.get_bone_shapes_library,
    )

    leg_offset_shape: EnumProperty(
        name="Leg Offset Shape",
        items=AddonFunctions.get_bone_shapes_library,
    )

    foot_ankle_shape: EnumProperty(
        name="Foot Ankle Shape",
        items=AddonFunctions.get_bone_shapes_library,
    )

    foot_heel_shape: EnumProperty(
        name="Foot Heel Shape",
        items=AddonFunctions.get_bone_shapes_library,
    )

    foot_ball_shape: EnumProperty(
        name="Foot Ball Shape",
        items=AddonFunctions.get_bone_shapes_library,
    )

    foot_roll_shape: EnumProperty(
        name="Foot Roll Shape",
        items=AddonFunctions.get_bone_shapes_library,
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

#__GENERATE CONSTRAINTS__

#__RENAME TOOL__
class BoneMapItems(PropertyGroup):
    source: StringProperty(name="Source Bone")
    target: StringProperty(name="Target Bone")

class ActionEntry(PropertyGroup):
    name: StringProperty()
    enabled: BoolProperty(default=False)

class BoneMappingSettings(PropertyGroup):
    show_mappings_settings: BoolProperty(default=True)

    mapping_actions: CollectionProperty(type=ActionEntry)

    source_type: EnumProperty(
        name="Source Type",
        items=[
            ('ARMATURE', "Armature", ""),
            ('ACTION', "Action", ""),
        ],
        default='ARMATURE',
    )
    source_armature: PointerProperty(
        type=bpy.types.Armature,
    )
    source_action: PointerProperty(
        type=bpy.types.Action,
    )
    target_armature: PointerProperty(
        type=bpy.types.Armature,
    )
    target_import: StringProperty(
        name="Target Bone",
        default="",
        update=AddonFunctions.update_target_import,
        search=AddonFunctions.target_bone_items,
        search_options={'SUGGESTION'},
    )

    mappings: CollectionProperty(type=BoneMapItems)
    active_index: IntProperty(
        update=AddonFunctions.update_selected_target
    )
    lock_mappings: BoolProperty(default=False)

    last_path: StringProperty(
        name="Last Path",
        default="//bone_mappings.json",
        subtype='FILE_PATH',
    )
    def get_last_path(self):
        return bpy.path.abspath(self.last_path)

    def set_last_path(self, path):
        self.last_path = path

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

#__EXPORT TOOL__
class ExportToUnreal(PropertyGroup):
    #Mesh/Armature
    mesh_path: StringProperty(
        name="Mesh Path",
        subtype='DIR_PATH',
        default="//"
    )

    is_export_mesh: BoolProperty(
        name="Export Mesh",
        default=True
    )

    apply_modifiers: BoolProperty(
        name="Apply Modifiers",
        default=True
    )

    skeletal_prefix: StringProperty(
        name="Skeletal Prefix",
        default=""
    )

    '''static_prefix: StringProperty(
        name="Static Prefix",
        default=""
    )'''
    #Action
    action_path: StringProperty(
        name="Action Path",
        subtype='DIR_PATH',
        default="//"
    )

    export_type: EnumProperty(
        name="Export Type",
        items=[
            ('SELECTED',"Selected Action", "Selected Action"),
            ('BATCH', "Batch", "Batch"),
            ('ALL', "All Actions", "All Actions"),
        ],
        default='SELECTED'
    )

    is_add_start_end: BoolProperty(
        name="Add Start/End Keyframes",
        default=False
    )

    action_prefix: StringProperty(
        name="Action Prefix",
        default=""
    )
    #Advanced
    only_deform: BoolProperty(
        name="Only Deform Bones",
        default=True
    )

    add_leaf: BoolProperty(
        name="Add Leaf Bones",
        default=False
    )

    primary_bone_axis: EnumProperty(
        name="Primary Bone Axis",
        items=[
            ('X', "X", "X"),
            ('-X', "-X", "-X"),
            ('Y', "Y", "Y"),
            ('-Y', "-Y", "-Y"),
            ('Z', "Z", "Z"),
            ('-Z', "-Z", "-Z"),
        ],
        default='Y'
    )

    secondary_bone_axis: EnumProperty(
        name="Secondary Bone Axis",
        items=[
            ('X', "X", "X"),
            ('-X', "-X", "-X"),
            ('Y', "Y", "Y"),
            ('-Y', "-Y", "-Y"),
            ('Z', "Z", "Z"),
            ('-Z', "-Z", "-Z"),
        ],
        default='X'
    )

    axis_forward: EnumProperty(
        name="FBX Axis Forward",
        items=[
            ('X', "X", "X"),
            ('-X', "-X", "-X"),
            ('Y', "Y", "Y"),
            ('-Y', "-Y", "-Y"),
            ('Z', "Z", "Z"),
            ('-Z', "-Z", "-Z"),
        ],
        default='-Z'
    )

    axis_up: EnumProperty(
        name="FBX Axis Up",
        items=[
            ('X', "X", "X"),
            ('-X', "-X", "-X"),
            ('Y', "Y", "Y"),
            ('-Y', "-Y", "-Y"),
            ('Z', "Z", "Z"),
            ('-Z', "-Z", "-Z"),
        ],
        default='Y'
    )