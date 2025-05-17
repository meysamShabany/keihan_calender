import tkinter as tk
from tkinter import font as tkfont
from tkinter import ttk
import jdatetime
from persian_tools import digits

class KeihanCalendar(tk.Toplevel):
    def __init__(self, master=None, callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.withdraw()
        self.callback = callback
        
        self.title("تقویم کیهان")
        self.geometry("520x580")
        self.configure(bg='#040720')
        self.resizable(False, False)
        
        self.overrideredirect(True)
        self.grab_set()
        
        self.farsi_font = tkfont.Font(family="Tahoma", size=12)
        self.farsi_font_bold = tkfont.Font(family="Tahoma", size=12, weight="bold")
        self.farsi_font_large = tkfont.Font(family="Tahoma", size=14, weight="bold")
        
        self.main_frame = tk.Frame(self, bg='#040720')
        self.main_frame.pack(pady=15, padx=10, fill='both', expand=True)
        
        self.today = jdatetime.date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month
        self.selected_day = None
        
        self.create_year_month_selector()
        self.create_header()
        self.create_calendar_grid()
        self.create_time_selection()
        self.create_stars()
        self.update_calendar()

    def create_year_month_selector(self):
        selector_frame = tk.Frame(self.main_frame, bg='#040720')
        selector_frame.grid(row=0, column=0, columnspan=7, pady=(0, 15), sticky='ew')
        
        self.year_var = tk.StringVar()
        self.year_combobox = ttk.Combobox(
            selector_frame, 
            textvariable=self.year_var,
            font=self.farsi_font,
            width=8,
            state="readonly",
            style='Modern.TCombobox'
        )
        years = [str(i) for i in range(self.today.year - 10, self.today.year + 11)]
        self.year_combobox['values'] = [digits.convert_to_fa(y) for y in years]
        self.year_combobox.current(10)
        self.year_combobox.pack(side='right', padx=5)
        self.year_combobox.bind("<<ComboboxSelected>>", self.on_year_month_change)
        
        tk.Label(
            selector_frame, 
            text="سال:", 
            font=self.farsi_font,
            bg='#040720', 
            fg='#e0f2fe'
        ).pack(side='right', padx=5)
        
        self.month_var = tk.StringVar()
        self.month_combobox = ttk.Combobox(
            selector_frame, 
            textvariable=self.month_var,
            font=self.farsi_font,
            width=8,
            state="readonly",
            style='Modern.TCombobox'
        )
        months = [
            'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
            'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'
        ]
        self.month_combobox['values'] = months
        self.month_combobox.current(self.current_month - 1)
        self.month_combobox.pack(side='right', padx=5)
        self.month_combobox.bind("<<ComboboxSelected>>", self.on_year_month_change)
        
        tk.Label(
            selector_frame, 
            text="ماه:", 
            font=self.farsi_font,
            bg='#040720', 
            fg='#e0f2fe'
        ).pack(side='right', padx=5)

    def on_year_month_change(self, event=None):
        self.current_year = int(digits.convert_to_en(self.year_var.get()))
        self.current_month = self.month_combobox.current() + 1
        self.update_calendar()

    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg='#040720')
        header_frame.grid(row=1, column=0, columnspan=7, pady=(0, 10))
        

        self.prev_button = tk.Button(
            header_frame, text="◀", command=self.prev_month,
            font=self.farsi_font_large, bg='#0c4a6e', fg='#7dd3fc',
            relief='flat', borderwidth=0
        )
        self.prev_button.pack(side='right', padx=5)
        

        self.month_year_label = tk.Label(
            header_frame, 
            font=self.farsi_font_bold, 
            bg='#040720', 
            fg='#7dd3fc'
        )
        self.month_year_label.pack(side='right', padx=10)

        self.next_button = tk.Button(
            header_frame, text="▶", command=self.next_month,
            font=self.farsi_font_large, bg='#0c4a6e', fg='#7dd3fc',
            relief='flat', borderwidth=0
        )
        self.next_button.pack(side='right', padx=5)

    def create_calendar_grid(self):
        """ایجاد شبکه تقویم"""
        weekdays = ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج']
        
        for i, day in enumerate(weekdays):
            label = tk.Label(
                self.main_frame, 
                text=day, 
                font=self.farsi_font_bold,
                bg='#0c4a6e',
                fg='#bae6fd',
                width=5, 
                height=2,
                relief='ridge',
                borderwidth=1
            )
            label.grid(row=2, column=i, padx=2, pady=2, sticky="nsew")
        
        self.day_boxes = []
        for row in range(6):
            row_boxes = []
            for col in range(7):
                box = tk.Label(
                    self.main_frame, 
                    text="", 
                    font=self.farsi_font,
                    bg='#040720',
                    fg='#e0f2fe',
                    width=5, 
                    height=2,
                    relief='ridge',
                    borderwidth=1,
                    highlightbackground='#0c4a6e'
                )
                box.grid(row=row+3, column=col, padx=2, pady=2, sticky="nsew")
                box.bind("<Button-1>", lambda e, r=row, c=col: self.select_day(r, c))
                row_boxes.append(box)
            self.day_boxes.append(row_boxes)
        
        for i in range(7):
            self.main_frame.grid_columnconfigure(i, weight=1)
        for i in range(9):
            self.main_frame.grid_rowconfigure(i, weight=1)

    def create_time_selection(self):
        time_frame = tk.Frame(self.main_frame, bg='#040720')
        time_frame.grid(row=9, column=0, columnspan=7, pady=(20, 10))
        
        self.hour_var = tk.StringVar()
        self.hour_combobox = ttk.Combobox(
            time_frame, 
            textvariable=self.hour_var,
            font=self.farsi_font,
            width=5,
            state="readonly",
            style='Modern.TCombobox'
        )
        self.hour_combobox['values'] = [digits.convert_to_fa(f"{i:02d}") for i in range(24)]
        self.hour_combobox.current(0)
        self.hour_combobox.pack(side='right', padx=5)
        
        tk.Label(
            time_frame, 
            text="ساعت:", 
            font=self.farsi_font,
            bg='#040720', 
            fg='#e0f2fe'
        ).pack(side='right', padx=5)
        
        self.minute_var = tk.StringVar()
        self.minute_combobox = ttk.Combobox(
            time_frame, 
            textvariable=self.minute_var,
            font=self.farsi_font,
            width=5,
            state="readonly",
            style='Modern.TCombobox'
        )
        self.minute_combobox['values'] = [digits.convert_to_fa(f"{i:02d}") for i in range(0, 60, 10)]
        self.minute_combobox.current(0)
        self.minute_combobox.pack(side='right', padx=5)
        
        tk.Label(
            time_frame, 
            text="دقیقه:", 
            font=self.farsi_font,
            bg='#040720', 
            fg='#e0f2fe'
        ).pack(side='right', padx=5)
        
        confirm_btn = ttk.Button(
            time_frame, 
            text="تأیید", 
            command=self.confirm_selection,
            style='Modern.TButton'
        )
        confirm_btn.pack(side='left', padx=10)

    def create_stars(self):
        stars_frame = tk.Frame(self.main_frame, bg='#040720')
        stars_frame.grid(row=10, column=0, columnspan=7, pady=(10, 0))
        
        stars = ["✦", "✧", "✺", "✹", "✷"]
        for i in range(20):
            star = tk.Label(
                stars_frame, 
                text=stars[i % len(stars)], 
                fg='#7dd3fc', 
                bg='#040720', 
                font=("Arial", 10)
            )
            star.pack(side='left', expand=True)

    def select_day(self, row, col):
        """انتخاب روز از تقویم"""
        if hasattr(self, 'selected_box'):
            self.selected_box.config(bg='#040720', fg='#e0f2fe')
        
        day_text = self.day_boxes[row][col].cget("text")
        if not day_text:
            return
        
        self.selected_day = int(digits.convert_to_en(day_text))
        self.selected_box = self.day_boxes[row][col]
        self.selected_box.config(bg='#075985', fg='#f0f9ff', font=self.farsi_font_bold)

    def confirm_selection(self):
        if not self.selected_day:
            return
        
        month_name = jdatetime.date(self.current_year, self.current_month, 1).strftime("%B")
        hour = digits.convert_to_en(self.hour_var.get())
        minute = digits.convert_to_en(self.minute_var.get())
        
        date_str = (
            f"{digits.convert_to_fa(str(self.selected_day))} {month_name} "
            f"{digits.convert_to_fa(str(self.current_year))} - "
            f"{digits.convert_to_fa(hour)}:{digits.convert_to_fa(minute)}"
        )
        
        if self.callback:
            self.callback(date_str)
        self.hide_calendar()

    def update_calendar(self):
        month_name = jdatetime.date(self.current_year, self.current_month, 1).strftime("%B")
        self.month_year_label.config(text=f"{digits.convert_to_fa(str(self.current_year))} {month_name}")
        
        self.year_var.set(digits.convert_to_fa(str(self.current_year)))
        self.month_combobox.current(self.current_month - 1)
        
        first_day = jdatetime.date(self.current_year, self.current_month, 1)
        start_weekday = first_day.weekday()
        month_days = jdatetime.j_days_in_month[self.current_month - 1]
        
        if self.current_month == 12 and first_day.isleap():
            month_days = 30
        
        self.selected_day = None
        if hasattr(self, 'selected_box'):
            self.selected_box.config(bg='#040720', fg='#e0f2fe')
            del self.selected_box
        
        for row in self.day_boxes:
            for box in row:
                box.config(text="", bg='#040720', fg='#e0f2fe')
        
        day = 1
        for row in range(6):
            for col in range(7):
                if (row == 0 and col < start_weekday) or day > month_days:
                    continue
                
                box = self.day_boxes[row][col]
                box.config(text=digits.convert_to_fa(str(day)))
                
                if (self.current_year == self.today.year and 
                    self.current_month == self.today.month and 
                    day == self.today.day):
                    box.config(bg='#7dd3fc', fg='#040720', font=self.farsi_font_bold)
                
                day += 1

    def show_calendar(self, x=0, y=0):
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        window_width = self.winfo_reqwidth()
        pos_x = screen_width - window_width - 100
        
        self.deiconify()
        self.geometry(f"+{pos_x}+20")
        self.lift()

        self.selected_day = None
        if hasattr(self, 'selected_box'):
            self.selected_box.config(bg='#040720', fg='#e0f2fe')
            del self.selected_box
        self.hour_combobox.current(0)
        self.minute_combobox.current(0)

    def hide_calendar(self):
        self.withdraw()
        self.grab_release()

    def prev_month(self):
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.update_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.update_calendar()


class PersianDatePicker(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.style = ttk.Style()
        self.style.configure('Modern.TCombobox', 
                           foreground='#333333',
                           fieldbackground='#ffffff',
                           selectbackground='#e0f2fe',
                           selectforeground='#075985',
                           font=('Tahoma', 11))
        
        self.style.configure('Modern.TButton', 
                           foreground='#ffffff',
                           background='#075985',
                           font=('Tahoma', 10, 'bold'),
                           padding=5)
        
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(
            self,
            textvariable=self.entry_var,
            font=('Tahoma', 12),
            width=20
        )
        self.entry.pack(side='left', padx=(0, 5), fill='both', expand=True)
        

        self.calendar_btn = ttk.Button(
            self,
            text="تقویم",
            command=self.show_calendar,
            style='Modern.TButton'
        )
        self.calendar_btn.pack(side='right')
        

        self.calendar = None
    
    def show_calendar(self):
        if self.calendar is None or not self.calendar.winfo_exists():
            self.calendar = KeihanCalendar(self.winfo_toplevel(), self.set_date)
        
        x = self.winfo_rootx() + self.winfo_width() - 520
        y = self.winfo_rooty() + self.winfo_height()
        self.calendar.show_calendar(x, y)
    
    def set_date(self, date_str):
        self.entry_var.set(date_str)
    
    def get(self):
        return self.entry_var.get()



if __name__ == "__main__":
    root = tk.Tk()
    root.title("تقویم فارسی کیهان - نسخه نهایی")
    root.geometry("400x250")
    

    style = ttk.Style()
    style.theme_use('clam')
    
    main_frame = ttk.Frame(root)
    main_frame.pack(pady=30, padx=20, fill='both', expand=True)
    
    label = ttk.Label(
        main_frame, 
        text="تاریخ را انتخاب کنید:", 
        font=("Tahoma", 12)
    )
    label.pack(pady=(0, 15))
    
    date_picker = PersianDatePicker(main_frame)
    date_picker.pack(fill='x')
    

    def show_selected_date():
        from tkinter import messagebox
        messagebox.showinfo("تاریخ انتخاب شده", date_picker.get())
    
    show_btn = ttk.Button(
        main_frame,
        text="نمایش تاریخ انتخاب شده",
        command=show_selected_date,
        style='Modern.TButton'
    )
    show_btn.pack(pady=20)
    
    root.mainloop()