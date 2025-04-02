import tkinter as tk
from tkinter import filedialog, messagebox

# Krijuam main application window
root = tk.Tk()
root.title("Python Notepad")
root.geometry("600x400")

# Krijuam Search bar 
search_frame = tk.Frame(root)
search_frame.pack(fill="x", padx=5, pady=5)

search_label = tk.Label(search_frame, text="Search:")
search_label.pack(side="left", padx=5)

search_entry = tk.Entry(search_frame)
search_entry.pack(side="left", expand=True, fill="x", padx=5)

search_button = tk.Button(search_frame, text="Highlight Search", command=lambda: highlight_text())
search_button.pack(side="left", padx=5)

# Krijuam hapesiren ku shkruhet teksti
text_area = tk.Text(root, wrap="word", font=("Arial", 12))
text_area.pack(expand=True, fill="both")

# Funksioni Highlight per te shenjuar tekstin e kerkuar
def highlight_text():
    text_area.tag_remove("highlight", "1.0", tk.END)  
    search_word = search_entry.get()

    if search_word:
        start_pos = "1.0"
        while True:
            start_pos = text_area.search(search_word, start_pos, stopindex=tk.END, nocase=True)
            if not start_pos:
                break
            end_pos = f"{start_pos}+{len(search_word)}c"
            text_area.tag_add("highlight", start_pos, end_pos)
            start_pos = end_pos  # Move forward

        text_area.tag_config("highlight", background="yellow", foreground="black")

# Funksioni Highlight per te shenjuar tekstin e selektuar
def highlight_selection():
    try:
        selected_text = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)  # Merr tekstin e selektuar
        text_area.tag_add("highlight", tk.SEL_FIRST, tk.SEL_LAST)  # Apliko tag
        text_area.tag_config("highlight", background="yellow", foreground="black")  # Konfigurimet e highlight
    except tk.TclError:
        messagebox.showwarning("Warning", "No text selected! Please select text first.")

# Funksioni per te hapur nje skedar (Open file)
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            text_area.delete(1.0, tk.END)  
            text_area.insert(tk.END, file.read())  

# Funksioni per te ruajtur nje skedar (Save file)
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_area.get(1.0, tk.END))  # Save text to file
        messagebox.showinfo("Saved", "File saved successfully!")

# Funksioni per te dale nga aplikacioni
def exit_app():
    root.quit()

# Krijimi i nje menuje per aplikacioni
menu_bar = tk.Menu(root)

# File Menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit Menu
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=lambda: root.focus_get().event_generate("<<Cut>>"))
edit_menu.add_command(label="Copy", command=lambda: root.focus_get().event_generate("<<Copy>>"))
edit_menu.add_command(label="Paste", command=lambda: root.focus_get().event_generate("<<Paste>>"))
edit_menu.add_separator()
edit_menu.add_command(label="Highlight Selection", command=highlight_selection)  # New highlight option
menu_bar.add_cascade(label="Edit", menu=edit_menu)

root.config(menu=menu_bar)

# Perdor aplikacionin
root.mainloop()

