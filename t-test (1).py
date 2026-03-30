"""
Small Sampling T-Test Analyzer
A GUI application for solving small sampling t-tests.
Maths Mini Project - Group of 6 Members
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import statistics

# ─────────────────────────────────────────────
#  MATH CORE
# ─────────────────────────────────────────────

def t_critical_value(df, alpha, two_tailed=True):
    """
    Approximate t-critical values using a lookup table for common scenarios.
    For a mini-project, we use a hardcoded table covering typical df and alpha combos.
    """
    # t-table: {df: {alpha_two_tail: t_crit}}
    t_table = {
        1:  {0.10: 6.314, 0.05: 12.706, 0.02: 31.821, 0.01: 63.657},
        2:  {0.10: 2.920, 0.05: 4.303,  0.02: 6.965,  0.01: 9.925},
        3:  {0.10: 2.353, 0.05: 3.182,  0.02: 4.541,  0.01: 5.841},
        4:  {0.10: 2.132, 0.05: 2.776,  0.02: 3.747,  0.01: 4.604},
        5:  {0.10: 2.015, 0.05: 2.571,  0.02: 3.365,  0.01: 4.032},
        6:  {0.10: 1.943, 0.05: 2.447,  0.02: 3.143,  0.01: 3.707},
        7:  {0.10: 1.895, 0.05: 2.365,  0.02: 2.998,  0.01: 3.499},
        8:  {0.10: 1.860, 0.05: 2.306,  0.02: 2.896,  0.01: 3.355},
        9:  {0.10: 1.833, 0.05: 2.262,  0.02: 2.821,  0.01: 3.250},
        10: {0.10: 1.812, 0.05: 2.228,  0.02: 2.764,  0.01: 3.169},
        11: {0.10: 1.796, 0.05: 2.201,  0.02: 2.718,  0.01: 3.106},
        12: {0.10: 1.782, 0.05: 2.179,  0.02: 2.681,  0.01: 3.055},
        13: {0.10: 1.771, 0.05: 2.160,  0.02: 2.650,  0.01: 3.012},
        14: {0.10: 1.761, 0.05: 2.145,  0.02: 2.624,  0.01: 2.977},
        15: {0.10: 1.753, 0.05: 2.131,  0.02: 2.602,  0.01: 2.947},
        16: {0.10: 1.746, 0.05: 2.120,  0.02: 2.583,  0.01: 2.921},
        17: {0.10: 1.740, 0.05: 2.110,  0.02: 2.567,  0.01: 2.898},
        18: {0.10: 1.734, 0.05: 2.101,  0.02: 2.552,  0.01: 2.878},
        19: {0.10: 1.729, 0.05: 2.093,  0.02: 2.539,  0.01: 2.861},
        20: {0.10: 1.725, 0.05: 2.086,  0.02: 2.528,  0.01: 2.845},
        21: {0.10: 1.721, 0.05: 2.080,  0.02: 2.518,  0.01: 2.831},
        22: {0.10: 1.717, 0.05: 2.074,  0.02: 2.508,  0.01: 2.819},
        23: {0.10: 1.714, 0.05: 2.069,  0.02: 2.500,  0.01: 2.807},
        24: {0.10: 1.711, 0.05: 2.064,  0.02: 2.492,  0.01: 2.797},
        25: {0.10: 1.708, 0.05: 2.060,  0.02: 2.485,  0.01: 2.787},
        26: {0.10: 1.706, 0.05: 2.056,  0.02: 2.479,  0.01: 2.779},
        27: {0.10: 1.703, 0.05: 2.052,  0.02: 2.473,  0.01: 2.771},
        28: {0.10: 1.701, 0.05: 2.048,  0.02: 2.467,  0.01: 2.763},
        29: {0.10: 1.699, 0.05: 2.045,  0.02: 2.462,  0.01: 2.756},
        30: {0.10: 1.697, 0.05: 2.042,  0.02: 2.457,  0.01: 2.750},
    }
    alpha_key = alpha if two_tailed else alpha * 2
    # clamp df to table range
    df_key = min(max(df, 1), 30)
    # find nearest available alpha
    avail = list(t_table[df_key].keys())
    closest_alpha = min(avail, key=lambda a: abs(a - alpha_key))
    return t_table[df_key][closest_alpha]


def one_sample_t_test(data, mu0, alpha, tail):
    n = len(data)
    mean = statistics.mean(data)
    std  = statistics.stdev(data)   # sample std dev (n-1)
    se   = std / math.sqrt(n)
    t_stat = (mean - mu0) / se
    df = n - 1
    two_tailed = (tail == "Two-tailed")
    t_crit = t_critical_value(df, alpha, two_tailed)

    if two_tailed:
        reject = abs(t_stat) > t_crit
    elif tail == "Right-tailed":
        reject = t_stat > t_crit
    else:
        reject = t_stat < -t_crit

    return {
        "n": n, "mean": mean, "std": std, "se": se,
        "t_stat": t_stat, "df": df, "t_crit": t_crit,
        "reject": reject, "tail": tail, "alpha": alpha,
        "mu0": mu0
    }


def two_sample_t_test(data1, data2, alpha, tail, equal_var=True):
    n1, n2 = len(data1), len(data2)
    m1, m2 = statistics.mean(data1), statistics.mean(data2)
    s1, s2 = statistics.stdev(data1), statistics.stdev(data2)

    if equal_var:
        sp2 = ((n1 - 1)*s1**2 + (n2 - 1)*s2**2) / (n1 + n2 - 2)
        sp  = math.sqrt(sp2)
        se  = sp * math.sqrt(1/n1 + 1/n2)
        df  = n1 + n2 - 2
    else:
        se_sq = s1**2/n1 + s2**2/n2
        se = math.sqrt(se_sq)
        df_num = se_sq**2
        df_den = (s1**2/n1)**2/(n1-1) + (s2**2/n2)**2/(n2-1)
        df = int(df_num / df_den)

    t_stat = (m1 - m2) / se
    two_tailed = (tail == "Two-tailed")
    t_crit = t_critical_value(df, alpha, two_tailed)

    if two_tailed:
        reject = abs(t_stat) > t_crit
    elif tail == "Right-tailed":
        reject = t_stat > t_crit
    else:
        reject = t_stat < -t_crit

    return {
        "n1": n1, "n2": n2, "m1": m1, "m2": m2,
        "s1": s1, "s2": s2, "se": se,
        "t_stat": t_stat, "df": df, "t_crit": t_crit,
        "reject": reject, "tail": tail, "alpha": alpha,
        "equal_var": equal_var
    }


def paired_t_test(data1, data2, alpha, tail):
    if len(data1) != len(data2):
        raise ValueError("Paired samples must have equal size.")
    diffs = [a - b for a, b in zip(data1, data2)]
    return one_sample_t_test(diffs, 0, alpha, tail)


# ─────────────────────────────────────────────
#  RESULT FORMATTING
# ─────────────────────────────────────────────

def format_one_sample(r):
    lines = [
        "═" * 52,
        "          ONE-SAMPLE T-TEST RESULTS",
        "═" * 52,
        f"  Sample Size (n)        : {r['n']}",
        f"  Sample Mean (x̄)       : {r['mean']:.4f}",
        f"  Sample Std Dev (s)     : {r['std']:.4f}",
        f"  Standard Error (SE)    : {r['se']:.4f}",
        f"  Hypothesised Mean (μ₀) : {r['mu0']}",
        "─" * 52,
        f"  Degrees of Freedom     : {r['df']}",
        f"  Significance Level (α) : {r['alpha']}",
        f"  Test Type              : {r['tail']}",
        "─" * 52,
        f"  Calculated t           : {r['t_stat']:.4f}",
        f"  Critical t             : ±{r['t_crit']:.4f}" if r['tail']=="Two-tailed" else f"  Critical t  : {r['t_crit']:.4f}",
        "─" * 52,
        "  FORMULA:",
        "       x̄ - μ₀",
        "  t = ────────   where SE = s / √n",
        "         SE",
        "─" * 52,
        f"  DECISION: {'✗ REJECT H₀  →  Significant result' if r['reject'] else '✓ FAIL TO REJECT H₀  →  Not significant'}",
        "═" * 52,
    ]
    return "\n".join(lines)


def format_two_sample(r):
    lines = [
        "═" * 52,
        "         TWO-SAMPLE T-TEST RESULTS",
        "═" * 52,
        f"  Sample 1: n={r['n1']}, x̄={r['m1']:.4f}, s={r['s1']:.4f}",
        f"  Sample 2: n={r['n2']}, x̄={r['m2']:.4f}, s={r['s2']:.4f}",
        f"  Variance Assumption    : {'Equal' if r['equal_var'] else 'Unequal (Welch)'}",
        "─" * 52,
        f"  Degrees of Freedom     : {r['df']}",
        f"  Significance Level (α) : {r['alpha']}",
        f"  Test Type              : {r['tail']}",
        "─" * 52,
        f"  Standard Error (SE)    : {r['se']:.4f}",
        f"  Calculated t           : {r['t_stat']:.4f}",
        f"  Critical t             : ±{r['t_crit']:.4f}" if r['tail']=="Two-tailed" else f"  Critical t  : {r['t_crit']:.4f}",
        "─" * 52,
        "  FORMULA  (equal var):",
        "       x̄₁ - x̄₂",
        "  t = ──────────   SE = Sp·√(1/n₁+1/n₂)",
        "         SE",
        "─" * 52,
        f"  DECISION: {'✗ REJECT H₀  →  Significant difference' if r['reject'] else '✓ FAIL TO REJECT H₀  →  No significant difference'}",
        "═" * 52,
    ]
    return "\n".join(lines)


def format_paired(r):
    lines = [
        "═" * 52,
        "          PAIRED SAMPLE T-TEST RESULTS",
        "═" * 52,
        f"  No. of Pairs (n)       : {r['n']}",
        f"  Mean of Differences    : {r['mean']:.4f}",
        f"  Std Dev of Differences : {r['std']:.4f}",
        f"  Standard Error (SE)    : {r['se']:.4f}",
        "─" * 52,
        f"  Degrees of Freedom     : {r['df']}",
        f"  Significance Level (α) : {r['alpha']}",
        f"  Test Type              : {r['tail']}",
        "─" * 52,
        f"  Calculated t           : {r['t_stat']:.4f}",
        f"  Critical t             : ±{r['t_crit']:.4f}" if r['tail']=="Two-tailed" else f"  Critical t  : {r['t_crit']:.4f}",
        "─" * 52,
        "  FORMULA:",
        "       d̄",
        "  t = ────   where SE = Sd / √n",
        "       SE",
        "─" * 52,
        f"  DECISION: {'✗ REJECT H₀  →  Significant difference' if r['reject'] else '✓ FAIL TO REJECT H₀  →  No significant difference'}",
        "═" * 52,
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────
#  GUI
# ─────────────────────────────────────────────

DARK_BG     = "#0f1117"
PANEL_BG    = "#1a1d27"
ACCENT      = "#4f8ef7"
ACCENT2     = "#7c5cbf"
SUCCESS     = "#2ecc71"
DANGER      = "#e74c3c"
TEXT        = "#e8eaf0"
MUTED       = "#7a7f94"
BORDER      = "#2e3347"
ENTRY_BG    = "#252836"
MONO        = ("Courier New", 10)
HEADER_FONT = ("Georgia", 18, "bold")
LABEL_FONT  = ("Segoe UI", 10)
SMALL_FONT  = ("Segoe UI", 9)


class TTestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Small Sampling T-Test Calculator")
        self.configure(bg=DARK_BG)
        self.geometry("900x720")
        self.minsize(820, 660)
        self._build_ui()

    # ── helpers ──────────────────────────────
    def _lbl(self, parent, text, font=LABEL_FONT, fg=TEXT, **kw):
        return tk.Label(parent, text=text, font=font, fg=fg, bg=parent["bg"], **kw)

    def _entry(self, parent, width=30):
        e = tk.Entry(parent, width=width, font=MONO,
                     bg=ENTRY_BG, fg=TEXT, insertbackground=ACCENT,
                     relief="flat", bd=0, highlightthickness=1,
                     highlightbackground=BORDER, highlightcolor=ACCENT)
        return e

    def _btn(self, parent, text, cmd, color=ACCENT):
        b = tk.Button(parent, text=text, command=cmd,
                      font=("Segoe UI", 10, "bold"),
                      bg=color, fg="white", activebackground=ACCENT2,
                      activeforeground="white", relief="flat",
                      padx=18, pady=6, cursor="hand2", bd=0)
        return b

    def _sep(self, parent):
        f = tk.Frame(parent, bg=BORDER, height=1)
        f.pack(fill="x", pady=8)

    # ── main layout ──────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=PANEL_BG, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📐  Small Sampling T-Test Calculator",
                 font=HEADER_FONT, fg=ACCENT, bg=PANEL_BG).pack()
        tk.Label(hdr, text="Maths Mini Project  •  Group of 6",
                 font=SMALL_FONT, fg=MUTED, bg=PANEL_BG).pack()

        # Main paned window
        paned = tk.PanedWindow(self, orient="horizontal",
                               bg=DARK_BG, sashwidth=4, sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=10, pady=8)

        # LEFT – input panel
        left = tk.Frame(paned, bg=PANEL_BG, padx=16, pady=14)
        paned.add(left, minsize=360)
        self._build_inputs(left)

        # RIGHT – output panel
        right = tk.Frame(paned, bg=PANEL_BG, padx=14, pady=14)
        paned.add(right, minsize=340)
        self._build_output(right)

    # ── input panel ──────────────────────────
    def _build_inputs(self, parent):
        self._lbl(parent, "Test Configuration", font=("Segoe UI", 11, "bold"),
                  fg=ACCENT).pack(anchor="w")
        self._sep(parent)

        # Test type
        r1 = tk.Frame(parent, bg=PANEL_BG)
        r1.pack(fill="x", pady=4)
        self._lbl(r1, "Test Type:").pack(side="left")
        self.test_type = ttk.Combobox(r1, values=["One-Sample", "Two-Sample (Independent)", "Paired"],
                                      state="readonly", width=24)
        self.test_type.current(0)
        self.test_type.pack(side="right")
        self.test_type.bind("<<ComboboxSelected>>", self._on_type_change)

        # Tail
        r2 = tk.Frame(parent, bg=PANEL_BG)
        r2.pack(fill="x", pady=4)
        self._lbl(r2, "Hypothesis Tail:").pack(side="left")
        self.tail = ttk.Combobox(r2, values=["Two-tailed", "Right-tailed", "Left-tailed"],
                                 state="readonly", width=24)
        self.tail.current(0)
        self.tail.pack(side="right")

        # Alpha
        r3 = tk.Frame(parent, bg=PANEL_BG)
        r3.pack(fill="x", pady=4)
        self._lbl(r3, "Significance Level (α):").pack(side="left")
        self.alpha = ttk.Combobox(r3, values=["0.10", "0.05", "0.02", "0.01"],
                                  state="readonly", width=24)
        self.alpha.current(1)
        self.alpha.pack(side="right")

        self._sep(parent)

        # ── Dynamic section ──
        self.dyn = tk.Frame(parent, bg=PANEL_BG)
        self.dyn.pack(fill="x")
        self._build_one_sample_inputs()

        self._sep(parent)

        # Variance option (two-sample only)
        self.var_frame = tk.Frame(parent, bg=PANEL_BG)
        self.var_frame.pack(fill="x", pady=2)
        self.equal_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.var_frame, text="Assume Equal Variances (pooled)",
                       variable=self.equal_var,
                       font=SMALL_FONT, fg=MUTED, bg=PANEL_BG,
                       selectcolor=ENTRY_BG, activebackground=PANEL_BG,
                       activeforeground=TEXT).pack(anchor="w")
        self.var_frame.pack_forget()

        # Buttons
        btn_row = tk.Frame(parent, bg=PANEL_BG)
        btn_row.pack(fill="x", pady=10)
        self._btn(btn_row, "  Calculate  ", self._calculate).pack(side="left", padx=4)
        self._btn(btn_row, "  Clear  ", self._clear, color=MUTED).pack(side="left", padx=4)

        # Quick ref t-table button
        self._btn(parent, "📋  View t-Critical Table", self._show_table,
                  color="#2c3e50").pack(pady=6, fill="x")

    def _build_one_sample_inputs(self):
        for w in self.dyn.winfo_children():
            w.destroy()

        self._lbl(self.dyn, "Sample Data (comma-separated):",
                  font=("Segoe UI", 10, "bold"), fg=ACCENT2).pack(anchor="w", pady=(0, 4))
        self.data1 = self._entry(self.dyn, 40)
        self.data1.pack(fill="x", ipady=5, pady=2)
        tk.Label(self.dyn, text="e.g.  12.3, 14.5, 11.8, 13.0, 15.2",
                 font=SMALL_FONT, fg=MUTED, bg=PANEL_BG).pack(anchor="w")

        self._sep(self.dyn)
        self._lbl(self.dyn, "Hypothesised Population Mean (μ₀):",
                  font=("Segoe UI", 10, "bold"), fg=ACCENT2).pack(anchor="w", pady=(0, 4))
        self.mu_entry = self._entry(self.dyn, 20)
        self.mu_entry.pack(anchor="w", ipady=5)

    def _build_two_sample_inputs(self):
        for w in self.dyn.winfo_children():
            w.destroy()

        self._lbl(self.dyn, "Sample 1 Data (comma-separated):",
                  font=("Segoe UI", 10, "bold"), fg=ACCENT2).pack(anchor="w", pady=(0, 4))
        self.data1 = self._entry(self.dyn, 40)
        self.data1.pack(fill="x", ipady=5, pady=2)

        self._lbl(self.dyn, "Sample 2 Data (comma-separated):",
                  font=("Segoe UI", 10, "bold"), fg=ACCENT2).pack(anchor="w", pady=(6, 4))
        self.data2 = self._entry(self.dyn, 40)
        self.data2.pack(fill="x", ipady=5, pady=2)

    def _build_paired_inputs(self):
        for w in self.dyn.winfo_children():
            w.destroy()

        self._lbl(self.dyn, "Before / Group 1 Data:",
                  font=("Segoe UI", 10, "bold"), fg=ACCENT2).pack(anchor="w", pady=(0, 4))
        self.data1 = self._entry(self.dyn, 40)
        self.data1.pack(fill="x", ipady=5, pady=2)

        self._lbl(self.dyn, "After / Group 2 Data:",
                  font=("Segoe UI", 10, "bold"), fg=ACCENT2).pack(anchor="w", pady=(6, 4))
        self.data2 = self._entry(self.dyn, 40)
        self.data2.pack(fill="x", ipady=5, pady=2)

    def _on_type_change(self, _=None):
        t = self.test_type.get()
        if t == "One-Sample":
            self._build_one_sample_inputs()
            self.var_frame.pack_forget()
        elif t == "Two-Sample (Independent)":
            self._build_two_sample_inputs()
            self.var_frame.pack(fill="x", pady=2)
        elif t == "Paired":
            self._build_paired_inputs()
            self.var_frame.pack_forget()

    # ── output panel ─────────────────────────
    def _build_output(self, parent):
        self._lbl(parent, "Results", font=("Segoe UI", 11, "bold"),
                  fg=ACCENT).pack(anchor="w")
        self._sep(parent)

        self.result_box = scrolledtext.ScrolledText(
            parent, font=("Courier New", 10), bg=ENTRY_BG, fg=TEXT,
            relief="flat", bd=0, state="disabled",
            wrap="word", highlightthickness=1,
            highlightbackground=BORDER
        )
        self.result_box.pack(fill="both", expand=True)
        self.result_box.tag_config("reject",  foreground=DANGER,  font=("Courier New", 10, "bold"))
        self.result_box.tag_config("accept",  foreground=SUCCESS, font=("Courier New", 10, "bold"))
        self.result_box.tag_config("header",  foreground=ACCENT,  font=("Courier New", 10, "bold"))
        self.result_box.tag_config("formula", foreground=ACCENT2)

        self._show_welcome()

    def _show_welcome(self):
        msg = (
            "Welcome to the Small Sampling T-Test Calculator!\n\n"
            "Steps:\n"
            "  1. Choose Test Type (One-Sample / Two-Sample / Paired)\n"
            "  2. Enter your data values\n"
            "  3. Set α and tail type\n"
            "  4. Click  Calculate\n\n"
            "Theory:\n"
            "  Small samples: n < 30\n"
            "  Uses Student's t-distribution\n"
            "  H₀ rejected if |t_calc| > t_critical\n"
        )
        self._write_output(msg)

    # ── actions ──────────────────────────────
    def _parse_data(self, raw):
        return [float(x.strip()) for x in raw.split(",") if x.strip()]

    def _calculate(self):
        try:
            alpha = float(self.alpha.get())
            tail  = self.tail.get()
            ttype = self.test_type.get()

            if ttype == "One-Sample":
                data = self._parse_data(self.data1.get())
                if len(data) < 2:
                    raise ValueError("Need at least 2 data points.")
                mu0 = float(self.mu_entry.get())
                res = one_sample_t_test(data, mu0, alpha, tail)
                out = format_one_sample(res)
                self._write_output(out, res["reject"])

            elif ttype == "Two-Sample (Independent)":
                d1 = self._parse_data(self.data1.get())
                d2 = self._parse_data(self.data2.get())
                if len(d1) < 2 or len(d2) < 2:
                    raise ValueError("Each sample needs at least 2 points.")
                res = two_sample_t_test(d1, d2, alpha, tail, self.equal_var.get())
                out = format_two_sample(res)
                self._write_output(out, res["reject"])

            elif ttype == "Paired":
                d1 = self._parse_data(self.data1.get())
                d2 = self._parse_data(self.data2.get())
                res = paired_t_test(d1, d2, alpha, tail)
                out = format_paired(res)
                self._write_output(out, res["reject"])

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")

    def _write_output(self, text, rejected=None):
        self.result_box.configure(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", text)
        # color the DECISION line
        start = "1.0"
        while True:
            pos = self.result_box.search("DECISION:", start, stopindex="end")
            if not pos:
                break
            line_end = f"{pos} lineend"
            if rejected is True:
                self.result_box.tag_add("reject", pos, line_end)
            elif rejected is False:
                self.result_box.tag_add("accept", pos, line_end)
            start = line_end
        self.result_box.configure(state="disabled")

    def _clear(self):
        for attr in ("data1", "data2", "mu_entry"):
            if hasattr(self, attr):
                getattr(self, attr).delete(0, "end")
        self._show_welcome()

    def _show_table(self):
        win = tk.Toplevel(self)
        win.title("t-Critical Value Reference Table")
        win.configure(bg=DARK_BG)
        win.geometry("600x480")

        tk.Label(win, text="t-Critical Values (Two-Tailed)",
                 font=("Segoe UI", 12, "bold"), fg=ACCENT, bg=DARK_BG).pack(pady=10)

        cols = ("df", "α=0.10", "α=0.05", "α=0.02", "α=0.01")
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                        background=ENTRY_BG, foreground=TEXT,
                        fieldbackground=ENTRY_BG, rowheight=22,
                        font=("Courier New", 10))
        style.configure("Custom.Treeview.Heading",
                        background=PANEL_BG, foreground=ACCENT,
                        font=("Segoe UI", 10, "bold"))

        tree = ttk.Treeview(win, columns=cols, show="headings",
                            style="Custom.Treeview")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=100, anchor="center")

        t_data = {
            1:(6.314,12.706,31.821,63.657), 2:(2.920,4.303,6.965,9.925),
            3:(2.353,3.182,4.541,5.841),    4:(2.132,2.776,3.747,4.604),
            5:(2.015,2.571,3.365,4.032),    6:(1.943,2.447,3.143,3.707),
            7:(1.895,2.365,2.998,3.499),    8:(1.860,2.306,2.896,3.355),
            9:(1.833,2.262,2.821,3.250),   10:(1.812,2.228,2.764,3.169),
           11:(1.796,2.201,2.718,3.106),   12:(1.782,2.179,2.681,3.055),
           13:(1.771,2.160,2.650,3.012),   14:(1.761,2.145,2.624,2.977),
           15:(1.753,2.131,2.602,2.947),   16:(1.746,2.120,2.583,2.921),
           17:(1.740,2.110,2.567,2.898),   18:(1.734,2.101,2.552,2.878),
           19:(1.729,2.093,2.539,2.861),   20:(1.725,2.086,2.528,2.845),
           25:(1.708,2.060,2.485,2.787),   30:(1.697,2.042,2.457,2.750),
        }
        for df, vals in t_data.items():
            tree.insert("", "end", values=(df, *[f"{v:.3f}" for v in vals]))

        sb = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side="left", fill="both", expand=True, padx=(14, 0), pady=6)
        sb.pack(side="right", fill="y", pady=6, padx=(0, 14))


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = TTestApp()
    app.mainloop()
