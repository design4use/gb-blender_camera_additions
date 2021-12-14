bl_info = {
    "name": "Camera Additions for View 3D",
    "author": "German Bauer (inspired by original code for camera_fit_view by Yashar JafarKhanpour, for cyclecameras by CoDEmanX)",
    "version": (0, 9),
    "blender": (2, 80, 0),
    "location": "View3D > View > Cameras",
    "category": "3D View",
    "description": "Add to Cameras menu: View → Camera, View → Add Camera, Camera → View, Previous Camera, Next Camera",
}


import bpy
from bpy.types import Operator


class VIEW3D_OT_camera_adds_view2cam(Operator):
    """Set camera to view/ add camera and set to view"""
    
    bl_idname = "view3d.camera_additions_view2cam"
    bl_label = "View → Camera"
    bl_options = {'UNDO'}

    addcam : bpy.props.BoolProperty(name="View → Add Camera",options = {'SKIP_SAVE'})
    
    @classmethod
    def poll(cls,context):
        return context.space_data.region_3d.view_perspective != 'CAMERA'

    def execute(self, context):
     
        if self.addcam:
            bpy.ops.object.camera_add()
        obj = context.object
        spd = context.space_data
        cam = context.scene.camera
        if obj and obj.type == 'CAMERA' and obj != cam:
            cam = context.scene.camera = obj
        if cam:
            bpy.ops.view3d.camera_to_view()
            cam.data.sensor_width = 72
            cam.data.lens = spd.lens
            cam.data.clip_start = spd.clip_start
            cam.data.clip_end = spd.clip_end
            spd.region_3d.view_camera_offset = [0, 0]
            spd.region_3d.view_camera_zoom = 29.0746

        return {'FINISHED'}

class VIEW3D_OT_camera_adds_cam2view(Operator):
    """Set view to current camera"""
    
    bl_idname = "view3d.camera_additions_cam2view"
    bl_label = "Camera → View"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls,context):
        return context.space_data.region_3d.view_perspective != 'CAMERA'

    def execute(self, context):
        cam = context.scene.camera
        if cam:
            cam.rotation_mode = "QUATERNION"
            mat = cam.rotation_quaternion.to_matrix().to_4x4()
            mat.translation = cam.location

            for area in bpy.context.screen.areas:
                if area.type == "VIEW_3D":
                    break

            r3d = area.spaces[0].region_3d
            r3d.view_matrix = mat.inverted()

        return {'FINISHED'}

class VIEW3D_OT_camera_adds_prevcam(Operator):
    """Cycle to previous camera"""
    
    bl_idname = "view3d.camera_additions_camprev"
    bl_label = "Previous Camera"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls,context):
        return context.space_data.region_3d.view_perspective == 'CAMERA'

    def execute(self, context):
           
        scene = context.scene
        a_cameras = [ob for ob in bpy.data.objects if ob.type == 'CAMERA']
        if len(a_cameras) == 0:
            return {'CANCELLED'}
        try:
            ci = a_cameras.index(scene.camera)
            ci = (ci - 1) % len(a_cameras)
        except ValueError:
            ci = 0
        context.scene.camera = a_cameras[ci]

        return {'FINISHED'}

class VIEW3D_OT_camera_adds_nextcam(Operator):
    """Cycle to next camera"""
    
    bl_idname = "view3d.camera_additions_camnext"
    bl_label = "Next Camera"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls,context):
        return context.space_data.region_3d.view_perspective == 'CAMERA'

    def execute(self, context):
           
        scene = context.scene
        a_cameras = [ob for ob in bpy.data.objects if ob.type == 'CAMERA']
        if len(a_cameras) == 0:
            return {'CANCELLED'}
        try:
            ci = a_cameras.index(scene.camera)
            ci = (ci + 1) % len(a_cameras)
        except ValueError:
            ci = 0
        context.scene.camera = a_cameras[ci]

        return {'FINISHED'}

classes = [VIEW3D_OT_camera_adds_view2cam, VIEW3D_OT_camera_adds_cam2view, VIEW3D_OT_camera_adds_prevcam, VIEW3D_OT_camera_adds_nextcam]

def add_menu_items(self, context):
    self.layout.separator()
    self.layout.operator(VIEW3D_OT_camera_adds_view2cam.bl_idname,text="View → Camera")
    self.layout.operator(VIEW3D_OT_camera_adds_view2cam.bl_idname,text="View → Add Camera").addcam=True
    self.layout.separator()
    self.layout.operator(VIEW3D_OT_camera_adds_cam2view.bl_idname,text="Camera → View")
    self.layout.separator()
    self.layout.operator(VIEW3D_OT_camera_adds_prevcam.bl_idname,text="Previous Camera")
    self.layout.operator(VIEW3D_OT_camera_adds_nextcam.bl_idname,text="Next Camera")

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_view_cameras.append(add_menu_items)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    bpy.types.VIEW3D_MT_view_cameras.remove(add_menu_items)


if __name__ == "__main__":
    register()
