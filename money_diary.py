import csv
import tkinter
import tkinter.ttk as ttk

DATABASE_FILE = "money_database.csv"


# ツリービューにデータを挿入する関数
def insert_data(row_data):
    tree.insert("", "end", values=(row_data[0], row_data[1], row_data[2]))


# ツリービューのデータを削除する関数
def delete():
    selected_ids = tree.selection()  # 選択されたアイテムのIDを取得
    print(selected_ids)
    for item_id in selected_ids:
        tree.delete(item_id)

    update_csv()


# データベースの中身をツリービューに表示する関数
def reflect_database():
    with open(DATABASE_FILE, "r", encoding="utf-8-sig", errors="ignore") as f:
        data_list = list(csv.reader(f))

    for data in data_list:
        insert_data(data)


# csvを更新する関数
def update_csv():
    all_ids = tree.get_children()  # ツリービューに表示されている全てのアイテムを取得
    all_data = []
    for item_id in all_ids:
        content = list(tree.item(item_id, "values"))
        all_data.append(content)

    print(all_data)

    with open(DATABASE_FILE, "w", encoding="utf-8-sig", errors="ignore") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows(all_data)  # 複数行に追加


# ツリービューにデータを追加する関数
def add():
    add_window()
    add_button.config(state="disabled")
    edit_button.config(state="disabled")
    delete_button.config(state="disabled")


# 追加ウィンドウ（サブウィンドウ）を作成する関数
def add_window():
    global date_entry, category_entry, money_entry, add_subwindow
    add_subwindow = tkinter.Toplevel()
    add_subwindow.geometry("200x200")
    add_subwindow.title("データ追加")

    date_label = tkinter.Label(add_subwindow, text="日付")
    date_entry = tkinter.Entry(add_subwindow, width=20)
    date_label.grid(row=0, column=0, padx=10, pady=20)
    date_entry.grid(row=0, column=1, padx=10, pady=20)

    category_label = tkinter.Label(add_subwindow, text="内訳")
    category_entry = tkinter.Entry(add_subwindow)
    category_label.grid(row=1, column=0, padx=10, pady=(0, 20))
    category_entry.grid(row=1, column=1, padx=10, pady=(0, 20))

    money_label = tkinter.Label(add_subwindow, text="金額")
    money_entry = tkinter.Entry(add_subwindow)
    money_label.grid(row=2, column=0, padx=10, pady=(0, 20))
    money_entry.grid(row=2, column=1, padx=10, pady=(0, 20))

    save_button = tkinter.Button(add_subwindow, text="保存", command=add_row)
    save_button.grid(row=3, column=0, columnspan=2)


# 行を追加する関数
def add_row():
    new_date = date_entry.get()
    new_category = category_entry.get()
    new_money = money_entry.get()
    new_data = [new_date, new_category, new_money]
    insert_data(new_data)
    update_csv()
    add_subwindow.destroy()

    add_button.config(state="normal")
    edit_button.config(state="normal")
    delete_button.config(state="normal")


# ツリービューのデータを編集する関数
def edit():
    global selected_id
    selected_id = tree.selection()[0]  # 選択されている一番初めのidを取得
    if len(selected_id) > 0:
        selected_data = tree.item(selected_id, "values")
        edit_window(selected_data)

        add_button.config(state="disabled")
        edit_button.config(state="disabled")
        delete_button.config(state="disabled")


# 編集ウィンドウ（サブウィンドウ）を作成する関数
def edit_window(selected_data):
    global date_entry, category_entry, money_entry, edit_subwindow
    edit_subwindow = tkinter.Toplevel()
    edit_subwindow.geometry("200x200")
    edit_subwindow.title("データ追加")

    date_label = tkinter.Label(edit_subwindow, text="日付")
    date_entry = tkinter.Entry(edit_subwindow, width=20)
    date_label.grid(row=0, column=0, padx=10, pady=20)
    date_entry.grid(row=0, column=1, padx=10, pady=20)

    date_entry.insert(0, selected_data[0])

    category_label = tkinter.Label(edit_subwindow, text="内訳")
    category_entry = tkinter.Entry(edit_subwindow)
    category_label.grid(row=1, column=0, padx=10, pady=(0, 20))
    category_entry.grid(row=1, column=1, padx=10, pady=(0, 20))

    category_entry.insert(0, selected_data[1])

    money_label = tkinter.Label(edit_subwindow, text="金額")
    money_entry = tkinter.Entry(edit_subwindow)
    money_label.grid(row=2, column=0, padx=10, pady=(0, 20))
    money_entry.grid(row=2, column=1, padx=10, pady=(0, 20))

    money_entry.insert(0, selected_data[2])

    save_button = tkinter.Button(edit_subwindow, text="保存", command=edit_row)
    save_button.grid(row=3, column=0, columnspan=2)


# 行を編集する関数
def edit_row():
    tree.delete(selected_id)  # 編集前のデータを削除する

    new_date = date_entry.get()
    new_category = category_entry.get()
    new_money = money_entry.get()
    new_data = [new_date, new_category, new_money]
    insert_data(new_data)
    update_csv()
    edit_subwindow.destroy()

    add_button.config(state="normal")
    edit_button.config(state="normal")
    delete_button.config(state="normal")


if __name__ == "__main__":
    # ウィンドウの作成
    root = tkinter.Tk()
    root.title("家計簿アプリ")
    root.iconbitmap("money_diary.ico")
    root.geometry("500x350")
    root.resizable(False, False)

    # フレームの作成
    output_frame = tkinter.Frame(root)
    button_frame = tkinter.Frame(root)
    output_frame.pack()
    button_frame.pack()

    # ツリービューの作成
    tree = ttk.Treeview(output_frame)
    tree["columns"] = (1, 2, 3)
    tree["show"] = "headings"  # 自分が設定した見出しのみを表示

    # カラム幅の設定
    tree.column(1, width=130)
    tree.column(2, width=130)
    tree.column(3, width=130)

    # カラムの見出し設定
    tree.heading(1, text="日付")
    tree.heading(2, text="内訳")
    tree.heading(3, text="金額")

    # ツリービューの配置
    tree.pack(pady=20)

    # データベースの中身をツリービューに表示
    reflect_database()

    # テーブルデータ編集に関するボタンの作成
    add_button = tkinter.Button(button_frame, text="追加", borderwidth=2, command=add)
    edit_button = tkinter.Button(button_frame, text="編集", borderwidth=2, command=edit)
    delete_button = tkinter.Button(
        button_frame, text="削除", borderwidth=2, command=delete
    )
    add_button.grid(row=0, column=0, padx=5, pady=15, ipadx=5)
    edit_button.grid(row=0, column=1, padx=5, pady=15, ipadx=5)
    delete_button.grid(row=0, column=2, padx=5, pady=15, ipadx=5)

    # ループ処理
    root.mainloop()
