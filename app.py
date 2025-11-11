import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
import pillow_heif
import os

__version__ = "0.1.0"
__author__ = "Adam Rogers"

class HEICConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("HEIC to JPG/PNG Converter")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        pillow_heif.register_heif_opener()
        
        main_frame = tk.Frame(root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(main_frame, text="HEIC Image Converter", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        self.drop_frame = tk.Frame(main_frame, relief=tk.RIDGE, 
                                   borderwidth=2, bg="#f0f0f0", height=150)
        self.drop_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        self.drop_frame.pack_propagate(False)
        
        drop_label = tk.Label(self.drop_frame, 
                             text="Drag & Drop HEIC file here\nor click Browse below",
                             bg="#f0f0f0", font=("Arial", 11))
        drop_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.drop_frame.drop_target_register(DND_FILES)
        self.drop_frame.dnd_bind('<<Drop>>', self.drop_file)
        
        self.file_path_var = tk.StringVar(value="No file selected")
        file_label = tk.Label(main_frame, textvariable=self.file_path_var,
                             wraplength=460, justify=tk.LEFT)
        file_label.pack(pady=(0, 10))
        
        browse_btn = tk.Button(main_frame, text="Browse File", 
                              command=self.browse_file, width=20, height=2)
        browse_btn.pack(pady=(0, 15))
        
        format_frame = tk.Frame(main_frame)
        format_frame.pack(pady=(0, 15))
        
        tk.Label(format_frame, text="Output Format:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.format_var = tk.StringVar(value="JPG")
        jpg_radio = tk.Radiobutton(format_frame, text="JPG", 
                                   variable=self.format_var, value="JPG")
        jpg_radio.pack(side=tk.LEFT, padx=5)
        
        png_radio = tk.Radiobutton(format_frame, text="PNG", 
                                   variable=self.format_var, value="PNG")
        png_radio.pack(side=tk.LEFT, padx=5)
        
        self.convert_btn = tk.Button(main_frame, text="Convert", 
                                     command=self.convert_file, 
                                     state=tk.DISABLED, width=20, height=2,
                                     bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.convert_btn.pack()
        
        self.current_file = None
    
    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="Select HEIC file",
            filetypes=[("HEIC files", "*.heic *.HEIC")]
        )
        if filename:
            self.load_file(filename)
    
    def drop_file(self, event):
        file_path = event.data
        file_path = file_path.strip('{}') # Needed for Windows
        self.load_file(file_path)
    
    def load_file(self, file_path):
        if not file_path.lower().endswith('.heic'):
            messagebox.showerror("Invalid File", 
                               "Please select a .heic file!")
            return
        
        if not os.path.exists(file_path):
            messagebox.showerror("File Not Found", 
                               "The selected file does not exist!")
            return
        
        self.current_file = file_path
        self.file_path_var.set(f"Selected: {os.path.basename(file_path)}")
        self.convert_btn.config(state=tk.NORMAL)
    
    def convert_file(self):
        if not self.current_file:
            return
        
        try:
            image = Image.open(self.current_file)
            
            output_format = self.format_var.get()
            extension = ".jpg" if output_format == "JPG" else ".png"
            
            base_name = os.path.splitext(self.current_file)[0]
            output_file = base_name + extension
            
            if output_format == "JPG":
                if image.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', image.size, (255, 255, 255))
                    if image.mode == 'P':
                        image = image.convert('RGBA')
                    background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                    image = background
                image.save(output_file, "JPEG", quality=95)
            else:
                image.save(output_file, "PNG")
            
            messagebox.showinfo("Success", 
                              f"File converted successfully!\nSaved as: {os.path.basename(output_file)}")
            
            # Reset
            self.current_file = None
            self.file_path_var.set("No file selected")
            self.convert_btn.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Conversion Error", 
                               f"Failed to convert file:\n{str(e)}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = HEICConverter(root)
    root.mainloop()