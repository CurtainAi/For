import random
import sys
import pygame
def gamestart():
    pygame.init()
    #参数设定
    screen=pygame.display.Info()
    WIDTH=screen.current_w
    HEIGHT=screen.current_h
    HSIZE=20
    #创建一个可视窗口
    window=pygame.display.set_mode(
        (WIDTH,HEIGHT),flags=pygame.FULLSCREEN|pygame.NOFRAME
    )#全屏显示，并设置无窗体控制按钮
    #加载字体
    font=pygame.font.SysFont('calibrii.ttf',HSIZE)
    #修改框体
    surface=pygame.Surface((WIDTH,HEIGHT),flags=pygame.SRCALPHA)
    pygame.Surface.convert(surface)
    #填充颜色
    surface.fill(pygame.Color(0,0,0,28))
    window.fill((0,0,0))
    #准备字符
    #数字版
    texts=[font.render(str(i),True,(0,255,0)) for i in range(2)]
    #字母版
    #letter=string.printable  #导入全部字母
    #texts=[font.render(str(letter[i]),True,(0,255,0)) for i in range(len(letter))]  #设置字体颜色
    #按屏幕的宽度计算可以在画板上放几列坐标并生成一个列表
    column=int(WIDTH/HSIZE)
    drops=[0 for i in range(column)]
    while True:
        #获取事件内容
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                #exit()
                pygame.quit()
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    #exit()
                    pygame.quit()
                    sys.exit()
        #以上是键盘事件处理
        #将暂停一段给定的毫秒数
        pygame.time.delay(20)
        #重新绘制图像
        window.blit(surface,(0,0))
        for i in range(len(drops)):
            text=random.choice(texts)
            #再次重绘，按坐标绘制字符
            #window.blit(text,(drops[i]*HSIZE,i*HSIZE))#横向跑码
            window.blit(text,(i*HSIZE,drops[i]*HSIZE))#纵向跑码
            drops[i]+=1
            #超出范围后重置坐标位置
            if drops[i]*10>HEIGHT or random.random()>0.95:
                drops[i]=0
        pygame.display.flip()

if __name__ == "__main__":
    gamestart()