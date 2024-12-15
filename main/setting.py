import pygame
import source as src
class SettingsUI:
    def __init__(self, window: pygame.Surface):
        self.window = window
        self.settings = {
            'speed': src.speed,
            'viewDistance': src.viewDistance,
            'collisionDistance': src.collisionDistance,
            'sepFactor': src.sepFactor,
            'aliFactor': src.aliFactor,
            'cohFactor': src.cohFactor,
            'foodFactor': src.foodFactor,
            'foodPerSecond': src.foodPerSecond,
            'foodPerClick': src.foodPerClick,
            'birdNum': src.birdNum,
            'foodNum': src.foodNum,
            'groupNum': src.groupNum,
            'enable_shark': False
        }
        self.sliders = self.createBar()
        self.font = pygame.font.Font(None, 32)
        
    def createBar(self):
        sliders = {}
        y = 50
        for key, value in self.settings.items():
            sliders[key] = {
                'rect': pygame.Rect(300, y, 200, 10),
                'btn_rect': pygame.Rect(300 + (value/self.getMax(key))*200, y-5, 20, 20),
                'dragging': False
            }
            y += 40
        return sliders
    
    def getMax(self, key):
        max_values = {
            'speed': 5,
            'viewDistance': 200,
            'collisionDistance': 30,
            'sepFactor': 0.1,
            'aliFactor': 0.2,
            'cohFactor': 0.2,
            'foodFactor': 0.2,
            'foodPerSecond': 30,
            'foodPerClick': 10,
            'birdNum': 200,
            'foodNum': 200,
            'groupNum': 5
        }
        return max_values.get(key, 100)

    def run(self, first = "None")->dict:
        running = True
        while running:
            self.window.fill(src.Colors['background'])
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                    
                if event.type == pygame.MOUSEBUTTONDOWN: 


                    if pygame.Rect(350, 550, 100, 40).collidepoint(event.pos):
                        return self.settings
                        
                    for key, slider in self.sliders.items():
                        if slider['btn_rect'].collidepoint(event.pos):
                            slider['dragging'] = True
                            
                if event.type == pygame.MOUSEBUTTONUP: 
                    for slider in self.sliders.values():
                        slider['dragging'] = False
                        
                if event.type == pygame.MOUSEMOTION:
                    for key, slider in self.sliders.items():
                        if slider['dragging']:
                            slider['btn_rect'].centerx = max(slider['rect'].left, 
                                min(event.pos[0], slider['rect'].right))
                            value = ((slider['btn_rect'].centerx - slider['rect'].left) 
                                / slider['rect'].width * self.getMax(key))

                            # 確保groupNum為1-8的整數
                            if key == 'groupNum':
                                value = max(1, min(8, round(value)))
                            elif key == 'birdNum':
                                value = max(1, min(200, round(value)))
                            elif key == 'foodNum':
                                value = max(1, min(200, round(value)))
                            elif key == 'foodPerSecond':
                                value = max(1, min(30, round(value)))
                            elif key == 'foodPerClick':
                                value = max(1, min(10, round(value)))
                            self.settings[key] = value
                            
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return None
            codeTable = {
                'speed': 'Speed',
                'viewDistance': 'View Distance',
                'collisionDistance': 'Collision Distance',
                'sepFactor': 'Separation Factor',
                'aliFactor': 'Alignment Factor',
                'cohFactor': 'Cohesion Factor',
                'foodFactor': 'Food Factor',
                'birdNum': 'Fish Number',
                'foodNum': 'Food Number',
                'groupNum': 'Group Number',
                'foodPerSecond': 'Food Per Second',
                'foodPerClick': 'Food Per Click',
            }
            # 繪製所有slider和文字
            y = 50
            for key, value in self.settings.items():
                if key != 'enable_shark':
                    if first == "None" and (key == "birdNum" or key == "foodNum" or key == "groupNum"):
                        continue
                    text = self.font.render(f"{codeTable[key]}: {value:.2f}", True, src.Colors['black'])
                    self.window.blit(text, (20, y-10))
                    pygame.draw.rect(self.window, src.Colors['black'], self.sliders[key]['rect'])
                    pygame.draw.rect(self.window, src.Colors['red'], self.sliders[key]['btn_rect'])
                    y += 40
            
            
            # 繪製開始按鈕
            pygame.draw.rect(self.window, src.Colors['green'], (350, 550, 100, 40))
            start_text = self.font.render("Start", True, src.Colors['black'])
            self.window.blit(start_text, (370, 560))
            
            pygame.display.flip()
        return self.settings