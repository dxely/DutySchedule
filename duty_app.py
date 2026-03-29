"""
我的值班表 - Android 应用
使用 Kivy 框架开发，可打包成 APK

安装依赖：
pip install kivy

打包 APK：
pip install buildozer
buildozer init
buildozer android debug
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from datetime import datetime, timedelta
from calendar import monthrange

# 窗口设置
Window.clearcolor = (0.4, 0.49, 0.92, 1)  # #667eea

# ==================== 你的个人排班配置 ====================
FIRST_DUTY_DATE = datetime(2026, 3, 31)  # 首次值班日期
DUTY_CYCLE = 4  # 每 4 天值班一次
DUTY_TIME = "9:00 - 次日 9:00"
NORMAL_TIME = "9:00 - 18:00"

# 2026 年法定节假日
HOLIDAYS_2026 = {
    (2026, 1, 1): "元旦",
    (2026, 2, 17): "春节", (2026, 2, 18): "春节", (2026, 2, 19): "春节",
    (2026, 2, 20): "春节", (2026, 2, 21): "春节", (2026, 2, 22): "春节", (2026, 2, 23): "春节",
    (2026, 4, 5): "清明节", (2026, 4, 6): "清明节", (2026, 4, 7): "清明节",
    (2026, 5, 1): "劳动节", (2026, 5, 2): "劳动节", (2026, 5, 3): "劳动节",
    (2026, 5, 4): "劳动节", (2026, 5, 5): "劳动节",
    (2026, 6, 19): "端午节", (2026, 6, 20): "端午节", (2026, 6, 21): "端午节",
    (2026, 9, 25): "中秋节", (2026, 9, 26): "中秋节", (2026, 9, 27): "中秋节",
    (2026, 10, 1): "国庆节", (2026, 10, 2): "国庆节", (2026, 10, 3): "国庆节",
    (2026, 10, 4): "国庆节", (2026, 10, 5): "国庆节", (2026, 10, 6): "国庆节",
    (2026, 10, 7): "国庆节", (2026, 10, 8): "国庆节"
}
# =========================================================


def is_duty_day(date):
    """判断是否是值班日"""
    diff_days = (date - FIRST_DUTY_DATE).days
    return diff_days >= 0 and diff_days % DUTY_CYCLE == 0


def is_weekend(date):
    """判断是否是周末"""
    return date.weekday() >= 5  # 5=周六，6=周日


def is_holiday(date):
    """判断是否是法定节假日"""
    key = (date.year, date.month, date.day)
    return HOLIDAYS_2026.get(key)


def get_shift_info(date):
    """获取班次信息"""
    holiday = is_holiday(date)
    duty = is_duty_day(date)
    weekend = is_weekend(date)
    
    if holiday:
        if duty:
            return f"节假日值班 ({holiday})", (1, 0.34, 0.13, 1), DUTY_TIME  # #ff5722
        else:
            return f"{holiday} 休息", (0.91, 0.12, 0.39, 1), "-"  # #e91e63
    
    if duty and weekend:
        return "周末值班", (0.61, 0.15, 0.69, 1), DUTY_TIME  # #9c27b0
    
    if duty:
        return "值班", (1, 0.59, 0, 1), DUTY_TIME  # #ff9800
    
    if weekend:
        return "休息", (0.13, 0.59, 0.95, 1), "-"  # #2196F3
    
    return "正常班", (0.3, 0.69, 0.31, 1), NORMAL_TIME  # #4CAF50


class CalendarDay(BoxLayout):
    """日历中的每一天"""
    def __init__(self, date, is_today=False, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=60, **kwargs)
        
        self.date = date
        shift_text, color, time = get_shift_info(date)
        
        # 日期标签
        date_label = Label(
            text=f"{date.month}/{date.day}",
            size_hint_y=None,
            height=25,
            font_size=16,
            bold=True
        )
        if is_today:
            date_label.color = (1, 0.84, 0, 1)  # 黄色高亮今天
        
        # 星期标签
        weekday = ["一", "二", "三", "四", "五", "六", "日"][date.weekday()]
        weekday_label = Label(
            text=f"周{weekday}",
            size_hint_y=None,
            height=20,
            font_size=12
        )
        
        # 班次标签
        shift_label = Label(
            text=shift_text,
            size_hint_y=None,
            height=15,
            font_size=10
        )
        
        self.add_widget(date_label)
        self.add_widget(weekday_label)
        self.add_widget(shift_label)
        
        # 设置背景色
        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class DutyScheduleApp(App):
    """值班表应用主类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_date = datetime.now()
    
    def build(self):
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(
            text="📅 我的值班表",
            size_hint_y=None,
            height=50,
            font_size=24,
            bold=True,
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(title)
        
        # 信息卡片
        info_box = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        with info_box.canvas.before:
            Color(0.94, 0.58, 0.98, 1)  # #f093fb
            info_box.rect = Rectangle(size=info_box.size, pos=info_box.pos)
        info_box.bind(size=lambda i, v: setattr(info_box.rect, 'size', v),
                     pos=lambda i, v: setattr(info_box.rect, 'pos', v))
        
        info_label = Label(
            text=f"值班周期：每{DUTY_CYCLE}天一次\n值班时间：{DUTY_TIME}\n首次值班：{FIRST_DUTY_DATE.strftime('%Y年%m月%d日')}",
            color=(1, 1, 1, 1),
            font_size=14
        )
        info_box.add_widget(info_label)
        main_layout.add_widget(info_box)
        
        # 下一次值班提示
        next_shift = self.get_next_shift()
        next_box = BoxLayout(size_hint_y=None, height=100)
        with next_box.canvas.before:
            Color(1, 0.58, 0.42, 1)  # #f5576c
            next_box.rect = Rectangle(size=next_box.size, pos=next_box.pos)
        next_box.bind(size=lambda i, v: setattr(next_box.rect, 'size', v),
                     pos=lambda i, v: setattr(next_box.rect, 'pos', v))
        
        next_label = Label(
            text=f"⏰ 下次值班：{next_shift[0]}\n{next_shift[1]}\n{next_shift[2]}",
            color=(1, 1, 1, 1),
            font_size=16,
            halign='left',
            valign='middle'
        )
        next_box.add_widget(next_label)
        main_layout.add_widget(next_box)
        
        # 月份控制
        control_layout = BoxLayout(size_hint_y=None, height=50, spacing=5)
        
        prev_btn = Button(text="◀ 上月", font_size=14)
        prev_btn.bind(on_press=self.prev_month)
        control_layout.add_widget(prev_btn)
        
        month_label = Label(
            text=f"{self.current_date.year}年{self.current_date.month}月",
            font_size=18,
            bold=True,
            size_hint_x=2
        )
        self.month_label = month_label
        control_layout.add_widget(month_label)
        
        today_btn = Button(text="今天", font_size=14)
        today_btn.bind(on_press=self.go_today)
        control_layout.add_widget(today_btn)
        
        next_btn = Button(text="下月 ▶", font_size=14)
        next_btn.bind(on_press=self.next_month)
        control_layout.add_widget(next_btn)
        
        main_layout.add_widget(control_layout)
        
        # 日历网格
        scroll_view = ScrollView()
        calendar_grid = GridLayout(cols=7, spacing=2, size_hint_y=None)
        calendar_grid.bind(minimum_height=calendar_grid.setter('height'))
        
        # 星期标题
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        for day in weekdays:
            header = Label(
                text=f"周{day}",
                size_hint_y=None,
                height=30,
                font_size=14,
                bold=True,
                color=(0.2, 0.2, 0.2, 1)
            )
            calendar_grid.add_widget(header)
        
        # 日期格子
        self.calendar_grid = calendar_grid
        self.update_calendar()
        
        scroll_view.add_widget(calendar_grid)
        main_layout.add_widget(scroll_view)
        
        # 图例
        legend_layout = BoxLayout(size_hint_y=None, height=40, spacing=5)
        legend_items = [
            ("正常班", (0.3, 0.69, 0.31, 1)),
            ("值班", (1, 0.59, 0, 1)),
            ("休息", (0.13, 0.59, 0.95, 1)),
            ("节假日", (0.91, 0.12, 0.39, 1))
        ]
        for text, color in legend_items:
            box = BoxLayout(size_hint_x=None, width=80)
            with box.canvas.before:
                Color(*color)
                box.rect = Rectangle(size=box.size, pos=box.pos)
            box.bind(size=lambda i, v: setattr(box.rect, 'size', v),
                    pos=lambda i, v: setattr(box.rect, 'pos', v))
            label = Label(text=text, font_size=10)
            box.add_widget(label)
            legend_layout.add_widget(box)
        
        main_layout.add_widget(legend_layout)
        
        return main_layout
    
    def get_next_shift(self):
        """获取下一次值班信息"""
        today = datetime.now()
        next_duty = FIRST_DUTY_DATE
        
        while next_duty <= today:
            next_duty += timedelta(days=DUTY_CYCLE)
        
        shift_text, color, time = get_shift_info(next_duty)
        weekday = ["一", "二", "三", "四", "五", "六", "日"][next_duty.weekday()]
        
        return (
            f"{next_duty.month}月{next_duty.day}日 周{weekday}",
            shift_text,
            f"时间：{time}"
        )
    
    def update_calendar(self):
        """更新日历显示"""
        self.calendar_grid.clear_widgets()
        
        # 星期标题
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        for day in weekdays:
            header = Label(
                text=f"周{day}",
                size_hint_y=None,
                height=30,
                font_size=14,
                bold=True
            )
            self.calendar_grid.add_widget(header)
        
        # 获取当月第一天和天数
        first_weekday, days_in_month = monthrange(self.current_date.year, self.current_date.month)
        
        # 填充上个月的空白
        for i in range(first_weekday):
            placeholder = Label(text="", size_hint_y=None, height=60)
            self.calendar_grid.add_widget(placeholder)
        
        # 添加当月日期
        today = datetime.now()
        for day in range(1, days_in_month + 1):
            date = datetime(self.current_date.year, self.current_date.month, day)
            is_today = (date.date() == today.date())
            calendar_day = CalendarDay(date, is_today=is_today)
            self.calendar_grid.add_widget(calendar_day)
        
        # 更新月份标签
        self.month_label.text = f"{self.current_date.year}年{self.current_date.month}月"
    
    def prev_month(self, instance):
        """上个月"""
        if self.current_date.month == 1:
            self.current_date = datetime(self.current_date.year - 1, 12, 1)
        else:
            self.current_date = datetime(self.current_date.year, self.current_date.month - 1, 1)
        self.update_calendar()
    
    def next_month(self, instance):
        """下个月"""
        if self.current_date.month == 12:
            self.current_date = datetime(self.current_date.year + 1, 1, 1)
        else:
            self.current_date = datetime(self.current_date.year, self.current_date.month + 1, 1)
        self.update_calendar()
    
    def go_today(self, instance):
        """回到今天"""
        self.current_date = datetime.now()
        self.update_calendar()


if __name__ == '__main__':
    DutyScheduleApp().run()
