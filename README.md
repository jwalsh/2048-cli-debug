# 2048 CLI Debug

[![C](https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white)](https://en.wikipedia.org/wiki/C_(programming_language))
[![LLDB](https://img.shields.io/badge/LLDB-3F4145?style=for-the-badge&logo=llvm&logoColor=white)](https://lldb.llvm.org/)
[![Emacs](https://img.shields.io/badge/Emacs-7F5AB6?style=for-the-badge&logo=gnu-emacs&logoColor=white)](https://www.gnu.org/software/emacs/)
[![macOS](https://img.shields.io/badge/macOS-000000?style=for-the-badge&logo=apple&logoColor=white)](https://www.apple.com/macos/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

A comprehensive debugging and analysis environment for the [2048-cli](https://github.com/Tiehuis/2048-cli) game, featuring LLDB integration, memory analysis tools, and Emacs development support.

## 🎮 Game Screenshot

```
Score: 28 (+12)
   Hi: 932
-----------------------------
|    2 |      |    4 |    8 |
|      |      |      |    8 |
|      |      |      |      |
|      |      |      |      |
-----------------------------
```

## 🚀 Features

- **LLDB Debug Scripts**: Automated board state dumps, memory inspection, and gameplay analysis
- **Emacs Integration**: Custom mode with compilation, debugging, and visualization support
- **Memory Analysis**: Tools for inspecting game state and board memory layout
- **AI Analysis**: Observe and analyze AI gameplay patterns
- **Build Automation**: Enhanced Makefile with debugging and source management targets

## 📋 Requirements

| Tool | Version | Required | Notes |
|------|---------|----------|-------|
| C Compiler | C99+ | ✅ | gcc/clang |
| LLDB | 14.0+ | ✅ | Primary debugger |
| Emacs | 25.1+ | ⭕ | For IDE features |
| Make | 3.81+ | ✅ | Build system |
| etags | Any | ⭕ | Code navigation |
| screen | 4.0+ | ⭕ | TTY capture |

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/jwalsh/2048-cli-debug.git
cd 2048-cli-debug

# Build the game
cd 2048-cli-0.9.1
make

# Build with debug symbols
make CFLAGS="-g -O0"

# Generate tags for navigation
make etags
```

## 🎯 Quick Start

### Running the Game

```bash
# Play interactively
./2048

# Watch AI play
./2048 --ai

# Custom board size
./2048 --size 5
```

### Debugging

```bash
# Basic debugging session
lldb ./2048 -s debug.lldb

# Interactive debugging with custom commands
lldb ./2048 -s debug-interactive.lldb

# Automated analysis
lldb ./2048 -s debug-automated.lldb
```

### Emacs Integration

Add to your Emacs configuration:

```elisp
(add-to-list 'load-path "/path/to/2048-cli-debug/2048-cli-0.9.1/")
(require '2048-mode)
```

Key bindings:
- `C-c C-c` - Compile
- `C-c C-d` - Debug with LLDB
- `C-c C-r` - Run game
- `C-c C-a` - Run with AI

## 📁 Project Structure

```
2048-cli-debug/
├── 2048-cli-0.9.1/         # Game source code
│   ├── src/                # C source files
│   ├── debug*.lldb         # LLDB scripts
│   ├── 2048-mode.el        # Emacs mode
│   └── Makefile            # Build configuration
├── README.md               # This file
├── CONTRIBUTING.md         # Contribution guidelines
├── ARCHITECTURE.md         # System architecture
└── LICENSE                 # MIT License
```

## 🔍 Debug Features

### LLDB Scripts

- **debug.lldb**: Basic breakpoints with automatic board dumps
- **debug-interactive.lldb**: Custom commands (board, raw, state)
- **debug-automated.lldb**: AI gameplay analysis
- **debug-symbols.lldb**: Symbol and type information

### Memory Layout

The game uses a clever memory layout:
- Single contiguous array for board data
- 2D pointer array for row access
- Efficient for both cache and iteration

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:
- Understanding the codebase
- Debugging techniques
- Emacs workflow
- Submitting changes

## 📚 Documentation

- [Architecture Overview](ARCHITECTURE.md)
- [Debug Tools Guide](2048-cli-0.9.1/DEBUG-README.md)
- [Original Game Documentation](2048-cli-0.9.1/README.md)

## 🙏 Acknowledgments

- Original [2048-cli](https://github.com/Tiehuis/2048-cli) by Marc Tiehuis
- 2048 game concept by Gabriele Cirulli

## 📄 License

This project maintains the MIT License from the original 2048-cli. See [LICENSE](LICENSE) for details.