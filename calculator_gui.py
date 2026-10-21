from tkinter import messagebox

import tkinter as tk

from calculator_engine import (
    evaluate_expression,
    load_history,
    save_history,
)

history = load_history()
just_calculated = False


# ===== カラーテーマ =====
BG = "#17191F"
DISPLAY_BG = "#23262E"
BUTTON_BG = "#2B2E37"
FUNCTION_BG = "#414550"
OPERATOR_BG = "#7774E8"
EQUAL_BG = "#5C59D6"
TEXT_COLOR = "#FFFFFF"
MUTED_COLOR = "#A5A7B0"


# ===== ウィンドウ =====
root = tk.Tk()
root.title("JOY CALCULATOR")
root.geometry("360x520")
root.minsize(320, 460)
root.configure(bg=BG)


# ===== 計算状態 =====
expression = tk.StringVar(value="")
result_text = tk.StringVar(value="0")


# ===== 表示エリア =====
header = tk.Frame(root, bg=BG, padx=18, pady=16)
header.pack(fill="x")

tk.Label(
    header,
    text="JOY CALCULATOR",
    font=("Segoe UI", 16, "bold"),
    fg=TEXT_COLOR,
    bg=BG,
).pack(anchor="w")

tk.Label(
    header,
    text="PYTHON EDITION",
    font=("Segoe UI", 8),
    fg=MUTED_COLOR,
    bg=BG,
).pack(anchor="w", pady=(3, 0))


display = tk.Frame(
    root,
    bg=DISPLAY_BG,
    padx=16,
    pady=14,
)
display.pack(fill="x", padx=14, pady=(0, 14))

tk.Label(
    display,
    text="計算式",
    font=("Segoe UI", 9),
    fg=MUTED_COLOR,
    bg=DISPLAY_BG,
).pack(anchor="e")

expression_label = tk.Label(
    display,
    textvariable=expression,
    font=("Consolas", 18),
    fg=TEXT_COLOR,
    bg=DISPLAY_BG,
    anchor="e",
    height=2,
)
expression_label.pack(fill="x")

result_label = tk.Label(
    display,
    textvariable=result_text,
    font=("Segoe UI", 24, "bold"),
    fg=TEXT_COLOR,
    bg=DISPLAY_BG,
    anchor="e",
)
result_label.pack(fill="x")


# ===== ボタン処理 =====
def press(value):
    global just_calculated

    current = expression.get()

    if just_calculated:
        if value in "+-*/^%":
            current = result_text.get()
        else:
            current = ""

        just_calculated = False

    expression.set(current + value)
    result_text.set("")


def clear():
    global just_calculated

    expression.set("")
    result_text.set("0")
    just_calculated = False

def delete_last():
    """計算式の最後の1文字を削除する。"""
    expression.set(expression.get()[:-1])
    result_text.set("")


def calculate():
    global just_calculated

    exp = expression.get().strip()

    if not exp:
        return

    try:
        result = evaluate_expression(exp)

        result_text.set(str(result))

        history.append(f"{exp}={result}")
        save_history(history)  # ← この1行を追加

        just_calculated = True

    except ZeroDivisionError:
        result_text.set("0で割ることはできません")
        just_calculated = False

    except (ValueError, IndexError, OverflowError):
        result_text.set("計算式が正しくありません")
        just_calculated = False

def show_history():
    if not history:
        messagebox.showinfo("計算履歴", "履歴はありません。")
        return

    history_window = tk.Toplevel(root)
    history_window.title("計算履歴")
    history_window.geometry("380x450")
    history_window.configure(bg=BG)

    tk.Label(
        history_window,
        text="計算履歴",
        font=("Arial", 16, "bold"),
        bg=BG,
        fg=TEXT_COLOR,
    ).pack(pady=10)

    listbox = tk.Listbox(
        history_window,
        font=("Consolas", 12),
        bg=DISPLAY_BG,
        fg=TEXT_COLOR,
        selectbackground=OPERATOR_BG,
        selectforeground="white",
    )
    listbox.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=8,
    )

    # 履歴を新しい順に表示する
    def refresh_history():
        listbox.delete(0, tk.END)

        for item in reversed(history):
            listbox.insert(tk.END, item)

    refresh_history()

    # 選択された履歴の位置を取得する
    def get_selected_index():
        selection = listbox.curselection()

        if not selection:
            messagebox.showwarning(
                "履歴の選択",
                "履歴を選択してください。",
                parent=history_window,
            )
            return None

        # 表示順は逆なので、元のリストの位置に変換する
        return len(history) - 1 - selection[0]

    # 選択した式を再利用する
    def use_selected_history():
        index = get_selected_index()

        if index is None:
            return

        selected = history[index]

        if "=" in selected:
            selected = selected.rsplit("=", 1)[0]

        expression.set(selected)
        result_text.set("")

        history_window.destroy()

    # 選択した履歴だけ削除する
    def delete_selected_history():
        index = get_selected_index()

        if index is None:
            return

        selected = history[index]

        confirmed = messagebox.askyesno(
            "履歴の削除",
            f"この履歴を削除しますか？\n\n{selected}",
            parent=history_window,
        )

        if not confirmed:
            return

        del history[index]

        save_history(history)
        refresh_history()

        if not history:
            history_window.destroy()
            messagebox.showinfo(
                "計算履歴",
                "すべての履歴を削除しました。",
            )

    # すべての履歴を削除する
    def delete_all_history():
        if not history:
            return

        confirmed = messagebox.askyesno(
            "履歴の全件削除",
            "すべての計算履歴を削除しますか？\n"
            "この操作は取り消せません。",
            parent=history_window,
        )

        if not confirmed:
            return

        history.clear()

        save_history(history)
        refresh_history()

        history_window.destroy()

        messagebox.showinfo(
            "計算履歴",
            "すべての履歴を削除しました。",
        )

    # ボタンエリア
    button_frame = tk.Frame(history_window, bg=BG)
    button_frame.pack(fill="x", padx=12, pady=10)

    tk.Button(
        button_frame,
        text="式を再利用",
        command=use_selected_history,
        bg=EQUAL_BG,
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
    ).pack(fill="x", pady=3)

    tk.Button(
        button_frame,
        text="選択した履歴を削除",
        command=delete_selected_history,
        bg=FUNCTION_BG,
        fg="white",
        font=("Arial", 10),
        relief="flat",
    ).pack(fill="x", pady=3)

    tk.Button(
        button_frame,
        text="全件削除",
        command=delete_all_history,
        bg="#A83D4D",
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat",
    ).pack(fill="x", pady=3)

def handle_key(event):
    key = event.keysym
    char = event.char

    # 数字・演算子・カッコ・小数点を入力
    if char and char in "0123456789.+-*/%^()":
        press(char)

    # Enter またはテンキーの Enter で計算
    elif key in ("Return", "KP_Enter"):
        calculate()

    # Backspace で1文字削除
    elif key == "BackSpace":
        delete_last()

    # Escape で全消去
    elif key in ("Escape", "Delete"):
        clear()

    # キー入力をほかのウィジェットに伝播させない
    return "break"

# ===== ボタン配置 =====
button_area = tk.Frame(root, bg=BG)
button_area.pack(fill="both", expand=True, padx=14, pady=(0, 14))

buttons = [
    ("AC",   0, 0, FUNCTION_BG, clear),
    ("(",    0, 1, FUNCTION_BG, lambda: press("(")),
    (")",    0, 2, FUNCTION_BG, lambda: press(")")),
    ("%",    0, 3, OPERATOR_BG, lambda: press("%")),
    ("÷",    0, 4, OPERATOR_BG, lambda: press("/")),

    ("7",    1, 0, BUTTON_BG, lambda: press("7")),
    ("8",    1, 1, BUTTON_BG, lambda: press("8")),
    ("9",    1, 2, BUTTON_BG, lambda: press("9")),
    ("^",    1, 3, OPERATOR_BG, lambda: press("^")),
    ("×",    1, 4, OPERATOR_BG, lambda: press("*")),

    ("4",    2, 0, BUTTON_BG, lambda: press("4")),
    ("5",    2, 1, BUTTON_BG, lambda: press("5")),
    ("6",    2, 2, BUTTON_BG, lambda: press("6")),
    ("⌫",    2, 3, FUNCTION_BG, delete_last),
    ("−",    2, 4, OPERATOR_BG, lambda: press("-")),

    ("1",    3, 0, BUTTON_BG, lambda: press("1")),
    ("2",    3, 1, BUTTON_BG, lambda: press("2")),
    ("3",    3, 2, BUTTON_BG, lambda: press("3")),
    (".",    3, 3, BUTTON_BG, lambda: press(".")),
    ("+",    3, 4, OPERATOR_BG, lambda: press("+")),

    ("履歴", 4, 0, FUNCTION_BG, show_history),
    ("0",    4, 1, BUTTON_BG, lambda: press("0")),
    ("00",   4, 2, BUTTON_BG, lambda: press("00")),
    ("⌫",    4, 3, FUNCTION_BG, delete_last),
    ("=",    4, 4, EQUAL_BG, calculate),
]

for text, row, col, color, command in buttons:
    button = tk.Button(
        button_area,
        text=text,
        command=command,
        font=("Segoe UI", 14, "bold"),
        fg=TEXT_COLOR,
        bg=color,
        activebackground=color,
        activeforeground=TEXT_COLOR,
        relief="flat",
        bd=0,
        cursor="hand2",
    )

    button.grid(
        row=row,
        column=col,
        sticky="nsew",
        padx=4,
        pady=4,
    )

for row in range(5):
    button_area.rowconfigure(row, weight=1)

for col in range(5):
    button_area.columnconfigure(col, weight=1)

# ===== キーボード操作 =====
root.bind_all("<Key>", handle_key)

# ===== 起動 =====
root.mainloop()
