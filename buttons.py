from base import Base

class Buttons(Base):
    def __init__(self):
        super().__init__()
        self.play_x_path = ("""//*[@id="movie_player"]/div[24]/div[2]/div[1]/button""")
        self.back_x_path = ("""//*[@id="movie_player"]/div[24]/div[2]/div[1]/a[1]""")
        self.next_x_path = ("""//*[@id="movie_player"]/div[24]/div[2]/div[1]/a[2]""")