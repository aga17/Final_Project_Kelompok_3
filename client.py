import pygame
from network import Network
pygame.font.init()

WIDTH = 1228
HEIGHT = 800

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, colour):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.width = 200
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Poppins", 36)
        text = font.render(self.text, 1, (203, 229, 255))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2)
                        - round(text.get_height()/2)))

    def click(self, position):
        x1 = position[0]
        y1 = position[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def re_draw_window(win, game, player):
    win.fill((128, 151, 88))

    if not(game.connected()):
        font = pygame.font.SysFont("Poppins", 36)
        text = font.render("Tunggu yah bro, nungguin ada yang masuk...", 1, (0, 77, 153))
        win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("Poppins", 60)
        text = font.render("KAMU", 1, (41, 41, 41))
        win.blit(text, (WIDTH/4 - text.get_width()/2, 100))

        text = font.render("LAWANMU", 1, (41, 41, 41))
        win.blit(text, (3*WIDTH/4 - text.get_width()/2, 100))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        font = pygame.font.SysFont("Poppins", 40)
        if game.both_went():
            text1 = font.render(move1, 1, (203, 229, 255))
            text2 = font.render(move2, 1, (203, 229, 255))
        else:
            if game.p1_went and player == 0:
                text1 = font.render(move1, 1, (70, 78, 81))
            elif game.p1_went:
                text1 = font.render("Lawanmu dah milih", 1, (70, 78, 81))
            else:
                text1 = font.render("Nunggu ngisi...", 1, (70, 78, 81))

            if game.p2_went and player == 1:
                text2 = font.render(move2, 1, (70, 78, 81))
            elif game.p2_went:
                text2 = font.render("Lawanmu dah milih", 1, (70, 78, 81))
            else:
                text2 = font.render("Nunggu ngisi...", 1, (70, 78, 81))

        if player == 1:
            win.blit(text2, (WIDTH/4 - text2.get_width()/2, 250))
            win.blit(text1, (3*WIDTH/4 - text1.get_width()/2, 250))
        else:
            win.blit(text1, (WIDTH/4 - text1.get_width()/2, 250))
            win.blit(text2, (3*WIDTH/4 - text2.get_width()/2, 250))

        for button in buttons:
            button.draw(win)

    pygame.display.update()

buttons = [Button("Batu", (WIDTH/4)-100, 400, (32, 87, 110)), Button("Gunting", (WIDTH/2)-100, 400, (102, 99, 98)),
           Button("Kertas", (3*WIDTH/4)-100, 400, (154, 108, 49)),Button("Air", (WIDTH/3)-100, 550, (128, 128, 128)),
           Button("Api", (2*WIDTH/3)-100, 550, (59, 68, 75))]


def main():
    run = True
    clock = pygame.time.Clock()
    network = Network()
    player = int(network.get_player())
    print("Kamu player ke: {}".format(player))

    while run:
        clock.tick(60)
        try:
            game = network.send("get")
        except:
            run = False
            print("Could not retrieve game from server - game failed locally")
            break

        if game.both_went():
            re_draw_window(window, game, player)
            try:
                game = network.send("reset")
            except:
                run = False
                print("Could not retrieve game from server")
                break

            font = pygame.font.SysFont("Poppins", 70)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("Ez, Kamu Menang!", 1, (244, 241, 134))
            elif game.winner() == -1:
                text = font.render("Seri Dong!", 1, (211, 211, 211))
            else:
                text = font.render("Noob, Kalah Lu!", 1, (100, 0, 0))

            window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height()*2))
            pygame.display.update()
            pygame.time.delay(1500)
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                position = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(position) and game.connected():
                        if player == 0:
                            if not game.p1_went:
                                network.send(button.text)
                        else:
                            if not game.p2_went:
                                network.send(button.text)

        re_draw_window(window, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        window.fill((144, 199, 255))
        font = pygame.font.SysFont("Poppins", 60)
        text = font.render("Klik Aku Mas!", 1, (0, 5, 10))
        window.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                run = False

    main()


while True:
    menu_screen()
