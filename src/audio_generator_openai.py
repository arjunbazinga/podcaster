import io
from loguru import logger
from openai import OpenAI, OpenAIError
from interfaces import AudioGenerator
import time
import threading
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)


class OpenAIAudioGenerator(AudioGenerator):
    def __init__(self, openai_api_key, max_requests_per_minute=50):
        self.openai_api_key = openai_api_key
        self.lock = threading.Lock()
        self.request_count = 0
        self.start_time = time.time()
        self.client = OpenAI(api_key=self.openai_api_key)
        self.max_requests_per_minute = max_requests_per_minute

    def _reset_request_count(self):
        self.request_count = 1
        self.start_time = time.time()

    def _throttle_requests(self):
        with self.lock:
            self.request_count += 1
            elapsed_time = time.time() - self.start_time

            if self.request_count > self.max_requests_per_minute:
                if elapsed_time < 60:
                    time.sleep(60 - elapsed_time)
                self._reset_request_count()
            elif elapsed_time >= 60:
                self._reset_request_count()

    def _get_voice(self, speaker: str) -> str:
        voices = {
            "female-1": "alloy",
            "male-1": "onyx",
            "female-2": "shimmer",
        }
        return voices.get(speaker, "alloy")

    @retry(
        retry=retry_if_exception_type(OpenAIError),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
    )
    def get_mp3(self, text: str, speaker: str) -> bytes:
        self._throttle_requests()

        voice = self._get_voice(speaker)

        try:
            with self.client.audio.speech.with_streaming_response.create(
                model="tts-1",
                voice=voice,
                input=text,
            ) as response:
                with io.BytesIO() as file:
                    for chunk in response.iter_bytes():
                        file.write(chunk)
                    return file.getvalue()
        except OpenAIError as e:
            logger.error(f"Error generating audio: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
