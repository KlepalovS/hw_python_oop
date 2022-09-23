class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        '''Возвращает информационное сообщение о тренировке.'''

        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_spead: float = self.get_distance() / self.duration
        return mean_spead

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        training_info = InfoMessage(self.__class__.__name__,
                                    self.duration,
                                    self.get_distance(),
                                    self.get_mean_speed(),
                                    self.get_spent_calories())
        return training_info


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1: int = 18
        coeff_calorie_2: int = 20
        time_in_min: float = self.duration * 60
        spend_calories: float = ((coeff_calorie_1
                                 * self.get_mean_speed()
                                 - coeff_calorie_2)
                                 * self.weight
                                 / self.M_IN_KM
                                 * time_in_min)
        return spend_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1: float = 0.035
        coeff_calorie_2: float = 0.029
        time_in_min: float = self.duration * 60
        spent_calories: float = ((coeff_calorie_1
                                 * self.weight
                                 + (self.get_mean_speed() ** 2 // self.height)
                                 * coeff_calorie_2 * self.weight)
                                 * time_in_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        mean_spead: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_spead

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1: float = 1.1
        coeff_calorie_2: int = 2
        spent_calories: float = ((self.get_mean_speed() + coeff_calorie_1)
                                 * coeff_calorie_2 * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    dict = {}
    if workout_type == 'SWM':
        dict[workout_type] = Swimming(data[0],
                                      data[1],
                                      data[2],
                                      data[3],
                                      data[4])
    elif workout_type == 'RUN':
        dict[workout_type] = Running(data[0],
                                     data[1],
                                     data[2])
    elif workout_type == 'WLK':
        dict[workout_type] = SportsWalking(data[0],
                                           data[1],
                                           data[2],
                                           data[3])
    return dict[workout_type]


def main(training: Training) -> None:
    """Главная функция."""

    info: str = training.show_training_info().get_message()
    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
