import pygame
import random

# Импорт модуля отрисовки
import drawing

pygame.init()

dis_width = 600
dis_height = 400

dis = pygame.display.set_mode((dis_width, dis_height + 50))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 5


# Вычисление новых случайных координат для яблока на поле
def random_food(controlled_snake_list, competitor_snake_list, width, height):
    foodx_coord = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody_coord = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    while ([foodx_coord, foody_coord] in controlled_snake_list) or ([foodx_coord, foody_coord] in competitor_snake_list):
        foodx_coord = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
        foody_coord = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
    return foodx_coord, foody_coord


# Проверка окончания игры (проигрышной ситуации врезания в границы поля)
def losing_situation(x, y):
    if x >= dis_width or x < 0 or y >= dis_height or y < 0:
        return True
    else:
        return False


# Проверка столкновения (проигрышной ситуации) змейки с самой собой или с противником (и наоборот)
def collision_check(controlled_snake_list, competitor_snake_list):
    # Проверка столкновения управляемой змейки с собой и со змейкой-соперником
    for coord in controlled_snake_list[:-1]:
        if coord == controlled_snake_list[-1]:  # == controlled_snake_head
            return True
    if controlled_snake_list[-1] in competitor_snake_list:
        return True

    # Проверка столкновения змейки-соперника с собой и с управляемой змейкой
    for coord in competitor_snake_list[:-1]:
        if coord == competitor_snake_list[-1]:
            return True
    if competitor_snake_list[-1] in controlled_snake_list:
        return True

    return False


# Проверка нахождения змейкой еды (увеличение счета)
def find_food(food_x, food_y, length_of_controlled_snake, length_of_competitor_snake, controlled_snake_list, competitor_snake_list):
    x_controlled, y_controlled = controlled_snake_list[-1]
    x_competitor, y_competitor = competitor_snake_list[-1]
    if (x_controlled == food_x and y_controlled == food_y) or (x_competitor == food_x and y_competitor == food_y):
        if x_controlled == food_x and y_controlled == food_y:
            length_of_controlled_snake += 1
        elif x_competitor == food_x and y_competitor == food_y:
            length_of_competitor_snake += 1

        return True, length_of_controlled_snake, length_of_competitor_snake

    return False, length_of_controlled_snake, length_of_competitor_snake


# Перемещение змеи на шаг (всех блоков тела) в координатах и увеличение длины, если змея заработала очко
def move_snake_blocks(snake_list, x_coord, y_coord, length_of_snake):
    snake_head = [x_coord, y_coord]
    snake_list.append(snake_head)
    if len(snake_list) > length_of_snake:
        del snake_list[0]

    return snake_list


# Расчет следующего шага змеи-соперника
def independent_snake_movement(food_x, food_y, competitor_snake_list, controlled_snake_list):
    x1 = (competitor_snake_list[-1])[0]
    y1 = (competitor_snake_list[-1])[1]

    # Рассчет расстояния до еды в разных направлениях
    right = food_x - x1
    left = -right
    bottom = food_y - y1
    top = -bottom

    points = [right, left, bottom, top]
    points.sort(reverse=True)   # выбор кратчайшего расстояния

    x1_change = 0
    y1_change = 0

    flag = 0
    for current_point in points:
        if current_point == right:
            if ((not losing_situation(x1 + snake_block, y1)) and ([x1 + snake_block, y1] not in competitor_snake_list)
                    and ([x1 + snake_block, y1] not in controlled_snake_list)):
                x1_change = snake_block
                y1_change = 0
                flag = -1
                break
        elif current_point == left:
            if ((not losing_situation(x1 - snake_block, y1)) and ([x1 - snake_block, y1] not in competitor_snake_list)
                    and ([x1 - snake_block, y1] not in controlled_snake_list)):
                x1_change = -snake_block
                y1_change = 0
                flag = -1
                break
        elif current_point == bottom:
            if ((not losing_situation(x1, y1 + snake_block)) and ([x1, y1 + snake_block] not in competitor_snake_list)
                    and ([x1, y1 + snake_block] not in controlled_snake_list)):
                y1_change = snake_block
                x1_change = 0
                flag = -1
                break
        elif current_point == top:
            if ((not losing_situation(x1, y1 - snake_block)) and ([x1, y1 - snake_block] not in competitor_snake_list)
                    and ([x1, y1 - snake_block] not in controlled_snake_list)):
                y1_change = -snake_block
                x1_change = 0
                flag = -1
                break

    if flag == 0:
        print("No possible moves")
        if ((not losing_situation(x1 + snake_block, y1)) and ([x1 + snake_block, y1] not in competitor_snake_list)
                and ([x1 + snake_block, y1] not in controlled_snake_list)):
            x1_change = snake_block
            y1_change = 0
        elif ((not losing_situation(x1 - snake_block, y1)) and ([x1 - snake_block, y1] not in competitor_snake_list)
              and ([x1 - snake_block, y1] not in controlled_snake_list)):
            x1_change = -snake_block
            y1_change = 0
        elif ((not losing_situation(x1, y1 + snake_block)) and ([x1, y1 + snake_block] not in competitor_snake_list)
              and ([x1, y1 + snake_block] not in controlled_snake_list)):
            y1_change = snake_block
            x1_change = 0
        elif ((not losing_situation(x1, y1 - snake_block)) and ([x1, y1 - snake_block] not in competitor_snake_list)
              and ([x1, y1 - snake_block] not in controlled_snake_list)):
            y1_change = -snake_block
            x1_change = 0
        else:
            print("No possible moves")

    return x1_change, y1_change


# Основной цикл игры
def game_loop(game_over=False):
    game_close = False

    # controlled - управляемая змейка (№1)
    x_controlled = dis_width / 3 * 2
    y_controlled = dis_height / 2

    x_controlled_change = 0
    y_controlled_change = 0

    controlled_snake_list = [[x_controlled, y_controlled]]

    length_of_controlled_snake = 1

    # competitor - самостоятельная (игровая) змейка-соперник (№2)
    x_competitor = dis_width / 3
    y_competitor = dis_height / 2

    x_competitor_change = 0
    y_competitor_change = 0

    competitor_snake_list = [[x_competitor, y_competitor]]

    length_of_competitor_snake = 1

    food_x, food_y = random_food(controlled_snake_list, competitor_snake_list, dis_width, dis_height)

    while not game_over:

        while game_close:
            drawing.draw_background(dis)    # отрисовка фона

            drawing.message("Game over!", dis_width / 8, 100, dis)   # отрисовка сообщения об окончании игры

            finish_message = ""
            if (length_of_controlled_snake - 1) > (length_of_competitor_snake - 1):
                finish_message = "You win!"
            elif (length_of_controlled_snake - 1) < (length_of_competitor_snake - 1):
                finish_message = "You lost!"
            else:
                finish_message = "Same score!"

            drawing.message(finish_message, dis_width / 8, 140, dis)    # отрисовка сообщения
            drawing.message("Press C to play again or Q to quit", dis_width / 8, 220, dis)  # отрисовка сообщения

            # Отрисовка счета
            drawing.show_scores(length_of_controlled_snake - 1, length_of_competitor_snake - 1, dis, dis_height, dis_width)
            pygame.display.update()

            # Отслеживание реакции на действия пользователя
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        if game_over:
            continue

        # Рассчет следующего шага змеи-соперника
        x_competitor_change, y_competitor_change = independent_snake_movement(food_x, food_y, competitor_snake_list, controlled_snake_list)

        # Отслеживание реакции на действия пользователя
        for event in pygame.event.get():
            # Для закрытия приложения
            if event.type == pygame.QUIT:
                game_over = True
                game_close = False
            # Реакция на нажатие стрелок
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_controlled_change = -snake_block
                    y_controlled_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_controlled_change = snake_block
                    y_controlled_change = 0
                elif event.key == pygame.K_UP:
                    y_controlled_change = -snake_block
                    x_controlled_change = 0
                elif event.key == pygame.K_DOWN:
                    y_controlled_change = snake_block
                    x_controlled_change = 0

        # Изменение координат управляемой змейки
        x_controlled += x_controlled_change
        y_controlled += y_controlled_change

        # Изменение координат самостоятельной (игровой) змейки-соперника
        x_competitor += x_competitor_change
        y_competitor += y_competitor_change

        # Перемещение змеи на шаг (всех блоков тела) в координатах и увеличение длины, если змея заработала очко
        controlled_snake_list = move_snake_blocks(controlled_snake_list, x_controlled, y_controlled,
                                                  length_of_controlled_snake)
        competitor_snake_list = move_snake_blocks(competitor_snake_list, x_competitor, y_competitor,
                                                  length_of_competitor_snake)

        # Проверка окончания игры (если game_close == True, игра заканчивается)
        game_close = losing_situation(x_controlled, y_controlled) or losing_situation(x_competitor, y_competitor)

        # Проверка столкновения управляемой змейки с собой и со змейкой-соперником
        # и столкновения змейки-соперника с собой и с управляемой змейкой
        game_close = game_close or collision_check(controlled_snake_list, competitor_snake_list)

        if game_close:
            continue

        # Отрисовка основных объектов на поле игры
        drawing.draw_field(food_x, food_y, snake_block, dis)

        # Отрисовка змей на экране игры
        drawing.draw_snakes(snake_block, controlled_snake_list, competitor_snake_list, dis)

        # Отрисовка счета (для обеих змеек) на экране игры
        drawing.show_scores(length_of_controlled_snake - 1, length_of_competitor_snake - 1, dis, dis_height, dis_width)

        pygame.display.update()

        # Проверка нахождения змейкой еды (увеличение счета)
        flag_find, length_of_controlled_snake, length_of_competitor_snake = find_food(food_x, food_y, length_of_controlled_snake, length_of_competitor_snake, controlled_snake_list, competitor_snake_list)
        # Если нашла еду, надо сгенерировать новое положение еды на поле
        if flag_find:
            food_x, food_y = random_food(controlled_snake_list, competitor_snake_list, dis_width, dis_height)

        clock.tick(snake_speed)

    pygame.quit()
    quit()


if __name__ == '__main__':
    game_loop()
