from abc import ABC, abstractmethod


class BaseSeeder(ABC):
    help = "An abstract class for the seeders"

    """ Clear all data and do not create any object """
    MODE_CLEAR: str = "clear"

    @abstractmethod
    def handle(self, mode: str) -> None:
        pass
