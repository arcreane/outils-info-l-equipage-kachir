import pygame

class HUD:
    def __init__(self, font, small_font=None):
        self.font = font
        self.small_font = small_font or font

    def draw(self, surface, player, game_state, level_manager, power_manager=None):
        x = 10
        y = 10
        line = 26

        score_text = self.font.render(f"Score : {game_state.score}", True, (255, 255, 255))
        surface.blit(score_text, (x, y))
        y += line

        hp_text = self.font.render(f"HP : {player.hp}/{player.max_hp}", True, (255, 255, 255))
        surface.blit(hp_text, (x, y))
        y += line

        lives_text = self.font.render(f"Vies : {game_state.lives}", True, (255, 255, 255))
        surface.blit(lives_text, (x, y))
        y += line

        weapon_name = getattr(player.weapon, "name", "Aucune")
        weapon_text = self.font.render(f"Arme : {weapon_name}", True, (255, 255, 255))
        surface.blit(weapon_text, (x, y))
        y += line

        diff_text = self.font.render(f"Difficulté : {game_state.difficulty}", True, (255, 255, 255))
        surface.blit(diff_text, (x, y))
        y += line

        level_id = level_manager.current.config.level_id
        level_text = self.font.render(f"Niveau : {level_id}", True, (255, 255, 255))
        surface.blit(level_text, (x, y))
        y += line

        if power_manager and power_manager.active_power:
            power_name = power_manager.active_power.name
            cooldown = power_manager.get_cooldown_remaining()
            power_text = self.font.render(f"Pouvoir : {power_name} ({cooldown:.1f}s)", True, (0, 200, 255))
        else:
            power_text = self.font.render("Pouvoir : Aucun", True, (150, 150, 150))

        surface.blit(power_text, (x, y))

        self.draw_hp_bar(surface, player)

    def draw_hp_bar(self, surface, player):
        bar_width = 200
        bar_height = 18
        x = 10
        y = surface.get_height() - bar_height - 10

        ratio = player.hp / player.max_hp

        back_rect = pygame.Rect(x, y, bar_width, bar_height)
        fill_rect = pygame.Rect(x, y, int(bar_width * ratio), bar_height)

        pygame.draw.rect(surface, (80, 80, 80), back_rect)
        pygame.draw.rect(surface, (0, 200, 50), fill_rect)
        pygame.draw.rect(surface, (255, 255, 255), back_rect, 2)
