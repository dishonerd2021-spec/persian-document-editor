"""
Default configuration and settings for Persian Document Editor
"""

DEFAULT_SETTINGS = {
    "app": {
        "name": "Persian Document Editor",
        "version": "1.0.0",
        "author": "dishonerd2021-spec",
        "license": "MIT"
    },
    "fonts": {
        "persian": {
            "default": "Vazirmatn",
            "options": ["Vazirmatn", "IRNazanin", "B Nazanin", "XB Zar"]
        },
        "english": {
            "default": "Times New Roman",
            "options": ["Times New Roman", "Arial", "Cambria", "Latin Modern"]
        },
        "sizes": {
            "body": 12,
            "title": 18,
            "heading": 14,
            "subheading": 12,
            "caption": 10,
            "footer": 10
        }
    },
    "layout": {
        "columns": 1,  # 1 or 2
        "direction": "auto",  # auto, rtl, ltr
        "margins": {
            "top": 25,      # mm
            "bottom": 25,
            "left": 20,
            "right": 20
        },
        "line_spacing": 1.5,
        "paragraph_spacing": 6  # pt
    },
    "export": {
        "format": "ieee",  # ieee, acm, springer, elsevier, thesis, custom
        "default_format": "both",  # pdf, docx, both
        "include_toc": True,
        "include_lof": True,  # List of Figures
        "include_lot": True,  # List of Tables
        "include_references": True
    },
    "language": {
        "detection": "auto",
        "default": "en",
        "supported": ["fa", "en"]
    },
    "ai": {
        "enabled": True,
        "summarize": True,
        "extract_keywords": True,
        "max_summary_words": 250,
        "keywords_count": 5,
        "model": "multilingual"
    },
    "references": {
        "style": "ieee",  # ieee, apa, vancouver, harvard, mla
        "format": "bibtex",  # bibtex, ris, endnote
        "auto_generate": True,
        "supported_styles": ["ieee", "apa", "vancouver", "harvard", "mla"]
    },
    "spellcheck": {
        "enabled": True,
        "persian_enabled": True,
        "english_enabled": True,
        "language": "en"
    },
    "templates": {
        "default": "ieee",
        "available": ["ieee", "acm", "springer", "elsevier", "thesis", "custom"]
    },
    "ui": {
        "theme": "light",  # light, dark
        "language": "en",  # en, fa
        "show_line_numbers": True,
        "show_whitespace": False,
        "word_wrap": True,
        "font_size_editor": 11
    },
    "projects": {
        "auto_save": True,
        "auto_save_interval": 300,  # seconds
        "recent_projects_count": 10
    }
}

# Supported export formats
EXPORT_FORMATS = {
    "pdf": {
        "name": "PDF Document",
        "extension": "pdf",
        "engine": "xelatex"
    },
    "docx": {
        "name": "Word Document",
        "extension": "docx",
        "engine": "python-docx"
    }
}

# Supported document formats
DOCUMENT_FORMATS = {
    "txt": "Plain Text",
    "docx": "Word Document",
    "md": "Markdown",
    "tex": "LaTeX",
    "pdf": "PDF"
}

# Document structure patterns
DOCUMENT_STRUCTURE = {
    "title": "title",
    "abstract": "abstract",
    "keywords": "keywords",
    "introduction": "introduction",
    "related_work": "related_work",
    "methods": "methods",
    "results": "results",
    "discussion": "discussion",
    "conclusion": "conclusion",
    "references": "references",
    "appendix": "appendix"
}

# LaTeX preamble for different formats
LATEX_PREAMBLES = {
    "ieee": r"""
\documentclass[conference]{IEEEtran}
\usepackage[utf8]{inputenc}
\usepackage{xepersian}
\settextfont{Vazirmatn}
\setlatintextfont{Times New Roman}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{cite}
\usepackage{url}
\usepackage{hyperref}
""",
    "acm": r"""
\documentclass[sigconf]{acmart}
\usepackage[utf8]{inputenc}
\usepackage{xepersian}
\settextfont{Vazirmatn}
\setlatintextfont{Times New Roman}
\usepackage{amsmath}
\usepackage{graphicx}
""",
    "springer": r"""
\documentclass{llncs}
\usepackage[utf8]{inputenc}
\usepackage{xepersian}
\settextfont{Vazirmatn}
\setlatintextfont{Times New Roman}
\usepackage{amsmath}
\usepackage{graphicx}
""",
    "elsevier": r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage{xepersian}
\settextfont{Vazirmatn}
\setlatintextfont{Times New Roman}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{amssymb}
"""
}
