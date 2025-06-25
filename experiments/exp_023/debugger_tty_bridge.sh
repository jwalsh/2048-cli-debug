#!/bin/bash
# Bridge between debugger and external control using TTYs and screen

# This demonstrates the "hard part" - coordinating between:
# 1. A debugger session (LLDB)
# 2. The program being debugged (2048) 
# 3. An external controller making decisions
# All through terminal interfaces

# Create named pipes for bidirectional communication
CONTROL_DIR="/tmp/debugger_bridge_$$"
mkdir -p "$CONTROL_DIR"

mkfifo "$CONTROL_DIR/lldb_in"    # Commands to LLDB
mkfifo "$CONTROL_DIR/lldb_out"   # Output from LLDB
mkfifo "$CONTROL_DIR/game_tty"   # Game's TTY output
mkfifo "$CONTROL_DIR/decisions"  # Decision engine input

# Function to set up LLDB with proper TTY handling
setup_lldb_session() {
    cat > "$CONTROL_DIR/lldb_init.py" << 'EOF'
import lldb
import os
import termios
import tty
import pty
import select
import time

# Global state
game_pty_master = None
game_pty_slave = None

def launch_with_pty(debugger, command, result, internal_dict):
    """Launch target with a PTY we can monitor"""
    global game_pty_master, game_pty_slave
    
    # Create a pseudo-terminal
    game_pty_master, game_pty_slave = pty.openpty()
    
    # Get the slave device name
    slave_name = os.ttyname(game_pty_slave)
    
    print(f"Created PTY: {slave_name}")
    
    # Create launch info with our PTY
    target = debugger.GetSelectedTarget()
    launch_info = lldb.SBLaunchInfo(None)
    launch_info.SetLaunchFlags(0)
    
    # Redirect stdio to our PTY
    launch_info.AddOpenFileAction(0, slave_name, True, False)  # stdin
    launch_info.AddOpenFileAction(1, slave_name, False, True)  # stdout
    launch_info.AddOpenFileAction(2, slave_name, False, True)  # stderr
    
    # Launch the process
    error = lldb.SBError()
    process = target.Launch(launch_info, error)
    
    if error.Success():
        print(f"Process {process.GetProcessID()} launched with PTY")
        # Start monitoring thread
        import threading
        monitor_thread = threading.Thread(target=monitor_pty_output)
        monitor_thread.daemon = True
        monitor_thread.start()
    else:
        print(f"Launch failed: {error}")
    
    return process

def monitor_pty_output():
    """Monitor PTY output and forward to analysis"""
    global game_pty_master
    
    output_file = os.environ.get('GAME_OUTPUT_PIPE', '/tmp/game_output')
    
    while game_pty_master:
        try:
            # Check if data is available
            r, _, _ = select.select([game_pty_master], [], [], 0.1)
            if r:
                data = os.read(game_pty_master, 4096)
                if data:
                    # Forward to output pipe
                    with open(output_file, 'ab') as f:
                        f.write(data)
                    
                    # Also print to LLDB console
                    print(data.decode('utf-8', errors='ignore'), end='')
        except OSError:
            break

def send_key(debugger, command, result, internal_dict):
    """Send a keystroke to the game"""
    global game_pty_master
    
    if len(command) < 1:
        print("Usage: send_key <character>")
        return
    
    key = command[0]
    if game_pty_master:
        os.write(game_pty_master, key.encode())
        print(f"Sent key: {key}")
    else:
        print("No PTY available")

def extract_board_state(debugger, command, result, internal_dict):
    """Extract and report current board state"""
    target = debugger.GetSelectedTarget()
    
    # Get board array
    board_var = target.FindGlobalVariables("board", 1)[0]
    score_var = target.FindGlobalVariables("score", 1)[0]
    
    board_values = []
    for i in range(16):
        cell = board_var.GetChildAtIndex(i)
        board_values.append(cell.GetValueAsUnsigned())
    
    score = score_var.GetValueAsUnsigned()
    
    # Write state to decision engine
    state_file = os.environ.get('STATE_OUTPUT', '/tmp/game_state')
    with open(state_file, 'w') as f:
        f.write(f"SCORE:{score}\\n")
        f.write(f"BOARD:{','.join(map(str, board_values))}\\n")
    
    # Pretty print
    print(f"\\nScore: {score}")
    print("Board:")
    for i in range(4):
        row = board_values[i*4:(i+1)*4]
        print(" ".join(f"{v:4}" if v else "   ." for v in row))

def auto_play_handler(frame, bp_loc, internal_dict):
    """Breakpoint handler for automated play"""
    debugger = frame.GetThread().GetProcess().GetTarget().GetDebugger()
    
    # Extract state
    debugger.HandleCommand("extract_board")
    
    # Wait for decision
    decision_file = os.environ.get('DECISION_INPUT', '/tmp/game_decision')
    
    # Signal ready for decision
    ready_file = decision_file + '.ready'
    open(ready_file, 'w').close()
    
    # Wait for decision (with timeout)
    start_time = time.time()
    while not os.path.exists(decision_file) and time.time() - start_time < 5:
        time.sleep(0.01)
    
    if os.path.exists(decision_file):
        with open(decision_file, 'r') as f:
            move = f.read().strip()
        os.remove(decision_file)
        
        # Send the move
        debugger.HandleCommand(f"send_key {move}")
    
    # Continue execution
    return False

def __lldb_init_module(debugger, internal_dict):
    """Initialize custom commands"""
    debugger.HandleCommand('command script add -f lldb_init.launch_with_pty launch_pty')
    debugger.HandleCommand('command script add -f lldb_init.send_key send_key')
    debugger.HandleCommand('command script add -f lldb_init.extract_board_state extract_board')
    
    print("TTY Bridge commands loaded:")
    print("  launch_pty - Launch with PTY monitoring")
    print("  send_key <char> - Send keystroke to game")
    print("  extract_board - Extract current board state")
EOF

    # Create LLDB startup script
    cat > "$CONTROL_DIR/lldb_commands" << EOF
# Load our Python module
command script import $CONTROL_DIR/lldb_init.py

# Set up environment
settings set target.env-vars GAME_OUTPUT_PIPE=$CONTROL_DIR/game_tty
settings set target.env-vars STATE_OUTPUT=$CONTROL_DIR/game_state
settings set target.env-vars DECISION_INPUT=$CONTROL_DIR/decision

# Load the game
file 2048-cli-0.9.1/2048

# Set breakpoints
b print_board
b getchar

# Set breakpoint commands
br command add 1
extract_board
c
DONE

br command add 2
script
import time
# Auto-play logic
frame = lldb.debugger.GetSelectedTarget().GetProcess().GetSelectedThread().GetSelectedFrame()
lldb_init.auto_play_handler(frame, None, None)
DONE

# Launch with PTY
launch_pty
EOF
}

# Function to run the decision engine
run_decision_engine() {
    echo "Starting decision engine..."
    
    while true; do
        # Wait for ready signal
        if [ -f "$CONTROL_DIR/decision.ready" ]; then
            rm -f "$CONTROL_DIR/decision.ready"
            
            # Read current state
            if [ -f "$CONTROL_DIR/game_state" ]; then
                SCORE=$(grep "SCORE:" "$CONTROL_DIR/game_state" | cut -d: -f2)
                BOARD=$(grep "BOARD:" "$CONTROL_DIR/game_state" | cut -d: -f2)
                
                echo "State - Score: $SCORE"
                
                # Simple decision logic (can be replaced with sophisticated AI)
                # Prefer: down > right > left > up
                MOVES=("s" "d" "a" "w")
                WEIGHTS=(40 30 20 10)
                
                # Weighted random selection
                RAND=$((RANDOM % 100))
                CUMULATIVE=0
                SELECTED_MOVE="s"
                
                for i in {0..3}; do
                    CUMULATIVE=$((CUMULATIVE + WEIGHTS[i]))
                    if [ $RAND -lt $CUMULATIVE ]; then
                        SELECTED_MOVE="${MOVES[i]}"
                        break
                    fi
                done
                
                echo "Decision: $SELECTED_MOVE"
                
                # Send decision
                echo "$SELECTED_MOVE" > "$CONTROL_DIR/decision"
            fi
        fi
        
        sleep 0.01
    done
}

# Main orchestration
main() {
    echo "Setting up debugger TTY bridge..."
    
    # Clean up on exit
    trap "rm -rf $CONTROL_DIR; kill 0" EXIT
    
    # Set up LLDB session
    setup_lldb_session
    
    # Start decision engine in background
    run_decision_engine &
    DECISION_PID=$!
    
    # Start screen session with LLDB
    echo "Starting LLDB in screen session..."
    screen -dmS lldb_2048 -L -Logfile "$CONTROL_DIR/lldb.log" \
        bash -c "cd $(pwd) && lldb -s $CONTROL_DIR/lldb_commands"
    
    # Monitor the session
    echo "Monitoring game... (Press Ctrl+C to stop)"
    echo "Attach to screen: screen -r lldb_2048"
    
    # Wait and show progress
    MOVE_COUNT=0
    while screen -list | grep -q lldb_2048; do
        if [ -f "$CONTROL_DIR/game_state" ]; then
            SCORE=$(grep "SCORE:" "$CONTROL_DIR/game_state" | cut -d: -f2 2>/dev/null || echo "0")
            echo -ne "\\rMoves: $MOVE_COUNT, Score: $SCORE    "
            MOVE_COUNT=$((MOVE_COUNT + 1))
        fi
        sleep 1
    done
    
    echo "\\nDebugger session ended"
}

# Run it
main "$@"