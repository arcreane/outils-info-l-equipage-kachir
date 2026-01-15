import pygame
import random
import math
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, GREEN, RED, ORANGE, PURPLE, YELLOW  

class Entity:
    def __init__(self, x, y, color=GREEN, speed=100):
        self.size = min(WINDOW_WIDTH, WINDOW_HEIGHT) // 15
        self.x = x
        self.y = y  # FIX: séparé de speed
        self.speed = speed
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def vitesse(self, speed):
        self.speed = speed

    def couleur(self, color):
        self.color = color

    def move_horizontal(self, direction):
        self.rect.x += direction * self.speed
        self.rect.x = max(0, min(self.rect.x, WINDOW_WIDTH - self.size))

    def move_vertical(self, direction):
        self.rect.y += direction * self.speed
        self.rect.y = max(0, min(self.rect.y, WINDOW_HEIGHT - self.size))

    def update(self, dt=1.0):
        """Méthode update ajoutée pour les boucles de jeu (dt pour fluidité)"""
        pass  # À surcharger

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

enemies_group = []
enemy_bullets_group = []

class Enemy(Entity):
    def __init__(self, x=None, y=-50):
        if x is None:
            x = random.randint(self.size, WINDOW_WIDTH - self.size)
        super().__init__(x, y, color=RED, speed=80)
        self.hp = 20
        self.max_hp = 20
        self.points = 100
        self.drop_chance = 0.3  # 30% drop bonus

    def update(self, dt, player=None):
        # Descente par défaut
        self.move_vertical(1 * dt)
        # Sortie écran → kill
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.die()

    def die(self):
        # Score + drop
        print(f"+{self.points} points!")  # À remplacer par EventBus
        if random.random() < self.drop_chance:
            self.drop_bonus()
        self.kill()

    def drop_bonus(self):
        # Stub bonus (à connecter Module J)
        print("Bonus droppé!")

    def kill(self):
        if self in enemies_group:
            enemies_group.remove(self)


class MinionType1(Enemy):
    def __init__(self):
        super().__init__(speed=120)
        self.hp = 15
        self.points = 50


class MinionType2(Enemy):
    def __init__(self):
        super().__init__(speed=90)
        self.hp = 25
        self.points = 80
        self.zigzag_phase = random.uniform(0, math.tau)
        self.zigzag_amp = 2.0

    def update(self, dt, player=None):
        # Zigzag horizontal + descente
        t = pygame.time.get_ticks() * 0.005
        zig = math.sin(t + self.zigzag_phase) * self.zigzag_amp
        self.move_horizontal(zig * dt)
        self.move_vertical(1 * dt)


class MinionType3(Enemy):
    def __init__(self):
        super().__init__(speed=0)  # Pas de vitesse fixe
        self.hp = 40
        self.points = 150
        self.accel = 150

    def update(self, dt, player=None):
        if player:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = math.sqrt(dx**2 + dy**2)
            if dist > 0:
                dx /= dist
                dy /= dist
                self.move_horizontal(dx * dt)
                self.move_vertical(dy * dt)


class MinionType4(Enemy):
    def __init__(self):
        super().__init__(speed=70)
        self.hp = 30
        self.points = 120
        self.weapon = EnemyWeapon(fire_rate=2.0)  # Système d'arme

    def update(self, dt, player=None):
        super().update(dt, player)
        if player:
            self.weapon.fire(self.rect.center, player.rect.center)


class EnemyWeapon:
    def __init__(self, fire_rate=1.5):
        self.fire_rate = fire_rate
        self.cooldown = 0.0

    def fire(self, enemy_pos, player_pos):
        self.cooldown -= 1/60  # Assume 60 FPS
        if self.cooldown <= 0:
            # Créer bullet
            bullet = EnemyBullet(enemy_pos[0], enemy_pos[1])
            dir_x = player_pos[0] - enemy_pos[0]
            dir_y = player_pos[1] - enemy_pos[1]
            dist = math.sqrt(dir_x**2 + dir_y**2)
            if dist > 0:
                bullet.rect.x += dir_x / dist * 10  # Offset
                bullet.vitesse(200)  # Vitesse bullet
                bullet.rect.y += dir_y / dist * 10
            enemy_bullets_group.append(bullet)
            self.cooldown = self.fire_rate

class EnemyBullet(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, color=ORANGE, speed=0)  # Speed ajustée à l'update
        self.size = self.size // 2
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size * 2)  # Allongé

    def update(self, dt, player=None):
        self.move_vertical(1 * dt)  # Vers le bas par défaut, ajusté au fire
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

    def kill(self):
        if self in enemy_bullets_group:
            enemy_bullets_group.remove(self)


def spawn_minion(type_id=1):
    """Spawn un minion aléatoire ou spécifique"""
    if type_id == 1:
        minion = MinionType1()
    elif type_id == 2:
        minion = MinionType2()
    elif type_id == 3:
        minion = MinionType3()
    elif type_id == 4:
        minion = MinionType4()
    else:
        minion = MinionType1()  # Default
    enemies_group.append(minion)
    return minion

def update_enemies(dt, player):
    """Update tous les ennemis (à appeler dans boucle principale)"""
    for enemy in enemies_group[:]:  # Copy pour éviter modification en iter
        enemy.update(dt, player)

def update_enemy_bullets(dt, player):
    """Update bullets ennemis + collisions"""
    for bullet in enemy_bullets_group[:]:
        bullet.update(dt, player)
        # Collision bullet -> player (stub)
        if player and bullet.rect.colliderect(player.rect):
            player.take_damage(10)  # Assume player a take_damage
            bullet.kill()

def draw_enemies(surface):
    for enemy in enemies_group:
        enemy.draw(surface)
    for bullet in enemy_bullets_group:
        bullet.draw(surface)
