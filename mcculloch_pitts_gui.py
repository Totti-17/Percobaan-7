"""
mcculloch_pitss Neural Network GUI
Run: python mcculloch_pitts_gui.py
Requires: Python 3.10+ (Tkinter is included with most Python installations)
"""

#Nama: Imanuel Totti Wijaya
#NIM: 24131310054
#Semester 5 

import tkinter as tk
from tkinter import ttk, messagebox

BG = "#0b1020"
PANEL = "#131b31"
PANEL2 = "#1b2742"
TEXT = "#edf3ff"
MUTED = "#9aabc9"
ACCENT = "#6ee7f9"
GREEN = "#e2e669"
RED = "#71e5ff"
GOLD = "#ff6666"

class McCullochPittsApp:
    def __init__(self, root):
        self.root = root
        root.title("NEURON LAB • McCulloch-Pitts")
        root.geometry("1100x760")
        root.minsize(900, 650)
        root.configure(bg=BG)
        self.x1 = tk.IntVar(value=1)
        self.x2 = tk.IntVar(value=1)
        self.w1 = tk.IntVar(value=1)
        self.w2 = tk.IntVar(value=1)
        self.threshold = tk.IntVar(value=2)
        self.gate = tk.StringVar(value="AND")
        self._style()
        self._build()
        self.update_result()

    def _style(self):
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except tk.TclError:
            pass
        s.configure("TFrame", background=BG)
        s.configure("Panel.TFrame", background=PANEL)
        s.configure("Panel2.TFrame", background=PANEL2)
        s.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))
        s.configure("Muted.TLabel", background=PANEL, foreground=MUTED, font=("Segoe UI", 10))
        s.configure("Heading.TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 22, "bold"))
        s.configure("Sub.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 10))
        s.configure("PanelTitle.TLabel", background=PANEL, foreground=ACCENT, font=("Segoe UI", 12, "bold"))
        s.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8))
        s.configure("Accent.TButton", background=ACCENT, foreground="#07111e")
        s.map("Accent.TButton", background=[("active", "#a5f3fc")])
        s.configure("TCombobox", padding=6)
        s.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=TEXT,
                    rowheight=30, borderwidth=0, font=("Consolas", 10))
        s.configure("Treeview.Heading", background=PANEL2, foreground=ACCENT,
                    font=("Segoe UI", 10, "bold"), relief="flat")
        s.map("Treeview", background=[("selected", "#274565")])

    def _panel(self, parent, title=None):
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=16)
        if title:
            ttk.Label(frame, text=title, style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 12))
        return frame

    def _build(self):
        header = ttk.Frame(self, style="TFrame") if False else tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=26, pady=(22, 16))
        tk.Label(header, text="NEURON LAB", bg=BG, fg=ACCENT,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ttk.Label(header, text="McCulloch-Pitts Network", style="Heading.TLabel").pack(anchor="w", pady=(4, 2))
        ttk.Label(header, text="Eksperimen neuron biner • ubah input, bobot, dan threshold secara langsung",
                  style="Sub.TLabel").pack(anchor="w")

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=26, pady=(0, 20))
        left = tk.Frame(body, bg=BG, width=340)
        left.pack(side="left", fill="y", padx=(0, 16))
        left.pack_propagate(False)
        right = tk.Frame(body, bg=BG)
        right.pack(side="left", fill="both", expand=True)

        controls = self._panel(left, "⚙ KONTROL NEURON")
        controls.pack(fill="x", pady=(0, 14))
        self._section_label(controls, "INPUT BINER")
        for label, var in (("Input X₁", self.x1), ("Input X₂", self.x2)):
            row = tk.Frame(controls, bg=PANEL)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=label, bg=PANEL, fg=TEXT, font=("Segoe UI", 11)).pack(side="left")
            switch = tk.Frame(row, bg=PANEL2, padx=3, pady=3)
            switch.pack(side="right")
            for val in (0, 1):
                tk.Radiobutton(switch, text=str(val), variable=var, value=val,
                               command=self.update_result, indicatoron=False, width=4,
                               bg=PANEL2, fg=MUTED, selectcolor="#176b78",
                               activebackground=PANEL2, activeforeground=TEXT,
                               font=("Segoe UI", 10, "bold"), relief="flat",
                               bd=0).pack(side="left", padx=2)

        self._section_label(controls, "BOBOT INPUT")
        self._scale_row(controls, "Bobot W₁", self.w1, -3, 3)
        self._scale_row(controls, "Bobot W₂", self.w2, -3, 3)
        self._section_label(controls, "THRESHOLD (θ)")
        scale = tk.Scale(controls, from_=-6, to=6, orient="horizontal", variable=self.threshold,
                         command=lambda _v: self.update_result(), bg=PANEL, fg=TEXT,
                         troughcolor=PANEL2, activebackground=ACCENT, highlightthickness=0,
                         bd=0, showvalue=True, font=("Segoe UI", 9), length=270)
        scale.pack(fill="x", pady=(0, 8))
        tk.Label(controls, text="Output Y = 1 jika net ≥ θ, selain itu 0 (XOR adalah simulasi)",
                 bg=PANEL, fg=MUTED, font=("Segoe UI", 9), wraplength=290,
                 justify="left").pack(anchor="w", pady=(0, 12))
        ttk.Label(controls, text="FUNGSI LOGIKA", style="PanelTitle.TLabel").pack(anchor="w", pady=(0, 8))
        gatebox = ttk.Combobox(controls, textvariable=self.gate, state="readonly",
                               values=("AND", "OR", "NAND", "NOR", "XOR (simulasi)", "CUSTOM"))
        gatebox.pack(fill="x", pady=(0, 12))
        gatebox.bind("<<ComboboxSelected>>", self.apply_gate)
        btns = tk.Frame(controls, bg=PANEL)
        btns.pack(fill="x")
        ttk.Button(btns, text="Reset", command=self.reset).pack(side="left")
        ttk.Button(btns, text="Semua kombinasi", command=self.show_truth_table,
                   style="Accent.TButton").pack(side="right")

        visual = self._panel(right, "👁 VISUALISASI REAL-TIME")
        visual.pack(fill="x", pady=(0, 14))
        self.canvas = tk.Canvas(visual, height=250, bg=PANEL, highlightthickness=0)
        self.canvas.pack(fill="x")
        self.net_label = tk.Label(visual, text="", bg=PANEL, fg=ACCENT,
                                  font=("Consolas", 13, "bold"))
        self.net_label.pack(anchor="center", pady=(10, 0))

        result = self._panel(right, "📊 HASIL AKTIVASI")
        result.pack(fill="x", pady=(0, 14))
        resultrow = tk.Frame(result, bg=PANEL)
        resultrow.pack(fill="x")
        self.output_badge = tk.Label(resultrow, text="Y = 1", bg=GREEN, fg="#07111e",
                                     font=("Segoe UI", 24, "bold"), padx=20, pady=10)
        self.output_badge.pack(side="left", padx=(0, 18))
        self.result_text = tk.Label(resultrow, text="", bg=PANEL, fg=TEXT,
                                    font=("Segoe UI", 11), justify="left", anchor="w")
        self.result_text.pack(side="left", fill="x", expand=True)
        self.progress = ttk.Progressbar(result, maximum=100, mode="determinate")
        self.progress.pack(fill="x", pady=(16, 4))
        self._section_label(result, "TABEL KEBENARAN (sesuai mode/bobot saat ini)")
        cols = ("x1", "x2", "net", "y")
        self.table = ttk.Treeview(result, columns=cols, show="headings", height=4)
        for col, title, width in (("x1", "X₁", 70), ("x2", "X₂", 70), ("net", "NET", 180), ("y", "OUTPUT Y", 100)):
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor="center")
        self.table.pack(fill="x", pady=(6, 0))
        self.table.tag_configure("active", background="#174b51", foreground="#ffffff")
        self.table.tag_configure("normal", background=PANEL, foreground=TEXT)

        footer = tk.Label(self.root, text="BINARY INPUT  /  WEIGHTED SUM  /  THRESHOLD ACTIVATION",
                          bg=BG, fg="#607391", font=("Consolas", 9))
        footer.pack(pady=(0, 12))

    def _section_label(self, parent, text):
        tk.Label(parent, text=text, bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(8, 4))

    def _scale_row(self, parent, label, var, low, high):
        row = tk.Frame(parent, bg=PANEL)
        row.pack(fill="x", pady=2)
        tk.Label(row, text=label, bg=PANEL, fg=TEXT, font=("Segoe UI", 10)).pack(anchor="w")
        scale = tk.Scale(row, from_=low, to=high, orient="horizontal", variable=var,
                         command=lambda _v: self.update_result(), bg=PANEL, fg=TEXT,
                         troughcolor=PANEL2, activebackground=ACCENT, highlightthickness=0,
                         bd=0, showvalue=True, font=("Segoe UI", 9), length=270)
        scale.pack(fill="x")

    def apply_gate(self, _event=None):
        """Set a logical-gate preset using a threshold neuron where possible."""
        gate = self.gate.get()
        settings = {
            "AND": (1, 1, 2),
            "OR": (1, 1, 1),
            "NAND": (-1, -1, -1),
            "NOR": (-1, -1, 0),
        }
        if gate in settings:
            w1, w2, theta = settings[gate]
            self.w1.set(w1)
            self.w2.set(w2)
            self.threshold.set(theta)
        # XOR is not linearly separable and cannot be represented by one
        # threshold neuron; this option explicitly simulates its truth table.
        self.update_result()

    def calculate(self, a, b):
        net = a * self.w1.get() + b * self.w2.get()
        if self.gate.get() == "XOR (simulasi)":
            y = int(a != b)
        else:
            y = int(net >= self.threshold.get())
        return net, y

    def update_result(self, *_):
        a, b = self.x1.get(), self.x2.get()
        net, y = self.calculate(a, b)
        theta = self.threshold.get()
        self.net_label.config(text=f"net = ({a} × {self.w1.get()}) + ({b} × {self.w2.get()}) = {net}  |  θ = {theta}")
        self.output_badge.config(text=f"Y = {y}", bg=GREEN if y else RED)
        if self.gate.get() == "XOR (simulasi)":
            status = "Mode XOR simulasi: perlu lebih dari satu neuron."
        else:
            status = ("Neuron aktif — net ≥ threshold." if y else
                      "Neuron tidak aktif — net < threshold.")
        self.result_text.config(
            text=status + f"\nInput: ({a}, {b})    Bobot: ({self.w1.get()}, {self.w2.get()})"
        )
        self.progress["value"] = max(0, min(100, int(100 * max(0, net) / max(1, abs(theta)))))
        self._draw_network(a, b, y)
        self._update_table(a, b)

    def _draw_network(self, a, b, y):
        c = self.canvas
        c.delete("all")
        w = max(c.winfo_width(), 500)
        h = 250
        # connections
        c.create_line(95, 65, w-160, 105, fill=ACCENT if a else "#53627c", width=3 if a else 1,
                      arrow=tk.LAST, arrowshape=(10, 12, 4))
        c.create_line(95, 185, w-160, 145, fill=ACCENT if b else "#53627c", width=3 if b else 1,
                      arrow=tk.LAST, arrowshape=(10, 12, 4))
        for x, yy, val, name in ((55, 65, a, "X₁"), (55, 185, b, "X₂")):
            color = "#176b78" if val else PANEL2
            c.create_oval(x-28, yy-28, x+28, yy+28, fill=color, outline=ACCENT if val else "#607391", width=2)
            c.create_text(x, yy, text=f"{name}\n{val}", fill=TEXT, font=("Segoe UI", 11, "bold"))
        nx = w - 160
        c.create_oval(nx-37, 87, nx+37, 163, fill="#176b78" if y else PANEL2,
                      outline=GREEN if y else RED, width=3)
        c.create_text(nx, 125, text=f"Y\n{y}", fill=TEXT, font=("Segoe UI", 13, "bold"))
        c.create_rectangle(w-95, 91, w-20, 159, outline=GOLD, width=2)
        c.create_text(w-57, 125, text=f"θ={self.threshold.get()}", fill=GOLD,
                      font=("Consolas", 10, "bold"))
        c.create_text(w/2, 28, text="WEIGHTED SUM  →  THRESHOLD  →  OUTPUT", fill=MUTED,
                      font=("Segoe UI", 9, "bold"))
        c.create_text(w/2, 225, text=f"W₁={self.w1.get()}    W₂={self.w2.get()}    NET={self.calculate(self.x1.get(), self.x2.get())[0]}",
                      fill=ACCENT, font=("Consolas", 10))

    def _update_table(self, active_a, active_b):
        for item in self.table.get_children():
            self.table.delete(item)
        for a, b in ((1, 1), (1, 0), (0, 1), (0, 0)):
            net, y = self.calculate(a, b)
            tag = "active" if (a, b) == (active_a, active_b) else "normal"
            self.table.insert("", "end", values=(a, b, net, y), tags=(tag,))

    def show_truth_table(self):
        win = tk.Toplevel(self.root)
        win.title("Tabel Kebenaran Lengkap")
        win.configure(bg=BG)
        win.geometry("460x340")
        tk.Label(win, text="TABEL KEBENARAN", bg=BG, fg=ACCENT,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w", padx=20, pady=18)
        tree = ttk.Treeview(win, columns=("x1", "x2", "net", "y"), show="headings", height=5)
        for col, title in (("x1", "X₁"), ("x2", "X₂"), ("net", "NET"), ("y", "OUTPUT Y")):
            tree.heading(col, text=title)
            tree.column(col, anchor="center", width=95)
        tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        for a, b in ((1, 1), (1, 0), (0, 1), (0, 0)):
            net, y = self.calculate(a, b)
            tree.insert("", "end", values=(a, b, net, y))

    def reset(self):
        self.x1.set(1)
        self.x2.set(1)
        self.w1.set(1)
        self.w2.set(1)
        self.threshold.set(2)
        self.gate.set("AND")
        self.update_result()

if __name__ == "__main__":
    root = tk.Tk()
    app = McCullochPittsApp(root)
    root.mainloop()