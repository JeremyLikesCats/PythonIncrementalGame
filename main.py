# You're a cat that really likes to eat fish and u try to build a fish empire
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
import os
import stats_and_upgrades
import asyncio

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
        self.prompt_session = PromptSession()

        self.stats = stats_and_upgrades.PlayerStats()
        
        self.ui_options: list[UIOption] = []
        self.current_ui = "main" # UI would switch from "main", "upgrades", etc.

        # UPGRADES UI
        self.upgrades_shown = 1
        self.upgrades_status = "" # Text shown in upgrades_ui

        self._register_ui_option(UIOption("Upgrades", "U", "show_upgrades"))
        
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

    # TODO: add passive income
    async def _passive_income(self):
        while True:
            await asyncio.sleep(1)
            self.stats.fish += self.stats.fish_per_second * self.stats.fish_per_second_multiplier
    
    def _main_screen_ui(self):
        options = "  ".join(opt.formatted() for opt in self.ui_options)
        return (
            f"Fish_TerminalOS 3.0\n\n"
            f"Options:\n{options}\n\n"
            f"Fish: {self.stats.fish}\n"
            f"Press 'enter' to fish. "
        )
        
    def _get_upgrades_prompt(self):
        lines = [
            "Upgrades!~~",
            "Input E to exit",
            f"Current Fish: {self.stats.fish}",
            self.upgrades_status,
        ]
        for i in range(min(self.upgrades_shown, len(stats_and_upgrades.available_upgrades_list))):
            upgrade = stats_and_upgrades.available_upgrades_list[i]
            lines.append(f"[{i}] {upgrade.name}: {upgrade.cost} fish [x{upgrade.level}]")
        
        lines.append("Which upgrade would you like? ")
        return "\n".join(lines)
        
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
            upgrade_index = upgrade_index.strip().upper()
            if upgrade_index == "E":
                self.current_ui = "main"
            else:
                upgrade_index = int(upgrade_index)
                chosen_upgrade = stats_and_upgrades.available_upgrades_list[upgrade_index]
                self.upgrades_status = ""
                if chosen_upgrade.cost > self.stats.fish:
                    self.upgrades_status = "Ur too poor for that"
                else:
                    if chosen_upgrade not in self.stats.owned_upgrades:
                        self.stats.owned_upgrades.append(chosen_upgrade)
                    self.stats.fish -= chosen_upgrade.cost
                    chosen_upgrade.buy()
                    chosen_upgrade.effect.effect(self.stats)
                    self.upgrades_status = f"Successful purchase of {chosen_upgrade.name}!"
    
    
    async def run_game(self):
        income_task = asyncio.create_task(self._passive_income())
        while True:
            await self.show_ui()
            
        
if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run_game())