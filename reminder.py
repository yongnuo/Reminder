# Import the required libraries
from tkinter import messagebox, Button, TOP, Tk, PhotoImage
import threading
from pystray import MenuItem as item, Icon
from PIL import Image, ImageTk

class Tray:
   def __init__(self):
      # Create an instance of tkinter frame or window
      self.title = "Exercise reminder"
      self.icon_photo = "C:\\OwnProjects\\Reminder\\alarm_icon.png"
      self.win=Tk()
      self.win.iconphoto(False, PhotoImage(file=self.icon_photo))
      self.win.title(self.title)
      # Set the size of the window
      self.win.geometry("700x350")

      button = Button(self.win, text = 'Snooze for 15', command = self.snooze)
      button.pack(side = TOP, pady = 5)
      self.timer = None
      self.icon = None
      self.win.protocol('WM_DELETE_WINDOW', lambda: self.quit(None, None))

   def start(self):
      self.win.mainloop()

   def click_button(self):
      messagebox.showinfo("Hello", "World")
   

   def restore_window(self, icon, item):
      print("Show window")
      self.cancel_timer_if_needed()
      self.icon.stop()
      self.win.after(0, self.win.deiconify)

   def snooze(self):
      print("Hide window")
      self.timer = threading.Timer(15, lambda: self.restore_window(None, None))
      self.timer.start()
      self.win.withdraw()
      self.icon = self.create_icon()
      self.icon.run()

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
      if(self.icon):
         self.icon.stop()
      self.win.destroy()

tray = Tray()
tray.start()




# win.after(1000, snooze)



# win.mainloop()


