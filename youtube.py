from base import Base
from buttons import Buttons

class YouTube(Buttons):
    def __init__(self):
        super().__init__()
        self.base_url = 'https://youtube.com/'
        self.kanye_url = "watch?v=1fpkdSfPzio&list=PLTDmNT4owFz2pivbgvdIIUR3yYTx6LCY0&index=1"
        if self.driver_pkl_file_path.exists():
            self.load_driver_path()
            
    def click_play(self):
        self.find_element(self.play_x_path).click()
        
    def click_back(self):
        self.find_element(self.back_x_path).click()
        
    def click_next(self):
        self.find_element(self.next_x_path)