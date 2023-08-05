from typing import Tuple

from chosco.annotation.domain.annotation_task_provider import AnnotationTaskProvider
from chosco.annotation.domain.annotation_task_status import AnnotationTaskStatus
from chosco.media.repository.domain.media_repository import MediaRepository

from IPython.core.display import Image


class MediaRetriever:
    def __init__(
        self,
        annotation_task_provider: AnnotationTaskProvider,
        repository: MediaRepository,
        image_width: int = 1200,
    ):
        self.annotation_task_provider = annotation_task_provider
        self.repository = repository
        self.image_width = image_width
        self.media_id = None

    def previous_media(self) -> Tuple[str, Image]:
        self.media_id = self.annotation_task_provider.previous()
        image = None
        if self.media_id:
            image = self.repository.retrieve(self.media_id)
        return self.media_id, image

    def next_media(self) -> Tuple[str, Image]:
        self.media_id = self.annotation_task_provider.next()
        image = None
        if self.media_id:
            image = self.repository.retrieve(self.media_id)

        return self.media_id, image

    def confirm(self, media_id):
        self.annotation_task_provider.confirm_current_task(media_id)

    def get_status(self) -> AnnotationTaskStatus:
        return self.annotation_task_provider.get_status()
