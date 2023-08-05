from IPython.core.display import Image
from google.cloud import storage
from google.cloud.exceptions import NotFound
from google.cloud.storage import Blob

from chosco.media.repository.domain.media_repository import MediaRepository


class GoogleCloudMediaRepository(MediaRepository):
    def __init__(self, bucket_name: str):
        self.storage_client = storage.Client()
        self.bucket_name = bucket_name

    def retrieve(self, media_id: str, width: int = None) -> Image:
        try:
            blob = self._get_blob(media_id, self.bucket_name)
            data = blob.download_as_string(client=self.storage_client)
        except NotFound:
            raise Exception(f"Media {media_id} not found in Google Cloud repository")

        return Image(data=data, format="jpg", unconfined=True, width=width)

    def _get_blob(self, media_id: str, bucket_name: str) -> Blob:
        bucket = self.storage_client.get_bucket(bucket_name)
        blob = bucket.blob(media_id)
        return blob
