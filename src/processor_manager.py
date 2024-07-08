from typing import Dict
from interfaces import Processor


class ProcessorManager:
    def __init__(self, processors: Dict[str, Processor]):
        self.processors = processors

    def get_target_from_event(self, url) -> (str, str):
        for processor_name, processor in self.processors.items():
            if processor.can_process(url):
                return processor_name, processor.get_id_from_url(url)
        raise ValueError(f"Unsupported URL: {url}")

    def process_event(self, url) -> bytes:
        # Determine the appropriate processor and target ID
        processor_name, target_id = self.get_target_from_event(url)
        processor = self.processors[processor_name]

        # Check if the audio already exists
        if processor.audio_exists(target_id):
            audio = processor.get_audio(target_id)
        else:
            # Process the target ID
            processor.process(target_id)
            audio = processor.get_audio(target_id)
        return audio
