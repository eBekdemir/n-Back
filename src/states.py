import os
import pygame
import src.settings as set
from random import randint, choice
import json

letters = [i for i in os.listdir("src/letters")]
pygame.mixer.init()

settings = set.get_settings()
if settings['sqr_col'] in settings['sqr_colors']:
    settings['sqr_colors'].remove(settings['sqr_col'])



class StateManager:
    """
    State (screen) manager
    """
    def __init__(self):
        self.states = {
            "loading": LoadingState(),
            "menu": MenuState(),
            "voice-pos":GameState('vp'),
            "color-pos":GameState('cp'),
            "voice-col":GameState('vc'),
            "trip":GameState('vcp'),
            "settings":set.SettingsState(),
            "stat":StatisticsState()
        }
        self.current_state = self.states["loading"]

    def switch_state(self, new_state):
        self.current_state.reset()
        self.current_state = self.states[new_state]
        self.current_state.reset()

    def update(self, events):
        next_state = self.current_state.update(events)
        if next_state == "quit":
            return "quit"
        if next_state:
            self.switch_state(next_state)

    def render(self, screen, size):
        self.current_state.render(screen, size)


class LoadingState:
    """
    Loading Screen
    """
    def __init__(self):
        ...

    def reset(self) -> None:
        ...

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE, pygame.K_BACKSPACE, pygame.K_ESCAPE]:
                    return "menu"  # Switch to the menu state
    def render(self, screen, screen_size):
        screen.fill(set.BLACK)
        text = set.times48.render("Welcome to Dual N-Back!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_size[0]/2, screen_size[1]/2)) # centers the text
        screen.blit(text, text_rect)
        text2 = set.times24.render("- press enter ~Kömen -", True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(screen_size[0]/2, (screen_size[1]/2)+60))
        screen.blit(text2, text2_rect)


class MenuState:
    """
    Menu Screen
    """
    def __init__(self):
        ...

    def reset(self) -> None:
        ...

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.voice_pos.is_clicked(event):
                    return "voice-pos"
                if self.col_pos.is_clicked(event):
                    return "color-pos"
                if self.voice_color.is_clicked(event):
                    return "voice-col"
                if self.trip.is_clicked(event):
                    return "trip"
                if self.sett.is_clicked(event):
                    return "settings"
                if self.stat.is_clicked(event):
                    return "stat"
                if self.qt.is_clicked(event):
                    return "quit"
                

    def render(self, screen, screen_size):
        screen.fill(set.MAIN_COLOR)
        w, h = screen_size
        button_w = 250
        button_h = 50
        button_margin = 20
        total_height = (button_h + button_margin) * 7 - button_margin # total height of buttons

        # buttons 
        self.voice_pos = set.Button((w-button_w)//2, (h-total_height)//2, button_w, button_h, 'Voice - Position n-Back', set.jbcode24, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.voice_pos.draw(screen)
        self.col_pos = set.Button((w-button_w)//2, (h-total_height)//2 + (button_h + button_margin), button_w, button_h, 'Color - Position n-Back', set.jbcode24, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.col_pos.draw(screen)
        self.voice_color = set.Button((w-button_w)//2, (h-total_height)//2 + (button_h + button_margin)*2, button_w, button_h, 'Voice - Color n-Back', set.jbcode24, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.voice_color.draw(screen)
        self.trip = set.Button((w-button_w)//2, (h-total_height)//2 + (button_h + button_margin)*3, button_w, button_h, 'Triple n-Back', set.jbcode24, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.trip.draw(screen)
        self.sett = set.Button((w-button_w)//2, (h-total_height)//2 + (button_h + button_margin)*4, button_w, button_h, 'Settings', set.jbcode24, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.sett.draw(screen)
        self.stat = set.Button((w-button_w)//2, (h-total_height)//2 + (button_h + button_margin)*5, button_w, button_h, 'Statistics', set.jbcode24, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.stat.draw(screen)
        self.qt = set.Button((w-button_w)//2, (h-total_height)//2 + (button_h + button_margin)*6, button_w, button_h, 'Quit', set.jbcode24, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.qt.draw(screen)


class StatisticsState:
    """
    Statistics Screen
    """
    def __init__(self):
        self.stats = None

    def reset(self) -> None:
        self.stats = self.get_stats()

    def get_stats(self) -> dict:
        with open('src/stats.json', 'r', encoding='utf-8') as file:
            stats = json.load(file)
        return stats
    
    def reset_stats(self) -> None:
        self.stats = {'type':['TRUE', 'WRONG', 'MISS'], 't_time':'TIME','color': [0, 0, 0], 'position': [0, 0, 0], 'voice': [0, 0, 0], 'c_time':0, 'p_time':0, 'v_time':0}
        with open('src/stats.json', 'w', encoding='utf-8') as file:
            json.dump(self.stats, file)
        return

    def time_convertor(self, total_seconds:int) -> str:
        if total_seconds < 60:
            return f"{total_seconds}s"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes}m {seconds}s"
        else:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    return "menu" 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.res.is_clicked(event):
                    self.reset_stats()
                if self.qt.is_clicked(event):
                    return "menu"
                
    def render(self, screen, screen_size):
        screen.fill(set.MAIN_COLOR)
        if not self.stats:
            self.stats = self.get_stats()
        w, h = screen_size
        total_w = 500
        each_h = 50
        hmargin = 20
        wmargin = 10
        total_height = (each_h + hmargin) * 6 - hmargin # total height of frame

        # stats
        for i, val in enumerate(['TYPE', 'COLOR', 'POSITION', 'VOICE']):
            rect = pygame.Rect((w-total_w)//2, (h-total_height)//2 + (each_h + hmargin)*(i+1), 120, each_h)
            text_rect = pygame.draw.rect(screen, set.BUTTON_COLOR, rect, border_radius=8)
            text_surf = set.jbcode24.render(val, True, set.TEXT_COLOR)
            text_rect = text_surf.get_rect(center=rect.center) 
            screen.blit(text_surf, text_rect)
            for ind in range(3):
                rect = pygame.Rect((w-total_w)//2 + (ind+1)*wmargin + (ind)*60 + 120, (h-total_height)//2 + (each_h + hmargin)*(i+1), 60, each_h)
                text_rect = pygame.draw.rect(screen, set.BUTTON_COLOR, rect, border_radius=8)
                text_surf = set.jbcode24.render(str(self.stats[val.lower()][ind]), True, set.TEXT_COLOR)
                text_rect = text_surf.get_rect(center=rect.center) 
                screen.blit(text_surf, text_rect)
            
            rect = pygame.Rect((w-total_w)//2 + (4)*wmargin + (3)*60 + 120, (h-total_height)//2 + (each_h + hmargin)*(i+1), 60, each_h)
            text_rect = pygame.draw.rect(screen, set.BUTTON_COLOR, rect, border_radius=8)
            if val != 'TYPE' and (self.stats[val.lower()][0] + self.stats[val.lower()][1] + self.stats[val.lower()][2]) != 0:
                succes = (self.stats[val.lower()][0]/(self.stats[val.lower()][0] + self.stats[val.lower()][1] + self.stats[val.lower()][2]))*100
                text_surf = set.jbcode24.render(f"{int(succes)}%", True, set.TEXT_COLOR)
            elif val != 'TYPE':
                text_surf = set.jbcode24.render('None', True, set.TEXT_COLOR)
            else:
                text_surf = set.jbcode24.render('SUCCES', True, set.TEXT_COLOR)
            text_rect = text_surf.get_rect(center=rect.center) 
            screen.blit(text_surf, text_rect)
            rect = pygame.Rect((w-total_w)//2 + (5)*wmargin + (4)*60 + 120, (h-total_height)//2 + (each_h + hmargin)*(i+1), 90, each_h)
            text_rect = pygame.draw.rect(screen, set.BUTTON_COLOR, rect, border_radius=8)
            if val == 'TYPE':
                text_surf = set.jbcode24.render(str(self.stats[val.lower()[0]+'_time']), True, set.TEXT_COLOR)
            else:
                text = self.time_convertor(self.stats[val.lower()[0]+'_time'])
                text_surf = set.jbcode24.render(text, True, set.TEXT_COLOR)
            text_rect = text_surf.get_rect(center=rect.center) 
            screen.blit(text_surf, text_rect)
                
        # buttons 
        self.qt = set.Button((w-total_w)//2, (h-total_height)//2, total_w, each_h, 'Quit', set.jbcode24, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.qt.draw(screen)
        self.res = set.Button((w-total_w)//2, (h-total_height)//2 + (each_h + hmargin)*5, total_w, each_h, 'Reset', set.jbcode24, set.BUTTON_COLOR, set.BUTTON_COLOR, set.TEXT_COLOR)
        self.res.draw(screen)

class GameState:
    """
    Game screen
    it takes a type argument:
        'vp' = voice position
        'cp' = color position
        'vc' = voice color
        'vcp' = voice color and position
    """
    def __init__(self, type) -> None:
        self.type = type
        self.game_time = None
        self.N_step = settings['N']
        self.grid_proc = 2
        self.memory = {'color':[], 'position':[], 'voice':[]}
        self.color_match = None
        self.color_insensible = None
        self.position_match = None
        self.position_insensible = None
        self.voice_match = None
        self.voice_insensible = None
        self.ind_statistics = {'color': [0, 0, 0], 'position': [0, 0, 0], 'voice': [0, 0, 0]} # T, Wrong, Missed
        self.settings = set.get_settings()
        self.in_state = 1
    
    def start_timer(self) -> None:
        self.start_time = pygame.time.get_ticks()
    
    def start_game_timer(self) -> None:
        self.game_time = pygame.time.get_ticks()

    def reset(self) -> None:
        self.game_time = None
        self.N_step = settings['N']
        self.grid_proc = 2
        self.memory = {'color':[], 'position':[], 'voice':[]}
        self.color_match = None
        self.color_insensible = None
        self.position_match = None
        self.position_insensible = None
        self.voice_match = None
        self.voice_insensible = None
        self.ind_statistics = {'color': [0, 0, 0], 'position': [0, 0, 0], 'voice': [0, 0, 0]}
        self.in_state = 1

    def update_stats(self, new_states) -> None:
        old_states = StatisticsState().get_stats()
        old_states['color'][0] += new_states['color'][0]
        old_states['color'][1] += new_states['color'][1]
        old_states['color'][2] += new_states['color'][2]
        old_states['position'][0] += new_states['position'][0]
        old_states['position'][1] += new_states['position'][1]
        old_states['position'][2] += new_states['position'][2]
        old_states['voice'][0] += new_states['voice'][0]
        old_states['voice'][1] += new_states['voice'][1]
        old_states['voice'][2] += new_states['voice'][2]
        old_states['c_time'] += new_states['c_time']
        old_states['p_time'] += new_states['p_time']
        old_states['v_time'] += new_states['v_time']
        with open('src/stats.json', 'w', encoding='utf-8') as file:
            json.dump(old_states, file)
        return

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    time =  (pygame.time.get_ticks()-self.game_time)//1000
                    if 'v' in self.type:
                        self.ind_statistics['v_time'] = time
                    else:
                        self.ind_statistics['v_time'] = 0
                    if 'p' in self.type:
                        self.ind_statistics['p_time'] = time
                    else:
                        self.ind_statistics['p_time'] = 0
                    if 'c' in self.type:
                        self.ind_statistics['c_time'] = time
                    else:
                        self.ind_statistics['c_time'] = 0
                    self.update_stats(self.ind_statistics)
                    return "menu" 

                if event.key == self.settings['color_match_key']:
                    if self.color_match:
                        self.ind_statistics['color'][0] += 1
                        self.color_insensible = True
                        self.color_match = None
                    elif not self.color_insensible:
                        self.ind_statistics['color'][1] += 1
                        self.color_insensible = True

                if event.key == self.settings['voice_match_key']:
                    if self.voice_match:
                        self.ind_statistics['voice'][0] += 1
                        self.voice_insensible = True
                        self.voice_match = None
                    elif not self.voice_insensible:
                        self.ind_statistics['voice'][1] += 1
                        self.voice_insensible = True

                if event.key == self.settings['position_match_key']:
                    if self.position_match:
                        self.ind_statistics['position'][0] += 1
                        self.position_insensible = True
                        self.position_match = None
                    elif not self.position_insensible:
                        self.ind_statistics['position'][1] += 1
                        self.position_insensible = True

    def render(self, screen, screen_size):
        if not self.game_time:
            self.start_game_timer()
        screen.fill(set.MAIN_COLOR)
        self.grid(screen, screen_size)
        if self.in_state:
            self.in_state = 0
            self.settings = set.get_settings()

        # visualise the stats
        stat_text = f"N: {self.settings['N']} "
        if 'p' in self.type:
            stat_text = stat_text + f"P: {self.ind_statistics['position'][0] - self.ind_statistics['position'][1] - self.ind_statistics['position'][2]} "
        if 'v' in self.type:
            stat_text = stat_text + f"V: {self.ind_statistics['voice'][0] - self.ind_statistics['voice'][1] - self.ind_statistics['voice'][2]} "
        if 'c' in self.type:
            stat_text = stat_text + f"C: {self.ind_statistics['color'][0] - self.ind_statistics['color'][1] - self.ind_statistics['color'][2]} "
        stat_text = stat_text + f"T: {round((pygame.time.get_ticks() - self.game_time)/1000, 2):.2f}"
        text = set.jbcode24.render(stat_text, True, set.TEXT_COLOR)
        stat_rect = text.get_rect(center=(screen_size[0]/2, 20))
        screen.blit(text, stat_rect)

    def grid(self, screen, screen_size) -> None:
        """
        it creates and draws grid
        and then mutate the squares
        """

        # creates default grid
        if 'p' in self.type:
            grid_x, grid_y = self.settings['grid']
        else: 
            grid_x, grid_y = 1, 1
        square_leng = (screen_size[0]-150-(self.settings['grid_margin']*(grid_x-1)))//grid_x if (screen_size[0]-150-(self.settings['grid_margin']*(grid_x-1)))//grid_x < (screen_size[1]-150-(self.settings['grid_margin']*(grid_y-1)))//grid_y else (screen_size[1]-150-(self.settings['grid_margin']*(grid_y-1)))//grid_y
        w_gap = (screen_size[0] - (grid_x * square_leng + (grid_x-1)*self.settings['grid_margin']))//2 # left and right gaps
        h_gap = (screen_size[1] - (grid_y * square_leng + (grid_y-1)*self.settings['grid_margin']))-10 # top gap (bottom is less then top (10 px))
        for sqr_x in range(grid_x):
            for sqr_y in range(grid_y):
                sqr = pygame.Rect(w_gap + sqr_x*(square_leng+self.settings['grid_margin']), h_gap + sqr_y*(square_leng+self.settings['grid_margin']),square_leng,square_leng)
                pygame.draw.rect(screen, set.SQUARE_COLOR, sqr)

        self.type_ops(screen, square_leng, w_gap, h_gap)

    def type_ops(self, screen, square_leng, w_gap, h_gap):
        # defines color, position, and voice, then matchs with n-back
        if self.grid_proc == 2:
            self.start_timer()
            if 'c' in self.type:
                if not self.settings['mode'][0] and randint(0, self.settings['mode'][1]-1) == 0 and len(self.memory['color'])>=(self.settings['N']+1):
                    selected_square_color = self.memory['color'][-self.settings['N']]
                else:
                    selected_square_color = choice(self.settings['sqr_colors'][1:])
                self.memory['color'].append(selected_square_color)
                if len(self.memory['color'])>=(self.settings['N']+1):
                    if self.memory['color'][-1] == self.memory['color'][-1-self.settings['N']]:
                        self.color_match = True
            elif len(self.memory['color'])<1:
                    self.memory['color'].append(self.settings['sel_sqr'])

            if 'p' in self.type:
                if not self.settings['mode'][0] and randint(0, self.settings['mode'][1]-1) == 0 and len(self.memory['position'])>=(self.settings['N']+1):
                    selected_x, selected_y = self.memory['position'][-self.settings['N']]
                else:    
                    selected_x, selected_y = randint(0, self.settings['grid'][0]-1), randint(0, self.settings['grid'][1]-1)
                self.memory['position'].append([selected_x, selected_y])
                if len(self.memory['position'])>=(self.settings['N']+1):
                    if self.memory['position'][-1] == self.memory['position'][-1-self.settings['N']]:
                        self.position_match = True
            elif len(self.memory['position'])<1:
                self.memory['position'].append([0, 0])
            
            if 'v' in self.type:
                if not self.settings['mode'][0] and randint(0, self.settings['mode'][1]-1) == 0 and len(self.memory['voice'])>=(self.settings['N']+1):
                    sound_path = self.memory['voice'][-self.settings['N']]
                else:
                    sound_path = f"src/letters/{choice(letters)}"
                self.memory['voice'].append(sound_path)
                if len(self.memory['voice'])>=(self.settings['N']+1):
                    if self.memory['voice'][-1] == self.memory['voice'][-1-self.settings['N']]:
                        self.voice_match = True
                
                pygame.mixer.Sound(sound_path).play()

            self.grid_proc = 0

        # color the selected square
        elif self.grid_proc == 0:
            proc_time = (pygame.time.get_ticks() - self.start_time) / 1000
            if proc_time >= self.settings['proc_time']:
                self.start_timer()
                self.grid_proc += 1
            sqr = pygame.Rect(w_gap + self.memory['position'][-1][0]*(square_leng+self.settings['grid_margin']), h_gap + self.memory['position'][-1][1]*(square_leng+self.settings['grid_margin']),square_leng,square_leng)
            pygame.draw.rect(screen, self.memory['color'][-1], sqr)

        # decolor the selected square and check if user answered 
        elif self.grid_proc == 1:
            proc_time = (pygame.time.get_ticks() - self.start_time) / 1000
            if proc_time >= self.settings['gap_time']:
                if self.color_match == True:
                    self.ind_statistics['color'][2] += 1
                if self.position_match == True:
                    self.ind_statistics['position'][2] += 1
                if self.voice_match == True:
                    self.ind_statistics['voice'][2] += 1
                self.color_match = None
                self.color_insensible = None
                self.position_match = None
                self.position_insensible = None
                self.voice_match = None
                self.voice_insensible = None
                self.grid_proc += 1

        