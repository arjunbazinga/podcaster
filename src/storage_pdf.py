from interfaces import Store
from loguru import logger


class PDFStorage:
    def __init__(self, store: Store):
        self.store = store

    def _generate_pdf_key(self, entry_id: str) -> str:
        return f"pdfs/{entry_id}.pdf"

    def create_pdf(self, entry_id: str, pdf_content: bytes):
        pdf_key = self._generate_pdf_key(entry_id)
        logger.info(f"Creating PDF with key: {pdf_key}")
        self.store.upload(pdf_key, pdf_content)
        logger.info(f"Created PDF with key: {pdf_key}")
        return pdf_key

    def get_pdf(self, entry_id: str) -> bytes:
        pdf_key = self._generate_pdf_key(entry_id)
        logger.info(f"Getting PDF with key: {pdf_key}")
        pdf_content = self.store.download(pdf_key)
        logger.info(f"Got PDF with key: {pdf_key}")
        return pdf_content

    def exists_pdf(self, entry_id: str) -> bool:
        pdf_key = self._generate_pdf_key(entry_id)
        logger.info(f"Checking if PDF exists with key: {pdf_key}")
        exists = self.store.exists(pdf_key)
        logger.info(
            f"PDF {'exists' if exists else 'does not exist'} with key: {pdf_key}"
        )
        return exists
