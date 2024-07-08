from typing import Protocol, List, Literal
from pydantic import BaseModel


# any class that implements this protocol can be used to extract text from a byte stream
# currently there is one for pdfs, but there will be others for other file types
# TODO: add implementations for images, audio, webpages
class DataExtractor(Protocol):
    def extract_text(self, file_content: bytes) -> str: ...


# represents a single item in a dialogue, containing text and speaker information
class DialogueItem(BaseModel):
    text: str
    speaker: Literal["female-1", "male-1", "female-2"]


# represents a dialogue consisting of a scratchpad and a list of dialogue items
class Dialogue(BaseModel):
    scratchpad: str
    dialogue: List[DialogueItem]


# any class that implements this protocol can be used to generate a dialogue from text
# currently there is one for arxiv papers, one for general wide audience podcasts
# TODO: add implementations for a generator that's funny, one focused on systems papers
class DialogueGenerator(Protocol):
    def generate_dialogue(self, text: str) -> Dialogue: ...


# any class that implements this protocol can be used to
# generate mp3 audio from text and speaker information
# currently there is one for openai, but there will be others for other providers
# TODO: explore options like idiap/coqui-ai-TTS
class AudioGenerator(Protocol):
    def get_mp3(self, text: str, speaker: str) -> bytes: ...


# any class that implements this protocol can be used to process a target url
# can be more generic, but right now it supports only urls based processors
# only arxiv papers processor has been implemented
# TODO: add implementations for other types of urls, like blogs, books, etc
class Processor(Protocol):

    # creates a podcast from a given target ID
    def process(self, target_id: str) -> None: ...

    # mp3 byte stream
    def get_audio(self, target_id: str) -> bytes: ...

    # text file byte stream
    def get_transcript(self, target_id: str) -> bytes: ...

    # checks if the processor can handle a given URL
    def can_process(self, url: str) -> bool: ...

    # extracts a target ID from a given URL,
    # this ID is used to determine if a cached version of the audio exists
    def get_id_from_url(self, url: str) -> str: ...

    # checks if audio already exists for a given target ID
    def audio_exists(self, target_id: str) -> bool: ...


# any class that implements this protocol can be used to provide a persistent storage
# currently there is one for s3, and local file system
class Store(Protocol):
    def upload(self, key: str, data: bytes): ...

    def download(self, key: str) -> bytes: ...

    def exists(self, key: str) -> bool: ...
