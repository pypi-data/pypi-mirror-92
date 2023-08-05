from abc import ABC, abstractmethod


class AnnotationTaskProvider(ABC):
    @abstractmethod
    def get_number_of_annotations(self):
        raise NotImplementedError

    @abstractmethod
    def get_number_pending_annotations(self):
        raise NotImplementedError

    @abstractmethod
    def get_total_annotations(self):
        raise NotImplementedError

    @abstractmethod
    def get_status(self):
        raise NotImplementedError

    @abstractmethod
    def next(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def previous(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def confirm_current_task(self, task_id: str):
        raise NotImplementedError
