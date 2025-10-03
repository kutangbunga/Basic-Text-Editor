import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os

currentFilename = None

def main():
    window = tk.Tk()
    window.title("Text Editor")
    window.rowconfigure(1,minsize=400, weight=3)
    window.columnconfigure(0,minsize=500, weight=3)
    
    #Toolbar
    toolbar = tk.Frame(window, relief=tk.RAISED, bd=2)
    toolbar.grid(row=0, column=0, sticky="ew")

    #Text Editor
    textEdit = tk.Text(window, font="Helvetica 12")
    textEdit.grid(row=1, column=0, sticky="nsew")

    #Scrollbar
    scrollBar=tk.Scrollbar(window)
    scrollBar.config(command=textEdit.yview)
    scrollBar.grid(row=1, column=4, sticky="nsew")

    #Menu button
    menuButton = tk.Menubutton(toolbar, text="File", relief=tk.RAISED)
    menu=tk.Menu(menuButton, tearoff=False)
    menu.add_command(label="Open", command=lambda:openFile(window, textEdit))
    menu.add_command(label="Save", command=lambda:saveFile(window, textEdit))
    menu.add_command(label="Save as", command=lambda:saveAsFile(window, textEdit))
    
    menuButton["menu"] = menu
    menuButton.grid(row=0, column=0, pady=5, padx=5, sticky="ns")

    #Key binding
    window.bind("<Control-o>", lambda x: openFile(window, textEdit))
    window.bind("<Control-s>", lambda x: saveFile(window, textEdit))
    window.bind("<Control-Shift-S>", lambda x: saveAsFile(window, textEdit))

    window.mainloop()


def openFile(window, textEdit):
    global currentFilename
    filepath = askopenfilename(filetypes=[("Text Files", "*.txt")])

    if not filepath:
        return
    try:
        textEdit.delete(1.0,tk.END)
        with open(filepath, "r") as f:
            content = f.read()
            textEdit.insert(tk.END, content)
        window.title(f"Open File: {os.path.basename(filepath)}")
        currentFilename = os.path.basename(filepath)
    except Exception as e:
        print(f"Error open file {e}")

def saveAsFile(window, textEdit):
    global currentFilename
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"),("All files","*.*")],
        initialfile="untitled.txt",
        title="Save your file as..."
        )

    if not filepath:
        return
    
    try:
        with open(filepath, "w") as f:              #Takes up the pen
            content = textEdit.get(1.0,tk.END)      #Copy everything from the pencil
            f.write(content)                        #write everything permanently with the pen (Save)

        window.title(f"Saved File: {os.path.basename(filepath)}")
        currentFilename = os.path.basename(filepath)

    except Exception as e:
        print(f"Error saving file {e}")


def saveFile(window, textEdit):
    global currentFilename                      #See whether currentFilename is "None" or not
    if not currentFilename:                     #If not
        saveAsFile(window, textEdit)            #Use the saveAsFile function
    else:
        try:
            with open(currentFilename, "w") as f:
                content= textEdit.get(1.0, tk.END)
                f.write(content)
                window.title(f"Saved file: {currentFilename}")
        except Exception as e:
            print(f"Error saving file {e}")

main()