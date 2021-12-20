import tkinter as tk
from model import process_trigrams
from textwrap import wrap


def main():
    def delete_excess_children_widgets():
        children = root.winfo_children()
        if len(children) >= 4:
            no_match_label.grid_forget()

    def manage_excess_label():
        text = word_gen_label_value.get()
        text = "\n".join(wrap(text, 45))
        word_gen_label_value.set(text)

    def format_likely_words(tails: tuple) -> str:
        tails, freqs = tails
        total_freq = sum(freqs)
        string = [f"{tail}: {round((freq / total_freq)*100, 2)}%" for tail, freq in zip(tails, freqs)]
        string = "\n".join(string)
        return string

    # noinspection PyUnusedLocal
    def my_tracer(*args):
        del args
        new_text: str = entry_value.get().strip()
        split_text = new_text.split()
        word_gen_label_value.set(new_text)
        delete_excess_children_widgets()
        if len(split_text) >= 2 and new_text[-1] != " ":
            tails = trigram_model.get_n_tail(split_text[-2:], False)
            if tails != "not found":
                main_tail, tails = tails
                word_gen_label_value.set(new_text + " " + main_tail)
                tails = format_likely_words(tails)
                likely_words_label_value.set(tails)
            else:
                no_match_label.grid(row=3, column=0, columnspan=2)
        manage_excess_label()

    def set_window_config():
        root.title("Word Generator")
        x_coords, y_coords = int(root.winfo_screenwidth() / 2 - window_width / 2), int(
            (root.winfo_screenheight() / 2 - window_height / 2))
        root.geometry(f"{window_width}x{window_height}+{x_coords}+{y_coords}")

    window_width, window_height = 450, 250
    # -------------- EXECUTION --------------
    trigram_model = process_trigrams()
    root = tk.Tk()
    set_window_config()

    # creation of linked variable, from entry to word_gen_label
    entry_value = tk.StringVar()
    entry_value.trace("w", my_tracer)

    word_gen_label_value = tk.StringVar()

    # creation of both word_gen_label and entry with shared variable
    word_gen_label = tk.Label(root, textvariable=word_gen_label_value, width=30).grid(row=0, column=0, padx=30)
    entry = tk.Entry(root, textvariable=entry_value, width=29).grid(row=1, column=0, pady=30, padx=30)
    no_match_label = tk.Label(root, text="No matches found in model")

    # most likely words label
    likely_words_label_value = tk.StringVar()
    likely_words_label = tk.Label(root, textvariable=likely_words_label_value).grid(row=0, column=1)

    root.mainloop()


if __name__ == '__main__':
    main()
