from abc import ABC, abstractmethod


class BaseReport(ABC):
    """Базовый класс для всех отчётов"""

    @abstractmethod
    def generate(self, stats):
        """Генерация отчёта на основе статистики"""
        pass
