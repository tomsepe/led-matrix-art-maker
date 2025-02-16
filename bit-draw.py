import tkinter as tk
from PIL import Image, ImageDraw
from datetime import datetime
import os

class PixelDrawer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Drawer")
        
        # Constants for the grid
        self.SQUARE_SIZE = 36
        self.GRID_WIDTH = 8  # squares
        self.GRID_HEIGHT = 24  # squares
        
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
        
        # Bind click event
        self.canvas.bind('<Button-1>', self.on_click)
        
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
        
        # Get the clicked rectangle
        rectangle = self.rectangles[row][col]
        
        # Toggle color
        current_color = self.canvas.itemcget(rectangle, 'fill')
        new_color = 'white' if current_color == 'black' else 'black'
        self.canvas.itemconfig(rectangle, fill=new_color)

    def save_drawing(self):
        # Create a new image with the same dimensions as the canvas
        image = Image.new('RGB', (self.GRID_WIDTH * self.SQUARE_SIZE, 
                                 self.GRID_HEIGHT * self.SQUARE_SIZE), 
                         'white')
        draw = ImageDraw.Draw(image)
        
        # Draw each rectangle in the current state
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                x1 = col * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                
                rectangle = self.rectangles[row][col]
                color = self.canvas.itemcget(rectangle, 'fill')
                
                draw.rectangle([x1, y1, x2, y2], fill=color)
        
        # Create 'drawings' directory if it doesn't exist
        if not os.path.exists('drawings'):
            os.makedirs('drawings')
            
        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"drawings/pixel_art_{timestamp}.png"
        image.save(filename)
        print(f"Drawing saved as {filename}")

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
            f.write("  pixelImg[][24] = {\n  { ")
            
            if not self.orientation_var.get():  # Unchecked = orientation 1
                self.save_orientation_1(f)
            else:  # Checked = orientation 2 (rotated)
                self.save_orientation_2(f)
            
            f.write(" },\n    };\n")
        
        print(f"Arduino format saved as {filename}")
    
    def save_orientation_1(self, f):
        # Original orientation
        for base_row in range(8):
            if base_row > 0:
                f.write("\n    ")
            
            for matrix in range(3):
                matrix_start_row = matrix * 8
                
                binary_number = 0
                for col in range(self.GRID_WIDTH):
                    actual_row = base_row + matrix_start_row
                    rectangle = self.rectangles[actual_row][col]
                    color = self.canvas.itemcget(rectangle, 'fill')
                    bit = 1 if color == 'white' else 0
                    binary_number |= (bit << (7 - col))
                
                binary_str = f"B{binary_number:08b}"
                f.write(binary_str)
                if not (base_row == 7 and matrix == 2):
                    f.write(", ")
    
    def save_orientation_2(self, f):
        # Current rotated orientation
        for base_row in range(7, -1, -1):
            if base_row < 7:
                f.write("\n    ")
            
            for matrix in range(3):
                matrix_start_row = matrix * 8
                
                binary_number = 0
                for bit_pos in range(8):
                    actual_row = matrix_start_row + (7 - bit_pos)
                    col = base_row
                    
                    rectangle = self.rectangles[actual_row][col]
                    color = self.canvas.itemcget(rectangle, 'fill')
                    bit = 1 if color == 'white' else 0
                    binary_number |= (bit << bit_pos)
                
                binary_str = f"B{binary_number:08b}"
                f.write(binary_str)
                if not (base_row == 0 and matrix == 2):
                    f.write(", ")

def main():
    root = tk.Tk()
    app = PixelDrawer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
