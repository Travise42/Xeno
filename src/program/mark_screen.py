import pygame
import pygame_gui

import json

from program import paint
from program.button import Button
import program.constants as constants

class MarkScreen:
    
    MARGIN = 30
    PADDING = 10
    FEATURE_SIZE = 50
    
    def __init__(self, program):
        self.program = program
        self.display = program.display
        
        self.load_variables()
        
        self.load_graphics()
        self.load_features()
        
        
    def load_variables(self):
        with open(constants.DIR_MONSTER_DATA, "r") as file:
            self.mark_data = json.load(file)
        self.default_data = ["New Monster", "--", "--", True, 0, False, 0, "...", "...", "..."]
        
        if len(self.mark_data) == 0:
            self.mark_data = [[], [0, True, 0, 0]]
        
        self.loaded_monsters = len(self.mark_data[0])
        
        self.monster_index = self.loaded_monsters - 1
        if self.loaded_monsters:
            self.data = self.mark_data[0][self.monster_index] + self.mark_data[1]
        else:
            self.data = ["No Monsters"] + self.default_data[1:] + self.mark_data[1]
        
        self.m = MarkScreen.MARGIN
        self.p = MarkScreen.PADDING
        self.s = MarkScreen.FEATURE_SIZE
        
        self.ft = constants.WIDTH / 3
        self.st = constants.WIDTH * 2 / 3
        self.tt = constants.WIDTH
        
        self.global_loaded_button_focused = False
        
        # Entries
        self.focused_data = None
    
    
    def load_graphics(self):
        self.text_font = pygame.font.SysFont("courier", 20)
        self.label_font = pygame.font.SysFont("courier", 35)
        
        self.separator = paint.draw_separator(constants.HEIGHT/2)
        
        self.load_gui()
        
    def load_gui(self):
        self.entry_textline = pygame_gui.elements.UITextEntryLine((constants.WIDTH//2 - 150, constants.HEIGHT//2 - 30, 300, 60),
                                                                 self.program.manager, object_id="#entry_textline", visible=False)
        self.entry_textbox = pygame_gui.elements.UITextEntryBox([constants.WIDTH//2 - 150, constants.HEIGHT//2 - 60, 300, 120],
                                                                 manager=self.program.manager, object_id="#entry_textbox", visible=False)
    
    def load_features(self):
        
        # Monster Select
        self.left_button = Button(self.m, self.m, self.s, self.s, image_path="src/images/buttons/left.png")
        self.monster_button = Button(self.m + self.s + self.p, self.m, self.st - 3*self.m - 4*self.s - 3*self.p, self.s, "", self.text_font)
        self.right_button = Button(self.st - 2*self.m - 3*self.s - self.p, self.m, self.s, self.s, image_path="src/images/buttons/right.png")
        
        self.add_button = Button(self.st - self.m - 2*self.s - self.p, self.m, self.s, self.s, image_path="src/images/buttons/add.png")
        self.delete_button = Button(self.st - self.m - self.s, self.m, self.s, self.s, image_path="src/images/buttons/delete.png")
        
        # Damage
        self.damage_button = Button(self.st - self.m - 2*self.s - self.p, 2*self.m + self.s, 2*self.s + self.p, self.s, image_path="src/images/buttons/damage.png")
        self.change_button = Button(self.st - self.m - 2*self.s - self.p, 2*self.m + 2*self.s + self.p, 2*self.s + self.p, self.s, "", self.text_font)
        self.heal_button = Button(self.st - self.m - 2*self.s - self.p, 2*self.m + 3*self.s + 2*self.p, 2*self.s + self.p, self.s, image_path="src/images/buttons/heal.png")
        
        # AC
        self.ac_min_button = Button(self.m, 2*self.m + 2*self.s + self.p, 2*self.s + self.p, self.s, "", self.text_font)
        self.ac_max_button = Button(self.m, 2*self.m + 3*self.s + 2*self.p, 2*self.s + self.p, self.s, "", self.text_font)
        self.ac_label = self.label_font.render("AC", True, constants.PALETTE_HIGHLIGHT)
        self.ac_label_pos = (self.m + self.s + self.p/2 - self.ac_label.get_width()/2, 2*self.m + self.s*3/2 - self.ac_label.get_height()/2)
        
        # Options
        self.moved_button = Button(self.st - 3*self.m - 7/2*self.s - 3/2*self.p, 2*self.m + self.s, self.s, self.s, "", self.text_font)
        self.moved_label = self.label_font.render("Moved", True, constants.PALETTE_HIGHLIGHT)
        self.moved_label_pos = (3*self.m + 2*self.s + self.p, 2*self.m + self.s*3/2 - self.moved_label.get_height()/2)
        
        self.damage_total_button = Button(self.st - 3*self.m - 4*self.s - 2*self.p, 2*self.m + 2*self.s + self.p, 2*self.s + self.p, self.s, "", self.text_font)
        self.total_damage_label = self.label_font.render("Damage", True, constants.PALETTE_HIGHLIGHT)
        self.total_damage_label_pos = (3*self.m + 2*self.s + self.p, 2*self.m + self.s*5/2 + self.p - self.total_damage_label.get_height()/2)
        
        self.mark_button = Button(self.st - 3*self.m - 7/2*self.s - 3/2*self.p, 2*self.m + 3*self.s + 2*self.p, self.s, self.s, "", self.text_font)
        self.mark_label = self.label_font.render("Marked", True, constants.PALETTE_HIGHLIGHT)
        self.mark_label_pos = (3*self.m + 2*self.s + self.p, 2*self.m + self.s*7/2 + 2*self.p - self.mark_label.get_height()/2)
        
        # Globals
        self.global_mark_button1 = Button(self.tt - 2*self.m - self.s*3/2 - self.p/2, 2*self.m - self.p, self.s * 2/3, self.s * 2/3, "", self.text_font, rounded_factor=0.7)
        self.global_mark_button2 = Button(self.tt - 2*self.m - self.s*5/6, 2*self.m - self.p, self.s * 2/3, self.s * 2/3, "", self.text_font, rounded_factor=0.7)
        self.global_mark_button3 = Button(self.tt - 2*self.m - self.s*1/6 + self.p/2, 2*self.m - self.p, self.s * 2/3, self.s * 2/3, "", self.text_font, rounded_factor=0.7)
        self.global_mark_label = self.label_font.render("Marks", True, constants.PALETTE_HIGHLIGHT)
        self.global_mark_label_pos = (self.st + 2*self.m, 2*self.m - self.p)
        self.update_global_mark_buttons()

        self.global_moved_button = Button(self.tt - 2*self.m - self.s, 2*self.m + self.s, self.s, self.s, "", self.text_font)
        self.global_moved_label = self.label_font.render("Moved", True, constants.PALETTE_HIGHLIGHT)
        self.global_moved_label_pos = (self.st + 2*self.m, 2*self.m + self.s)

        self.global_loaded_button = Button(self.tt - 2*self.m - self.s, 2*self.m + 2*self.s + self.p, self.s, self.s, "", self.text_font)
        self.global_loaded_label = self.label_font.render("Loaded", True, constants.PALETTE_HIGHLIGHT)
        self.global_loaded_label_pos = (self.st + 2*self.m, 2*self.m + 2*self.s + self.p)

        self.global_shield_button = Button(self.tt - 2*self.m - self.s, 2*self.m + 3*self.s + 2*self.p, self.s, self.s, "", self.text_font)
        self.global_shield_label = self.label_font.render("Shield", True, constants.PALETTE_HIGHLIGHT)
        self.global_shield_label_pos = (self.st + 2*self.m, 2*self.m + 3*self.s + 2*self.p)
        
        # Defenses
        self.resistances_button = Button(self.m, constants.HEIGHT/2 + self.s + 2*self.p, self.ft - 2*self.m, constants.HEIGHT/2 - self.m - self.s - 2*self.p, "", self.text_font, justify=True)
        self.resistances_label = self.label_font.render("Resistances", True, constants.PALETTE_HIGHLIGHT)
        self.resistances_label_pos = (self.m + self.ft/2 - self.m - self.resistances_label.get_width()/2, constants.HEIGHT/2 + self.m + self.s/2 - self.resistances_label.get_height())
        
        self.immunities_button = Button(self.ft + self.m, constants.HEIGHT/2 + self.s + 2*self.p, self.ft - 2*self.m, constants.HEIGHT/2 - self.m - self.s - 2*self.p, "", self.text_font, justify=True)
        self.immunities_label = self.label_font.render("Immunities", True, constants.PALETTE_HIGHLIGHT)
        self.immunities_label_pos = (self.ft + self.m + self.ft/2 - self.m - self.immunities_label.get_width()/2, constants.HEIGHT/2 + self.m + self.s/2 - self.immunities_label.get_height())
        
        self.weaknesses_button = Button(self.st + self.m, constants.HEIGHT/2 + self.s + 2*self.p, self.ft - 2*self.m, constants.HEIGHT/2 - self.m - self.s - 2*self.p, "", self.text_font, justify=True)
        self.weaknesses_label = self.label_font.render("Weaknesses", True, constants.PALETTE_HIGHLIGHT)
        self.weaknesses_label_pos = (self.st + self.m + self.ft/2 - self.m - self.weaknesses_label.get_width()/2, constants.HEIGHT/2 + self.m + self.s/2 - self.weaknesses_label.get_height())
        
        self.update_global_buttons()
        if self.loaded_monsters:
            self.update_monster_buttons()
        else:
            self.update_monster_button()
        
    def open_entry(self, entry: pygame_gui.elements.UITextEntryLine | pygame_gui.elements.UITextEntryBox, focused_data: int, button: Button):
        self.focused_data = (focused_data, button)
        entry.set_text(str(self.data[self.focused_data[0]]))
        entry.show()
        entry.focus()
        entry.select_range = (0, len(entry.get_text()))
        
    def close_entry(self, entry: pygame_gui.elements.UITextEntryLine | pygame_gui.elements.UITextEntryBox):
        self.data[self.focused_data[0]] = entry.get_text()
        self.focused_data[1].change_text(entry.get_text())
        self.focused_data[1].init_draw()
        entry.unfocus()
        entry.hide()
        self.focused_data = None
        
        
    def update(self):
        self.handle_events()
        self.update_buttons()
        
        
    def update_buttons(self):
        self.left_button.update()
        self.monster_button.update()
        self.right_button.update()
        
        self.add_button.update()
        self.delete_button.update()
        
        self.damage_button.update()
        self.change_button.update()
        self.heal_button.update()
        
        self.ac_min_button.update()
        self.ac_max_button.update()
        
        self.moved_button.update()
        self.damage_total_button.update()
        self.mark_button.update()
        
        self.global_mark_button1.update()
        self.global_mark_button2.update()
        self.global_mark_button3.update()
        self.global_moved_button.update()
        self.global_loaded_button.update()
        self.global_shield_button.update()
        
        self.resistances_button.update()
        self.immunities_button.update()
        self.weaknesses_button.update()
    
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.program.screen = constants.SCREEN_MAIN
                if self.entry_textline.visible:
                    self.entry_textline.unfocus()
                    self.entry_textline.hide()
                elif self.entry_textbox.visible:
                    self.entry_textbox.unfocus()
                    self.entry_textbox.hide()
                if self.loaded_monsters:
                    self.post_data()
            elif self.focused_data != None:
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_object_id == "#entry_textline":
                        self.close_entry(self.entry_textline)
                    elif event.ui_object_id == "#entry_textbox":
                        self.close_entry(self.entry_textbox)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.entry_textline.visible and not self.entry_textline.hovered:
                        self.close_entry(self.entry_textline)
                    elif self.entry_textbox.visible and not self.entry_textbox.hovered:
                        self.close_entry(self.entry_textbox)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.entry_textline.visible:
                        self.entry_textline.unfocus()
                        self.entry_textline.hide()
                    elif self.entry_textbox.visible:
                        self.entry_textbox.unfocus()
                        self.entry_textbox.hide()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            
            self.program.manager.process_events(event)
    
    def handle_mouse_up(self, event: pygame.Event):
        self.handle_buttons(event)
        
    def handle_buttons(self, event: pygame.Event):
        if self.left_button.hovered():
            if self.loaded_monsters:
                self.post_data()
                self.monster_index = (self.monster_index - 1) % self.loaded_monsters
                self.data = self.mark_data[0][self.monster_index] + self.mark_data[1]
                self.update_monster_buttons()
        elif self.monster_button.hovered():
            self.open_entry(self.entry_textline, constants.VAR_MONSTER_NAME, self.monster_button)
        elif self.right_button.hovered():
            if self.loaded_monsters:
                self.post_data()
                self.monster_index = (self.monster_index + 1) % self.loaded_monsters
                self.data = self.mark_data[0][self.monster_index] + self.mark_data[1]
                self.update_monster_buttons()
        elif self.add_button.hovered():
            if self.loaded_monsters:
                self.post_data()
            self.monster_index = self.loaded_monsters
            self.loaded_monsters += 1
            self.data = ["New Monster"] + self.default_data[1:] + self.mark_data[1]
            self.mark_data[0].append(self.data[:-4])
            self.update_monster_buttons()
        elif self.delete_button.hovered():
            del self.mark_data[0][self.monster_index]
            self.monster_index -= 1
            self.loaded_monsters -= 1
            if self.loaded_monsters:
                if self.monster_index < 0:
                    self.monster_index = 0
                self.data = self.mark_data[0][self.monster_index] + self.mark_data[1]
                self.update_monster_buttons()
            else:
                self.data = ["No Monsters"] + self.default_data[1:] + self.mark_data[1]
                self.update_monster_button()
        elif self.damage_button.hovered():
            try:
                self.data[constants.VAR_DAMAGE_TOTAL] = int(self.data[constants.VAR_DAMAGE_TOTAL]) + int(self.data[constants.VAR_DAMAGE_CHANGE])
            except:
                return
            self.data[constants.VAR_DAMAGE_CHANGE] = 0
            self.damage_total_button.change_text(str(self.data[constants.VAR_DAMAGE_TOTAL]))
            self.change_button.change_text(str(self.data[constants.VAR_DAMAGE_CHANGE]))
        elif self.change_button.hovered():
            self.open_entry(self.entry_textline, constants.VAR_DAMAGE_CHANGE, self.change_button)
        elif self.heal_button.hovered():
            try:
                self.data[constants.VAR_DAMAGE_TOTAL] = max(0, int(self.data[constants.VAR_DAMAGE_TOTAL]) - int(self.data[constants.VAR_DAMAGE_CHANGE]))
            except:
                return
            self.data[constants.VAR_DAMAGE_CHANGE] = 0
            self.damage_total_button.change_text(str(self.data[constants.VAR_DAMAGE_TOTAL]))
            self.change_button.change_text(str(self.data[constants.VAR_DAMAGE_CHANGE]))
        elif self.ac_min_button.hovered():
            self.open_entry(self.entry_textline, constants.VAR_AC_MIN, self.ac_min_button)
        elif self.ac_max_button.hovered():
            self.open_entry(self.entry_textline, constants.VAR_AC_MAX, self.ac_max_button)
        elif self.moved_button.hovered():
            self.data[constants.VAR_MONSTER_MOVED] = not self.data[constants.VAR_MONSTER_MOVED]
            self.moved_button.change_text("X" if self.data[constants.VAR_MONSTER_MOVED] else "")
        elif self.damage_total_button.hovered():
            self.open_entry(self.entry_textline, constants.VAR_DAMAGE_TOTAL, self.damage_total_button)
        elif self.mark_button.hovered():
            self.data[constants.VAR_MONSTER_MARKED] = not self.data[constants.VAR_MONSTER_MARKED]
            self.mark_button.change_text("X" if self.data[constants.VAR_MONSTER_MARKED] else "")
        elif self.global_mark_button1.hovered():
            self.data[constants.VAR_GLOBAL_MARKS] = (self.data[constants.VAR_GLOBAL_MARKS] != 1) + 0
            self.update_global_mark_buttons()
        elif self.global_mark_button2.hovered():
            self.data[constants.VAR_GLOBAL_MARKS] = (self.data[constants.VAR_GLOBAL_MARKS] != 2) + 1
            self.update_global_mark_buttons()
        elif self.global_mark_button3.hovered():
            self.data[constants.VAR_GLOBAL_MARKS] = (self.data[constants.VAR_GLOBAL_MARKS] != 3) + 2
            self.update_global_mark_buttons()
        elif self.global_moved_button.hovered():
            self.data[constants.VAR_GLOBAL_MOVED] = not self.data[constants.VAR_GLOBAL_MOVED]
            self.global_moved_button.change_text("X" if self.data[constants.VAR_GLOBAL_MOVED] else "")
        elif self.global_loaded_button.hovered():
            if self.global_loaded_button_focused:
                self.data[constants.VAR_GLOBAL_LOADED] = (self.data[constants.VAR_GLOBAL_LOADED] + 1) % 6
            else:
                self.data[constants.VAR_GLOBAL_LOADED] = not self.data[constants.VAR_GLOBAL_LOADED]
                self.global_loaded_button_focused = True
            self.global_loaded_button.change_text(["", "X", "B", "P", "R", "A"][self.data[constants.VAR_GLOBAL_LOADED]])
        elif self.global_shield_button.hovered():
            self.data[constants.VAR_GLOBAL_SHIELD] = (self.data[constants.VAR_GLOBAL_SHIELD] + 1) % 3
            self.global_shield_button.change_text(["", "O", "X"][self.data[constants.VAR_GLOBAL_SHIELD]])
        elif self.resistances_button.hovered():
            self.open_entry(self.entry_textbox, constants.VAR_RESISTANCES, self.resistances_button)
        elif self.immunities_button.hovered():
            self.open_entry(self.entry_textbox, constants.VAR_IMMUNITIES, self.immunities_button)
        elif self.weaknesses_button.hovered():
            self.open_entry(self.entry_textbox, constants.VAR_WEAKNESSES, self.weaknesses_button)
        
    def handle_mouse_motion(self, event: pygame.Event):
        if self.global_loaded_button_focused and not self.global_loaded_button.hovered():
            self.global_loaded_button_focused = False
    
    
    def draw(self):
        self.draw_background()
        self.draw_buttons()
        
        
    def draw_background(self):
        self.display.fill(constants.PALETTE_BACKGROUND)
        
        #pygame.draw.rect(self.display, constants.PALETTE_SHADOW, (self.m/2, self.m/2, self.st - self.m, self.s + self.m), 0, 15)
        pygame.draw.rect(self.display, constants.PALETTE_SHADOW, (self.st + self.m/2, self.m/2 + self.p, self.ft - self.m, constants.HEIGHT / 2 - self.m*2/3 - self.p), 0, 15)
        pygame.draw.rect(self.display, constants.PALETTE_SHADOW, (self.m/2, self.m/2 + self.m + self.s, self.st - self.m, constants.HEIGHT / 2 - self.m*5/3 - self.s), 0, 15)
        
        self.display.blit(self.separator, (constants.WIDTH * 2 / 3 - 13, 0))
        
        if not self.loaded_monsters:
            return
        
        self.display.blit(self.separator, (constants.WIDTH / 3 - 13, constants.HEIGHT/2))
        self.display.blit(self.separator, (constants.WIDTH * 2 / 3 - 13, constants.HEIGHT/2))
    
        
    def draw_buttons(self):
        self.left_button.draw(self.display)
        self.monster_button.draw(self.display)
        self.right_button.draw(self.display)
        
        self.add_button.draw(self.display)
        self.delete_button.draw(self.display)
        
        self.global_mark_button1.draw(self.display)
        self.global_mark_button2.draw(self.display)
        self.global_mark_button3.draw(self.display)
        self.display.blit(self.global_mark_label, self.global_mark_label_pos)
        
        self.global_moved_button.draw(self.display)
        self.display.blit(self.global_moved_label, self.global_moved_label_pos)
        
        self.global_loaded_button.draw(self.display)
        self.display.blit(self.global_loaded_label, self.global_loaded_label_pos)
        
        self.global_shield_button.draw(self.display)
        self.display.blit(self.global_shield_label, self.global_shield_label_pos)
        
        if not self.loaded_monsters:
            return
        
        self.damage_button.draw(self.display)
        self.change_button.draw(self.display)
        self.heal_button.draw(self.display)
        
        self.ac_min_button.draw(self.display)
        self.ac_max_button.draw(self.display)
        self.display.blit(self.ac_label, self.ac_label_pos)
        
        self.moved_button.draw(self.display)
        self.display.blit(self.moved_label, self.moved_label_pos)
        
        self.damage_total_button.draw(self.display)
        self.display.blit(self.total_damage_label, self.total_damage_label_pos)
        
        self.mark_button.draw(self.display)
        self.display.blit(self.mark_label, self.mark_label_pos)
        
        self.resistances_button.draw(self.display)
        self.display.blit(self.resistances_label, self.resistances_label_pos)
        self.immunities_button.draw(self.display)
        self.display.blit(self.immunities_label, self.immunities_label_pos)
        self.weaknesses_button.draw(self.display)
        self.display.blit(self.weaknesses_label, self.weaknesses_label_pos)
        
    def post_data(self):
        self.mark_data[1] = self.data[-4:]
        self.mark_data[0][self.monster_index] = self.data[:-4]
        
        with open(constants.DIR_MONSTER_DATA, "w") as file:
            json.dump(self.mark_data, file)
        
    def update_monster_buttons(self):
        self.update_monster_button()
        self.update_ac_min_button()
        self.update_ac_max_button()
        self.update_moved_button()
        self.update_damage_total_button()
        self.update_mark_button()
        self.update_change_button()
        self.update_resistances_button()
        self.update_immunities_button()
        self.update_weaknesses_button()
        
    def update_monster_button(self):
        self.monster_button.change_text(self.data[constants.VAR_MONSTER_NAME])
        self.monster_button.init_draw()

    def update_ac_min_button(self):
        self.ac_min_button.change_text(self.data[constants.VAR_AC_MIN])
        self.ac_min_button.init_draw()

    def update_ac_max_button(self):
        self.ac_max_button.change_text(self.data[constants.VAR_AC_MAX])
        self.ac_max_button.init_draw()

    def update_moved_button(self):
        self.moved_button.change_text("X" if self.data[constants.VAR_MONSTER_MOVED] else "")
        self.moved_button.init_draw()

    def update_damage_total_button(self):
        self.damage_total_button.change_text(str(self.data[constants.VAR_DAMAGE_TOTAL]))
        self.damage_total_button.init_draw()

    def update_mark_button(self):
        self.mark_button.change_text("X" if self.data[constants.VAR_MONSTER_MARKED] else "")
        self.mark_button.init_draw()

    def update_change_button(self):
        self.change_button.change_text(str(self.data[constants.VAR_DAMAGE_CHANGE]))
        self.change_button.init_draw()

    def update_resistances_button(self):
        self.resistances_button.change_text(self.data[constants.VAR_RESISTANCES])
        self.resistances_button.init_draw()

    def update_immunities_button(self):
        self.immunities_button.change_text(self.data[constants.VAR_IMMUNITIES])
        self.immunities_button.init_draw()

    def update_weaknesses_button(self):
        self.weaknesses_button.change_text(self.data[constants.VAR_WEAKNESSES])
        self.weaknesses_button.init_draw()
        
    def update_global_buttons(self):
        self.update_global_mark_buttons()
        self.update_global_moved_button()
        self.update_global_loaded_button()
        self.update_global_shield_button()
    
    def update_global_mark_buttons(self):
        self.global_mark_button1.change_text("X" if self.data[constants.VAR_GLOBAL_MARKS] >= 1 else "")
        self.global_mark_button2.change_text("X" if self.data[constants.VAR_GLOBAL_MARKS] >= 2 else "")
        self.global_mark_button3.change_text("X" if self.data[constants.VAR_GLOBAL_MARKS] >= 3 else "")
    
    def update_global_moved_button(self):
        self.global_moved_button.change_text("X" if self.data[constants.VAR_GLOBAL_MOVED] else "")
        self.global_moved_button.init_draw()

    def update_global_loaded_button(self):
        self.global_loaded_button.change_text(["", "X", "B", "P", "R", "A"][self.data[constants.VAR_GLOBAL_LOADED]])
        self.global_loaded_button.init_draw()

    def update_global_shield_button(self):
        self.global_shield_button.change_text(["", "O", "X"][self.data[constants.VAR_GLOBAL_SHIELD]])
        self.global_shield_button.init_draw()
    
    