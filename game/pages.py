import pygame
import sys
import json
from config import *
from body_control import body_cursor
from fish_data import get_fish_data, FISH_MASTER_DATA

def homepage_menu():
    pygame.display.set_caption("2D 體感釣魚大師 - 首頁")

    homepage_image = pygame.image.load("game/assets/homepage_menu.png").convert_alpha()
    resized_hompage_image = pygame.transform.smoothscale(homepage_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    game_start_button = pygame.image.load("game/assets/GameStart_button.png").convert_alpha()
    resized_game_start_button = pygame.transform.smoothscale(game_start_button, (200, 80))
    game_start_triggered_button = pygame.transform.smoothscale(game_start_button, (220, 88))
    
    game_exit_button = pygame.image.load("game/assets/GameExit_button.png").convert_alpha()
    resized_game_exit_button = pygame.transform.smoothscale(game_exit_button, (200, 80))
    game_exit_triggered_button = pygame.transform.smoothscale(game_exit_button, (220, 88))
    
    digital_field_guide_button = pygame.image.load("game/assets/DigitalFieldGuide_button.png").convert_alpha()
    resized_digital_field_guide_button = pygame.transform.smoothscale(digital_field_guide_button, (200, 80))
    digital_field_guide_triggered_button = pygame.transform.smoothscale(digital_field_guide_button, (220, 88))
    
    hand_cursor_image = pygame.image.load("game/assets/HandCursor.png").convert_alpha()
    resized_hand_cursor_image = pygame.transform.smoothscale(hand_cursor_image, (50, 50))

    progress_arc = pygame.image.load("game/assets/progressArc.png").convert_alpha()

    DWELL_THRESHOLD = 1.0  
    hovered_button = None
    hover_start_time = 0.0
    ratio = 0.0

    waiting_for_input = True
    while waiting_for_input:
        current_time = pygame.time.get_ticks() / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        cursor_x, cursor_y = body_cursor()
        cursor_pixel_x = max(min((cursor_x + 0.5) * WINDOW_WIDTH, WINDOW_WIDTH - 50), 50)
        cursor_pixel_y = max(min((cursor_y + 0.5) * WINDOW_HEIGHT, WINDOW_HEIGHT - 50), 50)

        current_hover = None
        if ((WINDOW_HEIGHT // 2 + 15 - 75) < cursor_pixel_y < (WINDOW_HEIGHT // 2 + 15 + 5)) and ((WINDOW_WIDTH // 2 - 100) < cursor_pixel_x < (WINDOW_WIDTH // 2 + 100)):
            current_hover = "start"
        elif ((WINDOW_HEIGHT // 2 + 15) < cursor_pixel_y < (WINDOW_HEIGHT // 2 + 15 + 80)) and ((WINDOW_WIDTH // 2 - 100) < cursor_pixel_x < (WINDOW_WIDTH // 2 + 100)):
            current_hover = "exit"
        elif ((WINDOW_HEIGHT // 2 + 15 + 75) < cursor_pixel_y < (WINDOW_HEIGHT // 2 + 15 + 155)) and ((WINDOW_WIDTH // 2 - 100) < cursor_pixel_x < (WINDOW_WIDTH // 2 + 100)):
            current_hover = "guide"

        if current_hover != hovered_button:
            hovered_button = current_hover
            hover_start_time = current_time
            ratio = 0.0
        else:
            if hovered_button is not None:
                ratio = (current_time - hover_start_time) / DWELL_THRESHOLD
                if ratio >= 1.0:
                    if hovered_button == "start":
                        print("觸發：開始遊戲")
                        #return "start" 
                    elif hovered_button == "exit":
                        print("觸發：退出遊戲")
                        #pygame.quit()
                        #sys.exit()
                    elif hovered_button == "guide":
                        print("觸發：進入數位圖鑑")
                        #return "guide" 

        SCREEN.blit(resized_hompage_image, (0, 0))

        if hovered_button == "start":
            SCREEN.blit(game_start_triggered_button, (WINDOW_WIDTH // 2 - 110, (WINDOW_HEIGHT // 2) + 15 - 80))
        else:
            SCREEN.blit(resized_game_start_button, (WINDOW_WIDTH // 2 - 100, (WINDOW_HEIGHT // 2) + 15 - 75))

        if hovered_button == "exit":
            SCREEN.blit(game_exit_triggered_button, (WINDOW_WIDTH // 2 - 110, (WINDOW_HEIGHT // 2) + 10))
        else:
            SCREEN.blit(resized_game_exit_button, (WINDOW_WIDTH // 2 - 100, (WINDOW_HEIGHT // 2) + 15))

        if hovered_button == "guide":
            SCREEN.blit(digital_field_guide_triggered_button, (WINDOW_WIDTH // 2 -110 , (WINDOW_HEIGHT // 2) + 10 + 70))
        else:
            SCREEN.blit(resized_digital_field_guide_button, (WINDOW_WIDTH // 2 - 100, (WINDOW_HEIGHT // 2) + 15 + 75))

        if ratio > 0.0:
            for i in range(int(ratio * 8 + 0.5)):
                rotated_arc = pygame.transform.rotate(progress_arc, -45 * i)
                arc_rect = rotated_arc.get_rect(center=(cursor_pixel_x, cursor_pixel_y))
                SCREEN.blit(rotated_arc, arc_rect)

        SCREEN.blit(resized_hand_cursor_image, (cursor_pixel_x - 25, cursor_pixel_y - 25))
        
        pygame.display.flip()

def game_menu():
    pygame.display.set_caption("2D 體感釣魚大師 - 遊戲選單")

    menu_image = pygame.image.load("game/assets/game_menu.png").convert_alpha()
    resized_menu_image = pygame.transform.smoothscale(menu_image, (400, 440))
    
    homepage_button = pygame.image.load("game/assets/backtohomepage_button.png").convert_alpha()
    resized_homepage_button = pygame.transform.smoothscale(homepage_button, (300, 120))
    triggered_homepage_button = pygame.transform.smoothscale(homepage_button, (310, 130))
    
    exit_button = pygame.image.load("game/assets/exitgame_button.png").convert_alpha()
    resized_exit_button = pygame.transform.smoothscale(exit_button, (300, 120))
    triggered_exit_button = pygame.transform.smoothscale(exit_button, (310, 130))
    
    digital_field_guide_button = pygame.image.load("game/assets/gotodigitalfieldguide_button.png").convert_alpha()
    resized_digital_field_guide_button = pygame.transform.smoothscale(digital_field_guide_button, (300, 120))
    triggered_digital_field_guide_button = pygame.transform.smoothscale(digital_field_guide_button, (310, 130))
    
    hand_cursor_image = pygame.image.load("game/assets/HandCursor.png").convert_alpha()
    resized_hand_cursor_image = pygame.transform.smoothscale(hand_cursor_image, (50, 50))

    progress_arc = pygame.image.load("game/assets/progressArc.png").convert_alpha()

    background_snapshot = SCREEN.copy() 

    darken_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    darken_overlay.fill((0, 0, 0, 120)) 
    background_snapshot.blit(darken_overlay, (0, 0))

    DWELL_THRESHOLD = 1.0 
    hovered_button = None  
    hover_start_time = 0.0 
    ratio = 0.0           

    waiting_for_input = True
    while waiting_for_input:
        current_time = pygame.time.get_ticks() / 1000.0 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_input = False
        
        cursor_x, cursor_y = body_cursor()
        cursor_pixel_x = max(min((cursor_x + 0.5) * WINDOW_WIDTH, WINDOW_WIDTH - 50), 50)
        cursor_pixel_y = max(min((cursor_y + 0.5) * WINDOW_HEIGHT, WINDOW_HEIGHT - 50), 50)

        current_hover = None
        if ((WINDOW_HEIGHT // 2 - 150) < cursor_pixel_y < (WINDOW_HEIGHT // 2 - 30)) and ((WINDOW_WIDTH // 2 - 140) < cursor_pixel_x < (WINDOW_WIDTH // 2 + 160)):
            current_hover = "homepage"
        elif ((WINDOW_HEIGHT // 2 - 75) < cursor_pixel_y < (WINDOW_HEIGHT // 2 + 45)) and ((WINDOW_WIDTH // 2 - 140) < cursor_pixel_x < (WINDOW_WIDTH // 2 + 160)):
            current_hover = "exit"
        elif ((WINDOW_HEIGHT // 2 ) < cursor_pixel_y < (WINDOW_HEIGHT // 2 + 120)) and ((WINDOW_WIDTH // 2 - 140) < cursor_pixel_x < (WINDOW_WIDTH // 2 + 160)):
            current_hover = "guide"

        if current_hover != hovered_button:
            hovered_button = current_hover
            hover_start_time = current_time
            ratio = 0.0
        else:
            if hovered_button is not None:
                ratio = (current_time - hover_start_time) / DWELL_THRESHOLD
                
                if ratio >= 1.0:
                    if hovered_button == "homepage":
                        print("觸發：返回主頁面")
                        #return "homepage" 
                    elif hovered_button == "exit":
                        print("觸發：退出遊戲")
                        #pygame.quit()
                        #sys.exit()
                    elif hovered_button == "guide":
                        print("觸發：進入數位圖鑑")
                        #return "guide"
        
        SCREEN.blit(background_snapshot, (0, 0))

        SCREEN.blit(resized_menu_image, (WINDOW_WIDTH // 2 - 200, (WINDOW_HEIGHT // 2) - 220))
        if hovered_button == "homepage":
            SCREEN.blit(triggered_homepage_button, (WINDOW_WIDTH // 2 - 140, (WINDOW_HEIGHT // 2) - 150))
        else:
            SCREEN.blit(resized_homepage_button, (WINDOW_WIDTH // 2 - 140, (WINDOW_HEIGHT // 2) - 150))

        if hovered_button == "exit":
            SCREEN.blit(triggered_exit_button, (WINDOW_WIDTH // 2 - 140, (WINDOW_HEIGHT // 2) - 75))
        else:
            SCREEN.blit(resized_exit_button, (WINDOW_WIDTH // 2 - 140, (WINDOW_HEIGHT // 2) - 75))

        if hovered_button == "guide":
            SCREEN.blit(triggered_digital_field_guide_button, (WINDOW_WIDTH // 2 - 140, (WINDOW_HEIGHT // 2)))
        else:
            SCREEN.blit(resized_digital_field_guide_button, (WINDOW_WIDTH // 2 - 140, (WINDOW_HEIGHT // 2)))

        if ratio > 0.0:
            for i in range(int(ratio * 8 + 0.5)):
                rotated_arc = pygame.transform.rotate(progress_arc, -45 * i)
                arc_rect = rotated_arc.get_rect(center=(cursor_pixel_x, cursor_pixel_y))
                SCREEN.blit(rotated_arc, arc_rect)

        SCREEN.blit(resized_hand_cursor_image, (cursor_pixel_x - 25, cursor_pixel_y - 25))
        pygame.display.flip()

def digital_field_guide():
    pygame.display.set_caption("2D 體感釣魚大師 - 數位圖鑑")
    try:
        digital_field_background = pygame.image.load("game/assets/DigitalFieldGuide_background.png").convert_alpha()
        digital_field_guide_button = pygame.image.load("game/assets/button.png").convert_alpha()
        hand_cursor_image = pygame.image.load("game/assets/HandCursor.png").convert_alpha()
        progress_arc = pygame.image.load("game/assets/ProgressArc.png").convert_alpha()
    except FileNotFoundError:
        print("⚠️ 警告：找不到部分 UI 圖片，請確認 game/assets/ 資料夾下有對應檔案。")
        return

    resized_digital_field_background = pygame.transform.smoothscale(digital_field_background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    resized_digital_field_guide_button = pygame.transform.smoothscale(digital_field_guide_button, (205, 85))
    resized_hand_cursor_image = pygame.transform.smoothscale(hand_cursor_image, (50, 50))
    progress_arc = pygame.transform.smoothscale(progress_arc, (50, 50))
    
    display_columns = {}
    
    for i in range(1, 6):
        img_path = f"game/assets/{i}star_column.png" 
        column_img = pygame.image.load(img_path).convert_alpha()
        display_columns[i] = pygame.transform.smoothscale(column_img, (600, 440))

    base_x = WINDOW_WIDTH // 2 - 350
    base_y = WINDOW_HEIGHT // 2 - 120
    buttons = []
    
    for i in range(1, 6):
        try:
            normal_img = pygame.image.load(f"game/assets/{i}star.png").convert_alpha()
            buttons.append({
                "star_level": i,
                "normal_img": pygame.transform.smoothscale(normal_img, (200, 80)),
                "hover_img": pygame.transform.smoothscale(normal_img, (220, 88)),
                "normal_pos": (base_x, base_y + (i - 1) * 60),
                "hover_pos": (base_x - 10, base_y + (i - 1) * 60 - 5),
                "rect": pygame.Rect(base_x, base_y + (i - 1) * 60, 200, 80) 
            })
        except FileNotFoundError:
            print(f"⚠️ 找不到按鈕圖片 game/assets/{i}star.png")

    try:
        with open('game/fishing_master_save.json', 'r', encoding='utf-8') as f:
            player_data = json.load(f)
            records = player_data.get("records", [])
    except FileNotFoundError:
        print("⚠️ 找不到 fishing_master_save.json，圖鑑將呈現空白狀態。")
        records = []

    loaded_fishes = {1: [], 2: [], 3: [], 4: [], 5: []}

    FISH_SIZE = (64, 64)
    COLS = 5
    SPACING_X = 75
    SPACING_Y = 85
    START_X = 275 
    START_Y = 140
    fish_counters = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    dummy_fish_surface = pygame.Surface(FISH_SIZE)
    dummy_fish_surface.fill((150, 0, 150)) # 解鎖魚的預設顏色

    dummy_silhouette_surface = pygame.Surface(FISH_SIZE)
    dummy_silhouette_surface.fill((100, 100, 100)) # 未解鎖魚的預設顏色

    for record in records:
        fish_id = record["id"]
        is_unlocked = record["is_unlocked"]
        
        if fish_id < 100:
            star_level = 1  
        else:
            star_level = (fish_id // 100) + 1  
            
        if star_level > 5 or star_level < 1: 
            continue

        img_path = f"fish_img/fish_{fish_id}.png" if is_unlocked else f"fish_silhouette/fish_{fish_id}_silhouette.png"

        try:
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.smoothscale(img, FISH_SIZE)
        except FileNotFoundError:
            img = pygame.Surface(FISH_SIZE)
            img.fill((150, 0, 150))

        current_index = fish_counters[star_level]
        row, col = current_index // COLS, current_index % COLS
        fish_pos = (START_X + (col * SPACING_X), START_Y + (row * SPACING_Y))

        loaded_fishes[star_level].append({
            "img": img,
            "pos": fish_pos,
            "rect": pygame.Rect(fish_pos[0], fish_pos[1], FISH_SIZE[0], FISH_SIZE[1]), 
            "data": record
        })
        fish_counters[star_level] += 1

    current_displayed_star = 1   
    hovered_button_index = None  

    hovered_fish_id = None       # 正在懸停哪隻魚
    show_modal = False           # 彈出視窗是否開啟
    selected_fish_record = None  # 目前選中了哪隻魚的資料
    
    hover_start_time = 0         
    DWELL_THRESHOLD = 1000       # 懸停 1 秒觸發
    ratio = 0.0                  # 進度條比例

    try:
        modal_bg = pygame.image.load("game/assets/display_icon-removebg-preview.png").convert_alpha()
        modal_bg = pygame.transform.smoothscale(modal_bg, (700, 400)) 
    except FileNotFoundError:
        print("⚠️ 找不到魚圖鑑底圖 game/assets/fish_display_column.png，暫用色塊代替")
        modal_bg = pygame.Surface((500, 400))
        modal_bg.fill((220, 200, 160)) 
        
    modal_rect = modal_bg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    try:
        close_icon_asset = pygame.image.load("game/assets/cross.png").convert_alpha()
        close_icon_asset = pygame.transform.smoothscale(close_icon_asset, (100, 100))
    except FileNotFoundError:
        print("⚠️ 找不到關閉圖示 game/assets/cross.png，將使用Fallback。")
        close_icon_asset = pygame.Surface((100, 100), pygame.SRCALPHA)
        close_icon_asset.fill((0,0,0,0))
        pygame.draw.line(close_icon_asset, (200, 0, 0), (10, 10), (90, 90), 5)
        pygame.draw.line(close_icon_asset, (200, 0, 0), (90, 10), (10, 90), 5)

    close_icon = close_icon_asset

    pygame.display.flip()
    waiting_for_input = True
    
    while waiting_for_input:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:  
                    waiting_for_input = False 

        cursor_x, cursor_y = pygame.mouse.get_pos()
        cursor_x = cursor_x / WINDOW_WIDTH - 0.5
        cursor_y = cursor_y / WINDOW_HEIGHT - 0.5
        cursor_pixel_x = max(min((cursor_x + 0.5) * WINDOW_WIDTH, WINDOW_WIDTH - 50), 50)
        cursor_pixel_y = max(min((cursor_y + 0.5) * WINDOW_HEIGHT, WINDOW_HEIGHT - 50), 50)

        SCREEN.blit(resized_digital_field_background, (0, 0))
        SCREEN.blit(resized_digital_field_guide_button, (WINDOW_WIDTH // 2 - 355, (WINDOW_HEIGHT // 2) - 180))
        SCREEN.blit(display_columns[current_displayed_star], (WINDOW_WIDTH // 2 - 200, (WINDOW_HEIGHT // 2) - 200))

        for fish in loaded_fishes[current_displayed_star]:
            SCREEN.blit(fish["img"], fish["pos"])

        is_hovering_something = False

        if not show_modal:
            for i, btn in enumerate(buttons):
                if btn["rect"].collidepoint(cursor_pixel_x, cursor_pixel_y):
                    is_hovering_something = True
                    SCREEN.blit(btn["hover_img"], btn["hover_pos"]) 
                    
                    if hovered_button_index != i:
                        hovered_button_index = i
                        hover_start_time = current_time
                        ratio = 0.0
                    else:
                        ratio = (current_time - hover_start_time) / DWELL_THRESHOLD
                        if current_time - hover_start_time >= DWELL_THRESHOLD:
                            if current_displayed_star != btn["star_level"]:
                                current_displayed_star = btn["star_level"]
                                ratio = 0.0
                else:
                    SCREEN.blit(btn["normal_img"], btn["normal_pos"])
            if not is_hovering_something:
                for fish in loaded_fishes[current_displayed_star]:
                    if fish["rect"].collidepoint(cursor_pixel_x, cursor_pixel_y) and fish["data"]["is_unlocked"]:
                        is_hovering_something = True

                        pygame.draw.rect(SCREEN, (255, 215, 0), fish["rect"].inflate(10, 10), 3, border_radius=5)
                        
                        if hovered_fish_id != fish["data"]["id"]:
                            hovered_fish_id = fish["data"]["id"]
                            hover_start_time = current_time
                            ratio = 0.0
                        else:
                            ratio = (current_time - hover_start_time) / DWELL_THRESHOLD
                            if current_time - hover_start_time >= DWELL_THRESHOLD:
                                show_modal = True
                                selected_fish_record = fish["data"]
                                ratio = 0.0
                                hover_start_time = current_time 
                        break 

        else:
            for btn in buttons:
                SCREEN.blit(btn["normal_img"], btn["normal_pos"])

            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            SCREEN.blit(overlay, (0, 0))

            SCREEN.blit(modal_bg, modal_rect.topleft)

            close_X_rect = close_icon.get_rect()
            close_X_rect.right = modal_rect.right - 10
            close_X_rect.top = modal_rect.top + 10

            SCREEN.blit(close_icon, close_X_rect.topleft)

            master_data = get_fish_data(selected_fish_record["id"])

            title_font = pygame.font.Font("game/assets/pixel_font.ttf", 32)
            desc_font = pygame.font.Font("game/assets/pixel_font.ttf", 20)
            title_color = (60, 40, 20)
            desc_color = (100, 80, 60)

            title_surface = title_font.render(master_data["name"], True, title_color)
            title_x = modal_rect.centerx - (title_surface.get_width() // 2)
            title_y = modal_rect.top + 10 
            SCREEN.blit(title_surface, (title_x, title_y))

            level_surface = desc_font.render(f"星級: {master_data['level']}  捕獲次數: {master_data['catch_count']}  最大重量: {master_data['max_weight']}", True, title_color)
            level_x = modal_rect.centerx - (level_surface.get_width() // 2 )
            level_y = modal_rect.bottom - 150 
            SCREEN.blit(level_surface, (level_x, level_y))

            full_text = master_data["comment"]
            lines = []

            for i in range(0, len(full_text), 16):
                single_line = full_text[i:i+16]
                lines.append(single_line)
                
            base_y = modal_rect.bottom - 120 
            line_height = 28  
            
            for index in range(len(lines)):
                line_text = lines[index]
                comment_surface = desc_font.render(line_text, True, desc_color)
                comment_x = modal_rect.centerx - (comment_surface.get_width() // 2)
                comment_y = base_y + (index * line_height)

                SCREEN.blit(comment_surface, (comment_x, comment_y))

            img_id = selected_fish_record["id"]
            img_path = f"fish_img/fish_{img_id}.png" 

            try:
                big_fish_surf = pygame.image.load(img_path).convert_alpha()
                scaled_big_fish = pygame.transform.smoothscale(big_fish_surf, (96, 96))
                SCREEN.blit(scaled_big_fish, (modal_rect.centerx - 48, modal_rect.top + 110))
            except FileNotFoundError:
                print(f"⚠️ 找不到放大魚圖: {img_path}")

            if close_X_rect.collidepoint(cursor_pixel_x, cursor_pixel_y):
                is_hovering_something = True # 用於通用計時器邏輯

                if hovered_fish_id != "close_button":
                    hovered_fish_id = "close_button"
                    hover_start_time = current_time
                    ratio = 0.0
                else:
                    ratio = (current_time - hover_start_time) / DWELL_THRESHOLD
                    if current_time - hover_start_time >= DWELL_THRESHOLD:
                        show_modal = False
                        selected_fish_record = None
                        ratio = 0.0
            else:
                pass
        if not is_hovering_something:
            hovered_button_index = None
            hovered_fish_id = None
            ratio = 0.0

        if ratio > 0.0:
            for i in range(int(ratio * 8 + 0.5)):
                # rotate 45 degree and draw again
                rotated_arc = pygame.transform.rotate(progress_arc, -45 * i)
                arc_rect = rotated_arc.get_rect(center=(cursor_pixel_x, cursor_pixel_y))
                SCREEN.blit(rotated_arc, arc_rect)
                
        SCREEN.blit(resized_hand_cursor_image, (cursor_pixel_x - 25, cursor_pixel_y - 25))
        
        pygame.display.flip()

def settle_menu(fish_id, weight, is_new_record, is_new_species):
    pygame.display.set_caption("2D 體感釣魚大師 - 結算畫面")

    settle_image = pygame.image.load("game/assets/settle_column2.png").convert_alpha()
    resized_settle_image = pygame.transform.smoothscale(settle_image, (650, 440))

    continue_button = pygame.image.load("game/assets/continue_button.png").convert_alpha()
    resized_continue_button = pygame.transform.smoothscale(continue_button, (250, 100))
    triggered_continue_button = pygame.transform.smoothscale(continue_button, (270, 110))

    go_to_digital_field_guide_button = pygame.image.load("game/assets/gotoguide_button.png").convert_alpha()
    resized_go_to_digital_field_guide_button = pygame.transform.smoothscale(go_to_digital_field_guide_button, (250, 100))
    triggered_go_to_digital_field_guide_button = pygame.transform.smoothscale(go_to_digital_field_guide_button, (270, 110))

    new_record_image = pygame.image.load("game/assets/new_record.png").convert_alpha()
    resized_new_record_image = pygame.transform.smoothscale(new_record_image, (300, 150))

    new_species_image = pygame.image.load("game/assets/new_species.png").convert_alpha()
    resized_new_species_image = pygame.transform.smoothscale(new_species_image, (300, 150))
        
    hand_cursor_image = pygame.image.load("game/assets/HandCursor.png").convert_alpha()
    resized_hand_cursor_image = pygame.transform.smoothscale(hand_cursor_image, (50, 50))

    progress_arc = pygame.image.load("game/assets/progressArc.png").convert_alpha()

    background_snapshot = SCREEN.copy()
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    background_snapshot.blit(overlay, (0, 0)) 

    title_font = pygame.font.Font("game/assets/pixel_font.ttf", 32)
    desc_font = pygame.font.Font("game/assets/pixel_font.ttf", 20)
    title_color = (60, 40, 20) 
    desc_color = (100, 80, 60) 

    fish = get_fish_data(int(fish_id))
    if fish:
        img_path = f"fish_img/fish_{fish['id']}.png"
        fish_image = pygame.image.load(img_path).convert_alpha()
        resized_fish_image = pygame.transform.smoothscale(fish_image, (128, 128))

    DWELL_THRESHOLD = 1.0  
    hovered_button = None
    hover_start_time = 0.0
    ratio = 0.0

    pygame.display.flip()
    waiting_for_input = True
    
    while waiting_for_input:
        current_time = pygame.time.get_ticks() / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:  
                    waiting_for_input = False
                    
        cursor_x, cursor_y = body_cursor()
        cursor_pixel_x = max(min((cursor_x + 0.5) * WINDOW_WIDTH, WINDOW_WIDTH - 50), 50)   
        cursor_pixel_y = max(min((cursor_y + 0.5) * WINDOW_HEIGHT, WINDOW_HEIGHT - 50), 50)

        current_hover = None
        if ((WINDOW_HEIGHT // 2 + 100) < cursor_pixel_y < (WINDOW_HEIGHT // 2 + 200)) and ((WINDOW_WIDTH // 2 ) < cursor_pixel_x < (WINDOW_WIDTH // 2 + 250)):
            current_hover = "continue"
        elif ((WINDOW_HEIGHT // 2 + 100) < cursor_pixel_y < (WINDOW_HEIGHT // 2 + 200)) and ((WINDOW_WIDTH // 2 - 225) < cursor_pixel_x < (WINDOW_WIDTH // 2 + 25)):
            current_hover = "guide"

        if current_hover != hovered_button:
            hovered_button = current_hover
            hover_start_time = current_time
            ratio = 0.0
        else:
            if hovered_button is not None:
                ratio = (current_time - hover_start_time) / DWELL_THRESHOLD
                if ratio >= 1.0:
                    if hovered_button == "continue":
                        print("觸發：繼續遊戲")
                        #return "continue" 
                    elif hovered_button == "guide":
                        print("觸發：前往圖鑑")
                        #return "guide"
                    
        SCREEN.blit(background_snapshot, (0, 0))
        SCREEN.blit(resized_settle_image, (WINDOW_WIDTH // 2 - 325, (WINDOW_HEIGHT // 2) - 220))

        if hovered_button == "continue":
            SCREEN.blit(triggered_continue_button, (WINDOW_WIDTH // 2 , (WINDOW_HEIGHT // 2) + 95)) # 微調放大後的座標以求置中
        else:
            SCREEN.blit(resized_continue_button, (WINDOW_WIDTH // 2 , (WINDOW_HEIGHT // 2) + 100))

        if hovered_button == "guide":
            SCREEN.blit(triggered_go_to_digital_field_guide_button, (WINDOW_WIDTH // 2 - 235, (WINDOW_HEIGHT // 2) + 95))
        else:
            SCREEN.blit(resized_go_to_digital_field_guide_button, (WINDOW_WIDTH // 2 - 225, (WINDOW_HEIGHT // 2) + 100))

        if fish:
            SCREEN.blit(resized_fish_image, (WINDOW_WIDTH // 2 - 175, (WINDOW_HEIGHT // 2) - 100))

            title_surface = title_font.render("釣魚結算", True, title_color)
            title_x = WINDOW_WIDTH // 2 - (title_surface.get_width() // 2)
            title_y = (WINDOW_HEIGHT // 2) - 200 
            SCREEN.blit(title_surface, (title_x, title_y))

            text_start_x = (WINDOW_WIDTH // 2) + 20
            base_y = (WINDOW_HEIGHT // 2) - 80
            line_spacing = 40

            name_surface = desc_font.render(f"魚名：{fish['name']}", True, desc_color)
            SCREEN.blit(name_surface, (text_start_x, base_y))

            weight_surface = desc_font.render(f"重量：{weight} kg", True, desc_color)
            SCREEN.blit(weight_surface, (text_start_x, base_y + line_spacing * 1))

            rarity_surface = desc_font.render(f"稀有度：{fish['level']}", True, desc_color)
            SCREEN.blit(rarity_surface, (text_start_x, base_y + line_spacing * 2))

            if is_new_species:
                SCREEN.blit(resized_new_species_image, (WINDOW_WIDTH // 2 - 45 , (WINDOW_HEIGHT // 2) - 5))
            elif is_new_record:
                SCREEN.blit(resized_new_record_image, (WINDOW_WIDTH // 2 - 45, (WINDOW_HEIGHT // 2) - 5))

        if ratio > 0.0:
            for i in range(int(ratio * 8 + 0.5)):
                rotated_arc = pygame.transform.rotate(progress_arc, -45 * i)
                arc_rect = rotated_arc.get_rect(center=(cursor_pixel_x, cursor_pixel_y))
                SCREEN.blit(rotated_arc, arc_rect)

        SCREEN.blit(resized_hand_cursor_image, (cursor_pixel_x - 25, cursor_pixel_y - 25))

        pygame.display.flip()

digital_field_guide()
#game_menu()
#homepage_menu()
settle_menu(403, 3.5, False, True)

