import pygame
import sys
import random  # Importer la bibliothèque random

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre de jeu
SCREEN_WIDTH, SCREEN_HEIGHT = 1300, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario mais pas trop")

# Couleurs
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Charger l'image de l'arrière-plan
background = pygame.image.load('Assets/bg.jpg') 
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cadence
clock = pygame.time.Clock()
FPS = 60

# Classe Joueur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Assets/player.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))  
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 100)
        self.velocity_y = 0
        self.jumping = False
        self.level_complete = False

        # Hauteur maximale de saut
        self.jump_height = 15

        # Définir une hitbox personnalisée (plus petite que l'image)
        self.hitbox = pygame.Rect(self.rect.x + 10, self.rect.y + 10, 60, 70)

    def update(self):
        keys = pygame.key.get_pressed()

        # Mise à jour de la position de la hitbox par rapport à la position du joueur
        self.hitbox.topleft = (self.rect.x + 10, self.rect.y + 10)

        # Mouvement gauche et droite
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Saut
        if keys[pygame.K_SPACE] and not self.jumping:
            self.velocity_y = -self.jump_height
            self.jumping = True

        # Appliquer la gravité
        self.velocity_y += 1
        if self.velocity_y > 10:
            self.velocity_y = 10
        self.rect.y += self.velocity_y

        # Empêcher le joueur de sortir de l'écran
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Vérifier si le joueur atteint la fin du niveau (droite de l'écran)
        if self.rect.right >= SCREEN_WIDTH - 10:
            self.level_complete = True

# Classe Ennemi
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Assets/mummy.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 80))  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.speed = 2

        # Définir une hitbox personnalisée (plus petite que l'image)
        self.hitbox = pygame.Rect(self.rect.x + 10, self.rect.y + 10, 60, 60)

    def update(self):
        # Mise à jour de la position de la hitbox par rapport à la position de l'ennemi
        self.hitbox.topleft = (self.rect.x + 10, self.rect.y + 10)

        self.rect.x += self.direction * self.speed
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1  # Change de direction

# Classe Plateforme
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, visible=True):
        super().__init__()
        self.image = pygame.Surface((width, height))
        if visible:
            self.image.fill(WHITE)  # Remplir de blanc si visible
        else:
            self.image.set_alpha(0)  # Rendre invisible
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Classe Niveau
class Level:
    def __init__(self, platforms):
        self.platforms = platforms

    def create_level(self, all_sprites, platforms_group, enemies_group):
        # Ajoute un sol invisible
        invisible_floor = Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20, visible=False)
        all_sprites.add(invisible_floor)
        platforms_group.add(invisible_floor)

        # Ajoute un maximum de 3 plateformes à une hauteur maximale de saut du joueur
        num_platforms = random.randint(3, 3)  # Nombre aléatoire de plateformes 3
        max_platform_height = SCREEN_HEIGHT - 150 - player.jump_height  # Hauteur maximale au-dessus du sol

        for _ in range(num_platforms):
            width = random.randint(100, 200)
            height = 20

            # Positionner les plateformes à la hauteur maximale de saut du joueur
            y = random.randint(max_platform_height - height, max_platform_height)

            x = random.randint(0, SCREEN_WIDTH - width)

            # Créer la plateforme et ajouter au groupe
            platform = Platform(x, y, width, height)
            all_sprites.add(platform)
            platforms_group.add(platform)

        # Générer un nombre aléatoire d'ennemis entre 2 et 6
        num_enemies = random.randint(2, 6)
        for _ in range(num_enemies):
            while True:
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = random.randint(100, SCREEN_HEIGHT - 200)  # Pour éviter que les ennemis apparaissent trop bas
                enemy = Enemy(x, y)
                # Vérifie que les ennemis n'apparaissent pas sur les plateformes
                if not pygame.sprite.spritecollide(enemy, platforms_group, False):
                    all_sprites.add(enemy)
                    enemies_group.add(enemy)
                    break

# Fonctions d'écrans de Game Over et de Victoire
def game_over_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Attendre 2 secondes

def win_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Vous avez gagné !", True, GREEN)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # Attendre 2 secondes

# Relancer le jeu
def restart_game(current_level_index):
    player.rect.center = (100, SCREEN_HEIGHT - 100)
    player.level_complete = False

    all_sprites.empty()
    platforms.empty()
    enemies.empty()

    all_sprites.add(player)
    levels[current_level_index].create_level(all_sprites, platforms, enemies)

# Création de plusieurs niveaux
levels = [
    Level(platforms=[]),  # Premier niveau vide au départ
    Level(platforms=[])   # Deuxième niveau vide au départ
]

# Variables globales du jeu
current_level_index = 0
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Création du joueur
player = Player()
all_sprites.add(player)

# Charger le premier niveau
levels[current_level_index].create_level(all_sprites, platforms, enemies)

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Détection des collisions du joueur avec les plateformes
    hits = pygame.sprite.spritecollide(player, platforms, False)
    if hits:
        if player.velocity_y > 0:
            player.rect.bottom = hits[0].rect.top
            player.velocity_y = 0
            player.jumping = False

    # Détection des collisions avec les ennemis
    if any(player.hitbox.colliderect(enemy.hitbox) for enemy in enemies):
        game_over_screen()  
        restart_game(0)  # Relancer le jeu depuis le niveau 1
        current_level_index = 0  # Réinitialiser l'index du niveau

    if player.level_complete:
        current_level_index += 1
        if current_level_index >= len(levels):
            win_screen()  
            restart_game(0)  # Relancer le jeu depuis le niveau 1
            current_level_index = 0  # Réinitialiser l'index du niveau
        else:
            restart_game(current_level_index)

    screen.blit(background, (0, 0))

    all_sprites.draw(screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
