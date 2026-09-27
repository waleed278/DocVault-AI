from pypdf import PdfReader

from app.core.exceptions import (
    DocumentExtractionError,
    NoExtractableTextError
)

MAX_EXTRACTED_CHARACTERS = 60_000

def extract_pdf_text_sync(
        file_object
)->str:
    try:
        file_object.seek(0)

        reader = PdfReader(
            file_object
        )

        text_parts = list[str] = []

        total_characters = 0

        for page in reader.pages:
            page_text = (
                page.extract_text() 
                or ""
            )

            if not page_text.strip():
                continue
            remaining = (
                MAX_EXTRACTED_CHARACTERS - total_characters
            )

            if remaining <=0:
                break
            selcted_text = page_text[:remaining]

            text_parts.append(selcted_text)
            total_characters += len(selcted_text)

        extracted_text = "\n\n".join(text_parts).strip()

    except Exception as exc:
        raise DocumentExtractionError(
            "Could not parse PDF"
        ) from exc
    if not extracted_text:
        raise NoExtractableTextError()

    return extracted_text