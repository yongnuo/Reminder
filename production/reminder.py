# Import the required libraries
# from tkinter import messagebox, Button, TOP, Tk, PhotoImage, Frame, RAISED, BOTH, LEFT, RIGHT, BOTTOM, X, Y
from tkinter import *
import tkinter.font as tkFont
import threading
import tkinter
from pystray import MenuItem as item, Icon
from PIL import Image, ImageTk

class Tray:
   def __init__(self):
      # Create an instance of tkinter frame or window
      self.title = "Exercise reminder"
      self.exercise_timeout = 4500
      self.icon_photo = "C:\\OwnProjects\\Reminder\\alarm_icon.png"
      self.win=Tk()
      self.win.iconphoto(False, PhotoImage(file=self.icon_photo))
      self.win.title(self.title)
      self.win["background"] = "#FF0000"
      # Set the size of the window
      # self.win.geometry("500x250")

      

      # top_frame = Frame(self.win)
      # top_frame.pack(fill=BOTH, expand=True)

      font1 = tkFont.Font(family="Arial", size=16, weight="bold", slant="italic")
      label1 = Label(self.win, text="Time to", bg="#00FF00", foreground="#FFFFFF", font=font1)
      label1.pack(fill=X, expand=False) # , ipadx=20, ipady=20
      font2 = tkFont.Font(family="Arial", size=40, weight="bold", slant="italic")
      label1 = Label(self.win, text="Exercise", bg="#00FF00", foreground="#FFFFFF", font=font2)
      label1.pack(fill=X, expand=False) # ipadx=20, ipady=20

      # middle_frame = top_frame = Frame(self.win)
      # middle_frame.pack(fill=BOTH, expand=True)
      font_button = tkFont.Font(family="Arial", size=10)

      until_next_time_button = Button(self.win, text='Until next time', command = lambda: self.start_timer_and_hide(self.exercise_timeout))
      until_next_time_button.pack(fill=BOTH, padx=5, pady=5)

      bottom_frame = Frame(self.win, relief=RAISED, borderwidth=1)
      bottom_frame.pack(side=BOTTOM, fill=X, expand=True)



      snooze_15_button = Button(bottom_frame, text = 'Snooze 15', command = lambda: self.start_timer_and_hide(900), font=font_button)
      snooze_15_button.pack(side=RIGHT, pady = 5, padx= 5, ipadx=5)
      snooze_10_button = Button(bottom_frame, text = 'Snooze 10', command = lambda: self.start_timer_and_hide(600), font=font_button)
      snooze_10_button.pack(side=RIGHT, ipadx=5)
      snooze_5_button = Button(bottom_frame, text = 'Snooze 5', command = lambda: self.start_timer_and_hide(300), font=font_button)
      snooze_5_button.pack(side=RIGHT, ipadx=5, padx=5)
      
      
      self.timer = None
      self.icon = None
      self.win.protocol('WM_DELETE_WINDOW', self.minimize_to_tray)

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
      return Icon("name", image, self.title, menu)

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

tray = Tray()
tray.start()