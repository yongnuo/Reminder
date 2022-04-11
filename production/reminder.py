# Import the required libraries
# from tkinter import messagebox, Button, TOP, Tk, PhotoImage, Frame, RAISED, BOTH, LEFT, RIGHT, BOTTOM, X, Y
from tkinter import *
from sys import exit, argv
from getopt import getopt, GetoptError
from tkinter import messagebox
import tkinter.font as tkFont
import threading
import tkinter
import yaml
import os
from pystray import MenuItem as item, Icon
from PIL import Image, ImageTk

class Reminder:
   def __init__(self, argv):
      settings_file_name = self.parse_command_line_options(argv)
      self.settings = self.safe_get_settings(settings_file_name)
      
      self.win=Tk()
      self.win.iconphoto(False, PhotoImage(file=self.settings["icon_image"]))
      self.win.title(self.settings["window_title"])
      self.win["background"] = self.settings["window_background_color"]
      self.exercise_timeout = IntVar()
      self.exercise_timeout.set(self.settings["default_timeout_in_minutes"])

      button_font = tkFont.Font(family="Arial", size=10)
      pre_title_font = tkFont.Font(family="Arial", size=16, weight="bold", slant="italic")
      title_font = tkFont.Font(family="Arial", size=40, weight="bold", slant="italic")
      slider_label_font = tkFont.Font(family="Arial", size=8)

      pre_title_label = Label(self.win, text=self.settings["pre_title"], bg=self.settings["window_background_color"], foreground=self.settings["title_color"], font=pre_title_font)
      pre_title_label.pack(fill=X, expand=False)
      title_label = Label(self.win, text=self.settings["title"], bg=self.settings["window_background_color"], foreground=self.settings["title_color"], font=title_font)
      title_label.pack(fill=X, expand=False)

      select_time_frame = Frame(self.win, relief=RAISED, borderwidth=2)
      select_time_frame.pack(fill=BOTH, padx=5)
      slider_label_frame = Frame(select_time_frame)
      slider_label_frame.pack(side=RIGHT, fill=Y)
      self.slider_label = Label(slider_label_frame, text=self.exercise_timeout.get(), font=slider_label_font, width=3)
      self.slider_label.pack(side=BOTTOM, ipady=2)
      slider = Scale(select_time_frame, orient=HORIZONTAL, resolution=5, from_=self.settings["min_timeout_in_minutes"], to=self.settings["max_timeout_in_minutes"], variable=self.exercise_timeout, command=self.set_slider_value, label="Number of minutes", showvalue=0)
      slider.pack(side=LEFT, fill=X, expand=TRUE)

      until_next_time_button = Button(self.win, text='Until next time', command = lambda: self.start_timer_and_hide(self.exercise_timeout.get() * 60), font=button_font)
      until_next_time_button.pack(fill=BOTH, padx=5, pady=5)

      bottom_frame = Frame(self.win, relief=RAISED, borderwidth=1)
      bottom_frame.pack(side=BOTTOM, fill=X)
      snooze_15_button = Button(bottom_frame, text = 'Snooze 15', command = lambda: self.start_timer_and_hide(15 * 60), font=button_font)
      snooze_15_button.pack(side=RIGHT, pady = 5, padx= 5, ipadx=5)
      snooze_10_button = Button(bottom_frame, text = 'Snooze 10', command = lambda: self.start_timer_and_hide(10 * 60), font=button_font)
      snooze_10_button.pack(side=RIGHT, ipadx=5)
      snooze_5_button = Button(bottom_frame, text = 'Snooze 5', command = lambda: self.start_timer_and_hide(5 * 60), font=button_font)
      snooze_5_button.pack(side=RIGHT, ipadx=5, padx=5)
      
      
      self.timer = None
      self.icon = None
      # if(self.settings["startup_timeout_in_minutes"] > 0):
      #    self.start_timer_and_hide(self.settings["startup_timeout_in_minutes"] * 60)

      # self.win.protocol('WM_DELETE_WINDOW', self.minimize_to_tray)

   def get_default_settings(self):
      settings = {
         "window_title": "Exercise reminder",
         "title": "Exercise",
         "pre_title": "Time to",
         "startup_timeout_in_minutes": 90,
         "default_timeout_in_minutes": 90,
         "min_timeout_in_minutes": 20,
         "max_timeout_in_minutes": 120,
         "window_background_color": "#004080",
         "title_color": "#FFFFFF",
         "icon_image": "alarm_icon.png"
      }
      return settings

   def safe_get_settings(self, settings_file_name):
      full_settings_file_name = os.path.abspath(settings_file_name)
      print(full_settings_file_name)
      with open(full_settings_file_name, 'r') as stream:
         try:
            settings=yaml.safe_load(stream)
         except yaml.YAMLError as exc:
            print(exc)
      default_settings = self.get_default_settings()
      if "window_title" not in settings:
         settings["window_title"] = default_settings["window_title"]
      if "pre_title" not in settings:
         settings["pre_title"] = default_settings["pre_title"]
      if "title" not in settings:
         settings["title"] = default_settings["title"]
      if "startup_timeout_in_minutes" not in settings:
         settings["startup_timeout_in_minutes"] = default_settings["startup_timeout_in_minutes"]
      if "default_timeout_in_minutes" not in settings:
         settings["default_timeout_in_minutes"] = default_settings["default_timeout_in_minutes"]
      if "min_timeout_in_minutes" not in settings:
         settings["min_timeout_in_minutes"] = default_settings["min_timeout_in_minutes"]
      if "max_timeout_in_minutes" not in settings:
         settings["max_timeout_in_minutes"] = default_settings["max_timeout_in_minutes"]
      if "window_background_color" not in settings:
         settings["window_background_color"] = default_settings["window_background_color"]
      if "title_color" not in settings:
         settings["title_color"] = default_settings["title_color"]
      if "icon_image" in settings:
         settings["icon_image"] = os.path.abspath(settings["icon_image"])
      else:
         settings["icon_image"] = os.path.abspath(default_settings["icon_image"])
      return settings


   def set_slider_value(self, val):
      self.exercise_timeout.set(val)
      self.slider_label["text"] = val

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
      image=Image.open(self.settings["icon_image"])
      menu=(item('Show', self.restore_window), item('-------', None), item('Quit', self.quit))
      return Icon("name", image, self.settings["window_title"], menu)

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

   def parse_command_line_options(self, argv):
      help_caption = "reminder.py -s <settingsfile>"
      settings_file = None
      try:
         opts, args = getopt(argv,"hs:",["settings="])
      except GetoptError:
         print(help_caption)
         exit(2)
      for opt, arg in opts:
         if opt == '-h':
            print(help_caption)
            default_settings = self.get_default_settings()
            default_settings_file_name = os.path.abspath("default_settings.yaml")
            with open(default_settings_file_name, 'w') as stream:
               try:
                  yaml.safe_dump(default_settings, stream)
               except yaml.YAMLError as exc:
                  print(exc)
            exit(0)
         elif opt in ("-s", "--settings"):
            settings_file = arg
      if settings_file == None:
         settings_file = "settings.yaml"
      print("Settings file is \"{0}\"".format(settings_file))
      return settings_file


if __name__ == "__main__":
   reminder = Reminder(argv[1:])
   reminder.start()



