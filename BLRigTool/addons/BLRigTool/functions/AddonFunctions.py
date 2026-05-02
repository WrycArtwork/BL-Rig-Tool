import difflib
import math
from email.policy import default

import bpy
import os
import mathutils

from bpy.utils import previews
from numpy.lib.utils import source
from numpy.matrixlib.defmatrix import matrix

from ..config import __addon_name__
from ..utils import AddonUtils


def get_preferences():
    return bpy.context.preferences.addons[__addon_name__].preferences

def get_selected_bones(context, self):
    pbone = context.selected_pose_bones

    if not pbone:
        if self:
            self.report({'ERROR'}, "No selected Bones")
        return None
    return pbone

def check_pose_mode(context, self):
    arm_obj = context.object

    if arm_obj is None:
        self.report({'WARNING'}, "Please select an Object")
        return False

    if arm_obj.type != 'ARMATURE' or context.mode != 'POSE':
        self.report({'WARNING'}, "Please select an Armature Object and into Pose Mode")
        return False

    return True

def sort_actions(collection):
    #class is AddonProperties.ActionEntry
    data = [{"name": item.name, "enabled": getattr(item, "enabled", False)} for item in collection]
    sorted_data = sorted(data, key=lambda x: x["name"].lower())

    collection.clear()
    for entry in sorted_data:
        item = collection.add()
        item.name = entry["name"]
        item.enabled = entry["enabled"]

#__CUSTOM DISPLAY SHAPE__
preview_collections = {}
def get_icon_folder():
    path = get_preferences().assets_folder
    return os.path.normpath(os.path.join(path, "icons"))

def get_library_path():
    path = get_preferences().assets_folder
    return os.path.normpath(os.path.join(path, "BoneShapesLibrary.blend"))

def load_icon_preview():
    pcoll = previews.new()
    icon_path = get_icon_folder()

    for filename in os.listdir(icon_path):
        if filename.lower().endswith(".png"):
            icon_name = os.path.splitext(filename)[0]
            pcoll.load(icon_name, os.path.join(icon_path, filename), 'IMAGE')

    preview_collections["custom_icons"] = pcoll

def unload_icon_preview():
    for pcoll in preview_collections.values():
        previews.remove(pcoll)
    preview_collections.clear()

def generate_icon(self, context, distance, angle, keep_generated):
    blend_path = get_library_path()
    icon_path = get_icon_folder()
    os.makedirs(icon_path, exist_ok=True)

    selected_name = context.scene.bone_display_settings.bone_shape
    if not selected_name or selected_name == "None":
        self.report({'INFO'}, f"Bone Shape {blend_path} not found")
        return {'CANCELLED'}

    obj = bpy.data.objects.get(selected_name)
    if obj is None:
        with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
            if selected_name not in data_from.objects:
                self.report({'INFO'}, f"Object '{selected_name}' not found in library file")
                return {'CANCELLED'}
            data_to.objects = [selected_name]

        obj = bpy.data.objects.get(selected_name)
        if obj is None:
            self.report({'ERROR'}, f"Failed to load object '{selected_name}' from library file")
            return {'CANCELLED'}
        elif obj.type == 'CURVE':
            curve_data = obj.data
            curve_data.bevel_depth = 0.03
        elif obj.type == 'MESH':
            soli_mod = obj.modifiers.new(name="TempSolidify", type='SOLIDIFY')
            soli_mod.thickness = 0.02

        context.collection.objects.link(obj)

    else:
        if obj.name not in context.scene.objects:
            context.scene.objects.link(obj)

    context.view_layer.update()

    icon_file = os.path.join(icon_path, f"{obj.name}.png")
    scene = bpy.context.scene

    original_filepath = scene.render.filepath
    original_engine = scene.render.engine
    original_transparent = scene.render.film_transparent
    original_res_x = scene.render.resolution_x
    original_res_y = scene.render.resolution_y

    original_camera = scene.camera

    scene.render.filepath = icon_file
    scene.render.engine = 'BLENDER_EEVEE_NEXT'
    scene.render.film_transparent = True
    scene.render.resolution_x = 128
    scene.render.resolution_y = 128

    cam_name = f"{obj.name}_TempIconCam"

    cam_obj = bpy.data.objects.get(cam_name)
    if not cam_obj:
        cam_data = bpy.data.cameras.new(name=cam_name)
        cam_obj = bpy.data.objects.new(name=cam_name, object_data=cam_data)
        scene.collection.objects.link(cam_obj)
        cam_location = obj.location.copy()
        cam_offset = mathutils.Vector((0, 0, max(obj.dimensions.z, 1) * distance))

        if angle == "DIAGONAL":
            cam_offset = mathutils.Vector((1, -1, 1)).normalized() * obj.dimensions.length * distance
            cam_obj.rotation_euler = (math.radians(50), 0, math.radians(45))
        else:
            cam_obj.rotation_euler = (math.radians(0), 0, 0)

        cam_obj.location = cam_location + cam_offset
    scene.camera = cam_obj

    light_name = f"{obj.name}_TempIconLight"

    light_obj = bpy.data.objects.get(light_name)
    if not light_obj:
        light_data = bpy.data.lights.new(name=light_name, type='SUN')
        light_obj = bpy.data.objects.new(name=light_name, object_data=light_data)
        scene.collection.objects.link(light_obj)
        light_obj.location = cam_obj.location + mathutils.Vector((0, 0, 2))

    hidden = {}
    keep_names = {obj.name, cam_obj.name, light_obj.name}

    for hidden_obj in scene.objects:
        hidden[hidden_obj.name] = hidden_obj.hide_render
        hidden_obj.hide_render = (hidden_obj.name not in keep_names)

    try:
        bpy.ops.render.render(write_still=True)
    except Exception as e:
        self.report({'ERROR'}, f"Render Failed: {e}")
        return {'CANCELLED'}
    finally:
        for name, was_hidden in hidden.items():
            if name in scene.objects:
                scene.objects[name].hide_render = was_hidden

        scene.render.filepath = original_filepath
        scene.render.engine = original_engine
        scene.render.film_transparent = original_transparent
        scene.render.resolution_x = original_res_x
        scene.render.resolution_y = original_res_y
        scene.camera = original_camera

        if not keep_generated:
            cam_data_name = cam_obj.data.name if cam_obj else None
            light_data_name = light_obj.data.name if light_obj else None


            if cam_obj and cam_obj.name in bpy.data.objects:
                bpy.data.objects.remove(cam_obj, do_unlink=True)
            if cam_data_name and cam_data_name in bpy.data.cameras:
                bpy.data.cameras.remove(bpy.data.cameras[cam_data_name], do_unlink=True)

            if light_obj and light_obj.name in bpy.data.objects:
                bpy.data.objects.remove(light_obj, do_unlink=True)
            if light_data_name and light_data_name in bpy.data.lights:
                bpy.data.lights.remove(bpy.data.lights[light_data_name], do_unlink=True)

            if obj.name in scene.objects:
                bpy.data.objects.remove(obj, do_unlink=True)

    self.report({'INFO'}, f"Saved icon: {icon_path}")
    load_icon_preview()
    return {'FINISHED'}

def remove_icon(self, context):
    selected_name = context.scene.bone_display_settings.bone_shape

    if not selected_name or selected_name == "None":
        return {'CANCELLED'}
    icon_path = get_icon_folder()
    icon_file = os.path.join(icon_path, f"{selected_name}.png")

    if os.path.exists(icon_file):
        os.remove(icon_file)
        self.report({'INFO'}, f"Removed icon: {icon_file}")
    else:
        self.report({'WARNING'}, f"Icon not found: {selected_name}, file path: {icon_file}")

    return {'FINISHED'}

def get_bone_shapes_library(self, context):
    blend_path = os.path.abspath(get_library_path())

    current_filepath = os.path.abspath(bpy.data.filepath)

    items = []

    if os.path.exists(blend_path):
        try:
            object_names = []
            if blend_path == current_filepath:
                object_names = [obj.name for obj in bpy.data.objects]
            else:
                with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
                    object_names = [name for name in data_from.objects if name]

            for index, obj_name in enumerate(object_names):
                if obj_name is None or obj_name.strip() == "":
                    continue

                icon_coll = preview_collections.get("custom_icons", {})
                icon_id = 'ERROR'

                if icon_coll:
                    icon = icon_coll.get(obj_name)
                    if icon and hasattr(icon, "icon_id"):
                        icon_id = icon.icon_id

                items.append((obj_name, obj_name, "Bone Shape Object", icon_id, index))

            items.sort(key=lambda x: x[1])
        except Exception as e:
            items.append(("None", "None", f"Error loading: {e}", 'ERROR', 0))
    else:
        print("Blend file not found")
        items.append(("None", "None", "No library file found", 'ERROR', 0))

    return items

def bone_color_items(self, context):
    palette_prop = bpy.types.BoneColor.bl_rna.properties["palette"]

    items = []
    for i, e in enumerate(palette_prop.enum_items):
        icon = 'NONE'

        if e.identifier.startswith("THEME"):
            num = e.identifier[-2:]
            icon = f'COLORSET_{num}_VEC'
        elif e.identifier == 'CUSTOM':
            icon = 'COLORSET_CUSTOM_VEC'

        items.append((
            e.identifier,
            e.name,
            e.description,
            icon,
            i
        ))

    return items

#__GENERATE CONSTRAINT__
def get_or_create_collection(arm, collection_name):
    name = str(collection_name)
    stack = list(arm.collections)
    while stack:
        coll = stack.pop()
        if coll.name == name:
            return coll
        stack.extend(coll.children)
    return arm.collections.new(name)

def apply_child_of_inverse(context, obj, pose_bone, constraint):
    bpy.ops.pose.select_all(action='DESELECT')

    obj.data.bones.active = pose_bone.bone
    AddonUtils.Compat.bone_selection(pose_bone, True)

    bpy.ops.constraint.childof_set_inverse(
        constraint=constraint.name,
        owner='BONE'
    )

def create_deform_bone(obj, target_pb, matrix_pb, def_bone_name, mapping, relation='head', parent_name=""):
    arm = obj.data

    bone_head_pos = matrix_pb.head.copy() if relation == 'head' else matrix_pb.tail.copy()
    bone_length = target_pb.length

    local_matrix = matrix_pb.matrix.to_3x3()
    bl_axes_vecs = {
        'X': local_matrix.col[0],
        'Y': local_matrix.col[1],
        'Z': local_matrix.col[2],
    }

    ue_axes = {}
    for bl_axis, ue_axis_raw in mapping.items():
        sign = -1.0 if ue_axis_raw.startswith('-') else 1.0
        axis_letter = ue_axis_raw.lstrip('-')
        ue_axes[axis_letter] = bl_axes_vecs[bl_axis] * sign

    target_rot_matrix = mathutils.Matrix((
        ue_axes['X'],
        ue_axes['Y'],
        ue_axes['Z']
    )).transposed()

    direction = target_rot_matrix.col[1].normalized()
    bone_tail_pos = bone_head_pos + direction * bone_length

    if def_bone_name in arm.edit_bones:
        arm.edit_bones.remove(arm.edit_bones[def_bone_name])

    new_bone = arm.edit_bones.new(name=def_bone_name)
    new_bone.head = bone_head_pos
    new_bone.tail = bone_tail_pos

    new_bone.matrix = mathutils.Matrix.LocRotScale(bone_head_pos, target_rot_matrix, None)
    new_bone.length = bone_length

    new_bone.use_connect = False
    if parent_name and parent_name in arm.edit_bones:
        new_bone.parent = arm.edit_bones[parent_name]

    created_bone_name = new_bone.name

    return created_bone_name

def get_or_create_constraint(pb, prefix, ctype):
    con = None
    for existing in pb.constraints:
        if existing.name.startswith(prefix) and existing.type == ctype:
            con = existing
            break
    if con is None:
        con = pb.constraints.new(type=ctype)
        con.name = f"{prefix}{ctype.replace('_', ' ').title()}"
    return con

def apply_bone_shape_settings(pb, config=None, armature=None):
    #if config is not None:
    pref = get_preferences()
    settings = getattr(pref.general, config, None)

    shape_name = settings.shape
    blend_path = get_library_path()
    with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
        if shape_name in data_from.objects:
            data_to.objects = [shape_name]
    shape_obj = bpy.data.objects.get(shape_name)

    if shape_obj:
        pb.custom_shape = shape_obj
    if settings.color:
        armature.pose.bones[pb.name].color.palette = settings.color
    pb.custom_shape_translation = settings.loc
    pb.custom_shape_rotation_euler = settings.rot
    pb.custom_shape_scale_xyz = settings.scale

def ensure_target(obj, source_bone, target_bone, config=None, parent_bone=None, use_connect=None, position=None, length=0.1, mode="DEFAULT",ref_name=None):
    arm = obj.data

    source_name = source_bone.name if hasattr(source_bone, "name") else source_bone
    target_name = target_bone.name if hasattr(target_bone, "name") else target_bone
    parent_name = parent_bone if isinstance(parent_bone, str) else None

    if target_bone in arm.bones:
        return obj.pose.bones[target_bone]

    bpy.ops.object.mode_set(mode='EDIT')

    eb_src = arm.edit_bones.get(source_name)
    if not eb_src:
        bpy.ops.object.mode_set(mode='POSE')
        return None

    eb_ref = arm.edit_bones.get(ref_name) if ref_name else None
    new_bone = arm.edit_bones.new(target_name)

    if mode == "DEFAULT":
        new_bone.head = eb_src.head
        new_bone.tail = eb_src.tail
        new_bone.roll = eb_src.roll
    elif mode == "POLE_TARGET":
        if position is not None:
            local_pos = obj.matrix_world.inverted() @ position
            new_bone.head = local_pos
            new_bone.tail = local_pos + mathutils.Vector((0, 0, length))
            new_bone.roll = 0
        else:
            new_bone.head = eb_src.head
            new_bone.tail = eb_src.tail
            new_bone.roll = eb_src.roll
    elif mode == "FOOT_TO_FLOOR":
        new_bone.head = eb_src.tail
        new_bone.roll = eb_src.roll
        new_bone.tail = mathutils.Vector((
            new_bone.head.x,
            new_bone.head.y,
            obj.location.z,
        ))
    elif mode == "FOOT_UNDER_FLOOR":
        new_bone.head = eb_src.tail
        new_bone.tail = eb_src.tail + mathutils.Vector((0, 0, -length))
        new_bone.roll = eb_src.roll
    elif mode == "BALL_ROLL":
        mat = eb_src.matrix.to_3x3()
        local_x = mat.col[0].normalized()
        local_y = mat.col[1].normalized()
        local_z = mat.col[2].normalized()

        world_x = mathutils.Vector((1, 0, 0))
        if abs(local_x.dot(world_x)) >= abs(local_z.dot(world_x)):
            roll_axis_vec = local_x
        else:
            roll_axis_vec = local_z

        direction = -local_y
        direction.z = 0
        direction = direction.normalized()

        new_bone.head = eb_src.head
        new_bone.tail = eb_src.head + (direction * length)
        new_bone.align_roll(roll_axis_vec)
    elif mode == "FOOT_ROLL":
        direction = (eb_ref.head - eb_src.tail)
        direction.z = 0
        direction = direction.normalized()
        new_bone.head = eb_src.tail
        new_bone.tail = eb_src.tail + (direction * length)
        new_bone.roll = eb_ref.roll + math.pi
    elif mode == "FOOT_CONTROL":
        direction = (eb_src.tail - eb_ref.head)
        direction.z = 0
        direction = direction.normalized()
        new_bone.head = eb_src.tail
        new_bone.tail = eb_src.tail + (direction * length)
        new_bone.roll = eb_ref.roll
    elif mode == "CHAIN_TARGET":
        new_bone.head = eb_src.head + position
        new_bone.tail = new_bone.head + mathutils.Vector((0, 0, length))
        new_bone.roll = eb_src.roll
    elif mode == "CHAIN_GIZMO":
        new_bone.head = eb_src.head + position
        new_bone.tail = eb_src.tail + position
        new_bone.roll = eb_src.roll
    elif mode == "HEAD_TRACK":
        new_bone.head = eb_src.head
        new_bone.tail = eb_src.head + mathutils.Vector((0, -length, 0))
        new_bone.roll = eb_src.roll
    elif mode == "HEAD_TARGET":
        new_bone.head = eb_ref.tail
        new_bone.tail = new_bone.head + mathutils.Vector((0, 0, length))
        new_bone.roll = eb_src.roll

    new_bone.use_deform = False
    if parent_name == "":
        new_bone.parent = None
        new_bone.use_connect = False
    elif parent_name:
        new_bone.parent = arm.edit_bones[parent_name]
        new_bone.use_connect = bool(use_connect)
    else:
        new_bone.parent = None
        new_bone.use_connect = bool(use_connect)

    bpy.ops.object.mode_set(mode='POSE')
    pb_new = obj.pose.bones.get(target_bone)

    if pb_new and config:
        apply_bone_shape_settings(pb_new, config, obj)

    return pb_new

def compute_pole_position(obj, upper_name, lower_name, end_name, distance=0.3):
    pb_upper = obj.matrix_world @ obj.pose.bones[upper_name].head
    pb_lower = obj.matrix_world @ obj.pose.bones[lower_name].head
    pb_end = obj.matrix_world @ obj.pose.bones[end_name].head

    v_upper = pb_lower - pb_upper
    v_line = pb_end - pb_upper

    #projection
    proj = v_line.dot(v_upper) / v_line.dot(v_line)
    pb_proj = pb_upper + proj * v_line
    pole_dir = (pb_lower - pb_proj).normalized()

    if pole_dir.length < 0.0001:
        pole_dir = (obj.matrix_world.to_3x3() @ obj.pose.bones[lower_name].x_axis).normalized()

    pole_pos = pb_lower + pole_dir * distance

    return pole_pos

def compute_pole_angle(obj, upper_name, end_name, pole_pos_world):
    upper = obj.pose.bones[upper_name]
    end = obj.pose.bones[end_name]

    pole_pos_pose = obj.matrix_world.inverted() @ pole_pos_world
    upper_matrix_inv = upper.bone.matrix_local.inverted()
    pole_local = upper_matrix_inv @ pole_pos_pose
    head_local = upper_matrix_inv @ upper.head
    tail_local = upper_matrix_inv @ upper.tail
    end_tail_local = upper_matrix_inv @ end.head

    pole_normal = (end_tail_local - head_local).cross(pole_local - head_local)
    bone_dir = (tail_local - head_local).normalized()

    projected_pole_axis = pole_normal.cross(tail_local - head_local)

    x_axis = mathutils.Vector((1, 0, 0))

    angle = x_axis.angle(projected_pole_axis)
    if x_axis.cross(projected_pole_axis).dot(bone_dir) > 0:
        angle = -angle

    return angle

def detect_roll_axis(obj, toe_name):
    toe_bone = obj.data.bones.get(toe_name)
    world_x = mathutils.Vector((1, 0, 0))

    mat = toe_bone.matrix_local.to_3x3()
    local_axes = {
        'x' : mat.col[0].normalized(),
        'y' : mat.col[1].normalized(),
        'z' : mat.col[2].normalized(),
    }

    roll_axis = max(local_axes, key=lambda a: abs(local_axes[a].dot(world_x)))
    is_positive = local_axes[roll_axis].dot(world_x) > 0
    return roll_axis, is_positive

def collect_bone_chain(root_pbone):
    chain = []
    def recure(pb):
        chain.append(pb)
        for child in pb.children:
            recure(child)
    recure(root_pbone)
    return chain

#__RENAME TOOL__
def update_selected_target(self, context):
    if 0 <= self.active_index < len(self.mappings):
        self.target_import = self.mappings[self.active_index].target
    else:
        self.target_import = ""

def update_target_import(self, context):
    if 0 <= self.active_index < len(self.mappings):
        tgt_armature = self.target_armature
        bone_name = self.target_import.strip()

        if bone_name == "" or bone_name =="None":
            self.mappings[self.active_index].target = ""
        elif bone_name in tgt_armature.bones:
            self.mappings[self.active_index].target = bone_name
        else:
            print(f"Bone name:{bone_name}is not Valid")
            update_selected_target(self, context)

def target_bone_items(self, context, edit_text):
    arm = self.target_armature
    if not arm:
        return []

    if not edit_text.strip():
        return []

    tgt_names = [b.name for b in arm.bones]
    matches = difflib.get_close_matches(edit_text, tgt_names, n=5, cutoff=0.3)

    return [m for m in matches]