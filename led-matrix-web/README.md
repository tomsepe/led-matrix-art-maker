# LED Matrix Art Maker

A simple, browser-based tool for creating 8x8 LED matrix art. Perfect for designing patterns for LED matrix displays.

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
- Export designs as JSON
- Save designs as PNG images
- Live gallery view of saved designs
- Delete saved designs from gallery
- Reset functionality
- Dark theme interface
- No installation required

## Usage

1. Simply open `index.html` in any modern web browser
2. Click on grid squares to toggle LEDs on/off
3. Select colors from the color palette below the grid
4. Use the Export button to save your design as a JSON file
5. To save your design as an image:
   - Click the "Save Image" button
   - When the browser's save dialog appears, right-click on the image
   - Select "Save image as..."
   - Navigate to your desired save location (e.g., a 'drawings' folder)
   - Click Save
   - The image will appear in the gallery once saved in the correct location
6. View your saved designs in the gallery on the right
7. Hover over gallery images to reveal delete button
8. Use the Reset button to clear the grid

## Running Locally

You can run this app in several ways:

1. **Direct File Opening:**
   - Simply double-click the `index.html` file to open in your browser

2. **Using Python's HTTP Server:**
   ```bash
   python -m http.server 3000
   ```
   Then visit `http://localhost:3000`

3. **Using any other static file server:**
   - Node's `http-server`
   - PHP's built-in server
   - Any web server (Apache, Nginx, etc.)

## Export Formats

### JSON Export
The exported JSON file contains:
```json
{
  "matrix": [
    [{"on": false, "color": "#FFFFFF"}, ...],
    ...
  ],
  "timestamp": "2024-03-19T18:00:00.000Z",
  "size": 8
}
```

### Image Export
- Format: PNG
- Resolution: 640x640 pixels (8x8 grid with 80px per LED)
- High-quality anti-aliased rendering
- Transparent background option
- Filename format: `pixel-art-TIMESTAMP.png`

## Gallery Features

- Real-time display of saved designs
- 2-column grid layout
- Hover effects on images
- Quick delete functionality
- Scrollable interface
- Maintains aspect ratio of designs

## Sharing

To share this tool with others:
1. Send them the `index.html` file
2. Host it on any static file hosting service (GitHub Pages, Netlify, etc.)
3. They can open it directly in their browser without installing anything

## Browser Compatibility

Works in all modern browsers:
- Chrome
- Firefox
- Safari
- Edge
