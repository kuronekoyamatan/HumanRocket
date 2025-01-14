import pygame
import random
import math
from pygame import mixer

# -------------------- 初期設定 --------------------
pygame.init()  # Pygameの初期化

# 背景画像設定
BACKGROUND_IMG = "background.png"
bg = pygame.image.load(BACKGROUND_IMG)
bg = pygame.transform.scale(bg, (800, 600))  # 背景を画面サイズに調整

# ゲーム画面の設定
screen = pygame.display.set_mode((800, 600))  # 画面サイズ 800x600
pygame.display.set_caption("Human Rocket")  # ゲームタイトル

# -------------------- プレイヤー設定 --------------------
# プレイヤーの画像と初期位置設定
playerImg = pygame.image.load("player.png")
playerX, playerY = 370, 480
playerX_change = 0  # 初期移動量

# -------------------- 弾設定 --------------------
# 弾の画像リスト
BULLET_IMAGES = ["bullet.png", "bullet1.png", "bullet2.png", "bullet3.png"]

# 弾の初期設定
def choose_bullet_image():
    return pygame.image.load(random.choice(BULLET_IMAGES))  # 弾の画像をランダム選択

bulletImg = choose_bullet_image()  # 初期弾画像
bulletX, bulletY = 0, 480  # 弾の初期位置
bulletX_change, bulletY_change = 0, 1  # 弾の移動量
bullet_state = 'ready'  # 弾の状態

# 弾の発射音
bullet_sound = mixer.Sound("laser.wav")

# -------------------- 敵設定 --------------------
# 敵の画像リスト
ENEMY_IMAGES = ["enemy.png", "enemy1.png", "enemy2.png"]
ENEMY_SPEEDS = [0, 2, 4, 6]  # 敵の速度リスト（ランダムで選択）

# 敵の初期設定
def choose_enemy_image():
    return pygame.image.load(random.choice(ENEMY_IMAGES))  # 敵画像をランダム選択

def choose_enemy_speed():
    return random.choice(ENEMY_SPEEDS)  # 敵の速度をランダム選択

# 初期敵の位置と設定
enemyX = random.randint(0, 736)  # 敵の横位置をランダムに決定。0から736までの整数をランダムに選ぶ。736は右端に敵が出る直前の位置。
enemyY = random.randint(50, 150)
enemyImg = choose_enemy_image()
enemy_speed = choose_enemy_speed()
enemyX_change = 0.35
enemyY_change = 40

# -------------------- 音楽設定 --------------------
mixer.Sound("background.wav").play(-1)  # 背景音楽をループ再生

# -------------------- スコア設定 --------------------
score_value = 0  # 初期スコア

# -------------------- ゲームオーバー処理 --------------------
def game_over():
    font = pygame.font.SysFont(None, 64)
    game_over_text = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over_text, (250, 250))  # 画面中央にゲームオーバー表示
    pygame.display.update()
    pygame.time.wait(5000)  # 1秒間ゲームオーバーメッセージを表示
    pygame.quit()  # ゲームを終了
    quit()  # プログラムを終了

# -------------------- ゲームループ --------------------
running = True
bullet_change_counter = 0  # 弾の画像変更カウンター
image_change_interval = 180  # 画像変更のインターバル（180フレーム）

while running:
    screen.blit(bg, (0, 0))  # 背景を描画

    # -------------------- イベント処理 --------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # ゲーム終了
        if event.type == pygame.KEYDOWN:  # キーが押されたとき
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5  # 左に移動
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5  # 右に移動
            if event.key == pygame.K_SPACE:  # スペースキーで弾を発射
                if bullet_state == 'ready':
                    bulletX = playerX  # 弾をプレイヤーの位置に発射
                    bullet_state = 'fire'  # 弾を発射状態に変更
                    bullet_sound.play()  # 弾の発射音を再生

        if event.type == pygame.KEYUP:  # キーを離したとき
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0  # プレイヤーの移動を停止

    # -------------------- プレイヤー移動処理 --------------------
    playerX += playerX_change  # プレイヤーの位置を更新
    if playerX <= 0:
        playerX = 0  # 左端に達した場合
    elif playerX >= 736:
        playerX = 736  # 右端に達した場合

    # -------------------- 弾の移動処理 --------------------
    if bullet_state == 'fire':
        screen.blit(bulletImg, (bulletX + 16, bulletY + 10))  # 弾を描画
        bulletY -= bulletY_change  # 弾を上に移動
        if bulletY <= 0:  # 弾が画面上端に到達した場合
            bulletY = 480  # 弾を元の位置に戻す
            bullet_state = 'ready'  # 弾を発射準備状態に戻す

        # 弾の画像変更
        bullet_change_counter += 1
        if bullet_change_counter >= image_change_interval:
            bulletImg = choose_bullet_image()  # 弾の画像をランダムに変更
            bullet_change_counter = 0

    # -------------------- 敵の移動処理 --------------------
    enemyX += enemyX_change * enemy_speed  # 敵の位置を更新（速度を反映）
    if enemyX <= 0:  # 敵が左端に達した場合
        enemyX_change = 0.35
        enemyY += enemyY_change  # 下に移動
    elif enemyX >= 736:  # 敵が右端に達した場合
        enemyX_change = -0.35
        enemyY += enemyY_change  # 下に移動

    # -------------------- プレイヤーと敵の衝突判定 --------------------
    distance = math.sqrt(math.pow(enemyX - playerX, 2) + math.pow(enemyY - playerY, 2))  # プレイヤーと敵の距離を計算
    if distance < 30:  # 衝突判定（30px以内で衝突と見なす）
        game_over()  # ゲームオーバー関数を呼び出す

    # -------------------- 敵がプレイヤーより下に行った場合の判定 --------------------
    if enemyY > playerY:  # 敵がプレイヤーより下に行った場合
        game_over()  # ゲームオーバー関数を呼び出す

    # -------------------- 衝突判定 --------------------
    distance_bullet = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))  # 敵と弾の距離を計算
    if distance_bullet < 27:  # 衝突範囲に入った場合
        bulletY = 480  # 弾の位置をリセット
        bullet_state = 'ready'  # 弾を発射準備状態に戻す
        score_value += 1  # スコアを1点増加
        enemyX = random.randint(0, 736)  # 新しい敵の位置をランダムで設定
        enemyY = random.randint(50, 150)
        enemyImg = choose_enemy_image()  # 新しい敵の画像を選択
        enemy_speed = choose_enemy_speed()  # 新しい敵の速度を選択

    # -------------------- スコア表示 --------------------
    font = pygame.font.SysFont(None, 32)
    score = font.render("Score : {}".format(score_value), True, (255, 255, 255))  # スコアを画面に描画
    screen.blit(score, (20, 50))  # スコアの位置を指定

    # -------------------- プレイヤーと敵を描画 --------------------
    screen.blit(playerImg, (playerX, playerY))  # プレイヤーを描画
    screen.blit(enemyImg, (enemyX, enemyY))  # 敵を描画

    # 画面を更新
    pygame.display.update()