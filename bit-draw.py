#!/usr/bin/env python3

import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageDraw, ImageTk
from datetime import datetime
import os

def ensure_directories():
    """Create necessary directories if they don't exist"""
    for directory in ['drawings', 'image-data']:
        if not os.path.exists(directory):
            os.makedirs(directory)

class MatrixConfigDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="Enter matrix configuration:").grid(row=0, columnspan=2)
        
        tk.Label(master, text="Number of columns:").grid(row=1)
        self.cols = tk.Entry(master)
        self.cols.grid(row=1, column=1)
        self.cols.insert(0, "1")
        
        tk.Label(master, text="Number of rows:").grid(row=2)
        self.rows = tk.Entry(master)
        self.rows.grid(row=2, column=1)
        self.rows.insert(0, "1")
        
        tk.Label(master, text="LED Color:").grid(row=3)
        self.led_colors = {
            'White': '#FFFFFF',
            'Red': '#FF0000',
            'Yellow-Green': '#9ACD32',
            'Blue': '#0000FF',
            'Yellow': '#FFFF00',
            'Green': '#00FF00',
            'Amber': '#FFBF00'
        }
        self.color_var = tk.StringVar(value='White')
        self.color_menu = tk.OptionMenu(
            master,
            self.color_var,
            *self.led_colors.keys()
        )
        self.color_menu.grid(row=3, column=1, sticky='ew')
        
        return self.cols  # Initial focus
    
    def validate(self):
        try:
            self.result_cols = int(self.cols.get())
            self.result_rows = int(self.rows.get())
            self.result_color = self.led_colors[self.color_var.get()]
            if self.result_cols < 1 or self.result_rows < 1:
                raise ValueError
            return True
        except ValueError:
            tk.messagebox.showerror(
                "Error",
                "Please enter positive integers"
            )
            return False

class PixelDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Drawer")
        self.root.configure(bg='#2B2B2B')  # Dark grey background
        
        # Set minimum window size (significantly reduced)
        self.root.minsize(1400, 600)
        
        # Get matrix configuration
        config_dialog = MatrixConfigDialog(root)
        if not config_dialog:  # Dialog was cancelled
            root.quit()
            return
            
        # Store matrix configuration
        self.MATRIX_COLS = config_dialog.result_cols
        self.MATRIX_ROWS = config_dialog.result_rows
        self.LED_COLOR = config_dialog.result_color
        
        # Constants for the grid
        self.SQUARE_SIZE = 36
        self.GRID_WIDTH = 8 * self.MATRIX_COLS
        self.GRID_HEIGHT = 8 * self.MATRIX_ROWS
        
        # Create split view
        self.split_frame = tk.Frame(root, bg='#2B2B2B')
        self.split_frame.pack(expand=True, fill=tk.BOTH)
        
        # Left side - Pixel Editor
        self.editor_frame = tk.Frame(self.split_frame, bg='#2B2B2B')
        self.editor_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=(0, 20))  # Reduced right padding
        
        # Right side - Image Gallery (with fixed width)
        # Increased width to 700 to accommodate padding while maintaining ~600px content width
        self.gallery_frame = tk.Frame(self.split_frame, bg='#2B2B2B', width=700, padx=40)
        self.gallery_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.gallery_frame.pack_propagate(False)  # Prevent frame from shrinking to content
        
        # Create editor components
        self.create_editor()
        
        # Create gallery components
        self.create_gallery()
        
        # Store rectangle references
        self.rectangles = []
        
        # Create grid of black squares
        self.create_grid()
        
        # Bind click and drag events
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        
        # Add state to track the current drawing color
        self.current_draw_color = None
        
        # Load existing images
        self.load_gallery_images()

    def create_editor(self):
        """Create the pixel editor side"""
        # Create spacer frame for top padding
        tk.Frame(self.editor_frame, bg='#2B2B2B', height=20).pack()  # Reduced from 40
        
        # Create canvas frame with border effect
        self.canvas_frame = tk.Frame(
            self.editor_frame,
            bg='#1E1E1E',
            padx=1,  # Reduced from 2
            pady=1   # Reduced from 2
        )
        self.canvas_frame.pack(expand=True)
        
        # Create canvas with padding frame
        self.canvas_padding = tk.Frame(
            self.canvas_frame,
            bg='#333333',
            padx=15,  # Reduced from 30
            pady=15   # Reduced from 30
        )
        self.canvas_padding.pack(expand=True)
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.canvas_padding,
            width=self.GRID_WIDTH * self.SQUARE_SIZE,
            height=self.GRID_HEIGHT * self.SQUARE_SIZE,
            bg='#333333',
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Create button frame with dark theme
        self.button_frame = tk.Frame(self.editor_frame, bg='#2B2B2B')
        self.button_frame.pack(pady=20)  # Reduced from 40
        
        # Style for buttons
        button_style = {
            'bg': '#404040',
            'fg': 'white',
            'relief': tk.FLAT,
            'padx': 15,
            'pady': 8
        }
        
        # Create buttons
        self.reset_button = tk.Button(
            self.button_frame,
            text="Reset Grid",
            command=self.reset_grid,
            **button_style
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = tk.Button(
            self.button_frame,
            text="Save",
            command=self.save_all,
            **button_style
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

    def create_gallery(self):
        """Create the image gallery side"""
        # Create title frame for better padding control
        title_frame = tk.Frame(self.gallery_frame, bg='#2B2B2B')
        title_frame.pack(pady=20)
        
        # Create gallery label
        tk.Label(
            title_frame,
            text="Saved Drawings",
            font=('Arial', 14),
            bg='#2B2B2B',
            fg='white'
        ).pack()
        
        # Add instruction text
        tk.Label(
            title_frame,
            text="right click to remove an image",
            font=('Arial', 9),
            bg='#2B2B2B',
            fg='#888888'  # Light grey color
        ).pack()
        
        # Create container frame for gallery canvas and scrollbar with extra padding
        gallery_container = tk.Frame(self.gallery_frame, bg='#2B2B2B', padx=20)  # Added padding to container
        gallery_container.pack(expand=True, fill=tk.BOTH, pady=(0, 20))
        
        # Create scrollable frame for images
        self.gallery_canvas = tk.Canvas(
            gallery_container,
            bg='#333333',
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            gallery_container,
            orient="vertical",
            command=self.gallery_canvas.yview
        )
        
        # Configure scrolling
        self.gallery_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create frame for image grid with padding
        self.gallery_grid = tk.Frame(
            self.gallery_canvas,
            bg='#333333',
            pady=20  # Bottom padding for grid
        )
        
        # Pack scrollbar and canvas with extra padding
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 20))  # Added right padding to scrollbar
        self.gallery_canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        # Create window in canvas for the frame
        self.gallery_canvas.create_window(
            (0, 0),
            window=self.gallery_grid,
            anchor="nw"
        )
        
        # Configure canvas scrolling
        self.gallery_grid.bind(
            "<Configure>",
            lambda e: self.gallery_canvas.configure(
                scrollregion=self.gallery_canvas.bbox("all")
            )
        )

    def load_gallery_images(self):
        """Load and display existing high-res images"""
        try:
            image_files = sorted(
                [f for f in os.listdir('drawings') if f.endswith('.png')],
                reverse=True
            )
            
            row = 0
            col = 0
            for img_file in image_files:
                try:
                    # Load and resize image
                    img_path = os.path.join('drawings', img_file)
                    img = Image.open(img_path)
                    img.thumbnail((120, 120))  # Smaller thumbnails for four columns
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(img)
                    
                    # Create frame for image
                    img_frame = tk.Frame(
                        self.gallery_grid,
                        bg='#1E1E1E',
                        padx=2,
                        pady=2
                    )
                    img_frame.grid(row=row, column=col, padx=6, pady=6)  # Reduced padding
                    
                    # Add image label
                    label = tk.Label(
                        img_frame,
                        image=photo,
                        bg='#333333'
                    )
                    label.image = photo  # Keep reference
                    label.filename = img_file  # Store filename for deletion
                    label.pack()
                    
                    # Bind right-click event
                    label.bind('<Button-3>', self.show_context_menu)
                    
                    # Update grid position
                    col += 1
                    if col >= 4:  # Changed to 4 columns
                        col = 0
                        row += 1
                        
                except Exception as e:
                    print(f"Error loading image {img_file}: {e}")
                    
        except Exception as e:
            print(f"Error loading gallery: {e}")

    def show_context_menu(self, event):
        """Show right-click context menu for image deletion"""
        label = event.widget
        menu = tk.Menu(self.root, tearoff=0, bg='#404040', fg='white', 
                      activebackground='#505050', activeforeground='white')
        menu.add_command(label="Delete", 
                        command=lambda: self.confirm_delete(label))
        menu.tk_popup(event.x_root, event.y_root)

    def confirm_delete(self, label):
        """Show confirmation dialog and delete if confirmed"""
        if messagebox.askyesno("Confirm Delete", 
                             "Are you sure you want to delete this image?",
                             icon='warning'):
            try:
                # Delete high-res image
                hi_res_path = os.path.join('drawings', label.filename)
                if os.path.exists(hi_res_path):
                    os.remove(hi_res_path)
                
                # Delete corresponding low-res image
                base_name = label.filename.replace('pixel_art_', '')
                timestamp = base_name.split('.')[0]
                low_res_files = [f for f in os.listdir('image-data') 
                               if f.startswith(f'pixel_art_{timestamp}')]
                
                for low_res_file in low_res_files:
                    low_res_path = os.path.join('image-data', low_res_file)
                    if os.path.exists(low_res_path):
                        os.remove(low_res_path)
                
                # Refresh gallery
                self.clear_gallery()
                self.load_gallery_images()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete image: {e}")

    def create_grid(self):
        for row in range(self.GRID_HEIGHT):
            row_rectangles = []
            for col in range(self.GRID_WIDTH):
                x1 = col * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                
                rectangle = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill='black',
                    outline='gray'
                )
                row_rectangles.append(rectangle)
            self.rectangles.append(row_rectangles)
    
    def on_click(self, event):
        # Convert click coordinates to grid position
        col = event.x // self.SQUARE_SIZE
        row = event.y // self.SQUARE_SIZE
        
        # Ensure we're within grid bounds
        if row >= self.GRID_HEIGHT or col >= self.GRID_WIDTH:
            return
            
        # Get the clicked rectangle
        rectangle = self.rectangles[row][col]
        
        # Toggle color and set current drawing color
        current_color = self.canvas.itemcget(rectangle, 'fill')
        self.current_draw_color = self.LED_COLOR if current_color == 'black' else 'black'
        self.canvas.itemconfig(rectangle, fill=self.current_draw_color)
    
    def on_drag(self, event):
        # Convert drag coordinates to grid position
        col = event.x // self.SQUARE_SIZE
        row = event.y // self.SQUARE_SIZE
        
        # Ensure we're within grid bounds
        if row >= self.GRID_HEIGHT or col >= self.GRID_WIDTH or row < 0 or col < 0:
            return
            
        # Get the rectangle under the cursor
        rectangle = self.rectangles[row][col]
        
        # Set to current drawing color (established by initial click)
        if self.current_draw_color is not None:
            self.canvas.itemconfig(rectangle, fill=self.current_draw_color)

    def clear_gallery(self):
        """Clear all images from the gallery grid"""
        for widget in self.gallery_grid.winfo_children():
            widget.destroy()

    def save_all(self):
        """Save both high-res and low-res images"""
        # Ensure directories exist
        ensure_directories()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save images
        self.save_drawing(timestamp)
        
        # Refresh gallery view
        self.clear_gallery()
        self.load_gallery_images()

    def save_drawing(self, timestamp):
        """Save high-res and low-res PNG images"""
        # Create high-res image
        hi_res_image = Image.new('RGB', (self.GRID_WIDTH * self.SQUARE_SIZE, 
                                self.GRID_HEIGHT * self.SQUARE_SIZE), 
                        'white')
        hi_res_draw = ImageDraw.Draw(hi_res_image)
        
        # Create low-res image (8px × 8px per matrix)
        low_res_width = 8 * self.MATRIX_COLS
        low_res_height = 8 * self.MATRIX_ROWS
        low_res_image = Image.new('RGB', (low_res_width, low_res_height), 'white')
        low_res_draw = ImageDraw.Draw(low_res_image)
        
        # Draw each rectangle in both resolutions
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                # High-res coordinates
                x1 = col * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                
                # Low-res coordinates (1:1 pixel mapping)
                lx1 = col
                ly1 = row
                lx2 = lx1 + 1
                ly2 = ly1 + 1
                
                rectangle = self.rectangles[row][col]
                color = self.canvas.itemcget(rectangle, 'fill')
                
                # Convert LED_COLOR back to white for saving
                if color == self.LED_COLOR:
                    color = 'white'
                
                # Draw in both images
                hi_res_draw.rectangle([x1, y1, x2, y2], fill=color)
                low_res_draw.rectangle([lx1, ly1, lx2, ly2], fill=color)
        
        # Save images with timestamp
        hi_res_filename = f"drawings/pixel_art_{timestamp}.png"
        low_res_filename = f"image-data/pixel_art_{timestamp}_{low_res_width}x{low_res_height}.png"
        
        hi_res_image.save(hi_res_filename)
        low_res_image.save(low_res_filename)
        print(f"Drawings saved as {hi_res_filename} and {low_res_filename}")

    def reset_grid(self):
        # Set all squares back to black
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                rectangle = self.rectangles[row][col]
                self.canvas.itemconfig(rectangle, fill='black')

def main():
    root = tk.Tk()
    app = PixelDrawer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
