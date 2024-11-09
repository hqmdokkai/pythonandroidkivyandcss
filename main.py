from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.lang import Builder
from kivy_css import CssParser
import sys
import io

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Tạo phần chiếm 50% màn hình
        self.top_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5))
        
        # Tạo ô văn bản để nhập mã Python
        self.code_input = TextInput(size_hint_y=0.8, multiline=True, hint_text='Enter Python code here')
        self.top_layout.add_widget(self.code_input)
        
        # Tạo nút để chạy mã Python
        self.run_button = Button(text='Run Code', size_hint_y=0.1)
        self.run_button.bind(on_press=self.run_code)
        self.top_layout.add_widget(self.run_button)
        
        # Tạo nhãn để hiển thị kết quả
        self.output_label = Label(size_hint_y=0.1, text='Output will be displayed here.')
        self.top_layout.add_widget(self.output_label)
        
        self.add_widget(self.top_layout)
        
        # Tạo BoxLayout hoặc ScrollView cho phần còn lại của màn hình
        self.bottom_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5))
        self.add_widget(self.bottom_layout)

        # Áp dụng kiểu dáng từ CSS
        self.apply_css()

        # Thay đổi màu nền cho ứng dụng
        with self.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Màu nền xám sáng
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def apply_css(self):
        css_parser = CssParser()
        kv_styles = css_parser.parse_file('style.css')
        
        # Phân tích KV styles
        Builder.load_string(kv_styles)  # Load KV styles into Builder
        for widget in self.top_layout.children:
            widget_class = widget.__class__.__name__.lower()
            kv_widget_styles = css_parser.styles.get(f'.{widget_class}', {})
            for prop, value in kv_widget_styles.items():
                kivy_prop = css_parser.convert_property(prop, value)
                if kivy_prop:
                    key, val = kivy_prop.split(':', 1)
                    key = key.strip()
                    val = val.strip()
                    setattr(widget, key, val)
    
    def run_code(self, instance):
        code = self.code_input.text
        
        # Thay đổi đối tượng sys.stdout để lấy kết quả từ exec
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            exec(code, globals())
            output = new_stdout.getvalue()
        except Exception as e:
            output = str(e)
        
        sys.stdout = old_stdout
        self.output_label.text = output

class MainApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    MainApp().run()
