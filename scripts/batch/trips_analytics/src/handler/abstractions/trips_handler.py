from abc import ABC, abstractmethod

class ITripsHandler(ABC):
    @abstractmethod
    def pipeline(self):
        raise NotImplementedError()