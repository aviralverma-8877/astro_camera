import threading
import logging
from flask import Flask
from werkzeug.serving import make_server

logger = logging.getLogger(__name__)

class WebInterface:
    """Web interface for remote camera control and preview"""

    def __init__(self, menu_obj):
        """
        Initialize web interface

        Args:
            menu_obj: Menu object containing camera settings and controls
        """
        self.menu_obj = menu_obj
        self.app = None
        self.server = None
        self.server_thread = None
        self.running = False
        self.camera_output = None

    def set_camera_output(self, output):
        """
        Set the camera output stream for MJPEG streaming

        Args:
            output: StreamingOutput instance from Camera class
        """
        self.camera_output = output

    def create_app(self):
        """Create and configure Flask application"""
        from WebInterface.server import create_app
        return create_app(self.menu_obj, self.camera_output)

    def start(self):
        """Start Flask web server in background thread"""
        if self.running:
            logger.warning("Web interface already running")
            return

        try:
            # Create Flask app
            self.app = self.create_app()

            # Create server
            self.server = make_server('0.0.0.0', 5000, self.app, threaded=True)

            # Start server in background thread
            self.server_thread = threading.Thread(target=self._run_server, daemon=True)
            self.server_thread.start()

            self.running = True
            logger.info("Web interface started on port 5000")

        except Exception as e:
            logger.error(f"Failed to start web interface: {e}")
            raise

    def _run_server(self):
        """Internal method to run server in thread"""
        try:
            self.server.serve_forever()
        except Exception as e:
            logger.error(f"Server error: {e}")

    def stop(self):
        """Stop Flask web server"""
        if not self.running:
            logger.warning("Web interface not running")
            return

        try:
            if self.server:
                self.server.shutdown()

            if self.server_thread:
                self.server_thread.join(timeout=5)

            self.running = False
            self.app = None
            self.server = None
            self.server_thread = None

            logger.info("Web interface stopped")

        except Exception as e:
            logger.error(f"Failed to stop web interface: {e}")
            raise
