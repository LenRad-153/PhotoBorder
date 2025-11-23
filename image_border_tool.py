import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageDraw
import os
from pathlib import Path
import threading

class ImageBorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Border Tool")
        self.root.geometry("600x550")
        self.root.resizable(True, True)
        
        self.selected_folder = ""
        self.image_files = []
        self.border_color = "#FFFFFF"  # Default white
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Allow the main frame to expand when the window is resized
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Image Border Tool", 
                               font=("Arial", 24, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=tk.W)
        
        # Section 1: Folder Selection
        section1_label = ttk.Label(main_frame, text="1. Select Image Folder", 
                                   font=("Arial", 12, "bold"))
        section1_label.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        self.browse_btn = ttk.Button(main_frame, text="Browse Folder...", 
                                     command=self.select_folder, width=20)
        self.browse_btn.grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        
        self.folder_label = ttk.Label(main_frame, text="No folder selected", 
                                      foreground="gray")
        self.folder_label.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        self.count_label = ttk.Label(main_frame, text="", foreground="green", 
                                     font=("Arial", 10, "bold"))
        self.count_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # Section 2: Border Thickness
        section2_label = ttk.Label(main_frame, text="2. Border Thickness", 
                                   font=("Arial", 12, "bold"))
        section2_label.grid(row=5, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        slider_frame = ttk.Frame(main_frame)
        slider_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.thickness_var = tk.DoubleVar(value=5.0)
        self.thickness_slider = ttk.Scale(slider_frame, from_=1, to=20, 
                                         variable=self.thickness_var, 
                                         orient=tk.HORIZONTAL, length=450,
                                         command=self.update_thickness_label)
        self.thickness_slider.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.thickness_label = ttk.Label(slider_frame, text="5.0%", width=10)
        self.thickness_label.grid(row=0, column=1, padx=(10, 0))
        
        # Section 3: Border Color
        section3_label = ttk.Label(main_frame, text="3. Border Color", 
                                   font=("Arial", 12, "bold"))
        section3_label.grid(row=7, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        self.color_btn = ttk.Button(main_frame, text="Choose Color", 
                                   command=self.choose_color, width=20)
        self.color_btn.grid(row=8, column=0, sticky=tk.W, pady=(0, 10))
        
        self.color_preview = tk.Canvas(main_frame, width=100, height=40, 
                                       bg=self.border_color, 
                                       highlightthickness=1, highlightbackground="black")
        self.color_preview.grid(row=9, column=0, sticky=tk.W, pady=(0, 20))
        
        # Section 4: Process Button
        self.process_btn = ttk.Button(main_frame, text="Process Images", 
                                     command=self.process_images, width=30)
        self.process_btn.grid(row=10, column=0, columnspan=2, pady=(0, 20))
        self.process_btn.state(['disabled'])
        
        # Style the button to make it prominent
        style = ttk.Style()
        style.configure('Process.TButton', font=('Arial', 12, 'bold'))
        self.process_btn.configure(style='Process.TButton')
        
        # Progress Bar
        self.progress = ttk.Progressbar(main_frame, length=550, mode='determinate')
        self.progress.grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(main_frame, text="", foreground="gray")
        self.status_label.grid(row=12, column=0, columnspan=2)
        
        # Info Label
        info_label = ttk.Label(main_frame, 
                              text="Output images will be saved in a 'bordered_images' subfolder",
                              foreground="gray", font=("Arial", 9))
        info_label.grid(row=13, column=0, columnspan=2, pady=(20, 0))
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder containing images")
        if folder:
            self.selected_folder = folder
            self.load_images()
            self.folder_label.config(text=self.selected_folder)
            if self.image_files:
                self.process_btn.state(['!disabled'])
    
    def load_images(self):
        self.image_files = []
        extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
        
        try:
            for file in os.listdir(self.selected_folder):
                if file.lower().endswith(extensions):
                    self.image_files.append(os.path.join(self.selected_folder, file))
            
            self.count_label.config(text=f"{len(self.image_files)} images found")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading images: {str(e)}")
    
    def update_thickness_label(self, value):
        self.thickness_label.config(text=f"{float(value):.1f}%")
    
    def choose_color(self):
        color = colorchooser.askcolor(title="Choose border color", 
                                     color=self.border_color)
        if color[1]:
            self.border_color = color[1]
            self.color_preview.config(bg=self.border_color)
    
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def process_images(self):
        if not self.image_files:
            messagebox.showwarning("Warning", "No images to process!")
            return
        
        # Disable button during processing
        self.process_btn.state(['disabled'])
        self.browse_btn.state(['disabled'])
        
        # Run processing in separate thread to keep UI responsive
        thread = threading.Thread(target=self.process_images_thread)
        thread.daemon = True
        thread.start()
    
    def process_images_thread(self):
        border_percent = self.thickness_var.get() / 100.0
        border_color_rgb = self.hex_to_rgb(self.border_color)
        
        # Create output folder
        output_folder = os.path.join(self.selected_folder, "bordered_images")
        os.makedirs(output_folder, exist_ok=True)
        
        total = len(self.image_files)
        self.progress['maximum'] = total
        processed = 0
        
        for image_path in self.image_files:
            try:
                self.process_single_image(image_path, output_folder, 
                                         border_percent, border_color_rgb)
                processed += 1
                self.progress['value'] = processed
                self.status_label.config(text=f"Processing: {processed}/{total}")
                self.root.update_idletasks()
            except Exception as e:
                print(f"Error processing {os.path.basename(image_path)}: {str(e)}")
        
        # Re-enable buttons
        self.process_btn.state(['!disabled'])
        self.browse_btn.state(['!disabled'])
        
        messagebox.showinfo("Complete", 
                           f"Successfully processed {processed} images!\n"
                           f"Saved to: {output_folder}")
        self.status_label.config(text=f"Complete! {processed} images processed")
    
    def process_single_image(self, input_path, output_folder, border_percent, border_color):
        # Open original image
        img = Image.open(input_path)
        
        # Convert to RGB if necessary (for PNG with transparency, etc.)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Create a white background
            background = Image.new('RGB', img.size, border_color)
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        original_width, original_height = img.size
        
        # Calculate border thickness based on smaller dimension
        smaller_dimension = min(original_width, original_height)
        border_thickness = int(smaller_dimension * border_percent)
        
        # New dimensions
        new_width = original_width + (border_thickness * 2)
        new_height = original_height + (border_thickness * 2)
        
        # Create new image with border
        bordered_img = Image.new('RGB', (new_width, new_height), border_color)
        
        # Paste original image in center
        bordered_img.paste(img, (border_thickness, border_thickness))
        
        # Save with same filename
        filename = os.path.basename(input_path)
        output_path = os.path.join(output_folder, filename)
        
        # Save with appropriate format
        bordered_img.save(output_path, quality=95)

def main():
    root = tk.Tk()
    app = ImageBorderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()