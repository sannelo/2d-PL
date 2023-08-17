import pygame
from src.game import Game

WIDTH = 500
HEIGHT = 500

FPS = 60

engine = Game((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.SRCALPHA)

engine.start()