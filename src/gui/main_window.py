import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import logging
from pathlib import Path

from src.config import Config
from src.processors.image_processor import ImageProcessor
from src.utils.validators import is_valid_file, is_valid_directory

class ImageProcessorGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Processor")
        self.window.geometry("600x450")
        self.window.resizable(False, False)  # Fix window size

        self.input_file = None
        self.preview_image = None

        self._create_widgets()
        self._setup_layout()

    def _create_widgets(self):
        # Main container frames
        self.left_frame = ttk.Frame(self.window)
        self.right_frame = ttk.Frame(self.window)

        # Preview area (left side)
        self.preview_frame = ttk.Frame(self.left_frame, width=300, height=300)
        self.preview_label = ttk.Label(self.preview_frame, text="No file selected")
        self.select_image_btn = ttk.Button(self.left_frame, text="Select Image", command=self._browse_input)

        # Output options (right side)
        self.options_frame = ttk.LabelFrame(self.right_frame, text="Output Options", padding="10")

        # Checkboxes for output formats
        self.format_vars = {
            'Logo.png (300x300)': tk.BooleanVar(value=True),
            'Smalllogo.png (136x136)': tk.BooleanVar(value=True),
            'KDlogo.png (140x112)': tk.BooleanVar(value=True),
            'RPTlogo.bmp (135x110)': tk.BooleanVar(value=True),
            'PRINTLOGO.bmp (Thermal Printer Optimized)': tk.BooleanVar(value=True)
        }

        self.format_checkboxes = []
        for text, var in self.format_vars.items():
            cb = ttk.Checkbutton(self.options_frame, text=text, variable=var)
            self.format_checkboxes.append(cb)

        # Output directory selection
        self.output_label = ttk.Label(self.options_frame, text="Output Directory:")
        self.output_path_var = tk.StringVar()
        self.output_entry = ttk.Entry(self.options_frame, textvariable=self.output_path_var)
        self.browse_output_btn = ttk.Button(self.options_frame, text="Browse...", command=self._browse_output)

        # Process button
        self.process_btn = ttk.Button(self.options_frame, text="Process Image", command=self._process_image)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.window, variable=self.progress_var, maximum=100)

    def _setup_layout(self):
        # Main frame layout
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

        # Preview area layout
        self.preview_frame.pack(fill=tk.BOTH, expand=True)
        self.preview_frame.pack_propagate(False)  # Maintain size
        self.preview_label.pack(fill=tk.BOTH, expand=True)
        self.select_image_btn.pack(pady=5)

        # Output options layout
        self.options_frame.pack(fill=tk.BOTH, expand=True)

        # Format checkboxes
        for cb in self.format_checkboxes:
            cb.pack(anchor=tk.W, pady=2)

        # Output directory
        self.output_label.pack(anchor=tk.W, pady=(10,2))
        self.output_entry.pack(fill=tk.X, pady=2)
        self.browse_output_btn.pack(anchor=tk.W, pady=2)

        # Process button
        self.process_btn.pack(pady=10)

        # Progress bar
        self.progress_bar.pack(fill=tk.X, padx=10, pady=(0,10))

    def _browse_input(self):
        filetypes = [("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        filename = filedialog.askopenfilename(filetypes=filetypes)
        if filename:
            try:
                self.input_file = filename
                self._update_preview(filename)
            except Exception as e:
                logging.error(f"Error loading image: {e}")
                messagebox.showerror("Error", "Failed to load image")

    def _browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path_var.set(directory)

    def _update_preview(self, image_path):
        try:
            # Load and resize image for preview
            image = Image.open(image_path)
            preview_size = (280, 280)  # Slightly smaller than frame for padding
            image.thumbnail(preview_size, Image.Resampling.LANCZOS)

            # Convert to PhotoImage for display
            photo = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo  # Keep a reference
        except Exception as e:
            logging.error(f"Error updating preview: {e}")
            messagebox.showerror("Error", "Failed to load preview")

    def _process_image(self):
        if not self.input_file or not self.output_path_var.get():
            messagebox.showerror("Error", "Please select input file and output directory")
            return

        try:
            self.progress_var.set(0)
            input_path = self.input_file
            output_dir = self.output_path_var.get()

            # Load the input image
            image = Image.open(input_path)

            # Get selected formats
            selected_formats = [name for name, var in self.format_vars.items() if var.get()]
            if not selected_formats:
                messagebox.showerror("Error", "Please select at least one output format")
                return

            # Process each selected format
            total_formats = len(selected_formats)
            for i, format_name in enumerate(selected_formats):
                # Extract size from format name
                if 'Logo.png (300x300)' in format_name:
                    size = (300, 300)
                    output_name = 'Logo.png'
                elif 'Smalllogo.png (136x136)' in format_name:
                    size = (136, 136)
                    output_name = 'Smalllogo.png'
                elif 'KDlogo.png (140x112)' in format_name:
                    size = (140, 112)
                    output_name = 'KDlogo.png'
                elif 'RPTlogo.bmp (135x110)' in format_name:
                    size = (135, 110)
                    output_name = 'RPTlogo.bmp'
                else:  # PRINTLOGO.bmp
                    size = (135, 110)  # Same size as RPTlogo but optimized for thermal
                    output_name = 'PRINTLOGO.bmp'

                # Create a copy and resize
                img_copy = image.copy()
                img_copy.thumbnail(size, Image.Resampling.LANCZOS)

                # Save the image
                output_path = os.path.join(output_dir, output_name)
                if output_name.endswith('.bmp'):
                    img_copy = img_copy.convert('1')  # Convert to 1-bit for thermal printer
                img_copy.save(output_path)

                # Update progress
                self.progress_var.set((i + 1) * 100 / total_formats)
                self.window.update()

            messagebox.showinfo("Success", "Image processing completed")
            self.progress_var.set(100)

        except Exception as e:
            logging.error(f"Error processing image: {e}")
            messagebox.showerror("Error", f"Failed to process image: {str(e)}")
            self.progress_var.set(0)

    def run(self):
        """Start the GUI application."""
        self.window.mainloop()
