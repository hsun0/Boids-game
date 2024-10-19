import pygame
from color import Colors

def main()->None:
    # 要有這個不然無法使用 pygame 的功能
    pygame.init()

    #設定視窗
    width, height = 800, 600
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Boids Simulation')

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Note: pygame 會將所有的東西畫在緩衝區，然後再透過 flip() 顯示到螢幕上
        # 清除畫面
        window.fill(Colors['black'])

        # 將緩衝區顯示到螢幕上
        pygame.display.flip() 

        # 60 FPS
        clock.tick(60)
    pygame.quit()

if __name__ == '__main__':
    main()