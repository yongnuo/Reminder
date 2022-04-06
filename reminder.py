# Import the required libraries
# from tkinter import messagebox, Button, TOP, Tk, PhotoImage, Frame, RAISED, BOTH, LEFT, RIGHT, BOTTOM, X, Y
from tkinter import *
from tkinter import messagebox
import tkinter.font as tkFont
import threading
import tkinter
import yaml
import os
from pystray import MenuItem as item, Icon
from PIL import Image, ImageTk

class Reminder:
   def __init__(self):
      file_path = os.path.realpath(__file__)
      # print(file_path)
      working_directory = os.path.dirname(file_path)
      # messagebox.showinfo("working_directory", working_directory)

      self.settings = self.safe_get_settings(os.path.join(working_directory, "settings.yaml"))
      # print(self.settings)

      
      self.icon_photo = os.path.join(working_directory, "alarm_icon.png")
      self.win=Tk()
      self.win.iconphoto(False, PhotoImage(file=self.icon_photo))
      self.win.title(self.settings["title"])
      self.win["background"] = self.settings["window_background_color"]
      self.exercise_timeout = IntVar()
      self.exercise_timeout.set(self.settings["default_timeout_in_minutes"])
      
      font1 = tkFont.Font(family="Arial", size=16, weight="bold", slant="italic")
      label1 = Label(self.win, text="Time to", bg=self.settings["window_background_color"], foreground="#FFFFFF", font=font1)
      label1.pack(fill=X, expand=False) # , ipadx=20, ipady=20
      font2 = tkFont.Font(family="Arial", size=40, weight="bold", slant="italic")
      label1 = Label(self.win, text="Exercise", bg=self.settings["window_background_color"], foreground="#FFFFFF", font=font2)
      label1.pack(fill=X, expand=False) # ipadx=20, ipady=20


      font_button = tkFont.Font(family="Arial", size=10)

      select_time_frame = Frame(self.win, relief=RAISED, borderwidth=2)
      select_time_frame.pack(fill=BOTH, padx=5)
      fontScaleLabel = tkFont.Font(family="Arial", size=8)
      label_scale_frame = Frame(select_time_frame)
      label_scale_frame.pack(side=RIGHT, fill=Y)
      self.labelScale = Label(label_scale_frame, text=self.exercise_timeout.get(), font=fontScaleLabel, width=3)
      self.labelScale.pack(side=BOTTOM, ipady=2)
      scale = Scale(select_time_frame, orient=HORIZONTAL, resolution=5, from_=self.settings["min_timeout_in_minutes"], to=self.settings["max_timeout_in_minutes"], variable=self.exercise_timeout, command=self.set_scale_value, label="Number of minutes", showvalue=0)
      scale.pack(side=LEFT, fill=X, expand=TRUE)

      until_next_time_button = Button(self.win, text='Until next time', command = lambda: self.start_timer_and_hide(self.exercise_timeout.get() * 60), font=font_button)
      # until_next_time_button = Button(self.win, text='Until next time', command = lambda: messagebox.showinfo("scale", self.exercise_timeout.get()), font=font_button)
      until_next_time_button.pack(fill=BOTH, padx=5, pady=5)



      bottom_frame = Frame(self.win, relief=RAISED, borderwidth=1)
      bottom_frame.pack(side=BOTTOM, fill=X)



      snooze_15_button = Button(bottom_frame, text = 'Snooze 15', command = lambda: self.start_timer_and_hide(900), font=font_button)
      snooze_15_button.pack(side=RIGHT, pady = 5, padx= 5, ipadx=5)
      snooze_10_button = Button(bottom_frame, text = 'Snooze 10', command = lambda: self.start_timer_and_hide(600), font=font_button)
      snooze_10_button.pack(side=RIGHT, ipadx=5)
      snooze_5_button = Button(bottom_frame, text = 'Snooze 5', command = lambda: self.start_timer_and_hide(300), font=font_button)
      snooze_5_button.pack(side=RIGHT, ipadx=5, padx=5)
      
      
      self.timer = None
      self.icon = None
      # self.win.protocol('WM_DELETE_WINDOW', self.minimize_to_tray)

   def safe_get_settings(self, file_name):
      with open(file_name, 'r') as stream:
         try:
            settings=yaml.safe_load(stream)
         except yaml.YAMLError as exc:
            pass
      if "title" not in settings:
         settings["title"] = "Exercise reminder"
      if "default_timeout_in_minutes" not in settings:
         settings["default_timeout_in_minutes"] = 90
      if "min_timeout_in_minutes" not in settings:
         settings["min_timeout_in_minutes"] = 20
      if "max_timeout_in_minutes" not in settings:
         settings["max_timeout_in_minutes"] = 120
      if "window_background_color" not in settings:
         settings["window_background_color"] = "#004080"
         # alarm_icon.png
      return settings


   def set_scale_value(self, val):
      self.exercise_timeout.set(val)
      self.labelScale["text"] = val

   def start(self):
      self.win.mainloop()

   def minimize_to_tray(self):
      self.win.withdraw()
      self.icon = self.create_icon()
      self.icon.run()

   def restore_from_tray(self):
      self.icon.stop()
      self.win.after(0, self.win.deiconify)

   def restore_window(self, icon, item):
      print("Show window")
      self.cancel_timer_if_needed()
      self.restore_from_tray()

   def start_timer_and_hide(self, timeout_in_seconds):
      print("Hide window")
      self.timer = threading.Timer(timeout_in_seconds, lambda: self.restore_window(None, None))
      self.timer.start()
      self.minimize_to_tray()

   def create_icon(self):
      image=Image.open(self.icon_photo)
      menu=(item('Show', self.restore_window), item('-------', None), item('Quit', self.quit))
      return Icon("name", image, self.settings["title"], menu)

   def cancel_timer_if_needed(self):
      if(self.timer):
         print("Cancelling timer")
         self.timer.cancel()
         self.timer = None
      else:
         print("timer does not exist")

   def quit(self, icon, item):
      self.cancel_timer_if_needed()
      self.icon.stop()
      self.win.destroy()


if __name__ == "__main__":
   reminder = Reminder()
   reminder.start()