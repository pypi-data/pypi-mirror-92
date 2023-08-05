class AnnotationTaskStatus:
    def __init__(
        self,
        index: int,
        number_of_annotations: int,
        total_annotations: int,
        current_task_id: str = None,
    ):
        self.index = index
        self.number_of_annotations = number_of_annotations
        self.total_annotations = total_annotations
        self.current_task_id = current_task_id

    def get_progress(self):
        return f"{self.number_of_annotations+1} of {self.total_annotations}"
