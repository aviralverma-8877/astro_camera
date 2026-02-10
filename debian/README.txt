Astro Camera - Debian Package Files
====================================

This directory contains files used to build the Debian package (.deb).

Files:
------
control         - Package metadata, dependencies, description
postinst        - Post-installation script (runs after package install)
prerm           - Pre-removal script (runs before package removal)
postrm          - Post-removal script (runs after package removal)
astro_cam.service - Systemd service file

Building:
---------
From the project root, run:
    ./build-deb.sh

This creates: astro-camera_2.0.0_armhf.deb

Installing:
-----------
    sudo apt install ./astro-camera_2.0.0_armhf.deb

For more information, see PACKAGING.md
