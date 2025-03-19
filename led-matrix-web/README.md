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
- Reset functionality
- Dark theme interface
- No installation required

## Usage

1. Simply open `index.html` in any modern web browser
2. Click on grid squares to toggle LEDs on/off
3. Select colors from the color palette below the grid
4. Use the Export button to save your design as a JSON file
5. Use the Reset button to clear the grid

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

## Export Format

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
