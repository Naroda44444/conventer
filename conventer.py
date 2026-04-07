import os
from typing import Optional
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image


class ImageConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Instant Image Converter")
        self.geometry("700x520")
        self.file_path = ""
        self.preview_img = None
        self.drop = ctk.CTkLabel(
            self,
            text="Drop area\nПеретягніть файл або натисніть вибрати файл",
            height=90,
        )

        self.drop.pack(fill="x", padx=16, pady=(16, 8))
        
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=16)
        ctk.CTkButton(top, text="Виберіть файл", command=self.pick_file).pack(side="left")
        self.path_lbl = ctk.CTkLabel(top, text="Файли не вибрано", anchor="w")
        self.path_lbl.pack(side="left", fill="x", expand=True, padx=(10,))
        
        box = ctk.CTkFrame(self)
        box.pack(fill="x", padx=16, pady=10)
        self.format_box = ctk.CTkComboBox(
            box,
            values=["JPEG", "PNG", "BMP", "GIF", "TIFF"],
            state="readonly",
        )
        self.format_box.set("JPEG")
        self.format_box.grid(row=0, column=0, padx=0, sticky="ew")
        self.q_lbl = ctk.CTkLabel(box, text="Якість (для JPG)", anchor="w")
        self.q_lbl.grid(row=0, column=1, padx=(10, 0), sticky="w")
        self.quality = ctk.CTkSlider(
            box,
            from_=1,
            to=100,
            number_of_steps=99,
            command=lambda v: self.q_lbl.configure(text=f"Якість: {int(float(v))}%")
        )
        self.quality.set(85)
        self.quality.grid(row=1, column=0, columnspan=2, padx=8, sticky="ew")
        
        self.r_lbl = ctk.CTkLabel(box, text="Resize: 100%")
        self.r_lbl.grid(row=2, column=0, padx=(0, 10), sticky="w")
        self.resize = ctk.CTkSlider(
            box,
            from_=10,
            to=200,
            number_of_steps=190,
            command=lambda v: self.r_lbl.configure(text=f"Resize: {int(float(v))}%")
        )
        self.resize.set(100)
        self.resize.grid(row=3, column=0, columnspan=2, padx=8, sticky="ew")
        box.grid_columnconfigure((0, 1), weight=1)
        
        ctk.CTkButton(self, text="Convert", height=40, command=self.convert).pack(fill="x", padx=16)
        self.progress = ctk.CTkProgressBar(self)
        self.progress.set(0)
        self.progress.pack(fill="x", padx=16, pady=10)
        self.preview = ctk.CTkLabel(self, text="Прев'ю зображення", height=200)
        self.preview.pack(fill="both", padx=16, pady=(0, 16), expand=True)

    def pick_file(self):
        p = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff"),
                ("All files", "*.*"),
            ]
        )
        if p:
            self.set_file(p)

    def set_file(self, path):
        if not os.path.isfile(path):
            return
        self.file_path = path
        self.path_lbl.configure(text=path)
        try:
            img = Image.open(path)
            img.thumbnail((260, 170))
            self.preview_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.preview.configure(image=self.preview_img, text="")
        except Exception as e:
            self.preview.configure(text="Неможливо завантажити зображення", image="")

    def convert(self):
        if not self.file_path:
            return messagebox.showwarning("Увага", "Спочатку виберіть файл для конвертації.")
        try:
            self.progress.set(0.2)
            self.update_idletasks()
            target = self.format_box.get()
            quality = int(self.quality.get())
            scale = int(self.resize.get())
            name, _ = os.path.splitext(self.file_path)
            out = f"{name}_converted.{target.lower()}"
            img = Image.open(self.file_path)
            
            if scale != 100:
                new_size = (
                    max(1, img.width * scale // 100),
                    max(1, img.height * scale // 100)
                )
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            self.progress.set(0.9)
            self.update_idletasks()
            
            if target == "JPEG":
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")
                img.save(out, "JPEG", quality=quality)
            else:
                img.save(out, target)
            
            self.progress.set(1)
            messagebox.showinfo("ГОТОВО", f"ГОТОВО! ФАЙЛ ЗБЕРЕЖЕНО ЯК \n{out}")
        except Exception as e:
            self.progress.set(0)
            messagebox.showerror("Помилка", str(e))


if __name__ == "__main__":
    ImageConverterApp().mainloop()