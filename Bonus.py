import pygame
from base_entity import Entity


class BaseBonus(Entity):
    def __init__(self, x, y, radius=12):
        super().__init__(x, y)
        self.radius = radius
        self.collected = False

    def update(self, dt):
        self.y += 40 * dt  

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), (int(self.x), int(self.y)), self.radius)

    def check_collision(self, player):
        if self.collected:
            return False
        return player.rect.collidepoint(self.x, self.y)

    def apply(self, player, game_state):
        raise NotImplementedError


class ScoreBonus(BaseBonus):
    def __init__(self, x, y, amount=100):
        super().__init__(x, y)
        self.amount = amount

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 215, 0), (int(self.x), int(self.y)), self.radius)

    def apply(self, player, game_state):
        game_state.score += self.amount
        self.collected = True


class HealBonus(BaseBonus):
    def __init__(self, x, y, heal=20):
        super().__init__(x, y)
        self.heal = heal

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 200, 255), (int(self.x), int(self.y)), self.radius)

    def apply(self, player, game_state):
        player.hp = min(player.max_hp, player.hp + self.heal)
        self.collected = True


class LifeBonus(BaseBonus):
    def __init__(self, x, y):
        super().__init__(x, y)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), self.radius)

    def apply(self, player, game_state):
        game_state.lives += 1
        self.collected = True


class WeaponUpgradeBonus(BaseBonus):
    def __init__(self, x, y, level_up=1):
        super().__init__(x, y)
        self.level_up = level_up

    def draw(self, surface):
        pygame.draw.circle(surface, (150, 0, 255), (int(self.x), int(self.y)), self.radius)

    def apply(self, player, game_state):
        player.weapon_level += self.level_up
        self.collected = True


class CooldownReductionBonus(BaseBonus):
    def __init__(self, x, y, factor=0.8):
        super().__init__(x, y)
        self.factor = factor

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 150), (int(self.x), int(self.y)), self.radius)

    def apply(self, player, game_state):
        player.fire_cooldown *= self.factor
        self.collected = True


class Level1Bonus(BaseBonus):
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 120, 0), (int(self.x), int(self.y)), self.radius)

    def apply(self, player, game_state):
        game_state.score += 300
        player.activate_power("fire_boost", duration=4)
        self.collected = True


class Level2Bonus(BaseBonus):
    def draw(self, surface):
        pygame.draw.circle(surface, (0, 120, 255), (int(self.x), int(self.y)), self.radius)

    def apply(self, player, game_state):
        player.activate_power("shield", duration=5)
        self.collected = True


class Level3Bonus(BaseBonus):
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 0, 200), (int(self.x), int(self.y)), self.radius)

    def apply(self, player, game_state):
        player.speed *= 1.5
        self.collected = True


class Level4Bonus(BaseBonus):
    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 255), (int(self.x), int(self.y)), self.radius)

    def apply(self, player, game_state):
        player.activate_power("clone", duration=6)
        self.collected = True


class Level5Bonus(BaseBonus):
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 50, 50), (int(self.x), int(self.y)), self.radius)

    def apply(self, player, game_state):
        game_state.score += 1000
        player.activate_power("ultimate", duration=3)
        self.collected = True


def create_bonus(bonus_type, x, y):
    if bonus_type == "score":
        return ScoreBonus(x, y)
    if bonus_type == "heal":
        return HealBonus(x, y)
    if bonus_type == "life":
        return LifeBonus(x, y)
    if bonus_type == "weapon_up":
        return WeaponUpgradeBonus(x, y)
    if bonus_type == "cooldown":
        return CooldownReductionBonus(x, y)

    if bonus_type == "level1":
        return Level1Bonus(x, y)
    if bonus_type == "level2":
        return Level2Bonus(x, y)
    if bonus_type == "level3":
        return Level3Bonus(x, y)
    if bonus_type == "level4":
        return Level4Bonus(x, y)
    if bonus_type == "level5":
        return Level5Bonus(x, y)

    return None
