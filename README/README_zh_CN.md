## 简体中文
此插件主要为自定义Rigging设计，功能包括 **批量自订骨骼显示外型**、**生成约束**、**动作重定向** 以及 **批量重命名顶点组(Vertex Group)与形状键(Shape Key)**。<br>
建议版本:Blender 4.2+ <br>
### 插件开启位置
![开启位置](https://github.com/user-attachments/assets/73be77a9-1e73-4666-939c-1b62c5013ef5)

### 功能目录
>[Custom Display Shape 自订骨骼显示外型](#自订骨骼显示外型)<br>
><br>
>[Generate Constraint 生成约束](#生成约束)<br>
><br>
>[Retarget Actions 动作重定向](#动作重定向)<br>
><br>
>[Rename Tool 重命名工具](#重命名工具)<br>

## 自订骨骼显示外型:
![custom display 介面](https://github.com/user-attachments/assets/db43d8e1-99ac-41ac-b1f4-d1e2ceda68d0)<br>
***需先进入姿态模式(Pose Mode)中选中要应用的骨骼。***
### 形状(Shape)
![Shape 介面](https://github.com/user-attachments/assets/2839f568-a25a-4d11-a525-21115430b37d)<br>
下拉选择要应用的形状。<br>
![Shape 选择](https://github.com/user-attachments/assets/c0ad7e09-9f54-49b4-95ea-a971c702edcf)<br>
**启用骨骼长度(Enable Scale bone length):** 使编辑模式中的骨骼长度应用到自订外型的大小。<br>
**应用骨骼显示外型(Apply Bone Shape):** 应用所选中骨骼的显示外型。<br>
### 颜色(Color)
![Bone Color](https://github.com/user-attachments/assets/035912f2-ff12-4a78-bed6-b45a4ae7d6a0)<br>
**Bone Color:** 在编辑模式下显示的骨骼颜色。<br>
**Pose Bone Color:** 在姿态模式下显示的骨骼颜色。<br>
**应用颜色(Apply Color):** 应用所选中骨骼的显示颜色。<br>
### 比例(Scale)
![Bone Scale](https://github.com/user-attachments/assets/a7b6d259-1f72-42c5-884b-46acb876073a)<br>
勾选应用所有轴向比例(Enable Apply Scale All)时，会将骨骼外型的x、y、z轴比例应用为Scale All的值；不勾选时则可以分开调整。<br>
**应用比例(Apply Scale):** 应用所选中骨骼的显示外型比例。<br>
### 位置(Translation)
![Bone Translation](https://github.com/user-attachments/assets/f48f7b29-deae-4434-bc65-258d2eebff1d)<br>
用于调整骨骼显示外型的位置偏移。<br>
**应用位置(Apply Translation)**:应用骨骼显示外型的位置偏移。<br>
### 旋转(Rotation)
![Bone Rotation](https://github.com/user-attachments/assets/fd0e81ec-a656-4dc8-b4ba-71bf5cc48625)<br>
用于调整骨骼显示外型的旋转量。<br>
**应用旋转(Apply Rotation):** 应用骨骼显示外型的旋转。<br>
### 应用全部(Apply All)
![Apply All](https://github.com/user-attachments/assets/d6f481fa-4afc-4c04-80a2-130da475da58)<br>
**从所选骨骼複製(Copy From Selected):** 从所选骨骼複製外型资讯。<br> 
**应用全部(Apply All):** 应用此区块的所有设置。<br>
<br>
### 如何将外型加入显示外型库?
骨骼外型图标与骨骼外型物件储存于插件偏好的骨骼外型资料夹(Bone Shape Folder)，预设资料夹路径为:<br>
插件位置\BLRigTool\addons\BLRigTool\assets<br>
![Bone Shape Folder](https://github.com/user-attachments/assets/7aab2626-55d7-4ebe-8c74-49b9c316de93)<br>
<br>
如果要更改指定路径，路径资料夹中务必包含icons资料夹与BoneShapesLibrary.blend档案。<br>
![Bone Shape Folder 内容](https://github.com/user-attachments/assets/c38f1537-ba94-487a-af14-72bbac9a8db5)<br>
***请在BoneShapesLibrary.blend中进行自订显示外型更改与操作。***<br>
<br>
要生成图标的物件请在插件中选择，不是在物件模式中选中的目标物件<br>
![生成 Shape 选择](https://github.com/user-attachments/assets/f2587441-bccb-4994-b1d1-5c2b376c0add)<br>
下拉选单:<br>
![Shape 自订](https://github.com/user-attachments/assets/d7468acc-b6ee-4348-87a2-a39b9cc9e48e)<br>
<br>
**为所选物件生成图标(Generate Icon for selected object):** 详见下方生成图标设定。<br>
**移除图标(Remove Icon):** 移除已生成的图标。<br>
**重新载入骨骼外型图标(Reload Bone Shape Icons):** 生成图标后图标没有变化或是插件载入后没有显示图标可以尝试使用。<br>

**生成图标设定:**<br>
>![Generate Icon](https://github.com/user-attachments/assets/d5d37a9f-1ddf-4704-9653-f2183bb5d126)<br>
><br>
>**摄像机距离(camera distance):** 撷取物件Icon的摄影机与物件的距离。<br>
>**摄像机角度(camera angle):** TOP:从上方撷取。/DIAGONAL:从斜对角撷取。<br>
>**保留生成(Keep generated camera & Light):** 在场景中保留生成Icons所使用的摄像机与灯光。如果生成时场景中已存在对应摄像机与灯光，则会优先使用。用于手动调整与预览。<br>
><br>
>![Keep Generated](https://github.com/user-attachments/assets/e8364eab-7678-4827-b584-9d890f916bb0)<br>
><br>
>使用曲线(Curve)物件用于生成图标前，需先在Curve data->Geometry->Bevel中给曲线一个厚度。<br>
>![Curve Bevel](https://github.com/user-attachments/assets/7e121715-0217-489e-9b3b-9efb5131926e)<br>

## 生成约束:
![Generate Constraint 介面](https://github.com/user-attachments/assets/9fe39eca-87d3-471e-8154-1c629c9121de)
### 移除约束(Remove Constraints)
![Remove Constraints 介面](https://github.com/user-attachments/assets/9e12e976-1add-44a3-a266-20264019e098)<br>
**移除约束(Remove Constraints):** 移除所选骨骼的所有约束。<br>
### 生成变形骨(Generate Deform Bones)
![Generate Deform Bones](https://github.com/user-attachments/assets/1dd29f81-4c0e-47cf-8b63-53ae11f9b2ec)<br>
某些DCC的骨骼轴向不同，这个功能可以帮助生成对应轴向的骨骼，或使用已有的轴向不同骨架绑定至Blender轴向骨架控制。<br>
生成的为虚拟变形骨，不会勾选变形选项，模型依然由Blender轴向骨骼进行控制，输出时要转换为变形骨时请使用BL-Export-to Unreal，勾选Use Virtul Deform。<br>
建议可以先把骨骼体绑定在角色身上完成调适后再进行虚拟变形骨的生成。<br>
<br>
**生成变形骨(Generate Deform):** 为选中的骨骼生成对应轴向的变形骨。<br>
![Generate Deform 介面](https://github.com/user-attachments/assets/122f4d03-7790-4b7d-bc10-ec4fde88f265)<br>
**XYZ-Axis:** 选择生成骨骼的轴向对应。<br>
**生成位置(Position Base):** 选择生成骨骼的生成位置，可以选择在源骨骼的根部或是尾部。<br>
**群组名称(Collection Name):** 自订右方Data>Bone Collections的群组名称。<br>
EX:<br>
![Generate Deform 示例](https://github.com/user-attachments/assets/46e50dcc-68f1-46e3-8259-f529a27b247a)<br>
X对应Y，Y对应X，Z对应-Z，在原骨骼根部生成。<br>

**UE5角色变形骨(UE5 Manny Deform):** 选中骨架为UE5骨架或是骨骼名称与UE5预设Manny骨架相同，则会为有对应的骨骼生成变形骨。(仅限Manny_Simple)<br>
可以在物体模式(Object Mode)从Add>Armature>Add UE5 Manny(Simple)加入整理好的骨骼体。<br>
![Add UE5 Manny 介面](https://github.com/user-attachments/assets/ee825568-fad0-4c80-9ffb-b6f6d3adc941)<br>
接着进入姿态模式(Pose Mode)按下UE5 Manny Deform。<br>
![UE5 Manny Deform 示例](https://github.com/user-attachments/assets/dc65dfaf-8354-4bc5-b0ca-c8035fb7bf09)<br>
建议使用整理好的骨骼体或相同轴向与设定的骨骼体，才能生成完全对应UE5 Manny的虚拟变形骨。<br>

**连结变形骨骨架(Connect Deform Armature):** 将另一个DCC汇入且没有进行轴向转换的骨架，作为变形骨连结到在Blender中进行过轴向整理的骨架上。<br>
![Connect Deform Armature 介面](https://github.com/user-attachments/assets/b337c71c-c416-4fb8-9d0e-942116585003)<br>
![Connect Deform Armature 示例1](https://github.com/user-attachments/assets/6aecf963-1952-4d29-8717-5a7927da4c9e)<br>
![Connect Deform Armature 示例2](https://github.com/user-attachments/assets/6eb8c391-81d6-42bc-ba0d-8bf744476b85)<br>

**全部设置反向(Set Inverse All):** 为所有选中的变形骨里的 Child Of 约束执行设定反向。当动画播放时变形骨没有正确的锁定在正确位置上时，请将骨架设为静止位置(Rest Position)后选中变形骨执行此功能。<br>

### 生成约束(Generate Constraints)
![Generate Constraints 生成约束](https://github.com/user-attachments/assets/163ce372-7c34-4702-a3d2-909c81e21c82)<br>
<br>
**头部(Head):** <br>
![Head 介面](https://github.com/user-attachments/assets/1265137e-a29e-424b-86fe-6845852516f5)<br>
![Head 结果](https://github.com/user-attachments/assets/d77262a1-0d40-4f7a-a456-428fa08435f9)<br>
胸部(Chest)为脖子下方的骨骼。<br>
<br>
**嵴椎(Spine):** <br>
![Spine 介面](https://github.com/user-attachments/assets/bfd76906-ca80-4bc4-ba82-8d5adf5c63be)<br>
![Spine 结果](https://github.com/user-attachments/assets/779a1955-4e5a-4417-977e-ffa3d8017e7d)<br>
<br>
**手臂(Arm):** <br>
![Arm 介面](https://github.com/user-attachments/assets/8eb0919e-19ee-49fa-a172-c6f97a914329)<br>
![Arm 结果](https://github.com/user-attachments/assets/716fe8a2-5fd5-4565-9976-c9e25766db04)<br>
手臂长度(Arm Length)为手掌上方骨骼的数量。<br>
<br>
**腿部(Leg):** <br>
![Leg 介面](https://github.com/user-attachments/assets/e1780c62-88d7-4fc1-a536-ce78ae005ffe)<br>
![Leg 结果](https://github.com/user-attachments/assets/fa28755d-4528-49f2-9084-8a7d3a851cfd)<br>
腿部长度(Leg Length)为脚掌上方骨骼的数量。<br>
是否生成脚趾(Is Create Toe)不勾选则不生成脚趾约束与控制器，适合没有脚趾的骨骼体。<br>
<br>
**手指(Finger):** <br>
![Finger 介面](https://github.com/user-attachments/assets/85a807ae-1bda-4470-8a57-c795975de7f4)<br>
![Finger 结果](https://github.com/user-attachments/assets/6497c80b-0282-4d28-9e1f-c2cb2840c8f5)<br>
根骨骼(Root Bone)选择手指最上方的骨骼。<br>
除了用来生成手指，也可以用来生成尾巴等长条状部位。<br>
<br>
**UE5 角色(UE5 Manny):** <br>
![UE5 Manny 结果](https://github.com/user-attachments/assets/cd5fe69a-9a12-41d5-87c7-620ad9e1acef)<br>
为名称与UE5 Manny(Simple)相同的骨骼生成控制器。<br>
可以适当的关闭一些骨骼群组，只留下主要的控制器。<br>
![UE5 Manny Collection 介面](https://github.com/user-attachments/assets/729ff6f7-324d-432e-8ef1-9945c2bfbf4e)<br>
![UE5 Manny 简化](https://github.com/user-attachments/assets/296da51f-5aaf-413e-82f0-5fad727b75c9)<br>
<br>
**生成骨骼前缀与外型设定:**
可以透过插件的偏好设定(Preferences)，生成骨骼前缀(Generated Bonee's Prefix)，为不同类型的生成骨骼设定前缀。<br>
以及一般骨骼外型设定(General Bone Display Settings)设定个别类型骨骼的生成外型。<br>
![Preferences Prefix 介面](https://github.com/user-attachments/assets/97055744-7d85-451a-ad0b-3e23cd7f969b)<br>
![Preferences Display 介面](https://github.com/user-attachments/assets/21a7383d-d670-4286-a8b1-05ec5e527482)<br>
预设绑定与外型设定参考自: Jim Kroovy - Mr.Mannquins Tools<br>
<br>
## 动作重定向:
![Retarget Actions 介面](https://github.com/user-attachments/assets/b58710b8-3e7f-4bd6-8f94-ac57f3e87a93)<br>
### 重定向来源/目标设定(Mapping Source/Target Settings)
**来源类型(Source Type):** 可以选择骨架(Armature)或是动作(Action)。<br>
**骨架/动作(Armature/Action):** 作为来源的骨架或是动作。<br>
**目标骨架(Target):** 进行重定向的目标骨架。<br>
**製作重定向骨骼清单(Create Bone List):** 生成的清单会在下方骨骼对应清单列出。<br>
### 骨骼对应清单(Bone Mapping List)
左侧为来源骨骼，右侧为目标骨骼。<br>
<br>
**锁定对应清单(Lock Mapping List):** 锁定状态无法变更清单，避免误触修改。<br>
**目标骨骼(Target Bone):** 选中上方清单内的目标骨骼，在这个输入框进行改名。<br>
**汇入(Import)/汇出(Export):** 汇入或汇出重定向对应清单的json档，方便跨档案进行相似骨架的重定向。<br>
**选择要进行重定向的动作(Select Mapping Actions):** 选择要进行重定向的动作，动作的骨骼名称将从来源名称改成对应清单上右侧的目标名称。<br>
**应用骨骼对应到所选动作(Apply Mapping to Actions):** 将骨骼对应清单上的目标骨骼名称应用在上个操作选中的动作上。<br>

## 重命名工具:
![Rename Tool 介面](https://github.com/user-attachments/assets/3376cb1c-5b4d-4fa4-bcdb-b50ab54a50e5)<br>
**目标(Target):** 可选重命名顶点组(Vertex Group)或形状键(Shape key)。<br>
**重命名模式(Rename Mode):** 可选 寻找/取代(Find/Replace)、设置前缀/后缀(Set Prefix/Suffix)、移除前缀后缀(Remove Prefix/Suffix)。
