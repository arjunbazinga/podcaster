from interfaces import Store
from loguru import logger


class PodcastStorage:
    def __init__(self, store: Store):
        self.store = store

    def _generate_audio_key(self, entry_id: str) -> str:
        return f"audio/{entry_id}.mp3"

    def _generate_transcript_key(self, entry_id: str) -> str:
        return f"transcripts/{entry_id}.txt"

    def create_audio(self, entry_id: str, audio: bytes):
        audio_key = self._generate_audio_key(entry_id)
        logger.info(f"Creating audio with key: {audio_key}")
        self.store.upload(audio_key, audio)
        logger.info(f"Created audio with key: {audio_key}")
        return audio_key

    def get_audio(self, entry_id: str) -> bytes:
        audio_key = self._generate_audio_key(entry_id)
        logger.info(f"Getting audio with key: {audio_key}")
        audio = self.store.download(audio_key)
        logger.info(f"Got audio with key: {audio_key}")
        return audio

    def exists_audio(self, entry_id: str) -> bool:
        audio_key = self._generate_audio_key(entry_id)
        logger.info(f"Checking if audio exists with key: {audio_key}")
        exists = self.store.exists(audio_key)
        logger.info(
            f"Audio {'exists' if exists else 'does not exist'} with key: {audio_key}"
        )
        return exists

    def create_transcript(self, entry_id: str, transcript: str):
        transcript_key = self._generate_transcript_key(entry_id)
        logger.info(f"Creating transcript with key: {transcript_key}")
        self.store.upload(transcript_key, transcript.encode("utf-8"))
        logger.info(f"Created transcript with key: {transcript_key}")
        return transcript_key

    def get_transcript(self, entry_id: str) -> bytes:
        transcript_key = self._generate_transcript_key(entry_id)
        logger.info(f"Getting transcript with key: {transcript_key}")
        transcript = self.store.download(transcript_key)
        logger.info(f"Got transcript with key: {transcript_key}")
        return transcript
