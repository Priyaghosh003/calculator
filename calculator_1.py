import tkinter as tk
from tkinter import ttk, scrolledtext
import re
import math
import sys
from typing import List, Dict, Any, Optional, Tuple, Union
from enum import Enum

class CalculatorEngine:
    """Core calculator logic for performing calculations"""
   
    def __init__(self):
        """Initialize the calculator engine"""
        self.history = []
        self.memory = 0
        self.last_result = 0
   
    def evaluate(self, expression: str) -> float:
        """
        Evaluate a mathematical expression
       
        Args:
            expression: The mathematical expression to evaluate
           
        Returns:
            The result of the calculation
           
        Raises:
            ValueError: If the expression is invalid
            ZeroDivisionError: If division by zero occurs
        """
        # Replace common mathematical functions
        expression = expression.lower()
        expression = expression.replace('π', str(math.pi))
        expression = expression.replace('pi', str(math.pi))
        expression = expression.replace('e', str(math.e))
       
        # Replace sqrt, sin, cos, tan, log, etc.
        expression = re.sub(r'sqrt\((.*?)\)', r'math.sqrt(\1)', expression)
        expression = re.sub(r'sin\((.*?)\)', r'math.sin(\1)', expression)
        expression = re.sub(r'cos\((.*?)\)', r'math.cos(\1)', expression)
        expression = re.sub(r'tan\((.*?)\)', r'math.tan(\1)', expression)
        expression = re.sub(r'log\((.*?)\)', r'math.log10(\1)', expression)
        expression = re.sub(r'ln\((.*?)\)', r'math.log(\1)', expression)
       
        # Replace ^ with ** for exponentiation
        expression = expression.replace('^', '**')
       
        # Replace ans with last result
        expression = expression.replace('ans', str(self.last_result))
       
        # Replace memory variable
        expression = expression.replace('m', str(self.memory))
       
        try:
            # Use eval to calculate the result
            # Note: eval can be dangerous with untrusted input
            # For a production calculator, consider using a safer parsing method
            result = eval(expression, {"__builtins__": None}, {"math": math})
           
            # Add to history
            self.history.append((expression, result))
           
            # Update last result
            self.last_result = result
           
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {str(e)}")
   
    def store_in_memory(self, value: float) -> None:
        """Store a value in memory"""
        self.memory = value
   
    def add_to_memory(self, value: float) -> None:
        """Add a value to memory"""
        self.memory += value
   
    def subtract_from_memory(self, value: float) -> None:
        """Subtract a value from memory"""
        self.memory -= value
   
    def clear_memory(self) -> None:
        """Clear the memory"""
        self.memory = 0
   
    def get_memory(self) -> float:
        """Get the value stored in memory"""
        return self.memory
   
    def get_history(self) -> List[Tuple[str, float]]:
        """Get the calculation history"""
        return self.history
   
    def clear_history(self) -> None:
        """Clear the calculation history"""
        self.history = []


class CommandLineCalculator:
    """Command-line interface for the calculator"""
   
    def __init__(self):
        """Initialize the command-line calculator"""
        self.engine = CalculatorEngine()
        self.commands = {
            'help': self.show_help,
            'history': self.show_history,
            'clear': self.clear_history,
            'memory': self.show_memory,
            'm+': self.memory_add,
            'm-': self.memory_subtract,
            'mc': self.memory_clear,
            'ms': self.memory_store,
            'exit': self.exit_app,
            'quit': self.exit_app
        }
   
    def show_help(self) -> None:
        """Show help information"""
        print("\n===== Calculator Help =====")
        print("Enter a mathematical expression to calculate, e.g., 2 + 2")
        print("Special commands:")
        print("  help - Show this help message")
        print("  history - Show calculation history")
        print("  clear - Clear calculation history")
        print("  memory - Show memory value")
        print("  m+ <value> - Add value to memory")
        print("  m- <value> - Subtract value from memory")
        print("  mc - Clear memory")
        print("  ms <value> - Store value in memory")
        print("  exit/quit - Exit the calculator")
        print("Special values:")
        print("  pi or π - The value of pi")
        print("  e - The value of e")
        print("  ans - The last calculated result")
        print("  m - The current memory value")
        print("Functions:")
        print("  sqrt(x) - Square root of x")
        print("  sin(x) - Sine of x (in radians)")
        print("  cos(x) - Cosine of x (in radians)")
        print("  tan(x) - Tangent of x (in radians)")
        print("  log(x) - Base-10 logarithm of x")
        print("  ln(x) - Natural logarithm of x")
        print("==========================\n")
   
    def show_history(self) -> None:
        """Show calculation history"""
        history = self.engine.get_history()
        if not history:
            print("No calculation history.")
            return
       
        print("\n===== Calculation History =====")
        for i, (expression, result) in enumerate(history, 1):
            print(f"{i}. {expression} = {result}")
        print("==============================\n")
   
    def clear_history(self) -> None:
        """Clear calculation history"""
        self.engine.clear_history()
        print("Calculation history cleared.")
   
    def show_memory(self) -> None:
        """Show memory value"""
        print(f"Memory: {self.engine.get_memory()}")
   
    def memory_add(self, value: str = None) -> None:
        """Add value to memory"""
        if value is None:
            value = input("Enter value to add to memory: ")
       
        try:
            self.engine.add_to_memory(float(value))
            print(f"Added {value} to memory. New memory value: {self.engine.get_memory()}")
        except ValueError:
            print("Invalid value. Please enter a number.")
   
    def memory_subtract(self, value: str = None) -> None:
        """Subtract value from memory"""
        if value is None:
            value = input("Enter value to subtract from memory: ")
       
        try:
            self.engine.subtract_from_memory(float(value))
            print(f"Subtracted {value} from memory. New memory value: {self.engine.get_memory()}")
        except ValueError:
            print("Invalid value. Please enter a number.")
   
    def memory_clear(self) -> None:
        """Clear memory"""
        self.engine.clear_memory()
        print("Memory cleared.")
   
    def memory_store(self, value: str = None) -> None:
        """Store value in memory"""
        if value is None:
            value = input("Enter value to store in memory: ")
       
        try:
            self.engine.store_in_memory(float(value))
            print(f"Stored {value} in memory.")
        except ValueError:
            print("Invalid value. Please enter a number.")
   
    def exit_app(self) -> None:
        """Exit the application"""
        print("Goodbye!")
        sys.exit(0)
   
    def process_input(self, user_input: str) -> None:
        """Process user input"""
        parts = user_input.strip().split(maxsplit=1)
        command = parts[0].lower()
       
        if command in self.commands:
            if len(parts) > 1:
                self.commands[command](parts[1])
            else:
                self.commands[command]()
        else:
            try:
                result = self.engine.evaluate(user_input)
                print(f"= {result}")
            except Exception as e:
                print(f"Error: {str(e)}")
   
    def run(self) -> None:
        """Run the command-line calculator"""
        print("Welcome to the Calculator!")
        print("Type 'help' for available commands.")
       
        while True:
            try:
                user_input = input("\n> ")
                if not user_input:
                    continue
               
                self.process_input(user_input)
           
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")


class CalculatorGUI:
    """Graphical user interface for the calculator"""
   
    def __init__(self, root):
        """Initialize the GUI calculator"""
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
       
        self.engine = CalculatorEngine()
       
        # Set style
        self.style = ttk.Style()
        self.style.theme_use('clam')
       
        # Create display frame
        self.create_display()
       
        # Create buttons frame
        self.create_buttons()
       
        # Create history panel
        self.create_history_panel()
   
    def create_display(self):
        """Create the calculator display"""
        display_frame = ttk.Frame(self.root, padding=10)
        display_frame.pack(fill=tk.X)
       
        self.display_var = tk.StringVar()
        self.display = ttk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=('Arial', 20),
            justify='right'
        )
        self.display.pack(fill=tk.X, ipady=10)
       
        # Add a result label
        self.result_var = tk.StringVar()
        self.result_var.set("= 0")
        self.result_label = ttk.Label(
            display_frame,
            textvariable=self.result_var,
            font=('Arial', 14),
            anchor='e'
        )
        self.result_label.pack(fill=tk.X, pady=(5, 0))
   
    def create_buttons(self):
        """Create the calculator buttons"""
        buttons_frame = ttk.Frame(self.root, padding=10)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
       
        # Configure grid
        for i in range(6):
            buttons_frame.columnconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
       
        # Button definitions: (text, row, column, colspan, function)
        button_data = [
            ('MC', 0, 0, 1, lambda: self.memory_operation('mc')),
            ('MR', 0, 1, 1, lambda: self.memory_operation('mr')),
            ('MS', 0, 2, 1, lambda: self.memory_operation('ms')),
            ('M+', 0, 3, 1, lambda: self.memory_operation('m+')),
            ('M-', 0, 4, 1, lambda: self.memory_operation('m-')),
            ('C', 0, 5, 1, self.clear),
           
            ('7', 1, 0, 1, lambda: self.append_to_display('7')),
            ('8', 1, 1, 1, lambda: self.append_to_display('8')),
            ('9', 1, 2, 1, lambda: self.append_to_display('9')),
            ('/', 1, 3, 1, lambda: self.append_to_display('/')),
            ('sqrt', 1, 4, 1, lambda: self.append_to_display('sqrt(')),
            ('(', 1, 5, 1, lambda: self.append_to_display('(')),
           
            ('4', 2, 0, 1, lambda: self.append_to_display('4')),
            ('5', 2, 1, 1, lambda: self.append_to_display('5')),
            ('6', 2, 2, 1, lambda: self.append_to_display('6')),
            ('*', 2, 3, 1, lambda: self.append_to_display('*')),
            ('sin', 2, 4, 1, lambda: self.append_to_display('sin(')),
            (')', 2, 5, 1, lambda: self.append_to_display(')')),
           
            ('1', 3, 0, 1, lambda: self.append_to_display('1')),
            ('2', 3, 1, 1, lambda: self.append_to_display('2')),
            ('3', 3, 2, 1, lambda: self.append_to_display('3')),
            ('-', 3, 3, 1, lambda: self.append_to_display('-')),
            ('cos', 3, 4, 1, lambda: self.append_to_display('cos(')),
            ('^', 3, 5, 1, lambda: self.append_to_display('^')),
           
            ('0', 4, 0, 1, lambda: self.append_to_display('0')),
            ('.', 4, 1, 1, lambda: self.append_to_display('.')),
            ('π', 4, 2, 1, lambda: self.append_to_display('π')),
            ('+', 4, 3, 1, lambda: self.append_to_display('+')),
            ('tan', 4, 4, 1, lambda: self.append_to_display('tan(')),
            ('=', 4, 5, 1, self.calculate),
        ]
       
        # Create buttons
        for text, row, col, colspan, command in button_data:
            button = ttk.Button(buttons_frame, text=text, command=command)
            button.grid(row=row, column=col, columnspan=colspan, sticky='nsew', padx=2, pady=2)
   
    def create_history_panel(self):
        """Create the history panel"""
        history_frame = ttk.LabelFrame(self.root, text="History", padding=10)
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
       
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            wrap=tk.WORD,
            height=5,
            font=('Arial', 10)
        )
        self.history_text.pack(fill=tk.BOTH, expand=True)
       
        # Make the history text read-only
        self.history_text.config(state=tk.DISABLED)
       
        # Add clear history button
        clear_button = ttk.Button(
            history_frame,
            text="Clear History",
            command=self.clear_history
        )
        clear_button.pack(pady=(5, 0))
   
    def append_to_display(self, text):
        """Append text to the display"""
        current_text = self.display_var.get()
        self.display_var.set(current_text + text)
   
    def clear(self):
        """Clear the display"""
        self.display_var.set("")
        self.result_var.set("= 0")
   
    def calculate(self):
        """Calculate the result of the expression"""
        expression = self.display_var.get()
        if not expression:
            return
       
        try:
            result = self.engine.evaluate(expression)
            self.result_var.set(f"= {result}")
           
            # Update history
            self.update_history(expression, result)
        except Exception as e:
            self.result_var.set(f"Error: {str(e)}")
   
    def update_history(self, expression, result):
        """Update the history panel"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, f"{expression} = {result}\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
   
    def clear_history(self):
        """Clear the history panel"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)
        self.engine.clear_history()
   
    def memory_operation(self, operation):
        """Perform a memory operation"""
        if operation == 'mc':
            self.engine.clear_memory()
        elif operation == 'mr':
            self.display_var.set(str(self.engine.get_memory()))
        elif operation == 'ms':
            try:
                value = float(self.result_var.get()[2:])  # Remove "= " prefix
                self.engine.store_in_memory(value)
            except ValueError:
                pass
        elif operation == 'm+':
            try:
                value = float(self.result_var.get()[2:])  # Remove "= " prefix
                self.engine.add_to_memory(value)
            except ValueError:
                pass
        elif operation == 'm-':
            try:
                value = float(self.result_var.get()[2:])  # Remove "= " prefix
                self.engine.subtract_from_memory(value)
            except ValueError:
                pass


def main():
    """Main function to run the calculator"""
    # Check if the user wants CLI or GUI
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        # Run command-line interface
        cli = CommandLineCalculator()
        cli.run()
    else:
        # Run graphical interface
        root = tk.Tk()
        app = CalculatorGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()


