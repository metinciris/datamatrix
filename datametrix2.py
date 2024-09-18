import cv2
from zxingcpp import read_barcodes
import tkinter as tk
from tkinter import simpledialog, messagebox
import pyperclip
import os
import winsound

# Kamera ayarları
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

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
            description = codes_memory[code]
            result_window = tk.Toplevel(root)
            result_window.title(description)
            open_windows[code] = result_window  # Aynı kod için tekrar pencere açılmasını engelleriz

            # Tanım (Boya ismi) büyük fontla gösterilecek
            description_label = tk.Label(result_window, text=description, font=("Helvetica", 24, "bold"))
            description_label.pack()

            # Pozitif/Negatif butonları
            pos_button = tk.Button(result_window, text="Pozitif", command=lambda: [add_result(code, description, "Pozitif"), result_window.destroy()])
            neg_button = tk.Button(result_window, text="Negatif", command=lambda: [add_result(code, description, "Negatif"), result_window.destroy()])
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
                result_window.destroy()
                open_windows.pop(code, None)  # Pencere kapandığında kaydı sil

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

# Kamera döngüsü
def camera_loop():
    ret, frame = cap.read()
    if ret:
        # Hem Data Matrix hem de barkodları çözümle
        decoded_objects = read_barcodes(frame)
        for obj in decoded_objects:
            code = obj.text
            handle_new_code(code)
        cv2.imshow('Data Matrix Tarama', frame)
    root.after(100, camera_loop)

root.after(100, camera_loop)
root.mainloop()

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
