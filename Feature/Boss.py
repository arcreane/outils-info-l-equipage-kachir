import pygame
import math
import random
from pygame.math import Vector2

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE
from resource_loader import load_image
from movable_entity import MovableEntity
from event_bus import EventBus

class PatternReader:
    """
    Lit une séquence d'actions pour le boss (timeline simple).
    Exemple de pattern interne :
    [
        {"type": "move_sine",   "duration": 4.5, "amplitude": 0.9},
        {"type": "shoot_single","duration": 1.2},
        {"type": "shoot_cone",  "duration": 2.0, "bullets": 7},
    ]
    """
    def __init__(self, actions_list, loop=True):
        self.actions = actions_list
        self.loop = loop
        self.current_idx = 0
        self.time_in_action = 0.0
        self.total_time = 0.0

    def update(self, boss, dt, player_pos):
        self.total_time += dt
        self.time_in_action += dt

        action = self.actions[self.current_idx]
        duration = action["duration"]

        # Passage à l'action suivante ?
        if self.time_in_action >= duration:
            self.current_idx += 1
            if self.current_idx >= len(self.actions):
                if self.loop:
                    self.current_idx = 0
                else:
                    self.current_idx = len(self.actions) - 1  # reste sur dernière
            self.time_in_action = 0.0
            action = self.actions[self.current_idx]

        t = self.time_in_action / action["duration"]

        # Exécution des différents types d'actions
        if action["type"] == "move_sine":
            amp = action.get("amplitude", 0.8)
            center_x = SCREEN_WIDTH * 0.5
            target_x = center_x + math.sin(t * math.pi * 2) * (SCREEN_WIDTH * 0.22 * amp)
            boss.velocity.x = (target_x - boss.pos.x) * 3.5   # suivi rapide

        elif action["type"] == "shoot_single":
            if t < 0.08:  # tir quasi instantané au début de l'action
                self._fire_toward_player(boss, player_pos, speed=220)

        elif action["type"] == "shoot_cone":
            if t < 0.12:
                count = action.get("bullets", 5)
                angle_spread = math.radians(35)
                for i in range(count):
                    angle = -angle_spread/2 + (angle_spread * i / (count-1 if count > 1 else 1))
                    direction = Vector2(0,1).rotate_rad(angle)
                    self._fire_direction(boss, direction, speed=190)

        elif action["type"] == "shoot_circle":
            if t < 0.15:
                count = action.get("bullets", 12)
                for i in range(count):
                    angle = (i / count) * math.tau
                    direction = Vector2(math.cos(angle), math.sin(angle))
                    self._fire_direction(boss, direction, speed=160)

        boss.velocity.x = max(-180, min(180, boss.velocity.x))  # limite vitesse


    def _fire_toward_player(self, boss, player_pos, speed=200):
        if player_pos:
            direction = (Vector2(player_pos) - boss.pos).normalize()
            bullet = EnemyBullet(boss.pos.copy() + Vector2(0,30), direction * speed)
            enemy_bullets.add(bullet)
            all_sprites.add(bullet)


    def _fire_direction(self, boss, direction, speed=180):
        bullet = EnemyBullet(boss.pos.copy() + Vector2(0,30), direction * speed)
        enemy_bullets.add(bullet)
        all_sprites.add(bullet)



class Boss(MovableEntity):
    def __init__(self, level=1):
        pos = (SCREEN_WIDTH // 2 - 64, 80)
        image = load_image(f"boss_level{level}.png") or load_image("boss_default.png")
        super().__init__(pos, image)

        self.level = level
        self.max_hp = 600 + level * 300
        self.hp = self.max_hp
        self.phase = 1

        # Patterns des différentes phases
        self.patterns = {
            1: PatternReader([
                {"type": "move_sine",   "duration": 5.0, "amplitude": 0.7},
                {"type": "shoot_single","duration": 1.8},
            ], loop=True),

            2: PatternReader([
                {"type": "move_sine",   "duration": 3.2, "amplitude": 0.95},
                {"type": "shoot_cone",  "duration": 2.1, "bullets": 7},
                {"type": "shoot_single","duration": 0.9},
            ], loop=True),

            # Phase 3 optionnelle (décommente si tu veux l'activer)
            # 3: PatternReader([
            #     {"type": "move_sine",   "duration": 2.5, "amplitude": 1.15},
            #     {"type": "shoot_circle","duration": 3.0, "bullets": 14},
            #     {"type": "shoot_cone",  "duration": 1.8, "bullets": 9},
            # ], loop=True),
        }

        self.current_pattern = self.patterns[1]
        self.pattern_timer = 0.0

        # Visuel / effet
        self.hit_flash = 0.0


    def update(self, dt, player_pos=None):
        self.pattern_timer += dt

        hp_ratio = self.hp / self.max_hp

        # Changement de phase automatique
        if hp_ratio <= 0.30 and 3 in self.patterns:
            if self.phase != 3:
                self.phase = 3
                self.current_pattern = self.patterns[3]
                self.pattern_timer = 0.0
                EventBus.trigger("boss_phase_changed", phase=3)

        elif hp_ratio <= 0.65:
            if self.phase != 2:
                self.phase = 2
                self.current_pattern = self.patterns[2]
                self.pattern_timer = 0.0
                EventBus.trigger("boss_phase_changed", phase=2)

        # Mise à jour du pattern actuel
        if player_pos:
            self.current_pattern.update(self, dt, player_pos)

        super().update(dt)

        # Limite horizontale (boss ne sort pas trop des côtés)
        self.pos.x = max(80, min(SCREEN_WIDTH - 80, self.pos.x))


    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        self.hit_flash = 0.18  # flash blanc court

        if self.hp <= 0:
            self.die()


    def die(self):
        # Loot + event de victoire niveau
        loot = BossLoot(self.pos.copy(), self.level)
        loots.add(loot)
        all_sprites.add(loot)

        EventBus.trigger("boss_defeated", level=self.level)
        self.kill()
