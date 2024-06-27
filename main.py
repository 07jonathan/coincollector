import pygame
import random

# Inisialisasi pygame
pygame.init()

# Ukuran layar
screen_width = 800
screen_height = 600

# Warna
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)

# Mengatur ukuran layar
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Coin Collector')

# Mengatur font untuk teks
font = pygame.font.Font(None, 36)

# Fungsi untuk menampilkan teks di layar
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.centery = y
    surface.blit(textobj, textrect)

# Fungsi untuk menampilkan pesan saat game over
def game_over():
    screen.fill(black)
    draw_text("Game Over!", font, white, screen, screen_width/2, screen_height/2)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    quit()

# Kelas untuk koin
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - 30)
        self.rect.y = random.randint(0, screen_height - 30)

    def update(self):
        pass

# Kelas untuk pemain
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        # Menggerakkan pemain berdasarkan input keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        elif keys[pygame.K_RIGHT]:
            self.speed_x = 5
        else:
            self.speed_x = 0

        if keys[pygame.K_UP]:
            self.speed_y = -5
        elif keys[pygame.K_DOWN]:
            self.speed_y = 5
        else:
            self.speed_y = 0

        # Update posisi pemain
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Batasan agar pemain tetap di dalam layar
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

# Membuat grup untuk koin
all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()

# Membuat koin-koin awal
for i in range(10):
    coin = Coin()
    all_sprites.add(coin)
    coins.add(coin)

# Membuat objek pemain
player = Player()
all_sprites.add(player)

# Memulai permainan
score = 0
running = True
while running:
    # Menangani input dari pemain
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mendapatkan tombol yang ditekan
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    # Mengupdate posisi dan tampilan koin
    all_sprites.update()

    # Deteksi tabrakan antara pemain dan koin
    hits = pygame.sprite.spritecollide(player, coins, True)
    for hit in hits:
        score += 1
        coin = Coin()
        all_sprites.add(coin)
        coins.add(coin)

    # Tampilan latar belakang
    screen.fill(black)

    # Menampilkan semua sprite
    all_sprites.draw(screen)

    # Menampilkan skor
    draw_text(f"Score: {score}", font, white, screen, 100, 50)

    # Update layar
    pygame.display.flip()

    # Mengatur kecepatan frame rate
    pygame.time.Clock().tick(60)

# Game over
game_over()
