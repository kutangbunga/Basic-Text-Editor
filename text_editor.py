import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def main():
    window = tk.Tk()
    window.title("Text Editor")
    window.rowconfigure(0,minsize=400)
    window.columnconfigure(1,minsize=500)
    
    textEdit = tk.Text(window, font="Helvetica 12")
    textEdit.grid(row=0, column=1)

    frame = tk.Frame(window, relief=tk.RAISED, bd=2)
    saveButton = tk.Button(frame, text = "Save", command = lambda: saveFile(window, textEdit))
    openButton = tk.Button(frame, text = "Open", command = lambda: openFile(window, textEdit))

    saveButton.grid(row = 0, column = 0, padx=5, pady=5, sticky="ew")
    openButton.grid(row = 1, column = 0, padx=5, sticky="ew")
    frame.grid(row=0, column=0, sticky="ns")

    window.bind("<Control-s>", lambda x: saveFile(window, textEdit))
    window.bind("<Control-o>", lambda x: openFile(window, textEdit))

    window.mainloop()


def openFile(window, textEdit):
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])

    if not filepath:
        return
    
    textEdit.delete(1.0,tk.END)
    with open(filepath, "r") as f:
        content = f.read()
        textEdit.insert(tk.END, content)
    window.title(f"Open File:{filepath}")


def saveFile(window, textEdit):
    filepath = asksaveasfilename(filetypes=[("Text Files", "*.txt")])

    if not filepath:
        return
    
    with open(filepath, "w") as f:
        content = textEdit.get(1.0,tk.END)
        f.write(content)
    window.title(f"Open File:{filepath}")


main()