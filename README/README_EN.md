## English
This add-on is primarily designed for custom rigging. Its core features include **batch customizing bone display shapes**, **generating constraints**, **retargeting action**, and **batch renaming vertex groups and shape keys.** <br>
Recommended Version: Blender 4.2+ <br>
### Add-on Location
![Location](https://github.com/user-attachments/assets/73be77a9-1e73-4666-939c-1b62c5013ef5)

### Feature Directory
>[Custom Display Shape](#custom-display-shape)<br>
><br>
>[Generate Constraint](#generate-constraint)<br>
><br>
>[Retarget Actions](#retarget-actions)<br>
><br>
>[Rename Tool](#rename-tool)<br>

## Custom Display Shape:
![Custom Display Interface](https://github.com/user-attachments/assets/db43d8e1-99ac-41ac-b1f4-d1e2ceda68d0)<br>
***You must first enter Pose Mode and select the bones to apply the changes to.***
### Shape
![Shape Interface](https://github.com/user-attachments/assets/2839f568-a25a-4d11-a525-21115430b37d)<br>
Select the shape to apply from the dropdown.<br>
![Shape Selection](https://github.com/user-attachments/assets/c0ad7e09-9f54-49b4-95ea-a971c702edcf)<br>
**Enable Scale bone length:** Applies the bone length from Edit Mode to the custom shape's size.<br>
**Apply Bone Shape:** Applies the display shape of the selected bone.<br>
### Color
![Bone Color](https://github.com/user-attachments/assets/035912f2-ff12-4a78-bed6-b45a4ae7d6a0)<br>
**Bone Color:** The color of the bone displayed in Edit Mode.<br>
**Pose Bone Color:** The color of the bone displayed in Pose Mode.<br>
**Apply Color:** Applies the display color of the selected bone.<br>
### Scale
![Bone Scale](https://github.com/user-attachments/assets/a7b6d259-1f72-42c5-884b-46acb876073a)<br>
When "Enable Apply Scale All" is checked, the X, Y, and Z scale of the bone shape will be applied as the "Scale All" value. If unchecked, individual axis scaling can be adjusted.<br>
**Apply Scale:** Applies the display shape scale of the selected bone.<br>
### Translation
![Bone Translation](https://github.com/user-attachments/assets/f48f7b29-deae-4434-bc65-258d2eebff1d)<br>
Used to adjust the positional offset of the bone display shape.<br>
**Apply Translation**: Applies the positional offset of the bone display shape.<br>
### Rotation
![Bone Rotation](https://github.com/user-attachments/assets/fd0e81ec-a656-4dc8-b4ba-71bf5cc48625)<br>
Used to adjust the rotation of the bone display shape.<br>
**Apply Rotation:** Applies the rotation of the bone display shape.<br>
### Apply All
![Apply All](https://github.com/user-attachments/assets/d6f481fa-4afc-4c04-80a2-130da475da58)<br>
**Copy From Selected:** Copies the shape information from the selected bone.<br>
**Apply All:** Applies all settings in this section.<br>
<br>
### How to Add Shapes to the Display Shape Library?
Bone shape icons and bone shape objects are stored in the add-on's preferences under the "Bone Shape Folder." The default folder path is:<br>
Add-on Location\BLRigTool\addons\BLRigTool\assets<br>
![Bone Shape Folder](https://github.com/user-attachments/assets/7aab2626-55d7-4ebe-8c74-49b9c316de93)<br>
<br>
If you wish to change the specified path, the folder must contain an "icons" folder and the "BoneShapesLibrary.blend" file.<br>
![Bone Shape Folder Contents](https://github.com/user-attachments/assets/c38f1537-ba94-487a-af14-72bbac9a8db5)<br>
***Custom display shape modifications and operations should be performed within BoneShapesLibrary.blend.***<br>
<br>
To generate icons for an object, select it within the add-on, not as a target object selected in Object Mode.<br>
![Generate Shape Selection](https://github.com/user-attachments/assets/f2587441-bccb-4994-b1d1-5c2b376c0add)<br>
Dropdown menu:<br>
![Shape Customization](https://github.com/user-attachments/assets/d7468acc-b6ee-4348-87a2-a39b9cc9e48e)<br>
<br>
**Generate Icon for selected object:** See "Generate Icon Settings" below for details.<br>
**Remove Icon:** Removes the generated icon.<br>
**Reload Bone Shape Icons:** Try using this if icons do not change after generation or do not display after the add-on loads.<br>

**Generate Icon Settings:**<br>
>![Generate Icon](https://github.com/user-attachments/assets/d5d37a9f-1ddf-4704-9653-f2183bb5d126)<br>
><br>
>**Camera Distance:** The distance between the camera capturing the object icon and the object.<br>
>**Camera Angle:** TOP: Captures from above. / DIAGONAL: Captures from a diagonal angle.<br>
>**Keep Generated (camera & Light):** Keeps the camera and light used for generating icons in the scene. If corresponding cameras and lights already exist in the scene during generation, they will be prioritized. This is useful for manual adjustments and previews.<br>
><br>
>![Keep Generated](https://github.com/user-attachments/assets/e8364eab-7678-4827-b584-9d890f916bb0)<br>
><br>
>When using a Curve object to generate an icon, you must first give the curve a thickness in Curve Data > Geometry > Bevel.<br>
>![Curve Bevel](https://github.com/user-attachments/assets/7e121715-0217-489e-9b3b-9efb5131926e)<br>

## Generate Constraint:
![Generate Constraint Interface](https://github.com/user-attachments/assets/9fe39eca-87d3-471e-8154-1c629c9121de)
### Remove Constraints
![Remove Constraints Interface](https://github.com/user-attachments/assets/9e12e976-1add-44a3-a266-20264019e098)<br>
**Remove Constraints:** Removes all constraints from the selected bones.<br>
### Generate Deform Bones
![Generate Deform Bones](https://github.com/user-attachments/assets/1dd29f81-4c0e-47cf-8b63-53ae11f9b2ec)<br>
Some DCCs have different bone axes. This function helps generate bones with corresponding axes or bind existing armatures with different axes to Blender's axis-controlled armature.<br>
The generated bones are virtual deform bones and will not have the deform option checked. The model is still controlled by Blender's axis-controlled bones. When exporting, if you need to convert to deform bones, use "BL-Export to Unreal" and check "Use Virtual Deform."<br>
It is recommended to bind the armature to the character and complete adjustments before generating virtual deform bones.<br>
<br>
**Generate Deform:** Generates deform bones with corresponding axes for the selected bones.<br>
![Generate Deform Interface](https://github.com/user-attachments/assets/122f4d03-7790-4b7d-bc10-ec4fde88f265)<br>
>**XYZ-Axis:** Select the corresponding axis for bone generation.<br>
>**Position Base:** Select the generation position for the bones. You can choose to generate at the head or tail of the source bone.<br>
>**Collection Name:** Customize the group name in Data > Bone Collections on the right.<br>
>EX:<br>
>![Generate Deform Example](https://github.com/user-attachments/assets/46e50dcc-68f1-46e3-8259-f529a27b247a)<br>
>X corresponds to Y, Y corresponds to X, Z corresponds to -Z, generated at the root of the original bone.<br>

**UE5 Manny Deform:** If the selected armature is a UE5 skeleton or the bone names match the UE5 default Manny skeleton, deform bones will be generated for the corresponding bones. (Manny_Simple only)<br>
You can add a prepared armature by going to Object Mode > Add > Armature > Add UE5 Manny (Simple).<br>
![Add UE5 Manny Interface](https://github.com/user-attachments/assets/ee825568-fad0-4c80-9ffb-b6f6d3adc941)<br>
Then, enter Pose Mode and press "UE5 Manny Deform."<br>
![UE5 Manny Deform Example](https://github.com/user-attachments/assets/dc65dfaf-8354-4bc5-b0ca-c8035fb7bf09)<br>
It is recommended to use a prepared armature or a armature with the same axes and settings to generate virtual deform bones that perfectly match UE5 Manny.<br>

**Connect Deform Armature:** Links a armature imported from another DCC, which has not undergone axis conversion, as a deform bone to a armature that has been axis-adjusted in Blender.<br>
![Connect Deform Armature Interface](https://github.com/user-attachments/assets/b337c71c-c416-4fb8-9d0e-942116585003)<br>
![Connect Deform Armature Example 1](https://github.com/user-attachments/assets/6aecf963-1952-4d29-8717-5a7927da4c9e)<br>
![Connect Deform Armature Example 2](https://github.com/user-attachments/assets/6eb8c391-81d6-42bc-ba0d-8bf744476b85)<br>

**Set Inverse All:** Executes "Set Inverse" for all Child Of constraints within the selected deform bones. If deform bones are not locking correctly when animation plays, set the armature to Rest Position and then execute this function on the selected deform bones.<br>

### Generate Constraints
![Generate Constraints](https://github.com/user-attachments/assets/163ce372-7c34-4702-a3d2-909c81e21c82)<br>
<br>
**Head:** <br>
![Head Interface](https://github.com/user-attachments/assets/1265137e-a29e-424b-86fe-6845852516f5)<br>
![Head Result](https://github.com/user-attachments/assets/d77262a1-0d40-4f7a-a456-428fa08435f9)<br>
Chest is the bone below the neck.<br>
<br>
**Spine:** <br>
![Spine Interface](https://github.com/user-attachments/assets/bfd76906-ca80-4bc4-ba82-8d5adf5c63be)<br>
![Spine Result](https://github.com/user-attachments/assets/779a1955-4e5a-4417-977e-ffa3d8017e7d)<br>
<br>
**Arm:** <br>
![Arm Interface](https://github.com/user-attachments/assets/8eb0919e-19ee-49fa-a172-c6f97a914329)<br>
![Arm Result](https://github.com/user-attachments/assets/716fe8a2-5fd5-4565-9976-c9e25766db04)<br>
Arm Length is the number of bones above the hand.<br>
<br>
**Leg:** <br>
![Leg Interface](https://github.com/user-attachments/assets/e1780c62-88d7-4fc1-a536-ce78ae005ffe)<br>
![Leg Result](https://github.com/user-attachments/assets/fa28755d-4528-49f2-9084-8a7d3a851cfd)<br>
Leg Length is the number of bones above the foot.<br>
If "Is Create Toe" is unchecked, toe constraints and controllers will not be generated, which is suitable for armatures without toes.<br>
<br>
**Finger:** <br>
![Finger Interface](https://github.com/user-attachments/assets/85a807ae-1bda-4470-8a57-c795975de7f4)<br>
![Finger Result](https://github.com/user-attachments/assets/6497c80b-0282-4d28-9e1f-c2cb2840c8f5)<br>
Root Bone: Select the uppermost bone of the finger.<br>
Besides generating fingers, it can also be used to generate tails and other elongated parts.<br>
<br>
**UE5 Manny:** <br>
![UE5 Manny Result](https://github.com/user-attachments/assets/cd5fe69a-9a12-41d5-87c7-620ad9e1acef)<br>
Generates controllers for armatures named identically to UE5 Manny (Simple).<br>
You can appropriately disable some bone collections to leave only the main controllers.<br>
![UE5 Manny Collection Interface](https://github.com/user-attachments/assets/729ff6f7-324d-432e-8ef1-9945c2bfbf4e)<br>
![UE5 Manny Simplified](https://github.com/user-attachments/assets/296da51f-5aaf-413e-82f0-5fad727b75c9)<br>
<br>
**Generate Bone Prefix and Shape Settings:**<br>
You can set prefixes for different types of generated bones through the add-on's Preferences > Generated Bone's Prefix.<br>
And configure the display shape for individual bone types in General Bone Display Settings.<br>
![Preferences Prefix Interface](https://github.com/user-attachments/assets/97055744-7d85-451a-ad0b-3e23cd7f969b)<br>
![Preferences Display Interface](https://github.com/user-attachments/assets/21a7383d-d670-4286-a8b1-05ec5e527482)<br>
Default Rigging and shape settings are referenced from: Jim Kroovy - Mr.Mannquins Tools<br>
<br>
## Retarget Actions:
![Retarget Actions Interface](https://github.com/user-attachments/assets/b58710b8-3e7f-4bd6-8f94-ac57f3e87a93)<br>
### Mapping Source/Target Settings
**Source Type:** You can choose between Armature or Action.<br>
**Armature/Action:** The armature or action to be used as the source.<br>
**Target Armature:** The target armature for retargeting.<br>
**Create Bone List:** The generated list will be displayed in the Bone Mapping List below.<br>
### Bone Mapping List
The left side shows the source bones, and the right side shows the target bones.<br>
<br>
**Lock Mapping List:** When locked, the list cannot be changed, preventing accidental modifications.<br>
**Target Bone:** Select a target bone from the list above and rename it in this input field.<br>
**Import/Export:** Import or export the retargeting mapping list as a JSON file, which is convenient for retargeting similar armatures across different files.<br>
**Select Mapping Actions:** Choose the actions to be retargeted. The bone names in the actions will be changed from the source names to the target names on the right side of the mapping list.<br>
**Apply Mapping to Actions:** Apply the target bone names from the bone mapping list to the actions selected in the previous step.<br>

## Rename Tool:
![Rename Tool Interface](https://github.com/user-attachments/assets/3376cb1c-5b4d-4fa4-bcdb-b50ab54a50e5)<br>
**Target:** Can select Vertex Group or Shape Key for renaming.<br>
**Rename Mode:** Can select Find/Replace, Set Prefix/Suffix, Remove Prefix/Suffix.<br>
