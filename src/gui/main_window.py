"""Main window implementation for LogoCraft app."""
import os
import logging
from typing import Dict, Optional
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFileDialog, QLabel, QCheckBox
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap, QMouseEvent, QDragEnterEvent, QDropEvent
from src.processors.image_processor import ImageProcessor
from src.config import config_manager
from src.core.error_handler import handle_errors
from .style_config import StyleConfig
from .component_factory import ComponentFactory

logger = logging.getLogger(__name__)

class DraggableImageLabel(QLabel):
    """Draggable image preview label with drop support"""
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(250, 250)
        self.setStyleSheet(StyleConfig.get_draggable_label_style())
        self.dragging = False
        self.offset = QPoint()
        self.image_pos = QPoint()
        self.setText("Drag and drop image here\nor click 'Select Image'")
        self.setWordWrap(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                    main_window = self.window()
                    if isinstance(main_window, ImageProcessorGUI):
                        main_window.process_selected_file(file_path)
                    break
            event.acceptProposedAction()
        event.ignore()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.offset = event.pos() - self.image_pos

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.image_pos = event.pos() - self.offset
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = False

    def setPixmap(self, pixmap: QPixmap):
        super().setPixmap(pixmap)
        self.image_pos = QPoint(
            (self.width() - pixmap.width()) // 2,
            (self.height() - pixmap.height()) // 2
        )

    def paintEvent(self, event):
        if self.pixmap() and not self.pixmap().isNull():
            from PyQt6.QtGui import QPainter
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            painter.drawPixmap(self.image_pos, self.pixmap())
        else:
            super().paintEvent(event)

class ImageProcessorGUI(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.current_file: Optional[str] = None
        self.format_checks: Dict[str, QCheckBox] = {}
        self.image_processor = ImageProcessor()
        self._setup_ui()
        logger.info("Application window initialized")
    
    def _setup_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("LogoCraft Image Processor")
        self.setMinimumSize(400, 600)
        self.setStyleSheet(StyleConfig.get_stylesheet())
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(6)
        main_layout.setContentsMargins(6, 6, 6, 6)

        main_layout.addWidget(self._create_preview_group())
        main_layout.addWidget(self._create_output_group())
        main_layout.addWidget(self._create_process_group())
        main_layout.addWidget(self._create_formats_group())

    def _create_preview_group(self) -> QWidget:
        """Create the preview section"""
        group, layout = ComponentFactory.create_group_box("Image Preview")

        self.preview_label = DraggableImageLabel()
        layout.addWidget(self.preview_label)

        controls = QHBoxLayout()
        controls.setSpacing(4)

        self.select_button = ComponentFactory.create_button(
            "Select Image",
            callback=self.select_files
        )
        controls.addWidget(self.select_button)

        self.file_status_label = ComponentFactory.create_file_status_label()
        controls.addWidget(self.file_status_label)

        layout.addLayout(controls)
        return group

    def _create_output_group(self) -> QWidget:
        """Create the output options section"""
        group, layout = ComponentFactory.create_group_box("Output Options")

        formats = [
            ('Logo PNG (300×300)', 'Logo.png'),
            ('Small Logo PNG (136×136)', 'Smalllogo.png'),
            ('KD Logo PNG (140×112)', 'KDlogo.png'),
            ('RPT Logo BMP (155×110)', 'RPTlogo.bmp'),
            ('Print Logo BMP (Thermal)', 'PRINTLOGO.bmp')
        ]

        for label, filename in formats:
            checkbox = ComponentFactory.create_checkbox(label, checked=True)
            self.format_checks[filename] = checkbox
            layout.addWidget(checkbox)

        return group

    def _create_process_group(self) -> QWidget:
        """Create the processing section"""
        group, layout = ComponentFactory.create_group_box("Output & Processing")

        dir_layout = QHBoxLayout()
        dir_layout.setSpacing(4)

        default_desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.dir_path = ComponentFactory.create_input_field(
            default_text=default_desktop.replace('/', '\\')
        )
        dir_layout.addWidget(self.dir_path)

        self.browse_button = ComponentFactory.create_button(
            "Browse",
            callback=self.browse_directory,
            width=70
        )
        dir_layout.addWidget(self.browse_button)

        layout.addLayout(dir_layout)

        self.process_button = ComponentFactory.create_button(
            "Process Image",
            callback=self.process_images,
            enabled=False
        )
        layout.addWidget(self.process_button)

        self.progress_bar = ComponentFactory.create_progress_bar()
        layout.addWidget(self.progress_bar)

        return group

    def _create_formats_group(self) -> QWidget:
        """Create the supported formats section"""
        group, layout = ComponentFactory.create_group_box("Formats")

        formats_info = ComponentFactory.create_label(
            "PNG • JPEG/JPG • GIF • TIFF • WebP • BMP",
            parent=group
        )
        formats_info.setWordWrap(True)
        layout.addWidget(formats_info)
        
        return group

    @handle_errors(logger)
    def select_files(self, sender=None):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image File",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp);;All Files (*)"
        )
        if file_name:
            self.process_selected_file(file_name)

    @handle_errors(logger)
    def process_selected_file(self, file_name: str):
        self.current_file = file_name
        self.file_status_label.setText(os.path.basename(file_name))
        self.process_button.setEnabled(True)
        self.update_preview(file_name)

    @handle_errors(logger)
    def update_preview(self, file_path: str):
        try:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                max_size = 200  # Increased from 180 to ensure full preview visibility
                scale_factor = min(
                    max_size / pixmap.width(),
                    max_size / pixmap.height()
                )

                scaled_pixmap = pixmap.scaled(
                    int(pixmap.width() * scale_factor),
                    int(pixmap.height() * scale_factor),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.preview_label.setPixmap(scaled_pixmap)
            else:
                self.preview_label.setText("Unable to load preview")
        except Exception as e:
            self.preview_label.setText(f"Preview error: {str(e)}")

    @handle_errors(logger)
    def browse_directory(self, sender=None):
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.dir_path.text()
        )
        if directory:
            self.dir_path.setText(directory)

    @handle_errors(logger)
    def process_images(self, *args):
        """Process the selected image"""
        if not self.current_file:
            return

        selected_formats = [fmt for fmt, cb in self.format_checks.items() if cb.isChecked()]
        if not selected_formats:
            self.statusBar().showMessage("Please select at least one output format")
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(len(selected_formats))
        self.progress_bar.setValue(0)

        try:
            image = self.image_processor.load_image(self.current_file)
            output_dir = self.dir_path.text()
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                logger.info(f"Created output directory: {output_dir}")

            for i, format_key in enumerate(selected_formats):
                format_spec = config_manager.get_format(format_key)
                if not format_spec:
                    logger.warning(f"No format specification found for {format_key}")
                    continue

                output_path = os.path.join(output_dir, format_key).replace('/', '\\')
                self.image_processor.process_image(image, format_spec, output_path)
                self.progress_bar.setValue(i + 1)

            self.statusBar().showMessage("Processing complete!")
            logger.info("Image processing completed successfully")

        finally:
            self.progress_bar.setVisible(False)
