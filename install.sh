sudo ln -sf /home/pi/astro_camera/astro_cam.service /etc/systemd/system/astro_cam.service
sudo systemctl daemon-reload
sudo systemctl start astro_cam.service
sudo systemctl enable astro_cam.service
