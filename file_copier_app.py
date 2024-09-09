import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from file_operations import copy_files, get_single_json_file_path
from utils import get_value_from_dict

class FileCopierApp:
    """
    A GUI application for copying files from a source directory to a destination directory.
    
    Attributes:
        root (tk.Tk): The root window of the application.
        header_image_path (str): The file path of the header image.
        header_image (PIL.ImageTk.PhotoImage): The resized header image.
        header_label (tk.Label): The label widget displaying the header image.
        source_dir_entry (tk.Entry): The entry widget for the source directory path.
        source_browse_button (tk.Button): The button widget for browsing the source directory.
        destination_dir_entry (tk.Entry): The entry widget for the destination directory path.
        destination_browse_button (tk.Button): The button widget for browsing the destination directory.
        copy_button (tk.Button): The button widget for triggering the file copy process.
    """
    
    def __init__(self, root):
        """
        Initializes the FileCopierApp with the given root window.
        
        Args:
            root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("Copy App")
        self.root.configure(bg="white")  # Set the background color of the root window
        
        # Set the window size and center it on the screen
        self.set_window_size_and_center(700, 500)
        
        # Load and resize the header image
        self.header_image_path = "./images/logo_copy_app.png"
        self.header_image = self.load_and_resize_image(self.header_image_path, 400, 200)
        
        self.header_label = tk.Label(root, image=self.header_image, bg="white")
        self.header_label.pack(pady=5)
        
        # Create labels and entry widgets for source and destination directories
        tk.Label(root, text="Source Directory:", bg="white").pack(pady=5)
        self.source_dir_entry = tk.Entry(root, width=50, bg="white")
        self.source_dir_entry.pack(pady=5)
        self.source_browse_button = tk.Button(root, text="Browse", command=self.browse_source_dir, bg="white")
        self.source_browse_button.pack(pady=5)
        
        tk.Label(root, text="Destination Directory:", bg="white").pack(pady=5)
        self.destination_dir_entry = tk.Entry(root, width=50, bg="white")
        self.destination_dir_entry.pack(pady=5)
        self.destination_browse_button = tk.Button(root, text="Browse", command=self.browse_destination_dir, bg="white")
        self.destination_browse_button.pack(pady=5)
        
        # Create a button to trigger the copy_files function
        self.copy_button = tk.Button(root, text="Copy Files", command=self.copy_files, bg="white")
        self.copy_button.pack(pady=20)
        
    def set_window_size_and_center(self, width, height):
        """
        Sets the size of the root window and centers it on the screen.
        
        Args:
            width (int): The width of the window.
            height (int): The height of the window.
        """
        self.root.geometry(f'{width}x{height}')
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_and_resize_image(self, image_path, width, height):
        """
        Loads an image from the given file path and resizes it to the specified dimensions.
        
        Args:
            image_path (str): The file path of the image.
            width (int): The desired width of the resized image.
            height (int): The desired height of the resized image.
        
        Returns:
            PIL.ImageTk.PhotoImage: The resized image as a PhotoImage object.
        """
        image = Image.open(image_path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)
    
    def browse_source_dir(self):
        """
        Opens a file dialog for selecting the source directory and updates the source directory entry widget.
        """
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.source_dir_entry.delete(0, tk.END)
            self.source_dir_entry.insert(0, selected_dir)
    
    def browse_destination_dir(self):
        """
        Opens a file dialog for selecting the destination directory and updates the destination directory entry widget.
        """
        selected_dir = filedialog.askdirectory()
        if selected_dir:
            self.destination_dir_entry.delete(0, tk.END)
            self.destination_dir_entry.insert(0, selected_dir)
    
    def copy_files(self):
        """
        Copies files from the source directory to the destination directory.
        Displays a success message if the copy process is successful, or a warning message if an error occurs.
        """
        source_dir = self.source_dir_entry.get()
        destination_dir = self.destination_dir_entry.get()
        
        try:
            json_file_path = get_single_json_file_path(source_dir)
            copy_files(source_dir, destination_dir, json_file_path)
            messagebox.showinfo("Success", "Files copied successfully!")
        except Exception as e:
            messagebox.showwarning("Warning", str(e))
            self.root.quit()
            self.root.destroy()
            exit(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileCopierApp(root)
    root.mainloop()