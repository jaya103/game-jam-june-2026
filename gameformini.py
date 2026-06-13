import pygame



def minigame(screen, dt):
    global score, current_screen
    global current_screen, running, start_ticks
    screen.fill("black")
    font = pygame.font.Font(None, 100)
    text = font.render("MINIGAME", True, "white")

    font = pygame.font.Font(None, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        start_ticks = pygame.time.get_ticks()
        current_screen = main(screen, dt)
    if keys[pygame.K_ESCAPE]:
        running = False
    
    return True
