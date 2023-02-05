import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import Text
from tkinter import ttk
from PIL import Image, ImageTk
import keyboard
import time


class ImageViewer(tk.Frame):

    def __init__(self, master=None, bg="#333"):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.last_key_press = time.time()
        self.label_timer = time.time()

    def create_widgets(self):
        self.winfo_toplevel().title("Image Caption Helper")
        self.image_label = tk.Label(self)
        self.caption_text = Text(self, height=5, width=30)
        self.prev_button = tk.Button(self, text='Prev', command=self.show_prev)
        self.next_button = tk.Button(self, text='Next', command=self.show_next)
        #self.save_button = tk.Button(self, text='Save', command=self.save_caption)
        self.open_folder_button = tk.Button(self, text='Open Folder', command=self.open_folder)
        self.open_folder_button.config(bg='#555555', fg='#FFFFFF', font=('Arial', 14), width=10, height=2, bd=2, relief=tk.GROOVE)
        self.open_folder_button.pack()
        self.label = ttk.Label(root, text="")
        self.label.config(text="", foreground="lightgreen", background="#333")

    def show_image(self):
        image_file = self.image_files[self.current_image]
        image = Image.open(os.path.join(self.folder_path, image_file))
        image = image.resize((512, 512), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(image=image)
        self.image_label.image = image
        self.image_label.pack()
        caption_file = image_file.split('.')[0] + '.txt'
        self.caption_text = Text(height=10, width=50, wrap=tk.WORD)
        if os.path.exists(os.path.join(self.folder_path, caption_file)):
            with open(os.path.join(self.folder_path, caption_file)) as f:
                caption = f.read()
                self.caption_text.delete('1.0', tk.END)
                self.caption_text.insert('1.0', caption)
        else:
            self.caption_text.delete('1.0', tk.END)
        self.caption_text.pack()
        self.caption_text.bind("<KeyRelease>", self.save_caption)
        self.prev_button = tk.Button(self, text='<< Prev', command=self.show_prev)
        self.prev_button.config(bg='#000000', fg='#FFFFFF', font=('Arial', 14), width=10, height=2, bd=2, relief=tk.GROOVE)
        self.next_button = tk.Button(self, text='Next >>', command=self.show_next)
        self.next_button.config(bg='#000000', fg='#FFFFFF', font=('Arial', 14), width=10, height=2, bd=2, relief=tk.GROOVE)
        #self.save_button = tk.Button(self, text='Save', command=self.save_caption)
        self.prev_button.pack(side="left")
        self.next_button.pack(side="right")
        #self.save_button.pack()
        self.label.pack(side="bottom")
        self.open_folder_button.pack()
        keyboard.on_press_key("left", self.show_prev)
        keyboard.on_press_key("right", self.show_next)
        

    def show_prev(self, *args):
        self.label.config(text="", foreground="lightgreen", background="#333")
        current_time = time.time()
        if current_time - self.last_key_press > 0.5:
            self.label.config(text="", foreground="lightgreen", background="#333")
            if self.current_image > 0:
                self.current_image -= 1
                self.clear_widgets()
                self.show_image()
            self.last_key_press = current_time

    def show_next(self, *args):
        self.label.config(text="", foreground="lightgreen", background="#333")
        current_time = time.time()
        if current_time - self.last_key_press > 0.5:
            self.label.config(text="", foreground="lightgreen", background="#333")
            if self.current_image < len(self.image_files) - 1:
                self.current_image += 1
                self.clear_widgets()
                self.show_image()
            self.last_key_press = current_time

    def save_caption(self, event=None):
        caption_file = self.image_files[self.current_image].split('.')[0] + '.txt'
        with open(os.path.join(self.folder_path, caption_file), 'w') as f:
            f.write(self.caption_text.get('1.0', tk.END))
        self.label.config(text="Changes Saved", foreground="lightgreen", background="#333")

        
    def open_folder(self):
        self.label.config(text="")
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path
            self.image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')]
            self.current_image = 0
            self.clear_widgets()
            self.show_image()
            #self.create_widgets()

    def clear_widgets(self):
        if hasattr(self, 'image_label'):
            self.image_label.pack_forget()
        if hasattr(self, 'caption_text'):
            self.caption_text.pack_forget()
        if hasattr(self, 'prev_button'):
            self.prev_button.pack_forget()
        if hasattr(self, 'next_button'):
            self.next_button.pack_forget()
        if hasattr(self, 'save_button'):
            self.save_button.pack_forget()
        if hasattr(self, 'open_folder_button'):
            self.open_folder_button.pack_forget()

if __name__ == '__main__':
    root = tk.Tk()
    root.config(bg="#333")
    app = ImageViewer(master=root)
    app.mainloop()

