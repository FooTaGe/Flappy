
import pygame
import MainWindow


def main():
    pygame.init()
    
    mainWindow = MainWindow.MainWindow() 
    mainWindow.MainLoop()
    
    pygame.quit()
    

if __name__ == '__main__':
    main()
