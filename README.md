# Quick selection set

Add quick selection set shortcuts in armature pose mode

**[Download latest](https://github.com/Pullusb/quick_selection_set/archive/refs/heads/main.zip)**

---

## Description

**Quick selection set**

Use combination of shortcut to super quickly associate a top row key number with current pose-bone selection.  

Pressing this button will select this bone and deselect the rest (keep current selection with added `Shift`).

Useful to quicly jump back and forth on pose bones when adjusting parts of a character/props animation.

## Shortcuts

`Alt + [1-9]` : Store quick Set  
`[1-9]` : Select quick Set  
`Shift + [1-9]` : Additive Select quick Set  


To handle the selection set, a scene property is stored per `scene` and per `armature`  
That way the association stay in the file.


## Preferences

The are buttons in addon preferences to enable/disable quick selection sets per key (allowing user to use some keys for something else)

<!-- # Possible upgrade:
 - Display buttons in interface ?
 - Toggle affect (only active / multiselect) with "Alt + 0" ? ->  "group mode" -->