import json
import os
from fish_data import FISH_MASTER_DATA

SAVE_FILENAME = "game/fishing_master_save.json"

class FishingSaveSystem:
    def __init__(self):
        self.player_dex_record = self.load_dex()

    def load_dex(self):
        """讀取 JSON 存檔。如果檔案不存在，則建立預設的空紀錄。"""
        if os.path.exists(SAVE_FILENAME):
            print(f"成功讀取存檔: {SAVE_FILENAME}")
            with open(SAVE_FILENAME, "r", encoding="utf-8") as file:
                return json.load(file)
        else:
            print(f"存檔不存在，正在建立新的存檔: {SAVE_FILENAME}")
            return self._initialize_new_save()

    def _initialize_new_save(self):
        """根據 Master Data 初始化所有魚類的個人紀錄。"""
        new_save_data = {
            "player_id": "single_player_001",
            "records": []
        }

        for fish in FISH_MASTER_DATA["fish_list"]:
            fish_record = {
                "id": fish["id"],
                "name": fish["name"], # 為了除錯方便可選，真正存檔只需 ID
                "is_unlocked": False,   # 初始化為 False
                "max_weight": 0.0,      # kg
                "catch_count": 0        # 次數
            }
            new_save_data["records"].append(fish_record)
        
        self._write_save(new_save_data)
        return new_save_data

    def _write_save(self, data):
        """將玩家紀錄寫入 JSON 檔案。"""
        with open(SAVE_FILENAME, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def on_fish_caught(self, fish_id, weight):
        print(f"\n--- 系統判定：釣獲魚 ID: {fish_id}, 重量: {weight} kg ---")
        
        updated_any = False
        new_unlock = False

        for record in self.player_dex_record["records"]:
            if record["id"] == fish_id:
                record["catch_count"] += 1

                if not record["is_unlocked"]:
                    record["is_unlocked"] = True
                    new_unlock = True
                    print(f"✨ 恭喜！您第一次釣到了【{record['name']}】，已成功解鎖圖鑑！")

                if weight > record["max_weight"]:
                    old_record = record["max_weight"]
                    record["max_weight"] = weight
                    print(f"🏆 打破紀錄啦！【{record['name']}】的新最大重量：{weight} kg (舊紀錄: {old_record} kg)")
                updated_any = True
                break 
        
        if updated_any:
            self._write_save(self.player_dex_record)
            print(f"存檔更新完成。")
        else:
            print(f"⚠️ 警告： Master Data 中找不到 ID 為 {fish_id} 的魚類資訊，存檔未更新。")

        return new_unlock 

    def get_fish_save_data(self, fish_id):
        for record in self.player_dex_record["records"]:
            if record["id"] == fish_id:
                return record