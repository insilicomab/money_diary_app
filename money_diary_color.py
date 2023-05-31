import csv
import tkinter
import tkinter.ttk as ttk
from tkinter import DISABLED, NORMAL


# ★バグ対応用の関数を追加
def fixed_map(option):
    return [
        elm
        for elm in style.map("Treeview", query_opt=option)
        if elm[:2] != ("!disabled", "!selected")
    ]


DATABASE_FILE = "money_database.csv"

# ウィンドウの作成
root = tkinter.Tk()
root.title("家計簿アプリ")
root.iconbitmap("money_diary.ico")
root.geometry("500x500")
root.resizable(0, 0)


# データベースの中身をツリービューに反映する関数
def reflect_database():
    with open(DATABASE_FILE, "r", encoding="utf-8-sig", errors="ignore") as f:
        data_list = list(csv.reader(f))

    for data in data_list:
        insert_data(data)


# データをツリービューに挿入する関数
def insert_data(row_data):
    tree.insert("", "end", values=(row_data[0], row_data[1], row_data[2]))


# フレームの作成
output_frame = tkinter.Frame(root)
button_frame = tkinter.Frame(root)
output_frame.pack()
button_frame.pack()


# ツリービューの作成
tree = ttk.Treeview(output_frame)
tree["columns"] = (1, 2, 3)  # カラム番号の設定
# tree["show"] = "headings"  # 表スタイルの設定(headingsはツリー形式ではない、通常の表形式) treeで階層を表示


# カラム幅の設定
tree.column("#0", width=80)
tree.column(1, width=80)
tree.column(2, width=80)
tree.column(3, width=80)

# カラムの見出し設定
tree.heading("#0", text="階層")
tree.heading(1, text="日付")
tree.heading(2, text="内訳")
tree.heading(3, text="金額")


# ツリービューの配置
tree.pack(pady=20)


# テーブルデータ編集に関するボタン作成
add_button = tkinter.Button(button_frame, text="追加", borderwidth=2)
edit_button = tkinter.Button(button_frame, text="編集", borderwidth=2)
delete_button = tkinter.Button(button_frame, text="削除", borderwidth=2)
add_button.grid(row=0, column=0, padx=5, pady=15, ipadx=5)
edit_button.grid(row=0, column=1, padx=5, pady=15, ipadx=5)
delete_button.grid(row=0, column=2, padx=5, pady=15, ipadx=5)


# データベースの反映
# reflect_database()

# 表スタイルの指定
style = ttk.Style()
style.configure(
    "Treeview.Heading", font=("Arial", 12, "bold"), rowheight=100, foreground="blue"
)
style.configure("Treeview", font=("Arial", 8), rowheight=30)

# ★バグ対応を処理
style.map(
    "Treeview", foreground=fixed_map("foreground"), background=fixed_map("background")
)


# データの追加
parent = tree.insert(
    "", "end", values=("cccc", "cccc", "cccc"), text="parant_data", tags="gray"
)
child = tree.insert(parent, "end", values=("ddd", "ddd", "ddd"), text="child")
tree.insert("", "end", values=("eeee", "eeee", "eeee"), text="parent_2", tags="pink")

# データの装飾
tree.tag_configure("gray", background="gray")  # tag_configure：（第1引数=tag）
tree.tag_configure("pink", foreground="pink")

# ループ処理実行
root.mainloop()
