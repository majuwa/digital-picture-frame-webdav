from webdav3.client import Client
import pygame
import io
import time
import json
import socket

def load_config(file_path):
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {file_path}: {e}")
        return None


def aspect_scale(img,bx,by):
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pygame.transform.scale(img, (sx,sy))




pygame.init()
screen = pygame.display.set_mode((1024, 600))
pygame.mouse.set_visible(False)


config_file_path = 'config.json'
options = load_config(config_file_path)
font = pygame.font.Font(None, 36)

client = Client(options)

while True:
    content = client.list()


                
    for image in content:
        if not image == "diashow/":

            trial = False
            while trial == False:
                try:
                    res = client.resource(image)
                    trial = True
                except socket.timeout:
                    print("Error")
                    pygame.event.get()
                    screen.fill("black")
                    message = "Error Connection"
                    text_color = (255, 255, 255)  # White text
                    text_surface = font.render(message, True, text_color)
                    text_rect = text_surface.get_rect()
                    text_rect.center = (1024/ 2, 600 / 2)
                    screen.blit(text_surface, text_rect)
                    pygame.display.flip()
                    time.sleep(5)  
            if not res.is_dir():
                pygame.event.get()
                print(image)
                screen.fill("black")
                buffer = io.BytesIO()
                res.write_to(buffer)
                buffer.seek(0)
                ball = pygame.image.load(buffer)
                ball = aspect_scale(ball,1024,600)
                ballrect = ball.get_rect()
                ballrect.center = (512, 300)
                screen.blit(ball, ballrect)


                # RENDER YOUR GAME HERE

                # flip() the display to put your work on screen
                pygame.display.flip()

                time.sleep(10)
                # clock = pygame.time.Clock().tick(400)

# pygame.quit()
                