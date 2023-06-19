from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
from typing import Set, List
import re
import json
import os
from pathlib import Path
from tkinter.font import Font


def main():
    storage_path = Path(".").absolute().parent.joinpath("ストレージ").absolute()
    if not storage_path.exists():
        messagebox.showerror("名前変更", "ストレージフォルダが見つかりません。\nストレージフォルダが配置されているフォルダに名前変更フォルダを配置してください。")
    diary_file_paths = [diary for reiwa_dir in storage_path.iterdir() for klass_dir in reiwa_dir.iterdir() for diary in
                        klass_dir.iterdir()]

    names: Set[str] = set()

    def extract_names(diary_data) -> List[str]:
        names = []
        if diary_data[10] is not None:
            for child_data in diary_data[10]:
                names.append(child_data[0])
        return names

    def reprace_name(filepath: Path, old: str, new: str):
        buffer: str = ""
        try:
            with open(filepath, mode="r", encoding="utf-8") as file:
                buffer = file.read()
            if buffer and not buffer.isspace() and old in buffer:
                with open(filepath, mode="w", encoding="utf-8") as file:
                    replaced = buffer.replace(old, new)
                    file.write(replaced)
        except:
            messagebox.showerror("名前変更", "ファイルの書き込みに失敗しました。")

    for path in diary_file_paths:
        try:
            with open(path, encoding="utf-8") as file:
                dump: str = file.read()
                if dump and not dump.isspace():
                    monthly_data = json.loads(dump)
                    for diary_data in monthly_data:
                        if diary_data is not None:
                            for name in extract_names(diary_data):
                                names.add(name)

        except:
            messagebox.showerror("名前変更", "ファイル読み込みに失敗しました。")

    root: Tk = Tk()
    root.geometry("600x200")
    root.title("名前変更")

    font = Font("", size=15)
    root.option_add("*TCombobox*Listbox.Font", font)

    old_frame: Frame = Frame(master=root)
    new_frame: Frame = Frame(master=root)

    old_label: Label = Label(master=old_frame, text="元の名前:")
    old_combo: Combobox = Combobox(master=old_frame, values=list(names), state="readonly", font=("", 20))

    new_label: Label = Label(master=new_frame, text="新しい名前:")
    new_entry: Entry = Entry(master=new_frame, font=("", 20))

    def onButtonClick():
        old_name = old_combo.get()
        if not old_name:
            return
        new_name = new_entry.get()
        if not new_name or new_name.isspace():
            return
        if new_name in names:
            messagebox.showwarning("名前変更", f'"{new_name}" は既に存在します。')
            return
        reply = messagebox.askyesno("名前変更", f'"{old_name}" を "{new_name}" へ置き換えてもいいですか？')
        if not reply:
            return
        for path in diary_file_paths:
            reprace_name(path, old_name, new_name)
        messagebox.showinfo("名前変更", "置き換えが完了しました。")
        exit()

    ok_button: Button = Button(master=root, text="OK", command=onButtonClick, width=10)

    old_label.pack(side=LEFT)
    old_combo.pack(side=RIGHT)
    new_label.pack(side=LEFT)
    new_entry.pack(side=RIGHT)
    old_frame.pack(side=TOP)
    new_frame.pack(side=TOP)
    ok_button.pack(side=BOTTOM)

    root.mainloop()


main()
