bl_info = {
    "name": "Block Tools",
	"description": "Tools to construct in-game blocks for the game Space Engineers",
	"author": "Harag",
	"version": (0, 3, 1),
    "blender": (2, 72, 0),
	"location": "Properties > Scene | Material | Empty , Tools > Create",
	"wiki_url": "https://github.com/harag-on-steam/se-blender/wiki",
	"tracker_url": "https://github.com/harag-on-steam/se-blender/issues",
    "category": "Space Engineers",
}

# properly handle Blender F8 reload

modules = locals()

def reload(module_name):
    import importlib
    try:
        importlib.reload(modules[module_name])
        return True
    except KeyError:
        return False

if not reload('utils'): from . import utils
if not reload('types'): from . import types
if not reload('mount_points'): from . import mount_points
if not reload('mwmbuilder'): from . import mwmbuilder
if not reload('fbx'): from . import fbx
if not reload('havok_options'): from . import havok_options
if not reload('merge_xml'): from . import merge_xml
if not reload('export'): from . import export

del modules

# register data & UI classes

import bpy

class TestOperator(bpy.types.Operator):
    bl_idname = 'object.testmodule' 
    bl_label = 'Test: Export current scene to .fbx'
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        import os
        import tempfile

        print(tempfile.gettempdir())
        testfile = os.path.join(tempfile.gettempdir(), 'test.fbx')

        fbx.save_single(
            self, 
            context.scene, 
            filepath=testfile, 
            context_objects = context.scene.objects, # context.selected_objects,
            object_types = {'EMPTY', 'MESH'},

        )
        
        self.report({'INFO'}, 'Exported scene to %s' % (testfile))
        
        return {'FINISHED'}

class SEView3DToolsPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Create"
    bl_context = "objectmode"
    bl_label = "Space Engineers"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)

        space = context.space_data
        if space.grid_scale != 1.25 or space.grid_subdivisions != 5:
            col.operator(mount_points.SetupGrid.bl_idname, icon='GRID')

        col.operator(mount_points.AddMountPointSkeleton.bl_idname, icon='FACESEL')

def register():
    from bpy.utils import register_class
    
    register_class(types.SEAddonPreferences)
    register_class(types.SESceneProperties)
    register_class(types.SEObjectProperties)
    register_class(types.SEMaterialProperties)
   
    bpy.types.Object.space_engineers = bpy.props.PointerProperty(type=types.SEObjectProperties)
    bpy.types.Scene.space_engineers = bpy.props.PointerProperty(type=types.SESceneProperties)
    bpy.types.Material.space_engineers = bpy.props.PointerProperty(type=types.SEMaterialProperties)
   
    register_class(types.DATA_PT_spceng_scene)
    register_class(types.DATA_PT_spceng_empty)
    register_class(types.DATA_PT_spceng_material)

    register_class(export.ExportSceneAsBlock)
    register_class(export.UpdateDefinitionsFromBlockScene)
    register_class(types.CheckVersionOnline)
    register_class(mount_points.AddMountPointSkeleton)
    register_class(mount_points.SetupGrid)

    register_class(SEView3DToolsPanel)

    mount_points.enable_draw_callback()


def unregister():
    from bpy.utils import unregister_class

    mount_points.disable_draw_callback()

    unregister_class(SEView3DToolsPanel)

    unregister_class(mount_points.SetupGrid)
    unregister_class(mount_points.AddMountPointSkeleton)
    unregister_class(types.CheckVersionOnline)
    unregister_class(export.UpdateDefinitionsFromBlockScene)
    unregister_class(export.ExportSceneAsBlock)

    unregister_class(types.DATA_PT_spceng_material)
    unregister_class(types.DATA_PT_spceng_empty)
    unregister_class(types.DATA_PT_spceng_scene)
    
    del bpy.types.Material.space_engineers
    del bpy.types.Object.space_engineers
    del bpy.types.Scene.space_engineers
    
    unregister_class(types.SEMaterialProperties)
    unregister_class(types.SEObjectProperties)
    unregister_class(types.SESceneProperties)
    unregister_class(types.SEAddonPreferences)

