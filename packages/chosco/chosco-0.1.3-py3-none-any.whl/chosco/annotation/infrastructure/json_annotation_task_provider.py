import json
from datetime import datetime
from typing import List

from chosco.annotation.domain.annotation_task_provider import AnnotationTaskProvider
from chosco.annotation.domain.annotation_task_status import AnnotationTaskStatus


class JsonAnnotationTaskProvider(AnnotationTaskProvider):
    @staticmethod
    def from_filename(filename: str):
        with open(filename, "r") as infile:
            kdict = json.load(infile)
            return JsonAnnotationTaskProvider(
                kdict.get("done"),
                kdict.get("pending"),
                kdict.get("session_id"),
                kdict.get("current_task_index"),
                filename,
            )

    @staticmethod
    def create(tasks: List[str], session_id: str):
        done = []
        pending = tasks
        return JsonAnnotationTaskProvider(done, pending, session_id)

    def __init__(
        self,
        done: List[str],
        pending: List[str],
        session_id: str,
        current_task_index: int = None,
        filename: str = None,
    ):
        self.done = done
        self.pending = pending
        self.total_tasks = self.done + self.pending
        self.current_task_index = current_task_index

        self.session_id = session_id
        self.updated_at = None
        if self.pending is None or len(self.pending) < 1:
            raise AttributeError(
                f"Pending documents must have at least a task. {self.to_dict()}"
            )
        self.current_task_id = None
        self.filename = filename

    def to_dict(self):
        return {
            "updated_at": self.updated_at,
            "number_of_annotations": self.get_number_of_annotations(),
            "number_pending_annotations": self.get_number_pending_annotations(),
            "done": self.done,
            "pending": self.pending,
            "session_id": self.session_id,
            "current_task_index": self.current_task_index,
        }

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=4)

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def save(self, filename):
        self.filename = filename
        with open(filename, "w") as outfile:
            json.dump(self.to_dict(), outfile, indent=4)

    def save_snapshot(self):
        if self.filename:
            self.save(self.filename)

    def get_current_index(self):
        return self.current_task_index

    def get_number_of_annotations(self):
        return len(self.done) if self.done else 0

    def get_number_pending_annotations(self):
        return len(self.pending) if self.pending else 0

    def get_total_annotations(self):
        return len(self.total_tasks)

    def get_status(self):
        return AnnotationTaskStatus(
            index=self.get_current_index(),
            number_of_annotations=self.get_number_of_annotations(),
            total_annotations=self.get_total_annotations(),
            current_task_id=self.current_task_id,
        )

    def next(self) -> str:
        self.current_task_index = (
            -1 if self.current_task_index is None else self.current_task_index
        )
        try:
            if self.current_task_index >= len(self.total_tasks) - 1:
                self.current_task_id = None
            else:
                self.current_task_index += 1
                self.current_task_id = self.total_tasks[self.current_task_index]
        except IndexError:
            self.current_task_id = None
        return self.current_task_id

    def previous(self) -> str:
        if self.current_task_index is None or self.current_task_index < 1:
            self.current_task_id = None
        else:
            self.current_task_index -= 1
            self.current_task_id = self.total_tasks[self.current_task_index]

        return self.current_task_id

    def confirm_current_task(self, task_id: str):
        if len(self.pending) > 0:
            try:
                self.pending.remove(task_id)
                self.done.append(task_id)
                self.updated_at = datetime.utcnow().strftime("%B %d %Y - %H:%M:%S")
                self.save_snapshot()
            except ValueError:
                pass
