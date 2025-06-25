#!/usr/bin/env python3
"""
LLDB Controller - A framework for programmatic debugger control
This creates a bridge between LLDB and external decision-making systems
"""

import os
import sys
import time
import json
import threading
import queue
import subprocess
from pathlib import Path

# Add LLDB to Python path
lldb_python_path = subprocess.check_output(['lldb', '-P']).decode().strip()
sys.path.append(lldb_python_path)

import lldb

class LLDBController:
    """Generic LLDB controller that can be extended for any program"""
    
    def __init__(self, executable_path):
        self.executable_path = executable_path
        self.debugger = lldb.SBDebugger.Create()
        self.debugger.SetAsync(True)
        self.target = None
        self.process = None
        self.listener = lldb.SBListener("LLDBController")
        self.command_queue = queue.Queue()
        self.state_callbacks = {}
        self.breakpoint_handlers = {}
        
        # Communication channels
        self.state_file = Path("/tmp/lldb_state.json")
        self.command_file = Path("/tmp/lldb_command.json")
        self.ready_file = Path("/tmp/lldb_ready")
        
        # Clean up old files
        for f in [self.state_file, self.command_file, self.ready_file]:
            f.unlink(missing_ok=True)
        
    def setup_target(self):
        """Create target and set up error handling"""
        self.target = self.debugger.CreateTarget(self.executable_path)
        if not self.target:
            raise Exception(f"Failed to create target for {self.executable_path}")
        
        # Set up listener for process events
        self.listener = self.debugger.GetListener()
        
    def add_breakpoint(self, location, handler=None):
        """Add a breakpoint with optional Python handler"""
        bp = self.target.BreakpointCreateByName(location)
        if not bp.IsValid():
            # Try by regex
            bp = self.target.BreakpointCreateByRegex(location)
        
        if bp.IsValid() and handler:
            bp_id = bp.GetID()
            self.breakpoint_handlers[bp_id] = handler
            # Set up breakpoint callback
            bp.SetScriptCallbackBody(f"""
import json
from pathlib import Path

# Get controller instance
controller = lldb.debugger.GetSelectedTarget().GetUserData()

# Extract state
state = controller.extract_state(frame, bp_loc, internal_dict)

# Write state to file
with open('{self.state_file}', 'w') as f:
    json.dump(state, f)

# Signal ready
Path('{self.ready_file}').touch()

# Wait for command
while not Path('{self.command_file}').exists():
    time.sleep(0.01)

# Read and execute command
with open('{self.command_file}', 'r') as f:
    command = json.load(f)

Path('{self.command_file}').unlink()

# Execute command
controller.execute_command(command, frame)

# Continue
return False
""")
        return bp
    
    def extract_state(self, frame, bp_loc, internal_dict):
        """Extract program state - override in subclasses"""
        state = {
            'breakpoint_id': bp_loc.GetBreakpoint().GetID(),
            'function': frame.GetFunctionName(),
            'line': frame.GetLineEntry().GetLine(),
            'timestamp': time.time()
        }
        
        # Extract all variables in scope
        variables = {}
        for var in frame.GetVariables(True, True, True, True):
            name = var.GetName()
            value = var.GetValue()
            if name and value:
                variables[name] = value
        
        state['variables'] = variables
        
        # Call custom handler if available
        bp_id = bp_loc.GetBreakpoint().GetID()
        if bp_id in self.breakpoint_handlers:
            custom_state = self.breakpoint_handlers[bp_id](frame, self.target)
            state.update(custom_state)
        
        return state
    
    def execute_command(self, command, frame):
        """Execute a command - override in subclasses"""
        cmd_type = command.get('type')
        
        if cmd_type == 'continue':
            pass  # Will continue automatically
        
        elif cmd_type == 'set_variable':
            var_name = command['name']
            var_value = command['value']
            frame.FindVariable(var_name).SetValueFromCString(str(var_value))
        
        elif cmd_type == 'return_value':
            # Return from current function with value
            return_val = command['value']
            # This is tricky - need to construct proper SBValue
            thread = frame.GetThread()
            # For simple types:
            thread.ReturnFromFrame(frame, 
                lldb.SBValue.CreateValueFromExpression("return", str(return_val)))
        
        elif cmd_type == 'inject_call':
            # Inject a function call
            expr = command['expression']
            frame.EvaluateExpression(expr)
        
        elif cmd_type == 'stdin':
            # Send input to process stdin
            data = command['data']
            self.process.PutSTDIN(data.encode())
    
    def run(self):
        """Run the target under debugger control"""
        error = lldb.SBError()
        self.process = self.target.Launch(
            self.listener,
            None,  # argv
            None,  # envp
            None,  # stdin_path
            None,  # stdout_path  
            None,  # stderr_path
            None,  # working_directory
            0,     # launch_flags
            False, # stop_at_entry
            error
        )
        
        if not error.Success():
            raise Exception(f"Failed to launch process: {error}")
        
        # Store reference to controller in target
        self.target.SetUserData(self)
        
        # Event loop
        event = lldb.SBEvent()
        while True:
            if self.listener.WaitForEvent(1, event):
                if lldb.SBProcess.EventIsProcessEvent(event):
                    state = lldb.SBProcess.GetStateFromEvent(event)
                    
                    if state == lldb.eStateExited:
                        print("Process exited")
                        break
                    elif state == lldb.eStateStopped:
                        # Check stop reason
                        thread = self.process.GetSelectedThread()
                        if thread.GetStopReason() == lldb.eStopReasonBreakpoint:
                            # Breakpoint hit - handler will take over
                            pass
                        else:
                            # Other stop reason
                            self.process.Continue()
            
            # Check for external commands
            if self.command_file.exists() and not self.ready_file.exists():
                with open(self.command_file, 'r') as f:
                    command = json.load(f)
                self.command_file.unlink()
                self.handle_external_command(command)
    
    def handle_external_command(self, command):
        """Handle commands sent from outside the debugger"""
        # This allows external control even when not at a breakpoint
        if command['type'] == 'interrupt':
            self.process.Stop()
        elif command['type'] == 'continue':
            self.process.Continue()
        # Add more as needed


class Game2048Controller(LLDBController):
    """Specific controller for 2048 game"""
    
    def __init__(self):
        super().__init__("2048-cli-0.9.1/2048")
        
    def setup(self):
        """Set up 2048-specific breakpoints and handlers"""
        self.setup_target()
        
        # Breakpoint when board is displayed
        self.add_breakpoint("print_board", self.extract_board_state)
        
        # Breakpoint when waiting for input
        self.add_breakpoint("getchar", self.handle_input_request)
        
    def extract_board_state(self, frame, target):
        """Extract 2048 board state"""
        state = {}
        
        # Get board array
        board_var = target.FindGlobalVariables("board", 1)
        if board_var:
            board_array = board_var[0]
            board = []
            for i in range(16):
                cell = board_array.GetChildAtIndex(i)
                board.append(cell.GetValueAsUnsigned() if cell else 0)
            state['board'] = board
        
        # Get score
        score_var = target.FindGlobalVariables("score", 1)
        if score_var:
            state['score'] = score_var[0].GetValueAsUnsigned()
        
        return state
    
    def handle_input_request(self, frame, target):
        """Called when game is waiting for input"""
        # Extract current state
        state = self.extract_board_state(frame, target)
        state['waiting_for_input'] = True
        return state


# Example external controller that makes decisions
class GamePlayer:
    """External process that controls the game through LLDB"""
    
    def __init__(self):
        self.state_file = Path("/tmp/lldb_state.json")
        self.command_file = Path("/tmp/lldb_command.json")
        self.ready_file = Path("/tmp/lldb_ready")
        
    def wait_for_state(self):
        """Wait for LLDB to provide state"""
        while not self.ready_file.exists():
            time.sleep(0.01)
        
        self.ready_file.unlink()
        
        with open(self.state_file, 'r') as f:
            return json.load(f)
    
    def send_command(self, command):
        """Send command to LLDB"""
        with open(self.command_file, 'w') as f:
            json.dump(command, f)
    
    def play(self):
        """Main game playing loop"""
        move_count = 0
        
        while True:
            state = self.wait_for_state()
            
            if state.get('waiting_for_input'):
                # Analyze board and decide move
                board = state.get('board', [])
                score = state.get('score', 0)
                
                print(f"Move {move_count}, Score: {score}")
                
                # Simple AI - you can make this much smarter
                import random
                moves = ['w', 's', 'a', 'd']
                weights = [0.1, 0.4, 0.2, 0.3]  # Prefer down and right
                move = random.choices(moves, weights)[0]
                
                # Send move as return value from getchar
                char_code = ord(move)
                self.send_command({
                    'type': 'return_value',
                    'value': char_code
                })
                
                move_count += 1
            
            else:
                # Just continue
                self.send_command({'type': 'continue'})


if __name__ == "__main__":
    # This would be split into two processes:
    # 1. LLDB controller process
    # 2. External decision-making process
    
    if len(sys.argv) > 1 and sys.argv[1] == "controller":
        # Run LLDB controller
        controller = Game2048Controller()
        controller.setup()
        controller.run()
    
    elif len(sys.argv) > 1 and sys.argv[1] == "player":
        # Run external player
        player = GamePlayer()
        player.play()
    
    else:
        print("Usage: python lldb_controller.py [controller|player]")
        print("Run 'controller' in one terminal and 'player' in another")