"""Style configuration for LogoCraft app."""

class StyleConfig:
    """Centralized style configuration"""
    
    colors = {
        'primary': '#108375',
        'primary_hover': '#9FCDC7',
        'disabled': '#636369',
        'text': '#231347',
        'background': '#f5f5f5',
        'border': '#636369',
        'white': 'white'
    }

    @staticmethod
    def get_stylesheet() -> str:
        """Get the application's stylesheet."""
        return f"""
            QMainWindow {{
                background-color: {StyleConfig.colors['background']};
            }}
            QGroupBox {{
                font-weight: bold;
                border: 1px solid {StyleConfig.colors['border']};
                border-radius: 4px;
                margin-top: 6px;
                padding-top: 8px;
                color: {StyleConfig.colors['text']};
                background-color: {StyleConfig.colors['white']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 6px;
                padding: 0px 3px;
            }}
            QPushButton {{
                background-color: {StyleConfig.colors['primary']};
                color: {StyleConfig.colors['white']};
                border: none;
                border-radius: 3px;
                padding: 5px 10px;
                min-width: 70px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {StyleConfig.colors['primary_hover']};
            }}
            QPushButton:disabled {{
                background-color: {StyleConfig.colors['disabled']};
            }}
            QLineEdit {{
                padding: 4px;
                border: 1px solid {StyleConfig.colors['border']};
                border-radius: 3px;
                background-color: {StyleConfig.colors['white']};
                min-height: 20px;
            }}
            QProgressBar {{
                border: 1px solid {StyleConfig.colors['border']};
                border-radius: 3px;
                text-align: center;
                background-color: {StyleConfig.colors['white']};
                max-height: 12px;
            }}
            QProgressBar::chunk {{
                background-color: {StyleConfig.colors['primary']};
                border-radius: 2px;
            }}
            QCheckBox {{
                spacing: 8px;
                color: {StyleConfig.colors['text']};
                padding: 4px 8px;
                border-radius: 4px;
                margin: 2px 0px;
            }}
            QCheckBox:hover {{
                background-color: #f0f0f0;
                border: 1px solid {StyleConfig.colors['primary']};
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 3px;
                background-color: {StyleConfig.colors['white']};
            }}
            QCheckBox::indicator:unchecked {{
                border: 2px solid {StyleConfig.colors['border']};
            }}
            QCheckBox::indicator:checked {{
                border: 2px solid {StyleConfig.colors['primary']};
                background-color: {StyleConfig.colors['primary']};
                image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
            }}
            QLabel {{
                color: {StyleConfig.colors['text']};
            }}
            QStatusBar {{
                background-color: {StyleConfig.colors['background']};
                color: {StyleConfig.colors['text']};
                padding: 2px 4px;
            }}
        """

    @staticmethod
    def get_draggable_label_style() -> str:
        """Get style for draggable label."""
        return f"""
            QLabel {{
                background-color: {StyleConfig.colors['white']};
                border: 2px dashed {StyleConfig.colors['border']};
                border-radius: 4px;
                color: {StyleConfig.colors['text']};
                padding: 12px;
                margin: 4px;
                min-height: 230px;
            }}
            QLabel:hover {{
                border-color: {StyleConfig.colors['primary']};
            }}
        """
