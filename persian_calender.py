import tkinter as tk
from tkinter import ttk, font
import jdatetime
from datetime import datetime
from tkinter import messagebox

class PersianCalendar:
    def __init__(self, root):
        self.root = root
        self.root.title("تقویم فارسی")
        self.root.geometry("400x500")
        self.root.resizable(True, True)
        
        self.farsi_font = font.Font(family="Vazir", size=10)
        self.farsi_font_bold = font.Font(family="Vazir", size=10, weight="bold")
        self.farsi_font_large = font.Font(family="Vazir", size=12, weight="bold")
        
        self.colors = {
            'primary': '#008080',
            'secondary': '#4B0082',
            'background': '#F0F8FF',
            'text': '#333333',
            'today': '#FFD700',
            'weekend': '#FF6347',
            'header': '#FFFFFF',
            'button': '#5F9EA0'
        }
        
        self.setup_ui()
        self.update_calendar()
        
    def setup_ui(self):
        self.main_frame = tk.Frame(self.root, bg=self.colors['background'])
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.today_label = tk.Label(
            self.main_frame,
            text=self.get_persian_date(jdatetime.date.today()),
            font=self.farsi_font_large,
            bg=self.colors['primary'],
            fg=self.colors['header'],
            pady=10
        )
        self.today_label.pack(fill=tk.X)
        
        self.control_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        self.control_frame.pack(fill=tk.X, pady=(10, 5))
        
        self.month_label = tk.Label(
            self.control_frame,
            text=": ماه",
            font=self.farsi_font,
            bg=self.colors['background']
        )
        self.month_label.pack(side=tk.RIGHT, padx=5)
        
        self.month_var = tk.StringVar()
        self.month_cb = ttk.Combobox(
            self.control_frame,
            textvariable=self.month_var,
            values=self.get_persian_months(),
            font=self.farsi_font,
            state="readonly",
            width=10
        )
        self.month_cb.pack(side=tk.RIGHT)
        self.month_cb.set(self.get_persian_month_name(jdatetime.date.today().month))
        self.month_cb.bind("<<ComboboxSelected>>", lambda e: self.update_calendar())
        
        self.year_label = tk.Label(
            self.control_frame,
            text=": سال",
            font=self.farsi_font,
            bg=self.colors['background']
        )
        self.year_label.pack(side=tk.RIGHT, padx=5)
        
        self.year_var = tk.StringVar()
        self.year_cb = ttk.Combobox(
            self.control_frame,
            textvariable=self.year_var,
            values=[str(year) for year in range(1330, 1500)],
            font=self.farsi_font,
            state="readonly",
            width=8
        )
        self.year_cb.pack(side=tk.RIGHT)
        self.year_cb.set(str(jdatetime.date.today().year))
        self.year_cb.bind("<<ComboboxSelected>>", lambda e: self.update_calendar())
        
        self.weekdays_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        self.weekdays_frame.pack(fill=tk.X, pady=(5, 0))
        
        weekdays = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه']
        for day in weekdays:
            day_label = tk.Label(
                self.weekdays_frame,
                text=day,
                font=("Arial", 12),
                bg=self.colors['secondary'],
                fg=self.colors['header'],
                width=4,
                pady=5
            )
            day_label.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.calendar_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)
        
        self.time_frame = tk.Frame(self.main_frame, bg=self.colors['background'])
        self.time_frame.pack(fill=tk.X, pady=(10, 5))
        
        self.minute_label = tk.Label(
            self.time_frame,
            text="دقیقه:",
            font=self.farsi_font,
            bg=self.colors['background']
        )
        self.minute_label.pack(side=tk.RIGHT, padx=5)
        
        self.minute_var = tk.StringVar()
        self.minute_cb = ttk.Combobox(
            self.time_frame,
            textvariable=self.minute_var,
            values=[f"{i:02d}" for i in range(0, 60, 5)],
            font=self.farsi_font,
            state="readonly",
            width=4
        )
        self.minute_cb.pack(side=tk.RIGHT)
        
        self.hour_label = tk.Label(
            self.time_frame,
            text="ساعت:",
            font=self.farsi_font,
            bg=self.colors['background']
        )
        self.hour_label.pack(side=tk.RIGHT, padx=5)
        
        self.hour_var = tk.StringVar()
        self.hour_cb = ttk.Combobox(
            self.time_frame,
            textvariable=self.hour_var,
            values=[f"{i:02d}" for i in range(0, 24)],
            font=self.farsi_font,
            state="readonly",
            width=4
        )
        self.hour_cb.pack(side=tk.RIGHT)
        
        self.date_entry = tk.Entry(
            self.main_frame,
            font=self.farsi_font,
            justify=tk.CENTER,
            bd=2,
            relief=tk.GROOVE
        )
        self.date_entry.pack(fill=tk.X, pady=(5, 10), ipady=5)
        
        now = datetime.now()
        self.hour_var.set(f"{now.hour:02d}")
        self.minute_var.set(f"{now.minute - now.minute % 5:02d}")
        
    def get_persian_date(self, date):
        months = self.get_persian_months()
        return str(date.day) + str(months[date.month - 1]) + str(date.year)
    
    def get_persian_months(self):
        return [
            'فروردین', 'اردیبهشت', 'خرداد', 
            'تیر', 'مرداد', 'شهریور', 
            'مهر', 'آبان', 'آذر', 
            'دی', 'بهمن', 'اسفند'
        ]
    
    def get_persian_month_name(self, month):
        return self.get_persian_months()[month - 1]
    
    def update_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        try:
            year = int(self.year_var.get())
            month = self.get_persian_months().index(self.month_var.get()) + 1
        except:
            messagebox.showerror("خطا", "لطفاً سال و ماه معتبر انتخاب کنید")
            return
        
        first_day = jdatetime.date(year, month, 1)
        
        if month == 12 and not first_day.isleap():
            days_in_month = 29
        else:
            days_in_month = 30 if month <= 6 else 29
        
        weekday = first_day.weekday()
        
        row, col = 0, 0
        today = jdatetime.date.today()
        
        for i in range(weekday):
            empty_label = tk.Label(
                self.calendar_frame,
                text="",
                bg=self.colors['background'],
                width=4,
                height=2
            )
            empty_label.grid(row=row, column=col, padx=2, pady=2)
            col += 1
        
        for day in range(1, days_in_month + 1):
            current_date = jdatetime.date(year, month, day)
            is_today = current_date == today
            is_weekend = current_date.weekday() == 6 
            
            if is_today:
                bg_color = self.colors['today']
                fg_color = '#000000'
            elif is_weekend:
                bg_color = self.colors['weekend']
                fg_color = '#FFFFFF'
            else:
                bg_color = self.colors['primary']
                fg_color = self.colors['header']
            
            day_btn = tk.Button(
                self.calendar_frame,
                text=str(day),
                font=self.farsi_font,
                bg=bg_color,
                fg=fg_color,
                width=5,
                height=2,
                relief=tk.FLAT,
                command=lambda d=day: self.select_date(d)
            )
            day_btn.grid(row=row, column=col, padx=2, pady=2)
            
            col += 1
            if col > 6:
                col = 0
                row += 1
        
        while col < 7:
            empty_label = tk.Label(
                self.calendar_frame,
                text="",
                bg=self.colors['background'],
                width=4,
                height=2
            )
            empty_label.grid(row=row, column=col)
            col += 1
    
    def select_date(self, day):
        try:
            year = int(self.year_var.get())
            month = self.get_persian_months().index(self.month_var.get()) + 1
            
            hour = self.hour_var.get()
            minute = self.minute_var.get()
            
            if not hour or not minute:
                now = datetime.now()
                hour = now.hour
                minute = now.minute
            else:
                hour = int(hour)
                minute = int(minute)
            
            selected_date = jdatetime.datetime(year, month, day, hour, minute)
            date_str = selected_date.strftime("%Y/%m/%d %H:%M")
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, date_str)
            
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در انتخاب تاریخ: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PersianCalendar(root)
    root.mainloop()