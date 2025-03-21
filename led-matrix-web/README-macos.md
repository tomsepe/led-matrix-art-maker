# LED Matrix Art Maker

A simple, browser-based tool for creating 8x8 LED matrix art. Perfect for designing patterns for LED matrix displays.

## Setup

1. Start the server:
   ```bash
   # First, find where you downloaded/extracted the LED Matrix Art Maker:
   # - If you received it by email, check your Downloads folder
   # - The folder should be named "led-matrix-web.zip"
   # - Double-click on the file to extract it
   
   # Open Terminal (Cmd + Space, type "terminal", press Enter)
   # Type "cd " (with a space after cd)
   # Drag and drop the "led-matrix-web" folder from Finder into Terminal
   # Press Enter
   # Then type:
   python server.py
   ```

2. The application will automatically:
   - Create the `web-drawings` folder if it doesn't exist
   - Start the server at [http://localhost:8000](http://localhost:8000)
   - Open your default web browser to the application

## Features

- 8x8 LED grid
- 7 color options:
  - White
  - Red
  - Green
  - Blue
  - Yellow
  - Orange
  - Pink
- Click to toggle LEDs on/off
- Save designs as PNG images
- Live gallery view of saved designs
- Reset functionality
- Dark theme interface

## Usage

1. Start the server as described in Setup
2. Click on grid squares to toggle LEDs on/off
3. Select colors from the color palette below the grid
4. To save your design as an image:
   - Click the "Save Image" button
   - When the modal appears, right-click on the image
   - Select "Save image as..."
   - **Important:** Save to the 'web-drawings' folder in your LED Matrix Art Maker directory
   - Click Save
   - The image will appear in the gallery automatically
5. View your saved designs in the gallery on the right
6. Use the Reset button to clear the grid

## File Structure
```
led-matrix-web/
├── index.html          # Main application file
├── server.py          # Python server script
├── README.md          # This documentation
└── web-drawings/      # Directory for saved images
    └── *.png         # Your saved LED matrix designs
```

### Image Export
- Format: PNG
- Resolution: 288x288 pixels (8x8 grid with 36px per LED)
- Black background
- Anti-aliased rendering
- Filename format: Based on save timestamp

## Gallery Features

- Real-time display of saved designs
- 4-column grid layout
- Hover effects on images
- Scrollable interface
- Maintains aspect ratio of designs
- Auto-refreshes when new images are saved

## Browser Compatibility

Works in all modern browsers:
- Chrome
- Firefox
- Safari
- Edge

## Troubleshooting

1. If the gallery is empty:
   - Make sure the Python server is running
   - Verify you're accessing via http://localhost:8000
   - Check that images exist in the web-drawings folder

2. If images won't save:
   - Ensure the web-drawings folder exists
   - Make sure you have write permissions for the folder

3. If the server won't start:
   - Try a different port: `python server.py 8080`
   - Check if another process is using port 8000
