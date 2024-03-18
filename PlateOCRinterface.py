import cv2
import serial.tools.list_ports
from tkinter.ttk import *
from tkinter import *
import tkinter as tk
import serial
import imutils
import pytesseract
from PIL import Image, ImageTk
from datetime import datetime
import string
import threading

translation_table = str.maketrans("", "", string.punctuation)

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
tessdata_dir_config = r'--tessdata-dir "C:\\Program Files\\Tesseract-OCR\\tessdata"'

# Serial Port seçim butonlarını oluştur
serial_ports = serial.tools.list_ports.comports()
port_buttons = []

serial_port = serial.Serial()

root = tk.Tk()
root.state("zoomed")

myfont = ("Helvetica", 16, "bold")

lists = Frame(root, bg="lightgray")
lists.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.15)

lists_lbl = Label(root, text="<=Port Menu", fg="blue", font=("Helvetica", 20, "bold"))
lists_lbl.place(rely=0.017, relx=0.15)



now = datetime.now()
tarih = datetime.strftime(now, '%x')
saat = datetime.strftime(now, '%X')

"""Seri haberleşme bağlan"""


def connect(port):
    global serial_port
    # Daha önceki bir seri bağlantı varsa kapat
    if serial_port is not None:
        serial_port.close()
    try:

        serial_port.port = port
        serial_port.baudrate = 9600
        serial_port.open()
        port_lbl.config(text=f"Port ismi: {port}", fg="green")
        print("baglandi")
    except:
        print("baglanmadi")


"""sol sütun frame butonları yenile fonksyonu"""


def upgrade_list():
    for widg in lists.winfo_children():
        widg.destroy()

    serial_ports = serial.tools.list_ports.comports()

    for port, desc, hwid in sorted(serial_ports):
        b = tk.Button(lists, font=("Helvetica", "15"), text="{} \n{}".format(port, desc),
                      command=lambda port=port: connect(port), height=4)
        b.pack(padx=2, pady=5)
        port_buttons.append(b)


rst_btn = Button(root, text="Port Menu\nYenile", font=myfont, fg="blue", command=upgrade_list)
rst_btn.place(relx=0.2, rely=0.85, relwidth=0.07, relheight=0.07)

port_lbl = Label(root, fg="red", text="Port ismi: None", font=("Helvetica", 20, "bold"))
port_lbl.place(relx=0.15, rely=0.05)

VidLbl = Label(root)
VidLbl.place(relx=0.2, rely=0.1)

"""Listbox oluştur"""
save_box = Listbox(root)
save_box.place(relx=0.7, rely=0.1, relwidth=0.25, relheight=0.5)

"""listbox scrollbar ekle"""
ListScrollbar = Scrollbar(save_box)
ListScrollbar.pack(side="right", fill="y")

"""List box temizleme fonksyon ve buton"""


def clr():
    save_box.delete(0, END)


clr_btn = Button(root, text="Liste\nSil", font=myfont, command=clr)
clr_btn.place(relx=0.7, rely=0.625, relwidth=0.07, relheight=0.07)


def box_print(plate):
    save_box.insert(0, f"Plaka:\n{plate} \n {saat} \n {tarih}")


def thd_box(plaka):
    threading.Thread(target=box_print(plaka)).start()


"""on fonksyon ve buton"""


def on():
    try:
        serial_port.write(b'H')
        # box_print("34 IST 34")
        print("led acik")


    except:
        if serial_port is not None:
            print("Secili port yok")


def on_thd():
    threading.Thread(target=on).start()


led_on = Button(root, text="Kapı Aç", font=myfont, command=on)
led_on.place(relx=0.3, rely=0.85, relwidth=0.07, relheight=0.07)

save_box.config(yscrollcommand=ListScrollbar.set)
ListScrollbar.config(command=save_box.yview)

#cap = cv2.VideoCapture(0)

vid_path = 'C:\\Users\\eren2\\PycharmProjects\\OCR_Plate_SQL\\examples\\pr1.mp4'
cap = cv2.VideoCapture(vid_path)
while True:
    # kamera görüntü oku

    ret, original_image = cap.read()
    # gelen görüntüyü boyutlandır
    original_image = imutils.resize(original_image, width=700)
    # kameradan gelen görüntüyü göster
    # cv2.imshow("Orjinal goruntu", original_image)

    # gelen görüntüyü gri tonlarına çevir
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)
    # gri tonlarında görüntüyü göster
    # cv2.imshow("Gray", gray_image)

    # görüntüde sınırları bul
    edged_image = cv2.Canny(gray_image, 30, 200)
    contours, new = cv2.findContours(edged_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    img1 = original_image.copy()
    cv2.drawContours(img1, contours, -1, (0, 255, 0), 3)
    # cv2.imshow("img1", img1)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]
    # stores the license plate contour
    screenCnt = None

    # kameradan gelen görüntüyü img2 e kopyala
    img2 = original_image.copy()
    # img2 kontur son9orlarını çiz ve göster
    cv2.drawContours(img2, contours, -1, (0, 255, 0), 3)
    # cv2.imshow("img2", img2)

    count = 0
    idx = 7

    for c in contours:
        # approximate the license plate contour
        contour_perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * contour_perimeter, True)

        # Look for contours with 4 corners
        if len(approx) == 4:
            screenCnt = approx

            # find the coordinates of the license plate contour
            x, y, w, h = cv2.boundingRect(c)
            new_img = original_image[y: y + h, x: x + w]

            # stores the new image
            cv2.imwrite('./' + str(idx) + '.png', new_img)
            idx += 1
            break
    try:
        # draws the license plate contour on original image
        #cv2.drawContours(original_image, [screenCnt], -1, (0, 255, 0), 3)
        if screenCnt is not None:
            cv2.drawContours(original_image, [screenCnt], -1, (0, 255, 0), 3)
        # cv2.imshow("detected license plate", original_image)

        # filename of the cropped license plate image
        cropped_License_Plate = './7.png'
        # cv2.imshow("cropped license plate", cv2.imread(cropped_License_Plate))

        # converts the license plate characters to string
        #text = pytesseract.image_to_string(cropped_License_Plate, lang='eng', config='--psm 7')
        text = pytesseract.image_to_string(cropped_License_Plate, lang='eng', config=tessdata_dir_config)
        # print(type(text))
        text = str(text)
        my_string_without_special_chars = text.translate(translation_table)

        if text:
            print("License plate is:", my_string_without_special_chars)

            if "34 IST 34" in my_string_without_special_chars:
                # print(text)
                thd_box("34 IST 34")
                on_thd()

            elif "06 ANK 06" in my_string_without_special_chars:
                print(text)
                thd_box("06 CD 1171")
                on_thd()

    except:
        pass

    # cv2img = original_image
    cv2img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGBA)

    img = Image.fromarray(cv2img)
    imgtk = ImageTk.PhotoImage(image=img)
    VidLbl.imgtk = imgtk
    VidLbl.configure(image=imgtk)

    root.update()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

root.mainloop()
cv2.waitKey(0)
cv2.destroyAllWindows()
