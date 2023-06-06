# SPDX-License-Identifier: GPL-2.0-or-later

bl_info = {
    "name": "Quick selection set",
    "description": "Add quick selection set shortcuts in armature pose mode",
    "author": "Samuel Bernou",
    "version": (1, 0, 0),
    "blender": (3, 5, 1),
    "location": "Armature pose mode Alt (set) / Shift (extend) / [1-4] (select)",
    "warning": "To try it is to adopt it",
    "doc_url": "https://github.com/Pullusb/quick_selection_set",
    "tracker_url": "https://github.com/Pullusb/quick_selection_set/issues",
    "category": "Animation"
}

import bpy

## ** Quick selection set **
# Scene property stored per Scene and per rig
# ---
# Alt + [1-4] Store quick Set
# [1-4] Select quick Set
# Shift + [1-4] Additive Select quick Set

### Possible upgrade:
## - Display buttons in interface ?
## - Toggle affect (only active / multiselect) with "Alt+0" ? ->  "group mode"

class ARMATURE_OT_quick_bone_select_store(bpy.types.Operator):
    bl_idname = "pose.quick_bone_select_store"
    bl_label = "Store Quick Selection Set"
    bl_description = "Store a quick selection set from selected bones"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'POSE'

    def invoke(self, context, event):
        self.key=event.type
        return self.execute(context)

    def execute(self, context):
        # print('!Store', self.key)# Dbg

        ### Global mode
        """
        pose_bones = [b for b in context.selected_pose_bones]
        armatures = set([b.id_data for b in pose_bones])
        pose_l = []
        if len(armatures) == 1:
            # only relate to bone name
            for b in context.selected_pose_bones:
                pose_l.append([b.name])
            self.report({'INFO'}, f'{len(pose_l)} selection stored')

        else:
            for b in context.selected_pose_bones:
                pose_l.append([b.name, b.id_data.name])
            self.report({'INFO'}, f'{len(pose_l)} selection stored')

        if pose_l:
            slot_name = f'quick_selection_set_{self.key}'
            context.scene[slot_name] = pose_l
        """

        ### Per armature mode
        # pose_bones = [b for b in context.selected_pose_bones]
        # armatures = set([b.id_data for b in pose_bones])
        active_only = True
        if active_only:
            scope = [context.object]
        else:
            scope = context.objects_in_mode_unique_data

        ct = 0
        for o in scope:
            pose_l = []

            for b in o.pose.bones:
                if b.bone.select:
                    pose_l.append(b.name)
                    ct += 1

            ## if nothing selected... leave untouched
            if pose_l:
                slot_name = f'quick_set_{o.name}_{self.key}'
                context.scene[slot_name] = pose_l

        if ct:
            self.report({'INFO'}, f'{ct} selection stored')
        else:
            self.report({'WARNING'}, f'No selection stored')

        return {"FINISHED"}

class ARMATURE_OT_quick_bone_select_apply(bpy.types.Operator):
    bl_idname = "pose.quick_bone_select_apply"
    bl_label = "Apply Quick Selection Set"
    bl_description = "Apply a quick selection set from selected bones"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        # if not hasattr(bpy.context.view_layer, 'quick_selection_set'):
        #     # cls.poll_message_set("Quick selection not set (use)")
        #     return False
        return context.object and context.mode == 'POSE'

    def invoke(self, context, event):
        self.key = event.type
        self.extend = event.shift
        return self.execute(context)

    def execute(self, context):

        ### Global mode
        """
        slot_name = f'quick_selection_set_{self.key}'

        if slot_name not in bpy.context.scene:
            self.report({"WARNING"}, f'No selection set')
            return {"CANCELLED"}

        select_set = bpy.context.scene[slot_name]

        ct = 0
        for name_list in select_set:
            if len(name_list) == 2:
                ## unpack
                name, arm_name = name_list

                for arm in context.objects_in_mode_unique_data:
                    if arm.name == arm_name:
                        if (b := arm.pose.bones.get(name)):
                            b.bone.select = True
                            ct += 1
                            break

            else:
                name = name_list[0]
                # single name
                # if (b := context.pose_object.pose.bones.get(name)):
                if (b := context.object.pose.bones.get(name)):
                    b.bone.select = True
                    ct += 1

        if not ct:
            self.report({'WARNING'}, 'No selectable bones with this set')
            return {"CANCELLED"}

        self.report({'INFO'}, f'{ct} bone selected')
        """

        ### Per armature mode
        active_only = True
        if active_only:
            scope = [context.object]
        else:
            scope = context.objects_in_mode_unique_data

        ct = 0
        for o in scope:
            slot_name = f'quick_set_{o.name}_{self.key}'
            if slot_name not in bpy.context.scene:
                continue

            select_set = bpy.context.scene[slot_name]

            if self.extend:
                for name in select_set:
                    if (b := context.object.pose.bones.get(name)):
                        b.bone.select = True
                        ct += 1
            else:
                ct += len(select_set)
                for b in o.pose.bones:
                    b.bone.select = b.name in select_set

        if ct:
            if active_only and not self.extend:
                ## if not in extend mode in active only, deselect other armatures
                # Deselect bone from other armatures
                for o in context.objects_in_mode_unique_data:
                    if o != context.object:
                        for b in o.pose.bones:
                            b.bone.select = False

            self.report({'INFO'}, f'{ct} bone selected')
        else:
            self.report({'WARNING'}, 'No selectable bones with this set')
        return {"FINISHED"}

addon_keymaps = []

def register_keymap():
    addon = bpy.context.window_manager.keyconfigs.addon

    if not addon:
        return

    km = addon.keymaps.new(name="Pose", space_type="EMPTY")

    ## Only four first keys are easily reachable and remembering more is probably difficult,
    for key in ['ONE', 'TWO', 'THREE', 'FOUR']: # ,'FIVE' ,'SIX' ,'SEVEN' ,'HEIGHT' ,'NINE', 'ZERO'
        kmi = km.keymap_items.new('pose.quick_bone_select_store', type=key, value='PRESS', alt=True) # Store
        kmi = km.keymap_items.new('pose.quick_bone_select_apply', type=key, value='PRESS') # Apply
        kmi = km.keymap_items.new('pose.quick_bone_select_apply', type=key, value='PRESS', shift=True) # Apply extend

    addon_keymaps.append((km, kmi))

def unregister_keymap():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


classes=(
ARMATURE_OT_quick_bone_select_store,
ARMATURE_OT_quick_bone_select_apply,
)

def register():

    for cls in classes:
        bpy.utils.register_class(cls)
    register_keymap()

def unregister():

    unregister_keymap()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)