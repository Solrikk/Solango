import tkinter as tk
from tkinter import ttk
from transformers import MarianMTModel, MarianTokenizer

model_name = 'Helsinki-NLP/opus-mt-en-ru'
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_text():
    source_text = input_text.get("1.0", tk.END).strip()
    if source_text:
        inputs = tokenizer(source_text, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        translated_text = [tokenizer.decode(t, skip_special_tokens=True, clean_up_tokenization_spaces=True) for t in translated]
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated_text[0])

root = tk.Tk()
root.title("Solango - Простой Переводчик")
root.geometry("600x450")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 12), background="#f0f0f0")
style.configure("TButton", font=("Helvetica", 12), background="#007ACC", foreground="white", padding=10)
style.configure("TFrame", background="#f0f0f0")

header_frame = ttk.Frame(root, padding="10", style="TFrame")
header_frame.pack(side="top", fill="x")

title_label = ttk.Label(header_frame, text="Добро пожаловать в Solango!", font=("Helvetica", 16, "bold"), foreground="#007ACC")
title_label.pack(pady=10)

frame = ttk.Frame(root, padding="10", style="TFrame")
frame.pack(expand=True)

input_label = ttk.Label(frame, text="Введите текст на английском:")
input_label.grid(row=0, column=0, sticky="w", pady=5)

input_text = tk.Text(frame, height=6, width=50, font=("Helvetica", 12), wrap="word", padx=10, pady=10)
input_text.grid(row=1, column=0, pady=5)

translate_button = ttk.Button(frame, text="Перевести", command=translate_text)
translate_button.grid(row=2, column=0, pady=10)

output_label = ttk.Label(frame, text="Перевод на русский:")
output_label.grid(row=3, column=0, sticky="w", pady=5)

output_text = tk.Text(frame, height=6, width=50, font=("Helvetica", 12), wrap="word", padx=10, pady=10, bg="#e0e0e0", fg="#333333")
output_text.grid(row=4, column=0, pady=5)

footer_label = ttk.Label(root, text="Solango © 2024", font=("Helvetica", 10), background="#f0f0f0", foreground="#666666")
footer_label.pack(side="bottom", pady=10)

root.mainloop()
