# BL Rig Tool
![介面](https://github.com/user-attachments/assets/0391e35a-4d71-4d08-bf5d-0a76a7b60f7d)<br><br>
[English](#english) | [繁體中文](#繁體中文)

---

## English

---

## 繁體中文
此插件主要為自定義Rigging設計，功能包括 **批量自訂骨骼顯示外型**、**生成約束(BETA)**、**動作重定向** 以及 **批量重命名頂點組(Vertex Group)與形狀鍵(Shape Key)**。<br>
建議版本:Blender 4.2+ <br>
### 插件開啟位置
![開啟位置](https://github.com/user-attachments/assets/73be77a9-1e73-4666-939c-1b62c5013ef5)

### 功能目錄
>[Custom Display Shape 自訂骨骼顯示外型](#自訂骨骼顯示外型)<br>
>[Generate Constraint 生成約束(BETA)](#生成約束)<br>
>[Retarget Actions 動作重定向](#動作重定向)<br>
>[Rename Tool 重命名工具](#重命名工具)<br>


## 自訂骨骼顯示外型:
![custom display 介面](https://github.com/user-attachments/assets/91cb8dfc-8ab2-4bac-b643-c02a21b829de)<br>
***需先進入姿態模式(Pose Mode)中選中要應用的骨骼。***
### 形狀(Shape)
下拉選擇要應用的形狀。<br>
![Shape 選擇](https://github.com/user-attachments/assets/c0ad7e09-9f54-49b4-95ea-a971c702edcf)<br>
**啟用骨骼長度**(Enable Scale bone length):使編輯模式中的骨骼長度應用到自訂外型的大小。<br>
**應用骨骼顯示外型(Apply Bone Shape)**:應用所選中骨骼的顯示外型。<br>
<br>
#### 將外型加入顯示外型庫
骨骼外型圖標與骨骼外型物件儲存於插件偏好的骨骼外型資料夾(Bone Shape Folder)，預設資料夾路徑為:<br>
插件位置\BLRigTool\addons\BLRigTool\assets<br>
![Bone Shape Folder](https://github.com/user-attachments/assets/ea98f24a-fde7-46a2-bca4-2f46256356ee)<br>
如果要更改指定路徑，路徑資料夾中務必包含icons資料夾與BoneShapesLibrary.blend檔案。<br>
![Bone Shape Folder 內容](https://github.com/user-attachments/assets/c38f1537-ba94-487a-af14-72bbac9a8db5)<br>
**請在BoneShapesLibrary.blend中進行自訂顯示外型操作。**<br>
<br>
生成圖標的物件請在插件中選擇，不是在物件模式中選中的目標物件<br>
![生成 Shape 選擇](https://github.com/user-attachments/assets/f2587441-bccb-4994-b1d1-5c2b376c0add)<br>
下拉選單:<br>
![Shape 自訂](https://github.com/user-attachments/assets/d7468acc-b6ee-4348-87a2-a39b9cc9e48e)<br>
**為所選物件生成圖標(Generate Icon for selected object)**<br>

>彈出生成圖標設定視窗:<br>
>![Generate Icon](https://github.com/user-attachments/assets/d5d37a9f-1ddf-4704-9653-f2183bb5d126)<br>
>**攝像機距離(camera distance)**:擷取物件Icon的攝影機與物件的距離。<br>
>**攝像機角度(camera angle)**:TOP:從上方擷取。/DIAGONAL:從斜對角擷取。<br>
>**保留生成(Keep generated camera & Light)**:在場景中保留生成Icons所使用的攝像機與燈光。如果生成時場景中已存在對應攝像機與燈光，則會優先使用。用於手動調整與預覽。<br>
>![Keep Generated](https://github.com/user-attachments/assets/e8364eab-7678-4827-b584-9d890f916bb0)<br>
>使用曲線(Curve)物件用於生成圖標前，需先在Curve data->Geometry->Bevel中給曲線一個厚度。<br>
>![Curve Bevel](https://github.com/user-attachments/assets/7e121715-0217-489e-9b3b-9efb5131926e)<br>

**移除圖標(Remove Icon)**:移除已生成的圖標。<br>
**重新載入骨骼外型圖標(Reload Bone Shape Icons)**:生成圖標後圖標沒有變化或是插件載入後沒有顯示圖標可以嘗試使用。<br>
### 顏色(Color)
![Bone Color](https://github.com/user-attachments/assets/035912f2-ff12-4a78-bed6-b45a4ae7d6a0)<br>
**Bone Color**:在編輯模式下顯示的骨骼顏色。<br>
**Pose Bone Color**:在姿態模式下顯示的骨骼顏色。<br>
**應用顏色(Apply Color)**:應用所選中骨骼的顯示顏色。<br>
### 比例(Scale)
![Bone Scale](https://github.com/user-attachments/assets/a7b6d259-1f72-42c5-884b-46acb876073a)<br>
勾選應用所有軸向比例(Enable Apply Scale All)時，會將骨骼外型的x、y、z軸比例應用為Scale All的值；不勾選時則可以分開調整。<br>
**應用比例(Apply Scale)**:應用所選中骨骼的顯示外型比例。<br>
### 位置(Translation)
![Bone Translation](https://github.com/user-attachments/assets/f48f7b29-deae-4434-bc65-258d2eebff1d)<br>
用於調整骨骼顯示外型的位置偏移。<br>
**應用位置(Apply Translation)**:應用骨骼顯示外型的位置偏移。<br>
### 旋轉(Rotation)
![Bone Rotation](https://github.com/user-attachments/assets/fd0e81ec-a656-4dc8-b4ba-71bf5cc48625)<br>
用於調整骨骼顯示外型的旋轉量。<br>
**應用旋轉(Apply Rotation)**:應用骨骼顯示外型的旋轉。<br>
### 應用全部(Apply All)
![Apply All](https://github.com/user-attachments/assets/32b3c239-8b3c-41e9-8149-b594e21a58d6)<br>
應用此區塊的所有設置。<br>

## 生成約束:
![Generate Constraint 介面](https://github.com/user-attachments/assets/f8d1bc60-eddb-4234-88cf-e13fd637e3fa)
###

## 動作重定向:
![Retarget Actions 介面](https://github.com/user-attachments/assets/b58710b8-3e7f-4bd6-8f94-ac57f3e87a93)
###

## 重命名工具:
![Rename Tool 介面](https://github.com/user-attachments/assets/3376cb1c-5b4d-4fa4-bcdb-b50ab54a50e5)
###
