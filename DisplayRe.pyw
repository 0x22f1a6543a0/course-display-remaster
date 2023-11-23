# -*- coding: utf-8 -*-
import os
import tkinter as tk
import tkinter.messagebox
from tkinter import Text, Label, Menu, PhotoImage, Scale, colorchooser, font, Listbox, Checkbutton
from tkinter.ttk import Frame, Combobox, Notebook, Button
from tkinter.scrolledtext import ScrolledText
import time, random, datetime, json, configparser
import idlelib.colorizer as idc
import idlelib.percolator as idp
import ctypes, platform, re

language_config = configparser.ConfigParser()
language_config.read("./Libs/resource/language.ini", encoding="utf-8")
language_choose = configparser.ConfigParser()
language_choose.read("./Libs/resource/settings.ini", encoding="utf-8")
languages = language_choose.get("program", "language")
if languages not in language_config.sections():
    tkinter.messagebox.showerror("Error",f"not found the languages '{languages}' sections in languages.ini,\nPlease change the language option in the settings.ini file to the correct language option")
    exit(0)

try:
    with open('./Libs/resource/class.json', 'r', encoding='utf-8') as json_file:
        json_data = json_file.read()

except UnicodeDecodeError:
    with open('./Libs/resource/class.json', 'r', encoding='gb18030') as json_file:
        json_data = json_file.read()

except:
    tkinter.messagebox.showerror(language_config.get(language,"errrortitle"), language_config.get(language,"errrormsg"))

class_ = dict(json.loads(json_data))

def starting():
    def show_window():
        starting.deiconify()
        starting.attributes("-alpha", 0)
        starting.after(1000, gradually_show)

    def gradually_close():
        alpha = starting.attributes("-alpha")
        if alpha > 0.5:
            alpha -= 0.1
            starting.attributes("-alpha", alpha)
            starting.after(30, gradually_close)
        else:
            starting.destroy()

    def gradually_show():
        alpha = starting.attributes("-alpha")
        if alpha < 1:
            alpha += 0.1
            starting.attributes("-alpha", alpha)
            starting.after(30, gradually_show)
        else:
            time.sleep(random.uniform(1,2))
            gradually_close()

    starting = tk.Tk()
    starting.title("INIT PROGRAM")
    starting.attributes("-topmost", 1)
    starting.overrideredirect(True)
    photo = PhotoImage(file="./Libs/resource/starting.png")
    label = Label(starting, image=photo)
    label.pack()
    wight = 665
    high = 250
    x = starting.winfo_screenwidth()
    y = starting.winfo_screenheight()
    starting.geometry(f'{wight}x{high}+{int(round((x - wight) / 2, 0))}+{int(round((y - high) / 2, 0))}')

    starting.withdraw()
    starting.after(0, show_window)
    starting.mainloop()

class Clock(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        config = configparser.ConfigParser()
        try:
            config.read("./Libs/resource/settings.ini",encoding="utf-8")
        except UnicodeDecodeError:
            config.read("./Libs/resource/settings.ini",encoding="utf-8")

        self.size = config.get("fgwindow","size")
        self.trans = config.get("fgwindow","trans")
        self.fg_color = config.get("fgwindow","color")
        self.type = config.get("fgwindow","type")
        self.c = config.get("fgwindow","state")

        self.bg_color = config.get("bgwindow","color")

        self.language = languages

        self.dll = ctypes.cdll.LoadLibrary(fr'{os.getcwd()}\Libs\SYSTEM_WIN'+"".join(re.findall("[\d+]", platform.architecture()[0]))+".dll")
        self.tk.call('tk', 'scaling', int(self.dll.GetScale()) / 75)

        self.times = 0
        self.subject = "未知"
        self.end_time = ""
        self.states = [language_config.get(self.language,"statef"), language_config.get(self.language,"states"), language_config.get(self.language,"statet")]
        self.attributes("-topmost", True)
        self.geometry(f"+0+0")
        self.overrideredirect(True)
        self.attributes("-alpha", self.trans)
        self.bind("<B1-Motion>", self.move)
        self.lbl = tk.Label(self,
                            text="",
                            font=(self.type, self.size, self.c),
                            background=self.bg_color,
                            foreground=self.fg_color)
        self.menu = Menu(self)
        self.menu.add_cascade(label=language_config.get(self.language,'settings'),command=self._settings)
        self.menu.add_cascade(label=language_config.get(self.language,'exit'),command=self._exit)
        with open("./Libs/autoexec.cfg", "r", encoding="utf-8") as f:
            menudata = f.read()
        for _ in menudata.strip().split("\n"):
            self.release(f"./Libs/{_}")
        self.showMenu(self, self.menu)
        self.lbl.pack()
        self.update_time()

    def move(self, event):
        self.geometry("+{0}+{1}".format(event.x_root, event.y_root))

    def _settings(self):
        def finish():
            w_config = configparser.ConfigParser()
            w_config.read("./Libs/resource/settings.ini",encoding="utf-8")
            languages = language.get()
            self.trans = trans_sca.get()
            self.size = size_com.get()
            self.c = state_com.get()
            w_config.set("fgwindow", "trans", str(self.trans))
            w_config.set("fgwindow", "size", str(self.size))
            w_config.set("fgwindow", "color", str(self.fg_color))
            w_config.set("fgwindow", "type", str(self.type))
            w_config.set("fgwindow", "state", str(self.c))
            w_config.set("bgwindow", "color", str(self.bg_color))
            w_config.set("program", "language", str(languages))
            try:
                with open("./Libs/resource/settings.ini","w",encoding="utf-8") as f:
                    w_config.write(f)
            except UnicodeDecodeError:
                with open("./Libs/resource/settings.ini","w",encoding="gb18030") as f:
                    w_config.write(f)
            settings.destroy()
            self.destroy()
            tkinter.messagebox.showwarning(language_config.get(self.language,"warntitle"),language_config.get(self.language,"warnmsg"))
            exit(0)

        def choose_color(who):
            color = colorchooser.askcolor(title=language_config.get(self.language,"choosecolor"))
            if color[1]:
                hex_color = color[1]
                if who == "bg":
                    self.bg_color = hex_color
                elif who == "fg":
                    self.fg_color = hex_color
        settings = tk.Tk()
        settings.title(language_config.get(self.language,"programsettings"))
        settings.geometry(f"1000x600+{self.winfo_x()+100}+{self.winfo_y()+50}")
        settings.tk.call('tk', 'scaling', int(self.dll.GetScale())/75)
        notebook = Notebook(settings)
        set_fg = Frame(notebook)
        set_font = Frame(notebook)
        other = Frame(notebook)
        notebook.add(set_fg, text=language_config.get(self.language,"setfg"))
        notebook.add(set_font, text=language_config.get(self.language,"setfont"))
        notebook.add(other, text=language_config.get(self.language,"setother"))

        # 悬浮窗
        size = Label(set_fg, text=language_config.get(self.language,"floatingsize"))
        trans = Label(set_fg, text=language_config.get(self.language,"floatingtrans"))
        state = Label(set_fg, text=language_config.get(self.language, "floatingstate"))
        state_com = Combobox(set_fg, values=['normal', 'bold', 'overstrike', 'italic', 'underline'], state="readonly")
        state_com.set(self.c)
        trans_sca = Scale(set_fg, from_=0.01, to=1,resolution=0.01,orient=tk.HORIZONTAL)
        trans_sca.set(self.trans)
        size_com = Combobox(set_fg, values=list(range(1,251)), state="readonly")
        size_com.set(self.size)
        fg_color = Label(set_fg, text=language_config.get(self.language,"floatingcolor"))
        bg_color = Label(set_fg, text=language_config.get(self.language,"floatingbgcolor"))
        color_btn1 = Button(set_fg, text=language_config.get(self.language,"choosebtn"),command=lambda: choose_color("fg"))
        color_btn2 = Button(set_fg, text=language_config.get(self.language,"choosebtn"), command=lambda: choose_color("bg"))

        size.place(x=int(language_config.get(self.language,"sx")),y=int(language_config.get(self.language,"sy")))
        size_com.place(x=int(language_config.get(self.language,"bx")),y=int(language_config.get(self.language,"sy")))
        state.place(x=int(language_config.get(self.language,"sx")), y=200)
        state_com.place(x=int(language_config.get(self.language,"mx")), y=200)
        trans.place(x=int(language_config.get(self.language,"sx")), y=int(language_config.get(self.language,"my")))
        trans_sca.place(x=int(language_config.get(self.language,"bx")), y=int(language_config.get(self.language,"mmy")))
        fg_color.place(x=int(language_config.get(self.language,"sx")), y=int(language_config.get(self.language,"by")))
        bg_color.place(x=int(language_config.get(self.language,"sx")), y=int(language_config.get(self.language,"bby")))
        color_btn1.place(x=int(language_config.get(self.language,"mx")), y=int(language_config.get(self.language,"by")))
        color_btn2.place(x=int(language_config.get(self.language,"mx")), y=int(language_config.get(self.language,"bby")))

        # 字体
        def get():
            self.type = fonts.get(fonts.curselection())
            self.c = state_com.get()
            show_font.config(text=f"{language_config.get(self.language,'choosing')} {self.type}")
            display_font4.config(text="这是预览效果  空格\nHere is the preview effect  space\nプレビュー効果は次のとおりです  箜\n1 2 3 4 5 6 7 8 9 0",font=(self.type, 20, self.c), fg=self.fg_color, bg=self.bg_color)

        fonts = Listbox(set_font, width=40,height=30)
        fonts.place(x=5,y=5)
        show_font = Label(set_font, text=language_config.get(self.language,'choosing'))
        show_font.place(x=300,y=10)
        display_font4 = Label(set_font, text="这是预览效果  空格\nHere is the preview effect  space\nプレビュー効果は次のとおりです  箜\n1 2 3 4 5 6 7 8 9 0",font=(self.type, 20, self.c), fg=self.fg_color, bg=self.bg_color)
        display_font4.place(x=300, y=90)
        family = list(font.families())
        for font_name in family:
            fonts.insert(tk.END, font_name)
        fonts.bind("<<ListboxSelect>>", lambda event: get())
        notebook.pack(expand=True, fill=tk.BOTH)
        roll = tk.Scrollbar(set_font, orient="vertical")
        roll.config(command=fonts.yview)
        fonts.config(yscrollcommand=roll.set)
        roll.pack(side="right", fill="y")
        global_ = Button(settings, text=language_config.get(self.language,'apply'),command=finish)
        cancel = Button(settings, text=language_config.get(self.language,'cancel'),command=settings.destroy)
        global_.place(x=800,y=550)
        cancel.place(x=700,y=550)

        # 其他设置
        frame = Frame(other, borderwidth=2, relief="solid")
        frame.place(x=5,y=50)
        def execute():
            info = tk.Tk()
            info.geometry(f"+{settings.winfo_x()+200}+{settings.winfo_y()+100}")
            info.overrideredirect(True)
            Label(info, text="======================\nFinished\nSuccessful executing this plugins\nFinished\n======================", fg="green").pack()
            info.after(1000, info.destroy)
            self.release("./Libs/"+choose_pyl.get())
            info.mainloop()

        def autoexec():
            info = tk.Tk()
            info.geometry(f"+{settings.winfo_x()+200}+{settings.winfo_y()+100}")
            info.overrideredirect(True)
            Label(info, text="======================\nFinished\nSuccessful auto exec this plugins\nFinished\n======================", fg="green").pack()
            info.after(1000, info.destroy)
            with open("./Libs/autoexec.cfg", "r", encoding="utf-8") as f:
                had_file = f.read()
            if choose_pyl.get() in had_file:
                with open("./Libs/autoexec.cfg", "r", encoding="utf-8") as f:
                    ori_data = f.read()
                with open("./Libs/autoexec.cfg", "w", encoding="utf-8") as f:
                    data = ori_data.replace(choose_pyl.get(), "")
                    f.write(data+"\n")
            else:
                with open("./Libs/autoexec.cfg", "a", encoding="utf-8") as f:
                    f.write(choose_pyl.get()+"\n")
            info.mainloop()

        Label(frame, text="Plugins：").pack()
        pyl_file = [file for file in os.listdir("./Libs") if file.endswith(".pyl")]
        choose_pyl = Combobox(frame, values=pyl_file, state="readonly")
        choose_pyl.set("None Plugins")
        choose_pyl.pack()
        run_pyl = Button(frame, text="▶ EXECUTE ▶", command=execute)
        autorun_pyl = Button(frame, text="▶ AUTO EXECUTE ▶", command=autoexec)
        autorun_pyl.pack()
        run_pyl.pack()

        def run():
            if runner['text'] == "Run ▶":
                runner['text'] = "Stop ■"
                runner['fg'] = "red"
                execcode = Frame(notebook)
                notebook.add(execcode, text="Running_information")
                try:
                    Label(execcode, text="Title: "+coder.get(1.0, tk.END).split('\n')[0].split('#')[1].strip(), font=("微软雅黑", 30, "underline")).pack()
                except IndexError:
                    Label(execcode, text="Title: Unset", font=("微软雅黑", 30, "underline"), fg="blue").pack()
                Label(execcode, text=f"Running Code:\n{'-='*10}\n {coder.get(1.0, tk.END)}\n{'-='*10}", font=("微软雅黑", 10), fg="purple").pack()
                try:
                    mg = globals()
                    ml = locals()
                    exec(coder.get(1.0, tk.END), mg, ml)
                    notebook.forget(3)
                    runner['text'] = "Run ▶"
                    runner['fg'] = "#41cc32"
                except Exception as e:
                    error_note = Frame(notebook)
                    notebook.add(error_note, text="Running_Error")
                    Label(error_note, text="RUNNING ERROR:\n==============================\n\n"+str(type(e))+" -> "+str(e)+"\n\n==============================", font=("宋体", 12, "bold"), fg="red").pack()

            else:
                runner['text'] = "Run ▶"
                runner['fg'] = "#41cc32"
                try:
                    notebook.forget(4)
                except:
                    pass
                finally:
                    notebook.forget(3)

        def auto_indent(event):
            text = event.widget
            line = text.get("insert linestart", "insert")
            match = re.match(r'^(\s+)', line)
            whitespace = match.group(0) if match else ""
            text.insert("insert", f"\n{whitespace}")
            return "break"

        def import_():
            if ".pyl" in pyl.get():
                path = "./Libs/" + pyl.get()
            else:
                path = "./Libs/" + pyl.get() + ".pyl"
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            coder.delete(1.0, tk.END)
            coder.insert(1.0, code)

        def save():
            if not pyl.get().strip() == "":
                if ".pyl" in pyl.get():
                    path = "./Libs/"+pyl.get()
                else:
                    path = "./Libs/"+pyl.get()+".pyl"
                with open(path, 'w', encoding="utf-8") as f:
                    f.write(coder.get(1.0, tk.END))
                    f.close()
            else:
                tkinter.messagebox.showerror(language_config.get(self.language, "savetitle"), language_config.get(self.language, "savemsg"))

        def delete():
            if tkinter.messagebox.askyesno(language_config.get(self.language, "deltitle"), language_config.get(self.language, "delmsg")):
                if ".pyl" in pyl.get():
                    os.remove("./Libs/"+pyl.get())
                else:
                    os.remove("./Libs/" + pyl.get()+".pyl")

        Label(other, text=language_config.get(self.language,'setlanguage')).place(x=10,y=10)
        language = Combobox(other, values=language_config.sections(), state="readonly")
        language.set(self.language)
        language.place(x=100,y=10)
        runner = tk.Button(other, text="Run ▶", font=("黑体", 14, "bold"), bg='#252424',fg='#41cc32', command=run)
        runner.place(x=400, y=20)
        tk.Button(other, text="Import ◀", bg='#252424',fg='white', command=import_).place(x=500, y=20)
        tk.Button(other, text="Save ▼", bg='#252424',fg='white', command=save).place(x=700, y=20)
        tk.Button(other, text="Delete ▲", font=("黑体", 14, "bold") ,bg='#252424',fg='red', command=delete).place(x=770, y=20)
        pyl = Combobox(other, values=pyl_file, width=15)
        try:
            pyl.set(pyl_file[0])
        except:
            pass
        coder = ScrolledText(other, width=70, height=24, font=("微软雅黑", 10, "bold"))
        coder.place(x=400,y=60)
        coder.focus_set()
        coder.bind("<Return>", auto_indent)
        idc.color_config(coder)
        p = idp.Percolator(coder)
        d = idc.ColorDelegator()
        p.insertfilter(d)
        pyl.place(x=570,y=20)
        
        settings.mainloop()

    def _exit(self):
        os.system(f"taskkill /F /PID {os.getpid()}")

    def update_time(self):
        Ymd_time = datetime.datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.lbl.config(text=now_time)
        now_day = datetime.datetime.now().strftime("%A")
        if now_day in class_:
            for i, class_info in class_[now_day].items():
                self.subject = class_info["subject"]
                start_time = class_info["starttime"]
                self.end_time = class_info["endtime"]
                state = self.get_state(start_time, self.end_time)
                if state == self.states[0]:
                    if self.times < 31:
                        self.lbl.config(text=f"{Ymd_time} {self.get_week()} {now_time} {state} {self.subject}")
                    else:
                        end = datetime.datetime.strptime(self.end_time,'%H:%M:%S') - datetime.datetime.strptime(datetime.datetime.now().strftime("%H:%M:%S"),'%H:%M:%S')
                        after = str(end).split(":")
                        after.insert(1, language_config.get(self.language, "hour"))
                        after.insert(3, language_config.get(self.language, "minute"))
                        after.insert(5, language_config.get(self.language, "second"))
                        after = ''.join(after)
                        if self.language == language_config.sections()[0]:
                            self.lbl.config(text=f"我最喜欢学{self.subject}了！！"+language_config.get(self.language, 'after') + str(after))
                        else:
                            self.lbl.config(text=language_config.get(self.language, 'after') + " " + str(after))
                            if self.times > 59:
                                self.times = 0
                    break
                elif state == self.states[1]:
                    self.lbl.config(text=f"{Ymd_time} {self.get_week()} {now_time} {state} {self.subject}")
                elif state == self.states[2]:
                    self.lbl.config(text=f"{Ymd_time} {self.get_week()} {now_time} {state} {self.subject}")
                    break
        self.times += 1
        self.after(100, self.update_time)

    def inter(self, io):
        with open(io, "r", encoding="utf-8") as f:
            code = f.read()
        mg = globals()
        ml = locals()
        exec(code, mg, ml)


    def release(self,io):
        try:
            with open(io, "r", encoding="utf-8") as f:
                name = f.read().split("\n")
            try:
                self.menu.insert_cascade(index=2,label=name[0].split("#")[1].strip(), command=lambda: self.inter(io))
            except:
                self.menu.insert_cascade(index=2,label="Unset", command=lambda: self.inter(io))
            self.showMenu(self, self.menu)
        except:
            pass


    def get_week(self,week="none"):
        if time.strftime("%A") == "Monday": week = language_config.get(self.language, 'monday')
        elif time.strftime("%A") == "Tuesday": week = language_config.get(self.language, 'tuesday')
        elif time.strftime("%A") == "Wednesday": week = language_config.get(self.language, 'wednesday')
        elif time.strftime("%A") == "Thursday": week = language_config.get(self.language, 'thursday')
        elif time.strftime("%A") == "Friday": week = language_config.get(self.language, 'friday')
        elif time.strftime("%A") == "Saturday": week = language_config.get(self.language, 'saturday')
        elif time.strftime("%A") == "Sunday": week = language_config.get(self.language, 'sunday')
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

    def showMenu(self,w, menu):
        def popout(event):
            menu.post(event.x + w.winfo_rootx(), event.y + w.winfo_rooty())
            w.update()
        w.bind('<Button-3>', popout)

if __name__ == '__main__':
    starting()
    Clock().mainloop()
