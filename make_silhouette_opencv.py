import cv2
import numpy as np
from pathlib import Path

# ================= 參數設定 =================
INPUT_DIR = 'fish_img'
OUTPUT_DIR = 'fish_silhouette'
# ============================================

def main():
    input_folder = Path(INPUT_DIR)
    output_folder = Path(OUTPUT_DIR)

    if not input_folder.exists():
        print(f"❌ 找不到資料夾 '{INPUT_DIR}'，請確認已經建立並放入圖片！")
        return

    output_folder.mkdir(parents=True, exist_ok=True)

    # 這次我們只抓取 png 檔案
    image_paths = list(input_folder.glob('*.png')) + list(input_folder.glob('*.PNG'))

    total_images = len(image_paths)
    if total_images == 0:
        print("⚠️ 在資料夾中沒有找到任何 PNG 圖片。")
        return

    print(f"🔍 總共找到 {total_images} 張圖片，啟動極速轉換...")
    print("-" * 30)

    count = 1
    for path in image_paths:
        img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
        
        if img is None:
            print(f"  ❌ 無法讀取圖片 {path.name}，已跳過。")
            count += 1
            continue

        if len(img.shape) < 3 or img.shape[2] != 4:
            print(f"  ⚠️ {path.name} 沒有透明通道(不是真正的去背圖)，已跳過。")
            count += 1
            continue

        try:
            # 1. 提取 Alpha 透明通道 (0 代表完全透明，1~255 代表有像素)
            alpha_channel = img[:, :, 3]
            
            # 2. 建立一張與原圖大小相同，且完全透明的空白畫布
            silhouette = np.zeros_like(img)
            
            # 3. 把原圖中「不透明」的地方 (alpha > 0)，在畫布上全部填滿純黑
            # 顏色格式為 (B, G, R, A)，所以 (0, 0, 0, 255) 就是不透明的黑色
            silhouette[alpha_channel > 0] = (0, 0, 0, 255)
            
            # 4. 存檔
            output_filename = f"{path.stem}_silhouette.png"
            output_path = output_folder / output_filename
            cv2.imwrite(str(output_path), silhouette)
            
            print(f"  ✅ 成功生成: {output_filename}")
            
        except Exception as e:
            print(f"  ❌ 處理 {path.name} 時發生錯誤: {e}")
            
        count += 1

    print("-" * 30)
    print("🎉 全部處理完成！")

if __name__ == "__main__":
    main()