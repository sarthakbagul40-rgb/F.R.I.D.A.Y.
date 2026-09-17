"""
F.R.I.D.A.Y. OS 10.0: PROJECT A.E.G.I.S. 6th Media Adapter - Books & Neural Narration Core
Features:
1. Multi-format ingestion: PDF (via pypdf), EPUB (via native zip/xml parse), and TXT/Markdown.
2. Intelligent chapter and semantic passage segmentation.
3. Real-time background neural audio narration streaming via OmniVoice.
4. Persistent bookmarking and reading progression synced with Viking Vault.
5. Interactive playback controls: play, pause, resume, seek, next/prev chapter.
"""

import os
import re
import json
import time
import zipfile
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime

class BooksAdapter:
    """The 6th Aegis Media Adapter: Literary Ingestion and Continuous Neural Narration Engine."""

    def __init__(self, vault_dir: Optional[str] = None):
        if vault_dir is None:
            vault_dir = os.path.join(os.path.dirname(__file__), "memory_vault")
        self.vault_dir = vault_dir
        os.makedirs(self.vault_dir, exist_ok=True)
        self.progress_file = os.path.join(self.vault_dir, "reading_progress.json")
        
        self.current_book: Dict[str, Any] = {}
        self.chapters: List[Dict[str, Any]] = []
        self.current_chapter_idx: int = 0
        self.current_paragraph_idx: int = 0
        
        self.is_reading: bool = False
        self.is_paused: bool = False
        self._stop_narration_event = threading.Event()
        self._narration_thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        self._load_saved_progress()

    def _load_saved_progress(self):
        """Loads last read book and position from Viking Vault."""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.current_chapter_idx = saved.get("chapter_idx", 0)
                    self.current_paragraph_idx = saved.get("paragraph_idx", 0)
            except Exception:
                pass

    def _save_progress(self):
        """Persists current reading bookmark to Viking Vault."""
        if not self.current_book:
            return
        data = {
            "book_title": self.current_book.get("title", "Unknown"),
            "book_path": self.current_book.get("path", ""),
            "chapter_idx": self.current_chapter_idx,
            "chapter_title": self.chapters[self.current_chapter_idx].get("title", "") if self.chapters else "",
            "paragraph_idx": self.current_paragraph_idx,
            "timestamp": datetime.now().isoformat()
        }
        try:
            with open(self.progress_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    # =========================================================================
    # 1. MULTI-FORMAT DOCUMENT INGESTION & SEGMENTATION
    # =========================================================================
    def load_document(self, file_path: str) -> Dict[str, Any]:
        """
        Ingests a book or document (PDF, EPUB, TXT, MD) and parses into structured chapters.
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        ext = os.path.splitext(file_path)[1].lower()
        title = os.path.splitext(os.path.basename(file_path))[0]
        
        self.stop_narration()
        self.chapters = []
        self.current_chapter_idx = 0
        self.current_paragraph_idx = 0

        try:
            if ext == ".pdf":
                raw_chapters = self._parse_pdf(file_path)
            elif ext == ".epub":
                raw_chapters = self._parse_epub(file_path)
            elif ext in [".txt", ".md", ".markdown"]:
                raw_chapters = self._parse_text(file_path)
            else:
                return {"success": False, "error": f"Unsupported document format: {ext}"}

            if not raw_chapters:
                return {"success": False, "error": "No readable text content extracted."}

            self.chapters = raw_chapters
            self.current_book = {
                "title": title,
                "path": file_path,
                "format": ext[1:].upper(),
                "total_chapters": len(self.chapters),
                "total_paragraphs": sum(len(c.get("paragraphs", [])) for c in self.chapters)
            }
            self._save_progress()

            return {
                "success": True,
                "book": self.current_book,
                "message": f"Successfully parsed '{title}' into {len(self.chapters)} chapter(s)."
            }
        except Exception as e:
            return {"success": False, "error": f"Failed to ingest document: {e}"}

    def _parse_pdf(self, path: str) -> List[Dict[str, Any]]:
        """Extracts text from PDF and segments by chapter markers or page chunks."""
        import pypdf
        reader = pypdf.PdfReader(path)
        total_pages = len(reader.pages)
        full_text_pages = []
        
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                full_text_pages.append((idx + 1, text.strip()))

        # Detect chapter headings (e.g. Chapter 1, Act I, Section)
        chapters = []
        current_ch_title = "Chapter 1: Opening"
        current_ch_paras = []

        for p_num, p_text in full_text_pages:
            paragraphs = [p.strip() for p in re.split(r'\n\s*\n', p_text) if p.strip()]
            for para in paragraphs:
                if re.match(r'^(?:chapter|part|act|section)\s+([0-9ivxlcdm]+|\w+)', para, re.IGNORECASE):
                    if current_ch_paras:
                        chapters.append({
                            "chapter_num": len(chapters) + 1,
                            "title": current_ch_title,
                            "paragraphs": current_ch_paras
                        })
                        current_ch_paras = []
                    current_ch_title = para[:80].strip()
                else:
                    current_ch_paras.append(para)

        if current_ch_paras:
            chapters.append({
                "chapter_num": len(chapters) + 1,
                "title": current_ch_title,
                "paragraphs": current_ch_paras
            })

        # Fallback: segment by 5-page chunks if no explicit chapters found
        if not chapters or (len(chapters) == 1 and len(chapters[0]["paragraphs"]) > 100):
            chapters = []
            chunk_size = 5
            for i in range(0, total_pages, chunk_size):
                chunk_pages = full_text_pages[i:i + chunk_size]
                chunk_paras = []
                for _, text in chunk_pages:
                    chunk_paras.extend([p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()])
                if chunk_paras:
                    chapters.append({
                        "chapter_num": len(chapters) + 1,
                        "title": f"Section {len(chapters) + 1} (Pages {i + 1}-{min(i + chunk_size, total_pages)})",
                        "paragraphs": chunk_paras
                    })

        return chapters

    def _parse_epub(self, path: str) -> List[Dict[str, Any]]:
        """Parses EPUB archive using native zipfile and xml parsing (zero dependencies)."""
        chapters = []
        with zipfile.ZipFile(path, 'r') as zf:
            html_files = [f for f in zf.namelist() if f.endswith(('.html', '.xhtml', '.htm'))]
            for idx, hfile in enumerate(html_files):
                content = zf.read(hfile).decode('utf-8', errors='ignore')
                # Strip HTML tags
                text = re.sub(r'<script[\s\S]*?</script>', '', content)
                text = re.sub(r'<style[\s\S]*?</style>', '', text)
                text = re.sub(r'<[^>]+>', ' ', text)
                text = re.sub(r'&[a-zA-Z0-9#]+;', ' ', text)
                paras = [p.strip() for p in re.split(r'\n\s*\n', text) if len(p.strip()) > 30]
                if paras:
                    ch_title = paras[0][:60].strip() if len(paras[0]) < 80 else f"Chapter {len(chapters) + 1}"
                    chapters.append({
                        "chapter_num": len(chapters) + 1,
                        "title": ch_title,
                        "paragraphs": paras
                    })
        return chapters

    def _parse_text(self, path: str) -> List[Dict[str, Any]]:
        """Segments plain text or Markdown files by markdown headers or chapter keywords."""
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        chapters = []
        lines = content.splitlines()
        current_title = "Chapter 1: Prelude"
        current_paras = []
        buffer = []

        for line in lines:
            stripped = line.strip()
            # Markdown header (# Chapter) or plain "Chapter 1"
            if re.match(r'^(?:#{1,3}\s+|chapter\s+[0-9ivxlcdm]+)', stripped, re.IGNORECASE):
                if buffer:
                    current_paras.append(" ".join(buffer))
                    buffer = []
                if current_paras:
                    chapters.append({
                        "chapter_num": len(chapters) + 1,
                        "title": current_title,
                        "paragraphs": current_paras
                    })
                    current_paras = []
                current_title = re.sub(r'^#+\s*', '', stripped)
            elif not stripped:
                if buffer:
                    current_paras.append(" ".join(buffer))
                    buffer = []
            else:
                buffer.append(stripped)

        if buffer:
            current_paras.append(" ".join(buffer))
        if current_paras:
            chapters.append({
                "chapter_num": len(chapters) + 1,
                "title": current_title,
                "paragraphs": current_paras
            })

        return chapters

    # =========================================================================
    # 2. NEURAL AUDIO NARRATION STREAMING
    # =========================================================================
    def start_narration(self, chapter_num: Optional[int] = None, start_paragraph: Optional[int] = None, speak_fn=None) -> Dict[str, Any]:
        """
        Starts or resumes neural audio narration in an asynchronous background thread.
        """
        if not self.chapters:
            return {"success": False, "error": "No book loaded. Load a document first via load_document()."}

        if chapter_num is not None:
            self.current_chapter_idx = max(0, min(len(self.chapters) - 1, chapter_num - 1))
            self.current_paragraph_idx = 0
        if start_paragraph is not None:
            self.current_paragraph_idx = max(0, start_paragraph)

        self.stop_narration()
        self._stop_narration_event.clear()
        self.is_reading = True
        self.is_paused = False

        # Duck or pause background music before starting narration
        try:
            from core.media_engine import media_engine
            if media_engine.is_playing:
                media_engine.duck_volume(15)
        except Exception:
            pass

        def _narration_worker():
            from core.omnivoice_service import neural_voice_engine
            
            while not self._stop_narration_event.is_set() and self.current_chapter_idx < len(self.chapters):
                chapter = self.chapters[self.current_chapter_idx]
                paras = chapter.get("paragraphs", [])
                
                # Announce chapter header if beginning a new chapter
                if self.current_paragraph_idx == 0:
                    neural_voice_engine.speak(f"{chapter.get('title', f'Chapter {self.current_chapter_idx + 1}')}.", block=True)

                while self.current_paragraph_idx < len(paras):
                    if self._stop_narration_event.is_set():
                        return

                    while self.is_paused:
                        time.sleep(0.2)
                        if self._stop_narration_event.is_set():
                            return

                    para_text = paras[self.current_paragraph_idx]
                    self._save_progress()

                    # Stream paragraph with completion wait for continuous book pacing
                    neural_voice_engine.speak(para_text, block=True)
                    self.current_paragraph_idx += 1
                    time.sleep(0.15) # Natural breathing pause between paragraphs

                # Chapter finished -> advance
                self.current_chapter_idx += 1
                self.current_paragraph_idx = 0
                self._save_progress()

            self.is_reading = False

        self._narration_thread = threading.Thread(target=_narration_worker, daemon=True)
        self._narration_thread.start()

        ch_name = self.chapters[self.current_chapter_idx].get("title", f"Chapter {self.current_chapter_idx + 1}")
        return {
            "success": True,
            "status": "narrating",
            "book": self.current_book.get("title"),
            "chapter": ch_name,
            "paragraph": self.current_paragraph_idx + 1
        }

    def pause_or_resume_narration(self) -> str:
        """Toggles narration pause / resume."""
        if not self.is_reading:
            return "No book narration currently active, Boss."
        self.is_paused = not self.is_paused
        if self.is_paused:
            try:
                from core.omnivoice_service import neural_voice_engine
                neural_voice_engine.stop_immediate()
            except Exception:
                pass
            return "Book narration paused, Boss."
        else:
            return "Resuming narration, Boss."

    def stop_narration(self):
        """Halts active book narration immediately."""
        self._stop_narration_event.set()
        self.is_reading = False
        self.is_paused = False
        try:
            from core.omnivoice_service import neural_voice_engine
            neural_voice_engine.stop_immediate()
        except Exception:
            pass
        self._save_progress()

    def next_chapter(self) -> str:
        """Advances to the next chapter."""
        if not self.chapters:
            return "No book loaded, Boss."
        if self.current_chapter_idx + 1 < len(self.chapters):
            self.current_chapter_idx += 1
            self.current_paragraph_idx = 0
            if self.is_reading:
                self.start_narration()
            return f"Skipping to {self.chapters[self.current_chapter_idx].get('title', f'Chapter {self.current_chapter_idx + 1}')}, Boss."
        return "You have reached the final chapter, Boss."

    def prev_chapter(self) -> str:
        """Rewinds to the previous chapter."""
        if not self.chapters:
            return "No book loaded, Boss."
        if self.current_chapter_idx > 0:
            self.current_chapter_idx -= 1
            self.current_paragraph_idx = 0
            if self.is_reading:
                self.start_narration()
            return f"Rewinding to {self.chapters[self.current_chapter_idx].get('title', f'Chapter {self.current_chapter_idx + 1}')}, Boss."
        return "Already at the beginning of the book, Boss."

    def get_status(self) -> Dict[str, Any]:
        """Returns active reading telemetry and bookmark progress."""
        if not self.current_book:
            return {"active": False, "message": "No book loaded."}
        
        current_ch = self.chapters[self.current_chapter_idx] if self.chapters else {}
        total_paras = sum(len(c.get("paragraphs", [])) for c in self.chapters) or 1
        read_paras = sum(len(self.chapters[i].get("paragraphs", [])) for i in range(self.current_chapter_idx)) + self.current_paragraph_idx
        progress_pct = round((read_paras / total_paras) * 100, 1)

        return {
            "active": True,
            "is_reading": self.is_reading,
            "is_paused": self.is_paused,
            "title": self.current_book.get("title"),
            "format": self.current_book.get("format"),
            "chapter_idx": self.current_chapter_idx + 1,
            "chapter_title": current_ch.get("title", ""),
            "paragraph_idx": self.current_paragraph_idx + 1,
            "total_chapters": len(self.chapters),
            "progress_percent": progress_pct
        }


# Global singleton instance
books_adapter = BooksAdapter()
