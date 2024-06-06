click_sound = pygame.mixer.Sound("Music/click.wav")
game_music = pygame.mixer.Sound("Music/game.mp3")
end_music = pygame.mixer.Sound("Music/end.mp3")


main_menu_music = pygame.mixer.Sound("Music/menu.mp3")

Menu_image = pygame.image.load('Background/Main_menu.jpg')

def main_menu():
    global current_phase

    main_menu_music.play(-1) 

    # Colors
    white = (255, 255, 255)
 

    # Fonts
    font = pygame.font.Font('Choi.ttf', 60)

    # Buttons
    start_button = pygame.Rect(340, 250, 300, 80)
    exit_button = pygame.Rect(340, 350, 300, 80)

    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    

    # Main Menu Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                if start_button.collidepoint(event.pos):
                    current_phase = 'spawning'  
                    running = False  
                if exit_button.collidepoint(event.pos):
                    pygame.quit()  # Quit Pygame
                    exit()

        # Fill the screen
        win.fill(white)
        win.blit(Menu_image, (0, 0))


        # Draw buttons
        #pygame.draw.rect(win, black, start_button)
        #pygame.draw.rect(win, black, exit_button)

        # Draw text
        draw_text("Start", font, (0, 255, 0), win, start_button.centerx - 50, start_button.centery - 15)
        draw_text("Exit", font, (0, 255, 0), win, exit_button.centerx - 40, exit_button.centery - 15)
        
        pygame.display.update()
        
    main_menu_music.stop()



