import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """创建得分板的类"""
    def __init__(self, ai_settings, screen, stats):
        """初始化得分板属性"""
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        
        self.text_color = 30, 30, 30
        self.font = pygame.font.SysFont(None, 48)
        
        #准备初始得分和最高得分图像
        self.prep_images()
        
    def prep_images(self):
        """集成得分板显示信息"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        
    def prep_score(self):
        """将得分板图像化"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, 
                self.ai_settings.bg_color)
        #将得分板放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def show_score(self):
        """呈现得分板"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)
        
    def prep_high_score(self):
        """将最高得分图像化"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, 
                self.text_color, self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20
    
    def prep_level(self):
        """将等级渲染成图片"""
        self.level_image = self.font.render(str(self.stats.level), True, 
                self.text_color, self.ai_settings.bg_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.right = self.score_rect.right
        self.level_image_rect.top = self.score_rect.bottom + 10
        
    def prep_ships(self):
        """在屏幕左上角显示剩余飞船数量"""
        self.ships = Group()

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
        
        

        
    
