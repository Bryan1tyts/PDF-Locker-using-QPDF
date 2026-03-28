#!/usr/bin/env python3
"""
DEBUG VERSION - Let's see what's happening
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import shutil
from pathlib import Path

def find_qpdf():
    """Find qpdf"""
    qpdf = shutil.which('qpdf')
    if qpdf:
        return qpdf
    
    for path in ['/usr/bin/qpdf', '/usr/local/bin/qpdf']:
        if Path(path).exists():
            return path
    
    try:
        result = subprocess.run(['whereis', 'qpdf'], 
                              capture_output=True, text=True)
        parts = result.stdout.strip().split()
        for part in parts[1:]:
            if Path(part).exists() and '.gz' not in part:
                return part
    except:
        pass
    
    return None

def browse_file():
    """Select PDF file"""
    filename = filedialog.askopenfilename(
        title="Select PDF to lock",
        filetypes=[("PDF files", "*.pdf")]
    )
    if filename:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)

def lock_pdf():
    """Lock the PDF"""
    qpdf_path = find_qpdf()
    
    if not qpdf_path:
        messagebox.showerror("Error", 
                           "qpdf not found!\n\nInstall: sudo apt install qpdf")
        return
    
    pdf_file = file_entry.get().strip()
    if not pdf_file:
        messagebox.showwarning("Error", "Please select a PDF file!")
        return
    
    password = password_entry.get().strip()
    if not password:
        messagebox.showwarning("Error", "Please enter a password!")
        return
    
    input_path = Path(pdf_file)
    if not input_path.exists():
        messagebox.showerror("Error", f"File not found: {pdf_file}")
        return
    
    output_path = input_path.parent / f"{input_path.stem}-LOCKED.pdf"
    
    # Add counter if file exists
    counter = 1
    while output_path.exists():
        output_path = input_path.parent / f"{input_path.stem}-LOCKED-{counter}.pdf"
        counter += 1
    
    cmd = [
        qpdf_path,
        "--encrypt", "", password, "256",
        "--accessibility=y",
        "--extract=n",
        "--modify=none",
        "--print=none",
        "--", str(input_path), str(output_path)
    ]
    
    try:
        lock_button.config(text="Processing...", state='disabled')
        window.update()
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            messagebox.showinfo("Success!", 
                              f"PDF locked!\n\n"
                              f"Saved: {output_path.name}\n\n"
                              f"Password: {password}\n\n"
                              f"BLOCKS:\n"
                              f"- Editing\n"
                              f"- Copying\n"
                              f"- Printing")
            file_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", f"Failed:\n{result.stderr}")
        
        lock_button.config(text="LOCK PDF", state='normal')
        
    except Exception as e:
        messagebox.showerror("Error", str(e))
        lock_button.config(text="LOCK PDF", state='normal')

# Create window
window = tk.Tk()
window.title("PDF Locker - DEBUG VERSION")

# Make window bigger to ensure button is visible
window.geometry("600x500")
window.configure(bg='lightgray')

print("=== DEBUG INFO ===")
print(f"Window created: {window}")

# Title
title = tk.Label(window, text="PDF Locker (DEBUG)", font=("Arial", 20, "bold"), bg='lightgray')
title.pack(pady=20)
print(f"Title packed: {title}")

# Info
info = tk.Label(window, text="Blocks: Editing, Copying, Printing", 
               font=("Arial", 11), fg="red", bg='lightgray')
info.pack(pady=5)
print(f"Info packed: {info}")

# File selection
file_frame = tk.Frame(window, bg='lightgray')
file_frame.pack(pady=20, padx=20, fill='x')
print(f"File frame packed: {file_frame}")

tk.Label(file_frame, text="Select PDF:", font=("Arial", 11), bg='lightgray').pack(anchor='w')

file_entry = tk.Entry(file_frame, font=("Arial", 10), width=45)
file_entry.pack(side='left', padx=(0, 10), ipady=5)
print(f"File entry packed: {file_entry}")

browse_button = tk.Button(file_frame, text="Browse", command=browse_file,
                         font=("Arial", 10), bg="#3498db", fg="white",
                         padx=15, pady=5)
browse_button.pack(side='left')
print(f"Browse button packed: {browse_button}")

# Password
password_frame = tk.Frame(window, bg='lightgray')
password_frame.pack(pady=20, padx=20, fill='x')
print(f"Password frame packed: {password_frame}")

tk.Label(password_frame, text="Password:", font=("Arial", 11), bg='lightgray').pack(anchor='w')

password_entry = tk.Entry(password_frame, show="*", font=("Arial", 12), width=30)
password_entry.pack(anchor='w', ipady=5)
print(f"Password entry packed: {password_entry}")

# ADD SOME SPACE BEFORE BUTTON
spacer = tk.Label(window, text="", bg='lightgray')
spacer.pack(pady=10)
print(f"Spacer added: {spacer}")

# Lock button - TRY DIFFERENT APPROACH
print("\n!!! CREATING LOCK BUTTON !!!")
lock_button = tk.Button(window, 
                       text="LOCK PDF", 
                       command=lock_pdf,
                       font=("Arial", 16, "bold"), 
                       bg="red", 
                       fg="white",
                       width=20,
                       height=2)
lock_button.pack(pady=20)
print(f"Lock button created: {lock_button}")
print(f"Lock button packed: YES")
print(f"Lock button geometry: {lock_button.winfo_geometry()}")

# Add another label BELOW the button to confirm it's there
below_button = tk.Label(window, text="↑ THE LOCK BUTTON SHOULD BE ABOVE THIS TEXT ↑", 
                       font=("Arial", 10, "bold"), fg="blue", bg='lightgray')
below_button.pack(pady=10)
print(f"Below button label: {below_button}")

# Check qpdf
qpdf = find_qpdf()
if qpdf:
    status = tk.Label(window, text=f"✓ qpdf found: {qpdf}", 
                     font=("Arial", 8), fg="green", bg='lightgray')
else:
    status = tk.Label(window, text="⚠ qpdf not found - Install: sudo apt install qpdf", 
                     font=("Arial", 9), fg="red", bg='lightgray')
status.pack()
print(f"Status packed: {status}")

print("\n=== ALL WIDGETS CREATED ===")
print("If you can't see the red LOCK PDF button, there's something weird with your display!")
print("Check the terminal for any errors when you close the window.\n")

window.mainloop()
