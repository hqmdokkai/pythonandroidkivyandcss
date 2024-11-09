import tkinter as tk
from tkinter import scrolledtext
import subprocess

class TerminalApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Terminal App")
        self.root.configure(bg='black')

        # Tạo layout chính
        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Tạo phần terminal với Scrollable Text
        self.terminal_frame = tk.Frame(self.main_frame, bg='black')
        self.terminal_frame.pack(fill=tk.BOTH, expand=True)

        self.terminal_output = scrolledtext.ScrolledText(self.terminal_frame, 
                                                         wrap=tk.WORD,
                                                         font=("Courier", 14),
                                                         bg='black', 
                                                         fg='white', 
                                                         state=tk.DISABLED)
        self.terminal_output.pack(fill=tk.BOTH, expand=True)

        # Tạo phần nhập lệnh
        self.command_frame = tk.Frame(self.main_frame, bg='black')
        self.command_frame.pack(fill=tk.X)

        self.command_input = tk.Entry(self.command_frame, 
                                      bg='black', 
                                      fg='white', 
                                      font=("Courier", 14), 
                                      bd=0, 
                                      insertbackground='white')
        self.command_input.pack(fill=tk.X, pady=10, padx=10)

        self.run_button = tk.Button(self.command_frame, 
                                    text="Run Command", 
                                    bg='black', 
                                    fg='white', 
                                    font=("Courier", 14), 
                                    command=self.run_command)
        self.run_button.pack(fill=tk.X)

    def run_command(self):
        command = self.command_input.get().strip()

        if "sudo" in command or "su" in command:
            result = "Security alert: Running 'sudo' or 'su' commands is not allowed for security reasons."
        else:
            try:
                # Chạy lệnh và lấy kết quả
                result = subprocess.run(command, 
                                        shell=True, 
                                        capture_output=True, 
                                        text=True)
                result_text = result.stdout + result.stderr
            except Exception as e:
                result_text = f"Error: {e}"

            result = f"$ {command}\n{result_text}"

        # Hiển thị kết quả
        self.terminal_output.config(state=tk.NORMAL)
        self.terminal_output.insert(tk.END, f"{result}\n")
        self.terminal_output.config(state=tk.DISABLED)
        
        # Cuộn xuống cuối
        self.terminal_output.yview(tk.END)

        # Xóa nội dung ô nhập lệnh
        self.command_input.delete(0, tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    app = TerminalApp(root)
    root.mainloop()
