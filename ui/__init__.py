"""
Main UI module initialization
"""

try:
    from ui.main_window import MainWindow
    from ui.editor_widget import EditorWidget
    from ui.preview_widget import PreviewWidget
    from ui.settings_widget import SettingsWidget
    
    __all__ = [
        'MainWindow',
        'EditorWidget',
        'PreviewWidget',
        'SettingsWidget'
    ]
except ImportError:
    # UI components not available
    __all__ = []
