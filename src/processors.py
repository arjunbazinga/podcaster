from processor_manager import ProcessorManager
from processor_arxiv import ArxivProcessor
from store_fs import FSStore
from podcast_generator import PodcastGenerator
from data_extractor_pdf import PDFDataExtractor
from dialogue_generator_research_paper import ResearchPaperGenerator
from audio_generator_openai import OpenAIAudioGenerator
import os


def get_default_processor_manager(
    store_base_path: str, gemini_api_key: str, openai_api_key: str
) -> ProcessorManager:
    PROCESSORS = {
        "arxiv": ArxivProcessor(
            store=FSStore(base_path=os.path.join(store_base_path, "arxiv")),
            podcast_generator=PodcastGenerator(
                data_extractor=PDFDataExtractor(),
                dialogue_generator=ResearchPaperGenerator(gemini_api_key),
                audio_generator=OpenAIAudioGenerator(openai_api_key),
            ),
        )
    }
    return ProcessorManager(PROCESSORS)
