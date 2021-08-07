import pygame
from pygame.locals import *
import time
import random
import sys

SIZE = 40
INITIAL_LENGTH = 1


class Game:
	def __init__(self):
		pygame.init()
		pygame.mixer.init()

		# Create a Screen
		self.surface = pygame.display.set_mode((1000, 800))
		pygame.display.set_caption("Snake Game")

		# Create a Snake Instance
		self.snake = Snake(self.surface, INITIAL_LENGTH)
		self.snake.draw()

		self.time_stamp = 0.02

		# Create an Apple Instance
		self.apple = Apple(self.surface)
		self.apple.draw()

		# Play Background Music
		self.play_background_music()

	def play(self):
		self.render_background_image()

		self.snake.walk()
		self.apple.draw()
		self.display_score()
		pygame.display.flip()

		# Collision of Snake with Apple
		for i in range(self.snake.length):
			if self.collide(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
				self.play_sound("resources/ding.mp3")

				self.snake.increase_length()
				self.apple.move()

		# Snake Colliding with itself
		for i in range(2, self.snake.length):
			if self.collide(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
				self.play_sound("resources/crash.mp3")
				raise Exception("An Error occurred")

		# Collision of snake with window boundaries
		if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
			self.play_sound("resources/crash.mp3")
			raise Exception("Snake hit the Wall")

	@staticmethod
	def collide(x_1, y_1, x_2, y_2):
		if x_1 >= x_2 and x_1 < x_2 + SIZE:
			if y_1 >= y_2 and y_1 < y_2 + SIZE:
				return True
			else:
				return False
		else:
			return False

	def display_score(self):
		font = pygame.font.SysFont('arial', 30)
		score = font.render(f'Score: {self.snake.length - INITIAL_LENGTH}', True, (255, 255, 255))
		l_block = font.render("Level 2", True, (255, 255, 255))
		self.surface.blit(score, (850, 10))
		self.surface.blit(l_block, (650, 10))

	def show_game_over(self):
		self.render_background_image()
		font = pygame.font.SysFont('arial', 30)

		line1 = font.render(f'Game Over! Your Score is: {self.snake.length - INITIAL_LENGTH}', True, (255, 255, 255))
		self.surface.blit(line1, (200, 300))

		line2 = font.render("To play Again, press ENTER. To exit, press ESC", True, (255, 255, 255))
		self.surface.blit(line2, (200, 200))

		pygame.display.flip()

		# Stop the Background Music
		pygame.mixer.music.pause()

	def game_reset(self):
		self.snake = Snake(self.surface, INITIAL_LENGTH)
		self.apple = Apple(self.surface)

	@staticmethod
	def play_sound(sound):
		sound_to_be_played = pygame.mixer.Sound(sound)
		pygame.mixer.Sound.play(sound_to_be_played)

	@staticmethod
	def play_background_music():
		pygame.mixer.music.load("resources/bg_music_1.mp3")
		pygame.mixer.music.play(-1, 0)

	def render_background_image(self):
		background_image = pygame.image.load("resources/background.jpg")
		self.surface.blit(background_image, (0, 0))

	def run(self):
		# Show the window
		pygame.display.flip()

		# Create mainloop
		running = True
		pause = False
		while running:
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False
					pygame.quit()
					pygame.display.quit()
					break
				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						running = False
						pygame.quit()
						pygame.display.quit()
						break
					elif event.key == K_RETURN:
						# Re-run the background Music
						pygame.mixer.music.unpause()

						pause = False
					elif not pause:
						if event.key == K_DOWN:
							self.snake.move_down()
						elif event.key == K_UP:
							self.snake.move_up()
						elif event.key == K_LEFT:
							self.snake.move_left()
						elif event.key == K_RIGHT:
							self.snake.move_right()
			try:
				if not pause:
					self.play()
			except Exception as e:
				self.show_game_over()
				pause = True
				self.game_reset()

			# This is will make the snake walk after every .2 seconds
			time.sleep(self.time_stamp)


class Snake:
	def __init__(self, parent_screen, length):
		self.parent_screen = parent_screen

		# Get The Block Image
		self.block = pygame.image.load("resources/block.jpg").convert()

		# This parameter will check the length of box
		self.length = length
		# Initialize default block properties
		self.x = [SIZE] * length
		self.y = [SIZE] * length

		# Define the default direction in which box moves
		self.direction = "down"

	def draw(self):
		# Change block position
		for i in range(self.length):
			self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
		pygame.display.flip()

	def walk(self):
		for i in range(self.length - 1, 0, -1):
			self.x[i] = self.x[i - 1]
			self.y[i] = self.y[i - 1]

		if self.direction == 'down':
			self.y[0] += SIZE
		elif self.direction == 'up':
			self.y[0] -= SIZE
		elif self.direction == 'left':
			self.x[0] -= SIZE
		else:
			self.x[0] += SIZE
		self.draw()

	def increase_length(self):
		self.length += 2
		self.x.append(-1)
		self.x.append(-1)
		self.y.append(-1)
		self.y.append(-1)

	def move_up(self):
		if self.direction == 'down':
			self.direction = 'down'
		else:
			self.direction = "up"

	def move_down(self):
		if self.direction == 'up':
			self.direction = 'up'
		else:
			self.direction = "down"

	def move_left(self):
		if self.direction == 'right':
			self.direction = 'right'
		else:
			self.direction = "left"

	def move_right(self):
		if self.direction == 'left':
			self.direction = 'left'
		else:
			self.direction = "right"


class Apple:
	def __init__(self, parent_screen):
		self.parent_screen = parent_screen
		self.apple_image = pygame.image.load("resources/apple.jpg").convert()
		self.x = SIZE * 3
		self.y = SIZE * 3

	def draw(self):
		self.parent_screen.blit(self.apple_image, (self.x, self.y))
		pygame.display.flip()

	def move(self):
		self.x = random.randint(1, 23) * SIZE
		self.y = random.randint(1, 19) * SIZE

