# WebAssembly Build Guide

## Prerequisites

Install Emscripten SDK:

```bash
# macOS
brew install emscripten

# Or run the setup script
./setup-wasm.sh
```

## Building

```bash
# Production build
make wasm

# Debug build with assertions
make wasm-debug
```

This creates:
- `2048.js` - JavaScript wrapper
- `2048.wasm` - WebAssembly binary

## Running

1. Start a local web server:
   ```bash
   python3 -m http.server 8000
   # or
   npx http-server .
   ```

2. Open `web/index.html` in your browser

## Architecture

The WASM build uses:
- `src/gfx_web.c` - Browser-specific graphics implementation
- Emscripten's HTML5 API for input handling
- JavaScript for UI and debugging tools

## Debugging

The web interface includes:
- Memory dump visualization
- Game state inspection
- Board layout display
- Step-by-step execution

## Known Limitations

- No file I/O (highscores use localStorage)
- Synchronous input model needs adaptation
- Terminal animations not supported

## TODO

- [ ] Complete input handling
- [ ] Implement game reset
- [ ] Add AI visualization
- [ ] Memory profiling tools
- [ ] Save/load game states