## 繁體中文
此插件主要為自定義Rigging設計，功能包括 **批量自訂骨骼顯示外型**、**生成約束**、**動作重定向** 以及 **批量重命名頂點組(Vertex Group)與形狀鍵(Shape Key)**。<br>
建議版本:Blender 4.2+ <br>
### 插件開啟位置
![開啟位置](https://github.com/user-attachments/assets/73be77a9-1e73-4666-939c-1b62c5013ef5)

### 功能目錄
>[Custom Display Shape 自訂骨骼顯示外型](#自訂骨骼顯示外型)<br>
><br>
>[Generate Constraint 生成約束](#生成約束)<br>
><br>
>[Retarget Actions 動作重定向](#動作重定向)<br>
><br>
>[Rename Tool 重命名工具](#重命名工具)<br>

## 自訂骨骼顯示外型:
![custom display 介面](https://github.com/user-attachments/assets/db43d8e1-99ac-41ac-b1f4-d1e2ceda68d0)<br>
***需先進入姿態模式(Pose Mode)中選中要應用的骨骼。***
### 形狀(Shape)
![Shape 介面](https://github.com/user-attachments/assets/2839f568-a25a-4d11-a525-21115430b37d)<br>
下拉選擇要應用的形狀。<br>
![Shape 選擇](https://github.com/user-attachments/assets/c0ad7e09-9f54-49b4-95ea-a971c702edcf)<br>
**啟用骨骼長度(Enable Scale bone length):** 使編輯模式中的骨骼長度應用到自訂外型的大小。<br>
**應用骨骼顯示外型(Apply Bone Shape):** 應用所選中骨骼的顯示外型。<br>
### 顏色(Color)
![Bone Color](https://github.com/user-attachments/assets/035912f2-ff12-4a78-bed6-b45a4ae7d6a0)<br>
**Bone Color:** 在編輯模式下顯示的骨骼顏色。<br>
**Pose Bone Color:** 在姿態模式下顯示的骨骼顏色。<br>
**應用顏色(Apply Color):** 應用所選中骨骼的顯示顏色。<br>
### 比例(Scale)
![Bone Scale](https://github.com/user-attachments/assets/a7b6d259-1f72-42c5-884b-46acb876073a)<br>
勾選應用所有軸向比例(Enable Apply Scale All)時，會將骨骼外型的x、y、z軸比例應用為Scale All的值；不勾選時則可以分開調整。<br>
**應用比例(Apply Scale):** 應用所選中骨骼的顯示外型比例。<br>
### 位置(Translation)
![Bone Translation](https://github.com/user-attachments/assets/f48f7b29-deae-4434-bc65-258d2eebff1d)<br>
用於調整骨骼顯示外型的位置偏移。<br>
**應用位置(Apply Translation)**:應用骨骼顯示外型的位置偏移。<br>
### 旋轉(Rotation)
![Bone Rotation](https://github.com/user-attachments/assets/fd0e81ec-a656-4dc8-b4ba-71bf5cc48625)<br>
用於調整骨骼顯示外型的旋轉量。<br>
**應用旋轉(Apply Rotation):** 應用骨骼顯示外型的旋轉。<br>
### 應用全部(Apply All)
![Apply All](https://github.com/user-attachments/assets/d6f481fa-4afc-4c04-80a2-130da475da58)<br>
**從所選骨骼複製(Copy From Selected):** 從所選骨骼複製外型資訊。<br> 
**應用全部(Apply All):** 應用此區塊的所有設置。<br>
<br>
### 如何將外型加入顯示外型庫?
骨骼外型圖標與骨骼外型物件儲存於插件偏好的骨骼外型資料夾(Bone Shape Folder)，預設資料夾路徑為:<br>
插件位置\BLRigTool\addons\BLRigTool\assets<br>
![Bone Shape Folder](https://github.com/user-attachments/assets/7aab2626-55d7-4ebe-8c74-49b9c316de93)<br>
<br>
如果要更改指定路徑，路徑資料夾中務必包含icons資料夾與BoneShapesLibrary.blend檔案。<br>
![Bone Shape Folder 內容](https://github.com/user-attachments/assets/c38f1537-ba94-487a-af14-72bbac9a8db5)<br>
***請在BoneShapesLibrary.blend中進行自訂顯示外型更改與添加，存檔後，在另一個Blend檔中進行生成操作***<br>
<br>
要生成圖標的物件請在插件中選擇，不是在物件模式中選中的目標物件<br>
![生成 Shape 選擇](https://github.com/user-attachments/assets/f2587441-bccb-4994-b1d1-5c2b376c0add)<br>
下拉選單:<br>
![Shape 自訂](https://github.com/user-attachments/assets/d7468acc-b6ee-4348-87a2-a39b9cc9e48e)<br>
<br>
**為所選物件生成圖標(Generate Icon for selected object):** 詳見下方生成圖標設定。<br>
**移除圖標(Remove Icon):** 移除已生成的圖標。<br>
**重新載入骨骼外型圖標(Reload Bone Shape Icons):** 生成圖標後圖標沒有變化或是插件載入後沒有顯示圖標可以嘗試使用。<br>

**生成圖標設定:**<br>
>![Generate Icon](https://github.com/user-attachments/assets/d5d37a9f-1ddf-4704-9653-f2183bb5d126)<br>
><br>
>**攝像機距離(camera distance):** 擷取物件Icon的攝影機與物件的距離。<br>
>**攝像機角度(camera angle):** TOP:從上方擷取。/DIAGONAL:從斜對角擷取。<br>
>**保留生成(Keep generated camera & Light):** 在場景中保留生成Icons所使用的攝像機與燈光。如果生成時場景中已存在對應攝像機與燈光，則會優先使用。用於手動調整與預覽。<br>
><br>
>![Keep Generated](https://github.com/user-attachments/assets/e8364eab-7678-4827-b584-9d890f916bb0)<br>
><br>
>使用曲線(Curve)物件用於生成圖標前，需先在Curve data->Geometry->Bevel中給曲線一個厚度。<br>
>![Curve Bevel](https://github.com/user-attachments/assets/7e121715-0217-489e-9b3b-9efb5131926e)<br>

## 生成約束:
![Generate Constraint 介面](https://github.com/user-attachments/assets/9fe39eca-87d3-471e-8154-1c629c9121de)
### 移除約束(Remove Constraints)
![Remove Constraints 介面](https://github.com/user-attachments/assets/9e12e976-1add-44a3-a266-20264019e098)<br>
**移除約束(Remove Constraints):** 移除所選骨骼的所有約束。<br>
### 生成變形骨(Generate Deform Bones)
![Generate Deform Bones](https://github.com/user-attachments/assets/1dd29f81-4c0e-47cf-8b63-53ae11f9b2ec)<br>
某些DCC的骨骼軸向不同，這個功能可以幫助生成對應軸向的骨骼，或使用已有的軸向不同骨架綁定至Blender軸向骨架控制。<br>
生成的為虛擬變形骨，不會勾選變形選項，模型依然由Blender軸向骨骼進行控制，輸出時要轉換為變形骨時請使用BL-Export-to Unreal，勾選Use Virtul Deform。<br>
建議可以先把骨骼體綁定在角色身上完成調適後再進行虛擬變形骨的生成。<br>
<br>
**生成變形骨(Generate Deform):** 為選中的骨骼生成對應軸向的變形骨。<br>
![Generate Deform 介面](https://github.com/user-attachments/assets/122f4d03-7790-4b7d-bc10-ec4fde88f265)<br>
**XYZ-Axis:** 選擇生成骨骼的軸向對應。<br>
**生成位置(Position Base):** 選擇生成骨骼的生成位置，可以選擇在源骨骼的根部或是尾部。<br>
**群組名稱(Collection Name):** 自訂右方Data>Bone Collections的群組名稱。<br>
EX:<br>
![Generate Deform 示例](https://github.com/user-attachments/assets/46e50dcc-68f1-46e3-8259-f529a27b247a)<br>
X對應Y，Y對應X，Z對應-Z，在原骨骼根部生成。<br>

**UE5角色變形骨(UE5 Manny Deform):** 選中骨架為UE5骨架或是骨骼名稱與UE5預設Manny骨架相同，則會為有對應的骨骼生成變形骨。(僅限Manny_Simple)<br>
可以在物體模式(Object Mode)從Add>Armature>Add UE5 Manny(Simple)加入整理好的骨骼體。<br>
![Add UE5 Manny 介面](https://github.com/user-attachments/assets/ee825568-fad0-4c80-9ffb-b6f6d3adc941)<br>
接著進入姿態模式(Pose Mode)按下UE5 Manny Deform。<br>
![UE5 Manny Deform 示例](https://github.com/user-attachments/assets/dc65dfaf-8354-4bc5-b0ca-c8035fb7bf09)<br>
建議使用整理好的骨骼體或相同軸向與設定的骨骼體，才能生成完全對應UE5 Manny的虛擬變形骨。<br>

**連結變形骨骨架(Connect Deform Armature):** 將另一個DCC匯入且沒有進行軸向轉換的骨架，作為變形骨連結到在Blender中進行過軸向整理的骨架上。<br>
![Connect Deform Armature 介面](https://github.com/user-attachments/assets/b337c71c-c416-4fb8-9d0e-942116585003)<br>
![Connect Deform Armature 示例1](https://github.com/user-attachments/assets/6aecf963-1952-4d29-8717-5a7927da4c9e)<br>
![Connect Deform Armature 示例2](https://github.com/user-attachments/assets/6eb8c391-81d6-42bc-ba0d-8bf744476b85)<br>

**全部設置反向(Set Inverse All):** 為所有選中的變形骨裡的 Child Of 約束執行設定反向。當動畫播放時變形骨沒有正確的鎖定在正確位置上時，請將骨架設為靜止位置(Rest Position)後選中變形骨執行此功能。<br>

### 生成約束(Generate Constraints)
![Generate Constraints 生成約束](https://github.com/user-attachments/assets/163ce372-7c34-4702-a3d2-909c81e21c82)<br>
<br>
**頭部(Head):** <br>
![Head 介面](https://github.com/user-attachments/assets/1265137e-a29e-424b-86fe-6845852516f5)<br>
![Head 結果](https://github.com/user-attachments/assets/d77262a1-0d40-4f7a-a456-428fa08435f9)<br>
胸部(Chest)為脖子下方的骨骼。<br>
<br>
**脊椎(Spine):** <br>
![Spine 介面](https://github.com/user-attachments/assets/bfd76906-ca80-4bc4-ba82-8d5adf5c63be)<br>
![Spine 結果](https://github.com/user-attachments/assets/779a1955-4e5a-4417-977e-ffa3d8017e7d)<br>
<br>
**手臂(Arm):** <br>
![Arm 介面](https://github.com/user-attachments/assets/8eb0919e-19ee-49fa-a172-c6f97a914329)<br>
![Arm 結果](https://github.com/user-attachments/assets/716fe8a2-5fd5-4565-9976-c9e25766db04)<br>
手臂長度(Arm Length)為手掌上方骨骼的數量。<br>
<br>
**腿部(Leg):** <br>
![Leg 介面](https://github.com/user-attachments/assets/e1780c62-88d7-4fc1-a536-ce78ae005ffe)<br>
![Leg 結果](https://github.com/user-attachments/assets/fa28755d-4528-49f2-9084-8a7d3a851cfd)<br>
腿部長度(Leg Length)為腳掌上方骨骼的數量。<br>
是否生成腳趾(Is Create Toe)不勾選則不生成腳趾約束與控制器，適合沒有腳趾的骨骼體。<br>
<br>
**手指(Finger):** <br>
![Finger 介面](https://github.com/user-attachments/assets/85a807ae-1bda-4470-8a57-c795975de7f4)<br>
![Finger 結果](https://github.com/user-attachments/assets/6497c80b-0282-4d28-9e1f-c2cb2840c8f5)<br>
根骨骼(Root Bone)選擇手指最上方的骨骼。<br>
除了用來生成手指，也可以用來生成尾巴等長條狀部位。<br>
<br>
**UE5 角色(UE5 Manny):** <br>
![UE5 Manny 結果](https://github.com/user-attachments/assets/cd5fe69a-9a12-41d5-87c7-620ad9e1acef)<br>
為名稱與UE5 Manny(Simple)相同的骨骼生成控制器。<br>
可以適當的關閉一些骨骼群組，只留下主要的控制器。<br>
![UE5 Manny Collection 介面](https://github.com/user-attachments/assets/729ff6f7-324d-432e-8ef1-9945c2bfbf4e)<br>
![UE5 Manny 簡化](https://github.com/user-attachments/assets/296da51f-5aaf-413e-82f0-5fad727b75c9)<br>
<br>
**生成骨骼前綴與外型設定:**
可以透過插件的偏好設定(Preferences)，生成骨骼前綴(Generated Bonee's Prefix)，為不同類型的生成骨骼設定前綴。<br>
以及一般骨骼外型設定(General Bone Display Settings)設定個別類型骨骼的生成外型。<br>
![Preferences Prefix 介面](https://github.com/user-attachments/assets/97055744-7d85-451a-ad0b-3e23cd7f969b)<br>
![Preferences Display 介面](https://github.com/user-attachments/assets/21a7383d-d670-4286-a8b1-05ec5e527482)<br>
預設綁定與外型設定參考自: Jim Kroovy - Mr.Mannquins Tools<br>
<br>
## 動作重定向:
![Retarget Actions 介面](https://github.com/user-attachments/assets/b58710b8-3e7f-4bd6-8f94-ac57f3e87a93)<br>
### 重定向來源/目標設定(Mapping Source/Target Settings)
**來源類型(Source Type):** 可以選擇骨架(Armature)或是動作(Action)。<br>
**骨架/動作(Armature/Action):** 作為來源的骨架或是動作。<br>
**目標骨架(Target):** 進行重定向的目標骨架。<br>
**製作重定向骨骼清單(Create Bone List):** 生成的清單會在下方骨骼對應清單列出。<br>
### 骨骼對應清單(Bone Mapping List)
左側為來源骨骼，右側為目標骨骼。<br>
<br>
**鎖定對應清單(Lock Mapping List):** 鎖定狀態無法變更清單，避免誤觸修改。<br>
**目標骨骼(Target Bone):** 選中上方清單內的目標骨骼，在這個輸入框進行改名。<br>
**匯入(Import)/匯出(Export):** 匯入或匯出重定向對應清單的json檔，方便跨檔案進行相似骨架的重定向。<br>
**選擇要進行重定向的動作(Select Mapping Actions):** 選擇要進行重定向的動作，動作的骨骼名稱將從來源名稱改成對應清單上右側的目標名稱。<br>
**應用骨骼對應到所選動作(Apply Mapping to Actions):** 將骨骼對應清單上的目標骨骼名稱應用在上個操作選中的動作上。<br>

## 重命名工具:
![Rename Tool 介面](https://github.com/user-attachments/assets/3376cb1c-5b4d-4fa4-bcdb-b50ab54a50e5)<br>
**目標(Target):** 可選重命名頂點組(Vertex Group)或形狀鍵(Shape key)。<br>
**重命名模式(Rename Mode):** 可選 尋找/取代(Find/Replace)、設置前綴/後綴(Set Prefix/Suffix)、移除前綴後綴(Remove Prefix/Suffix)。
