# -*- coding: utf-8 -*-
from pathlib import Path
from pdfminer.high_level import extract_text

def pdf_to_txt(pdf_path: Path, txt_path: Path) -> None:
    txt_path.parent.mkdir(parents=True, exist_ok=True)
    text = extract_text(str(pdf_path)) or ""
    # Normalización básica
    text = text.replace("\x00", " ").replace("\u200b", " ").strip()
    txt_path.write_text(text, encoding="utf-8", errors="ignore")