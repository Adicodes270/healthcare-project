"""
utils/pdf_reader.py
Robust PDF text extraction with multiple strategies and OpenAI vision fallback for scanned PDFs.
"""
import io
from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file) -> dict:
    """
    Extract text from a Streamlit UploadedFile (PDF) using multiple strategies.

    Returns a dict:
        {
            "text": str | None,        # extracted text (None if none found)
            "pages": int,              # total pages
            "strategy": str,           # which method succeeded
            "is_scanned": bool,        # True if no selectable text found
            "raw_bytes": bytes,        # original PDF bytes (for vision fallback)
        }
    """
    try:
        pdf_bytes = uploaded_file.read()
    except Exception as e:
        raise RuntimeError(f"Could not read uploaded file: {e}")

    result = {
        "text": None,
        "pages": 0,
        "strategy": "none",
        "is_scanned": False,
        "raw_bytes": pdf_bytes,
    }

    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        result["pages"] = len(reader.pages)
    except Exception as e:
        raise RuntimeError(f"Could not parse PDF structure: {e}")

    # ── Strategy 1: Standard extraction with layout mode ──────────────────────
    text_parts = []
    for page in reader.pages:
        try:
            # layout mode preserves table/column structure better
            page_text = page.extract_text(extraction_mode="layout")
            if not page_text or not page_text.strip():
                # fallback to plain mode for this page
                page_text = page.extract_text()
        except Exception:
            try:
                page_text = page.extract_text()
            except Exception:
                page_text = ""
        if page_text and page_text.strip():
            text_parts.append(page_text.strip())

    if text_parts:
        combined = "\n\n---PAGE BREAK---\n\n".join(text_parts)
        # Quality check: must have enough real words (not just noise chars)
        words = [w for w in combined.split() if len(w) > 1]
        if len(words) >= 20:
            result["text"] = combined
            result["strategy"] = "layout+plain extraction"
            return result

    # ── Strategy 2: Visit all annotations / embedded text streams ─────────────
    annotation_parts = []
    for page in reader.pages:
        try:
            if "/Annots" in page:
                for annot in page["/Annots"]:
                    obj = annot.get_object()
                    if "/Contents" in obj:
                        annotation_parts.append(str(obj["/Contents"]))
        except Exception:
            pass

    if annotation_parts:
        result["text"] = "\n".join(annotation_parts)
        result["strategy"] = "annotations"
        return result

    # ── No text found — likely a scanned/image PDF ────────────────────────────
    result["is_scanned"] = True
    result["strategy"] = "none (scanned/image-based)"
    return result


def pdf_bytes_to_images(pdf_bytes: bytes) -> list:
    """
    Convert PDF pages to PIL Images for OpenAI vision analysis.
    Returns list of PIL Image objects (one per page, up to 5 pages).
    Requires: pip install pypdfium2
    """
    try:
        import pypdfium2 as pdfium
        from PIL import Image

        pdf = pdfium.PdfDocument(pdf_bytes)
        images = []
        for i in range(min(len(pdf), 5)):  # limit to 5 pages
            page = pdf[i]
            bitmap = page.render(scale=2.0)  # 2x for better OCR quality
            pil_image = bitmap.to_pil()
            images.append(pil_image)
        return images
    except ImportError:
        return []
    except Exception:
        return []
