import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QProgressBar, QCheckBox,
    QFrame, QLineEdit, QGroupBox, QHBoxLayout
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap, QMouseEvent


class DraggableImageLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(300, 300)
        self.setStyleSheet("QLabel { background-color: white; border: 1px solid #cccccc; }")
        self.dragging = False
        self.offset = QPoint()
        self.image_pos = QPoint()

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
        # Center the image initially
        self.image_pos = QPoint(
            (self.width() - pixmap.width()) // 2,
            (self.height() - pixmap.height()) // 2
        )

    def paintEvent(self, event):
        if self.pixmap() and not self.pixmap().isNull():
            from PyQt6.QtGui import QPainter
            painter = QPainter(self)
            painter.drawPixmap(self.image_pos, self.pixmap())
        else:
            super().paintEvent(event)

class ImageProcessorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Processor")
        self.setMinimumSize(600, 400)

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Left side - Preview area and select button
        left_panel = QFrame()
        left_layout = QVBoxLayout(left_panel)

        # Preview area with draggable functionality
        self.preview_label = DraggableImageLabel()
        left_layout.addWidget(self.preview_label)

        # Select image button
        self.select_button = QPushButton("Select Image")
        self.select_button.clicked.connect(self.select_files)
        left_layout.addWidget(self.select_button)

        # "No file selected" label
        self.file_status_label = QLabel("No file selected")
        self.file_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.file_status_label)

        main_layout.addWidget(left_panel)

        # Right side - Output options
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)

        # Output Options group
        output_group = QGroupBox("Output Options")
        output_layout = QVBoxLayout(output_group)

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
            cb.setChecked(True)  # Default to checked
            self.format_checks[size] = cb
            output_layout.addWidget(cb)

        right_layout.addWidget(output_group)

        # Output Directory section
        out_dir_group = QGroupBox("Output Directory:")
        out_dir_layout = QVBoxLayout(out_dir_group)

        # Directory path and browse button in horizontal layout
        dir_layout = QHBoxLayout()
        self.dir_path = QLineEdit()
        # Set default output directory using Windows path style
        default_desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.dir_path.setText(default_desktop.replace('/', '\\'))
        dir_layout.addWidget(self.dir_path)

        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.browse_button)

        out_dir_layout.addLayout(dir_layout)
        right_layout.addWidget(out_dir_group)

        # Process button and progress bar
        self.process_button = QPushButton("Process Image")
        self.process_button.clicked.connect(self.process_images)
        self.process_button.setEnabled(False)
        right_layout.addWidget(self.process_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        right_layout.addWidget(self.progress_bar)

        right_layout.addStretch()  # Add stretch to push everything up
        main_layout.addWidget(right_panel)

        # Initialize variables
        self.current_file = None

    def select_files(self):
        """Handle file selection through dialog"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image File",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        if file_name:
            self.process_selected_file(file_name)

    def process_selected_file(self, file_name):
        """Process the selected file"""
        self.current_file = file_name
        self.file_status_label.setText(file_name.split('/')[-1])
        self.process_button.setEnabled(True)
        self.update_preview(file_name)

    def update_preview(self, file_path):
        """Update the preview with the selected image"""
        try:
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                # Calculate the preview size based on the image dimensions
                max_size = 280  # Slightly smaller than container to ensure visibility
                scale_factor = min(
                    max_size / pixmap.width(),
                    max_size / pixmap.height()
                )

                # Scale the image while maintaining aspect ratio
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
                # Get format specification
                format_spec = Config.OUTPUT_FORMATS.get(format_key)
                if not format_spec:
                    logger.warning(f"No format specification found for {format_key}")
                    continue

                # Process image
                output_dir = self.dir_path.text()
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                    logger.info(f"Created output directory: {output_dir}")

                # Ensure Windows path style
                output_name = os.path.join(output_dir, format_key).replace('/', '\\')
                logger.info(f"Processing image for format: {format_key}")
                logger.info(f"Output path: {output_name}")

                # Process and save the image
                processor.process_image(image, format_spec, output_name)

                # Update progress
                self.progress_bar.setValue(i + 1)

            self.statusBar().showMessage("Processing complete!")
            logger.info("Image processing completed successfully")

        except Exception as e:
            self.statusBar().showMessage(f"Error processing image: {str(e)}")
        finally:
            self.progress_bar.setVisible(False)
