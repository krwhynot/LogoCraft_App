"""
UI Component Factory for LogoCraft app.
Provides centralized component creation with consistent styling.
"""
from PyQt6.QtWidgets import (
    QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QProgressBar, QLineEdit, QCheckBox, QWidget
)
from PyQt6.QtCore import Qt
from typing import Optional, Tuple, Callable
from .style_config import StyleConfig

class ComponentFactory:
    """Factory for creating styled UI components"""
    
    @staticmethod
    def create_group_box(
        title: str,
        layout_type=QVBoxLayout,
        parent: Optional[QWidget] = None
    ) -> Tuple[QGroupBox, QVBoxLayout]:
        """Create a styled group box with layout"""
        group = QGroupBox(title, parent)
        layout = layout_type(group)
        layout.setSpacing(4)
        layout.setContentsMargins(6, 12, 6, 6)
        return group, layout

    @staticmethod
    def create_button(
        text: str,
        callback: Optional[Callable] = None,
        width: Optional[int] = None,
        enabled: bool = True,
        parent: Optional[QWidget] = None
    ) -> QPushButton:
        """Create a styled button"""
        button = QPushButton(text, parent)
        if callback:
            button.clicked.connect(callback)
        if width:
            button.setMaximumWidth(width)
        button.setEnabled(enabled)
        return button

    @staticmethod
    def create_progress_bar(
        parent: Optional[QWidget] = None,
        visible: bool = False
    ) -> QProgressBar:
        """Create a styled progress bar"""
        progress = QProgressBar(parent)
        progress.setVisible(visible)
        progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return progress

    @staticmethod
    def create_checkbox(
        text: str,
        checked: bool = False,
        callback: Optional[Callable] = None,
        parent: Optional[QWidget] = None
    ) -> QCheckBox:
        """Create a styled checkbox"""
        checkbox = QCheckBox(text, parent)
        checkbox.setChecked(checked)
        if callback:
            checkbox.stateChanged.connect(callback)
        return checkbox

    @staticmethod
    def create_input_field(
        placeholder: str = "",
        default_text: str = "",
        parent: Optional[QWidget] = None
    ) -> QLineEdit:
        """Create a styled input field"""
        input_field = QLineEdit(parent)
        input_field.setPlaceholderText(placeholder)
        if default_text:
            input_field.setText(default_text)
        return input_field

    @staticmethod
    def create_label(
        text: str,
        alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
        parent: Optional[QWidget] = None
    ) -> QLabel:
        """Create a styled label"""
        label = QLabel(text, parent)
        label.setAlignment(alignment)
        return label

    @staticmethod
    def create_status_label(
        text: str = "Ready",
        parent: Optional[QWidget] = None
    ) -> QLabel:
        """Create a styled status label"""
        label = QLabel(text, parent)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"color: {StyleConfig.colors['text']}; font-size: 9pt;")
        return label

    @staticmethod
    def create_file_status_label(
        text: str = "No file selected",
        parent: Optional[QWidget] = None
    ) -> QLabel:
        """Create a styled file status label"""
        label = QLabel(text, parent)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"color: {StyleConfig.colors['disabled']}; font-size: 9pt;")
        return label