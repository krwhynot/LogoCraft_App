from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, 
    QLabel, QFileDialog, QProgressBar, QCheckBox,
    QFrame, QLineEdit, QGroupBox, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

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
        
        # Preview area
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(300, 300)
        self.preview_label.setStyleSheet("QLabel { background-color: white; border: 1px solid #cccccc; }")
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
            ('Logo.png (300x300)', '300x300'),
            ('Smalllogo.png (136x136)', '136x136'),
            ('KDlogo.png (140x112)', '140x112'),
            ('RPTlogo.bmp (155x110)', '155x110'),
            ('PRINTLOGO.bmp (Thermal Printer Optimized)', 'thermal')
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
        self.dir_path.setText("C:\\Users\\Default\\Desktop")
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
            "Image Files (*.png *.jpg *.jpeg *.bmp);;All Files (*)"
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
                # Scale pixmap to fit preview area while maintaining aspect ratio
                scaled_pixmap = pixmap.scaled(
                    300, 300,  # Fixed size preview
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
        
        # TODO: Implement actual image processing logic
        self.statusBar().showMessage("Processing image...")