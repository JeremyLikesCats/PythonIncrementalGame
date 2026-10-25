class PlayerStats:
    def __init__(self):
        self.fish = 10000
        self.fish_per_second = {
            "+": 0,
            "blessings": 0
        }
        self.fish_per_second_multiplier = {
            "+": 1, #additive
            "*": 1, #multiplicative
            "blessings_+": 0,
            "blessings_*": 1,
        }
        self.fish_per_enter = {
            "+": 1,
            "blessings": 0
        }
        self.fish_per_enter_multiplier = {
            "+": 1, #additive
            "*": 1, #multiplicative
            "blessings_+": 0,
            "blessings_*": 1,
        }
        self.owned_upgrades = []
        self.current_blessings = []
        self.max_blessings = {
            "+": 1,
            "blessings": 0
        }
        self.total_enter_revenue = 0
        self.all_time_revenue = 0
class Effect:
    def __init__(self, value):
        self.value = value

class AdditivePerSecondEffect(Effect):
    def do_effect(self, player_stats: PlayerStats):
        player_stats.fish_per_second["+"] += self.value

class AdditivePerEnterEffect(Effect):
    def do_effect(self, player_stats: PlayerStats):
        player_stats.fish_per_enter["+"] += self.value

class AdditiveMultiplicativePerSecondEffect(Effect):
    def do_effect(self, player_stats: PlayerStats):
        player_stats.fish_per_second_multiplier["+"] *= self.value

class MultiplicativeMultiplicativePerSecondEffect(Effect):
    def do_effect(self, player_stats: PlayerStats):
            player_stats.fish_per_second_multiplier["*"] *= self.value

class AddBlessingSlotEffect(Effect):
    def do_effect(self, player_stats: PlayerStats):
        player_stats.max_blessings["+"] += self.value

class Upgrade:
    def __init__(self, name, id, description, base_cost, cost_growth_rate, effect, is_one_time = False):
        self.name = name
        self.id = id
        self.description = description
        self.effect = effect
        self.base_cost = base_cost
        self.cost_growth_rate = cost_growth_rate
        self.cost = base_cost
        self.is_one_time = is_one_time
        
        self.level = 0
    
    def buy(self):
        self.level += 1
        self.cost = self.base_cost * (self.cost_growth_rate ** self.level)
        
    
available_upgrades = {
    "fisher_cat": Upgrade("Fisher Cat", "fisher_cat", "A little cat that fishes +1 fish for you per second!" ,20, 1.07, AdditivePerSecondEffect(1)),
    "cat_boat": Upgrade("Cat Boat", "cat_boat", "The cat upgraded to a boat. +5 fish per second.", 100, 1.07, AdditivePerSecondEffect(5)),
    "iron_claws": Upgrade("Iron Claws", "iron_claws", "Sharp claws. One-time upgrade. +1 fish per enter hit.", 500, 1, AdditivePerEnterEffect(1), True),
    "fish_farm": Upgrade("Fish Farm", "fish_farm", "Woah a whole fish farm?? +20 fish per second.", 250, 1.07, AdditivePerSecondEffect(20)),
    "blessed_halo": Upgrade("Blessed Halo", "blessed_halo", "This holy item provides you with an extra blessing slot.", 3000, 1, AddBlessingSlotEffect(1), True),
    "golden_claws": Upgrade("Golden Claws", "golden_claws", "Even sharper claws. One-time upgrade. +1 fish per enter hit.", 1000, 1, AdditivePerEnterEffect(1), True),
    "milk": Upgrade("Milk", "milk", "This milk tastes strange... at least it makes your fish generation 100% faster!", 2000, 1, AdditivePerEnterEffect(1), True),
    "fish_factory": Upgrade("Fish Factory", "fish_factory", "This fish factory mass produces +100 fish every second.", 1000, 1.07, AdditivePerSecondEffect(100))
}
available_upgrades_list = list(available_upgrades.values())
