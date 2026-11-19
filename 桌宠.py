import json
import random
import tkinter as tk
from pathlib import Path

from 语录 import 成都, 哲学, 歌, 夸赞, 劝别卷, 默认, 自嘲

BASE_DIR = Path(__file__).resolve().parent
SETTINGS_FILE = BASE_DIR / "设置.json"
TRANSPARENT = "#FEFEFE"
FONT = "Microsoft YaHei UI"
ACCENT = "#5B6CFF"
ACCENT_HOVER = "#4656D9"
SCALE_OPTIONS = (("较小", 0.75), ("标准", 1.0), ("较大", 1.25), ("最大", 1.5))
PET_IMAGE_FILES = {
    0.75: "小房子100桌宠_75.png",
    1.0: "小房子100桌宠.png",
    1.25: "小房子100桌宠_125.png",
    1.5: "小房子100桌宠_150.png",
}
LIN_IMAGE_FILES = {
    0.75: "林妹妹_75.png",
    1.0: "林妹妹.png",
    1.25: "林妹妹_125.png",
    1.5: "林妹妹_150.png",
}
EAT_IMAGE_FILES = {
    0.75: "小房子100桌宠_吃屎版_75.png",
    1.0: "小房子100桌宠_吃屎版_100.png",
    1.25: "小房子100桌宠_吃屎版_125.png",
    1.5: "小房子100桌宠_吃屎版.png",
}
POOP_IMAGE_FILES = {
    0.75: "屎桌宠_75.png",
    1.0: "屎桌宠.png",
    1.25: "屎桌宠_125.png",
    1.5: "屎桌宠_150.png",
}


def load_settings():
    try:
        data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    if not isinstance(data, dict):
        data = {}
    scale = data.get("scale", 1.0)
    interval = data.get("interval_minutes", 60)
    if scale not in PET_IMAGE_FILES:
        scale = 1.0
    if isinstance(interval, bool) or not isinstance(interval, (int, float)) or not 0.1 <= interval <= 10080:
        interval = 60
    return scale, interval


def match_any(text, words):
    return any(word in text for word in words)


def reply(user_input: str) -> str:
    text = user_input.strip()
    if not text:
        return random.choice(默认)
    if match_any(text, ["题", "考试", "复习", "作业", "学习", "刷题", "绩点", "论文", "代码", "项目"]):
        return random.choice(夸赞 + 劝别卷)
    if match_any(text, ["我在", "我准备", "我打算", "我要", "卷"]):
        if "卷" in text:
            return random.choice(劝别卷 + 自嘲)
        return random.choice(自嘲)
    if match_any(text, ["你呢", "你怎么样", "你考", "你学", "你会吗", "你行吗"]):
        return random.choice(自嘲)
    if match_any(text, ["为什么", "哲学", "本质", "意义", "严谨", "逻辑", "定义", "形而上"]):
        return random.choice(哲学)
    if "成都" in text:
        return random.choice(成都)
    if "歌" in text:
        return random.choice(歌)
    if match_any(text, ["厉害", "强", "牛", "大佬", "佩服"]):
        return random.choice(夸赞 + 自嘲)
    if match_any(text, ["你好", "hi", "hello", "在吗", "早", "晚上好"]):
        return random.choice(默认)
    if random.random() < 0.15:
        return random.choice(哲学)
    return random.choice(默认)


def rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
        x2, y2 - radius, x2, y2, x2 - radius, y2, x1 + radius, y2,
        x1, y2, x1, y2 - radius, x1, y1 + radius, x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=36, **kwargs)


class ChatWindow:
    WIDTH = 350
    HEIGHT = 430

    def __init__(self, pet):
        self.pet = pet
        self.window = tk.Toplevel(pet.root)
        self.window.withdraw()
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.configure(bg="#E1E6EF")
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.window.protocol("WM_DELETE_WINDOW", self.hide)

        container = tk.Frame(self.window, bg="#F5F7FB", highlightbackground="#E1E6EF", highlightthickness=1)
        container.pack(fill="both", expand=True)
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)

        header = tk.Frame(container, bg="white", height=70)
        header.grid(row=0, column=0, sticky="ew")
        header.pack_propagate(False)
        tk.Frame(header, bg=ACCENT, width=4).place(x=0, y=16, height=38)
        title = tk.Label(header, text="小房子100", bg="white", fg="#252B3A", font=(FONT, 13, "bold"))
        title.place(x=18, y=10)
        subtitle = tk.Label(header, text="在线，随时准备劝你别卷", bg="white", fg="#939CAD", font=(FONT, 9))
        subtitle.place(x=18, y=39)
        close = tk.Label(header, text="×", bg="white", fg="#8B95A7", font=(FONT, 18), cursor="hand2")
        close.place(x=310, y=15, width=26, height=30)
        close.bind("<Button-1>", lambda event: self.hide())
        close.bind("<Enter>", lambda event: close.configure(fg="#303748"))
        close.bind("<Leave>", lambda event: close.configure(fg="#8B95A7"))
        for widget in (header, title, subtitle):
            widget.bind("<ButtonPress-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.drag)

        history_frame = tk.Frame(container, bg="#F5F7FB")
        history_frame.grid(row=1, column=0, sticky="nsew")
        self.history = tk.Canvas(history_frame, bg="#F5F7FB", highlightthickness=0, bd=0)
        self.history.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(
            history_frame, orient="vertical", command=self.history.yview, width=9,
            bg="#CDD5E3", troughcolor="#F5F7FB", activebackground="#AEB9CC",
            relief="flat", bd=0, elementborderwidth=0,
        )
        scrollbar.pack(side="right", fill="y")
        self.history.configure(yscrollcommand=scrollbar.set)

        input_area = tk.Frame(container, bg="white", padx=12, pady=10)
        input_area.grid(row=2, column=0, sticky="ew")
        input_area.columnconfigure(0, weight=1)
        self.input = tk.Text(
            input_area, height=3, wrap="word", font=(FONT, 10), bg="#F5F7FB", fg="#303748",
            insertbackground=ACCENT, relief="flat", highlightbackground="#E1E6EF",
            highlightcolor=ACCENT, highlightthickness=1, padx=8, pady=6,
        )
        self.input.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.input.bind("<Return>", self.send_from_key)
        self.input.bind("<Shift-Return>", lambda event: None)
        self.send_button = tk.Button(
            input_area, text="发送", command=self.send, font=(FONT, 10, "bold"),
            bg=ACCENT, fg="white", activebackground=ACCENT_HOVER, activeforeground="white",
            disabledforeground="#E4E8F3", relief="flat", bd=0, padx=12, cursor="hand2",
        )
        self.send_button.grid(row=0, column=1, sticky="ns")
        hint = tk.Label(input_area, text="Enter 发送 · Shift+Enter 换行", bg="white", fg="#A2ABBA", font=(FONT, 8))
        hint.grid(row=1, column=0, sticky="w", pady=(5, 0))

        self.messages = []
        self.pending = False
        self.add_message("pet", "哇！大佬，来聊两句？")
        self.history.bind("<Configure>", lambda event: self.redraw_messages())
        self.window.bind("<MouseWheel>", self.scroll)
        self.window.bind("<Button-3>", lambda event: self.hide())

    def start_drag(self, event):
        self.drag_x = event.x_root - self.window.winfo_x()
        self.drag_y = event.y_root - self.window.winfo_y()

    def drag(self, event):
        self.window.geometry(f"+{event.x_root - self.drag_x}+{event.y_root - self.drag_y}")

    def scroll(self, event):
        self.history.yview_scroll(int(-event.delta / 120), "units")

    def position(self):
        pet_x = self.pet.root.winfo_x()
        pet_y = self.pet.root.winfo_y()
        x = pet_x - self.WIDTH - 14
        if x < 12:
            x = pet_x + self.pet.WIDTH + 14
        x = max(12, min(x, self.window.winfo_screenwidth() - self.WIDTH - 12))
        y = max(12, min(pet_y + 12, self.window.winfo_screenheight() - self.HEIGHT - 60))
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")

    def show(self):
        self.position()
        self.window.deiconify()
        self.window.lift()
        self.input.focus_set()
        self.redraw_messages()

    def hide(self):
        self.window.withdraw()

    def send_from_key(self, event):
        if not (event.state & 0x1):
            self.send()
            return "break"
        return None

    def send(self):
        if self.pending:
            return
        text = self.input.get("1.0", "end-1c").strip()
        if not text:
            return
        self.input.delete("1.0", "end")
        self.add_message("user", text)
        self.pending = True
        self.send_button.configure(state="disabled")
        self.pet.show_message("让我想想……")
        self.window.after(450, lambda: self.finish_reply(text))

    def finish_reply(self, text):
        answer = reply(text)
        self.add_message("pet", answer)
        self.pet.show_message(answer)
        self.pending = False
        self.send_button.configure(state="normal")
        self.input.focus_set()

    def add_message(self, sender, text):
        self.messages.append((sender, text))
        self.redraw_messages()

    def redraw_messages(self):
        self.history.delete("all")
        width = max(self.history.winfo_width(), 300)
        y = 14
        for sender, text in self.messages:
            text_item = self.history.create_text(
                0, 0, text=text, width=210, anchor="nw", font=(FONT, 10), justify="left"
            )
            bounds = self.history.bbox(text_item)
            self.history.delete(text_item)
            text_height = bounds[3] - bounds[1]
            bubble_width = 234
            bubble_height = text_height + 18
            if sender == "user":
                x1 = width - bubble_width - 14
                fill = ACCENT
                outline = ""
                text_fill = "white"
            else:
                x1 = 14
                fill = "white"
                outline = "#E3E8F0"
                text_fill = "#303748"
            x2 = x1 + bubble_width
            rounded_rectangle(
                self.history, x1, y, x2, y + bubble_height, 13,
                fill=fill, outline=outline,
            )
            self.history.create_text(
                x1 + 12, y + 9, text=text, width=210, anchor="nw",
                font=(FONT, 10), fill=text_fill, justify="left",
            )
            y += bubble_height + 12
        visible_height = self.history.winfo_height()
        self.history.configure(scrollregion=(0, 0, width, max(y, visible_height)))
        self.history.after_idle(lambda: self.history.yview_moveto(1.0))


class IntervalWindow:
    WIDTH = 310
    HEIGHT = 225

    def __init__(self, pet):
        self.pet = pet
        self.window = tk.Toplevel(pet.root)
        self.window.withdraw()
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        self.window.configure(bg="#E1E6EF")
        self.window.protocol("WM_DELETE_WINDOW", self.hide)

        container = tk.Frame(self.window, bg="white", highlightbackground="#E1E6EF", highlightthickness=1)
        container.pack(fill="both", expand=True)
        tk.Frame(container, bg=ACCENT, width=4).place(x=0, y=16, height=28)
        tk.Label(container, text="提醒间隔", bg="white", fg="#252B3A", font=(FONT, 13, "bold")).place(x=18, y=15)
        tk.Label(
            container, text="去死后，经过相同时间再次出现",
            bg="white", fg="#939CAD", font=(FONT, 9),
        ).place(x=18, y=50)

        input_frame = tk.Frame(container, bg="#F5F7FB", highlightbackground="#E1E6EF", highlightthickness=1)
        input_frame.place(x=18, y=83, width=274, height=42)
        self.value = tk.StringVar()
        self.entry = tk.Entry(
            input_frame, textvariable=self.value, font=(FONT, 11), bg="#F5F7FB", fg="#303748",
            insertbackground=ACCENT, relief="flat", bd=0,
        )
        self.entry.place(x=10, y=7, width=220, height=27)
        tk.Label(input_frame, text="分钟", bg="#F5F7FB", fg="#7D889B", font=(FONT, 10)).place(x=235, y=9)
        self.error = tk.Label(container, text="", bg="white", fg="#C65D65", font=(FONT, 8))
        self.error.place(x=18, y=130)

        cancel = tk.Button(
            container, text="取消", command=self.hide, font=(FONT, 10), bg="#E9EDF5", fg="#5C687D",
            activebackground="#DCE3EF", activeforeground="#303748", relief="flat", bd=0, cursor="hand2",
        )
        cancel.place(x=104, y=163, width=82, height=36)
        save = tk.Button(
            container, text="保存设置", command=self.save, font=(FONT, 10, "bold"), bg=ACCENT, fg="white",
            activebackground=ACCENT_HOVER, activeforeground="white", relief="flat", bd=0, cursor="hand2",
        )
        save.place(x=196, y=163, width=96, height=36)
        self.entry.bind("<Return>", lambda event: self.save())
        self.window.bind("<Escape>", lambda event: self.hide())

    def show(self):
        self.value.set(f"{self.pet.interval_minutes:g}")
        self.error.configure(text="")
        x = self.pet.root.winfo_x() + (self.pet.WIDTH - self.WIDTH) // 2
        y = self.pet.root.winfo_y() + self.pet.scaled(105)
        x = max(12, min(x, self.window.winfo_screenwidth() - self.WIDTH - 12))
        y = max(12, min(y, self.window.winfo_screenheight() - self.HEIGHT - 60))
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")
        self.window.deiconify()
        self.window.lift()
        self.entry.focus_set()
        self.entry.selection_range(0, "end")

    def hide(self):
        self.window.withdraw()

    def save(self):
        try:
            value = float(self.value.get().strip())
        except ValueError:
            self.error.configure(text="请输入数字，例如 60 或 0.5")
            return
        if not 0.1 <= value <= 10080:
            self.error.configure(text="可设置 0.1 到 10080 分钟")
            return
        self.pet.set_interval(value)
        self.hide()


class DesktopPet:
    BASE_WIDTH = 330
    BASE_HEIGHT = 514

    def __init__(self):
        self.scale, self.interval_minutes = load_settings()
        self.reminder_job = None
        self.beauty_job = None
        self.showing_lin = False
        self.message_before_beauty = ""
        self.eating = False
        self.showing_eat = False
        self.eating_job = None
        self.eating_restore_job = None
        self.poop_window = None
        self.message_before_eating = ""
        self.eating_start_pos = None
        self.update_dimensions()
        self.root = tk.Tk()
        self.root.title("小房子100桌宠")
        self.root.overrideredirect(True)
        self.root.configure(bg=TRANSPARENT)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", TRANSPARENT)
        self.root.geometry(self.start_position())
        self.size_var = tk.StringVar(value=str(self.scale))

        self.canvas = tk.Canvas(
            self.root, width=self.WIDTH, height=self.HEIGHT,
            bg=TRANSPARENT, highlightthickness=0, bd=0,
        )
        self.canvas.pack()
        self.current_message = "哇！大佬，来聊两句？"
        self.draw()
        self.chat = ChatWindow(self)
        self.interval_window = IntervalWindow(self)
        self.menu = tk.Menu(self.root, tearoff=0, font=(FONT, 10))
        self.menu.add_command(label="聊一聊", command=self.chat.show)
        self.menu.add_command(label="提醒间隔", command=self.interval_window.show)
        self.size_menu = tk.Menu(self.menu, tearoff=0, font=(FONT, 10))
        for label, value in SCALE_OPTIONS:
            self.size_menu.add_radiobutton(
                label=f"{label}（{round(value * 100)}%）", value=str(value),
                variable=self.size_var, command=lambda selected=value: self.set_scale(selected),
            )
        self.menu.add_cascade(label="调整大小", menu=self.size_menu)
        self.menu.add_command(label="暂时离开（去死）", command=self.dismiss)
        self.menu.add_separator()
        self.menu.add_command(label="收到并退出", command=self.close)

        self.canvas.tag_bind("pet", "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind("pet", "<B1-Motion>", self.drag)
        self.canvas.tag_bind("pet", "<ButtonRelease-1>", self.finish_drag)
        self.canvas.tag_bind("pet", "<Button-3>", self.show_menu)
        self.root.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.schedule_reminder()

    def scaled(self, value):
        return round(value * self.scale)

    def update_dimensions(self):
        self.WIDTH = round(self.BASE_WIDTH * self.scale)
        self.HEIGHT = round(self.BASE_HEIGHT * self.scale)

    def start_position(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - self.WIDTH - 28
        y = screen_height - self.HEIGHT - 64
        return f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}"

    def draw(self):
        self.canvas.delete("all")
        self.canvas.configure(width=self.WIDTH, height=self.HEIGHT)
        if self.showing_eat:
            image_files = EAT_IMAGE_FILES
        elif self.showing_lin:
            image_files = LIN_IMAGE_FILES
        else:
            image_files = PET_IMAGE_FILES
        self.image = tk.PhotoImage(file=str(BASE_DIR / image_files[self.scale]))
        self.pet_item = self.canvas.create_image(
            self.scaled(165), self.scaled(260), image=self.image, tags="pet"
        )
        self.show_message(self.current_message)
        self.create_controls()

    def create_controls(self):
        self.chat_shape = rounded_rectangle(
            self.canvas, self.scaled(32), self.scaled(420), self.scaled(164), self.scaled(456),
            self.scaled(18), fill=ACCENT, outline="", tags="chat_button",
        )
        self.canvas.create_text(
            self.scaled(98), self.scaled(438), text="聊一聊", fill="white",
            font=(FONT, max(9, self.scaled(11)), "bold"), tags="chat_button",
        )
        self.canvas.tag_bind("chat_button", "<Button-1>", lambda event: self.chat.show())
        self.canvas.tag_bind("chat_button", "<Enter>", lambda event: self.canvas.itemconfigure(self.chat_shape, fill=ACCENT_HOVER))
        self.canvas.tag_bind("chat_button", "<Leave>", lambda event: self.canvas.itemconfigure(self.chat_shape, fill=ACCENT))

        self.interval_shape = rounded_rectangle(
            self.canvas, self.scaled(172), self.scaled(420), self.scaled(230), self.scaled(456),
            self.scaled(18), fill="#E9EDF5", outline="", tags="interval_button",
        )
        self.canvas.create_text(
            self.scaled(201), self.scaled(438), text="间隔", fill="#5C687D",
            font=(FONT, max(8, self.scaled(10))), tags="interval_button",
        )
        self.canvas.tag_bind("interval_button", "<Button-1>", lambda event: self.interval_window.show())
        self.canvas.tag_bind("interval_button", "<Enter>", lambda event: self.canvas.itemconfigure(self.interval_shape, fill="#DCE3EF"))
        self.canvas.tag_bind("interval_button", "<Leave>", lambda event: self.canvas.itemconfigure(self.interval_shape, fill="#E9EDF5"))

        self.size_shape = rounded_rectangle(
            self.canvas, self.scaled(238), self.scaled(420), self.scaled(296), self.scaled(456),
            self.scaled(18), fill="#E9EDF5", outline="", tags="size_button",
        )
        self.canvas.create_text(
            self.scaled(267), self.scaled(438), text="大小", fill="#5C687D",
            font=(FONT, max(8, self.scaled(10))), tags="size_button",
        )
        self.canvas.tag_bind("size_button", "<Button-1>", self.show_size_menu)
        self.canvas.tag_bind("size_button", "<Enter>", lambda event: self.canvas.itemconfigure(self.size_shape, fill="#DCE3EF"))
        self.canvas.tag_bind("size_button", "<Leave>", lambda event: self.canvas.itemconfigure(self.size_shape, fill="#E9EDF5"))

        rounded_rectangle(
            self.canvas, self.scaled(24), self.scaled(464), self.scaled(218), self.scaled(502),
            self.scaled(18), fill="white", outline="#E1E6EF", tags="beauty_button",
        )
        self.canvas.create_text(
            self.scaled(121), self.scaled(483), text="还是欣赏林妹妹美照吧", fill=ACCENT,
            font=(FONT, max(8, self.scaled(10))), tags="beauty_button",
        )
        self.canvas.tag_bind("beauty_button", "<Button-1>", lambda event: self.show_lin())

        rounded_rectangle(
            self.canvas, self.scaled(226), self.scaled(464), self.scaled(306), self.scaled(502),
            self.scaled(18), fill="#F3EBDD", outline="", tags="eat_button",
        )
        self.canvas.create_text(
            self.scaled(266), self.scaled(483), text="想吃屎了", fill="#8A684A",
            font=(FONT, max(8, self.scaled(9))), tags="eat_button",
        )
        self.canvas.tag_bind("eat_button", "<Button-1>", lambda event: self.start_eating())

        rounded_rectangle(
            self.canvas, self.scaled(10), self.scaled(112), self.scaled(66), self.scaled(142),
            self.scaled(14), fill="#FCEEEF", outline="", tags="dismiss_button",
        )
        self.canvas.create_text(
            self.scaled(38), self.scaled(127), text="去死", fill="#B65B65",
            font=(FONT, max(8, self.scaled(9))), tags="dismiss_button",
        )
        self.canvas.tag_bind("dismiss_button", "<Button-1>", lambda event: self.dismiss())

        rounded_rectangle(
            self.canvas, self.scaled(264), self.scaled(112), self.scaled(320), self.scaled(142),
            self.scaled(14), fill="white", outline="#E3E8F0", tags="ack_button",
        )
        self.canvas.create_text(
            self.scaled(292), self.scaled(127), text="收到", fill="#5C687D",
            font=(FONT, max(8, self.scaled(9))), tags="ack_button",
        )
        self.canvas.tag_bind("ack_button", "<Button-1>", lambda event: self.close())

    def show_message(self, text):
        self.current_message = text
        self.canvas.delete("speech_bubble")
        rounded_rectangle(
            self.canvas, self.scaled(25), self.scaled(22), self.scaled(305), self.scaled(100),
            self.scaled(19), fill="#DCE2EC", outline="", tags="speech_bubble",
        )
        rounded_rectangle(
            self.canvas, self.scaled(25), self.scaled(18), self.scaled(305), self.scaled(96),
            self.scaled(19), fill="white", outline="#E5EAF2", tags="speech_bubble",
        )
        self.canvas.create_polygon(
            self.scaled(148), self.scaled(94), self.scaled(172), self.scaled(94), self.scaled(157), self.scaled(108),
            fill="white", outline="", tags="speech_bubble",
        )
        self.canvas.create_text(
            self.scaled(165), self.scaled(56), text=text, width=self.scaled(244), justify="center",
            fill="#303748", font=(FONT, max(9, self.scaled(11))), tags="speech_bubble",
        )
        self.canvas.tag_raise("pet")
        self.canvas.tag_raise("chat_button")
        self.canvas.tag_raise("interval_button")
        self.canvas.tag_raise("size_button")
        self.canvas.tag_raise("beauty_button")
        self.canvas.tag_raise("eat_button")
        self.canvas.tag_raise("dismiss_button")
        self.canvas.tag_raise("ack_button")

    def set_scale(self, value):
        if self.eating or value == self.scale:
            return
        center_x = self.root.winfo_x() + self.WIDTH // 2
        bottom = self.root.winfo_y() + self.HEIGHT
        self.scale = value
        self.size_var.set(str(value))
        self.update_dimensions()
        x = max(12, min(center_x - self.WIDTH // 2, self.root.winfo_screenwidth() - self.WIDTH - 12))
        y = max(12, min(bottom - self.HEIGHT, self.root.winfo_screenheight() - self.HEIGHT - 60))
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{x}+{y}")
        self.draw()
        self.show_message(f"当前大小：{round(value * 100)}%")
        self.save_settings()
        if self.chat.window.winfo_viewable():
            self.chat.position()

    def save_settings(self):
        SETTINGS_FILE.write_text(
            json.dumps(
                {"scale": self.scale, "interval_minutes": self.interval_minutes},
                ensure_ascii=False, indent=2,
            ),
            encoding="utf-8",
        )

    def set_interval(self, value):
        self.interval_minutes = value
        self.save_settings()
        self.schedule_reminder()
        self.show_message(f"提醒间隔：{value:g} 分钟")

    def schedule_reminder(self):
        if self.reminder_job is not None:
            self.root.after_cancel(self.reminder_job)
        self.reminder_job = self.root.after(round(self.interval_minutes * 60000), self.show_reminder)

    def show_reminder(self):
        self.reminder_job = None
        if self.showing_lin:
            self.restore_pet()
        self.root.deiconify()
        self.root.lift()
        self.show_message("大佬别卷了")
        if self.eating:
            self.message_before_eating = self.current_message
        self.schedule_reminder()

    def dismiss(self):
        self.cancel_eating()
        if self.showing_lin:
            self.restore_pet()
        self.chat.hide()
        self.interval_window.hide()
        self.root.withdraw()
        self.schedule_reminder()

    def show_lin(self):
        self.cancel_eating()
        if self.beauty_job is not None:
            self.root.after_cancel(self.beauty_job)
        if not self.showing_lin:
            self.message_before_beauty = self.current_message
        self.showing_lin = True
        self.draw()
        self.show_message("爱你呀~~~~~")
        self.beauty_job = self.root.after(3000, self.restore_pet)

    def restore_pet(self):
        if self.beauty_job is not None:
            self.root.after_cancel(self.beauty_job)
            self.beauty_job = None
        if not self.showing_lin:
            return
        self.showing_lin = False
        self.draw()
        self.show_message(self.message_before_beauty)

    def start_eating(self):
        if self.eating:
            return
        if self.showing_lin:
            self.restore_pet()
        self.eating = True
        self.message_before_eating = self.current_message
        self.chat.hide()
        self.interval_window.hide()
        start_x = self.root.winfo_x()
        start_y = self.root.winfo_y()
        self.eating_start_pos = (start_x, start_y)
        mouth_x = start_x + self.scaled(182)
        mouth_y = start_y + self.scaled(344)
        travel = self.scaled(130)
        right_room = self.root.winfo_screenwidth() - 12 - self.WIDTH - start_x
        left_room = start_x - 12
        if right_room >= travel:
            direction = 1
            available = right_room
        elif left_room >= travel:
            direction = -1
            available = left_room
        elif right_room >= left_room:
            direction = 1
            available = max(0, right_room)
        else:
            direction = -1
            available = max(0, left_room)
        travel = min(travel, available)
        self.eating_target_x = start_x + direction * travel

        self.poop_image = tk.PhotoImage(file=str(BASE_DIR / POOP_IMAGE_FILES[self.scale]))
        poop_width = self.poop_image.width()
        poop_height = self.poop_image.height()
        poop_center_x = mouth_x + direction * travel
        self.poop_window = tk.Toplevel(self.root)
        self.poop_window.overrideredirect(True)
        self.poop_window.configure(bg=TRANSPARENT)
        self.poop_window.attributes("-topmost", True)
        self.poop_window.attributes("-transparentcolor", TRANSPARENT)
        poop_canvas = tk.Canvas(
            self.poop_window, width=poop_width, height=poop_height,
            bg=TRANSPARENT, highlightthickness=0, bd=0,
        )
        poop_canvas.pack()
        poop_canvas.create_image(poop_width // 2, poop_height // 2, image=self.poop_image)
        self.poop_window.geometry(
            f"{poop_width}x{poop_height}+{round(poop_center_x - poop_width / 2)}+{round(mouth_y - poop_height / 2)}"
        )
        self.poop_window.lift()
        self.eating_step = 0
        self.animate_eating()

    def animate_eating(self):
        self.eating_step += 1
        progress = self.eating_step / 24
        eased = progress * progress * (3 - 2 * progress)
        start_x, start_y = self.eating_start_pos
        x = round(start_x + (self.eating_target_x - start_x) * eased)
        self.root.geometry(f"+{x}+{start_y}")
        if self.eating_step < 24:
            self.eating_job = self.root.after(35, self.animate_eating)
            return
        self.eating_job = None
        if self.poop_window is not None:
            self.poop_window.destroy()
            self.poop_window = None
        self.showing_eat = True
        self.draw()
        self.eating_restore_job = self.root.after(3000, self.finish_eating)

    def finish_eating(self):
        self.eating_restore_job = None
        self.showing_eat = False
        self.eating = False
        self.draw()
        self.show_message(self.message_before_eating)
        self.root.geometry(f"+{self.eating_start_pos[0]}+{self.eating_start_pos[1]}")

    def cancel_eating(self):
        if self.eating_job is not None:
            self.root.after_cancel(self.eating_job)
            self.eating_job = None
        if self.eating_restore_job is not None:
            self.root.after_cancel(self.eating_restore_job)
            self.eating_restore_job = None
        if self.poop_window is not None:
            self.poop_window.destroy()
            self.poop_window = None
        if not self.eating and not self.showing_eat:
            return
        self.eating = False
        self.showing_eat = False
        self.draw()
        self.show_message(self.message_before_eating)
        self.root.geometry(f"+{self.eating_start_pos[0]}+{self.eating_start_pos[1]}")

    def show_size_menu(self, event=None):
        if self.eating:
            return
        self.size_menu.post(
            self.root.winfo_x() + self.scaled(208),
            self.root.winfo_y() + self.scaled(414),
        )

    def start_drag(self, event):
        if self.eating:
            self.drag_moved = True
            return
        self.drag_offset_x = event.x_root - self.root.winfo_x()
        self.drag_offset_y = event.y_root - self.root.winfo_y()
        self.drag_moved = False

    def drag(self, event):
        if self.eating:
            return
        self.drag_moved = True
        x = event.x_root - self.drag_offset_x
        y = event.y_root - self.drag_offset_y
        self.root.geometry(f"+{x}+{y}")
        if self.chat.window.winfo_viewable():
            self.chat.position()

    def finish_drag(self, event):
        if not self.drag_moved:
            self.show_message(random.choice(默认))

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

    def close(self):
        if self.reminder_job is not None:
            self.root.after_cancel(self.reminder_job)
        if self.beauty_job is not None:
            self.root.after_cancel(self.beauty_job)
        self.cancel_eating()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    DesktopPet().run()
