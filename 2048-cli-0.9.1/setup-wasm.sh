#!/bin/bash
# Setup script for WebAssembly build tools

echo "=== WASM Build Tools Setup ==="
echo ""

# Detect OS
OS=$(uname -s)

if [ "$OS" = "Darwin" ]; then
    echo "macOS detected. Installing via Homebrew..."
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Error: Homebrew not found. Please install from https://brew.sh"
        exit 1
    fi
    
    echo "Installing Emscripten..."
    brew install emscripten
    
    echo "Installing additional WASM tools..."
    brew install wabt  # WebAssembly Binary Toolkit
    
elif [ "$OS" = "Linux" ]; then
    echo "Linux detected. Installing Emscripten..."
    
    # Check for package manager
    if command -v apt-get &> /dev/null; then
        echo "Using apt-get..."
        sudo apt-get update
        sudo apt-get install -y emscripten
    elif command -v yum &> /dev/null; then
        echo "Using yum..."
        sudo yum install -y emscripten
    else
        echo "Manual installation required. Visit https://emscripten.org/docs/getting_started/downloads.html"
        exit 1
    fi
    
elif [ "$OS" = "FreeBSD" ] || [ "$OS" = "OpenBSD" ] || [ "$OS" = "NetBSD" ]; then
    echo "BSD detected. Checking ports..."
    
    if [ -d "/usr/ports" ]; then
        echo "Ports tree found. Install with:"
        echo "  cd /usr/ports/devel/emscripten && make install clean"
    else
        echo "Using pkg..."
        sudo pkg install emscripten
    fi
    
else
    echo "Unsupported OS: $OS"
    echo "Please install Emscripten manually from https://emscripten.org"
    exit 1
fi

echo ""
echo "Verifying installation..."

if command -v emcc &> /dev/null; then
    echo "✓ emcc found: $(emcc --version | head -1)"
else
    echo "✗ emcc not found in PATH"
fi

if command -v wasm-objdump &> /dev/null; then
    echo "✓ wabt found: $(wasm-objdump --version)"
else
    echo "✗ wabt tools not found"
fi

echo ""
echo "Setup complete! You can now build with: make wasm"