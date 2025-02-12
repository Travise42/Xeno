import pygame
import pygame_gui

import json

import program.constants as constants

import program.paint as paint
from program.button import Button
from program.container import Container
from program.integrity_panel import IntegrityPanel

class MainScreen:
    def __init__(self, program):
        self.program = program
        self.display = self.program.display
        
        self.load_variables()
        self.load_graphics()
        
    def load_variables(self):
        
        self.lp_x = constants.DIMENSION_LEFT_PANEL*constants.WIDTH
        self.rp_x = constants.DIMENSION_RIGHT_PANEL*constants.WIDTH
        
        self.rect_power_display = (20, 10 + ((constants.HEIGHT - 40) // 7)*3, self.lp_x - 40, constants.HEIGHT // 6)
        self.rect_center_panel = (self.lp_x + 40, 20, (self.rp_x - self.lp_x) - 60, constants.HEIGHT - 40)
        self.rect_right_top_panel = (self.rp_x + 40, 55, constants.WIDTH - self.rp_x - 60, constants.HEIGHT//8)
        self.rect_right_middle_panel = (self.rp_x + 40, 170, constants.WIDTH - self.rp_x - 60, constants.HEIGHT//8)
        self.rect_right_bottom_panel = (self.rp_x + 40, constants.HEIGHT//2 + 20, constants.WIDTH - self.rp_x - 60, constants.HEIGHT//2 - 40)
        
        
    def load_graphics(self):
        self.power_font = pygame.font.SysFont("courier", 40)
        self.text_font = pygame.font.SysFont("courier", 20)
        
        self.surf_separators = [paint.draw_separator(constants.HEIGHT), paint.draw_separator(constants.HEIGHT//2)]
        
        self.load_power_buttons()
        self.load_power_display()
        
        self.load_option_buttons()
        
        self.load_gui()
        self.load_containers()
        self.widgets = []
        self.selected_widget = None
        
        self.integrity_panel = IntegrityPanel(constants.DIR_DATA, self.rect_right_bottom_panel)
        
        
    def load_power_buttons(self):
        texts = ["+10", "+5", "+1", "-1", "-5", "-10"]
        self.power_buttons = [Button(20, 25 + ((constants.HEIGHT - 40) // 8)*(i if i < 3 else i + 2),
                                    self.lp_x - 40, constants.HEIGHT // 9, texts[i], self.power_font) 
                              for i in range(6)]
        
        
    def load_power_display(self):
        self.power_display = paint.draw_label(self.rect_power_display[2], self.rect_power_display[3], f"{self.program.current_power}%",
                                              self.power_font, color=(constants.PALETTE_HIGHLIGHT if 100 >= self.program.current_power > 20
                                                                      else constants.PALETTE_ERROR))
        
        
    def load_option_buttons(self):
        self.mark_button = Button(constants.WIDTH*constants.DIMENSION_RIGHT_PANEL + 80, 260,
                                  50, 50, image_path="src/images/buttons/target.png")
        self.stats_button = Button(constants.WIDTH*constants.DIMENSION_RIGHT_PANEL + 153, 260,
                                  50, 50, image_path="src/images/buttons/stats.png")
        
        
    def load_gui(self):
        self.gui_textentry = pygame_gui.elements.UITextEntryLine((constants.WIDTH//2 - 150, constants.HEIGHT//2 - 30, 300, 60),
                                                                 self.program.manager, object_id="#widget_entry", visible=False)
        
    
    def load_containers(self):
        self.containers = [Container(constants.DIR_DATA, self.rect_center_panel, self.text_font, 9, 22),
                           Container(constants.DIR_DATA, self.rect_right_top_panel, self.text_font, 1, 16),
                           Container(constants.DIR_DATA, self.rect_right_middle_panel, self.text_font, 1, 16)]
        
        
        
    def update(self):
        self.handle_events()
        
        self.update_buttons()
        self.integrity_panel.update()
    
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.program.running = False
            elif self.selected_widget != None:
                if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#widget_entry") or (
                        event.type == pygame.MOUSEBUTTONUP and not self.gui_textentry.hovered):
                    self.selected_widget.rename(self.gui_textentry.get_text())
                    self.selected_widget.container.store_container_data()
                    self.selected_widget = None
                    self.gui_textentry.unfocus()
                    self.gui_textentry.hide()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.selected_widget.text == "":
                        for container in self.containers:
                            if self.selected_widget in container.widgets:
                                container.widgets.remove(self.selected_widget)
                    self.selected_widget = None
                    self.gui_textentry.unfocus()
                    self.gui_textentry.hide()
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_movement(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)
            
            self.program.manager.process_events(event)

    def update_buttons(self):
        # Power Buttons
        for power_button in self.power_buttons:
            power_button.update()
            
        # Option Buttons
        self.mark_button.update()
        self.stats_button.update()
        
    def open_entry_widget(self, widget):
        self.selected_widget = widget
        self.gui_textentry.set_text(widget.text)
        self.gui_textentry.show()
        self.gui_textentry.focus()
        
        
        
    def handle_mouse_movement(self, event: pygame.event.Event):
        for container in self.containers:
            container.drag()
        
    def handle_mouse_down(self, event: pygame.event.Event):
        if event.button == 1:
            for container in self.containers:
                container.grab()
        
    def handle_mouse_up(self, event: pygame.event.Event):
        # Power Buttons
        for i, power_button in enumerate(self.power_buttons):
            if power_button.state == Button.STATE_PRESSED:
                self.program.change_power([10, 5, 1, -1, -5, -10][i])
                self.load_power_display()
                break
            
        # Option Buttons
        if self.mark_button.state == Button.STATE_PRESSED:
            self.program.screen = constants.SCREEN_MARK
        elif self.stats_button.state == Button.STATE_PRESSED:
            self.program.screen = constants.SCREEN_STAT
        
        if event.button == 1:
            for container in self.containers:
                container.interact(self)
            
        self.integrity_panel.interact()
        
        if event.button == 4 or event.button == 5:
            if paint.hovering_label(pygame.mouse.get_pos(), self.rect_power_display):
                self.program.change_power(9 - event.button*2)
                self.load_power_display()
    
    
    
    def draw(self):
        self.draw_background()
        self.draw_integrity()
        self.draw_buttons()
        self.draw_widgets()
        
    def draw_background(self):
        self.display.fill(constants.PALETTE_BACKGROUND)
        
        # Center Background
        pygame.draw.rect(self.display, constants.PALETTE_SHADOW, self.rect_center_panel, 0, 12)
        
        # Right Backgrounds
        pygame.draw.rect(self.display, constants.PALETTE_SHADOW, self.rect_right_bottom_panel, 0, 12)
        pygame.draw.rect(self.display, constants.PALETTE_SHADOW, self.rect_right_top_panel, 0, 12)
        pygame.draw.rect(self.display, constants.PALETTE_SHADOW, self.rect_right_middle_panel, 0, 12)
        
        # Seperators
        self.display.blit(self.surf_separators[0], (self.lp_x, 0))
        self.display.blit(self.surf_separators[1], (self.rp_x, 0))
        self.display.blit(self.surf_separators[1], (self.rp_x, constants.HEIGHT//2))
        
        # Power Display
        self.display.blit(self.power_display, self.rect_power_display[:2])
        
    def draw_buttons(self):
        # Power Buttons
        for power_button in self.power_buttons:
            power_button.draw(self.display)
            
        # Option Buttons
        self.mark_button.draw(self.display)
        self.stats_button.draw(self.display)
        
    def draw_widgets(self):
        grabbed = None
        for container in self.containers:
            container.draw(self.display)
            if container.grabbed:
                grabbed = container
            
        if grabbed:
            grabbed.draw_grabbed(self.display)
        
    def draw_integrity(self):
        self.integrity_panel.draw(self.display)