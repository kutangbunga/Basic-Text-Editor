import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os

class TextEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Editor")
        self.geometry("600x400")
        
        self.current_path = None

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        toolbar = tk.Frame(self, relief=tk.RAISED, bd=2)
        toolbar.grid(row=0, column=0, sticky="ew")

        menubtn = tk.Menubutton(toolbar,text="File", relief=tk.RAISED)
        menu = tk.Menu(menubtn,tearoff=0)
        menu.add_command(label="Open", accelerator="Ctrl+o", command=self.open_file)
        menu.add_command(label="Save", accelerator="Ctrl+s", command=self.save_file)
        menu.add_command(label="Save as", accelerator="Ctrl+Shift+S", command=self.save_as_file)
        menubtn["menu"] = menu
        menubtn.pack(side=tk.LEFT, padx=4, pady=4)

        self.text = tk.Text(self, font="Helvetica 12", undo=True, wrap="word")
        self.text.grid(row=1, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.text.config(yscrollcommand=scrollbar.set)
        
        self.text.bind("<<Modified>>", self._on_modified)

        self.bind("<Control-o>" , lambda e: self.open_file())
        self.bind("<Control-s>" , lambda e: self.save_file())
        self.bind("<Control-Shift-S>" , lambda e: self.save_as_file())

        self.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _set_title(self):
        name = os.path.basename(self.current_path) if self.current_path else "Untitled"
        self.title(f"{name} | Text Editor")

    def _maybe_discard_changes(self):
        if self.text.edit_modified():
            ans= messagebox.askyesnocancel(
                "Unsaved changes"
                "Wanna save it? Do you care?"
            )
            if ans is None:
                return False
            if ans:
                if not self.save_file():
                    return False
                
        return True
    
    def open_file(self):
        if not self._maybe_discard_changes():
            return
        
        path = askopenfilename(filetypes=[("Text FIles", "*.txt")("Asll Files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, content)
            self.current_path = path
            self._set_title()
            self.text.edit_modified(False)
        except Exception as e:
            messagebox.showerror("Open Error", f"Could not open file. \n\n{e}")

    def save_as_file(self):
        path = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text FIles", "*.txt")("Asll Files", "*.*")],
            initialfile=os.path.basename(self.current_path) if self.current_path else "untitled.txt",
            title= "Save your file as..."
        )
        if not path:
            return False
        try:
            content = self.text.get("1.0", tk.END)
            with open(path, "w", encoding="utf-8") as f:
                f. write(content)
            self. current_path = path
            self._set_title
            self.text.edit_modified(False)
            return True
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file \n\n{e}")
            return False
        
    def save_file(self):
        if not self.current_path:
            return self.save_as_file()
        try:
            content=self.text.get("1.0", tk.END)
            with open(self.current_path, "w", encoding="utf-8") as f:
                f.write(content)
            self._set_title()
            self.text.edit_modified(False)
            return True
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file \n\n{e}")
            return False
        
    def _on_modified(self, _event=None):
        base = os.path.basename(self.current_path) if self.current_path else "Untitled"
        dirty = self.text.edit_modified()
        self.title(f"{base}{' *' if dirty else ''}")
    
    def _on_close(self):
        if self._maybe_discard_changes():
            self.destroy()
    
if __name__ == "__main__":
    TextEditor().mainloop()