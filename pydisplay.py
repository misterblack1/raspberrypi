# Display stats for framebuffer1 LCD
# Nov 22 2014
# Updated: Jan 18 2016
# Adding living room temp and humidity

import pygame, sys, os, time, datetime, urllib, csv
from pygame.locals import *
os.environ["SDL_FBDEV"] = "/dev/fb1"

## Globals

values = "NULL"
labels = "NULL"
timetopoll = True

pygame.init()

## Set up the screen

DISPLAYSURF = pygame.display.set_mode((320, 240), 0, 16)
pygame.mouse.set_visible(0)
pygame.display.set_caption('Stats')

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
CYAN  = (  0, 255, 255)

## Main loop

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    currentime = datetime.datetime.time(datetime.datetime.now())


## Poll temperature date from splunk as CSV and parse it

    if timetopoll:
      try:
       tempdata = urllib.urlopen("http://10.0.0.14:3344/info/pitemp.cgi")
       if tempdata.getcode() <= 299:
         reader = csv.reader(tempdata, delimiter=',', quotechar='"')
         labels = reader.next()
         values = reader.next()
         timetopoll = False
         try:
           test = values[0]
           test = values[1]
           test = values[2]
           test = values[3]
           test = values[4]
	   test = values[5]
           test = values[6]
         except:
           values = "--.-", "--.-", "--.-", "--.-", "--.-", "--.-", "--.-"
       else:
         values = "--.-", "--.-", "--.-", "--.-", "--.-", "--.-", "--.-"
         timetopoll = False
      except:
       values = "--.-", "--.-", "--.-", "--.-", "--.-", "--.-", "--.-"
       timetopoll = False

# Relies on lighthttpd on Richmond to poll Splunk for this data

    else:
      #print "Not polling"
      timetopoll = True


## Draw the title

    ##graph = pygame.image.load("/root/lcd/background.png")
    #graphrect = graph.get_rect()
    #DISPLAYSURF.blit(graph, graphrect)

    black_square_that_is_the_size_of_the_screen = pygame.Surface(DISPLAYSURF.get_size())
    black_square_that_is_the_size_of_the_screen.fill((0, 0, 0))
    DISPLAYSURF.blit(black_square_that_is_the_size_of_the_screen, (0, 0))

    font = pygame.font.Font(None, 40)
    text = font.render("Outside", 1, RED)
    textpos = text.get_rect(centerx=DISPLAYSURF.get_width()/4+13)
    DISPLAYSURF.blit(text, textpos)

    font = pygame.font.Font(None, 40)
    text = font.render("Inside", 1, RED)
    textpos = text.get_rect(centerx=DISPLAYSURF.get_width()/4+179)
    DISPLAYSURF.blit(text, textpos)



## Draw temperatures

    font = pygame.font.Font(None, 98)
    text = font.render(values[4], 1, WHITE)
##    text = font.render("188.8", 1, WHITE)
    textpos = text.get_rect(center=(DISPLAYSURF.get_width()/4+10,80))
    DISPLAYSURF.blit(text, textpos)

    font = pygame.font.Font(None, 20)
    textF = font.render(u'\u00b0' + "F", 1, WHITE)
    textposF = textpos[0] + textpos[2], textpos[1] + 10    
    DISPLAYSURF.blit(textF, textposF)

## Draw Lines

    pygame.draw.line(DISPLAYSURF, GREEN, [5, 140], [DISPLAYSURF.get_width()-5,140], 1)

    pygame.draw.line(DISPLAYSURF, GREEN, [DISPLAYSURF.get_width()/2+30, 5], [DISPLAYSURF.get_width()/2+30,140], 1)


## Living room Temp

    font = pygame.font.Font(None, 75)
    text = font.render(values[6], 1, WHITE)
    textpos = text.get_rect(topright=(DISPLAYSURF.get_width()/4+220,30))
    DISPLAYSURF.blit(text, textpos)

    font = pygame.font.Font(None, 20)
    textF = font.render(u'\u00b0' + "F", 1, WHITE)
    textposF = textpos[0] + textpos[2], textpos[1] + 10
    DISPLAYSURF.blit(textF, textposF)


## Living room humidity

    font = pygame.font.Font(None, 75)
    text = font.render(values[5], 1, WHITE)
    textpos = text.get_rect(topright=(DISPLAYSURF.get_width()/4+220,80))
    DISPLAYSURF.blit(text, textpos)

    font = pygame.font.Font(None, 20)
    textF = font.render(" %", 1, WHITE)
    textposF = textpos[0] + textpos[2], textpos[1] + 10
    DISPLAYSURF.blit(textF, textposF)


## Min

    font = pygame.font.Font(None, 30)
    text = font.render("Min:", 1, WHITE)
    textpos = text.get_rect(topright=(DISPLAYSURF.get_width()/2-90,145))
    DISPLAYSURF.blit(text, textpos)

    font = pygame.font.Font(None, 30)
    textF = font.render(values[2], 1, WHITE)
##  textF = font.render("981.8", 1, WHITE)
    textposF = textpos[0] + textpos[2] + 10, textpos[1]
    DISPLAYSURF.blit(textF, textposF)


## Max

    font = pygame.font.Font(None, 30)
    text = font.render("Max:", 1, WHITE)
##    textpos = text.get_rect(topright=(DISPLAYSURF.get_width()/2+90,145))
    textpos = text.get_rect(topright=(DISPLAYSURF.get_width()/2-90,165))
    DISPLAYSURF.blit(text, textpos)

    font = pygame.font.Font(None, 30)
    textF = font.render(values[3], 1, WHITE)
##  textF = font.render("1.8", 1, WHITE)
    textposF = textpos[0] + textpos[2] + 10, textpos[1]
    DISPLAYSURF.blit(textF, textposF)



## Attic

    font = pygame.font.Font(None, 30)
    text = font.render("Attic:", 1, WHITE)
##    textpos = text.get_rect(topright=(DISPLAYSURF.get_width()/2-90,165))
    textpos = text.get_rect(topright=(DISPLAYSURF.get_width()/2+90,145))
    DISPLAYSURF.blit(text, textpos)

    font = pygame.font.Font(None, 30)
    textF = font.render(values[0], 1, WHITE)
##  textF = font.render("1.8", 1, WHITE)
    textposF = textpos[0] + textpos[2] + 10, textpos[1]
    DISPLAYSURF.blit(textF, textposF)

## Garage

    font = pygame.font.Font(None, 30)
    text = font.render("Garage:", 1, WHITE)
    textpos = text.get_rect(topright=(DISPLAYSURF.get_width()/2+90,165))
    DISPLAYSURF.blit(text, textpos)

    font = pygame.font.Font(None, 30)
    textF = font.render(values[1], 1, WHITE)
    textposF = textpos[0] + textpos[2] + 10, textpos[1]
    DISPLAYSURF.blit(textF, textposF)

## Draw time

    font = pygame.font.Font(None, 75)
    text = font.render(currentime.strftime("%I:%M %p"), 1, CYAN)
    textpos = text.get_rect(center=(DISPLAYSURF.get_width()/2,215))
    DISPLAYSURF.blit(text, textpos)


## Update the LCD

    pygame.display.update()    


## Sleep time!

    time.sleep(60) 
