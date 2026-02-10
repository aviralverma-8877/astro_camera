from flask import Flask, render_template, Response, jsonify, request
import logging
import time

logger = logging.getLogger(__name__)

def create_app(menu_obj, camera_output):
    """
    Create and configure Flask application

    Args:
        menu_obj: Menu object containing camera settings
        camera_output: StreamingOutput instance for MJPEG streaming

    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'astro_camera_secret'

    # Store references for route access
    app.menu_obj = menu_obj
    app.camera_output = camera_output

    def generate_frames():
        """Generator function for MJPEG streaming"""
        if not app.camera_output:
            logger.error("No camera output available")
            return

        while True:
            try:
                with app.camera_output.condition:
                    app.camera_output.condition.wait()
                    frame = app.camera_output.frame

                if frame:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                else:
                    time.sleep(0.1)

            except Exception as e:
                logger.error(f"Error generating frame: {e}")
                time.sleep(0.1)

    @app.route('/')
    def index():
        """Render main web interface"""
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed():
        """MJPEG video stream endpoint"""
        return Response(
            generate_frames(),
            mimetype='multipart/x-mixed-replace; boundary=frame'
        )

    @app.route('/api/settings', methods=['GET'])
    def get_settings():
        """
        Get current camera settings

        Returns:
            JSON with ISO, shutter, output format, image time, image count
        """
        try:
            menu = app.menu_obj.menu

            # Get current settings
            iso_value = menu[0]["options"][menu[0]["current-option"]]
            shutter_value = menu[1]["options"][menu[1]["current-option"]]
            output_value = menu[4]["options"][menu[4]["current-option"]]
            image_time_value = menu[3]["options"][menu[3]["current-option"]]
            image_count_value = menu[5]["options"][menu[5]["current-option"]]

            settings = {
                'iso': {
                    'value': iso_value,
                    'index': menu[0]["current-option"],
                    'options': menu[0]["options"]
                },
                'shutter': {
                    'value': shutter_value,
                    'index': menu[1]["current-option"],
                    'options': menu[1]["options"]
                },
                'output': {
                    'value': output_value,
                    'index': menu[4]["current-option"],
                    'options': menu[4]["options"]
                },
                'image_time': {
                    'value': image_time_value,
                    'index': menu[3]["current-option"],
                    'options': menu[3]["options"]
                },
                'image_count': {
                    'value': image_count_value,
                    'index': menu[5]["current-option"],
                    'options': menu[5]["options"]
                }
            }

            return jsonify(settings)

        except Exception as e:
            logger.error(f"Error getting settings: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/settings', methods=['POST'])
    def update_settings():
        """
        Update camera settings

        Expected JSON body:
        {
            "setting": "iso" | "shutter" | "output" | "image_time" | "image_count",
            "index": <option_index>
        }

        Returns:
            JSON with success status
        """
        try:
            data = request.get_json()

            if not data or 'setting' not in data or 'index' not in data:
                return jsonify({'error': 'Missing setting or index'}), 400

            setting = data['setting']
            index = int(data['index'])

            menu = app.menu_obj.menu

            # Map setting names to menu indices
            setting_map = {
                'iso': 0,
                'shutter': 1,
                'output': 4,
                'image_time': 3,
                'image_count': 5
            }

            if setting not in setting_map:
                return jsonify({'error': f'Unknown setting: {setting}'}), 400

            menu_index = setting_map[setting]

            # Validate index
            if index < 0 or index >= len(menu[menu_index]["options"]):
                return jsonify({'error': 'Index out of range'}), 400

            # Update setting
            menu[menu_index]["current-option"] = index

            # Get new value
            new_value = menu[menu_index]["options"][index]

            logger.info(f"Updated {setting} to {new_value} (index {index})")

            return jsonify({
                'success': True,
                'setting': setting,
                'value': new_value,
                'index': index
            })

        except Exception as e:
            logger.error(f"Error updating settings: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/capture', methods=['POST'])
    def start_capture():
        """
        Trigger image capture

        Returns:
            JSON with success status
        """
        try:
            # Stop web preview temporarily
            if app.menu_obj.web_server_running:
                logger.info("Stopping web preview for capture")
                if app.menu_obj.web_encoder:
                    app.menu_obj.camera.stop_web_preview(app.menu_obj.web_encoder)

            # Start capture
            logger.info("Starting capture from web interface")
            # Use existing capture method
            # Note: This will run in the main thread, blocking the web server
            # For production, this should be done in a background thread
            app.menu_obj.camera.capture(app.menu_obj)

            # Restart web preview
            if app.menu_obj.web_server_running:
                logger.info("Restarting web preview after capture")
                app.menu_obj.web_output, app.menu_obj.web_encoder = app.menu_obj.camera.start_web_preview(app.menu_obj)
                app.camera_output = app.menu_obj.web_output

            return jsonify({
                'success': True,
                'message': 'Capture completed'
            })

        except Exception as e:
            logger.error(f"Error during capture: {e}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/status', methods=['GET'])
    def get_status():
        """
        Get system status

        Returns:
            JSON with system information
        """
        try:
            menu = app.menu_obj.menu

            status = {
                'wifi_ap': 'active',
                'camera': 'streaming' if app.camera_output else 'inactive',
                'capturing': app.menu_obj.previewing if hasattr(app.menu_obj, 'previewing') else False,
                'current_menu': menu[0]["head"] if menu else 'Unknown'
            }

            return jsonify(status)

        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return jsonify({'error': str(e)}), 500

    return app
