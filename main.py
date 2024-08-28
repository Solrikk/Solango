import tkinter as tk
from tkinter import ttk, messagebox
from transformers import MarianMTModel, MarianTokenizer
from PIL import Image, ImageTk

class TranslatorApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Solango - Простой Переводчик")
        self.root.geometry("950x650")
        self.root.configure(bg="#F0F0F0")

        self.model_name_en_ru = 'Helsinki-NLP/opus-mt-en-ru'
        self.model_name_ru_en = 'Helsinki-NLP/opus-mt-ru-en'
        self.tokenizer_en_ru = MarianTokenizer.from_pretrained(self.model_name_en_ru)
        self.model_en_ru = MarianMTModel.from_pretrained(self.model_name_en_ru)
        self.tokenizer_ru_en = MarianTokenizer.from_pretrained(self.model_name_ru_en)
        self.model_ru_en = MarianMTModel.from_pretrained(self.model_name_ru_en)

        self.current_direction = "en_ru"

        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Helvetica", 10), background="#F0F0F0")
        style.configure("TButton", font=("Helvetica", 10, "bold"), background="#4A6FA5", foreground="white", padding=6)
        style.map("TButton", background=[('active', '#3A5982')], foreground=[('active', 'white')])
        style.configure("TFrame", background="#F0F0F0")

        main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        main_frame.pack(expand=True, fill="both")

        title_label = ttk.Label(main_frame, text="Добро пожаловать в Solango!", font=("Helvetica", 16, "bold"), foreground="#4A6FA5")
        title_label.pack(pady=10)

        try:
            icon_image = Image.open("translator_icon.png").resize((50, 50), Image.Resampling.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label = ttk.Label(main_frame, image=icon_photo, background="#F0F0F0")
            icon_label.image = icon_photo
            icon_label.pack(pady=10)
        except Exception:
            pass

        self.direction_button = tk.Button(main_frame, text="EN → RU", command=self.toggle_direction, bg="#4A6FA5", fg="white", font=("Helvetica", 10, "bold"))
        self.direction_button.pack(pady=10)

        self.input_label = ttk.Label(main_frame, text="Введите текст на английском:", font=("Helvetica", 12))
        self.input_label.pack(pady=5)

        self.input_text = tk.Text(main_frame, height=5, width=50, font=("Helvetica", 10), wrap="word", padx=10, pady=10, bd=2, relief="flat", bg="#FFFFFF", fg="#333333")
        self.input_text.pack(pady=10)
        self.input_text.config(highlightbackground="#D3D3D3", highlightthickness=1, bd=0)

        translate_button = tk.Button(main_frame, text="Перевести", command=self.translate_text, bg="#4A6FA5", fg="white", font=("Helvetica", 10, "bold"))
        translate_button.pack(pady=10)

        self.output_label = ttk.Label(main_frame, text="Перевод на русский:", font=("Helvetica", 12))
        self.output_label.pack(pady=5)

        self.output_text = tk.Text(main_frame, height=5, width=50, font=("Helvetica", 10), wrap="word", padx=10, pady=10, bg="#F9F9F9", fg="#333333", bd=2, relief="flat")
        self.output_text.pack(pady=10)
        self.output_text.config(highlightbackground="#D3D3D3", highlightthickness=1, bd=0)

        footer_label = ttk.Label(main_frame, text="Solango © 2024", font=("Helvetica", 8), foreground="#777777")
        footer_label.pack(side="bottom", pady=10)

    def toggle_direction(self):
        if self.current_direction == "en_ru":
            self.current_direction = "ru_en"
            self.direction_button.config(text="RU → EN")
            self.input_label.config(text="Введите текст на русском:")
            self.output_label.config(text="Перевод на английский:")
        else:
            self.current_direction = "en_ru"
            self.direction_button.config(text="EN → RU")
            self.input_label.config(text="Введите текст на английском:")
            self.output_label.config(text="Перевод на русский:")

    def translate_text(self):
        source_text = self.input_text.get("1.0", tk.END).strip()
        if source_text:
            if self.current_direction == "en_ru":
                tokenizer, model = self.tokenizer_en_ru, self.model_en_ru
            else:
                tokenizer, model = self.tokenizer_ru_en, self.model_ru_en

            try:
                inputs = tokenizer(source_text, return_tensors="pt", padding=True)
                translated = model.generate(**inputs)
                translated_text = [tokenizer.decode(t, skip_special_tokens=True, clean_up_tokenization_spaces=True) for t in translated]
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, translated_text[0])
            except Exception as e:
                messagebox.showerror("Ошибка перевода", f"Произошла ошибка во время перевода: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()
