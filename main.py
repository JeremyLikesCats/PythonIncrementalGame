# You're a cat that really likes to eat fish and u try to build a fish empire
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings

import stats_and_upgrades


class UIOption:
    def __init__(self, name, key, function):
        self.name = name
        self.key = key
        self.function = function
    
    def formatted(self):
        return f"{self.name} [{self.key}]"


class Game:
    def clear_screen(self):
        print("\033[H\033[2J", end="")
        
    def __init__(self):
        # Initialize Prompt toolkit bindings
        
        self.key_bindings = KeyBindings()

        self.stats = stats_and_upgrades.PlayerStats()
        
        self.ui_options: list[UIOption] = []
        self.current_ui = "main" # UI would switch from "main", "upgrades", etc.

        # UPGRADES UI
        self.upgrades_shown = 1
        self.upgrades_status = "" # Text shown in upgrades_ui

        self._register_ui_option(UIOption("Upgrades", "U", "show_upgrades"))
        self.run_game()
    
    def _register_ui_option(self, ui_option):
        self.ui_options.append(ui_option)
        self.key_bindings.add(ui_option.key.lower())(getattr(self, ui_option.function))
        
    def show_upgrades(self, event=None):
        self.current_ui = "upgrades"
        event.app.exit()
        self.show_ui()
    
    def show_ui(self):
        self.clear_screen()
        if self.current_ui == "main":
            print("Fish_TerminalOS 3.0")
            print("")
            
            # Show options
            print("Options: ")
            for option in self.ui_options:
                print(option.formatted(), end = "  ")
                
            # Show fish
            print()
            print()
            print("Fish: " + str(self.stats.fish))
            prompt("Press 'enter' to fish. ", key_bindings=self.key_bindings)
            if self.current_ui == "main":
                self.stats.fish += self.stats.fish_per_enter * self.stats.fish_per_enter_multiplier
        elif self.current_ui == "upgrades":
            print("Upgrades!~~")
            print(self.upgrades_status)
            for i in range(min(self.upgrades_shown, len(stats_and_upgrades.available_upgrades_list))):
                upgrade = stats_and_upgrades.available_upgrades_list[i]
                print(f"[{i}] {upgrade.name}: {upgrade.cost} fish [x{upgrade.level}]")

            upgrade_index = int(prompt("Which upgrade would you like? ").strip())
            chosen_upgrade = stats_and_upgrades.available_upgrades_list[upgrade_index]
            self.upgrades_status = ""
            if chosen_upgrade.cost > self.stats.fish:
                self.upgrades_status = "Ur too poor for that"
            else:
                if chosen_upgrade not in self.stats.owned_upgrades:
                    self.stats.owned_upgrades.append(chosen_upgrade)
                chosen_upgrade.buy()
                chosen_upgrade.effect.effect(self.stats)
                self.stats.fish -= chosen_upgrade.cost
                self.upgrades_status = f"Successful purchase of {chosen_upgrade.name}!"
    
    
    def run_game(self):
        while True:
            self.show_ui()
        
if __name__ == "__main__":
    game = Game()