import pygame

pygame.init()

game_screen = pygame.display.set_mode((960, 540))
pygame.display.set_caption("Math Display")

background_1 = pygame.image.load('assets/oak_woods_v1.0/oak_woods_v1.0/background/background_layer_1.png').convert_alpha()
background_2 = pygame.image.load('assets/oak_woods_v1.0/oak_woods_v1.0/background/background_layer_2.png').convert_alpha()
background_3 = pygame.image.load('assets/oak_woods_v1.0/oak_woods_v1.0/background/background_layer_3.png').convert_alpha()

background_1 = pygame.transform.rotozoom(background_1, 0, 3)
background_2 = pygame.transform.rotozoom(background_2, 0, 3)
background_3 = pygame.transform.rotozoom(background_3, 0, 3)

blue_stand_surf = pygame.image.load('assets/oak_woods_v1.0/oak_woods_v1.0/character/char_blue_standby_1.png').convert_alpha()
blue_stand_rect = blue_stand_surf.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game_screen.blit(background_1, (0, 0))
    game_screen.blit(background_2, (0, 0))
    game_screen.blit(background_3,  (0,0))

    pygame.display.update()