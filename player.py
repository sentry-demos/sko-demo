class Player:
    def __init__(self, name="Engineer", level=1, hp=100, mp=50, inventory=None, xp=0):
        self.name = name
        self.level = level
        self.hp = hp
        self.mp = mp
        self.xp = xp
        self.inventory = inventory or ["Rusty Sword", "Healing Potion"]

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def restore_hp(self, amount):
        # assuming a maximum HP of 100
        self.hp = min(100, self.hp + amount)

    def use_mp(self, amount):
        self.mp = max(0, self.mp - amount)

    def restore_mp(self, amount):
        # assuming a maximum MP of 50
        self.mp = min(50, self.mp + amount)

    def gain_xp(self, amount):
        self.xp += amount
        # Level up if XP exceeds the threshold (e.g., 100 * current level)
        if self.xp >= 100 * self.level:
            self.level += 1
            self.xp = 0  # reset XP after leveling up

    def add_item(self, item):
        self.inventory.append(item) 