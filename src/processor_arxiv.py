import requests
import re
from loguru import logger
from interfaces import Processor, Store

from storage_pdf import PDFStorage
from storage_podcast import PodcastStorage
from podcast_generator import PodcastGenerator
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


@retry(
    retry=retry_if_exception_type(requests.exceptions.ConnectionError),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
)
def download_arxiv_file(arxiv_id: str) -> bytes:
    arxiv_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    response = requests.get(arxiv_url)
    response.raise_for_status()
    return response.content


def get_arxiv_id_from_url(url: str) -> str:
    # https://arxiv.org/abs/2306.00248v1 -> 2306.00248v1
    # https://arxiv.org/pdf/2306.00248v1 -> 2306.00248v1
    # https://arxiv.org/html/1706.03762v7/#S4 -> 1706.03762v7
    # we need to be carefull it's not always just the last part,
    # some times a header is present
    # Define a regular expression pattern to match arXiv IDs
    pattern = r"(?:abs|pdf|html)/(\d{4}\.\d{4,5}(?:v\d+)?)"
    # Search for the pattern in the URL
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        raise ValueError("Unable to extract arXiv ID from the given URL")


class ArxivProcessor(Processor):
    def __init__(self, store: Store, podcast_generator: PodcastGenerator):
        self.podcast_storage = PodcastStorage(store)
        self.pdf_storage = PDFStorage(store)
        self.podcast_generator = podcast_generator

    def _process_arxiv_paper(self, arxiv_id: str):
        logger.info(f"Downloading arXiv file for ID: {arxiv_id}")
        file_content = download_arxiv_file(arxiv_id)
        logger.info(f"Downloaded arXiv file for ID: {arxiv_id}")

        logger.info(f"Storing pdf for arXiv ID: {arxiv_id}")
        self.pdf_storage.create_pdf(arxiv_id, file_content)
        logger.info(f"Stored pdf for arXiv ID: {arxiv_id}")

        logger.info(f"Generating podcast content for arXiv ID: {arxiv_id}")
        audio, transcript = self.podcast_generator.generate_content(file_content)
        logger.info(f"Generated podcast content for arXiv ID: {arxiv_id}")

        logger.info(f"Storing audio for arXiv ID: {arxiv_id}")
        self.podcast_storage.create_audio(arxiv_id, audio)
        logger.info(f"Stored audio for arXiv ID: {arxiv_id}")
        logger.info(f"Storing transcript for arXiv ID: {arxiv_id}")
        self.podcast_storage.create_transcript(arxiv_id, transcript)
        logger.info(f"Stored transcript for arXiv ID: {arxiv_id}")

    def process(self, target_id: str):
        self._process_arxiv_paper(target_id)

    def get_audio(self, target_id: str) -> bytes:
        return self.podcast_storage.get_audio(target_id)

    def get_transcript(self, target_id: str) -> bytes:
        return self.podcast_storage.get_transcript(target_id)

    def audio_exists(self, target_id: str) -> bool:
        return self.podcast_storage.exists_audio(target_id)

    def can_process(self, url: str) -> bool:
        return url.startswith("https://arxiv.org")

    def get_id_from_url(self, url: str) -> str:
        return get_arxiv_id_from_url(url)
