class Settings():
    """存储《外星人入侵》的所有设置的类"""
    
    def __init__(self):
        """初始化游戏的设置"""
        #设置屏幕的信息
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        
        #设置每局游戏飞船数量
        self.ship_limit = 3
        
        #子弹设置

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        
        #外星人设置
        self.fleet_drop_speed = 10


        #设置加速参数
        self.speedup_factor = 1.1
        
        #外星人点数的提高速度
        self.alien_scale = 1.5
        
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        """添加随游戏进行难度系数增加的属性"""
        #设置飞船、子弹和外星人移动速度
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_points = 50
        
         #fleet_direction为1表示向右移动，为-1表示向左移动
        self.fleet_direction = 1
        
    def increase_speed(self):
        """进行游戏加速，提高游戏难度,并提高外星人点数"""
        self.ship_speed_factor *= self.speedup_factor
        self.bullet_speed_factor *= self.speedup_factor
        self.alien_speed_factor  *= self.speedup_factor
        self.alien_points = int(self.alien_points * self.alien_scale)

