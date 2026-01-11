class EnemySpawn:
    def __init__(self, time, enemy_type, x, params=None):
        self.time = time
        self.enemy_type = enemy_type
        self.x = x
        self.params = params or {}


class BossSpawn:
    def __init__(self, time, boss_type, params=None):
        self.time = time
        self.boss_type = boss_type
        self.params = params or {}


class LevelConfig:
    def __init__(self, level_id, enemy_spawns, boss_spawn):
        self.level_id = level_id
        self.enemy_spawns = enemy_spawns
        self.boss_spawn = boss_spawn


class Level:
    def __init__(self, config, enemy_factory, boss_factory):
        self.config = config
        self.enemy_factory = enemy_factory
        self.boss_factory = boss_factory

        self.time = 0
        self.done = False
        self.boss_spawned = False

        self.pending_spawns = list(config.enemy_spawns)

    def update(self, dt, world):
        if self.done:
            return

        self.time += dt

        # Spawn ennemis
        while self.pending_spawns and self.pending_spawns[0].time <= self.time:
            spawn = self.pending_spawns.pop(0)
            enemy = self.enemy_factory(spawn.enemy_type, spawn.x, spawn.params)
            world.add_enemy(enemy)

        # Spawn boss
        if not self.boss_spawned and self.time >= self.config.boss_spawn.time:
            boss = self.boss_factory(self.config.boss_spawn.boss_type,
                                     self.config.boss_spawn.params)
            world.add_boss(boss)
            self.boss_spawned = True

        # Fin du niveau
        if self.boss_spawned and not world.has_boss():
            self.done = True


class LevelManager:
    def __init__(self, levels, enemy_factory, boss_factory):
        self.levels = levels
        self.index = 0
        self.enemy_factory = enemy_factory
        self.boss_factory = boss_factory
        self.current = self._create_level()

    def _create_level(self):
        return Level(
            self.levels[self.index],
            self.enemy_factory,
            self.boss_factory
        )

    def update(self, dt, world):
        self.current.update(dt, world)

        if self.current.done:
            self.index += 1
            if self.index < len(self.levels):
                self.current = self._create_level()
            else:
                print("Tous les niveaux terminés !")


def create_level_1():
    enemy_spawns = [
        EnemySpawn(1, "minion1", 0.2),
        EnemySpawn(2, "minion1", 0.5),
        EnemySpawn(4, "zigzag", 0.8, {"amplitude": 50}),
        EnemySpawn(7, "kamikaze", 0.3),
    ]

    boss = BossSpawn(20, "boss_level_1", {"hp": 500})

    return LevelConfig(1, enemy_spawns, boss)


def create_level_2():
    enemy_spawns = [
        EnemySpawn(1, "minion1", 0.1),
        EnemySpawn(1.5, "minion1", 0.9),
        EnemySpawn(3, "shooter", 0.5),
        EnemySpawn(6, "zigzag", 0.3, {"amplitude": 80}),
    ]

    boss = BossSpawn(25, "boss_level_2", {"hp": 800})

    return LevelConfig(2, enemy_spawns, boss)


def create_level_3():
    enemy_spawns = [
        EnemySpawn(1, "minion1", 0.2),
        EnemySpawn(2, "shooter", 0.7),
        EnemySpawn(4, "zigzag", 0.4, {"amplitude": 100}),
        EnemySpawn(8, "kamikaze", 0.5),
    ]

    boss = BossSpawn(30, "boss_level_3", {"hp": 1000})

    return LevelConfig(3, enemy_spawns, boss)


def create_level_4():
    enemy_spawns = [
        EnemySpawn(0.5, "minion1", 0.1),
        EnemySpawn(1, "minion1", 0.9),
        EnemySpawn(3, "shooter", 0.5),
        EnemySpawn(5, "zigzag", 0.3, {"amplitude": 120}),
        EnemySpawn(9, "kamikaze", 0.6),
    ]

    boss = BossSpawn(35, "boss_level_4", {"hp": 1300})

    return LevelConfig(4, enemy_spawns, boss)


def create_level_5():
    enemy_spawns = [
        EnemySpawn(0.5, "minion1", 0.2),
        EnemySpawn(1.5, "shooter", 0.8),
        EnemySpawn(3, "zigzag", 0.4, {"amplitude": 150}),
        EnemySpawn(6, "kamikaze", 0.5),
        EnemySpawn(10, "shooter", 0.3),
    ]

    boss = BossSpawn(40, "boss_level_5", {"hp": 1800})

    return LevelConfig(5, enemy_spawns, boss)
