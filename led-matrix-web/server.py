import http.server
import socketserver
import os
import webbrowser

def run_server(port=8000):
    # Create web-drawings folder if it doesn't exist
    if not os.path.exists('web-drawings'):
        os.makedirs('web-drawings')
        print("Created 'web-drawings' folder")

    # Start the server
    try:
        with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"\nServer running at http://localhost:{port}")
            print("Press Ctrl+C to stop the server")
            
            # Open the browser
            webbrowser.open(f'http://localhost:{port}')
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nServer stopped.")
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"Port {port} is already in use. Trying port {port + 1}")
            run_server(port + 1)
        else:
            raise

if __name__ == '__main__':
    run_server() 