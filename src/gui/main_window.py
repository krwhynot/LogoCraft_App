import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QLabel, QFileDialog,
    QProgressBar, QCheckBox, QLineEdit, QGroupBox, QVBoxLayout,
    QHBoxLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap, QMouseEvent, QDragEnterEvent, QDropEvent

STYLESHEET = """
QMainWindow {
    background-color: #f5f5f5;
}
QGroupBox {
    font-weight: bold;
    border: 1px solid #636369;  /* Cool Gray */
    border-radius: 6px;
    margin-top: 6px;
    padding-top: 10px;
    color: #231347;  /* Deep Navy */
    background-color: white;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 7px;
    padding: 0px 5px 0px 5px;
}
QPushButton {
    background-color: #108375;  /* Teal Green */
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    min-width: 80px;
}
QPushButton:hover {
    background-color: #9FCDC7;  /* 60% lighter Teal Green */
}
QPushButton:disabled {
    background-color: #636369;  /* Cool Gray */
}
QLineEdit {
    padding: 4px;
    border: 1px solid #636369;  /* Cool Gray */
    border-radius: 4px;
    background-color: white;
}
QProgressBar {
    border: 1px solid #636369;  /* Cool Gray */
    border-radius: 4px;
    text-align: center;
    background-color: white;
}
QProgressBar::chunk {
    background-color: #108096;  /* Teal Blue */
}
QCheckBox {
    spacing: 8px;
    color: #231347;  /* Deep Navy */
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
}
QCheckBox::indicator:checked {
    background-color: #108375;  /* Teal Green */
    border: 2px solid #108375;
    border-radius: 2px;
}
QCheckBox::indicator:unchecked {
    background-color: white;
    border: 2px solid #636369;  /* Cool Gray */
    border-radius: 2px;
}
QLabel {
    color: #231347;  /* Deep Navy */
}
"""

class DraggableImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(300, 250)
        self.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px dashed #636369;  /* Cool Gray */
                border-radius: 8px;
                color: #231347;  /* Deep Navy */
            }
            QLabel:hover {
                border-color: #108375;  /* Teal Green */
            }
        """)
        self.dragging = False
        self.offset = QPoint()
        self.image_pos = QPoint()
        self.setText("Drag and drop image here\nor click 'Select Image'")
        self.setWordWrap(True)
        self.setAcceptDrops(True)

    # [Previous DraggableImageLabel methods remain unchanged...]
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LogoCraft Image Processor")
        self.setMinimumSize(500, 700)
        self.setStyleSheet(STYLESHEET)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(8, 8, 8, 8)

        # Preview section
        preview_group = QGroupBox("Image Preview")
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setSpacing(8)
        preview_layout.setContentsMargins(8, 16, 8, 8)

        self.preview_label = DraggableImageLabel()
        preview_layout.addWidget(self.preview_label)

        preview_controls = QHBoxLayout()
        self.select_button = QPushButton("Select Image")
        self.select_button.clicked.connect(self.select_files)
        preview_controls.addWidget(self.select_button)

        self.file_status_label = QLabel("No file selected")
        self.file_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_status_label.setStyleSheet("color: #636369;")  # Cool Gray
        preview_controls.addWidget(self.file_status_label)
        preview_layout.addLayout(preview_controls)

        main_layout.addWidget(preview_group)

        # Output options
        output_group = QGroupBox("Output Options")
        output_layout = QVBoxLayout(output_group)
        output_layout.setSpacing(4)
        output_layout.setContentsMargins(8, 16, 8, 8)

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
            cb.setStyleSheet("QCheckBox { font-size: 10pt; }")
            self.format_checks[size] = cb
            output_layout.addWidget(cb)

        main_layout.addWidget(output_group)

        # Process section with output directory
        process_group = QGroupBox("Output Directory & Processing")
        process_layout = QVBoxLayout(process_group)
        process_layout.setSpacing(8)
        process_layout.setContentsMargins(8, 16, 8, 8)

        dir_layout = QHBoxLayout()
        dir_layout.setSpacing(8)

        self.dir_path = QLineEdit()
        default_desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.dir_path.setText(default_desktop.replace('/', '\\'))
        dir_layout.addWidget(self.dir_path)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.browse_button)

        process_layout.addLayout(dir_layout)

        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self.process_images)
        self.process_button.setEnabled(False)
        process_layout.addWidget(self.process_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        process_layout.addWidget(self.progress_bar)

        main_layout.addWidget(process_group)

        # Supported formats in a more compact layout
        formats_group = QGroupBox("Supported Formats")
        formats_layout = QVBoxLayout(formats_group)
        formats_layout.setSpacing(2)
        formats_layout.setContentsMargins(8, 16, 8, 8)

        formats_info = QLabel(
            "PNG • JPEG/JPG • GIF • TIFF • WebP • BMP"
        )
        formats_info.setStyleSheet("color: #636369; font-size: 10pt;")  # Cool Gray
        formats_info.setWordWrap(True)
        formats_layout.addWidget(formats_info)
        
        main_layout.addWidget(formats_group)

        # Set stretch factors
        main_layout.setStretch(0, 2)  # Preview
        main_layout.setStretch(1, 1)  # Output options
        main_layout.setStretch(2, 1)  # Process section
        main_layout.setStretch(3, 0)  # Formats (minimal space)

        # Initialize variables
        self.current_file = None

    # [Previous methods remain unchanged...]
    def select_files(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image File",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp);;All Files (*)"
        )
        if file_name:
            self.process_selected_file(file_name)

    def process_selected_file(self, file_name):
        self.current_file = file_name
        self.file_status_label.setText(os.path.basename(file_name))
        self.process_button.setEnabled(True)
        self.update_preview(file_name)

    def update_preview(self, file_path):
        try:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                max_size = 230
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
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory",
            self.dir_path.text()
        )
        if directory:
            self.dir_path.setText(directory)

    def process_images(self):
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

            processor = ImageProcessor()
            logger.info(f"Loading image from: {self.current_file}")
            image = processor.load_image(self.current_file)

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
