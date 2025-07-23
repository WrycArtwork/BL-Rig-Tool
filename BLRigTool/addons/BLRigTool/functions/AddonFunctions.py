import math

import bpy
import os

import mathutils
from Cython.Compiler.Naming import self_cname

preview_collections = {}

def get_icon_folder():
    return os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets", "icons"))

def get_library_path():
    return os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets", "BoneShapesLibrary.blend"))

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

def get_selected_bones(context, self = None):
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