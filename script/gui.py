import tkinter as tk
from model import process_trigrams
from textwrap import wrap


def main():
    def delete_excess_children_widgets():
        children = root.winfo_children()
        if len(children) >= 3:
            children[-1].pack_forget()

    def manage_excess():
        text = label_value.get()
        text = "\n".join(wrap(text, 45))
        label_value.set(text)

    # noinspection PyUnusedLocal
    def my_tracer(*args):
        del args
        new_text: str = entry.get().strip()
        split_text = new_text.split()
        label_value.set(new_text)
        delete_excess_children_widgets()
        if len(split_text) >= 2 and new_text[-1] != " ":
            tail = trigram_model.get_tail(split_text[-2:])
            if tail != "not found":
                label_value.set(new_text + " " + tail)
            else:
                temp_label.pack()
        manage_excess()

    def set_window_config():
        root.title("Word Generator")
        x_coords, y_coords = int(root.winfo_screenwidth() / 2 - window_width / 2), int(
            (root.winfo_screenheight() / 2 - window_height / 2))
        root.geometry(f"{window_width}x{window_height}+{x_coords}+{y_coords}")

    window_width, window_height = 350, 150
    # -------------- EXECUTION --------------
    trigram_model = process_trigrams()
    root = tk.Tk()
    set_window_config()

    # creation of linked variable, from entry to label
    entry_value = tk.StringVar()
    entry_value.trace("w", my_tracer)

    label_value = tk.StringVar()

    # creation of both label and entry with shared variable
    entry = tk.Entry(root, textvariable=entry_value, width=window_width)
    label = tk.Label(root, textvariable=label_value)
    label.pack(padx=30)
    entry.pack(pady=30, padx=30)
    temp_label = tk.Label(root, text="No matches found in model")

    root.mainloop()


if __name__ == '__main__':
    main()
