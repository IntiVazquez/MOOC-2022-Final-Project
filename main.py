import pygame
from random import randint


class Game:
    def __init__(self):
        pygame.init()
        
        self.load_files()
        self.clock = pygame.time.Clock()

        self.window_height = 540
        self.window_width = 960
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.game_font = pygame.font.SysFont("comicsansms", 30)

        self.to_right = False
        self.to_left = False

        self.restart()

        pygame.display.set_caption("Catch the Coin")

        self.new_timer = randint(100,200)
        self.generate_drop()

        self.state = 'start'
        self.main_loop()


    def load_files(self):
        # elements not renamed to avoid causing error if a professor runs the programm with the images using their original names
        self.robot = pygame.image.load("robot.png")
        self.coin = pygame.image.load("coin.png")
        self.monster = pygame.image.load("monster.png")
        self.battery = pygame.image.load("door.png")

        self.tutorial = pygame.image.load("tutorial_background.png")
        self.game = pygame.image.load("game_background.png")
        self.end = pygame.image.load("end_background.png")


    def main_loop(self):
        while True:
            self.check_events()
            if self.state == 'game':
                self.timer += 1
                self.manage_drops()
            self.draw()
            self.clock.tick(60)


    def check_events(self):
        if self.state == 'game':
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.to_right = True
                    if event.key == pygame.K_LEFT:
                        self.to_left = True
        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.to_right = False
                    if event.key == pygame.K_LEFT:
                        self.to_left = False

                if event.type == pygame.QUIT:
                    exit()
            
            self.move_robot()

        elif self.state == 'start':
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 'game'

                if event.type == pygame.QUIT:
                    exit()

        elif self.state == 'info':
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = 'start'
                    self.restart()

                if event.type == pygame.QUIT:
                    exit()


    def move_robot(self):
        if self.to_right and self.robot_x + self.robot.get_width() <= self.window_width:
            self.robot_x += 3

        if self.to_left and self.robot_x > 0:
            self.robot_x -= 3


    def generate_drop(self):
        # there is the possibility that 2 batteries got generated while you have 2 and if you cath both you end with 4 batteries but even if it looks strange in the hud there shouldnt be any problem
        if self.batteries == 3:
            drop_type = randint(1,5)
        else:
            drop_type = randint(1,6)
        if drop_type <= 4:
            self.drops.append([randint(0, self.window_width - self.coin.get_width()), -self.coin.get_height(), 0])
        elif drop_type == 5:
            self.drops.append([randint(0, self.window_width - self.monster.get_width()), -self.monster.get_height(), 1])
        else:
            self.drops.append([randint(0, self.window_width - self.battery.get_width()), -self.battery.get_height(), 2])


    def manage_drops(self):
        interacted = -1
        # im not sure about the speed of the drops or the time between each, this actual settings work decent (in terms of fun im talking about)
        self.new_timer -= 1
        if self.new_timer == 0:
            self.generate_drop()
            self.new_timer = randint(100,250)
        
        if self.speed <= 3:
            self.speed += 1e-4

        # i could make the check a funciton and add it to the part where the drops are draw to make only 1 for loop per tick but i think about it later and for what i see the time is similar
        # i have to use the interacted varaible because if i pop an item inside the for loop it goes out of range
        for i in range(len(self.drops)):
            if self.drops[i][2] == 0:
                self.drops[i][1] += self.speed
                
                if self.drops[i][1] + self.coin.get_height() >= self.window_height:
                    interacted = i
                    self.batteries -= 1

                if self.drops[i][1] + self.coin.get_height() >= self.robot_y:
                    robot_middle = self.robot_x + self.robot.get_width()/2
                    coin_middle = self.drops[i][0] + self.coin.get_width()/2
                    if abs(robot_middle - coin_middle) <= (self.robot.get_width() + self.coin.get_width())/2:
                        self.score += 1
                        interacted = i

            if self.drops[i][2] == 1:
                self.drops[i][1] += self.speed

                if self.drops[i][1] + self.monster.get_height() >= self.window_height:
                    interacted = i

                if self.drops[i][1] + self.monster.get_height() >= self.robot_y:
                    robot_middle = self.robot_x + self.robot.get_width()/2
                    monster_middle = self.drops[i][0] + self.monster.get_width()/2
                    if abs(robot_middle - monster_middle) <= (self.robot.get_width() + self.monster.get_width())/2:
                        self.batteries = 0

            if self.drops[i][2] == 2:
                self.drops[i][1] += self.speed

                if self.drops[i][1] + self.battery.get_height() >= self.window_height:
                    interacted = i

                if self.drops[i][1] + self.battery.get_height() >= self.robot_y:
                    robot_middle = self.robot_x + self.robot.get_width()/2
                    battery_middle = self.drops[i][0] + self.battery.get_width()/2
                    if abs(robot_middle - battery_middle) <= (self.robot.get_width() + self.battery.get_width())/2:
                        self.batteries += 1
                        interacted = i

        if interacted != -1:
            self.drops.pop(interacted)

        if self.batteries <= 0:
            self.state = 'info'
            self.drops.clear()


    def draw(self):
        # draw each thing with functions take so much time so i use the online images for the background and all the words that werent variables like the timer and the score
        self.window.fill((0, 0, 0))
        
        # the location of the varaibles arent perfect but i think they arent terrible either
        if self.state == 'start':
            self.window.blit(self.tutorial, (0, 0))

        elif self.state == 'game':
            self.window.blit(self.game, (0, 0))
            
            self.window.blit(self.robot, (self.robot_x, self.robot_y))

            for i in range(len(self.drops)):
                if self.drops[i][2] == 0:
                    self.window.blit(self.coin, (self.drops[i][0], self.drops[i][1]))
                elif self.drops[i][2] == 1:
                    self.window.blit(self.monster, (self.drops[i][0], self.drops[i][1]))
                elif self.drops[i][2] == 2:
                    self.window.blit(self.battery, (self.drops[i][0], self.drops[i][1]))
                    
            for i in range(self.batteries):
                self.window.blit(self.battery, (830 + i * 41, -8))
            coin_data = self.game_font.render(f"{self.score}", True, (0, 0, 0))
            self.window.blit(coin_data, (60, 20))

        elif self.state == 'info':
            self.window.blit(self.end, (0, 0))

            time_text = self.game_font.render(f"{self.timer//60}", True, (255, 255, 0))
            self.window.blit(time_text, (415, 269))
            score_text = self.game_font.render(f"{self.score}", True, (255, 255, 0))
            self.window.blit(score_text, (424, 347))

        pygame.display.flip()


    def restart(self):
        # this is to set all things to default
        self.robot_x = (self.window_width - self.robot.get_width()) / 2
        self.robot_y = self.window_height - self.robot.get_height()

        self.drops = []
        self.score = 0
        self.batteries = 3
        self.speed = 1
        self.timer = 0


if __name__ == "__main__":
    Game()