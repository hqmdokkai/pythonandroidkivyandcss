from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import subprocess

# Đặt màu nền toàn bộ ứng dụng
Window.clearcolor = (0, 0, 0, 1)  # Đen

class TerminalApp(App):

    def build(self):
        # Tạo layout chính chia màn hình theo chiều dọc
        main_layout = BoxLayout(orientation='vertical')

        # Tạo một layout cho phần terminal
        terminal_layout = BoxLayout(orientation='vertical', size_hint_y=0.5)
        
        # Tạo ScrollView để cuộn nội dung
        self.scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.terminal_output = TextInput(font_size=20,
                                         readonly=True,
                                         background_color=(0, 0, 0, 1),
                                         foreground_color=(1, 1, 1, 1),
                                         size_hint_y=None)
        self.terminal_output.bind(
            minimum_height=self.terminal_output.setter('height'))
        self.scroll_view.add_widget(self.terminal_output)
        terminal_layout.add_widget(self.scroll_view)
        
        # Tạo layout cho phần nhập lệnh và nút
        command_layout = BoxLayout(orientation='vertical', size_hint_y=0.5)

        # TextInput để nhập lệnh
        self.command_input = TextInput(hint_text="Enter command here",
                                       multiline=False,
                                       size_hint=(1, None),
                                       height=50,
                                       background_color=(0, 0, 0, 1),
                                       foreground_color=(1, 1, 1, 1))
        command_layout.add_widget(self.command_input)

        # Nút để thực thi lệnh
        run_button = Button(text="Run Command", size_hint=(1, None), height=50)
        run_button.bind(on_press=self.run_command)
        command_layout.add_widget(run_button)

        # Thêm cả hai layout vào main_layout
        main_layout.add_widget(terminal_layout)
        main_layout.add_widget(command_layout)

        return main_layout

    def run_command(self, instance):
        command = self.command_input.text.strip()

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
        self.terminal_output.text += f"{result}\n"
        self.command_input.text = ""  # Xóa nội dung ô nhập lệnh

        # Cuộn xuống cuối cùng
        self.scroll_view.scroll_to(self.terminal_output)

if __name__ == '__main__':
    TerminalApp().run()
