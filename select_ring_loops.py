bl_info = {
    "name": "Select Ring Loops",
    "author": "Chromaspring",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "description": "Select edge loops from edge ring selection",
    "category": "Mesh",
}

import bpy
import bmesh

class MESH_OT_select_ring_loops(bpy.types.Operator):
    """Select edge loops from edge ring selection"""
    bl_idname = "mesh.select_ring_loops"
    bl_label = "Select Ring Loops"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.edit_object
        mesh = obj.data

        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "No mesh object in edit mode")
            return {'CANCELLED'}

        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(mesh)
        bm.edges.ensure_lookup_table()

        edges_to_process = [edge for edge in bm.edges if edge.select]
        originally_selected_edges = set(edges_to_process)

        bpy.ops.mesh.select_all(action='DESELECT')
        bm.select_flush(False)

        for edge in edges_to_process:
            edge.select = True
            bpy.ops.mesh.loop_multi_select(ring=False)
            edge.select = False

        for edge in originally_selected_edges:
            edge.select = True

        bmesh.update_edit_mesh(mesh)
        return {'FINISHED'}

def add_menu_item(self, context):
    self.layout.operator(MESH_OT_select_ring_loops.bl_idname)

def register():
    bpy.utils.register_class(MESH_OT_select_ring_loops)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(add_menu_item)

def unregister():
    bpy.utils.unregister_class(MESH_OT_select_ring_loops)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(add_menu_item)

if __name__ == "__main__":
    register()
