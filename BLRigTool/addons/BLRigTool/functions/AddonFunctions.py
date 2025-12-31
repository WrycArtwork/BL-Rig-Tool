import difflib
import math
from typing import final

import bpy
import os
import mathutils

from ..config import __addon_name__

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
    path = get_preferences().bone_shape_folder
    return os.path.normpath(os.path.join(path, "icons"))

def get_library_path():
    path = get_preferences().bone_shape_folder
    return os.path.normpath(os.path.join(path, "BoneShapesLibrary.blend"))

def load_icon_preview():
    pcoll = bpy.utils.previews.new()
    icon_path = get_icon_folder()

    for filename in os.listdir(icon_path):
        if filename.lower().endswith(".png"):
            icon_name = os.path.splitext(filename)[0]
            pcoll.load(icon_name, os.path.join(icon_path, filename), 'IMAGE')

    preview_collections["custom_icons"] = pcoll

def unload_icon_preview():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

def generate_icon(self, context, distance, angle, keep_generated):
    blend_path = get_library_path()
    icon_path = get_icon_folder()
    os.makedirs(icon_path, exist_ok=True)

    selected_name = context.window_manager.bone_shapes_library.bone_shape
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
        else:
            return {'FINISHED'}

    self.report({'INFO'}, f"Saved icon: {icon_path}")
    load_icon_preview()
    return {'FINISHED'}

def remove_icon(self, context):
    selected_name = context.window_manager.bone_shapes_library.bone_shape

    if not selected_name or selected_name == "None":
        return {'CANCELLED'}
    icon_path = get_icon_folder()
    icon_file = os.path.join(icon_path, f"(selected_name).png")

    if os.path.exists(icon_file):
        os.remove(icon_file)
        self.report({'INFO'}, f"Removed icon: {icon_file}")
    else:
        self.report({'WARNING'}, f"Icon not found: {selected_name}, file path: {icon_file}")

    return {'FINISHED'}

def get_bone_shapes_library(self, context):
    blend_path = get_library_path()
    blend_path = os.path.abspath(blend_path)

    items = []

    if os.path.exists(blend_path):
        try:
            with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
                for index, obj_name in enumerate(data_from.objects):
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

#__GENERATE CONSTRAINT__
def apply_child_of_inverse(context, obj, pose_bone, constraint):
    arm = obj.data

    bpy.ops.pose.select_all(action='DESELECT')

    arm.bones.active = arm.bones[pose_bone.name]
    arm.bones[pose_bone.name].select = True

    bpy.ops.constraint.childof_set_inverse(
        constraint=constraint.name,
        owner='BONE'
    )
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

def ensure_target(obj, source_name, target_name, shape_name="None", parent_name=None, use_connect=None, position=None, length=0.0):
    arm = obj.data

    if hasattr(source_name, "name"):
        source_name = source_name.name
    if hasattr(target_name, "name"):
        target_name = target_name.name
    if hasattr(parent_name, "name"):
        parent_name = parent_name.name

    if target_name in arm.bones:
        return obj.pose.bones[target_name]

    bpy.ops.object.mode_set(mode='EDIT')
    eb_src = arm.edit_bones[source_name]
    new_bone = arm.edit_bones.new(target_name)

    src_vec = eb_src.tail - eb_src.head
    src_len = src_vec.length
    if src_len <= 1e-8:
        src_vec = mathutils.Vector((0, 0, 0))
        src_len = 1.0

    if position is not None:
        head = position
        use_len = (length if (length is not None and length > 1e-8) else src_len)
        dir_n = src_vec.normalized()
        tail = head + dir_n * use_len
    else:
        head = eb_src.head
        tail = eb_src.tail
    new_bone.head = head
    new_bone.tail = tail
    new_bone.roll = eb_src.roll
    new_bone.use_deform = False


    if parent_name is not None:
        if parent_name == "":
            new_bone.parent = None
            new_bone.use_connect = False
        else:
            new_bone.parent = arm.edit_bones[parent_name]
            new_bone.use_connect = bool(use_connect) if use_connect is not None else False
    else:
        new_bone.parent = eb_src.parent
        new_bone.use_connect = bool(use_connect) if use_connect is not None else eb_src.use_connect

    bpy.ops.object.mode_set(mode='POSE')
    pb_new = obj.pose.bones[target_name]

    if shape_name and shape_name != "None":
        blend_path = get_library_path()
        shape_obj = bpy.data.objects.get(shape_name)
        if not shape_obj:
            with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
                if shape_name in data_from.objects:
                    data_to.objects = [shape_name]
            shape_obj = bpy.data.objects.get(shape_name)
        if shape_obj:
            pb_new.custom_shape = shape_obj

    return pb_new

def ensure_foot_ob_bone(obj, source_name, target_name, shape_name="None", ):
    arm = obj.data

    if hasattr(source_name, "name"):
        source_name = source_name.name
    if hasattr(target_name, "name"):
        target_name = target_name.name

    if target_name in arm.bones:
        return obj.pose.bones[target_name]

    bpy.ops.object.mode_set(mode='EDIT')
    eb_src = arm.edit_bones[source_name]
    new_bone = arm.edit_bones.new(target_name)

    new_bone.head = eb_src.tail
    new_bone.roll = eb_src.roll
    new_bone.tail = mathutils.Vector((
        new_bone.head.x,
        new_bone.head.y,
        obj.location.z,
    ))
    new_bone.use_deform = False

    bpy.ops.object.mode_set(mode='POSE')
    pb_new = obj.pose.bones[target_name]

    if shape_name and shape_name != "None":
        blend_path = get_library_path()
        shape_obj = bpy.data.objects.get(shape_name)
        if not shape_obj:
            with bpy.data.libraries.load(blend_path, link=False) as (data_from, data_to):
                if shape_name in data_from.objects:
                    data_to.objects = [shape_name]
            shape_obj = bpy.data.objects.get(shape_name)
        if shape_obj:
            pb_new.custom_shape = shape_obj

    return pb_new

def compute_pole_position(obj, upper_name, lower_name, end_name, direction="X+", distance=0.5):
    pb_upper = obj.pose.bones[upper_name]
    pb_lower = obj.pose.bones[lower_name]
    pb_end = obj.pose.bones[end_name]

    u = obj.matrix_world @ pb_upper.head
    l = obj.matrix_world @ pb_lower.head
    e = obj.matrix_world @ pb_end.head

    axis_map = {
        "X+": pb_lower.x_axis,
        "X-": -pb_lower.x_axis,
        "Y+": pb_lower.y_axis,
        "Y-": -pb_lower.y_axis,
        "Z+": pb_lower.z_axis,
        "Z-": -pb_lower.z_axis,
    }

    if direction not in axis_map:
        direction = "X+"

    pole_dir_local = axis_map[direction].normalized()
    pole_dir_world = obj.matrix_world.to_3x3() @ pole_dir_local

    len = (e - u).length
    pole_pos = u + pole_dir_world * (len * distance)

    return pole_pos

def compute_pole_angle(obj, upper_name, end_name, pole_pos_world):
    upper = obj.pose.bones[upper_name]
    end = obj.pose.bones[end_name]

    upper_matrix = upper.bone.matrix_local
    upper_matrix_inv = upper_matrix.inverted()
    pole_local = upper_matrix_inv @ pole_pos_world
    head_local = upper_matrix_inv @ upper.head
    tail_local = upper_matrix_inv @ upper.tail
    end_tail_local = upper_matrix_inv @ end.tail

    pole_normal = (end_tail_local - head_local).cross(pole_local - head_local)
    bone_dir = (tail_local - head_local).normalized()

    projected_pole_axis = pole_normal.cross(tail_local - head_local)

    x_axis = mathutils.Vector((1, 0, 0))

    angle = x_axis.angle(projected_pole_axis)
    if x_axis.cross(projected_pole_axis).dot(bone_dir) > 0:
        angle = -angle

    return angle

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