class PlayerStats:
    def __init__(self):
        self.fish = 0
        self.fish_per_second = 0
        self.fish_per_second_multiplier = 1
        self.fish_per_enter = 1
        self.fish_per_enter_multiplier = 1
        self.owned_upgrades = []

class Effect:
    def __init__(self, value):
        self.value = value

class AdditivePerSecondEffect(Effect):

    def effect(self, player_stats: PlayerStats):
        player_stats.fish_per_second += self.value

class Upgrade:
    def __init__(self, name, id, base_cost, cost_growth_rate, effect):
        self.name = name
        self.id = id
        self.effect = effect
        self.base_cost = base_cost
        self.cost_growth_rate = cost_growth_rate
        self.cost = base_cost
        self.level = 0
    
    def buy(self):
        self.level += 1
        self.cost = self.base_cost * (self.cost_growth_rate ** self.level)
    
available_upgrades = {
    "fisher_cat": Upgrade("Fisher Cat", "fisher_cat", 20, 1.07, AdditivePerSecondEffect(1))
}
available_upgrades_list = list(available_upgrades.values())
