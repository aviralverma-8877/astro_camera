# Debian Package Build Guide

This guide explains how to build and distribute the Astro Camera Debian package (.deb file).

## Overview

The Debian package system allows users to install Astro Camera with a single command:
```bash
sudo apt install ./astro-camera_2.0.0_armhf.deb
```

This automatically handles:
- ✓ Dependency installation
- ✓ File placement in correct directories
- ✓ Service configuration
- ✓ Permission setup
- ✓ SPI interface enabling
- ✓ Directory creation

## Prerequisites

### Build System Requirements

To build the package, you need:
- **Linux system** (Raspberry Pi OS, Ubuntu, Debian, or WSL on Windows)
- **dpkg-deb** tool (usually pre-installed on Debian/Ubuntu)
- **Git** (to clone the repository)

Install build tools if needed:
```bash
sudo apt update
sudo apt install dpkg git
```

### Package Structure

The package contains:
```
astro-camera_2.0.0_armhf.deb
├── DEBIAN/
│   ├── control       # Package metadata and dependencies
│   ├── postinst      # Post-installation script (runs after install)
│   ├── prerm         # Pre-removal script (runs before uninstall)
│   └── postrm        # Post-removal script (runs after uninstall)
├── opt/astro_camera/ # Application files (Python modules, scripts)
├── etc/systemd/system/
│   └── astro_cam.service  # Systemd service file
└── usr/share/doc/astro-camera/
    ├── README.md     # Documentation
    └── LICENSE       # License file (if present)
```

## Building the Package

### Method 1: Using the Build Script (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aviralverma-8877/astro_camera.git
   cd astro_camera
   ```

2. **Make the build script executable:**
   ```bash
   chmod +x build-deb.sh
   ```

3. **Run the build script:**
   ```bash
   ./build-deb.sh
   ```

   The script will:
   - Create the package directory structure
   - Copy all necessary files
   - Set proper permissions
   - Build the .deb package
   - Display installation instructions

4. **Output:**
   ```
   astro-camera_2.0.0_armhf.deb  (ready for distribution)
   ```

### Method 2: Manual Build

If you need to customize the build process:

```bash
# 1. Create package structure
PACKAGE="astro-camera_2.0.0_armhf"
mkdir -p "$PACKAGE/DEBIAN"
mkdir -p "$PACKAGE/opt/astro_camera"
mkdir -p "$PACKAGE/etc/systemd/system"
mkdir -p "$PACKAGE/usr/share/doc/astro-camera"

# 2. Copy application files
cp -r Buttons Camera Display Functions fonts images "$PACKAGE/opt/astro_camera/"
cp main logging_config.py GPIO_Compat.py "$PACKAGE/opt/astro_camera/"

# 3. Copy control files
cp debian/control debian/postinst debian/prerm debian/postrm "$PACKAGE/DEBIAN/"
cp debian/astro_cam.service "$PACKAGE/etc/systemd/system/"

# 4. Copy documentation
cp README.md "$PACKAGE/usr/share/doc/astro-camera/"

# 5. Set permissions
chmod 755 "$PACKAGE/opt/astro_camera/main"
chmod 755 "$PACKAGE/DEBIAN/postinst"
chmod 755 "$PACKAGE/DEBIAN/prerm"
chmod 755 "$PACKAGE/DEBIAN/postrm"
chmod 644 "$PACKAGE/etc/systemd/system/astro_cam.service"

# 6. Set ownership (if running as root)
sudo chown -R root:root "$PACKAGE"

# 7. Build package
dpkg-deb --build --root-owner-group "$PACKAGE"

# Result: astro-camera_2.0.0_armhf.deb
```

## Testing the Package

### Local Installation Test

**On a Raspberry Pi:**

1. **Install the package:**
   ```bash
   sudo apt install ./astro-camera_2.0.0_armhf.deb
   ```

2. **Check service status:**
   ```bash
   sudo systemctl status astro_cam.service
   ```

3. **View logs:**
   ```bash
   sudo journalctl -u astro_cam.service -f
   ```

4. **Test functionality:**
   - Physical buttons should respond
   - Display should show menu
   - Camera should capture images

5. **Verify installation:**
   ```bash
   dpkg -L astro-camera  # List installed files
   dpkg -s astro-camera  # Show package status
   ```

### Package Verification

**Inspect package contents:**
```bash
dpkg-deb --contents astro-camera_2.0.0_armhf.deb
```

**Check package info:**
```bash
dpkg-deb --info astro-camera_2.0.0_armhf.deb
```

**Validate package:**
```bash
lintian astro-camera_2.0.0_armhf.deb  # Check for common issues
```

## Distribution

### GitHub Releases (Recommended)

1. **Create a new release on GitHub:**
   - Go to: https://github.com/aviralverma-8877/astro_camera/releases/new
   - Tag version: `v2.0.0`
   - Release title: `Astro Camera v2.0.0`
   - Description: Changelog and features

2. **Upload the .deb file:**
   - Attach `astro-camera_2.0.0_armhf.deb` to the release

3. **Users can install with:**
   ```bash
   # Download
   wget https://github.com/aviralverma-8877/astro_camera/releases/download/v2.0.0/astro-camera_2.0.0_armhf.deb

   # Install
   sudo apt install ./astro-camera_2.0.0_armhf.deb
   ```

### Alternative Distribution Methods

**1. Host on a web server:**
```bash
# Users download and install
wget https://yourserver.com/packages/astro-camera_2.0.0_armhf.deb
sudo apt install ./astro-camera_2.0.0_armhf.deb
```

**2. Create an APT repository:**

For advanced users wanting automatic updates, create a full APT repository:
```bash
# Set up repository structure
mkdir -p repo/pool/main
cp astro-camera_2.0.0_armhf.deb repo/pool/main/

# Generate Packages file
cd repo
dpkg-scanpackages pool /dev/null > pool/Packages
gzip -k pool/Packages

# Generate Release file
apt-ftparchive release pool > pool/Release

# Sign with GPG (optional but recommended)
gpg --armor --detach-sign -o pool/Release.gpg pool/Release
```

Users add repository:
```bash
echo "deb [trusted=yes] https://yourserver.com/repo pool/" | sudo tee /etc/apt/sources.list.d/astro-camera.list
sudo apt update
sudo apt install astro-camera
```

## Package Management

### Installation

**Standard installation:**
```bash
sudo apt install ./astro-camera_2.0.0_armhf.deb
```

**Force dependency resolution:**
```bash
sudo dpkg -i astro-camera_2.0.0_armhf.deb
sudo apt-get install -f  # Fix broken dependencies
```

### Upgrade

**Upgrade to newer version:**
```bash
sudo apt install ./astro-camera_2.1.0_armhf.deb
```

The package system handles:
- Stopping the old version service
- Replacing files
- Restarting with new version
- Preserving configuration and data

### Removal

**Remove package (keep configuration):**
```bash
sudo apt remove astro-camera
```

**Purge package (remove everything except images):**
```bash
sudo apt purge astro-camera
```

**Manual image cleanup:**
```bash
sudo rm -rf /mnt/astro_camera_storage
```

## Customization

### Changing Package Version

Edit `debian/control`:
```
Version: 2.1.0
```

Update `build-deb.sh`:
```bash
PACKAGE_VERSION="2.1.0"
```

### Adding Dependencies

Edit `debian/control`:
```
Depends: python3 (>= 3.7), python3-pil, python3-numpy, your-new-dependency
Recommends: python3-lgpio, your-optional-dependency
Suggests: samba, your-suggested-package
```

### Modifying Installation Behavior

Edit `debian/postinst`:
```bash
# Add custom installation steps
echo "Running custom setup..."
your-custom-command
```

### Adding Configuration Files

1. Create config file: `debian/astro_camera.conf`

2. Update `build-deb.sh`:
   ```bash
   mkdir -p "$PACKAGE_DIR/etc/astro_camera"
   cp debian/astro_camera.conf "$PACKAGE_DIR/etc/astro_camera/"
   ```

3. Mark as conffile in `debian/control`:
   ```
   Conffiles: /etc/astro_camera/astro_camera.conf
   ```

## Troubleshooting

### Build Errors

**Error: dpkg-deb: command not found**
```bash
sudo apt install dpkg
```

**Error: Permission denied**
```bash
chmod +x build-deb.sh
./build-deb.sh
```

**Error: Cannot set ownership**
- Run build script with sudo to set root ownership
- Or set ownership manually after build:
  ```bash
  sudo chown -R root:root astro-camera_2.0.0_armhf/
  dpkg-deb --build --root-owner-group astro-camera_2.0.0_armhf
  ```

### Installation Errors

**Error: Dependency problems**
```bash
sudo apt update
sudo apt install -f  # Fix broken dependencies
```

**Error: Package is not installed**
```bash
# Check if already installed
dpkg -l | grep astro-camera

# Remove completely and reinstall
sudo apt purge astro-camera
sudo apt install ./astro-camera_2.0.0_armhf.deb
```

**Error: Service fails to start**
```bash
# Check logs
sudo journalctl -u astro_cam.service -n 50

# Check permissions
ls -la /opt/astro_camera/main

# Verify Python dependencies
python3 -c "import picamera2; import RPi.GPIO"
```

## Best Practices

### Version Numbering

Follow semantic versioning: `MAJOR.MINOR.PATCH`
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Example: `2.0.0` → `2.1.0` (new feature) → `2.1.1` (bug fix)

### Testing Checklist

Before releasing a package:

- [ ] Build completes without errors
- [ ] Package installs cleanly on fresh Pi
- [ ] Service starts automatically after reboot
- [ ] All dependencies are declared correctly
- [ ] Application functions as expected
- [ ] Package removes cleanly
- [ ] Documentation is up-to-date
- [ ] Version numbers are correct

### Release Checklist

- [ ] Update version in `debian/control`
- [ ] Update version in `build-deb.sh`
- [ ] Update `README.md` with new version
- [ ] Build package
- [ ] Test on multiple Pi models (Pi 4, Pi 5, Zero)
- [ ] Create GitHub release
- [ ] Upload .deb to release
- [ ] Update installation instructions
- [ ] Announce release

## Advanced Topics

### Multi-Architecture Support

To build for different architectures:

**For arm64 (64-bit Raspberry Pi OS):**
```bash
# Update control file
Architecture: arm64

# Build
dpkg-deb --build astro-camera_2.0.0_arm64
```

**For all architectures:**
```bash
Architecture: all  # For pure Python packages
```

### Package Signing

Sign packages with GPG for security:

```bash
# Generate GPG key (if needed)
gpg --gen-key

# Sign package
dpkg-sig --sign builder astro-camera_2.0.0_armhf.deb

# Verify signature
dpkg-sig --verify astro-camera_2.0.0_armhf.deb
```

### Automated Builds

Use CI/CD to automatically build packages:

**GitHub Actions example:**
```yaml
name: Build Debian Package
on: [push, release]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build package
        run: ./build-deb.sh
      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: debian-package
          path: '*.deb'
```

## Resources

- [Debian Policy Manual](https://www.debian.org/doc/debian-policy/)
- [Debian New Maintainers' Guide](https://www.debian.org/doc/manuals/maint-guide/)
- [dpkg-deb man page](https://manpages.debian.org/dpkg-deb)
- [Debian Package Format](https://wiki.debian.org/Packaging)
- [Lintian Documentation](https://lintian.debian.org/)

---

**Questions or Issues?**

Open an issue on GitHub: https://github.com/aviralverma-8877/astro_camera/issues
