from ipywidgets import Output

from chosco.annotation.domain.annotation import Annotation
from chosco.annotation.domain.annotation_repository import AnnotationRepository
from chosco.media.retriever.domain.media_retriever import MediaRetriever
from chosco.view.interactor.domain.view_interactor import ViewInteractor


class AnnotatorBuilder:
    def __init__(
        self,
        username: str,
        retriever: MediaRetriever,
        repository: AnnotationRepository,
        view_interactor: ViewInteractor,
    ):
        self.username = username
        self.retriever = retriever
        self.repository = repository
        self.view_interactor = view_interactor
        self.current_media_id = None

        def update_item(media_id, image):
            self.current_media_id = media_id
            status = self.retriever.get_status()
            self.view_interactor.update_header_box(media_id, image, status)
            try:
                annotation = self.repository.retrieve(media_id, self.username)
                self.view_interactor.update_annotation_box(annotation.metadata)
            except ValueError:
                self.view_interactor.clear_annotation_box()

        def previous_item():
            media_id, image = self.retriever.previous_media()
            if media_id:
                update_item(media_id, image)
                return True
            return False

        def next_item():
            media_id, image = self.retriever.next_media()
            if media_id:
                update_item(media_id, image)
                return True
            return False

        def confirm_annotation(create_metadata):
            metadata = create_metadata()
            annotation = Annotation(self.current_media_id, self.username, metadata)
            self.repository.save(annotation)
            self.repository.show()
            self.retriever.confirm(self.current_media_id)

        self.view_interactor.set_callbacks(
            {
                "next_item": next_item,
                "previous_item": previous_item,
                "confirm_annotation": confirm_annotation,
            }
        )

    def build(self, output=None):
        if not output:
            output = Output()
        self.view_interactor.execute(output)
        return output
