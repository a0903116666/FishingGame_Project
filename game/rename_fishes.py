import json
import os

def main():
    # 1. 讀取目前的 JSON
    try:
        with open('game/fishing_master_save.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ 找不到 fishing_master_save.json，請確認檔案位置！")
        return

    # 2. 將垃圾 (一星) 和魚類分開
    trashes = [r for r in data['records'] if r['id'] < 100]
    fishes = [r for r in data['records'] if r['id'] >= 100]

    # 3. 重新指派魚類的 ID (每滿 15 隻就進位到下一個星級)
    new_fishes = []
    current_star = 1  # 1 代表 100 系列 (UI 上的二星)
    count = 1
    
    rename_mapping = {} # 記錄 [舊ID -> 新ID] 的對應表

    for fish in fishes:
        old_id = fish['id']
        new_id = (current_star * 100) + count
        
        # 只要 ID 有變動，就記錄下來準備改檔名
        if old_id != new_id:
            rename_mapping[old_id] = new_id
            
        fish['id'] = new_id
        new_fishes.append(fish)
        
        count += 1
        if count > 15:
            count = 1
            current_star += 1

    # 將重新編排好的資料合併
    data['records'] = trashes + new_fishes

    # 4. 存成新的 JSON 檔案 (安全起見，我們存成另一個檔名)
    with open('game/new_fishing_master_save.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("✅ JSON 重新編號完成！已產生 'new_fishing_master_save.json'。")
    print("請確認無誤後，將它改名覆蓋原本的 fishing_master_save.json\n")

    # 5. 自動修改 game/ 資料夾下的圖片檔名
    print("-" * 30)
    print("🐟 開始重新命名圖片檔案...")
    
    rename_count = 0
    # 反向排序修改，避免 ID 衝突 (例如要把 201 改成 301，但 301 已經存在)
    for old_id, new_id in sorted(rename_mapping.items(), reverse=True):
        # 原圖與剪影圖的路徑
        old_img = f"fish_img/fish_{old_id}.png"
        new_img = f"fish_img/fish_{new_id}.png"

        # 修改原圖檔名
        if os.path.exists(old_img):
            os.rename(old_img, new_img)
            rename_count += 1
            
    print(f"✅ 圖片改名完成！共修改了 {rename_count} 個圖檔。")
    print("-" * 30)

if __name__ == "__main__":
    main()