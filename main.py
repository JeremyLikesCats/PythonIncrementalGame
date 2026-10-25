# You're a cat that really likes to eat fish and u try to build a fish empire
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
import stats_and_upgrades
import asyncio
import random

class UIOption:
    def __init__(self, name, key, function):
        self.name = name
        self.key = key
        self.function = function
    
    def formatted(self):
        return f"{self.name} [{self.key}]"

# You can either roll a good blessing or a bad blessing. 
# Blessings give stat boosts and have special abilities.
class Blessing:
    def __init__(self, name, id, roll_weight, is_curse = False):
        self.name = name
        self.id = id
        self.roll_weight = roll_weight
        self.is_curse = is_curse
        
        
# Blessing of the fish - every second there is a 20% chance for you to gain 10x your fish per second and 2% chance for you to gain 100x your fish per second
class BlessingOfTheFish(Blessing):
    def do_effect(self, player_stats: stats_and_upgrades.PlayerStats):
        player_stats.current_blessings.append(self)
    

class Game:
    def clear_screen(self):
        print("\033[H\033[2J", end="")
        
    def __init__(self):
        # Initialize Prompt toolkit bindings
        
        self.key_bindings = KeyBindings()
        self.prompt_session = PromptSession()

        self.stats = stats_and_upgrades.PlayerStats()
        
        self.ui_options: list[UIOption] = []
        self.current_ui = "main" # UI would switch from "main", "upgrades", etc.

        # MAIN UI
        self.main_ui_passive_status = ""
        
        # UPGRADES UI
        self.upgrades_shown = 1
        self.upgrades_status = "" # Text shown in upgrades_ui

        self._register_ui_option(UIOption("Upgrades", "U", "show_upgrades"))
        
        # BLESSINGS
        self.blessings_cost = 1000
        self.available_blessings = [BlessingOfTheFish("Blessing of the Fish", "blessing_of_the_fish", 1)]

        # BASIC FISHING
        @self.key_bindings.add("enter")
        def _(event):
            self.stats.fish += (
                self.stats.fish_per_enter * self.stats.fish_per_enter_multiplier
            )
            event.app.invalidate()
            
        
            
    def _register_ui_option(self, ui_option):
        self.ui_options.append(ui_option)
        self.key_bindings.add(ui_option.key.lower())(getattr(self, ui_option.function))
        self.key_bindings.add(ui_option.key.upper())(getattr(self, ui_option.function))
        
    def show_upgrades(self, event=None):
        self.current_ui = "upgrades"
        event.app.exit()

    def show_blessings_roller(self, event=None):
        self.current_ui = "blessings_roller"
        event.app.exit()
    
    async def _passive_income(self):
        
        while True:
            await asyncio.sleep(1)
            # Also Resets passive status
            self.main_ui_passive_status = ""
            
            self.stats.fish += self.stats.fish_per_second * self.stats.fish_per_second_multiplier
            
            # Blessings that affect passive income
            for blessing in self.stats.current_blessings:
                if blessing.id == "blessing_of_the_fish":
                    if random.randint(1, 100) <= 20:
                        self.stats.fish += self.stats.fish_per_second * self.stats.fish_per_second_multiplier * 10
                        self.main_ui_passive_status += f"Blessing of the fish! +{self.stats.fish_per_second * self.stats.fish_per_second_multiplier * 10} "
                    if random.randint(1, 100) <= 2:
                        self.stats.fish += self.stats.fish_per_second * self.stats.fish_per_second_multiplier * 100
                        self.main_ui_passive_status += f"ULTIMATE Blessing of the fish! +{self.stats.fish_per_second * self.stats.fish_per_second_multiplier * 100}"

            
    def _main_screen_ui(self):
        options = "  ".join(opt.formatted() for opt in self.ui_options)
        
        return (
            f"Fish_TerminalOS 3.0\n\n"
            f"Options:\n{options}\n\n"
            f"Fish: {self.stats.fish} (+{self.stats.fish_per_second * self.stats.fish_per_second_multiplier} fish/s){" (" if self.main_ui_passive_status != "" else "" + self.main_ui_passive_status + ")" if self.main_ui_passive_status != "" else ""}\n"
            f"Press 'enter' to fish. "
        )
        
    def _get_upgrades_prompt(self):
        lines = [
            "Upgrades!~~",
            "Input E to exit",
            f"Current Fish: {self.stats.fish}",
            self.upgrades_status,
        ]
        i = 0
        count = 0
        while count < min(self.upgrades_shown, len(stats_and_upgrades.available_upgrades_list)) and i < len(stats_and_upgrades.available_upgrades_list):
            upgrade = stats_and_upgrades.available_upgrades_list[count]
            if upgrade.is_one_time and upgrade.level > 0:
                i += 1
                continue
            lines.append(f"[{count}] {upgrade.name}: {upgrade.cost} fish [x{upgrade.level}]")
            lines.append(f"{upgrade.description}")
            lines.append("")
            i += 1
            count += 1
        
        lines.append("Which upgrade would you like? ")
        
        return "\n".join(lines)
        
    def _get_blessings_roller_prompt(self):
        return (
            f"BLESSINGS ROLLER"
            f"Would you like to roll a blessing ({self.blessings_cost} fish)? (Y/N) "
        )
        
    async def show_ui(self):
        self.clear_screen()
        if self.current_ui == "main":

            await self.prompt_session.prompt_async(
                self._main_screen_ui, 
                key_bindings=self.key_bindings,
                refresh_interval=0.5
            )


        elif self.current_ui == "upgrades":
            upgrade_index = await self.prompt_session.prompt_async(
                self._get_upgrades_prompt, 
                key_bindings=KeyBindings(),
                refresh_interval=0.5
            )
            
            # Create a link between index and count (list index vs number that shows up in ui)
            index_list = []
            count = 0
            i = 0
            while count < min(self.upgrades_shown, len(stats_and_upgrades.available_upgrades_list)) and i < len(stats_and_upgrades.available_upgrades_list):
                upgrade = stats_and_upgrades.available_upgrades_list[i]
                if upgrade.is_one_time and upgrade.level > 0:
                    i += 1
                    continue
                index_list.append(i)
                i += 1
                count += 1
                
                
            upgrade_index = upgrade_index.strip().upper()
            if upgrade_index == "E":
                self.current_ui = "main"
            else:
                upgrade_index = index_list[int(upgrade_index)]
                chosen_upgrade = stats_and_upgrades.available_upgrades_list[upgrade_index]
                self.upgrades_status = ""
                if chosen_upgrade.cost > self.stats.fish:
                    self.upgrades_status = "Ur too poor for that"
                else:
                    if chosen_upgrade not in self.stats.owned_upgrades:
                        self.stats.owned_upgrades.append(chosen_upgrade)
                    self.stats.fish -= chosen_upgrade.cost
                    chosen_upgrade.buy()
                    chosen_upgrade.effect.do_effect(self.stats)
                    self.upgrades_status = f"Successful purchase of {chosen_upgrade.name}!"
                    
        elif self.current_ui == "blessings_roller":
            roll_blessing = await self.prompt_session.prompt_async(
                            self._get_blessings_roller_prompt, 
                            key_bindings=KeyBindings(),
                            refresh_interval=0.5
                        )
            roll_blessing = roll_blessing.strip().upper()
            if roll_blessing == "Y":
                blessing = self.choose_random_blessing()
                self.stats.current_blessings.pop(0)
                self.stats.current_blessings.append(blessing)
                
                
    def choose_random_blessing(self):
        # Weighted randomness
        values = []
        current = 0
        for blessing in self.available_blessings:
            current += blessing.roll_weight
            values.append(current)
        number = random.randint(1, current) 
        for index, value in enumerate(values):
            if number <= value:
                continue
            else:
                return blessing[index]
    
    def check_milestones(self):
        # Check if certain milestones are reached to unlock more upgrades
        
        ## UPGRADE MILESTONES
        
        # UPGRADE MILESTONES - OWNED UPGRADES 
        for upgrade in self.stats.owned_upgrades:
            # Unlock Boat Cat at fisher cat lvl 5
            if upgrade.id == "fisher_cat":
                if upgrade.level == 5:
                    self._set_upgrades_shown_amount(2)
        # UPGRADE MILESTONES - MONEY MILESTONES
        # Unlock iron claws at 500 fish
        if self.stats.fish >= 500:
            self._set_upgrades_shown_amount(3)
        
        
        ## UI MILESTONES
        
        # UI MILESTONES - MONEY MILESTONES
        if self.stats.fish >= 1000:
            if len(self.key_bindings.get_bindings_for_keys("b")) == 0:
                self._register_ui_option(UIOption("Blessings Roller", "b", "show_blessings_roller"))
    
    def _set_upgrades_shown_amount(self, amount):
        self.upgrades_shown = max(amount, self.upgrades_shown)
                    
            
    
    async def run_game(self):
        income_task = asyncio.create_task(self._passive_income())
        while True:
            await self.show_ui()
            self.check_milestones()
            
        
if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run_game())