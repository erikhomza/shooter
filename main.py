import pygame as pg
import random
import math
import pickle
import os


pg.init()

clock = pg.time.Clock()
fps = 20
max_hp = 20
hp = 20
score = 0
if os.path.exists('./highscore.dat'):
    highscore = pickle.load(open("highscore.dat", "rb"))
else:
    highscore = 0
level = 1
enemies_in_level = 20
enemy_counter = 20
enemies_alive = 0
x_distance = 0
y_distance = 0

screen_width = 1400
screen_height = 800

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Defense")

bullet_img = pg.image.load("laserYellowVertical.png").convert_alpha()
bullet_img = pg.transform.scale(bullet_img, (10, 10))
bullet2_img = pg.image.load("laserRedVertical.png").convert_alpha()
bullet2_img = pg.transform.scale(bullet2_img, (10, 10))
bg = pg.image.load("bg_castle.png").convert_alpha()
bg = pg.transform.scale(bg, (screen_width, screen_height))
mouse = pg.transform.scale(pg.image.load("crosshair.png"), (30, 30))
score_font = pg.font.Font("Turok.ttf", 30)
big_font = pg.font.Font("Turok.ttf", 80)

pg.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
screen.blit(bg, (0, 0))

bullet_group = pg.sprite.Group()
enemy_group = pg.sprite.Group()


class Player:
    def __init__(self, x, y):
        image = pg.image.load("player1.png").convert_alpha()
        self.image = pg.transform.scale(image, (50, 50))
        self.image = pg.transform.scale(image, (50, 50))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.fired = False

    def update(self, x, y):
        pos = pg.mouse.get_pos()
        x_pos = pos[0] - x
        y_pos = -(pos[1] - y)
        angle = math.degrees(math.atan2(y_pos, x_pos))
        self.img = pg.transform.rotate(self.image, angle-90)
        self.img.set_colorkey((255, 255, 255))
        self.rect = self.img.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        screen.blit(self.img, self.rect)

    def shoot(self):
        pos = pg.mouse.get_pos()
        x_pos = pos[0] - self.rect.centerx
        y_pos = -(pos[1] - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_pos, x_pos))

        if pg.mouse.get_pressed()[0] and self.fired == False:
            self.fired = True
            bullet = Bullet(pg.transform.rotate(bullet_img, self.angle-90), self.rect.centerx, self.rect.centery, self.angle, 1)
            bullet_group.add(bullet)

        if pg.mouse.get_pressed()[0] == False:
            self.fired = False


class Bullet(pg.sprite.Sprite):
    def __init__(self, image, x, y, angle, shooter):
        pg.sprite.Sprite.__init__(self)
        self.shooter = shooter
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 20
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)
        self.time = 200

    def update(self):
        self.time -= 1
        if self.time == 0:
            self.kill()
        if self.rect.right < 0 or self.rect.left >= screen_width:
            self.dx *= -1
            self.image = pg.transform.rotate(self.image, self.angle-90)
        if self.rect.bottom < 0 or self.rect.top >= screen_height:
            self.dy *= -1
            self.image = pg.transform.rotate(self.image, self.angle-90)

        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self):
        screen.blit(self.image, self.rect)


class Enemy(pg.sprite.Sprite):
    def __init__(self, x, y, number, speed, stop_dist):
        super().__init__()
        self.number = number
        image = pg.image.load(f"enemy-shooter{self.number}.png").convert_alpha()
        self.image = pg.transform.scale(image, (50, 50))
        self.image = pg.transform.scale(image, (50, 50))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.cooldown = 50
        self.speed = speed
        self.stop_dist = stop_dist
        self.move_lenght = 0
        self.x_move = 0
        self.y_move = 0

    def update(self, x, y):
        x_pos = player.rect.centerx - x
        y_pos = -(player.rect.centery - y)
        angle = math.degrees(math.atan2(y_pos, x_pos))
        self.img = pg.transform.rotate(self.image, angle-90)
        self.img.set_colorkey((255, 255, 255))
        self.rect = self.img.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.angle = math.radians(angle)
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)
        dist = math.sqrt((player.rect.centerx - self.rect.centerx) ** 2 + (player.rect.centery - self.rect.centery) ** 2)
        if dist > self.stop_dist:
            self.rect.centerx += self.dx
            self.rect.centery += self.dy
        if dist > self.stop_dist*2:
            self.rect.centerx += self.dx
            self.rect.centery += self.dy

        screen.blit(self.img, self.rect)

    def shoot(self):
        x_pos = player.rect.centerx - self.rect.centerx
        y_pos = -(player.rect.centery - self.rect.centery)
        self.angle = math.degrees(math.atan2(y_pos, x_pos))
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.cooldown == 0:
            self.cooldown = 50
            bullet = Bullet(pg.transform.rotate(bullet2_img, self.angle-90), self.rect.centerx, self.rect.centery, self.angle, 0)
            bullet_group.add(bullet)

    def random_move(self):
        random_move = random.randint(0, 200)
        if random_move == 10:
            self.x_move = random.randint(-8, 8)
            self.y_move = random.randint(-8, 8)
            self.move_lenght = random.randint(5, 15)
        if self.move_lenght != 0:
            self.rect.centerx += self.x_move
            self.rect.centery += self.y_move
            self.move_lenght -= 1


def health_bar(hp, max_hp):
    color1 = round(255/max_hp*hp)
    color2 = 255-color1
    if color1 < 0:
        color1 = 0
    if color2 < 0:
        color2 = 0
    if color1 > 255:
        color1 = 255
    if color2 > 255:
        color2 = 255
    pg.draw.rect(screen, (0, 0, 0), pg.Rect(27, 27, 10*max_hp+6, 36))
    pg.draw.rect(screen, (color2, color1, 0), pg.Rect(30, 30, 10*hp, 30))


def background(x_distance, y_distance):
    bg_rect = pg.Rect(0+x_distance, 0+y_distance, 1400, 800)
    screen.blit(bg, bg_rect)
    bg_rect = pg.Rect(-1400 + x_distance, 0 + y_distance, 1400, 800)
    screen.blit(bg, bg_rect)
    bg_rect = pg.Rect(1400 + x_distance, 0 + y_distance, 1400, 800)
    screen.blit(bg, bg_rect)
    bg_rect = pg.Rect(0 + x_distance, 800 + y_distance, 1400, 800)
    screen.blit(bg, bg_rect)
    bg_rect = pg.Rect(0 + x_distance, -800 + y_distance, 1400, 800)
    screen.blit(bg, bg_rect)
    bg_rect = pg.Rect(1400 + x_distance, 800 + y_distance, 1400, 800)
    screen.blit(bg, bg_rect)
    bg_rect = pg.Rect(-1400 + x_distance, 800 + y_distance, 1400, 800)
    screen.blit(bg, bg_rect)
    bg_rect = pg.Rect(1400 + x_distance, -800 + y_distance, 1400, 800)
    screen.blit(bg, bg_rect)
    bg_rect = pg.Rect(-1400 + x_distance, -800 + y_distance, 1400, 800)
    screen.blit(bg, bg_rect)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def next_level(enemies_in_level):
    enemies_in_level += 5
    return enemies_in_level


def cursor(cursor):
    pos = pg.mouse.get_pos()
    screen.blit(cursor, (pos[0]-15, pos[1]-15))


def restart(run):
    game_lost = True
    draw_text("YOU LOST!", big_font, (200, 200, 30), 530, 250)
    draw_text("press r to restart", big_font, (200, 200, 30), 400, 400)
    pg.display.update()
    while game_lost:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                game_lost = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    game_lost = False
    return run


def pause(run):
    game_paused = True
    draw_text("GAME PAUSED", big_font, (200, 200, 30), 480, 300)
    pg.display.update()
    while game_paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                game_paused = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    game_paused = False
    return run


player = Player(675, 375)


run = True
while run:
    clock.tick(fps)
    screen.fill((155, 155, 155))

    if score > highscore:
        highscore = score
    if enemy_counter > 0:
        for i in range(20):
            n = random.randint(1, 1000)
            t = random.randint(0, 1)
            if n == 25:
                enemy = Enemy(i * 50, 1400 * t, random.randint(1, 4), random.randint(2, 6), random.randint(130, 270))
                enemy_group.add(enemy)
                enemies_alive += 1
                enemy_counter -= 1
        for i in range(20):
            n = random.randint(1, 1000)
            t = random.randint(0, 1)
            if n == 25:
                enemy = Enemy(1400 * t, i * 50, random.randint(1, 4), random.randint(2, 6), random.randint(130, 270))
                enemy_group.add(enemy)
                enemies_alive += 1
                enemy_counter -= 1

    key = pg.key.get_pressed()
    if key[pg.K_UP]:
        if y_distance*-1 < -800:
            if player.rect.centery > 25:
                player.rect.centery -= 10
        else:
            if player.rect.centery > 375:
                player.rect.centery -= 10
            else:
                y_distance += 10
                for enemy in enemy_group:
                    enemy.rect.centery += 10
                for bullet in bullet_group:
                    bullet.rect.y += 10
    if key[pg.K_DOWN]:
        if y_distance*-1 > 800:
            if player.rect.centery < 775:
                player.rect.centery += 10
        else:
            if player.rect.centery < 375:
                player.rect.centery += 10
            else:
                y_distance -= 10
                for enemy in enemy_group:
                    enemy.rect.centery -= 10
                for bullet in bullet_group:
                    bullet.rect.y -= 10
    if key[pg.K_LEFT]:
        if x_distance * -1 < -1400:
            if player.rect.centerx > 25:
                player.rect.centerx -= 10
        else:
            if player.rect.centerx > 675:
                player.rect.centerx -= 10
            else:
                x_distance += 10
                for enemy in enemy_group:
                    enemy.rect.centerx += 10
                for bullet in bullet_group:
                    bullet.rect.x += 10
    if key[pg.K_RIGHT]:
        if x_distance*-1 > 1400:
            if player.rect.centerx < 1375:
                player.rect.centerx += 10
        else:
            if player.rect.centerx < 675:
                player.rect.centerx += 10
            else:
                x_distance -= 10
                for enemy in enemy_group:
                    enemy.rect.centerx -= 10
                for bullet in bullet_group:
                    bullet.rect.x -= 10

    background(x_distance, y_distance)
    player.shoot()

    for enemy in enemy_group:
        enemy.shoot()
        enemy.random_move()

    bullet_group.update()
    bullet_group.draw(screen)
    player.update(player.rect.centerx, player.rect.centery)

    for enemy in enemy_group:
        enemy.update(enemy.rect.centerx, enemy.rect.centery)
        for bullet in bullet_group:
            if pg.sprite.collide_rect(enemy, bullet):
                if bullet.shooter == 1:
                    enemy.kill()
                    bullet.kill()
                    score += 1
                    enemies_alive -= 1

    for bullet in bullet_group:
        if pg.sprite.collide_rect(player, bullet):
            if bullet.shooter == 0:
                hp -= 1
                bullet.kill()

    if hp <= 0:
        run = restart(run)
        x_distance = 0
        y_distance = 0
        background(x_distance, y_distance)
        if score == highscore:
            pickle.dump(highscore, open("highscore.dat", "wb"))
        level = 1
        score = 0
        enemy_counter = 20
        enemies_in_level = 20
        enemies_alive = 0
        enemy_group.empty()
        bullet_group.empty()
        player = Player(675, 375)
        hp = max_hp


    health_bar(hp, max_hp)
    draw_text(f"enemies alive: {enemies_alive}", score_font, (200, 200, 30), 1100, 30)
    draw_text(f"level: {level}", score_font, (200, 200, 30), 1100, 70)
    draw_text(f"score: {score}", score_font, (200, 200, 30), 800, 30)
    draw_text(f"highscore: {highscore}", score_font, (200, 200, 30), 800, 70)

    if enemy_counter == 0 and enemies_alive == 0:
        enemy_counter = next_level(enemies_in_level)
        enemies_in_level = enemy_counter
        level += 1
        x_distance, y_distance = 0, 0
        background(x_distance, y_distance)
        player = Player(675, 375)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                run = pause(run)
    cursor(mouse)
    pg.display.update()

pg.quit()