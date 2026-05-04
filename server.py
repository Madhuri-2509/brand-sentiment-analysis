import http.server
import socketserver
import os

PORT = 8000
# This finds the 'dashboard' folder where your HTML and JS live
base_path = r"C:\Users\madhu\OneDrive\Brand_Perception_Analysis_System"
dashboard_dir = os.path.join(base_path, "dashboard")

# Change the "active directory" to the dashboard folder
if os.path.exists(dashboard_dir):
    os.chdir(dashboard_dir)
    Handler = http.server.SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 DASHBOARD IS LIVE!")
        print(f"👉 Open your browser and go to: http://localhost:{PORT}")
        print("--- Press Ctrl+C in this terminal to stop the server ---")
        httpd.serve_forever()
else:
    print(f"❌ ERROR: Cannot find the 'dashboard' folder at {dashboard_dir}")