from IPython.core.display import Image

from chosco.media.repository.domain.media_repository import MediaRepository


class HardcodedWebMediaRepository(MediaRepository):
    def retrieve(self, media_id: str, width: int = None) -> Image:
        try:
            return Image(media_id, unconfined=True, width=width)
        except:  # noqa
            raise IndexError(
                f"media_id {media_id} cannot be loaded on HardcodedWebMediaRepository"
            )
