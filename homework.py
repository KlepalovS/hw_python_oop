from dataclasses import dataclass, asdict
from typing import ClassVar, Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    GET_MESSAGE_TEXT: ClassVar[str] = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Возвращает информационное сообщение о тренировке."""
        return self.GET_MESSAGE_TEXT.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    MINS_PER_HOUR: int = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Непереназначен метод get_spent_calories() '
            f'в классе {type(self).__name__}'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories(),
                           )


class Running(Training):
    """Тренировка: бег."""

    SPENT_RUNNING_CALORIES_MULTIPLIER_1: float = 18
    SPENT_RUNNING_CALORIES_MULTIPLIER_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.SPENT_RUNNING_CALORIES_MULTIPLIER_1
             * self.get_mean_speed()
             - self.SPENT_RUNNING_CALORIES_MULTIPLIER_2)
            * self.weight
            / self.M_IN_KM
            * self.duration * self.MINS_PER_HOUR
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    SPENT_SPORTWALCKING_CALORIES_MULTIPLIER_1: float = 0.035
    SPENT_SPORTWALCKING_CALORIES_MULTIPLIER_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.SPENT_SPORTWALCKING_CALORIES_MULTIPLIER_1
             * self.weight
             + (self.get_mean_speed() ** 2 // self.height)
             * self.SPENT_SPORTWALCKING_CALORIES_MULTIPLIER_2 * self.weight)
            * self.duration * self.MINS_PER_HOUR
        )


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    SPENT_SWIMMING_CALORIES_MULTIPLIER_1: float = 1.1
    SPENT_SWIMMING_CALORIES_MULTIPLIER_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration
                )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.SPENT_SWIMMING_CALORIES_MULTIPLIER_1)
                * self.SPENT_SWIMMING_CALORIES_MULTIPLIER_2
                * self.weight
                )


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    key_to_training: Dict[str, Type(Training)] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    if workout_type in key_to_training:
        return key_to_training[workout_type](*data)
    else:
        raise KeyError(f'Неопознанный тип тренировки {workout_type}.')


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
