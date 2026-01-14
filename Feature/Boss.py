import pygame
from pygame.math import Vector2
import math
import random
from entities.enemies import Enemy, EnemyBullet  # Import Enemy et EnemyBullet
from settings import SCREEN_WIDTH, SCREEN_HEIGHT  # Constantes écran

class Boss(Enemy):
    def __init__(self, level, x, y):
        hp = 50 * level + 50  # HP élevé, scale par niveau (ex: L1=100, L5=300)
        image_key = f'boss{level}.png'  # Images: boss1.png à boss5.png (taille ~120x120)
        image = load_image(image_key)
        image = pygame.transform.scale(image, (120, 120))  # Plus grand que minions
        super().__init__(x, y, hp=hp, image_key=image_key)  # image_key non utilisé car override image
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.level = level
        self.max_hp = hp
        self.reward = 1000 * level  # Gros score
        self.drop_chance = 1.0  # Toujours drop loot spécial
        self.phase = 1
        self.phase_thresholds = [2/3, 1/3]  # Phases: >66%=1, >33%=2, <33%=3
        self.attack_timer = random.uniform(0.5, 1.5)
        self.patrol_timer = 0
        self.patrol_amplitude = 250 * (1 + level * 0.2)  # Plus large par niveau
        self.patrol_speed = 60 + level * 10
        self.descend_speed = 40
        self.hover_y = SCREEN_HEIGHT * 0.25  # Position hover après descente
        self.font = pygame.font.SysFont('arial', 24, bold=True)
        self.big_font = pygame.font.SysFont('arial', 36, bold=True)

    def update_ai(self, dt, player_pos):
        self.update_phase()
        self.move_pattern(dt)
        self.attack_pattern(dt, player_pos)

    def update_phase(self):
        hp_ratio = self.hp / self.max_hp
        if hp_ratio <= self.phase_thresholds[1]:
            self.phase = 3
        elif hp_ratio <= self.phase_thresholds[0]:
            self.phase = 2
        # Phase 1 par défaut

    def move_pattern(self, dt):
        self.patrol_timer += dt
        # Mouvement sinusoidal horizontal (patrouille)
        target_x = SCREEN_WIDTH // 2 + math.sin(self.patrol_timer * 1.5) * self.patrol_amplitude
        dx = target_x - self.pos.x
        if abs(dx) > 5:
            self.vel.x = math.copysign(self.patrol_speed, dx)
        else:
            self.vel.x = 0
        # Descente initiale puis hover
        if self.pos.y < self.hover_y:
            self.vel.y = self.descend_speed
        else:
            self.vel.y = 0
            self.pos.y = self.hover_y  # Clamp
        # Clamp horizontal
        if self.rect.left < 0:
            self.pos.x = self.rect.width / 2
        elif self.rect.right > SCREEN_WIDTH:
            self.pos.x = SCREEN_WIDTH - self.rect.width / 2

    def attack_pattern(self, dt, player_pos):
        self.attack_timer += dt
        # Délai plus court par phase/niveau
        delay = max(0.8 - (self.phase - 1) * 0.3 - self.level * 0.1, 0.4)
        if self.attack_timer >= delay and player_pos:
            self.execute_attack(self.phase, player_pos)
            self.attack_timer = 0

    def execute_attack(self, phase, player_pos):
        if phase == 1:
            # Phase 1: Tir simple vers player
            self.shoot_towards(player_pos, speed=200)
        elif phase == 2:
            # Phase 2: Tir spread (triple cône)
            angles = [-20, 0, 20]
            for angle_offset in angles:
                self.shoot_spread(player_pos, angle_offset, speed=180)
        elif phase == 3:
            # Phase 3: Tir cercle + summon minions
            self.shoot_circle(8, speed=160)
            self.summon_minions()

    def shoot_towards(self, player_pos, speed):
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > 0:
            vel_x = (dx / dist) * speed
            vel_y = (dy / dist) * speed
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, vel_x, vel_y)
            enemy_bullets.add(bullet)
            all_sprites.add(bullet)

    def shoot_spread(self, player_pos, angle_offset, speed):
        # Angle vers player + offset
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        angle = math.atan2(dy, dx)
        angle += math.radians(angle_offset)
        vel_x = math.cos(angle) * speed
        vel_y = math.sin(angle) * speed
        bullet = EnemyBullet(self.rect.centerx, self.rect.centery, vel_x, vel_y)
        enemy_bullets.add(bullet)
        all_sprites.add(bullet)

    def shoot_circle(self, num_bullets, speed):
        for i in range(num_bullets):
            angle = (i / num_bullets) * 2 * math.pi
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            bullet = EnemyBullet(self.rect.centerx, self.rect.centery, vel_x, vel_y)
            enemy_bullets.add(bullet)
            all_sprites.add(bullet)

    def summon_minions(self):
        # Summon 3 minions près du boss (type simple pour éviter boucle infinie)
        for _ in range(3):
            offset_x = random.uniform(-100, 100)
            offset_y = random.uniform(50, 150)
            minion_x = self.rect.centerx + offset_x
            minion_y = self.rect.centery + offset_y
            if 0 < minion_x < SCREEN_WIDTH:
                minion = StraightMinion(minion_x, minion_y)  # Import depuis enemies
                enemies.add(minion)
                all_sprites.add(minion)

    def draw(self, screen):
        super().draw(screen)  # Petite barre au-dessus (optionnel)
        # Grande barre HP en haut écran
        bar_x = 50
        bar_y = 20
        bar_width = SCREEN_WIDTH - 100
        bar_height = 40
        fill_width = (self.hp / self.max_hp) * bar_width
        # Fond barre
        pygame.draw.rect(screen, (80, 20, 20), (bar_x, bar_y, bar_width, bar_height))
        # Remplissage
        pygame.draw.rect(screen, (20, 255, 20), (bar_x, bar_y, fill_width, bar_height))
        # Bordure
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 4)
        # Texte "BOSS PHASE X"
        phase_text = self.big_font.render(f"BOSS PHASE {self.phase}", True, (255, 255, 0))
        screen.blit(phase_text, (bar_x, bar_y - 35))
        # Nom niveau
        level_text = self.font.render(f"Level {self.level}", True, (255, 255, 255))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, bar_y - 35))

    def die(self):
        print(f"Boss Level {self.level} defeated! +{self.reward} points - Level Complete!")
        # Loot spécial
        # spawn_level_bonus(self.level, self.rect.center)  # TODO: Module J (bonus spécifique niveau)
        # Effet explosion (TODO: particules ou anim)
        # game_state.next_level()  # Via EventBus (Module A)
        super().die()

# Fonction spawn (appelée depuis LevelManager après fin vague)
def spawn_boss(level):
    x = SCREEN_WIDTH // 2
    y = -200  # Hors écran haut
    boss = Boss(level, x, y)
    enemies.add(boss)
    all_sprites.add(boss)
    print(f"Boss Level {level} spawned!")
    return boss
