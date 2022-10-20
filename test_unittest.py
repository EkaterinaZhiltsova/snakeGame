import unittest
from mock import patch
import mock

import game


class TestGame(unittest.TestCase):
    # Блочные тесты на функцию random_food
    # Позитивный тест
    # Переделать тест, так как изменилась функция
    def test_random_food_positive(self):
        food_x, food_y = game.random_food([[720.0, 250.0], [730.0, 250.0]],
                                          [[560.0, 160.0], [560.0, 150.0], [570.0, 150.0], [570.0, 140.0]], 600, 400)
        # True - функция выдает подходящие случайные значения для размещения еды внутри игрового поля
        self.assertTrue(0 <= food_x < 600 and 0 <= food_y < 400)

    # Негативный тест
    def test_random_food_negative(self):
        width = 1000
        height = 300
        food_x, food_y = game.random_food([[720.0, 250.0], [730.0, 250.0]],
                                          [[560.0, 160.0], [560.0, 150.0], [570.0, 150.0], [570.0, 140.0]], width, height)
        # True - функция выдает подходящие случайные значения для размещения еды внутри игрового поля c заявленными width и height (неправильными размерами поля)
        self.assertTrue(0 <= food_x < 1000 and 0 <= food_y < 300)

    # Блочные тесты на функцию losing_situation
    # Позитивный тест
    def test_not_losing_situation_positive(self):
        self.assertFalse(game.losing_situation(200, 300))   # False - ситуация не проигрышная

    # Позитивный тест
    def test_not_losing_situation_positive_2(self):
        self.assertFalse(game.losing_situation(590, 390))  # False - ситуация не проигрышная (краевой случай)

    # Негативный тест
    def test_losing_situation_negative(self):
        self.assertTrue(game.losing_situation(600, 400))   # True - ситуация проигрышная (краевой случай)

    # Негативный тест
    def test_losing_situation_negative_2(self):
        self.assertTrue(game.losing_situation(-10, -10))   # True - ситуация проигрышная (краевой случай)

    # Блочные тесты на функцию collision_check
    # Позитивный тест (ситуация не проигрышная)
    # Змейки не врезаются
    def test_not_collision_check_positive(self):
        self.assertFalse(game.collision_check([[230.0, 350.0]], [[290.0, 370.0], [290.0, 380.0]]))  # False - ситуация не проигрышная

    # Негативный тест (ситуация проигрышная)
    # Управляемая змейка врезалась в противника
    def test_collision_check_negative_1(self):
        self.assertTrue(game.collision_check([[280.0, 350.0]], [[280.0, 360.0], [280.0, 350.0], [280.0, 340.0]]))    # True - ситуация проигрышная

    # Негативный тест (ситуация проигрышная)
    # Управляемая змейка врезалась в себя
    def test_collision_check_negative_2(self):
        self.assertTrue(game.collision_check([[150.0, 200.0], [150.0, 210.0], [150.0, 220.0], [160.0, 220.0], [160.0, 210.0], [150.0, 210.0]],
                                             [[210.0, 170.0], [220.0, 170.0], [220.0, 160.0], [230.0, 160.0], [240.0, 160.0], [250.0, 160.0], [260.0, 160.0], [270.0, 160.0], [280.0, 160.0], [290.0, 160.0]]))

    # Негативный тест (ситуация проигрышная)
    # Змейка противник врезалась в себя
    def test_collision_check_negative_3(self):
        self.assertTrue(game.collision_check([[210.0, 170.0], [220.0, 170.0], [220.0, 160.0], [230.0, 160.0], [240.0, 160.0], [250.0, 160.0], [260.0, 160.0], [270.0, 160.0], [280.0, 160.0], [290.0, 160.0]],
                                             [[150.0, 200.0], [150.0, 210.0], [150.0, 220.0], [160.0, 220.0], [160.0, 210.0], [150.0, 210.0]]))

    # Негативный тест (ситуация проигрышная)
    # Змейка противник врезалась в управляемую
    def test_collision_check_negative_4(self):
        self.assertTrue(game.collision_check([[280.0, 360.0], [280.0, 350.0], [280.0, 340.0]], [[280.0, 350.0]]))

    # Блочные тесты на функцию find_food
    # Позитивный тест (змейка нашла еду)
    def test_find_food_positive(self):
        self.assertEqual(game.find_food(400.0, 160.0, 1, 1, [[400.0, 160.0]], [[350.0, 200.0]]), (True, 2, 1))

    # Негативный тест (змейка не нашла еду)
    def test_find_food_negative(self):
        self.assertEqual(game.find_food(150.0, 210.0, 1, 3, [[580.0, 200.0]], [[310.0, 380.0], [310.0, 370.0], [300.0, 370.0]]), (False, 1, 3))

    # Блочные тесты на функцию move_snake_blocks
    # Позитивный тест (с увеличением длины при добавлением очка)
    def test_move_snake_blocks_positive(self):
        self.assertEqual(game.move_snake_blocks([[120.0, 90.0], [120.0, 80.0]], 130.0, 80.0, 3),
                         [[120.0, 90.0], [120.0, 80.0], [130.0, 80.0]])

    # Позитивный тест (без увеличения длины без добавления очка)
    def test_move_snake_blocks_positive_2(self):
        self.assertEqual(game.move_snake_blocks([[100.0, 140.0], [100.0, 130.0]], 100.0, 120.0, 2),
                         [[100.0, 130.0], [100.0, 120.0]])

    # Негативный тест (выход за пределы поля без добавления очка)
    def test_move_snake_blocks_negative(self):
        self.assertEqual(game.move_snake_blocks([[580.0, 110.0], [590.0, 110.0]], 600.0, 110.0, 2),
                         [[590.0, 110.0], [600.0, 110.0]])

    # Негативный тест (змейка заполняет всё поле и выходит за него)
    def test_move_snake_blocks_negative_2(self):
        full_screen_snake_list = []
        full_screen_snake_list_new = []
        for i in range(0, 400, 10):
            for j in range(0, 600, 10):
                y = j
                if i % 20 != 0:
                    y = 590 - j
                full_screen_snake_list.append([float(i), float(y)])
                full_screen_snake_list_new.append([float(i), float(y)])

        full_screen_snake_list_new.append([400.0, 0.0])

        self.assertEqual(game.move_snake_blocks(full_screen_snake_list, 400.0, 0.0, len(full_screen_snake_list) + 1), full_screen_snake_list_new)

    # Блочные тесты на функцию independent_snake_movement
    # С mock-объектом на вызываемую функцию losing_situation
    # Позитивный тест
    def test_unit_independent_snake_movement_positive(self):
        with patch('game.losing_situation') as losing_situation_mock:
            losing_situation_mock.return_value = False
            self.assertEqual(
                game.independent_snake_movement(180.0, 310.0, [[150.0, 270.0], [150.0, 280.0]], [[600.0, 200.0]]),
                (10, 0))

    # Негативный тест (нет возможных перемещений)
    def test_unit_independent_snake_movement_negative(self):
        with patch('game.losing_situation') as losing_situation_mock:
            losing_situation_mock.return_value = False
            self.assertEqual(
                game.independent_snake_movement(20.0, 90.0,
                                                [[430.0, 220.0], [440.0, 220.0], [440.0, 230.0], [450.0, 230.0], [450.0, 240.0], [460.0, 240.0], [460.0, 250.0], [470.0, 250.0], [470.0, 260.0], [480.0, 260.0], [480.0, 270.0], [490.0, 270.0], [490.0, 280.0], [500.0, 280.0], [500.0, 290.0], [490.0, 290.0], [480.0, 290.0], [470.0, 290.0], [460.0, 290.0], [450.0, 290.0], [440.0, 290.0], [430.0, 290.0], [420.0, 290.0], [410.0, 290.0], [400.0, 290.0], [390.0, 290.0], [390.0, 280.0], [390.0, 270.0], [390.0, 260.0], [390.0, 250.0], [400.0, 250.0], [400.0, 240.0], [410.0, 240.0], [410.0, 230.0], [420.0, 230.0], [420.0, 240.0], [420.0, 250.0], [410.0, 250.0], [410.0, 260.0], [400.0, 260.0], [400.0, 270.0], [400.0, 280.0], [410.0, 280.0], [410.0, 270.0], [420.0, 270.0], [420.0, 260.0], [430.0, 260.0], [430.0, 250.0], [430.0, 240.0], [430.0, 230.0], [430.0, 230.0]],
                                                [[400.0, 200.0]]),
                (0, 0))

    # Блочные/Интеграционные тесты на функцию game_loop (?)

    # Интеграционные тесты на функцию independent_snake_movement -> вызываемая функция losing_situation
    # Позитивный тест
    def test_integration_independent_snake_movement_positive(self):
        self.assertEqual(
            game.independent_snake_movement(230.0, 50.0, [[260.0, 90.0], [260.0, 80.0], [250.0, 80.0]], [[400.0, 200.0]]),
            (0, -10))

    # Негативный тест (нет возможных перемещений)
    def test_integration_independent_snake_movement_negative(self):
        self.assertEqual(
            game.independent_snake_movement(310.0, 230.0,
                                            [[430.0, 80.0], [440.0, 80.0], [440.0, 70.0], [430.0, 70.0], [420.0, 70.0], [420.0, 80.0], [410.0, 80.0], [410.0, 90.0], [400.0, 90.0], [400.0, 100.0], [390.0, 100.0], [380.0, 100.0], [370.0, 100.0], [360.0, 100.0], [350.0, 100.0], [340.0, 100.0], [330.0, 100.0], [320.0, 100.0], [310.0, 100.0], [310.0, 90.0], [320.0, 90.0], [330.0, 90.0], [340.0, 90.0], [350.0, 90.0], [360.0, 90.0], [370.0, 90.0], [380.0, 90.0], [390.0, 90.0], [390.0, 80.0], [380.0, 80.0], [370.0, 80.0], [360.0, 80.0], [350.0, 80.0], [340.0, 80.0], [330.0, 80.0], [320.0, 80.0], [310.0, 80.0], [310.0, 70.0], [320.0, 70.0], [330.0, 70.0], [340.0, 70.0], [350.0, 70.0], [360.0, 70.0], [370.0, 70.0], [380.0, 70.0], [390.0, 70.0], [400.0, 70.0], [400.0, 80.0], [400.0, 80.0]],
                                            [[400.0, 200.0]]),
            (0, 0))


if __name__ == '__main__':
    unittest.main()
