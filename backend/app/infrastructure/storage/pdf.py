"""PDF parsing utilities."""
from io import BytesIO

from fastapi.concurrency import run_in_threadpool
from pdfminer.high_level import extract_text_to_fp


async def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """Extract plain text from PDF bytes asynchronously.

    Uses pdfminer (blocking) in a threadpool to avoid blocking the event loop.
    """
    if not file_bytes:
        return ""

    def _extract() -> str:
        output = BytesIO()
        extract_text_to_fp(BytesIO(file_bytes), output, laparams=None)
        return output.getvalue().decode("utf-8", errors="ignore")

    return await run_in_threadpool(_extract)
