import pygame

light_green_color = (144, 238, 144)
green_color = (0, 128, 0)
dark_green_color = (0, 100, 0)
black_color = (0, 0, 0)
violet_color = (75, 0, 130)
red_color = (213, 50, 80)
brown_color = (139, 69, 19)
dark_red_color = (139, 0, 0)


# Отрисовка счета (для обеих змеек) на экране игры
def show_scores(score1, score2, dis, dis_height, dis_width):
    score_font = pygame.font.SysFont("verdana", 36)
    pygame.draw.rect(dis, green_color, [0, dis_height, dis_width, 50])  # фон для счета
    # управляемая змейка
    show_score(score1, violet_color, "Your score: ", 350, score_font, dis)
    # змейка-соперник
    show_score(score2, black_color, "Score: ", 10, score_font, dis)


# Отрисовка счета (для одной змейки) на экране игры
def show_score(score, color, text, x_coord, score_font, dis):
    value = score_font.render(text + str(score), True, color)  # счёт
    dis.blit(value, [x_coord, 402])


# Вывод сообщения на экран игры
def message(msg, x_coord, y_coord, dis):
    font_style = pygame.font.SysFont("verdana", 22)
    mesg = font_style.render(msg, True, dark_red_color)
    dis.blit(mesg, [x_coord, y_coord])


# Отрисовка змей на экране игры
def draw_snakes(snake_block, controlled_snake_list, competitor_snake_list, dis):
    # управляемая змейка
    draw_snake(snake_block, controlled_snake_list, violet_color, dis)
    # змейка-соперник
    draw_snake(snake_block, competitor_snake_list, black_color, dis)


# Отрисовка змеи (каждого блока) на экране игры
def draw_snake(snake_block, snake_list, color, dis):
    for block in snake_list:
        pygame.draw.rect(dis, color, [block[0], block[1], snake_block, snake_block])    # змея


# Отрисовка фона
def draw_background(dis):
    dis.fill(light_green_color)  # зелёный фон


# Отрисовка основных объектов
def draw_field(foodx, foody, snake_block, dis):
    draw_background(dis)    # отрисовка фона
    pygame.draw.rect(dis, red_color, [foodx, foody, snake_block, snake_block])  # красное яблоко
    pygame.draw.rect(dis, brown_color, [foodx + 4, foody - 3, 2, 5])  # веточка
    pygame.draw.ellipse(dis, dark_green_color, (foodx + 4, foody - 4.5, 6, 3))  # листик
