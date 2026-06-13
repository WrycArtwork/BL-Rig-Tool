import bpy

#__BLENDER API COMPAT__
class Compat:
    @staticmethod
    def bone_selection(pb, select_state=True):
        version =  bpy.app.version
        if version >= (5,0,0): #Blender 5.0+
            pb.select = select_state
        else: #Blender 4.0+
            pb.bone.select = select_state

    @staticmethod
    def get_fcurve_collection(action):
        collection = []
        if not action:
            return []
        #Blender 4.0+
        if hasattr(action, 'fcurves') and len(action.fcurves) > 0:
            collection.append(action.fcurves)
        #Blender 5.0+
        if hasattr(action, 'bindings'):
            for b in action.bindings:
                collection.append(b.fcurves)
        return collection

    @staticmethod
    def render_engine_eevee():
        version = bpy.app.version
        if version >= (5, 0, 0):  # Blender 5.0+
            return 'BLENDER_EEVEE'
        else:  # Blender 4.0+
            return 'BLENDER_EEVEE_NEXT'