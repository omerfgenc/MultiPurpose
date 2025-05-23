bl_info = {
    'name': 'Multi Purpose New',
    'author': 'Yazılımcı Genç',
    'description': "Bismillah! Blender'da işlerimizi kolaylaştırmak amacıyla yazılmıştır.",
    'blender': (4, 4, 0),
    'version': (1, 2, 9),
    'location': 'View3D > Sidebar > mp',
    'warning': '',
    'wiki_url': "",
    'tracker_url': "",
    'category': 'Animation'
}

import bpy
from bpy.props import EnumProperty, StringProperty, PointerProperty
from bpy.types import Operator, Panel, PropertyGroup, Menu, Header
from bpy.utils import register_class, unregister_class
from bpy_extras.io_utils import ImportHelper
import os
import re
from pathlib import Path
from . import addon_updater_ops

############################ Link Operations ############################

class MP_PT_LinkOperations(Panel):
    bl_label = "Link"
    bl_idname = "mp.link_operations"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MP'

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2
        
        layout.operator("mp.find_file_paths", text="Dosyaları Bul", icon="FILE_FOLDER")
        
        layout.separator()
        
        layout.prop(context.scene, "link_tabs", expand=True)

        if context.scene.link_tabs == 'TAB1':
            layout.operator("mp.karakter_rigi", text="Karakter Rigi Aktif Et", icon="ARMATURE_DATA")
        elif context.scene.link_tabs == 'TAB2':
            layout.operator("mp.model_rigi", text="Model Rigi Aktif Et", icon="OBJECT_DATA")
        elif context.scene.link_tabs == 'TAB3':
            layout.operator("mp.relations_make", text="Shape Keys Aktif Et", icon="SHAPEKEY_DATA")

def find_file(folder_path, file_name):
    
    character_names = ["Aykut", "Büşra", "Cemile Teyze", "Dr. Arif Aydın", "Elif", "Emir", 
                        "Esma", "Fatih", "Halil", "Musab", "Ömer", "Orhan", "Yakup",
                        "Busra", "Omer", "Dr. Arif Aydin"]
    character_file_names = [str(i)+".blend" for i in character_names]
    
    for root, dirs, files in os.walk(folder_path):
        if file_name in character_file_names:
            if "Ana Karakterler" in root and file_name in files:
                return os.path.join(root, file_name)
        elif file_name in files:
            return os.path.join(root, file_name)
    return None

def get_desktop_path():
    return str(Path.home() / "Desktop")

class MP_OT_FindFilePaths(Operator):
    bl_idname = "mp.find_file_paths"
    bl_label = "Kayıp Dosyaları Bul"
    bl_options = {'REGISTER', 'UNDO'}

    directory: StringProperty(
        name="Directory",
        subtype='DIR_PATH'
    )

    def execute(self, context):
        folder_path = self.directory
        
        # if "Animasyon Kütüphanesi" not in folder_path:
        #     self.report({'WARNING'}, "Animasyon Kütüphanesi isimli klasörü seçiniz!")
        # else:
        for library in bpy.data.libraries:
            
            file_path = library.filepath
            file_name = os.path.basename(file_path)
            
            result = find_file(folder_path, file_name)
            
            if result:
                library.filepath = result
            else:
                print("Dosya bulunamadı.")
            
        if bpy.data.filepath:
            bpy.ops.wm.save_mainfile()
        else:
            
            new_file_path = os.path.join(get_desktop_path(), "animasyon_projesi_mp.blend")
            bpy.ops.wm.save_as_mainfile(filepath=new_file_path)
        
        bpy.ops.wm.revert_mainfile()
        
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class MP_OT_KarakterRigi(Operator):
    bl_idname = "mp.karakter_rigi"
    bl_label = "Karakter Rigi Aktif Et"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        try:
            bpy.ops.object.make_override_library()
        except:
            pass
        
        try:
            bpy.ops.object.make_local(type='SELECT_OBDATA_MATERIAL')
        except:
            try:
                bpy.ops.object.make_local(type='SELECT_OBDATA_MATERIAL')
            except:
                pass
            pass
    
        return {'FINISHED'}
    
class MP_OT_ModelRigi(Operator):
    bl_idname = "mp.model_rigi"
    bl_label = "Model Rigi Aktif Et"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        try:
            bpy.ops.object.make_override_library()
        except:
            pass
        
        try:
            bpy.ops.object.make_local(type='SELECT_OBDATA_MATERIAL')
        except:
            try:
                bpy.ops.object.make_local(type='SELECT_OBDATA_MATERIAL')
            except:
                pass
            pass
        
        return {'FINISHED'}
    
class MP_OT_RelationsMake(Operator):
    bl_idname = "mp.relations_make"
    bl_label = "Shape Keys Aktif Et"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.make_local(type='SELECT_OBDATA_MATERIAL')
        
        selected_objects = bpy.context.selected_objects
        for object in selected_objects:
            if object.type == "MESH":
                try:
                    bpy.data.objects[object.name].modifiers["Armature"].show_in_editmode = True
                    bpy.data.objects[object.name].modifiers["Armature"].show_on_cage = True
                except:
                    pass
                
        return {'FINISHED'}
    
############################ Animation Operations ############################

class MP_PT_AnimationOperations(Panel):
    bl_label = "Animasyon"
    bl_idname = "mp.animation_operations"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MP'

    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2
        
        layout.prop(context.scene, "animation_tabs", expand=True)

        if context.scene.animation_tabs == 'TAB1':
            row1 = layout.row()
            row1.operator("mp.walking_straight", text="", icon="ACTION")
            row1.menu("mp.action_menu", text="Action Seciniz")
            
        elif context.scene.animation_tabs == 'TAB2':
            row2 = layout.row()
            row2.operator("mp.create_path", text="Path Ekle", icon="OUTLINER_OB_CURVE")
            row2.operator("mp.break_path", text="Pathten Ayrıl", icon="FORCE_CURVE")
            
            row3 = layout.row()
            row3.operator("mp.walking_straight", text="", icon="ACTION")
            row3.menu("mp.action_menu", text="Action Seciniz")
            
        elif context.scene.animation_tabs == 'TAB3':
            layout.operator("mp.root_move", text="Root'u Karaktere Getir", icon="ORIENTATION_CURSOR")

character_actions = []
class MP_OT_WalkingStraight(Operator, ImportHelper):
    bl_idname = "mp.walking_straight"
    bl_label = "Düz Yürüme"
    
    filepath: StringProperty(subtype="FILE_PATH")

    def execute(self, context):
    
        global character_actions
        if len(character_actions) > 0:
            for act in character_actions:
                if act in bpy.data.actions:
                    bpy.data.actions.remove(bpy.data.actions[act])
        character_actions = []
        
        with bpy.data.libraries.load(self.filepath, link=False) as (data_from, data_to):
            for action in data_from.actions:
                if "Yurume Dongusu" in action:
                    data_to.actions.append(action)
                    character_actions.append(action)
                
        return {'FINISHED'}

def duz_yurume_uygula(act_name):
    
    anim_action_name = act_name
    if anim_action_name in bpy.data.actions:
        anim_action = bpy.data.actions[anim_action_name]
    
    current_frame = bpy.context.scene.frame_current
    obj = bpy.context.active_object

    if obj.type != "ARMATURE":
        return {'CANCELLED'}
    else:
        armature = obj.data
        
    for a in obj.data.bones:
        a.select = False
    
    if 'root' in obj.pose.bones:
        bone = obj.pose.bones['root']
    else:
        for bone in obj.pose.bones:
            if bone.name.startswith("root") and len(bone.name) > 4:
                bone = obj.pose.bones[bone.name]
                break
        else:
            return {'CANCELLED'}
        
    first_locations = bone.location[:]
    if len(bone.rotation_mode) == 3:
        first_rotations = bone.rotation_euler[:]
    elif bone.rotation_mode == "QUATERNION":
        first_rotations = bone.rotation_quaternion[:]
    first_scales = bone.scale[:]
        
    if obj.animation_data.action is not None:
        current_action = obj.animation_data.action
    else:
        actions_list = [i.name for i in bpy.data.actions]
        count = 1
        temp_name = "New Action"
        while temp_name in actions_list:
            temp_name = "New Action " + str(count)
            count += 1
        bpy.data.actions.new(name=temp_name)
        current_action = bpy.data.actions[temp_name]
        obj.animation_data.action = current_action
        
    obj.animation_data.action = anim_action
            
    armature.collections_all["Root"].is_visible = True
    bpy.ops.object.mode_set(mode='POSE')
    
    pose_bone = obj.pose.bones.get(bone.name)  
    bpy.ops.pose.select_all(action='DESELECT')
    obj.data.bones[bone.name].select = True
    obj.data.bones.active = obj.data.bones[bone.name]
    
    action = anim_action
    suitable_slots = [slot for slot in action.slots if slot.target_id_type == 'OBJECT']
    if len(suitable_slots) > 0:
        obj.animation_data.action_slot = suitable_slots[0]
    else:
        print("Slot Bulunamadi!")
    
    bpy.context.scene.frame_set(1)
    loc_y_1 = obj.pose.bones["foot_ik.L"].location[1]
    loc_y_1 = abs(round(loc_y_1, 6))
    
    last_frame = max([keyframe.co[0] for fcurve in anim_action.fcurves for keyframe in fcurve.keyframe_points])
    bpy.context.scene.frame_set(int(last_frame))
    loc_y_last = obj.pose.bones["foot_ik.L"].location[1]
    loc_y_last = abs(round(loc_y_last, 6))
    
    total = (loc_y_1 + loc_y_last) * 2
    
    if not anim_action or not current_action:
        self.report({'ERROR'}, f"Actionlar bulunurken bir hata olustu.")
        return {'CANCELLED'}

    for fcurve in anim_action.fcurves:
        group_name = fcurve.group.name if fcurve.group else None

        target_fcurve = current_action.fcurves.find(fcurve.data_path, index=fcurve.array_index)
        if not target_fcurve:
            target_fcurve = current_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)
        
        if group_name:
            if group_name not in current_action.groups:
                new_group = current_action.groups.new(name=group_name)
            target_fcurve.group = current_action.groups[group_name]

        for keyframe in fcurve.keyframe_points:
            new_keyframe = target_fcurve.keyframe_points.insert(keyframe.co.x + current_frame - 1, keyframe.co.y)
            new_keyframe.interpolation = keyframe.interpolation

        for keyframe in fcurve.keyframe_points:
            new_keyframe_x = keyframe.co.x + current_frame - 1
            if 0 <= new_keyframe_x < len(target_fcurve.keyframe_points):
                new_keyframe = target_fcurve.keyframe_points[int(new_keyframe_x)]
                new_keyframe.handle_left_type = keyframe.handle_left_type
                new_keyframe.handle_right_type = keyframe.handle_right_type

    bpy.context.scene.frame_set(current_frame)
    bpy.context.view_layer.update()
    obj.animation_data.action = current_action
    
    bone.location = first_locations
    if len(bone.rotation_mode) == 3:
        bone.rotation_euler = first_rotations
        bone.keyframe_insert(data_path="rotation_euler", frame=current_frame, group=bone.name)
    elif bone.rotation_mode == "QUATERNION":
        bone.rotation_quaternion = first_rotations
        bone.keyframe_insert(data_path="rotation_quaternion", frame=current_frame, group=bone.name)
    bone.scale = first_scales
    bone.keyframe_insert(data_path="location", frame=current_frame, group=bone.name)
    bone.keyframe_insert(data_path="scale", frame=current_frame, group=bone.name)
    
    bpy.context.scene.frame_set(current_frame+int(last_frame)-1)
    bone.location[1] = -total + (first_locations[1])
    bone.keyframe_insert(data_path="location", frame=current_frame+last_frame-1, group=bone.name)
    bone.keyframe_insert(data_path="scale", frame=current_frame+last_frame-1, group=bone.name)
    if len(bone.rotation_mode) == 3:
        bone.keyframe_insert(data_path="rotation_euler", frame=current_frame+last_frame-1, group=bone.name)
    elif bone.rotation_mode == "QUATERNION":
        bone.keyframe_insert(data_path="rotation_quaternion", frame=current_frame+last_frame-1, group=bone.name)
        
    action = obj.animation_data.action
    for fcurve in action.fcurves:
        if fcurve.data_path == f'pose.bones["{bone.name}"].location':
            for keyframe in fcurve.keyframe_points:
                if keyframe.co.x == current_frame or keyframe.co.x == current_frame+int(last_frame)-1:
                    keyframe.interpolation = 'LINEAR'
                    
    for fcurve in action.fcurves:
        if fcurve.data_path == f'pose.bones["{bone.name}"].location' and fcurve.array_index == 1:
            fcurve.extrapolation = 'LINEAR'
            break
    
    bpy.context.scene.frame_set(current_frame)
    bpy.ops.object.mode_set(mode='OBJECT')

class MP_MT_Action_Menu(Menu):
    bl_label = "Actionlar"
    bl_idname = "mp.action_menu"

    def draw(self, context):
        layout = self.layout
        
        for action in bpy.data.actions:
            if action.name in character_actions:
                op = layout.operator("mp.set_action", text=action.name)
                op.action = action.name 

def kontrol():
    a = bpy.context.active_object
    if a.type == 'ARMATURE':
        obj = a
        armature = obj.data
        
        for bone in obj.pose.bones:
            if bone.name.startswith("root") and len(bone.name) > 4:
                bone = obj.pose.bones[bone.name]
                break                
        else:
            if 'root' in obj.pose.bones:
                bone = obj.pose.bones['root']
        
        for cons in bone.constraints:
            if cons.influence == 1.0:
                return "path"
        
        return "duz"

class MP_OT_SetAction(Operator):
    bl_idname = "mp.set_action"
    bl_label = "Action Uygulanacak!"
    action: StringProperty()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"'{self.action}' uygulanacak.")
        layout.label(text="Emin misiniz?")

    def execute(self, context):
        action = bpy.data.actions[self.action]
        action_name = self.action
        
        control = kontrol()
        if control == "duz":
            duz_yurume_uygula(action_name)
        elif control == "path":
            ret = path_yurume(action_name)
            if ret == "curve tools addon":
                self.report({'ERROR'}, f'Curve Tools addonu yüklenemedi!')
        else:
            self.report({'ERROR'}, f'Belirlemede bir hata olustu!')
            return {'CANCELLED'}
        
        self.report({'INFO'}, f'"{self.action}" uygulandı.!')
        return {'FINISHED'}


class MP_OT_CreatePath(Operator):
    bl_idname = "mp.create_path"
    bl_label = "Path Oluştur"

    def execute(self, context):
        
        a = bpy.context.active_object
        cursor_first = bpy.context.scene.cursor.location[:]
        
        if a.type == 'ARMATURE':
            obj = a
            armature = obj.data
        else:
            self.report({'WARNING'}, "Lütfen Karakter Rigini Seçiniz!")
            return {'CANCELLED'}
            
        armature.collections_all["Root"].is_visible = True
        
        for a in obj.data.bones:
            a.select = False
        
        for bone in obj.pose.bones:
            if bone.name.startswith("root") and len(bone.name) > 4:
                bone = obj.pose.bones[bone.name]
                break                
        else:
            if 'root' in obj.pose.bones:
                bone = obj.pose.bones['root']
            else:
                self.report({'ERROR'}, "Root Kemiği Bulunamadı!")
                return {'CANCELLED'}
            
        for cons in bone.constraints:
            if cons.type == "FOLLOW_PATH":
                if cons.influence != 0.0 and cons.target is not None:
                    self.report({'WARNING'}, "Burada Zaten Bir Path Var Gibi Gözüküyor!")
                    return {'CANCELLED'}
            
        bpy.ops.object.mode_set(mode='OBJECT')
        current_location = obj.location[:]
        current_frame = bpy.context.scene.frame_current
        
        obj.keyframe_insert(data_path="location", frame=current_frame-1, group="Object Transform")
        if len(obj.rotation_mode) == 3:
            obj.keyframe_insert(data_path="rotation_euler", frame=current_frame-1, group="Object Transform")
        elif obj.rotation_mode == 'QUATERNION':
            obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame-1, group="Object Transform")
        obj.keyframe_insert(data_path="scale", frame=current_frame-1, group="Object Transform")
        
        obj.location = current_location
        obj.keyframe_insert(data_path="location", frame=current_frame, group="Object Transform")
        if len(obj.rotation_mode) == 3:
            obj.keyframe_insert(data_path="rotation_euler", frame=current_frame, group="Object Transform")
        elif obj.rotation_mode == 'QUATERNION':
            obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame, group="Object Transform")
        obj.keyframe_insert(data_path="scale", frame=current_frame, group="Object Transform")
        bpy.ops.object.mode_set(mode='POSE')
        
        for cons in bone.constraints:
            if cons.type == "FOLLOW_PATH":
                if cons.target is None:
                    bone.constraints.remove(cons)
                
        bone.bone.select = True
        obj.data.bones.active = obj.data.bones.get(bone.name)
        bpy.context.view_layer.update()
        
        center_bone = bone
        world_matrix = obj.matrix_world @ center_bone.matrix
        global_location = world_matrix @ center_bone.bone.head
        bpy.context.scene.cursor.location = global_location

        cursor_location = bpy.context.scene.cursor.location[:]
        c = cursor_location
        bpy.ops.curve.primitive_bezier_curve_add(radius=1, enter_editmode=False, align='WORLD', 
            location=(c[0], c[1], c[2]), scale=(1, 1, 1))
        
        curve = bpy.context.object
        number = 1
        temp_name = obj.name.replace("RIG-", "") + "_path_" + str(number) 
        while temp_name in bpy.data.objects:
            if obj.name.startswith("RIG-"):
                temp_name = obj.name.replace("RIG-", "") + "_path_" + str(number)
                number += 1
            else:
                temp_name = obj.name + "_path_" + str(number)
                number += 1
        curve.name = temp_name
        
        target_collection_name = "Karakter Pathleri"
        if target_collection_name in bpy.data.collections:
            target_collection = bpy.data.collections[target_collection_name]
        else:
            target_collection = bpy.data.collections.new(target_collection_name)
            bpy.context.scene.collection.children.link(target_collection)
            
        if curve.users_collection:
            old_collection = curve.users_collection[0]
            old_collection.objects.unlink(curve)

        if curve.name not in target_collection.objects:
            target_collection.objects.link(curve)
        
        if curve.type == 'CURVE' and curve.data.splines:
            first_spline = curve.data.splines[0]
            
            if first_spline.bezier_points:
                first_point = first_spline.bezier_points[0].co
            elif first_spline.points:
                first_point = first_spline.points[0].co
            else:
                first_point = None

            if first_point:
                bpy.context.scene.cursor.location = curve.matrix_world @ first_point
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        
        curve.location = c

        constraint = bone.constraints.new('FOLLOW_PATH')
        constraint.name = "_".join(curve.name.split("_")[1:])
        constraint.target = bpy.data.objects[curve.name]
        constraint.use_curve_follow = True
        constraint.forward_axis = 'TRACK_NEGATIVE_Y'
        constraint.up_axis = 'UP_Z'
        constraint.influence = 0.0
        constraint.keyframe_insert(data_path="influence", frame=current_frame-1, group=bone.name)
        constraint.influence = 1.0
        constraint.keyframe_insert(data_path="influence", frame=current_frame, group=bone.name)
        
        bpy.ops.object.mode_set(mode='OBJECT')
        obj.location = (0,0,0)
        if len(obj.rotation_mode) == 3:
            obj.rotation_euler = (0,0,0)
            obj.keyframe_insert(data_path="rotation_euler", frame=current_frame, group="Object Transform")
        elif obj.rotation_mode == 'QUATERNION':
            obj.rotation_quaternion = (1,0,0,0)
            obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame, group="Object Transform")
        obj.keyframe_insert(data_path="location", frame=current_frame, group="Object Transform")
        obj.keyframe_insert(data_path="scale", frame=current_frame, group="Object Transform")

        curve_data = curve.data
        curve_data.resolution_u = 64
        curve_data.render_resolution_u = 64
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)

        bpy.ops.object.mode_set(mode='POSE')
        bpy.ops.pose.select_all(action='SELECT')
        bones = [b.name for b in bpy.context.selected_pose_bones]
        
        for a in bones:
            temp_a = obj.pose.bones[a]
            temp_a.bone.select = True
            obj.data.bones.active = obj.data.bones[a]
            if a == bone.name:
                bone.location[1] = 0
            temp_a.keyframe_insert(data_path="location", frame=current_frame-1, group=a)
            if len(obj.rotation_mode) == 3:
                temp_a.keyframe_insert(data_path="rotation_euler", frame=current_frame-1, group=a)
            elif obj.rotation_mode == 'QUATERNION':
                temp_a.keyframe_insert(data_path="rotation_quaternion", frame=current_frame-1, group=a)
            temp_a.keyframe_insert(data_path="scale", frame=current_frame-1, group=a)
        
        for a in bones:
            temp_a = obj.pose.bones[a]
            temp_a.bone.select = True
            obj.data.bones.active = obj.data.bones.get(a)
            obj.data.bones.active = obj.data.bones[a]
            bpy.ops.pose.transforms_clear()
            temp_a.keyframe_insert(data_path="location", frame=current_frame, group=a)
            if len(obj.rotation_mode) == 3:
                temp_a.keyframe_insert(data_path="rotation_euler", frame=current_frame, group=a)
            elif obj.rotation_mode == 'QUATERNION':
                temp_a.keyframe_insert(data_path="rotation_quaternion", frame=current_frame, group=a)
            temp_a.keyframe_insert(data_path="scale", frame=current_frame, group=a)

        bone.bone.select = True
        obj.data.bones.active = obj.data.bones[bone.name]
        bpy.context.view_layer.update()

        bpy.ops.object.mode_set(mode='OBJECT')
            
        bpy.context.scene.cursor.location = cursor_first
        
        return {'FINISHED'}

def path_yurume(act_name):
    current_frame = bpy.context.scene.frame_current
    obj = bpy.context.active_object

    if obj.type != "ARMATURE":
        return {'CANCELLED'}
    else:
        armature = obj.data
        
    if obj is not None:
        if obj.animation_data.action is not None:
            current_action = obj.animation_data.action
        else:
            actions_list = [i.name for i in bpy.data.actions]
            count = 1
            temp_name = "New Action"
            while temp_name in actions_list:
                temp_name = "New Action " + str(count)
                count += 1
            bpy.data.actions.new(name=temp_name)
            current_action = bpy.data.actions[temp_name]
            obj.animation_data.action = current_action
    else:
        return {'CANCELLED'}

    if act_name in bpy.data.actions:
        anim_action = bpy.data.actions[act_name]
    
    obj.animation_data.action = anim_action
        
    armature.collections_all["Root"].is_visible = True
    bpy.ops.object.mode_set(mode='POSE')
    
    for a in obj.data.bones:
        a.select = False
    
    for bone in obj.pose.bones:
        if bone.name.startswith("root") and len(bone.name) > 4:
            bone = obj.pose.bones[bone.name]
            break
    else:
        if 'root' in obj.pose.bones:
            bone = obj.pose.bones['root']
        else:
            return {'CANCELLED'}
    pose_bone = obj.pose.bones.get(bone.name)  
    bpy.ops.pose.select_all(action='DESELECT')
    obj.data.bones[bone.name].select = True
    obj.data.bones.active = obj.data.bones[bone.name]
    
    action = anim_action
    suitable_slots = [slot for slot in action.slots if slot.target_id_type == 'OBJECT']
    if len(suitable_slots) > 0:
        obj.animation_data.action_slot = suitable_slots[0]
    else:
        print("Slot Bulunamadi!")
    
    bpy.context.scene.frame_set(1)
    loc_y_1 = bpy.context.object.pose.bones["foot_ik.L"].location[1]
    loc_y_1 = abs(round(loc_y_1, 6))
    
    last_frame = max([keyframe.co[0] for fcurve in anim_action.fcurves for keyframe in fcurve.keyframe_points])
    bpy.context.scene.frame_set(int(last_frame))
    loc_y_last = bpy.context.object.pose.bones["foot_ik.L"].location[1]
    loc_y_last = abs(round(loc_y_last, 6))
    
    total = (loc_y_1 + loc_y_last) * 2
    
    if not anim_action or not current_action:
        print("Belirtilen action'lar bulunamadı.")
        return {'CANCELLED'}

    for fcurve in anim_action.fcurves:
        target_fcurve = current_action.fcurves.find(fcurve.data_path, index=fcurve.array_index)
        if not target_fcurve:
            target_fcurve = current_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)
        
        for keyframe in fcurve.keyframe_points:
            new_keyframe = target_fcurve.keyframe_points.insert(keyframe.co.x + current_frame - 1, keyframe.co.y)
            new_keyframe.interpolation = keyframe.interpolation
        
        for keyframe in fcurve.keyframe_points:
            new_keyframe_x = keyframe.co.x + current_frame - 1
            if 0 <= new_keyframe_x < len(target_fcurve.keyframe_points):
                new_keyframe = target_fcurve.keyframe_points[int(new_keyframe_x)]
                new_keyframe.handle_left_type = keyframe.handle_left_type
                new_keyframe.handle_right_type = keyframe.handle_right_type
            else:
                print(f"Index {int(new_keyframe_x)} geçersiz, keyframe eklenmedi.")

    bpy.context.scene.frame_set(current_frame)
    bpy.context.view_layer.update()
    
    obj.animation_data.action = current_action
    bpy.context.scene.frame_set(current_frame)
    
    offset_value = - ((48.53 * total) + 1.625)
    
    constraint_path = None
    for fcurve in current_action.fcurves:
        if fcurve.data_path.endswith("influence") and bone.name in fcurve.data_path:
            keyframes = [kp.co.x for kp in fcurve.keyframe_points]
            if len(keyframes) == 4:
                if keyframes[1] <= current_frame <= keyframes[2]:
                    constraint_path = fcurve.data_path
            elif len(keyframes) == 2:
                if keyframes[1] <= current_frame:
                    constraint_path = fcurve.data_path
            else:
                self.report({'WARNING'}, "Path bağlanırken bir sorun oluştu, animasyonunuzu kontrol ediniz!")
                
    if constraint_path is not None:
        constraint_name_mtch = re.search(r'constraints\["([^"]+)"\]', constraint_path)
        constraint_name = constraint_name_mtch.group(1)
        constraint = bone.constraints[constraint_name]
    
    curve = constraint.target
    for bone in bpy.context.selected_pose_bones:
        bone.bone.select = False
    bpy.context.view_layer.update()
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    
    if "bl_ext.blender_org.curve_tools" not in bpy.context.preferences.addons:
        try:
            bpy.ops.extensions.package_install(repo_index=0, pkg_id="curve_tools")
        except:
            self.report({'ERROR'}, "Preferences'tan Get Extensions kısmından allow seçeneğini seçiniz!")
    
    bpy.ops.preferences.addon_enable(module="bl_ext.blender_org.curve_tools")
    bpy.ops.curvetools.operatorcurvelength()
    curve_len = bpy.context.scene.curvetools.CurveLength
    half_curve_len = curve_len/ 2.08248
    
    offset_value = offset_value / half_curve_len
    
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    
    
    bpy.context.scene.frame_set(current_frame)
    constraint.offset = 0
    constraint.keyframe_insert(data_path="offset", frame=current_frame, group=bone.name)
    
    bpy.context.scene.frame_set(current_frame + 24)
    constraint.offset = offset_value
    constraint.keyframe_insert(data_path="offset", frame=current_frame + 24, group=bone.name) 
    
    action = obj.animation_data.action
    fcurve = None
    for fc in action.fcurves:
        if fc.data_path == f'pose.bones["{bone.name}"].constraints["{constraint.name}"].offset':
            fcurve = fc
            break

    if fcurve is not None:
        for keyframe in fcurve.keyframe_points:
            if keyframe.co[0] in {current_frame, current_frame+24}:
                keyframe.interpolation = 'LINEAR'
        fcurve.extrapolation = 'LINEAR'
    
    bpy.context.scene.frame_set(current_frame)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    bpy.ops.preferences.addon_disable(module="bl_ext.blender_org.curve_tools")

class MP_OT_BreakPath(Operator):
    bl_idname = "mp.break_path"
    bl_label = "Path'den Ayrıl"

    def execute(self, context):
        
        current_frame = bpy.context.scene.frame_current
        a = bpy.context.active_object
        
        if a.type == 'ARMATURE':
            obj = a
            armature = obj.data
        else:
            self.report({'WARNING'}, "Lütfen Karakter Rigini Seçiniz!")
            return {'CANCELLED'}
            
        for a in obj.data.bones:
            a.select = False
        
        for bone in obj.pose.bones:
            if bone.name.startswith("root") and len(bone.name) > 4:
                bone = obj.pose.bones[bone.name]
                break
        else:
            if 'root' in obj.pose.bones:
                bone = obj.pose.bones['root']
            else:
                return {'CANCELLED'}
            
        bone.bone.select = True
        obj.data.bones.active = obj.data.bones.get(bone.name)
        bpy.context.view_layer.update()
        
        constraint_path = None
        if obj.animation_data and obj.animation_data.action:
            action = obj.animation_data.action
            
            mutlak_deger = float('inf')
            for fcurve in action.fcurves:
                if fcurve.data_path.endswith("influence") and bone.name in fcurve.data_path:
                    keyframes = [kp.co.x for kp in fcurve.keyframe_points]
                    last_keyframe = max(keyframes)
                    if len(keyframes) < 4 and current_frame > last_keyframe:
                        if abs(current_frame - int(last_keyframe)) < mutlak_deger:
                            mutlak_deger = abs(current_frame - int(last_keyframe))
                            constraint_path = fcurve.data_path
        
        if constraint_path is not None:
            constraint_name_mtch = re.search(r'constraints\["([^"]+)"\]', constraint_path)
            constraint_name = constraint_name_mtch.group(1)
            constraint = bone.constraints[constraint_name]
            
            obj.location = (0,0,0)
            obj.keyframe_insert(data_path="location", frame=current_frame, group="Object Transform")
            if len(obj.rotation_mode) == 3:
                obj.rotation_euler = (0,0,0)
                obj.keyframe_insert(data_path="rotation_euler", frame=current_frame, group="Object Transform")
            elif obj.rotation_mode == 'QUATERNION':
                obj.rotation_quaternion = (1,0,0,0)
                obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame, group="Object Transform")
            obj.keyframe_insert(data_path="scale", frame=current_frame, group="Object Transform")
            
            center_bone = bone
            world_matrix = obj.matrix_world @ center_bone.matrix
            global_location = world_matrix @ center_bone.bone.head
            bpy.context.scene.cursor.location = global_location[:]
            cursor_location = bpy.context.scene.cursor.location[:]
            
            if constraint is not None:
                bpy.context.scene.frame_set(current_frame)
                constraint.influence = 1.0
                constraint.keyframe_insert(data_path="influence", frame=current_frame, group=bone.name)
                bpy.context.scene.frame_set(current_frame+1)
                constraint.influence = 0.0
                constraint.keyframe_insert(data_path="influence", frame=current_frame+1, group=bone.name)
            else:
                return {'CANCELLED'}
            
            bpy.context.scene.frame_set(current_frame+1)
            obj.location = cursor_location
            
            obj.keyframe_insert(data_path="location", frame=current_frame+1, group="Object Transform")
            if len(obj.rotation_mode) == 3:
                obj.keyframe_insert(data_path="rotation_euler", frame=current_frame+1, group="Object Transform")
            elif obj.rotation_mode == 'QUATERNION':
                obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame+1, group="Object Transform")
            obj.keyframe_insert(data_path="scale", frame=current_frame+1, group="Object Transform")
                
            armature.collections_all["Root"].is_visible = True
            bpy.context.scene.frame_set(current_frame)
            
            bpy.ops.object.mode_set(mode='OBJECT')
        
        return {'FINISHED'}

class MP_OT_RootMove(Operator):
    bl_idname = "mp.root_move"
    bl_label = "Root'u taşı"

    def execute(self, context):
        
        current_frame = bpy.context.scene.frame_current
        a = bpy.context.active_object
        
        if a.type == 'ARMATURE':
            obj = a
            armature = obj.data
        else:
            self.report({'WARNING'}, "Lütfen Karakter Rigini Seçiniz!")
            return {'CANCELLED'}
            
        for a in obj.data.bones:
            a.select = False
        
        for bone in obj.pose.bones:
            if bone.name.startswith("root") and len(bone.name) > 4:
                root_bone = obj.pose.bones[bone.name]
                break
        else:
            if 'root' in obj.pose.bones:
                root_bone = obj.pose.bones['root']
            else:
                return {'CANCELLED'}
        
        if 'root' in obj.pose.bones:
            small_root_bone = obj.pose.bones['root']
                
        armature.collections_all["Root"].is_visible = True
        
        root_bone.bone.select = True
        obj.data.bones.active = obj.data.bones.get(root_bone.name)
        bpy.context.view_layer.update()
        
        if "karakter_konumu" in obj.pose.bones:
            location_bone = obj.pose.bones["karakter_konumu"]
        else:
            self.report({'ERROR'}, "Karakter konumu için kemik bulunamadı!")
            return {'CANCELLED'}
        
        # Bu kısım hata verdiriyor object mode'a key atadığı için
        """if obj.location[:] != (0,0,0):
            obj.keyframe_insert(data_path="location", frame=current_frame-1, group="Object Transform")
            if len(obj.rotation_mode) == 3:
                obj.keyframe_insert(data_path="rotation_euler", frame=current_frame-1, group="Object Transform")
            elif obj.rotation_mode == 'QUATERNION':
                obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame-1, group="Object Transform")
            obj.keyframe_insert(data_path="scale", frame=current_frame-1, group="Object Transform")
            
            obj.location = (0,0,0)
            obj.keyframe_insert(data_path="location", frame=current_frame, group="Object Transform")
            if len(obj.rotation_mode) == 3:
                obj.rotation_euler = (0,0,0)
                obj.keyframe_insert(data_path="rotation_euler", frame=current_frame, group="Object Transform")
            elif obj.rotation_mode == 'QUATERNION':
                obj.rotation_quaternion = (1,0,0,0)
                obj.keyframe_insert(data_path="rotation_quaternion", frame=current_frame, group="Object Transform")
            obj.keyframe_insert(data_path="scale", frame=current_frame, group="Object Transform")
        """
        bone_names = ["torso", "foot_ik.L", "foot_ik.R", root_bone.name, small_root_bone.name]
        for b_name in bone_names:
            temp_bone = obj.pose.bones[b_name]
            temp_bone.keyframe_insert(data_path="location", frame=current_frame-1, group=b_name)
            if len(temp_bone.rotation_mode) == 3:
                temp_bone.keyframe_insert(data_path="rotation_euler", frame=current_frame-1, group=b_name)
            elif temp_bone.rotation_mode == "QUATERNION":
                temp_bone.keyframe_insert(data_path="rotation_quaternion", frame=current_frame-1, group=b_name)
            temp_bone.keyframe_insert(data_path="scale", frame=current_frame-1, group=b_name)
        
        old_cursor_location = bpy.context.scene.cursor.location.copy()
        center_bone = location_bone
        world_matrix = obj.matrix_world @ center_bone.matrix
        global_location = world_matrix @ center_bone.bone.head
        bpy.context.scene.cursor.location = global_location
        current_cursor_location = bpy.context.scene.cursor.location.copy()

        rig_matrix_world = obj.matrix_world
        bone_global_matrix = rig_matrix_world @ root_bone.matrix
        bone_global_matrix.translation = current_cursor_location
        root_bone.matrix = rig_matrix_world.inverted() @ bone_global_matrix
        small_root_bone.location = (0,0,0)

        bpy.context.scene.cursor.location = old_cursor_location[:]
        
        for b_name in bone_names[:3]:
            temp_bone = obj.pose.bones[b_name]
            temp_bone.location = (0.0, 0.0, 0.0)
            temp_bone.keyframe_insert(data_path="location", frame=current_frame, group=temp_bone.name)
            if len(temp_bone.rotation_mode) == 3:
                temp_bone.rotation_euler = (0.0, 0.0, 0.0)
                temp_bone.keyframe_insert(data_path="rotation_euler", frame=current_frame, group=temp_bone.name)
            elif temp_bone.rotation_mode == "QUATERNION":
                temp_bone.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
                temp_bone.keyframe_insert(data_path="rotation_quaternion", frame=current_frame, group=temp_bone.name)
            temp_bone.scale = (1.0, 1.0, 1.0)
            temp_bone.keyframe_insert(data_path="scale", frame=current_frame, group=temp_bone.name)
        
        for a in bone_names[-2:]:
            temp_a = obj.pose.bones[a]
            temp_a.bone.select = True
            obj.data.bones.active = obj.data.bones[a]
            temp_a.keyframe_insert(data_path="location", frame=current_frame, group=a)
            if len(temp_a.rotation_mode) == 3:
                temp_a.keyframe_insert(data_path="rotation_euler", frame=current_frame, group=a)
            elif temp_a.rotation_mode == "QUATERNION":
                temp_a.keyframe_insert(data_path="rotation_quaternion", frame=current_frame, group=a)
            temp_a.keyframe_insert(data_path="scale", frame=current_frame, group=a)
        

        return {'FINISHED'}

############################ Action Editor Operations ############################

class MP_MT_DeleteActionsMenu(Menu):
    bl_label = "Action Sil"
    bl_idname = "mp.delete_actions_menu"

    def draw(self, context):
        layout = self.layout
        
        for action in bpy.data.actions:
            op = layout.operator("mp.delete_action_confirm", text=action.name)
            op.action = action.name 

class MP_OT_DeleteActionConfirm(Operator):
    bl_idname = "mp.delete_action_confirm"
    bl_label = "Action Sil"
    action: StringProperty()

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        return bpy.ops.mp.delete_action('INVOKE_DEFAULT', action=self.action)

class MP_OT_DeleteAction(Operator):
    bl_idname = "mp.delete_action"
    bl_label = "Action Silinecek!"
    action: StringProperty()

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"'{self.action}' isimli action silinecek.")
        layout.label(text="Emin misiniz?")

    def execute(self, context):
        bpy.data.actions.remove(bpy.data.actions[self.action])
        self.report({'INFO'}, f'"{self.action}" isimli action silindi!')
        return {'FINISHED'}

class MP_OT_ActionEditorHeader(Operator):
    bl_idname = "mp.action_editor_header_menu"
    bl_label = "Action Editor Header Menu"

    def execute(self, context):
        bpy.ops.wm.call_menu(name="mp.delete_actions_menu")
        return {'FINISHED'}

class MP_OT_DeleteAllActionAssets(Operator):
    bl_idname = "mp.delete_action_assets"
    bl_label = "Asset actionları silinecek. Onaylıyor musunuz?"

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        actions_to_remove = [action for action in bpy.data.actions if action.asset_data is not None]
        for action in actions_to_remove:
            bpy.data.actions.remove(action)
        self.report({'INFO'}, f"{len(actions_to_remove)} tane action asset silindi.")
        return {'FINISHED'}

def draw_header(self, context):
    if context.space_data.mode == 'ACTION':
        layout = self.layout
        layout.operator("mp.action_editor_header_menu", text="Action Sil", icon="DOWNARROW_HLT")
        layout.operator("mp.delete_action_assets", text="Asset Actionları Sil", icon='TRASH')


########### Scripting Settings ###########

class MP_PT_Scripting_Settings(Panel):
    bl_idname = 'mp.scripting_settings'
    bl_label = "Scripting Settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2

        layout.menu(MP_MT_RunScript.bl_idname)

class MP_MT_RunScript(Menu):
    bl_label = "Script Çalıştır"
    bl_idname = "mp.run_sript"

    def draw(self, context):
        layout = self.layout

        for text in bpy.data.texts:
            layout.operator("mp.confirm_run_script", text=text.name).text_name = text.name

class MP_OT_ConfirmRunScript(Operator):
    bl_idname = "mp.confirm_run_script"
    bl_label = "Script Çalıştırılacak!"

    text_name: StringProperty()

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"{self.text_name} isimli script çalıştırılacak.")
        layout.label(text="Devam etmek istiyor musunuz?")
        
    def execute(self, context):
        text_block = bpy.data.texts.get(self.text_name)
        
        if text_block:
            current_type = context.area.type
            context.area.type = 'TEXT_EDITOR'
            context.space_data.text = text_block
            bpy.ops.text.run_script()
            context.area.type = current_type
            self.report({'INFO'}, f"{self.text_name} çalıştırıldı.")
        else:
            self.report({'ERROR'}, f"Text bloğu bulunamadı: {self.text_name}")
                
        return {'FINISHED'}
    
classes = (
    # Link Operations
    MP_PT_LinkOperations, MP_OT_FindFilePaths, MP_OT_KarakterRigi, MP_OT_ModelRigi, MP_OT_RelationsMake,
    
    # Animation Operations
    MP_PT_AnimationOperations, MP_OT_WalkingStraight, MP_MT_Action_Menu, MP_OT_SetAction, 
    MP_OT_CreatePath, MP_OT_BreakPath, MP_OT_RootMove,
    
    # Action Editor Operations
    MP_MT_DeleteActionsMenu, MP_OT_DeleteActionConfirm, MP_OT_DeleteAction, 
    MP_OT_ActionEditorHeader, MP_OT_DeleteAllActionAssets,
    
    # Scripting Settings
    MP_PT_Scripting_Settings, MP_MT_RunScript, MP_OT_ConfirmRunScript
)

@addon_updater_ops.make_annotations
class DemoPreferences(bpy.types.AddonPreferences):
	
	bl_idname = __package__

	# Addon updater preferences.

	auto_check_update = bpy.props.BoolProperty(
		name="Auto-check for Update",
		description="If enabled, auto-check for updates using an interval",
		default=False)

	updater_interval_months = bpy.props.IntProperty(
		name='Months',
		description="Number of months between checking for updates",
		default=0,
		min=0)

	updater_interval_days = bpy.props.IntProperty(
		name='Days',
		description="Number of days between checking for updates",
		default=7,
		min=0,
		max=31)

	updater_interval_hours = bpy.props.IntProperty(
		name='Hours',
		description="Number of hours between checking for updates",
		default=0,
		min=0,
		max=23)

	updater_interval_minutes = bpy.props.IntProperty(
		name='Minutes',
		description="Number of minutes between checking for updates",
		default=0,
		min=0,
		max=59)

	def draw(self, context):
		layout = self.layout
		addon_updater_ops.update_settings_ui(self, context)


def register():

    addon_updater_ops.register(bl_info)

    for cls in classes:
        bpy.utils.register_class(cls)
        
    bpy.types.DOPESHEET_HT_header.append(draw_header)

    bpy.utils.register_class(DemoPreferences)
    
    bpy.types.Scene.link_tabs = bpy.props.EnumProperty(
        items=[('TAB1', "Karakter", ""),
               ('TAB2', "Model", ""),
               ('TAB3', "Shape Keys", "")],
        name="Tab Sekmeleri"
    )
    
    bpy.types.Scene.animation_tabs = bpy.props.EnumProperty(
        items=[('TAB1', "Düz", ""),
               ('TAB2', "Path", ""),
               ('TAB3', "Root", "")],
        name="Animasyon Sekmeleri"
    )
    
def unregister():

    addon_updater_ops.unregister()

    for cls in classes:
        bpy.utils.unregister_class(cls)

    bpy.types.DOPESHEET_HT_header.remove(draw_header)

    bpy.utils.unregister_class(DemoPreferences)
    
    del bpy.types.Scene.link_tabs
    del bpy.types.Scene.animation_tabs
    
if __name__ == "__main__":
    register()
