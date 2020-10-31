# This is the setup file. Run this once before running the Play_Rwecent_Likes file
from youtube import YouTube

d = YouTube()
d.save_driver_path()
d.launch_chrome()
d.open("")
input("Please log in in to your Google account. Press enter when account is logged in.")
d.save_cookies()
print("Setup complete. You can now run play.py.")
d.driver.quit()
