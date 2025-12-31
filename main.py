import customtkinter as ctk
import platform

class UnitConverter(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 根据操作系统选择平滑字体
        self.setup_fonts()
        
        # 换算系数定义
        self.conversions = {
            "meter_feet": {
                "factor": 3.28084,
                "units_zh": ("米", "英尺"),
                "units_en": ("Meter", "Feet"),
                "name_zh": "米 ↔ 英尺",
                "name_en": "Meter ↔ Feet"
            },
            "hpa_inhg": {
                "factor": 0.02953,
                "units_zh": ("百帕", "英寸水银柱"),
                "units_en": ("hPa", "inHg"),
                "name_zh": "百帕 ↔ 英寸水银柱",
                "name_en": "hPa ↔ inHg"
            },
            "pound_kg": {
                "factor": 0.453592,
                "units_zh": ("磅", "千克"),
                "units_en": ("Pound", "Kilogram"),
                "name_zh": "磅 ↔ 千克",
                "name_en": "Pound ↔ Kilogram"
            },
            "nm_km": {
                "factor": 1.852,
                "units_zh": ("海里", "公里"),
                "units_en": ("NM", "KM"),
                "name_zh": "海里 ↔ 公里",
                "name_en": "NM ↔ KM"
            },
            "knot_kmh": {
                "factor": 1.852,
                "units_zh": ("节", "千米/小时"),
                "units_en": ("Knot", "km/h"),
                "name_zh": "节 ↔ 千米/小时",
                "name_en": "Knot ↔ km/h"
            }
        }
        
        # 界面文本
        self.texts = {
            "zh": {
                "title": "飞行常用单位换算器",
                "select_type": "选择换算类型:",
                "language": "English",
                "clear": "清除",
                "input_hint": "输入数值..."
            },
            "en": {
                "title": "Aviation Unit Converter",
                "select_type": "Select Type:",
                "language": "中文",
                "clear": "Clear",
                "input_hint": "Enter value..."
            }
        }
        
        # 当前语言
        self.current_lang = "zh"
        
        # 防止循环更新的标志
        self.updating = False
        
        # 设置窗口
        self.title(self.texts[self.current_lang]["title"])
        self.geometry("520x380")
        self.resizable(False, False)


        # 设置主题
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # 创建界面
        self.create_widgets()
        
    def setup_fonts(self):
        """根据操作系统设置平滑字体"""
        system = platform.system()
        
        if system == "Windows":
            # Windows 使用微软雅黑
            self.font_family = "Microsoft YaHei UI"
            self.font_family_mono = "Consolas"
        elif system == "Darwin":
            # macOS 使用苹方
            self.font_family = "PingFang SC"
            self.font_family_mono = "SF Mono"
        else:
            # Linux 使用文泉驿或Noto
            self.font_family = "Noto Sans CJK SC"
            self.font_family_mono = "Noto Sans Mono"
        
        # 预定义字体样式
        self.fonts = {
            "title": ctk.CTkFont(family=self.font_family, size=18, weight="bold"),
            "heading": ctk.CTkFont(family=self.font_family, size=16, weight="bold"),
            "body": ctk.CTkFont(family=self.font_family, size=14),
            "input": ctk.CTkFont(family=self.font_family, size=20),
            "button": ctk.CTkFont(family=self.font_family, size=14),
            "symbol": ctk.CTkFont(family="Segoe UI Symbol", size=32) if system == "Windows" 
                      else ctk.CTkFont(family=self.font_family, size=32),
        }
        
    def create_widgets(self):
        # 主框架
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 顶部栏：标题和语言切换
        top_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            top_frame,
            text="⚖️",
            font=self.fonts["title"]
        )
        title_label.pack(side="left")
        
        self.title_text = ctk.CTkLabel(
            top_frame,
            text=self.texts[self.current_lang]["title"],
            font=self.fonts["title"]
        )
        self.title_text.pack(side="left", padx=(5, 0))
        
        self.lang_button = ctk.CTkButton(
            top_frame,
            text=self.texts[self.current_lang]["language"],
            width=90,
            height=32,
            font=self.fonts["button"],
            command=self.toggle_language
        )
        self.lang_button.pack(side="right")
        
        # 换算类型选择
        type_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        type_frame.pack(fill="x", pady=(0, 20))
        
        self.type_label = ctk.CTkLabel(
            type_frame,
            text=self.texts[self.current_lang]["select_type"],
            font=self.fonts["body"]
        )
        self.type_label.pack(side="left", padx=(0, 10))
        
        # 下拉菜单
        self.conversion_options = self.get_conversion_options()
        self.selected_type = ctk.StringVar(value=list(self.conversion_options.keys())[0])
        
        self.type_menu = ctk.CTkOptionMenu(
            type_frame,
            variable=self.selected_type,
            values=list(self.conversion_options.keys()),
            width=280,
            height=35,
            font=self.fonts["body"],
            dropdown_font=self.fonts["body"],
            command=self.on_type_change
        )
        self.type_menu.pack(side="left", fill="x", expand=True)
        
        # 换算区域
        convert_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        convert_frame.pack(fill="both", expand=True, pady=10)
        
        # 左侧单位
        left_frame = ctk.CTkFrame(convert_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=25, pady=25)
        
        self.left_label = ctk.CTkLabel(
            left_frame,
            text="",
            font=self.fonts["heading"],
            text_color=("#1E88E5", "#64B5F6")
        )
        self.left_label.pack(pady=(0, 12))
        
        self.left_entry = ctk.CTkEntry(
            left_frame,
            placeholder_text=self.texts[self.current_lang]["input_hint"],
            font=self.fonts["input"],
            height=55,
            corner_radius=10,
            justify="center"
        )
        self.left_entry.pack(fill="x")
        self.left_entry.bind("<KeyRelease>", self.on_left_change)
        
        # 中间箭头
        arrow_label = ctk.CTkLabel(
            convert_frame,
            text="⇄",
            font=self.fonts["symbol"],
            text_color=("#666666", "#AAAAAA")
        )
        arrow_label.pack(side="left", padx=5)
        
        # 右侧单位
        right_frame = ctk.CTkFrame(convert_frame, fg_color="transparent")
        right_frame.pack(side="left", fill="both", expand=True, padx=25, pady=25)
        
        self.right_label = ctk.CTkLabel(
            right_frame,
            text="",
            font=self.fonts["heading"],
            text_color=("#43A047", "#81C784")
        )
        self.right_label.pack(pady=(0, 12))
        
        self.right_entry = ctk.CTkEntry(
            right_frame,
            placeholder_text=self.texts[self.current_lang]["input_hint"],
            font=self.fonts["input"],
            height=55,
            corner_radius=10,
            justify="center"
        )
        self.right_entry.pack(fill="x")
        self.right_entry.bind("<KeyRelease>", self.on_right_change)
        
        # 清除按钮
        self.clear_button = ctk.CTkButton(
            self.main_frame,
            text=self.texts[self.current_lang]["clear"],
            font=self.fonts["button"],
            width=120,
            height=38,
            corner_radius=8,
            fg_color=("#E53935", "#C62828"),
            hover_color=("#C62828", "#B71C1C"),
            command=self.clear_entries
        )
        self.clear_button.pack(pady=18)
        
        # 初始化标签
        self.update_labels()
        
    def get_conversion_options(self) -> dict:
        """获取当前语言的换算选项"""
        lang_key = f"name_{self.current_lang}"
        return {
            self.conversions[key][lang_key]: key 
            for key in self.conversions
        }
        
    def get_current_conversion_key(self) -> str:
        """获取当前选择的换算类型的key"""
        selected_name = self.selected_type.get()
        return self.conversion_options.get(selected_name, "meter_feet")
    
    def update_labels(self):
        """更新单位标签"""
        conv_key = self.get_current_conversion_key()
        conv = self.conversions[conv_key]
        units = conv[f"units_{self.current_lang}"]
        self.left_label.configure(text=units[0])
        self.right_label.configure(text=units[1])
        
    def on_type_change(self, choice):
        """换算类型改变时"""
        self.update_labels()
        # 如果有输入值，重新计算
        if self.left_entry.get():
            self.on_left_change()
        elif self.right_entry.get():
            self.on_right_change()
        
    def on_left_change(self, event=None):
        """左侧输入变化时"""
        if self.updating:
            return
        self.updating = True
        
        try:
            value = self.left_entry.get()
            if value:
                num = float(value)
                conv_key = self.get_current_conversion_key()
                factor = self.conversions[conv_key]["factor"]
                result = num * factor
                
                self.right_entry.delete(0, "end")
                self.right_entry.insert(0, f"{result:.6g}")
            else:
                self.right_entry.delete(0, "end")
        except ValueError:
            pass
        
        self.updating = False
        
    def on_right_change(self, event=None):
        """右侧输入变化时"""
        if self.updating:
            return
        self.updating = True
        
        try:
            value = self.right_entry.get()
            if value:
                num = float(value)
                conv_key = self.get_current_conversion_key()
                factor = self.conversions[conv_key]["factor"]
                result = num / factor
                
                self.left_entry.delete(0, "end")
                self.left_entry.insert(0, f"{result:.6g}")
            else:
                self.left_entry.delete(0, "end")
        except ValueError:
            pass
        
        self.updating = False
        
    def clear_entries(self):
        """清除所有输入"""
        self.left_entry.delete(0, "end")
        self.right_entry.delete(0, "end")
        
    def toggle_language(self):
        """切换语言"""
        self.current_lang = "en" if self.current_lang == "zh" else "zh"
        
        # 保存当前选择的换算类型key
        current_key = self.get_current_conversion_key()
        
        # 更新界面文本
        self.title(self.texts[self.current_lang]["title"])
        self.title_text.configure(text=self.texts[self.current_lang]["title"])
        self.lang_button.configure(text=self.texts[self.current_lang]["language"])
        self.type_label.configure(text=self.texts[self.current_lang]["select_type"])
        self.clear_button.configure(text=self.texts[self.current_lang]["clear"])
        self.left_entry.configure(placeholder_text=self.texts[self.current_lang]["input_hint"])
        self.right_entry.configure(placeholder_text=self.texts[self.current_lang]["input_hint"])
        
        # 更新下拉菜单选项
        self.conversion_options = self.get_conversion_options()
        new_options = list(self.conversion_options.keys())
        self.type_menu.configure(values=new_options)
        
        # 恢复之前选择的类型
        new_name = self.conversions[current_key][f"name_{self.current_lang}"]
        self.selected_type.set(new_name)
        
        # 更新单位标签
        self.update_labels()


if __name__ == "__main__":
    app = UnitConverter()
    app.mainloop()
