GRT v4.1.0 - 6/4/2024

## Summary

Fix Action Bakery to work in Blender 4.1 primarily caused by Blender 4.1 new Layer System, Renamed Property, and Used the new Proper Panel. Also Exposed new property from Bake Operators and Added Subpanel for Utility Operators

---

### Fixed

- Fix Error Caused by Changed name for Bone Color Viewport Display Property
- Fix Error Convert bendy Bones to Bone due to Bone Collection Updates
- Fix Bugs for Batch Rename Actions when using "All" Mode where it will append name unpredictably

### Update

- Expose Bake Channel (Lot, Rot, Scale, BBone, Custom Properties) to Global Bake Settings
- String Field Now uses Placeholder Text
- Added Subpanel for Utility Tool and Cleanup Tool
- Added Relation (Tail / Head) Options to Active Armature Display

### Removed

- Remove "Bake Custom Properties" Operator
- Remove "Move All Bones to Layer" Operator
