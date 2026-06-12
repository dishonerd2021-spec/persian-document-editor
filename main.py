"""
Main entry point for Persian Document Editor
"""

import sys
from pathlib import Path
from loguru import logger

# Configure logging
log_file = Path.home() / ".persian_doc_editor" / "logs" / "app.log"
log_file.parent.mkdir(parents=True, exist_ok=True)

logger.remove()  # Remove default handler
logger.add(
    str(log_file),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="1 MB"
)
logger.add(
    sys.stderr,
    format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)

logger.info("Persian Document Editor starting...")

# Import core modules
from settings.user_settings import UserSettings
from core.language_detector import LanguageDetector
from core.structure_analyzer import StructureAnalyzer
from core.document import Document

# Try importing UI components
try:
    from PySide6.QtWidgets import QApplication
    from ui.main_window import MainWindow
    UI_AVAILABLE = True
    logger.info("UI components loaded successfully")
except ImportError:
    UI_AVAILABLE = False
    logger.warning("PySide6 not available, running in CLI mode")


def main():
    """Main entry point"""
    try:
        # Initialize settings
        settings = UserSettings()
        logger.info(f"Settings loaded from {settings.settings_dir}")
        
        if UI_AVAILABLE:
            # Run GUI application
            logger.info("Starting GUI application...")
            app = QApplication(sys.argv)
            window = MainWindow()
            window.show()
            sys.exit(app.exec())
        else:
            # Run CLI demo
            logger.info("Running in CLI demo mode...")
            demo_cli()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


def demo_cli():
    """CLI demo mode"""
    print("\n" + "="*60)
    print("Persian Document Editor - CLI Demo Mode")
    print("="*60 + "\n")
    
    # Demo: Create a document
    logger.info("Creating sample document...")
    doc = Document(title="سلام دنیا - Hello World")
    doc.metadata.author = "Demo Author"
    doc.metadata.abstract = "This is a sample document demonstrating the Persian Document Editor capabilities."
    doc.metadata.keywords = ["Persian", "Document", "Editor", "Python"]
    
    # Add paragraphs
    doc.add_paragraph("Introduction to the document.", style=doc.paragraphs[0].format.style if doc.paragraphs else None)
    doc.add_paragraph("This is a sample paragraph with both Persian and English text.")
    doc.add_paragraph("مقدمه‌ای بر سند. این یک نمونه‌ای از متن فارسی است.")
    
    # Detect languages
    logger.info("Detecting languages...")
    detector = LanguageDetector()
    for i, para in enumerate(doc.paragraphs):
        if not para.is_empty():
            lang = detector.detect_paragraph_language(para.get_text())
            print(f"Paragraph {i+1}: Language = {lang}")
    
    # Analyze structure
    logger.info("Analyzing document structure...")
    analyzer = StructureAnalyzer()
    stats = analyzer.get_document_statistics(doc.get_all_text())
    
    print(f"\nDocument Statistics:")
    print(f"  Words: {stats.get('words', 0)}")
    print(f"  Characters: {stats.get('characters', 0)}")
    print(f"  Reading Time: {stats.get('reading_time_minutes', 0)} minutes")
    
    print(f"\nDocument created with {len(doc.paragraphs)} paragraphs")
    print("\n✓ Demo completed successfully!\n")


if __name__ == "__main__":
    main()
