import tkinter as tk
from main import process_trigrams


def main():
    def my_tracer(*args):
        del args
        new_text: str = entry.get()
        split_text = new_text.split()
        label_value.set(new_text)
        if len(split_text) == 2:
            tail = my_trigrams.get_tail(split_text)
            if tail != "not found":
                label_value.set(new_text + " " + tail)

    my_trigrams = process_trigrams()

    root = tk.Tk(className="My tkinter app")
    # creation of linked variable, from entry to label
    entry_value = tk.StringVar()
    entry_value.trace("w", my_tracer)

    label_value = tk.StringVar()

    # creation of both label and entry with shared variable
    entry = tk.Entry(root, textvariable=entry_value)
    entry.pack()
    label = tk.Label(root, textvariable=label_value)
    label.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
