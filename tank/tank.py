import pgzrun,random

WIDTH=1067
HEIGHT=800
SIZE_TANK = 25
walls =[]
bullets=[]
buffs=[]
bullets_holdoff=0
enemies_holdoff=0
enemy_move_count=0
tank_life=1
boss_life=20
score=0
enemy_bullets=[]
boss_bullets=[]
visible=False
game_over=False
enemies=[]


background=Actor('grass')
for x in range(21):
    for y in range(14):
        if random.randint(0,10)<6:
            if random.randint(0,40)==5 and len(buffs)<=3:
                buff=Actor('shield')
                buff.x=x*50+SIZE_TANK
                buff.y=y*50+50+SIZE_TANK
                buffs.append((buff))
            wall=Actor('wall')
            wall.x=x*50+SIZE_TANK
            wall.y=y*50+50+SIZE_TANK
            walls.append(wall)            

sounds.gamestart.play()

tank=Actor('tank_blue')
tank.pos=(WIDTH/2,HEIGHT-SIZE_TANK)
tank.angle=90


for i in range(10):
    enemy=Actor('tank_red')
    enemy.x =i*100+100
    enemy.y = SIZE_TANK
    enemy.angle=270
    enemies.append(enemy)


boss=Actor('tank_dark')
boss.x = 2*WIDTH
boss.y = 2*HEIGHT
boss.angle=270

def tank_set():
    global tank_life
    original_x=tank.x
    original_y=tank.y
    if keyboard.left:
        tank.x-=2
        tank.angle=180
    elif keyboard.right:
        tank.x+=2
        tank.angle=0
    elif keyboard.up:
        tank.y-=2
        tank.angle=90
    elif keyboard.down:
        tank.y+=2
        tank.angle=270
    
    if tank.collidelist(walls)!=-1:
        tank.x=original_x
        tank.y=original_y

    if tank.x < SIZE_TANK or tank.x >WIDTH-SIZE_TANK or tank.y <SIZE_TANK or tank.y > HEIGHT-SIZE_TANK:
        tank.x=original_x
        tank.y=original_y
    index_buff=tank.collidelist(buffs)
    if index_buff!=-1:
        sounds.bonus.play()
        tank_life+=1
        del buffs[index_buff]
def tank_bullets_set():
    
    global boss_life, score
    global bullets_holdoff
    if bullets_holdoff==0:
        if keyboard.space:
            sounds.gun10.play()
            bullet=Actor('bulletblue2')
            bullet.angle= tank.angle
            if bullet.angle==0:
                bullet.pos=(tank.x+SIZE_TANK,tank.y)
            if bullet.angle==180:
                bullet.pos=(tank.x-SIZE_TANK,tank.y)
            if bullet.angle==90: 
                bullet.pos=(tank.x,tank.y-SIZE_TANK)
            if bullet.angle==270:
                bullet.pos=(tank.x,tank.y+SIZE_TANK)
            bullets.append(bullet)
            bullets_holdoff=20
    else:
        bullets_holdoff-=1
    for bullet in bullets:
        if bullet.angle==0:
            bullet.x+=5
        if bullet.angle==180:
            bullet.x-=5
        if bullet.angle==90: 
            bullet.y-=5
        if bullet.angle==270:
            bullet.y+=5

    for bullet in bullets:
        walls_index=bullet.collidelist(walls)
        if walls_index!=-1:
            sounds.gun9.play()
            del walls[walls_index]
            bullets.remove(bullet)
        if bullet.x<0 or bullet.x >WIDTH or bullet.y<0 or bullet.y>HEIGHT:
            bullets.remove(bullet)
        bullet_index=bullet.collidelist(enemies)
        if bullet_index!=-1:
            sounds.exp.play()
            bullets.remove(bullet)
            del enemies[bullet_index]
            if tank_life > 0:
                score+=100
        if bullet.colliderect(boss):
            sounds.exp.play()
            bullets.remove(bullet)
            boss_life-=1
            if boss_life <= 0:
                score+=500           
            
def enemy_set():
    
    global enemy_move_count
    global enemies_holdoff
    for enemy in enemies:
        original_x=enemy.x
        original_y=enemy.y
        choice=random.randint(0,8)
        if enemy_move_count >0:
            enemy_move_count-=1
            if enemy.angle==0:
                enemy.x+=2
            elif enemy.angle==180:
                enemy.x-=2
            elif enemy.angle ==90:
                enemy.y-=2
            elif enemy.angle ==270:
                enemy.y+=2
            if enemy.x<SIZE_TANK or enemy.x>WIDTH-SIZE_TANK or enemy.y<SIZE_TANK or enemy.y > HEIGHT-SIZE_TANK:
                enemy.x=original_x
                enemy.y=original_y
                enemy_move_count=0
            if enemy.collidelist(walls) !=-1:
                enemy.x=original_x
                enemy.y=original_y
                enemy_move_count=0
        
        elif choice<=1:
            enemy.angle=random.randint(0,3)*90
        elif choice>=3:
            if enemies_holdoff==0:
                bullet=Actor('bulletred2')
                bullet.angle=enemy.angle
                bullet.pos=enemy.pos
                enemy_bullets.append(bullet)
                enemies_holdoff=20
            else:
                enemies_holdoff-=1
        else:
            enemy_move_count=30


def enemy_bullets_set():
    global game_over,enemies, tank_life

    for bullet in enemy_bullets:
        if bullet.angle==0:
            bullet.x+=5
        if bullet.angle==180:
            bullet.x-=5
        if bullet.angle==90:
            bullet.y-=5
        if bullet.angle==270:
            bullet.y+=5
    for bullet in enemy_bullets:
        walls_index=bullet.collidelist(walls)
        if walls_index!=-1:
            sounds.gun9.play()
            del walls[walls_index]
            enemy_bullets.remove(bullet)
        if bullet.x<0 or bullet.x >WIDTH or bullet.y<0 or bullet.y>HEIGHT:
            enemy_bullets.remove(bullet)
        if bullet.colliderect(tank):
            sounds.exp.play()
            tank_life-=1
            enemy_bullets.remove(bullet)
def boss_set():
    
    global enemy_move_count
    global enemies_holdoff
    
    original_x=boss.x
    original_y=boss.y
    choice=random.randint(0,2)
    if enemy_move_count >0:
        enemy_move_count-=1
        if boss.angle==0:
            boss.x+=4
        elif boss.angle==180:
            boss.x-=4
        elif boss.angle ==90:
            boss.y-=4
        elif boss.angle ==270:
            boss.y+=4
        if boss.x<SIZE_TANK or boss.x>WIDTH-SIZE_TANK or boss.y<SIZE_TANK or boss.y > HEIGHT-SIZE_TANK:
            boss.x=original_x
            boss.y=original_y
            enemy_move_count=0
        if boss.collidelist(walls) !=-1:
            boss.x=original_x
            boss.y=original_y
            enemy_move_count=0
    if choice==0:
        enemy_move_count=30
    elif choice==1:
        boss.angle=random.randint(0,3)*90
    else:
        if enemies_holdoff==0:
            bullet=Actor('bulletdark2')
            bullet.angle=boss.angle
            bullet.pos=boss.pos
            boss_bullets.append(bullet)
            enemies_holdoff=20
        else:
            enemies_holdoff-=1


def boss_bullets_set():
    global game_over,boss_life, tank_life

    for bullet in boss_bullets:
        if bullet.angle==0:
            bullet.x+=5
        if bullet.angle==180:
            bullet.x-=5
        if bullet.angle==90:
            bullet.y-=5
        if bullet.angle==270:
            bullet.y+=5
    for bullet in boss_bullets:
        walls_index=bullet.collidelist(walls)
        if walls_index!=-1:
            sounds.gun9.play()
            del walls[walls_index]
            boss_bullets.remove(bullet)
        if bullet.x<0 or bullet.x >WIDTH or bullet.y<0 or bullet.y>HEIGHT:
            boss_bullets.remove(bullet)
        if bullet.colliderect(tank):
            sounds.exp.play()
            tank_life-=1
            boss_bullets.remove(bullet)       
def update():
    global visible, boss
    if tank_life > 0 and boss_life > 0: 
        tank_set()
        tank_bullets_set()
        enemy_set()
        enemy_bullets_set()
        if len(enemies) == 0:
            if visible==False:
                visible=True
                boss.x=500
                boss.y=SIZE_TANK
                sounds.intro.play()
            boss_set()
            boss_bullets_set()
def draw():
    global game_over
    if tank_life<=0 and boss_life!=0:
        screen.fill((0,0,0))
        screen.draw.text('LOSE',(450,370),color=(255,255,255),fontsize=100)
        screen.draw.text('Score: '+ str(score),(450,450),color=(255,255,255),fontsize=100)
        if game_over==False:
            sounds.intro.stop()
            sounds.gameover.play()
            game_over=True
    elif tank_life>0 and boss_life <=0:
        screen.fill((0,0,0))
        screen.draw.text('WIN',(450,370),color=(255,255,255),fontsize=100)
        screen.draw.text('Score: '+ str(score),(450,450),color=(255,255,255),fontsize=100)        
        if game_over==False:
            sounds.intro.stop()
            sounds.hg.play()
            game_over=True        
    else:
        background.draw()
        tank.draw()
        for buff in buffs:
            buff.draw()
        for wall in walls:
            wall.draw()
        for bullet in bullets:
            bullet.draw()
        for bullet in enemy_bullets:
            bullet.draw()
        for enemy in enemies:
            enemy.draw()
        
        if len(enemies)==0:
            boss.draw()
            for bullet in boss_bullets:
                bullet.draw()
        screen.draw.text('Life: '+str(tank_life),(10,750),color=(255,255,255),fontsize = 40)
        screen.draw.text('Score: '+ str(score),(10,710),color=(255,255,255),fontsize=40)
pgzrun.go()
