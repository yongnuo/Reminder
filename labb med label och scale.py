from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont

win=Tk()
scale_value = IntVar()
scale_value.set(40)

select_time_frame = Frame(win, relief=RAISED, borderwidth=2, background="#0000FF")
select_time_frame.pack(fill=BOTH, padx=5)
fontScaleLabel = tkFont.Font(family="Arial", size=8)
label_scale_frame = Frame(select_time_frame, bg="#FF0000", background="#FF0000")
label_scale_frame.pack(side=RIGHT, fill=Y)

labelScale = Label(label_scale_frame, text=scale_value.get(), font=fontScaleLabel, bg="#FFFF00", background="#FFFF00")
labelScale.pack(side=BOTTOM)
scale = Scale(select_time_frame, orient=HORIZONTAL, resolution=5, from_=20, to=120, variable=scale_value, label="Number of minutes", showvalue=0)
scale.pack(side=LEFT, fill=X, expand=TRUE)

import yaml
with open("settings.yaml", 'r') as stream:
    try:
        settings=yaml.safe_load(stream)
        print(settings)
    except yaml.YAMLError as exc:
        print(exc)


if __name__ == "__main__":
    main()