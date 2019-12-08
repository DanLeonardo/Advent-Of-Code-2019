import pygame as pg

pixel_size = 25
pixels_width, pixels_height = 25, 6
with open('./message.txt') as file:
    pixels = [int(pixel) for pixel in file.readline().rstrip('\n')]

black = (0, 0, 0)
blue = (0, 25, 255)

screen_width, screen_height = pixels_width * pixel_size, pixels_height * pixel_size
screen = pg.display.set_mode((screen_width, screen_height))

clock = pg.time.Clock()

running = True
while running:
    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill(black)

    # Draw pixels
    for y in range(0, pixels_height):
        for x in range(0, pixels_width):
            if pixels[x+y*pixels_width] == 1:
                pg.draw.rect(screen, blue, (x*pixel_size,y*pixel_size,pixel_size,pixel_size))

    pg.display.flip()
