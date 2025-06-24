#!/usr/bin/env python3
"""
Universal Program Debugger - Demonstrates debugging arbitrary programs
Shows how we can apply the same techniques to any code
"""

import lldb
import json
import time
from pathlib import Path
from lldb_controller import LLDBController

class UniversalDebugger(LLDBController):
    """Debug any program with configurable inspection points"""
    
    def __init__(self, executable_path, config):
        super().__init__(executable_path)
        self.config = config
        self.execution_trace = []
        self.call_graph = {}
        self.memory_snapshots = []
        
    def setup(self):
        """Set up debugging based on configuration"""
        self.setup_target()
        
        # Set up inspection points from config
        for point in self.config.get('inspection_points', []):
            if point['type'] == 'function_entry':
                self.add_function_trace(point['name'])
            elif point['type'] == 'line':
                self.add_line_breakpoint(point['file'], point['line'])
            elif point['type'] == 'condition':
                self.add_conditional_breakpoint(point['expression'])
            elif point['type'] == 'watchpoint':
                self.add_watchpoint(point['variable'])
    
    def add_function_trace(self, function_name):
        """Trace function calls and returns"""
        def trace_handler(frame, target):
            func_name = frame.GetFunctionName()
            
            # Get arguments
            args = {}
            for i in range(frame.GetNumArguments()):
                arg = frame.GetValueForVariableExpressionPath(f"argv[{i}]")
                if arg:
                    args[f"arg{i}"] = str(arg.GetValue())
            
            # Record call
            call_info = {
                'function': func_name,
                'arguments': args,
                'timestamp': time.time(),
                'call_depth': frame.GetThread().GetNumFrames()
            }
            
            self.execution_trace.append(call_info)
            
            # Build call graph
            if frame.GetThread().GetNumFrames() > 1:
                caller = frame.GetThread().GetFrameAtIndex(1).GetFunctionName()
                if caller not in self.call_graph:
                    self.call_graph[caller] = []
                self.call_graph[caller].append(func_name)
            
            return {'trace_event': call_info}
        
        self.add_breakpoint(function_name, trace_handler)
    
    def add_line_breakpoint(self, file_path, line_number):
        """Break at specific source line"""
        bp = self.target.BreakpointCreateByLocation(file_path, line_number)
        
        def line_handler(frame, target):
            # Capture all local variables
            locals_dict = {}
            variables = frame.GetVariables(True, True, False, True)
            
            for var in variables:
                name = var.GetName()
                value = var.GetValue()
                type_name = var.GetTypeName()
                
                if name:
                    locals_dict[name] = {
                        'value': value,
                        'type': type_name,
                        'address': hex(var.GetAddress().GetLoadAddress(target))
                    }
            
            return {
                'line_break': {
                    'file': file_path,
                    'line': line_number,
                    'locals': locals_dict
                }
            }
        
        if bp.IsValid():
            self.breakpoint_handlers[bp.GetID()] = line_handler
    
    def add_watchpoint(self, variable_expression):
        """Watch for variable changes"""
        # This would set up a watchpoint - more complex implementation needed
        pass
    
    def analyze_memory(self, frame):
        """Analyze memory usage at current point"""
        process = frame.GetThread().GetProcess()
        
        # Get memory regions
        memory_info = {
            'heap_size': 0,
            'stack_size': 0,
            'allocations': []
        }
        
        # This is simplified - real implementation would walk memory regions
        for i in range(process.GetNumMemoryRegions()):
            region = lldb.SBMemoryRegionInfo()
            if process.GetMemoryRegionInfo(i, region).Success():
                if region.IsReadable():
                    size = region.GetRegionEnd() - region.GetRegionBase()
                    memory_info['heap_size'] += size
        
        return memory_info


# Example: Debug a Fibonacci implementation
class FibonacciDebugger(UniversalDebugger):
    """Specific debugger for analyzing Fibonacci implementations"""
    
    def __init__(self):
        config = {
            'inspection_points': [
                {'type': 'function_entry', 'name': 'fibonacci'},
                {'type': 'function_entry', 'name': 'fib_recursive'},
                {'type': 'function_entry', 'name': 'fib_iterative'},
            ]
        }
        super().__init__("fibonacci", config)
        self.call_counts = {}
        self.computation_tree = {}
    
    def setup(self):
        super().setup()
        
        # Add custom analysis for fibonacci
        def fib_analyzer(frame, target):
            func_name = frame.GetFunctionName()
            
            # Get the input parameter (n)
            n_var = frame.FindVariable("n")
            if not n_var:
                n_var = frame.GetValueForVariableExpressionPath("argv[0]")
            
            n_value = n_var.GetValueAsSigned() if n_var else -1
            
            # Track call counts
            key = f"{func_name}({n_value})"
            self.call_counts[key] = self.call_counts.get(key, 0) + 1
            
            # Build computation tree
            if n_value not in self.computation_tree:
                self.computation_tree[n_value] = {
                    'computed_by': func_name,
                    'call_count': 0,
                    'children': []
                }
            
            self.computation_tree[n_value]['call_count'] += 1
            
            # Track recursion depth
            recursion_depth = 0
            for i in range(frame.GetThread().GetNumFrames()):
                if frame.GetThread().GetFrameAtIndex(i).GetFunctionName() == func_name:
                    recursion_depth += 1
            
            return {
                'fibonacci_analysis': {
                    'n': n_value,
                    'function': func_name,
                    'call_count': self.call_counts[key],
                    'recursion_depth': recursion_depth
                }
            }
        
        # Override the handlers
        for bp_id, handler in self.breakpoint_handlers.items():
            self.breakpoint_handlers[bp_id] = fib_analyzer
    
    def generate_report(self):
        """Generate analysis report"""
        report = {
            'total_calls': sum(self.call_counts.values()),
            'unique_calls': len(self.call_counts),
            'most_called': max(self.call_counts.items(), key=lambda x: x[1]),
            'max_recursion_depth': max(self.computation_tree.values(), 
                                     key=lambda x: x.get('call_count', 0)),
            'execution_trace_length': len(self.execution_trace)
        }
        
        return report


# Example: Create a debugging MCP server
class DebuggerMCPServer:
    """
    MCP (Model Context Protocol) server that provides debugging capabilities
    This would expose debugging operations as MCP tools
    """
    
    def __init__(self, debugger):
        self.debugger = debugger
        self.tools = {
            'debug.set_breakpoint': self.tool_set_breakpoint,
            'debug.get_variables': self.tool_get_variables,
            'debug.step': self.tool_step,
            'debug.continue': self.tool_continue,
            'debug.evaluate': self.tool_evaluate,
            'debug.get_backtrace': self.tool_get_backtrace,
            'debug.modify_variable': self.tool_modify_variable,
            'debug.inject_code': self.tool_inject_code
        }
    
    def tool_set_breakpoint(self, params):
        """Set a breakpoint at function or line"""
        location = params.get('location')
        condition = params.get('condition')
        
        if '::' in location:  # File::line format
            file_path, line = location.split('::')
            bp = self.debugger.target.BreakpointCreateByLocation(
                file_path, int(line))
        else:  # Function name
            bp = self.debugger.target.BreakpointCreateByName(location)
        
        if condition and bp.IsValid():
            bp.SetCondition(condition)
        
        return {
            'breakpoint_id': bp.GetID() if bp.IsValid() else None,
            'enabled': bp.IsEnabled() if bp.IsValid() else False
        }
    
    def tool_get_variables(self, params):
        """Get all variables in current scope"""
        frame = self.debugger.process.GetSelectedThread().GetSelectedFrame()
        
        variables = {}
        for var in frame.GetVariables(True, True, True, True):
            name = var.GetName()
            if name:
                variables[name] = {
                    'value': var.GetValue(),
                    'type': var.GetTypeName(),
                    'in_scope': var.IsInScope()
                }
        
        return variables
    
    def tool_evaluate(self, params):
        """Evaluate an expression in current context"""
        expression = params.get('expression')
        frame = self.debugger.process.GetSelectedThread().GetSelectedFrame()
        
        result = frame.EvaluateExpression(expression)
        
        return {
            'result': result.GetValue(),
            'type': result.GetTypeName(),
            'error': result.GetError().GetCString() if result.GetError().Fail() else None
        }
    
    def tool_modify_variable(self, params):
        """Modify a variable's value"""
        var_name = params.get('variable')
        new_value = params.get('value')
        
        frame = self.debugger.process.GetSelectedThread().GetSelectedFrame()
        var = frame.FindVariable(var_name)
        
        if var:
            success = var.SetValueFromCString(str(new_value))
            return {'success': success}
        
        return {'success': False, 'error': 'Variable not found'}
    
    def tool_inject_code(self, params):
        """Inject and execute code at current point"""
        code = params.get('code')
        frame = self.debugger.process.GetSelectedThread().GetSelectedFrame()
        
        # This is powerful - we can inject arbitrary code!
        result = frame.EvaluateExpression(code)
        
        return {
            'executed': True,
            'result': result.GetValue() if result.GetValue() else None,
            'side_effects': 'Code executed in target process context'
        }
    
    # ... more tools for stepping, backtraces, etc.


# Example usage for different scenarios
def demonstrate_capabilities():
    """Show how this can be used for various debugging tasks"""
    
    print("=== Universal Debugger Capabilities ===")
    print()
    print("1. Game State Extraction (2048)")
    print("   - Read board state from memory")
    print("   - Make intelligent moves based on analysis")
    print("   - Track score progression")
    print()
    print("2. Algorithm Analysis (Fibonacci)")
    print("   - Count function calls")
    print("   - Track recursion depth")
    print("   - Build computation trees")
    print("   - Identify optimization opportunities")
    print()
    print("3. Performance Profiling")
    print("   - Function call timing")
    print("   - Memory allocation tracking")
    print("   - Hot path identification")
    print()
    print("4. Interactive Debugging via MCP")
    print("   - Set breakpoints dynamically")
    print("   - Inspect and modify variables")
    print("   - Inject code for testing")
    print("   - Control execution flow")
    print()
    print("5. Automated Testing")
    print("   - Drive programs through test scenarios")
    print("   - Verify internal state at checkpoints")
    print("   - Detect anomalies and edge cases")
    print()
    print("The key insight: Once we can control the debugger")
    print("programmatically, we can build powerful tools for")
    print("understanding and manipulating any program!")


if __name__ == "__main__":
    demonstrate_capabilities()