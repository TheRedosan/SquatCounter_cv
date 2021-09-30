from tkinter import *
from tkinter.ttk import Combobox
import cv2 as ocv
import imutils
from PIL import Image
from PIL import ImageTk
from ttkbootstrap import Style

import vision
from vision import process_frame
import numpy as np

import camloc


def visualizar():
    global cap

    if cap is not None:
        ret, frame = cap.read()

        if ret:
            frame = ocv.cvtColor(ocv.flip(imutils.resize(frame, width=640), 1), ocv.COLOR_BGR2RGB)

            frame = process_frame(frame)

            frame_gui = Image.fromarray(frame)
            frame2show = ImageTk.PhotoImage(image=frame_gui)

            lbl_video.configure(image=frame2show)
            lbl_video.image = frame2show

            lbl_squatcount.configure(text=str(vision.count))

            lbl_video.after(1, visualizar)

        else:
            if cap is not None:
                cap.release()
            lbl_video.image = ""
            cap = None


def init_camera():
    global cap, lbl_video

    if cap is None:
        cap = ocv.VideoCapture(0, ocv.CAP_DSHOW)
        lbl_video.configure(bg="gray")
        visualizar()


def finalizar():
    global cap
    if cap is not None:
        cap.release()
        lbl_video.configure(bg="black", text="No se ha seleccionado una camara válida", padx=50, pady=70)


style = Style(theme='lumen')
root = style.master
cap = None

lbl_video = Label(root, bg="black", text="No se ha seleccionado una camara válida", padx=50, pady=70)
lbl_video.grid(column=0, row=3, columnspan=2, padx=5, pady=10)

lbl_squat = Label(root, text="Sentadillas realizadas", padx=2, pady=2)
lbl_squat.grid(column=0, row=1, padx=5, pady=5)

lbl_squatcount = Label(root, text="0", padx=2, pady=2)
lbl_squatcount.grid(column=0, row=2, padx=5, pady=5)

lbl_combo = Label(root, text="Cámara seleccionada", padx=2, pady=2)
lbl_combo.grid(column=1, row=1, padx=5, pady=5)

selected_camera = StringVar()
list_cameras = Combobox(root, state="readonly", textvariable=selected_camera)
list_cameras.grid(column=1, row=2, padx=5, pady=5)
list_cameras["values"] = camloc.camera_list()

btn_iniciar = Button(root, text="Iniciar", width=45, command=init_camera)
btn_iniciar.grid(column=0, row=0, padx=5, pady=5)

btn_finalizar = Button(root, text="Finalizar", width=45, command=finalizar)
btn_finalizar.grid(column=1, row=0, padx=5, pady=5)

root.mainloop()
