from tempfile import NamedTemporaryFile
from loguru import logger
from pypdf import PdfReader
from interfaces import DataExtractor


class PDFDataExtractor(DataExtractor):
    def extract_text(self, file_content: bytes) -> str:
        logger.info("Extracting text from PDF content")
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        with open(temp_file_path, "rb") as f:
            reader = PdfReader(f)
            text = "\n\n".join([page.extract_text() for page in reader.pages])
        logger.info("Extracted text from PDF content")
        return text
