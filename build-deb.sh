#!/bin/bash
#
# Debian Package Build Script for Astro Camera
# Creates a .deb package for easy installation on Raspberry Pi OS
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Package information
PACKAGE_NAME="astro-camera"
PACKAGE_VERSION="2.0.0"
PACKAGE_ARCH="armhf"
PACKAGE_DIR="${PACKAGE_NAME}_${PACKAGE_VERSION}_${PACKAGE_ARCH}"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}==>${NC} $1"
}

# Check if running on Linux (required for dpkg-deb)
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    log_warn "This script is designed to run on Linux (Raspberry Pi OS)"
    log_warn "If running on Windows/Mac, consider using WSL or a Linux VM"
fi

# Check for required commands
for cmd in dpkg-deb; do
    if ! command -v $cmd &> /dev/null; then
        log_error "$cmd is required but not installed. Install with: sudo apt install dpkg"
        exit 1
    fi
done

# Start build process
log_step "Building Astro Camera Debian Package v${PACKAGE_VERSION}"
echo ""

# Clean previous build
if [ -d "$PACKAGE_DIR" ]; then
    log_info "Cleaning previous build..."
    rm -rf "$PACKAGE_DIR"
fi

if [ -f "${PACKAGE_DIR}.deb" ]; then
    log_info "Removing previous .deb file..."
    rm -f "${PACKAGE_DIR}.deb"
fi

# Create package directory structure
log_step "Creating package directory structure..."
mkdir -p "$PACKAGE_DIR/DEBIAN"
mkdir -p "$PACKAGE_DIR/opt/astro_camera"
mkdir -p "$PACKAGE_DIR/etc/systemd/system"
mkdir -p "$PACKAGE_DIR/usr/share/doc/astro-camera"

# Copy application files
log_step "Copying application files..."

# Copy Python modules and scripts
log_info "Copying Python modules..."
cp -r Buttons "$PACKAGE_DIR/opt/astro_camera/"
cp -r Camera "$PACKAGE_DIR/opt/astro_camera/"
cp -r Display "$PACKAGE_DIR/opt/astro_camera/"
cp -r Functions "$PACKAGE_DIR/opt/astro_camera/"
cp -r WebInterface "$PACKAGE_DIR/opt/astro_camera/"
cp -r fonts "$PACKAGE_DIR/opt/astro_camera/"
cp -r images "$PACKAGE_DIR/opt/astro_camera/"

# Copy main scripts
log_info "Copying main scripts..."
cp main "$PACKAGE_DIR/opt/astro_camera/"
cp logging_config.py "$PACKAGE_DIR/opt/astro_camera/"
cp GPIO_Compat.py "$PACKAGE_DIR/opt/astro_camera/"

# Copy documentation
log_info "Copying documentation..."
cp README.md "$PACKAGE_DIR/usr/share/doc/astro-camera/"
if [ -f LICENSE ]; then
    cp LICENSE "$PACKAGE_DIR/usr/share/doc/astro-camera/"
fi

# Copy systemd service file
log_info "Copying systemd service..."
cp debian/astro_cam.service "$PACKAGE_DIR/etc/systemd/system/"

# Copy DEBIAN control files
log_step "Setting up package metadata..."
cp debian/control "$PACKAGE_DIR/DEBIAN/"
cp debian/postinst "$PACKAGE_DIR/DEBIAN/"
cp debian/prerm "$PACKAGE_DIR/DEBIAN/"
cp debian/postrm "$PACKAGE_DIR/DEBIAN/"

# Set permissions
log_step "Setting file permissions..."
chmod 755 "$PACKAGE_DIR/opt/astro_camera/main"
chmod 755 "$PACKAGE_DIR/DEBIAN/postinst"
chmod 755 "$PACKAGE_DIR/DEBIAN/prerm"
chmod 755 "$PACKAGE_DIR/DEBIAN/postrm"
chmod 644 "$PACKAGE_DIR/etc/systemd/system/astro_cam.service"

# Set ownership to root (required for proper package installation)
log_info "Setting ownership to root..."
if [ "$EUID" -eq 0 ]; then
    chown -R root:root "$PACKAGE_DIR"
else
    log_warn "Not running as root - ownership may need adjustment"
    log_warn "Consider running: sudo chown -R root:root $PACKAGE_DIR"
fi

# Calculate installed size
log_step "Calculating package size..."
INSTALLED_SIZE=$(du -sk "$PACKAGE_DIR" | cut -f1)
echo "Installed-Size: $INSTALLED_SIZE" >> "$PACKAGE_DIR/DEBIAN/control"

# Build the package
log_step "Building .deb package..."
dpkg-deb --build --root-owner-group "$PACKAGE_DIR"

if [ $? -eq 0 ]; then
    echo ""
    log_step "✓ Package built successfully!"
    echo ""
    log_info "Package: ${GREEN}${PACKAGE_DIR}.deb${NC}"
    log_info "Size: $(du -h ${PACKAGE_DIR}.deb | cut -f1)"
    echo ""

    # Package information
    log_step "Package Information:"
    dpkg-deb --info "${PACKAGE_DIR}.deb" | grep -E "Package|Version|Architecture|Installed-Size|Description" | head -5
    echo ""

    # Installation instructions
    log_step "Installation Instructions:"
    echo ""
    echo "  To install on Raspberry Pi:"
    echo "    ${BLUE}sudo apt install ./${PACKAGE_DIR}.deb${NC}"
    echo ""
    echo "  Or using dpkg:"
    echo "    ${BLUE}sudo dpkg -i ${PACKAGE_DIR}.deb${NC}"
    echo "    ${BLUE}sudo apt-get install -f${NC}  # Install dependencies"
    echo ""
    echo "  To remove:"
    echo "    ${BLUE}sudo apt remove astro-camera${NC}"
    echo ""
    echo "  To purge (including logs):"
    echo "    ${BLUE}sudo apt purge astro-camera${NC}"
    echo ""

    # Distribution instructions
    log_step "Distribution:"
    echo ""
    echo "  Upload to GitHub Releases:"
    echo "    https://github.com/aviralverma-8877/astro_camera/releases"
    echo ""
    echo "  Users can then install with:"
    echo "    ${BLUE}wget https://github.com/aviralverma-8877/astro_camera/releases/download/v${PACKAGE_VERSION}/${PACKAGE_DIR}.deb${NC}"
    echo "    ${BLUE}sudo apt install ./${PACKAGE_DIR}.deb${NC}"
    echo ""

    # Clean up build directory
    log_info "Cleaning up build directory..."
    rm -rf "$PACKAGE_DIR"

    log_step "Done! Package ready for distribution."
    echo ""
else
    log_error "Package build failed!"
    exit 1
fi
