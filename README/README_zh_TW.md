## 繁體中文
此插件主要為自定義Rigging設計，功能包括 **批量自訂骨骼顯示外型**、**生成約束**、**動作重定向** 以及 **批量重命名頂點組(Vertex Group)與形狀鍵(Shape Key)**。<br>
建議版本:Blender 4.2+ <br>
### 插件開啟位置
![開啟位置](https://github.com/user-attachments/assets/73be77a9-1e73-4666-939c-1b62c5013ef5)

### 功能目錄
>[Custom Display Shape 自訂骨骼顯示外型](#自訂骨骼顯示外型)<br>
>[Generate Constraint 生成約束](#生成約束)<br>
>[Retarget Actions 動作重定向](#動作重定向)<br>
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
![Bone Shape Folder](https://github.com/user-attachments/assets/ef193ba3-183a-4ed1-93c4-d7f5216064fd)<br>
<br>
如果要更改指定路徑，路徑資料夾中務必包含icons資料夾與BoneShapesLibrary.blend檔案。<br>
![Bone Shape Folder 內容](https://github.com/user-attachments/assets/c38f1537-ba94-487a-af14-72bbac9a8db5)<br>
***請在BoneShapesLibrary.blend中進行自訂顯示外型更改與操作。***<br>
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
**移除約束(Remove Constraints):** 移除所選骨骼的所有約束。<br>
### 生成變形骨(Generate Deform Bones)
某些DCC的骨骼軸向不同，這個功能可以幫助生成對應軸向的骨骼，或使用已有的軸向不同骨架綁定至Blender軸向骨架控制。<br>
生成的為虛擬變形骨，不會勾選變形選項，模型依然由Blender軸向骨骼進行控制，輸出時要轉換為變形骨時請使用BL-Export-to Unreal，勾選Use Virtul Deform。<br>
<br>
**生成變形骨(Generate Deform):** 為選中的骨骼生成對應軸向的變形骨。<br>
**UE5角色變形骨(UE5 Manny Deform):** 選中骨架為UE5骨架或是骨骼名稱與UE5預設Manny骨架相同，則會為有對應的骨骼生成變形骨。(僅限Manny_Simple)<br>
**連結變形骨骨架(Connect Deform Armature):** 將另一個DCC匯入且沒有進行軸向轉換的骨架，作為變形骨連結到在Blender中進行過軸向整理的骨架上。<br>
**全部設置反向(Set Inverse All):** 為所有選中的變形骨裡的 Child Of 約束執行設定反向。當動畫播放時變形骨沒有正確的鎖定在正確位置上時，請將骨架設為靜止位置(Rest Position)後選中變形骨執行此功能。<br>

### 生成約束(Generate Constraints)
**頭部(Head):** <br>
**脊椎(Spine):** <br>
**手臂(Arm):** <br>
**腿部(Leg):** <br>
**手指(Finger):** <br>
**UE5 角色(UE5 Manny):** <br>
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
