import sys
import spiel1
import spiel2
import hashlib
import csv
import tkinter as tk



def LOGINMASKE():
    def import_stats():
        user = {}
        with open('scores.csv', 'r') as f:
            text = csv.reader(f)
            for line in text:
                key = line[0]
                values = line[1:4]
                user[key] = values

        return user

    def anmelden(text_entry, start):
        global username, my_font
        username = text_entry.get()
        start.destroy()
        if username in user:
            password = tk.Tk()
            password.geometry("400x200+720+400")
            password.configure(background="gray36")
            password.title("Gruppe 27 Login")
            my_font = ("Purple Smile", 15)
            label = tk.Label(password, padx=70, pady=5, text="Geben Sie Ihr Passwort ein:", font=my_font, width=15,
                             fg="red", bg="#5C5C5C")
            label.pack()

            b_entry = tk.Entry(password, width=20, font=("Purple Smile", 15), show='*', bg="gray62")
            b_entry.pack()

            show_text_button = tk.Button(password, text="OK", width=10, height=1, font=("Purple Smile", 13), bg="red",
                                         command=lambda: user_true(user, username, b_entry, password))
            show_text_button.place(x=136.5, y=100)

            password.mainloop()

        else:

            my_font = ("Purple Smile", 15)
            c = tk.Tk()
            c.geometry("400x200+720+400")
            c.configure(background="gray36")
            c.title("User nicht gefunden")

            label = tk.Label(c, padx=70, pady=5, text="User nicht gefunden!", font=my_font, width=15, fg="red",
                             bg="#5C5C5C")
            label.pack()

            show_text_button = tk.Button(c, text="Wiederholen", width=10, height=1, font=("Purple Smile", 13), bg="red",
                                         command=lambda: begin())
            show_text_button.place(x=136.5, y=70)

            quit_button = tk.Button(c, text="Registrieren", width=10, height=1, font=("Purple Smile", 13), bg="red",
                                    command=lambda: pre_reg(username, c))
            quit_button.place(x=136.5, y=120)

            c.mainloop()

            return username

    def user_true(user, username, b_entry, password):
        clear_pass = b_entry.get()
        password.destroy()
        hash_pass = hashlib.md5(clear_pass.encode())
        hash_pass = hash_pass.hexdigest()
        if hash_pass in user[username]:
            home_menu()
        else:
            password_wrong()

    def pre_reg(username, c):
        c.destroy()
        d = tk.Tk()
        d.geometry("400x200+720+400")
        d.configure(background="gray36")
        d.title("Gruppe 27 Login - Password")

        label = tk.Label(d, padx=80, pady=5, text="Neues Passwort\n und Bestätigen!", font=my_font, width=20, fg="red",
                         bg="#5C5C5C")
        label.pack()

        pw1_entry = tk.Entry(d, width=20, font=("Purple Smile", 15), show='*', bg="gray62")
        pw1_entry.place(x=90, y=70)

        pw2_entry = tk.Entry(d, width=20, font=("Purple Smile", 15), show='*', bg="gray62")
        pw2_entry.place(x=90, y=110)

        show_text_button = tk.Button(d, text="OK", width=10, height=1, font=("Purple Smile", 13), bg="red",
                                     command=lambda: registrieren(username, pw1_entry, pw2_entry, d))
        show_text_button.place(x=140, y=150)

        d.mainloop()

    def password_wrong():
        f = tk.Tk()
        f.geometry("400x200+720+400")
        f.configure(background="gray36")
        f.title("Fehler Passwort")

        label = tk.Label(f, padx=70, pady=5, text="Passwort falsch", font=my_font, width=15, fg="red", bg="#5C5C5C")
        label.pack()

        show_text_button = tk.Button(f, text="Wiederholen", width=10, height=1, font=("Purple Smile", 13), bg="red",
                                     command=begin)
        show_text_button.place(x=140, y=70)

        quit_button = tk.Button(f, text="Beenden", width=10, height=1, font=("Purple Smile", 13), bg="red",
                                command=f.quit)
        quit_button.place(x=140, y=130)

        f.mainloop()

    def registrieren(username, pw1_entry, pw2_entry, d):
        password = pw1_entry.get()
        password2 = pw2_entry.get()
        d.destroy()
        if password == password2:
            new_hash_pass = hashlib.md5(password.encode())
            new_hash_pass = new_hash_pass.hexdigest()
            user.update({username: [new_hash_pass, 0, 0]})
            export_stats(user)
            home_menu()
        else:
            e = tk.Tk()
            e.title("Fehler Passwort")
            e.geometry("400x200+720+400")
            e.configure(background="gray36")

            label = tk.Label(e, padx=70, pady=5, text="Passwörter stimmen \nnicht über ein!", font=my_font, width=15,
                             fg="red", bg="#5C5C5C")
            label.pack()

            show_text_button = tk.Button(e, text="Wiederholen", width=10, height=1, font=("Purple Smile", 13), bg="red",
                                         command=lambda: begin())
            show_text_button.place(x=140, y=85)

            quit_button = tk.Button(e, text="Beenden", width=10, height=1, font=("Purple Smile", 13), bg="red",
                                    command=e.quit)
            quit_button.place(x=140, y=135)

            e.mainloop()

    def home_menu():
        MAIN(username, user)

    def export_stats(user):
        with open('scores.csv', "w", newline="") as f:
            writer = csv.writer(f)
            for key, values in user.items():
                row = [key] + values
                writer.writerow(row)

    def begin():

        start = tk.Tk()
        start.geometry("400x200+720+400")
        start.configure(background="gray36")
        start.title("Gruppe 27 | Login")
        my_font = ("Purple Smile", 15)

        label = tk.Label(start, padx=150, pady=5, text="Geben Sie Ihren Benutzernamen ein:", font=my_font, width=15,
                         fg="red", bg="#5C5C5C")
        label.pack()

        text_entry = tk.Entry(start, width=20, font=("Purple Smile", 15), bg="gray62")
        text_entry.place(x=90, y=50)

        show_text_button = tk.Button(start, text="OK", width=10, height=1, font=("Purple Smile", 13), bg="red",
                                     command=lambda: anmelden(text_entry, start))
        show_text_button.place(x=140, y=95)

        quit_button = tk.Button(start, text="Beenden", width=10, height=1, font=("Purple Smile", 13), bg="red",
                                command=start.quit)
        quit_button.place(x=140, y=145)

        start.mainloop()

    #### Commands
    user = import_stats()
    begin()


def MAIN(username, user):
    import pygame
    pygame.init()
    pygame.mixer.init()

    running = True
    width = 1440
    height = 900

    screen = pygame.display.set_mode((width, height))
    background = pygame.image.load("Menü/Menü_background_.png")
    hover_sound = pygame.mixer.Sound("Menü/Menu Selection Click.wav")

    class Button:
        def __init__(self, x, y, image, image_hover, function):
            self.x = x
            self.y = y
            self.image = image
            self.image_hover = image_hover
            self.function = function
            self.hover = False
            self.sound_played = True

        def draw(self, screen):
            if self.hover:
                screen.blit(self.image_hover, (self.x, self.y))
            else:
                screen.blit(self.image, (self.x, self.y))

        def click(self, pos):
            x1 = pos[0]
            y1 = pos[1]
            x2 = self.x + self.image.get_width()
            y2 = self.y + self.image.get_height()
            if self.x < x1 < x2 and self.y < y1 < y2:
                self.function()

        def hover_check(self, pos):
            x1 = pos[0]
            y1 = pos[1]
            x2 = self.x + self.image.get_width()
            y2 = self.y + self.image.get_height()
            if self.x < x1 < x2 and self.y < y1 < y2:
                self.hover = True
                pygame.mixer.Sound.play(hover_sound)
            else:
                self.hover = False

    def game1():
        spiel1.play(user, username)

    def game2():
        spiel2.play(user, username)

    class DataDisplay:
        pygame.font.init()

        def __init__(self, csv_file, font_file, font_size, color, x, y, row_spacing):
            self.csv_file = csv_file
            self.font = pygame.font.Font(font_file, font_size)
            self.font_user = pygame.font.Font("Purple Smile.ttf", 60)
            self.color = color
            self.x = x
            self.y = y
            self.row_spacing = row_spacing
            self.labels = []
            self.extract_data()

        def extract_data(self):
            label_username = Label(username + ":", self.font_user, (255,130,0), 550, 480)
            self.labels.append(label_username)

            label = Label("Highscore Volcano: " + str(user[username][2]), self.font, self.color, self.x, self.y)
            self.labels.append(label)
            label2 = Label("Highscore Snake: " + str(user[username][1]), self.font, self.color, 550, 650)
            self.labels.append(label2)


        def display(self, screen):
            for label in self.labels:
                label.display(screen)

    class Label:
        def __init__(self, text, font, color, x, y):
            self.text = text
            self.font = font
            self.color = color
            self.x = x
            self.y = y

        def display(self, screen):
            text = self.font.render(self.text, True, self.color)
            text_rect = text.get_rect()
            text_rect.x = self.x
            text_rect.y = self.y
            screen.blit(text, text_rect)

    # Initialisieren Sie den Daten-Display-Objekt
    data_display = DataDisplay("app/scores.csv", "Purple Smile.ttf", 30, (139, 0, 0), 550, 595, 50)

    # global running
    button1_image = pygame.image.load("Menü/Button_Volcano.png")
    button1_image_hover = pygame.image.load("Menü/Button_Volcano_Hover.png")
    button2_image = pygame.image.load("Menü/Button_Snake.png")
    button2_image_hover = pygame.image.load("Menü/Button_Snake_Hover.png")
    button1 = Button(120, 780, button1_image, button1_image_hover, game1)
    button2 = Button(1035, 780, button2_image, button2_image_hover, game2)
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                button1.click(pos)
                button2.click(pos)
        pos = pygame.mouse.get_pos()
        button1.hover_check(pos)
        button2.hover_check(pos)
        screen.blit(background, (0, 0))
        button1.draw(screen)
        button2.draw(screen)
        # Zeichnen Sie die Daten auf dem Bildschirm
        data_display.display(screen)
        pygame.display.update()

    return user, username


if __name__ == "__main__":
    LOGINMASKE()
