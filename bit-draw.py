#!/usr/bin/env python3

import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageDraw
from datetime import datetime
import os

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
        self.rows.insert(0, "3")
        
        tk.Label(master, text="LED Color:").grid(row=3)
        self.led_colors = {
            'Red': '#FF0000',
            'Yellow-Green': '#9ACD32',
            'Blue': '#0000FF',
            'White': '#FFFFFF',
            'Yellow': '#FFFF00',
            'Green': '#00FF00',
            'Amber': '#FFBF00'
        }
        self.color_var = tk.StringVar(value='Red')
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
        self.GRID_WIDTH = 8 * self.MATRIX_COLS  # 8 pixels × number of columns
        self.GRID_HEIGHT = 8 * self.MATRIX_ROWS  # 8 pixels × number of rows
        
        # Create main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.main_frame,
            width=self.GRID_WIDTH * self.SQUARE_SIZE,
            height=self.GRID_HEIGHT * self.SQUARE_SIZE,
            bg='white'
        )
        self.canvas.pack()
        
        # Create button frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)
        
        # Create reset button
        self.reset_button = tk.Button(
            self.button_frame,
            text="Reset Grid",
            command=self.reset_grid
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Create save PNG button
        self.save_button = tk.Button(
            self.button_frame,
            text="Save as PNG",
            command=self.save_drawing
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        # Create save Arduino button
        self.save_arduino_button = tk.Button(
            self.button_frame,
            text="Save for Arduino",
            command=self.save_arduino_format
        )
        self.save_arduino_button.pack(side=tk.LEFT, padx=5)
        
        # Add orientation state
        self.orientation_var = tk.BooleanVar(value=False)  # Changed to False to start unchecked
        
        # Create orientation checkbox
        self.orientation_checkbox = tk.Checkbutton(
            self.button_frame,
            text="Rotate Output -90",
            variable=self.orientation_var,
            command=self.on_orientation_change
        )
        self.orientation_checkbox.pack(side=tk.LEFT, padx=5)
        
        # Store rectangle references
        self.rectangles = []
        
        # Create grid of black squares
        self.create_grid()
        
        # Bind click and drag events
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)  # Add drag binding
        
        # Add state to track the current drawing color
        self.current_draw_color = None
        
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

    def save_drawing(self):
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
        
        # Create 'drawings' directory if it doesn't exist
        if not os.path.exists('drawings'):
            os.makedirs('drawings')
            
        # Save both versions with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hi_res_filename = f"drawings/pixel_art_{timestamp}.png"
        low_res_filename = f"drawings/pixel_art_{timestamp}_8x8.png"
        
        hi_res_image.save(hi_res_filename)
        low_res_image.save(low_res_filename)
        print(f"Drawings saved as {hi_res_filename} and {low_res_filename}")

    def on_orientation_change(self):
        # The orientation_var.get() will return True for checked (rotated) and False for unchecked
        pass  # We don't need to do anything here since we'll check orientation_var.get() when saving
    
    def save_arduino_format(self):
        if not os.path.exists('arduino'):
            os.makedirs('arduino')
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"arduino/pixel_art_{timestamp}.h"
        
        with open(filename, 'w') as f:
            f.write("static uint8_t PROGMEM\n")
            f.write(f"  pixelImg[][{self.GRID_WIDTH}] = {{\n  {{ ")  # Updated array size
            
            if not self.orientation_var.get():
                self.save_orientation_1(f)
            else:
                self.save_orientation_2(f)
            
            f.write(" },\n    };\n")
        
        print(f"Arduino format saved as {filename}")
    
    def save_orientation_1(self, f):
        # Original orientation
        for base_row in range(8):
            if base_row > 0:
                f.write("\n    ")
            
            for matrix_row in range(self.MATRIX_ROWS):
                for matrix_col in range(self.MATRIX_COLS):
                    matrix_start_row = matrix_row * 8
                    matrix_start_col = matrix_col * 8
                    
                    binary_number = 0
                    for col in range(8):  # Process each column within the matrix
                        actual_row = base_row + matrix_start_row
                        actual_col = col + matrix_start_col
                        rectangle = self.rectangles[actual_row][actual_col]
                        color = self.canvas.itemcget(rectangle, 'fill')
                        bit = 1 if color == self.LED_COLOR else 0
                        binary_number |= (bit << (7 - col))
                    
                    binary_str = f"B{binary_number:08b}"
                    f.write(binary_str)
                    # Add comma if not the last number
                    if not (base_row == 7 and matrix_row == self.MATRIX_ROWS-1 
                           and matrix_col == self.MATRIX_COLS-1):
                        f.write(", ")
    
    def save_orientation_2(self, f):
        # Rotated orientation
        for base_row in range(7, -1, -1):
            if base_row < 7:
                f.write("\n    ")
            
            for matrix_row in range(self.MATRIX_ROWS):
                for matrix_col in range(self.MATRIX_COLS):
                    matrix_start_row = matrix_row * 8
                    matrix_start_col = matrix_col * 8
                    
                    binary_number = 0
                    for bit_pos in range(8):
                        actual_row = matrix_start_row + (7 - bit_pos)
                        actual_col = base_row + matrix_start_col
                        
                        rectangle = self.rectangles[actual_row][actual_col]
                        color = self.canvas.itemcget(rectangle, 'fill')
                        bit = 1 if color == self.LED_COLOR else 0
                        binary_number |= (bit << bit_pos)
                    
                    binary_str = f"B{binary_number:08b}"
                    f.write(binary_str)
                    if not (base_row == 0 and matrix_row == self.MATRIX_ROWS-1 
                           and matrix_col == self.MATRIX_COLS-1):
                        f.write(", ")

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
