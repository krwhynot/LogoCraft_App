import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QLabel, QFileDialog,
    QProgressBar, QCheckBox, QLineEdit, QGroupBox, QGridLayout,
    QSizePolicy, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt, QPoint, QMimeData
from PyQt6.QtGui import QPixmap, QMouseEvent, QDragEnterEvent, QDropEvent

STYLESHEET = """
QMainWindow {
    background-color: #f0f0f0;
}
QGroupBox {
    font-weight: bold;
    border: 1px solid #cccccc;
    border-radius: 6px;
    margin-top: 6px;
    padding-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 7px;
    padding: 0px 5px 0px 5px;
}
QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    min-width: 80px;
}
QPushButton:hover {
    background-color: #106ebe;
}
QPushButton:disabled {
    background-color: #cccccc;
}
QLineEdit {
    padding: 4px;
    border: 1px solid #cccccc;
    border-radius: 4px;
}
QProgressBar {
    border: 1px solid #cccccc;
    border-radius: 4px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #0078d4;
}
QCheckBox {
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
}
"""

class DraggableImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(300, 300)
        self.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px dashed #cccccc;
                border-radius: 8px;
            }
            QLabel:hover {
                border-color: #0078d4;
            }
        """)
        self.dragging = False
        self.offset = QPoint()
        self.image_pos = QPoint()
        self.setText("Drag and drop image here\nor click 'Select Image'")
        self.setWordWrap(True)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events for files"""
        if event.mimeData().hasUrls():
            # Check if at least one URL is a supported image file
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        """Handle drop events for files"""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff', '.webp')):
                    # Get reference to main window to process the file
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LogoCraft Image Processor")
        self.setMinimumSize(900, 600)
        self.setStyleSheet(STYLESHEET)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QGridLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Left side - Preview section
        preview_group = QGroupBox("Image Preview")
        preview_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setSpacing(10)
        preview_layout.setContentsMargins(10, 20, 10, 10)

        self.preview_label = DraggableImageLabel()
        self.preview_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        preview_layout.addWidget(self.preview_label)

        self.select_button = QPushButton("Select Image")
        self.select_button.clicked.connect(self.select_files)
        preview_layout.addWidget(self.select_button)

        self.file_status_label = QLabel("No file selected")
        self.file_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_status_label.setStyleSheet("color: #666666;")
        preview_layout.addWidget(self.file_status_label)

        main_layout.addWidget(preview_group, 0, 0, 3, 1)

        # Supported Formats Info
        formats_group = QGroupBox("Supported Input Formats")
        formats_layout = QVBoxLayout(formats_group)
        formats_layout.setSpacing(5)
        formats_layout.setContentsMargins(15, 20, 15, 15)

        formats_info = QLabel(
            "• PNG\n"
            "• JPEG/JPG\n"
            "• GIF\n"
            "• TIFF\n"
            "• WebP\n"
            "• BMP"
        )
        formats_info.setStyleSheet("color: #666666; font-size: 11pt;")
        formats_layout.addWidget(formats_info)
        main_layout.addWidget(formats_group, 3, 0)

        # Right side - Output options
        output_group = QGroupBox("Output Options")
        output_group.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        output_layout = QVBoxLayout(output_group)
        output_layout.setSpacing(8)
        output_layout.setContentsMargins(15, 20, 15, 15)

        # Predefined output formats
        self.format_checks = {}
        formats = [
            ('Logo.png (300x300)', 'Logo.png'),
            ('Smalllogo.png (136x136)', 'Smalllogo.png'),
            ('KDlogo.png (140x112)', 'KDlogo.png'),
            ('RPTlogo.bmp (155x110)', 'RPTlogo.bmp'),
            ('PRINTLOGO.bmp (Thermal Printer Optimized)', 'PRINTLOGO.bmp')
        ]

        for label, size in formats:
            cb = QCheckBox(label)
            cb.setChecked(True)
            cb.setStyleSheet("QCheckBox { font-size: 11pt; }")
            self.format_checks[size] = cb
            output_layout.addWidget(cb)

        main_layout.addWidget(output_group, 0, 1)

        # Output Directory section
        out_dir_group = QGroupBox("Output Directory")
        out_dir_layout = QVBoxLayout(out_dir_group)
        out_dir_layout.setSpacing(10)
        out_dir_layout.setContentsMargins(15, 20, 15, 15)

        dir_layout = QHBoxLayout()
        dir_layout.setSpacing(10)

        self.dir_path = QLineEdit()
        self.dir_path.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        default_desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.dir_path.setText(default_desktop.replace('/', '\\'))
        dir_layout.addWidget(self.dir_path)

        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.browse_button)

        out_dir_layout.addLayout(dir_layout)
        main_layout.addWidget(out_dir_group, 1, 1)

        # Process section
        process_group = QGroupBox("Process")
        process_layout = QVBoxLayout(process_group)
        process_layout.setSpacing(10)
        process_layout.setContentsMargins(15, 20, 15, 15)

        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self.process_images)
        self.process_button.setEnabled(False)
        process_layout.addWidget(self.process_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        process_layout.addWidget(self.progress_bar)

        main_layout.addWidget(process_group, 2, 1, 2, 1)

        # Set column stretch factors
        main_layout.setColumnStretch(0, 3)  # Preview takes more space
        main_layout.setColumnStretch(1, 2)  # Options take less space

        # Initialize variables
        self.current_file = None

    def select_files(self):
        """Handle file selection through dialog"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image File",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp);;All Files (*)"
        )
        if file_name:
            self.process_selected_file(file_name)

    def process_selected_file(self, file_name):
        """Process the selected file"""
        self.current_file = file_name
        self.file_status_label.setText(os.path.basename(file_name))
        self.process_button.setEnabled(True)
        self.update_preview(file_name)

    def update_preview(self, file_path):
        """Update the preview with the selected image"""
        try:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                max_size = 280
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

    def browse_directory(self):
        """Handle output directory selection"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.dir_path.text()
        )
        if directory:
            self.dir_path.setText(directory)

    def process_images(self):
        """Handle image processing"""
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
            from src.processors.image_processor import ImageProcessor
            from src.config import Config
            import os
            import logging

            logger = logging.getLogger(__name__)

            # Load the image
            processor = ImageProcessor()
            logger.info(f"Loading image from: {self.current_file}")
            image = processor.load_image(self.current_file)

            # Process for each selected format
            for i, format_key in enumerate(selected_formats):
                format_spec = Config.OUTPUT_FORMATS.get(format_key)
                if not format_spec:
                    logger.warning(f"No format specification found for {format_key}")
                    continue

                output_dir = self.dir_path.text()
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    logger.info(f"Created output directory: {output_dir}")

                output_name = os.path.join(output_dir, format_key).replace('/', '\\')
                logger.info(f"Processing image for format: {format_key}")
                logger.info(f"Output path: {output_name}")

                processor.process_image(image, format_spec, output_name)
                self.progress_bar.setValue(i + 1)

            self.statusBar().showMessage("Processing complete!")
            logger.info("Image processing completed successfully")

        except Exception as e:
            self.statusBar().showMessage(f"Error processing image: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)
