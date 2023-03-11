import pygame
import sys
import math

clock = pygame.time.Clock()

screen_width = 1920
screen_height = 1080
map_size = 10
fov = math.pi / 3
half_fov = fov / 2

tile_size = (int(screen_width) / map_size)

casted_rays = 120
step_angle = fov / casted_rays
max_depth = int(map_size * tile_size)
scale = (screen_width / 2) / casted_rays

player_x = screen_height / 2
player_y = screen_width / 2
player_angle = math.pi

pygame.init()

game_map = (
    '##########'
    '#  #   ###'
    '#  #   # #'
    '#    ### #'
    '###      #'
    '#    #####'
    '#    #   #'
    '#    #   #'
    '#        #'
    '##########'
)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hello World')


def cast_rays():
    # defining left angle of field of view
    start_angle = player_angle - half_fov

    # loop casted rays
    for ray in range(casted_rays):
        # cast single ray step by step
        for depth in range(max_depth):
            # get ray target coordinates
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y + math.cos(start_angle) * depth

            # convert target XY coordinate to map row and collum
            col2 = int(target_x / tile_size)
            row2 = int(target_y / tile_size)

            # calculate map square index
            square = row2 * map_size + col2

            if game_map[square] == '#':

                # wall shading
                color = 201 / (1 + depth * depth * 0.0001)
                color2 = 169 / (1 + depth * depth * 0.0001)
                color3 = 118 / (1 + depth * depth * 0.0001)

                # fix fish eye effect
                depth *= math.cos(player_angle - start_angle)

                # calculate wall height
                wall_height = 100000 / (depth + 0.0001)

                # fix stuck at the wall
                if wall_height > screen_height:
                    wall_height = screen_height

                # draw 3D projection
                pygame.draw.rect(screen, (color, color2, color3), (
                    screen_height + ray * scale,
                    (screen_height / 2) - wall_height / 2,
                    scale, wall_height))

                break

        # incrementing angle by a single step
        start_angle += step_angle


forward = True

run = True
while run:

    # if the game ends or the escape key is pressed run will set to FALSE and stop the while loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    col = int(player_x / tile_size)
    row = int(player_y / tile_size)
    square1 = row * map_size + col

    # stops the player from going through the wall
    if game_map[square1] == '#':
        if forward:
            player_x -= -math.sin(player_angle) * 5
            player_y -= math.cos(player_angle) * 5
        else:
            player_x += -math.sin(player_angle) * 5
            player_y += math.cos(player_angle) * 5

    # draws the ray casting to the screen, making the floor and ceiling two different colours
    pygame.draw.rect(screen, (100, 100, 100), (1080, screen_height / 2, screen_height, screen_height))
    pygame.draw.rect(screen, (174, 214, 241), (1080, -screen_height / 2, screen_height, screen_height))

    # runs the cast rays function while the game is running
    cast_rays()

    # gets the player input for moving around, uses WASD
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_angle -= 0.1
    if keys[pygame.K_d]:
        player_angle += 0.1
    if keys[pygame.K_w]:
        forward = True  # sets forward true so that the player can be stopped from going through walls
        player_x += -math.sin(player_angle) * 6
        player_y += math.cos(player_angle) * 6
    if keys[pygame.K_s]:
        player_x -= -math.sin(player_angle) * 6
        player_y -= math.cos(player_angle) * 6

    # set FPS
    clock.tick(60)

    # display FPS
    fps = str(int(clock.get_fps()))

    pygame.display.flip()

pygame.quit()
