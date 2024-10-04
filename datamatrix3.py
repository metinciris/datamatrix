import serial
import tkinter as tk
from tkinter import simpledialog, messagebox
import pyperclip
import os
import winsound
import threading

# Tanım dosyasının yolu
memory_file = "codes_memory.txt"

# Eğer dosya mevcutsa kod ve tanımları yükle, değilse boş bir dictionary başlat
codes_memory = {}
if os.path.exists(memory_file):
    with open(memory_file, 'r') as f:
        for line in f:
            code, description = line.strip().split(': ', 1)
            codes_memory[code] = description

# Sonuçları saklamak için liste
results = []
open_windows = {}  # Aynı kod için üst üste pencere açılmasını engellemek için

# Tkinter arayüzü
root = tk.Tk()
root.title("Data Matrix Kodu Girişi ve Sonuçlar")
root.geometry("600x400")

# Sonuçları clipboard'a kopyalama fonksiyonu
def update_clipboard():
    clipboard_text = "\n".join([f"{desc}: {result}" for desc, result in results])
    pyperclip.copy(clipboard_text)
    messagebox.showinfo("Kopyalama Başarılı", "Sonuçlar kopyalandı ve clipboard'a eklendi.")

# Sonuç ekleme fonksiyonu
def add_result(code, description, result):
    results.append((description, result))
    result_display.insert(tk.END, f"{description}: {result}\n")

# Hasta yenileme fonksiyonu
def reset_patient():
    global results
    results = []
    result_display.delete(1.0, tk.END)

# Kod taraması fonksiyonu
def handle_new_code(code):
    if code not in open_windows:
        winsound.Beep(1000, 200)  # Bip sesi çıkart

        if code not in codes_memory:
            description = simpledialog.askstring("Yeni Kod", f"Yeni kod bulundu: {code}. Lütfen tanım girin:")
            if description:
                codes_memory[code] = description
                with open(memory_file, 'a') as f:
                    f.write(f"{code}: {description}\n")
            else:
                return  # Eğer tanım girilmezse işlemi iptal et
        else:
            description = codes_memory[code]

        result_window = tk.Toplevel(root)
        result_window.title(description)
        open_windows[code] = result_window  # Aynı kod için tekrar pencere açılmasını engelleriz

        # Tanım (Boya ismi) büyük fontla gösterilecek
        description_label = tk.Label(result_window, text=description, font=("Helvetica", 24, "bold"))
        description_label.pack()

        # Pencereyi kapatma fonksiyonu
        def close_window(code):
            if code in open_windows:
                open_windows[code].destroy()
                open_windows.pop(code, None)

        # Pozitif/Negatif butonları
        pos_button = tk.Button(result_window, text="Pozitif", command=lambda: [add_result(code, description, "Pozitif"), close_window(code)])
        neg_button = tk.Button(result_window, text="Negatif", command=lambda: [add_result(code, description, "Negatif"), close_window(code)])
        pos_button.config(bg="light green")
        neg_button.config(bg="light coral")
        pos_button.pack()
        neg_button.pack()

        # Ekstra boya sonucu girişi
        input_entry = tk.Entry(result_window, font=("Helvetica", 20))
        input_entry.pack()

        # Sonucu gönder butonu
        def submit_result():
            boya_result = input_entry.get()
            if boya_result:
                add_result(code, description, boya_result)
            close_window(code)

        submit_button = tk.Button(result_window, text="Sonuç Gir", command=submit_result, bg="light blue")
        submit_button.pack()

# GUI elemanları
result_display = tk.Text(root, height=15, width=70)
result_display.pack()

# Kopyala ve Hasta Yenile butonları
copy_button = tk.Button(root, text="Kopyala", command=update_clipboard, bg="yellow")
copy_button.pack(side=tk.LEFT, padx=10, pady=10)

reset_button = tk.Button(root, text="Hasta Yenile", command=reset_patient, bg="orange")
reset_button.pack(side=tk.LEFT, padx=10, pady=10)

# Seri port ayarları
ser = serial.Serial('COM4', 9600, timeout=1)

# Seri port okuma döngüsü
def serial_read_loop():
    while True:
        code = ser.readline().decode('utf-8').strip()
        if code:
            root.after(0, handle_new_code, code)

# Seri port okuma işlemini ayrı bir iş parçacığında başlat
serial_thread = threading.Thread(target=serial_read_loop, daemon=True)
serial_thread.start()

# Uygulama kapatıldığında seri portu kapatma fonksiyonu
def on_closing():
    ser.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
