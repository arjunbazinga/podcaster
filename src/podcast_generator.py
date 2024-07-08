from interfaces import DataExtractor, DialogueGenerator, AudioGenerator, Dialogue
from typing import Tuple
from loguru import logger
import concurrent.futures as cf


class PodcastGenerator:
    def __init__(
        self,
        data_extractor: DataExtractor,
        dialogue_generator: DialogueGenerator,
        audio_generator: AudioGenerator,
    ):
        self.data_extractor = data_extractor
        self.dialogue_generator = dialogue_generator
        self.audio_generator = audio_generator
        self.podcast_with_transcript = PodcastWithTranscript(audio_generator)

    def generate_content(self, content: bytes) -> Tuple[bytes, str]:
        logger.info("Extracting text from content")

        text = self.data_extractor.extract_text(content)

        logger.info("Extracted text from content")
        logger.info("Generating dialogue from text")

        dialogue = self.dialogue_generator.generate_dialogue(text)

        logger.info("Generated dialogue from text")
        logger.info("Synthesizing audio from dialogue")

        audio, transcript = self.podcast_with_transcript.synthesize_audio(dialogue)

        logger.info("Synthesized audio from dialogue")
        return audio, transcript


class PodcastWithTranscript:
    def __init__(self, audio_generator: AudioGenerator):
        self.audio_generator = audio_generator

    def synthesize_audio(self, dialogue: Dialogue) -> Tuple[bytes, str]:
        audio = b""
        transcript = ""
        characters = 0

        with cf.ThreadPoolExecutor() as executor:
            futures = []
            for line in dialogue.dialogue:
                transcript_line = f"{line.speaker}: {line.text}"
                future = executor.submit(
                    self.audio_generator.get_mp3, line.text, line.speaker
                )
                futures.append((future, transcript_line))
                characters += len(line.text)

            for future, transcript_line in futures:
                audio_chunk = future.result()
                audio += audio_chunk
                transcript += transcript_line + "\n\n"

        logger.info(f"Generated {characters} characters of audio")
        return audio, transcript
