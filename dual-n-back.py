# from memory_profiler import profile
import pygame
import sys
import os
os.environ['SDL_VIDEO_CENTERED'] = '1' # centers the screen
pygame.init()

import win32con
import win32gui

class Call_Window():
    """
    it makes screen maximized
    u/Voir-dire
    https://www.reddit.com/r/pygame/comments/12eklyg/comment/jux1w6e/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    """

    def find_window(window_title):
        # Use window title to get window's handle
        window_handle = win32gui.FindWindow(None,window_title)
        return window_handle

    def maximize_window(window_handle):
            # Get current status
            window_placement = win32gui.GetWindowPlacement(window_handle)
            
            # If minimized currently, restore it
            if window_placement[1] == win32con.SW_SHOWMINIMIZED:
                win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
            
            # Maximize it
            win32gui.ShowWindow(window_handle, win32con.SW_MAXIMIZE)

import src.settings as set
import src.states as states

# Main game loop
# @profile
def process() -> None:
    settings = set.init_settings()
    if settings['fullscreen']:
        info = pygame.display.Info()
        SCREEN_WIDTH, SCREEN_HEIGHT = (info.current_w-10, info.current_h-25)
        sets = set.get_settings()
        sets['width'], sets['height'] = (info.current_w, info.current_h)
        set.dump_settings(sets)
        del sets
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    else:
        SCREEN_WIDTH, SCREEN_HEIGHT = (settings['width']-10, settings['height']-40)
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    # else:
    #     info = pygame.display.Info()
    #     screen = pygame.display.set_mode((info.current_w-10, info.current_h-50), pygame.RESIZABLE)

    pygame.display.set_caption("Dual N-Back")
    if settings['maximize']:
        window_handle = Call_Window.find_window("Dual N-Back") # makes the screen maximized
        Call_Window.maximize_window(window_handle)

    clock = pygame.time.Clock()
    state_manager = states.StateManager()

    while True:
        settings = set.get_settings()
        events = pygame.event.get()
        # Handle events
        for event in events:
            if event.type == pygame.QUIT:
                # Quit Pygame
                pygame.quit()
                return
            if event.type == pygame.VIDEORESIZE:
                SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

        ch = state_manager.update(events)
        if ch == 'quit':
            pygame.quit()
            return
        # Clear the screen
        screen.fill(set.BLACK)


        state_manager.render(screen, (SCREEN_WIDTH, SCREEN_HEIGHT))



        # Cap the frame rate
        clock.tick(settings['fps-limit'])  # Limit to 60 (default) frames per second
        if settings['show_fps']:
            screen.blit(set.jbcode24.render(str(int(clock.get_fps())), True, set.TEXT_COLOR), (10,10))


        # Update the display
        pygame.display.flip()


if __name__=='__main__':
    process()
    sys.exit()