# Persian Document Editor

**یک ویرایشگر مستند حرفه‌ای فارسی آفلاین** برای تبدیل متن خام به اسناد حرفه‌ای.

## ویژگی‌های اصلی

### 📝 ورودی‌ها
- متن مستقیم
- فایل‌های TXT، DOCX، Markdown، LaTeX
- استخراج متن از PDF

### 📄 خروجی‌ها
- **PDF** (با XeLaTeX)
- **DOCX** (با Python-docx)
- **هر دو به‌صورت همزمان**

### 🎨 امکانات طراحی
- ✅ تک‌ستونی و دو‌ستونی
- ✅ انتخاب فونت (فارسی و انگلیسی)
- ✅ راست‌چین/چپ‌چین خودکار
- ✅ قالب‌های آماده (IEEE، ACM، Springer، Elsevier)

### 🧠 ویژگی‌های هوشمند
- ✅ تشخیص خودکار زبان (فارسی/انگلیسی)
- ✅ تشخیص ساختار مقاله خودکار
- ✅ تولید چکیده با AI
- ✅ استخراج کلمات کلیدی

### 📊 مدیریت محتوا
- ✅ مدیریت شکل‌ها و جداول
- ✅ شماره‌گذاری خودکار
- ✅ فهرست مطالب خودکار
- ✅ مدیریت رفرنس‌ها (BibTeX، RIS، EndNote)

### ✍️ بررسی نگارشی
- ✅ اصلاح نیم‌فاصله‌های فارسی
- ✅ بررسی نگارش انگلیسی
- ✅ بررسی دستور

### 🖥️ رابط کاربری
- ✅ ایجاد شده با **PySide6** (Qt)
- ✅ پیش‌نمایش زنده PDF
- ✅ ویرایش‌گر متن قدرتمند
- ✅ مدیریت تنظیمات

## نصب و راه‌اندازی

### الزامات سیستم
- Python 3.12+
- XeLaTeX (برای تولید PDF)
- فونت‌های فارسی نصب‌شده

### نصب وابستگی‌ها

```bash
# کلون مخزن
git clone https://github.com/dishonerd2021-spec/persian-document-editor.git
cd persian-document-editor

# ایجاد محیط مجازی
python -m venv venv

# فعال‌سازی محیط
# در Linux/Mac:
source venv/bin/activate
# در Windows:
venv\Scripts\activate

# نصب وابستگی‌ها
pip install -r requirements.txt

# دانلود مدل‌های spaCy و NLTK
python -m spacy download en_core_web_sm
python -m nltk.downloader punkt stopwords wordnet
```

### اجرای برنامه

```bash
python main.py
```

## ساختار پروژه

```
persian-document-editor/
│
├── ui/                          # رابط کاربری (PySide6)
│   ├── __init__.py
│   ├── main_window.py           # پنجره اصلی
│   ├── editor_widget.py         # ویجت ویرایش‌گر
│   ├── preview_widget.py        # ویجت پیش‌نمایش
│   ├── settings_widget.py       # ویجت تنظیمات
│   ├── references_widget.py     # ویجت رفرنس‌ها
│   ├── figures_widget.py        # ویجت شکل‌ها
│   ├── tables_widget.py         # ویجت جداول
│   └── dialogs/                 # پنجره‌های گفتگو
│
├── core/                        # منطق اصلی
│   ├── __init__.py
│   ├── document.py              # مدل سند
│   ├── paragraph.py             # مدل پاراگراف
│   ├── language_detector.py     # تشخیص زبان
│   ├── structure_analyzer.py    # تحلیل ساختار
│   └── project_manager.py       # مدیریت پروژه
│
├── parsers/                     # تجزیه‌کننده‌های ورودی
│   ├── __init__.py
│   ├── text_parser.py           # تجزیه متن
│   ├── docx_parser.py           # تجزیه DOCX
│   ├── markdown_parser.py       # تجزیه Markdown
│   ├── latex_parser.py          # تجزیه LaTeX
│   └── pdf_parser.py            # تجزیه PDF
│
├── exporters/                   # صادرکنندگان
│   ├── __init__.py
│   ├── pdf_exporter.py          # صادرکننده PDF
│   ├── docx_exporter.py         # صادرکننده DOCX
│   └── formats/
│       ├── ieee.py              # قالب IEEE
│       ├── acm.py               # قالب ACM
│       ├── springer.py          # قالب Springer
│       └── elsevier.py          # قالب Elsevier
│
├── text_processing/            # پردازش متن
│   ├── __init__.py
│   ├── persian_processor.py     # پردازش فارسی
│   ├── english_processor.py     # پردازش انگلیسی
│   ├── spellcheck.py            # بررسی نگارش
│   └── grammar_check.py         # بررسی دستور
│
├── references/                 # مدیریت رفرنس‌ها
│   ├── __init__.py
│   ├── bibtex_manager.py        # مدیریت BibTeX
│   ├── citation_engine.py       # موتور استناد
│   └── styles/
│       ├── ieee.py
│       ├── apa.py
│       ├── vancouver.py
│       ├── harvard.py
│       └── mla.py
│
├── ai/                          # قابلیت‌های هوش مصنوعی
│   ├── __init__.py
│   ├── summarizer.py            # تولیدکننده خلاصه
│   ├── keyword_extractor.py     # استخراجکننده کلمات کلیدی
│   └── ai_config.py             # تنظیمات AI
│
├── settings/                    # مدیریت تنظیمات
│   ├── __init__.py
│   ├── config.py                # پیکربندی سیستم
│   ├── user_settings.py         # تنظیمات کاربر
│   └── defaults.json            # مقادیر پیش‌فرض
│
├── assets/                      # منابع
│   ├── fonts/
│   ├── icons/
│   └── templates/
│
├── templates/                   # قالب‌های LaTeX
│   ├── ieee.tex
│   ├── acm.tex
│   ├── springer.tex
│   └── elsevier.tex
│
├── tests/                       # تست‌ها
│   ├── __init__.py
│   ├── test_language_detector.py
│   ├── test_structure_analyzer.py
│   ├── test_exporters.py
│   └── test_text_processing.py
│
├── main.py                      # نقطه شروع برنامه
├── requirements.txt             # وابستگی‌های پروژه
├── README.md                    # این فایل
├── .gitignore                   # فایل‌های نادیده‌گرفته شده
└── .env.example                 # نمونه متغیرهای محیطی
```

## استفاده

### مرحله 1: ایجاد یا باز کردن پروژه
1. **File** → **New Project** یا **Open Project**
2. انتخاب موارد تنظیمات

### مرحله 2: وارد کردن متن
1. متن را درون ویرایش‌گر بچسبانید
2. یا **File** → **Open** برای بارگذاری فایل

### مرحله 3: تنظیم خروجی
- **Settings** پنل را باز کنید
- فونت، ستون‌بندی، راست‌چین را انتخاب کنید
- قالب را انتخاب کنید (IEEE، ACM، وغیره)

### مرحله 4: صادرات
1. **Export** → **PDF** یا **Word**
2. محل ذخیره را انتخاب کنید
3. فایل تولید می‌شود ✅

## مثال‌های کد

### تشخیص خودکار زبان
```python
from core.language_detector import LanguageDetector

detector = LanguageDetector()
text = "سلام دنیا. Hello World"
language = detector.detect(text)  # {fa: 0.5, en: 0.5}
```

### صادرات PDF
```python
from exporters.pdf_exporter import PDFExporter
from core.document import Document

doc = Document()
doc.title = "عنوان مقاله"
doc.add_paragraph("متن مقاله...")

exporter = PDFExporter()
exporter.export(doc, "output.pdf", format="ieee")
```

### استخراج کلمات کلیدی
```python
from ai.keyword_extractor import KeywordExtractor

extractor = KeywordExtractor()
keywords = extractor.extract("متن مقاله...", count=5)
print(keywords)
```

## تنظیمات

تنظیمات در فایل `settings/defaults.json` ذخیره می‌شوند:

```json
{
  "fonts": {
    "persian": "Vazirmatn",
    "english": "Times New Roman",
    "size_body": 12,
    "size_title": 16,
    "size_heading": 14
  },
  "layout": {
    "columns": 1,
    "margin_top": 25,
    "margin_bottom": 25,
    "margin_left": 20,
    "margin_right": 20
  },
  "export": {
    "format": "ieee",
    "direction": "auto"
  },
  "ai": {
    "enabled": true,
    "summarize": true,
    "extract_keywords": true
  }
}
```

## درخواست‌های ویژگی و گزارش خرابی

لطفاً از [Issues](https://github.com/dishonerd2021-spec/persian-document-editor/issues) برای گزارش خرابی‌ها و درخواست‌های ویژگی استفاده کنید.

## مشارکت

مشارکت خوش‌آمد! لطفاً:
1. مخزن را Fork کنید
2. شاخه‌ای برای ویژگی خود ایجاد کنید
3. Commit کنید و Push کنید
4. Pull Request ارسال کنید

## مجوز

این پروژه تحت مجوز MIT است - فایل [LICENSE](LICENSE) را ببینید.

## تماس و حمایت

- **مسائل و سوالات:** [Issues](https://github.com/dishonerd2021-spec/persian-document-editor/issues)
- **ایمیل:** dishonerd2021@gmail.com

---

**ساخته‌شده با ❤️ برای جامعه فارسی‌زبان**
