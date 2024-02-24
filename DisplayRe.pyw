# -*- coding: utf-8 -*-
import os
import time
import datetime
import json
import configparser
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import tkinter.colorchooser as colorchooser
import tkinter.font as font

if len(os.listdir("./Libs/resource")) >= 3:
    try:
        language_config = configparser.ConfigParser()
        language_config.read("./Libs/resource/language.ini", encoding="utf-8")
        language_choose = configparser.ConfigParser()
        language_choose.read("./Libs/resource/settings.ini", encoding="utf-8")
        languages = language_choose.get("program", "language")
        del language_choose
    except Exception as error:
        tkinter.messagebox.showerror("Error", f"During read configure file\n{type(error)} -> {error}")
        exit(-1)

    if languages not in language_config.sections():
        tkinter.messagebox.showerror(
            "Error",
            f"not found the languages '{languages}' "
            f"sections in languages.ini,\n"
            f"Please change the language option in the settings.ini file to the correct language option"
        )
        exit(-1)

    try:
        with open('./Libs/resource/class.json', 'r', encoding='utf-8') as json_file:
            json_data = json_file.read()

    except UnicodeDecodeError:
        try:
            with open('./Libs/resource/class.json', 'r', encoding='gbk') as json_file:
                json_data = json_file.read()
        except UnicodeDecodeError:
            tkinter.messagebox.showerror("Error", "No any encoding can encode the 'class.json'")
            exit(-1)

    except OSError:
        tkinter.messagebox.showerror(
            language_config.get(
                languages,
                "errrortitle"
            ),
            language_config.get(languages, "errrormsg")
        )
        exit(-1)
    try:
        class_ = json.loads(json_data)
        del json_data

    except Exception as error:
        tkinter.messagebox.showerror("Error", f"Cannot evaluate the class.json file\n{type(error)} -> {error}")
        exit(-1)

else:
    lost_file = ""
    listfile = os.listdir("./Libs/resource")
    if "class.json" not in listfile:
        lost_file = "class.json"

    elif "settings.ini" not in listfile:
        lost_file = "settings.ini"

    else:
        lost_file = "language.ini"
    tkinter.messagebox.showerror(
        "Error",
        f"The folder '{os.getcwd()}\\Libs\\resource "
        f"impantant children files lost\n\n"
        f"The folder length should be 4, but the folder length is {len(os.listdir('./Libs/resource'))}\n\n"
        f"Maybe you lost {lost_file}"
    )
    exit(-1)


class Clock(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.config = configparser.ConfigParser()
        self.config.read(f"{os.getcwd()}/Libs/resource/settings.ini", encoding="utf-8")

        self.size = self.config.get("fgwindow", "size")
        self.trans = self.config.get("fgwindow", "trans")
        self.fg_color = self.config.get("fgwindow", "color")
        self.type = self.config.get("fgwindow", "type")
        self.c = self.config.get("fgwindow", "state")
        self.c = self.c.replace("{", "").replace("}", "").split(",")
        self.bg_color = self.config.get("bgwindow", "color")

        self.attributes("-topmost", True)
        self.geometry(f"+0+0")
        self.overrideredirect(True)
        self.attributes("-alpha", float(self.trans))

        self.lbl = tk.Label(self,
                            text="",
                            font=(self.type, self.size, [c for c in self.c]),
                            background=self.bg_color,
                            foreground=self.fg_color)
        self.menu = tk.Menu(self)
        self.menu.add_cascade(label=language_config.get(languages, 'settings'), command=lambda: Setting.open())
        self.menu.add_cascade(label=language_config.get(languages, 'exit'), command=lambda: os.kill(os.getpid(), 0))

        self.stateus = self.c
        self.Pause = False
        self.click_times = 0
        self.subject = "未知"
        self.end_time = None
        self.states = [
            language_config.get(languages, "statef"),
            language_config.get(languages, "states"),
            language_config.get(languages, "statet")
        ]

        # 设置的界面
        self.notebook = ttk.Notebook(self)
        self.basic_frame = tk.Frame(self.notebook)
        self.advanced_frame = tk.Frame(self.notebook)
        self.class_frame = tk.Frame(self.notebook)

        self.date_notebook = ttk.Notebook(self.class_frame)
        self.Monday_frame = tk.Frame(self.date_notebook)
        self.Tuesday_frame = tk.Frame(self.date_notebook)
        self.Wednesday_frame = tk.Frame(self.date_notebook)
        self.Thursday_frame = tk.Frame(self.date_notebook)
        self.Friday_frame = tk.Frame(self.date_notebook)
        self.Saturday_frame = tk.Frame(self.date_notebook)
        self.Sunday_frame = tk.Frame(self.date_notebook)
        self.notebook.add(self.basic_frame, text=language_config.get(languages, "setfg"))
        self.notebook.add(self.advanced_frame, text=language_config.get(languages, "setfont"))
        self.notebook.add(self.class_frame, text=language_config.get(languages, "curriculum"))
        # 日期
        self.date_notebook.add(self.Monday_frame, text=language_config.get(languages, "monday"))
        self.date_notebook.add(self.Tuesday_frame, text=language_config.get(languages, "tuesday"))
        self.date_notebook.add(self.Wednesday_frame, text=language_config.get(languages, "wednesday"))
        self.date_notebook.add(self.Thursday_frame, text=language_config.get(languages, "thursday"))
        self.date_notebook.add(self.Friday_frame, text=language_config.get(languages, "friday"))
        self.date_notebook.add(self.Saturday_frame, text=language_config.get(languages, "saturday"))
        self.date_notebook.add(self.Sunday_frame, text=language_config.get(languages, "sunday"))
        # 课表设置
        self.info_text = tk.Text(self.class_frame, width=45, height=5)
        self.date_treeview_list = []
        columns = {"ID": 50, "星期": 100, "科目名称": 80, "开始时间": 80, "结束时间": 80, "状态": 80}
        for d in [
            self.Monday_frame, self.Tuesday_frame,
            self.Wednesday_frame, self.Thursday_frame,
            self.Friday_frame, self.Saturday_frame,
            self.Sunday_frame
        ]:
            tree = ttk.Treeview(d, show="headings", columns=list(columns))
            for text, width in columns.items():
                tree.heading(text, text=text, anchor='center')
                tree.column(text, anchor='center', width=width, stretch=False)
            self.date_treeview_list.append(tree)
        del tree
        self.status_btn = tk.Button(self.class_frame, text=language_config.get(languages, "disable"), command=Setting.change_status)

        # 基础设置
        self.size_font_label = tk.Label(self.basic_frame, text=language_config.get(languages, "floatingsize"))
        self.size_font_combo = ttk.Combobox(
            self.basic_frame,
            values=list(map(lambda v: str(v), range(1, 501))),
            width=9,
            state="readonly"
        )
        self.trans_font_label = tk.Label(self.basic_frame, text=language_config.get(languages, "floatingtrans"))
        self.trans_font_scale = tk.Scale(
            self.basic_frame,
            resolution=0.01,
            from_=0.01,
            to=1,
            orient=tk.HORIZONTAL,
            command=Setting.view
        )
        self.state_font_label = tk.Label(self.basic_frame, text=language_config.get(languages, "floatingstate"))
        self.state_font_combo = ttk.Combobox(
            self.basic_frame,
            values=['normal', 'bold', 'overstrike', 'italic', 'underline'],
            width=12,
            state="readonly"
        )
        self.state_value = tk.BooleanVar()
        if len(self.c) > 1:
            self.state_value.set(True)
        else:
            self.state_value.set(False)
        self.more_state_checkbtn = tk.Checkbutton(
            self.basic_frame,
            text=language_config.get(languages, "stateus_append"),
            variable=self.state_value,
            onvalue=True,
            offvalue=False
        )
        self.fore_color_label = tk.Label(self.basic_frame, text=language_config.get(languages, "floatingcolor"))
        self.fore_color_btn = tk.Button(
            self.basic_frame,
            text=language_config.get(languages, "choosebtn"),
            command=Setting.fore_color_chooser
        )
        self.back_color_label = tk.Label(self.basic_frame, text=language_config.get(languages, "floatingbgcolor"))
        self.back_color_btn = tk.Button(
            self.basic_frame,
            text=language_config.get(languages, "choosebtn"),
            command=Setting.back_color_chooser
        )
        self.cancel_btn = tk.Button(
            self,
            text=language_config.get(languages, "cancel"),
            fg="red",
            command=lambda: Setting.play_disappear()
        )
        self.apply_btn = tk.Button(
            self,
            text=language_config.get(languages, "apply"),
            fg="green",
            command=Setting.apply
        )

        self.size_font_combo.set(self.size)
        self.state_font_combo.set(self.c[0])
        self.trans_font_scale.set(float(self.trans))
        # 高级设置
        columns = {"ID": 50, "字体名字": 400}
        self.yscroll = tk.Scrollbar(self.advanced_frame, orient=tk.VERTICAL)
        self.set_font_treeview = ttk.Treeview(
            self.advanced_frame,
            show="headings",
            columns=list(columns),
            height=12,
            yscrollcommand=self.yscroll.set
        )
        for text, width in columns.items():
            self.set_font_treeview.heading(text, text=text, anchor='center')
            self.set_font_treeview.column(text, anchor='center', width=width, stretch=False)
        font_families = font.families()
        for i in range(len(font_families)):
            self.set_font_treeview.insert('', tk.END, values=[i, font_families[i]])
        del font_families
        self.set_language_label = tk.Label(self.advanced_frame, text=language_config.get(languages, 'setlanguage'))
        self.set_language_combo = ttk.Combobox(
            self.advanced_frame,
            values=language_config.sections(),
            width=13,
            state="readonly"
        )
        self.set_language_combo.set(languages)
        # 启动
        self.bind("<B1-Motion>", self.move)
        self.lbl.bind("<Double-Button-1>", lambda event: self.alpha())
        self.showmenu(self, self.menu)
        self.lbl.pack()
        self.update_time()

    def move(self, event):
        self.geometry(f"+{event.x_root}+{event.y_root}")

    def update_time(self):
        if not self.Pause:
            ymd_time = datetime.datetime.now().strftime("%Y-%m-%d")
            now_time = datetime.datetime.now().strftime("%H:%M:%S")
            now_day = datetime.datetime.now().strftime("%A")
            if now_day in class_:
                for i, class_info in eval(str(class_[now_day])).items():
                    self.subject = class_info["subject"]
                    start_time = class_info["starttime"]
                    self.end_time = class_info["endtime"]
                    state = self.get_state(start_time, self.end_time)
                    if state == self.states[0]:
                        if not class_info['enable'] and self.winfo_rootx() == 0:
                            self.attributes("-alpha", 0.01)
                            self.lbl.config(text="禁用状态")
                        else:
                            self.attributes("-alpha", self.trans)
                            end = (datetime.datetime.strptime(
                                self.end_time,
                                '%H:%M:%S') -
                                   datetime.datetime.strptime(
                                       datetime.datetime.now().strftime("%H:%M:%S"),
                                       '%H:%M:%S')
                                   )
                            after = str(end).split(":")
                            after.insert(1, language_config.get(languages, "hour"))
                            after.insert(3, language_config.get(languages, "minute"))
                            after.insert(5, language_config.get(languages, "second"))
                            for _ in range(2):
                                for a in after:
                                    if str(a) == "0" or str(a) == "00":
                                        index = after.index(a)
                                        if after[index + 1] != language_config.get(languages, "second"):
                                            after.remove(a)
                                            after.pop(index)
                                        del index
                            after = ''.join(after)
                            self.lbl.config(
                                text=f"{time.strftime('%m-%d')} {time.strftime('%H:%M')} "
                                f"{language_config.get(languages, 'after').replace('{time}', after)}"
                            )
                        break
                    elif state == self.states[1]:
                        self.lbl.config(text=f"{ymd_time} {self.get_week()} {now_time} {state} {self.subject}")
                    elif state == self.states[2]:
                        self.lbl.config(text=f"{ymd_time} {self.get_week()} {now_time} {state} {self.subject}")
                        break
            del ymd_time, now_time, now_day
            self.after(400, self.update_time)

    def alpha(self):
        self.click_times += 1
        self.attributes("-alpha", 0.2) if self.click_times % 2 == 1 else self.attributes("-alpha", self.trans)

    @staticmethod
    def get_week(week="none"):
        if time.strftime("%A") == "Monday":
            week = language_config.get(languages, 'monday')
        elif time.strftime("%A") == "Tuesday":
            week = language_config.get(languages, 'tuesday')
        elif time.strftime("%A") == "Wednesday":
            week = language_config.get(languages, 'wednesday')
        elif time.strftime("%A") == "Thursday":
            week = language_config.get(languages, 'thursday')
        elif time.strftime("%A") == "Friday":
            week = language_config.get(languages, 'friday')
        elif time.strftime("%A") == "Saturday":
            week = language_config.get(languages, 'saturday')
        elif time.strftime("%A") == "Sunday":
            week = language_config.get(languages, 'sunday')
        return week

    def get_state(self, start, end) -> str:
        now_time = datetime.datetime.now().time()
        start_time = datetime.datetime.strptime(start, "%H:%M:%S").time()
        end_time = datetime.datetime.strptime(end, "%H:%M:%S").time()

        if now_time < start_time:
            return self.states[2]
        elif start_time <= now_time <= end_time:
            return self.states[0]
        else:
            return self.states[1]

    @staticmethod
    def showmenu(w, menu):
        def poput(event):
            menu.post(event.x + w.winfo_rootx(), event.y + w.winfo_rooty())
            w.update()
        w.lbl.bind('<Button-3>', poput)


class Setting(tk.Tk):
    def __init__(self):
        super().__init__()
        self.selected = None
        self.text = ""
        self.count = -1
        self.y = 0
        self.x = 0
        self.withdraw()

    def open(self):
        self.__init__()
        self.text = Clock.lbl['text']
        Clock.Pause = True
        self.play_show()

    def close(self):
        if tk.messagebox.askyesno(
            language_config.get(languages, "settings_title"),
            language_config.get(languages, "settings_msg")
        ):
            self.text = Clock.lbl['text']
            Clock.overrideredirect(True)
            self.play_disappear()

    def play_disappear(self):
        Clock.geometry(f"{self.x}x{self.y}")
        if self.x != 0 and self.y != 0:
            self.x -= 10
            self.y -= 10
            self.after(10, self.play_disappear)
        else:
            os.kill(os.getpid(), 0)

    def play_show(self):
        self.count += 1
        if self.count < len(self.text):
            Clock.lbl['text'] = self.text[self.count:]
            self.after(20, self.play_show)
        else:
            Clock.geometry(f"{self.x}x{self.y}")
            Clock.attributes("-topmost", False)
            Clock.attributes("-alpha", 1)
            Clock.lbl['text'] = (f"Display {language_config.get(languages, 'settings')}\n"
                                 f"first. Welcome to {time.strftime('%Y')}\n"
                                 f"second\n\n"
                                 f"Display by QQ: 2953911716\n"
                                 f"It's Free and open-source Software!\n"
                                 f"The Open-Source URL is on github.com")
            if self.x != 500 and self.y != 600:
                self.x += 10
                self.y += 10
                self.after(10, self.play_show)
            else:
                Clock.protocol("WM_DELETE_WINDOW", self.close)
                Clock.title(f"{language_config.get(languages, 'settings')} - Display")
                Clock.overrideredirect(False)
                Clock.Pause = False
                Clock.update_time()
                self.settings()

    @staticmethod
    def fore_color_chooser():
        color = colorchooser.askcolor(title=language_config.get(languages, "choosecolor"))
        if color[1]:
            hex_color = color[1]
            Clock.lbl.config(fg=str(hex_color))

    @staticmethod
    def back_color_chooser():
        color = colorchooser.askcolor(title=language_config.get(languages, "choosecolor"))
        if color[1]:
            hex_color = color[1]
            Clock.lbl.config(bg=str(hex_color))

    @staticmethod
    def view(event=None):
        global languages
        languages = Clock.set_language_combo.get()
        try:
            items = Clock.set_font_treeview.selection()[0]
            selected_font = Clock.set_font_treeview.item(items)['values'][-1]
        except IndexError:
            selected_font = Clock.config.get("fgwindow", "type")
        if Clock.state_value.get():
            if Clock.state_font_combo.get() not in Clock.stateus:
                Clock.stateus.append(Clock.state_font_combo.get())
        else:
            Clock.stateus = [Clock.state_font_combo.get()]
        Clock.lbl.config(
            font=(
                selected_font,
                int(Clock.size_font_combo.get()),
                [Clock.stateus[i] for i in range(len(Clock.stateus))]
            )
        )
        if isinstance(event, str):
            Clock.attributes("-alpha", float(event))

    def change_status(self):
        global class_
        if Clock.status_btn['text'] == language_config.get(languages, "enable"):
            class_[self.selected[1]][str(self.selected[0])]['enable'] = True
        else:
            if tkinter.messagebox.askyesno(
                    language_config.get(languages, "settings_enable_title"),
                    language_config.get(languages, "settings_enable_msg")
            ):
                class_[self.selected[1]][str(self.selected[0])]['enable'] = False
        try:
            with open(f'{os.getcwd()}/Libs/resource/class.json', 'w', encoding='utf-8') as f:
                json.dump(class_, f, indent=3, ensure_ascii=False)
        except UnicodeDecodeError:
            try:
                with open(f'{os.getcwd()}/Libs/resource/class.json', 'w', encoding='gb18030') as f:
                    json.dump(class_, f, indent=3, ensure_ascii=False)
            except UnicodeDecodeError:
                tkinter.messagebox.showerror("Error", "Failed to save data")
        self.update_class()

    def swich(self):
        for tree in Clock.date_treeview_list:
            try:
                try:
                    items = tree.selection()[0]
                except IndexError:
                    continue
                self.selected = tree.item(items)['values']
                break
            except UnboundLocalError:
                continue
        else:
            return

        Clock.info_text.insert(tk.END, f"{self.selected}\n")
        Clock.info_text.yview_moveto(True)
        Clock.info_text.update()
        if self.selected[-1] == language_config.get(languages, "enable"):
            Clock.status_btn['text'] = language_config.get(languages, "disable")
        else:
            Clock.status_btn['text'] = language_config.get(languages, "enable")

        for tree in Clock.date_treeview_list:
            try:
                tree.selection_remove(tree.selection()[0])
            except IndexError:
                pass

    @staticmethod
    def update_class():
        dates_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for tree in Clock.date_treeview_list:
            tree.delete(*tree.get_children())
        for date, fir_values in class_.items():
            for index, values in fir_values.items():
                res = [index, date]
                for value in values.values():
                    if value is True:
                        res.append('启用')
                    elif value is False:
                        res.append("禁用")
                    else:
                        res.append(value)
                Clock.date_treeview_list[
                    dates_day.index(date)
                ].insert(
                    '',
                    tk.END,
                    values=res
                )

    @staticmethod
    def apply():
        config = Clock.config
        try:
            items = Clock.set_font_treeview.selection()[0]
            selected_font = Clock.set_font_treeview.item(items)['values'][-1]
        except IndexError:
            selected_font = config.get("fgwindow", "type")
            pass
        config.set("fgwindow", "trans", str(Clock.attributes("-alpha")))
        config.set("fgwindow", "size", Clock.size_font_combo.get())
        config.set("fgwindow", "color", Clock.lbl['fg'])
        config.set("fgwindow", "type", selected_font)
        config.set("fgwindow", "state", ','.join(Clock.stateus))
        # 背景
        config.set("bgwindow", "color", Clock.lbl['bg'])
        # 程序
        config.set("program", "language", languages)
        try:
            with open(f"{os.getcwd()}/Libs/resource/settings.ini", "w", encoding="utf-8") as f:
                config.write(f)
        except UnicodeDecodeError:
            with open(f"{os.getcwd()}/Libs/resource/settings.ini", "w", encoding="gb18030") as f:
                config.write(f)
        tkinter.messagebox.showinfo(
            language_config.get(languages, "warntitle"),
            language_config.get(languages, "warnmsg")
        )
        os.kill(os.getpid(), 0)

    def settings(self):
        Clock.call("tk", "scaling", 1.3)
        Clock.unbind("<B1-Motion>")
        Clock.yscroll.config(command=Clock.set_font_treeview.yview)
        Clock.yscroll.pack(side=tk.RIGHT, fill=tk.Y)
        Clock.size_font_label.place(
            x=int(language_config.get(languages, "sx")),
            y=int(language_config.get(languages, "sy"))
        )
        Clock.size_font_combo.place(
            x=int(language_config.get(languages, "bx")),
            y=int(language_config.get(languages, "sy"))
        )
        Clock.trans_font_label.place(
            x=int(language_config.get(languages, "sx")),
            y=int(language_config.get(languages, "my"))
        )
        Clock.trans_font_scale.place(
            x=int(language_config.get(languages, "bx")),
            y=int(language_config.get(languages, "mmy"))
        )
        Clock.state_font_label.place(
            x=int(language_config.get(languages, "sx")),
            y=200
        )
        Clock.state_font_combo.place(
            x=int(language_config.get(languages, "mx")),
            y=200
        )
        Clock.more_state_checkbtn.place(
            x=int(language_config.get(languages, "mx")) + 150,
            y=200
        )
        Clock.fore_color_label.place(
            x=int(language_config.get(languages, "sx")),
            y=int(language_config.get(languages, "by"))
        )
        Clock.fore_color_btn.place(
            x=int(language_config.get(languages, "mx")),
            y=int(language_config.get(languages, "by"))
        )
        Clock.back_color_label.place(
            x=int(language_config.get(languages, "sx")),
            y=int(language_config.get(languages, "bby"))
        )
        Clock.back_color_btn.place(
            x=int(language_config.get(languages, "mx")),
            y=int(language_config.get(languages, "bby"))
        )
        Clock.set_language_label.place(
            x=int(language_config.get(languages, "mx")) // 3 - int(language_config.get(languages, "sx")),
            y=int(language_config.get(languages, "bby")) * 2
        )
        Clock.set_language_combo.place(
            x=int(language_config.get(languages, "mx")),
            y=int(language_config.get(languages, "bby")) * 2
        )
        Clock.status_btn.place(x=400, y=300)
        for tree in Clock.date_treeview_list:
            tree.bind("<<TreeviewSelect>>", lambda event: self.swich())
            tree.pack()
        Clock.info_text.place(x=0, y=260)
        Clock.set_font_treeview.pack()
        Clock.cancel_btn.place(x=300, y=400)
        Clock.apply_btn.place(x=400, y=400)
        Clock.set_font_treeview.bind("<<TreeviewSelect>>", self.view)
        Clock.size_font_combo.bind("<<ComboboxSelected>>", self.view)
        Clock.state_font_combo.bind("<<ComboboxSelected>>", self.view)
        Clock.set_language_combo.bind("<<ComboboxSelected>>", self.view)
        Clock.notebook.pack(fill=tk.BOTH, expand=True)
        Clock.date_notebook.pack(fill=tk.BOTH, expand=True)
        self.update_class()


Setting = Setting()
Clock = Clock()
if __name__ == '__main__':
    Clock.mainloop()
