import pygame
import sys
import random
from openai import OpenAI
from typing import List, Dict

pygame.init()

client = OpenAI(
    base_url='http://10.15.88.73:5017/v1',
    api_key='ollama',  # required but ignored
)

dialogAI=['','','','']

window = pygame.display.set_mode((1024, 800)) # create a window
pygame.display.set_caption('DEMO of My First Pygame') # name

class Player(pygame.sprite.Sprite):
    def __init__(self, image_file, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = position

class Wall(pygame.sprite.Sprite):
    def __init__(self, image_file, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = position

image_title = pygame.image.load('assets/title.png') # prepare title
window.blit(image_title, (0, 0)) # display title
pygame.display.flip() # 1st refresh

image_lab = pygame.image.load('assets/lab.png')
image_castle = pygame.image.load('assets/castle.png')
image_forest = pygame.image.load('assets/forest.png')
image_forest_battle = pygame.image.load('assets/forest_battle.png')

sprite_wall_lab = Wall('assets/wall_lab.png', (0, 0))
sprite_wall0 = Wall('assets/wall0.png', (0, 0))
sprite_wall1 = Wall('assets/wall1.png', (0, 0))

image_castle_battle = pygame.image.load('assets/castle_battle.png')
image_forest_battle = pygame.image.load('assets/forest_battle.png')

image_lose = pygame.image.load('assets/lose.jpg')

image_green = pygame.image.load('assets/green.png')

image_green_ingame = pygame.transform.scale(image_green, (30, 40))

image_purple = pygame.image.load('assets/purple.png')

image_purple_ingame = pygame.transform.scale(image_purple, (30, 40))

image_Aventurine = pygame.image.load('assets/Aventurine.png')

image_Aventurine_ingame = pygame.transform.scale(image_Aventurine, (30, 40))

image_red = pygame.image.load('assets/red.png')
image_red = pygame.transform.scale(image_red, (250, 333))

image_red_battle = pygame.transform.scale(image_red, (250, 333))
image_red_ingame = pygame.transform.scale(image_red, (30, 40))

image_ice = pygame.image.load('assets/ice.png')
image_ice = pygame.transform.scale(image_ice, (250, 333))

image_ice_battle = pygame.transform.scale(image_ice, (250, 333))

image_endt = pygame.image.load('assets/ice.png')
image_endt = pygame.transform.scale(image_endt, (250, 333))

image_endt_battle = pygame.transform.scale(image_endt, (250, 333))

image_banana = pygame.image.load('assets/banana.png')

image_banana_ingame = pygame.transform.scale(image_banana, (30, 40))

ingame_dialogblock = pygame.image.load('assets/dialogblock.png')

ingame_hp_bar_boss = pygame.image.load('assets/hp_bar_boss.png')
ingame_hp_bar_enemy1 = pygame.image.load('assets/hp_bar_enemy1.png')
ingame_hp_bar_enemy2 = pygame.image.load('assets/hp_bar_enemy2.png')
ingame_hp_bar_enemy3 = pygame.image.load('assets/hp_bar_enemy3.png')
ingame_hp_bar_player = pygame.image.load('assets/hp_bar_player.png')

image_coinbar = pygame.image.load('assets/coinbar.png')

image_enemy1_battle = pygame.image.load('assets/enemy1.png')
image_enemy2_battle = pygame.image.load('assets/enemy2.png')
image_enemy3_battle = pygame.image.load('assets/enemy3.png')

image_boss_battle = pygame.image.load('assets/boss.png')

image_boss = pygame.transform.scale(image_boss_battle, (76, 92))

image_machine = pygame.image.load('assets/machine.png')

image_machine_ingame = pygame.transform.scale(image_machine, (42, 40))

image_enemy1 = pygame.transform.scale(image_enemy1_battle, (45, 46))
image_enemy2 = pygame.transform.scale(image_enemy2_battle, (43, 32))
image_enemy3 = pygame.transform.scale(image_enemy3_battle, (36, 43))

image_food1_battle = pygame.image.load('assets/food1.png')
image_food2_battle = pygame.image.load('assets/food2.png')
image_food3_battle = pygame.image.load('assets/food3.png')

image_food1 = pygame.transform.scale(image_food1_battle, (158, 216))
image_food2 = pygame.transform.scale(image_food2_battle, (158, 184))
image_food3 = pygame.transform.scale(image_food3_battle, (208, 128))

image_blast = pygame.image.load('assets/blast.png')

hplist = [20,35,60,90,120,200,400,1000,2700,8100]

world = 0
move = 0
battlemode = 0
interactive = False
interact_object = 0
dialog = -1

coins = 0
exp = 100
if (exp // 100) <= 6:
    lv = (exp // 100)
else: 
    exp = 699
    lv = 6
sword = 0
buff = 0

attack = 6 * lv
hp = hplist[lv]
defend = - 5 + lv * 5

if world == 1 and exp <= 698:
    lv_enemy = ((exp + 50) // 100)
elif world == 1 and exp >= 699: 
    lv_enemy = 8
else:
    lv_enemy = 10

attack_enemy = lv_enemy * 6 - 5
hp_enemy = hplist[(lv_enemy - 1)]
defend_enemy = - 5 + lv_enemy * 5
coin_min = 3 + lv_enemy * 4
coin_max = 10 + lv_enemy * 5

player_rect = [710, 125]
hero_rect = [140, 264]
enemy_rect = [590, 264]

enemyx = 512
enemyy = 400
enemytype = 1

dialoglist = [['Purple: Are you ready to go to research the grass or ','the castle?'], #0
['Press X if you\'re ready to go. Press C to cancel.'], 
['Press X if you\'re going to the grassland. Press C if','you\'re going to the castle.'],
['Purple: Don\'t you forget to play my VR game!'],
['Now I will trasnport you to thr grassland! Have a ','nice play!'],
['Now I will trasnport you to thr castle! Have a nice','play!'], #5
['Green: HEY YOU!! IT\'S ME!!!'],
['Green: EV3RY BUDDY \'S FAVORITE [[Number 1 Rated ','Salesman1997]]'],
['Green: LOOKS LIKE YOU\'RE [[All Alone On A Late','Night?]]'],
['Green: WELL HAVE I GOT SOME [[Special Upgrades]] FOR','LONELY [[Hearts]] LIKE YOU!!'],
['Green: HURRY UP AND BUY!'], #10
['Press X to see what you can buy. Press C to cancel.'],
['Green: YOUR [[Bronze Sword]] SEEMS TOO WEAK!!'],
['Green: ARE YOU LOOKING FOR THIS [[Iron Sword?]]'],
['Green: IT GIVES OUT 20% MORE [[Attack]] AND ONLY ','TAKES [[$15]]!!'],
['Press X to buy it. Press C to cancel.'], #15
['Green: YOUR [Iron Sword]] SEEMS TOO WEAK!!'],
['Green: ARE YOU LOOKING FOR THIS [[Steel Sword?]]'],
['Green: IT GIVES OUT 60% MORE [[Attack]] AND ONLY ','TAKES [[$30]]!!'],
['Press X to buy it. Press C to cancel.'], #19
['Green: YOUR [[Steel Sword]] SEEMS TOO WEAK!!'],
['Green: ARE YOU LOOKING FOR THIS [[Golden Sword?]]'],
['Green: IT GIVES OUT 100% MORE [[Attack]] AND ONLY','TAKES [[$50]]!!'],
['Press X to buy it. Press C to cancel.'], #23
['Green: YOUR [[Golden Sword]] SEEMS TOO WEAK!!'],
['Green: ARE YOU LOOKING FOR THIS [[Crystal Sword?]]'],
['Green: IT GIVES OUT 150% MORE [[Attack]] AND ONLY','TAKES [[$70]]!!'],
['Press X to buy it. Press C to cancel.'], #27
['Green: DELICIOUS KROMER'],
['Green: MONEY NO'],
['Green: WHAT!? YOU WERE SO CLOSE!!'],
['Green: SORRY, MY GOODS WERE SOLD OUT!!!'],
['Banana: Hey buddy, I\'m Banana te Chef!'], #32
['Banana: Do you want to purchase for some','energy-giving food?'], 
['Press X to see what you can buy. Press C to cancel.'],
['Banana: Try our canteen\'s best-cooked Hot Banana','Pie!'], #35
['Banana: It will active your nerves and give you a 30%','\addition to your attack in the next battle.'],
['Banana: It is on sale now and only takes you $26.'],
['(Remember: Buffs given by foods will only last one','battle and only the last buff will take effect.)'],
['Press X to buy it. Press C to cancel.'],
['Banana: What about our canteen\'s Herring-Flavored','Potato Chips'], #40
['Banana: It \'s our canteen\'s special and give you a','50% \addition to tour defend in the next battle.'],
['Banana: It is on sale now and only takes you $36.'],
['(Remember: Buffs given by foods will only last one','battle and only the last buff will take effect.)'],
['Press X to buy it. Press C to cancel.'],
['Banana: Well, are you interested in some kind of out','canteen\'s free Glutinous Flavored Lemonade!'], #45
['Banana: It will deduct 15% hp at the beginning but','make it easier to release end technique.'],
['(Remember: Buffs given by foods will only last one','battle and only the last buff will take effect.)'],
['Press X to take it. Press C to cancel.'],
['Banana: Thanks for purchasing!'],
['Banana: Uh-oh, you should get more coins and back!'], #50
['Banana: Come back whenever you want and see you!'],
['Aventurine: Hey, Do you wanna make a deal with me on','the recently started spaceship race?'],
['Aventurine: Lemme tell you this tiime\'s competitors:'],
['Aventurine: Lane 1 - Light particle ramjet engine,','you deserve to have it!'],
['Aventurine: Lane 2 - Sublight speed spacecraft, don\'t','forget to install a time stabilizer!'], #55
['Aventurine: Lane 3 - Sushi spaceship, why consider','streamline in vacuum?'],
['Aventurine: Oh! I forgor that you\'ve got no money','to bid!'],
['Aventurine: I will take you $10 to bid, OK?'],
['Press X - Bid for the light particle ramjet engine','Press C - Bid for the sublight speed spacecraft','Press V - Bid for the sushi spaceship'],
['Aventurine: You are truly worthy! The light particle','ramjet engine you chose did not disappoint and ranked','first.'], #60
['Aventurine: You are very smart, but you killed a dark','horse halfway. The light particle ramjet engine you','chose only ranked second.'],
['Aventurine: A good choice, but the light particle','ramjet engine you chose broke down midway and ranked','third.'],
['Aventurine: Are you Bole? The sub light speed','spacecraft you chose, which was not favored by others,','unexpectedly surpassed the most favored light particle','ramjet engine and won first place!'],
['Aventurine: Unfortunately, the sub light speed','spacecraft you chose ultimately did not surpass it\'s','biggest competitor, but second place is also very good'],
['Aventurine: I\'m very sorry, the sub light speed','spacecraft you selected was unable to complete the','race due to insufficient power and ranked third'], #65
['Aventurine: Sparkle installed bombs on two other','spacecraft, detonating them all. The clumsy sushi','spacecraft became the only contestant to advance to','the finish line, becoming the undisputed number one!'],
['Aventurine: The clumsy sushi spaceship, which has','always been least favored, unexpectedly surpassed one','opponent and became the second place.'],
['Aventurine: How could you think that the sushi','spaceship could win? It unsurprisingly came at the','bottom and became the third place.'],
['Aventurine: Congratulations on guessing the first','place correctly. But I\'ll give $9 to you. After all,','our transaction needs to continue so I can\'t possibly','lose money, can I?'],
['Aventurine: Sorry, the spaceship you guessed only','came in second. Let me give you $30 as comfort.'], #70
['Aventurine: Sorry, the spaceship you guessed only','came in third. Let\'s accept the bet and accept the','loss.'],
['Green: YOUR [[Crystal Sword]] SEEMS TOO WEAK!!'],
['Green: ARE YOU LOOKING FOR THIS [[Nether Alloy Sword?]]'],
['Green: IT GIVES OUT 220% MORE [[Attack]] AND ONLY','TAKES [[$110]]!!'],
['Press X to buy it. Press C to cancel.'], #75
['Press X to bid for the best. Press C to cancel.'],
['Aventurine: Maybe you can try it later.'],
['The machine seems glad to speak to you.'],
['Press X to ask how to apply LLM in the pygame','Press C to ask which spaceship may be the best choice.']
]

pygame.display.update() # refresh again

clock = pygame.time.Clock()

speed = 5

pygame.mixer.music.load('assets/title_theme.mp3')
pygame.mixer.music.play(-1, 0.0)

pygame.display.flip()

while True:
    if battlemode == 0:
        speed = 8
    else:
        speed = 80

    if (exp // 100) <= 6:
        lv = (exp // 100)
    else: 
        exp = 699
        lv = 6

    attack = 6 * lv
    hp = hplist[lv]
    defend = - 5 + lv * 5

    if (world == 1 or world == 307 or world == 308 or world == 309):
        lv_enemy = lv
        if sword >= 2: 
            lv_enemy += 1
        if sword >= 5: 
            lv_enemy += 1
    else:
        lv_enemy = 10

    attack_enemy = lv_enemy * 6 - 5
    hp_enemy = hplist[(lv_enemy - 1)]
    defend_enemy = - 5 + lv_enemy * 5
    coin_min = 3 + lv_enemy * 4
    coin_max = 10 + lv_enemy * 5

    if battlemode == 1:
        if row == 2 and hero_rect[0] < 540:
            hero_rect[0] += speed
        if row == 2 and hero_rect[0] >= 540:
            row = 3
        if row != 2 and hero_rect[0] > 140:
            hero_rect[0] -= speed
        if row == 6 and enemy_rect[0] > 190:
            enemy_rect[0] -= speed
        if row == 6 and enemy_rect[0] <= 190:
            row = 7
        if row != 6 and enemy_rect[0] < 590:
            enemy_rect[0] += speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                if battlemode == 0:
                    if interact_object == 1 and dialog == -1:
                        move = 0
                        dialog = 0
                    elif interact_object == 2 and dialog == -1:
                        move = 0
                        dialog = 6
                    elif interact_object == 3 and dialog == -1:
                        move = 0
                        dialog = 32
                    elif interact_object == 4 and dialog == -1:
                        move = 0
                        dialog = 52
                    elif interact_object == 5 and dialog == -1:
                        move = 0
                        dialog = 78
                    elif dialog == 0 or (dialog >= 6 and dialog <= 10) or (dialog >= 12 and dialog <= 14) or (dialog >= 16 and dialog <= 18) or (dialog >= 20 and dialog <= 22) or (dialog >= 24 and dialog <= 26) or (dialog >= 32 and dialog <= 33) or (dialog >= 35 and dialog <= 38) or (dialog >= 40 and dialog <= 43) or (dialog >= 45 and dialog <= 47) or (dialog >= 52 and dialog <= 55) or dialog == 58 or (dialog >= 72 and dialog <= 74) or dialog == 78:
                        dialog += 1
                    elif dialog == 56 and coins < 10:
                        dialog = 57
                    elif dialog == 56 and coins >= 10:
                        dialog = 76
                    elif dialog == 60 or dialog == 63 or dialog == 66:
                        dialog = 69
                    elif dialog == 61 or dialog == 64 or dialog == 67:
                        dialog = 70
                    elif dialog == 62 or dialog == 65 or dialog == 68:
                        dialog = 71
                    elif dialog == 69:
                        coins += 9
                        dialog = -1
                        move = 1
                    elif dialog == 70:
                        coins += 30
                        dialog = -1
                        move = 1
                    elif dialog == 3 or (dialog >= 28 and dialog <= 31) or (dialog >= 49 and dialog <= 51) or dialog == 57 or dialog == 71 or dialog == 77 or dialog == 80:
                        dialog = -1
                        move = 1
                    elif dialog == 4:
                        dialog = -1
                        world = 1
                        pygame.mixer.music.load('assets/forest.mp3')
                        pygame.mixer.music.play(-1, 0.0)
                        move = 1
                        player = Player('assets/wall_lab.png', (64, 64))

                        player_rect = [512,400]

                        enemyx = random.randint(50,974)
                        enemyy = random.randint(50,750)
                        enemytype = random.randint(1,3)

                        pygame.display.update()

                    elif dialog == 5:
                        dialog = -1
                        world = 3
                        pygame.mixer.music.load('assets/castle.mp3')
                        pygame.mixer.music.play(-1, 0.0)
                        move = 1
                        player = Player('assets/wall_lab.png', (64, 64))

                        player_rect = [64, 128]

                        enemyx = 476
                        enemyy = 354
                        enemytype = 10

                        pygame.display.update()

                    elif interact_object == 10 and dialog == -1:
                        world = (306 + enemytype)
                        move = 0
                        pygame.display.update()

                        hero_rect = [140, 264]
                        enemy_rect = [590, 264]
                        if enemytype < 4:
                            pygame.mixer.music.load('assets/forest_fight.mp3')
                            pygame.mixer.music.play(-1, 0.0)
                        else:
                            pygame.mixer.music.load('assets/boss_music.mp3')
                            pygame.mixer.music.play(-1, 0.0)

                        battlemode = 1
                        hp_battle = hp
                        hp_enemy_battle = hp_enemy
                        attack_battle = attack
                        attack_enemy_battle = attack_enemy
                        defend_battle = defend
                        defend_enemy_battle = defend_enemy
                        tp = 0
                        tp_enemy = 0
                        if buff == 3:
                            hp_battle = hp_battle * 0.85
                        elif buff == 2:
                            defend_battle = 1.5 * defend_battle
                        elif buff == 1:
                            attack_battle = 1.3 * attack_battle
                        else:
                            pass
                        if sword == 1:
                            attack_battle = 1.2 * attack_battle
                        elif sword == 2:
                            attack_battle = 1.6 * attack_battle
                        elif sword == 3:
                            attack_battle = 2 * attack_battle
                        elif sword == 4:
                            attack_battle = 2.5 * attack_battle
                        elif sword == 5:
                            attack_battle = 3.2 * attack_battle
                        else:
                            pass
                        attack_battle = int(attack_battle)
                        defend_battle = int(defend_battle)
                        hp_battle = int(hp_battle)
                        row = -1
                        xingtai = 0
                        weakness = 0
                        iced = False
                        fired = False
                        causeattack = 0
                        rongbao = 0
                        if enemytype < 4:
                            battleinst = ['An enemy approached you!']
                        else:
                            battleinst = ['Kamek the Evil Wizard approached you!']

                    elif interact_object == 20:
                        interact_object == 0
                        battlemode = 0
                        world = 2
                        pygame.mixer.music.load('assets/spacelab.mp3')
                        pygame.mixer.music.play(-1, 0.0)
                        move = 1
                        player = Player('assets/wall_lab.png', (710, 125))
                        player_rect = [710, 125]
                        pygame.display.update()

                else:
                    if row == -2:
                        interact_object == 20
                        battlemode = 0
                        world = 318
                        pygame.mixer.music.load('assets/gameover.mp3')
                        pygame.mixer.music.play(-1, 0.0)
                        move = 0
                        buff = 0
                        pygame.display.update()

                    if row == 0 or row == 4 or row == 8:
                        if hp_enemy_battle <= 0:
                            row = 10
                        elif hp_battle <= 0:
                            row = -2
                            battleinst = ['You were knocked down!']
                        else:
                            row += 1
                        if xingtai >= 2:
                            xingtai -= 2
                    if row == 9 or row == -1:
                        row = 1
                    if buff == 3 and tp <= 0:
                        tp = 1
                    if tp >= 5:
                        tp = 5
                    if row == 5:
                        tp_enemy += 1
                        if tp_enemy >= 5:
                            tp_enemy = 5
                            chat_completion = client.chat.completions.create(
                                messages=[
                                    {
                                        'role': 'system',
                                        'content': '你现在需要扮演游戏里面的NPC需要跟玩家进行回合制对战，在这个游戏中双方每个回合各自使用一次技能攻击对方，率先将对方生命值降低到小于等于0的一方会获胜，你需要采取最优策略以将对方生命值降至0，以获取游戏的胜利。当前是你的回合，你现在共有生命值' + str(hp_enemy_battle) + '点，你的对手玩家有生命值' + str(hp_battle) + '点，你有' + str(tp_enemy) + 'TP，你目前总共只有3个技能可以使用，它们分别是：1. 发起攻击，减少对手' + str(((attack_enemy_battle) * (100 - defend_battle)) // 100) + '点生命值，增加1TP。2. 回复' + str(((sword + 1) * attack_enemy_battle) // 3) + '点生命值，增加1TP，回复后的生命值将不超过' + str(hp_enemy_battle) + '。3. 释放终结技，减少对手' + str((attack_enemy_battle * (100 - defend_battle)) // 100) + '点生命值，减少5TP。你最多储存5TP。下一回合对方可能对你造成' + str(((attack_battle + lv * weakness) * (100 - defend_enemy_battle)) // 100) + '点伤害。请你输出你这回合需要发动的技能。如果要发动1技能，请输出1。如果要发动2技能请输出2。如果要发动3技能请输出3。请输出一个数字。'
                                    },
                                    {
                                        'role': 'user',
                                        'content': "Output the number of your chosen skill",
                                    }
                                ],
                                model='llama3.2',
                            )
                            # print(chat_completion.choices[0].message.content)
                        else:
                            chat_completion = client.chat.completions.create(
                                messages=[
                                    {
                                        'role': 'system',
                                        'content': '你现在需要扮演游戏里面的NPC需要跟玩家进行回合制对战，在这个游戏中双方每个回合各自使用一次技能攻击对方，率先将对方生命值降低到小于等于0的一方会获胜，你需要采取最优策略以将对方生命值降至0，以获取游戏的胜利。当前是你的回合，你现在共有生命值' + str(hp_enemy_battle) + '点，你的对手玩家有生命值' + str(hp_battle) + '点，你有' + str(tp_enemy) + 'TP，你目前总共只有2个技能可以使用，它们分别是：1. 发起攻击，减少对手' + str((attack_enemy_battle * (100 - defend_battle)) // 100) + '点生命值，增加1TP。2. 回复' + str(((sword + 1) * attack_enemy_battle) // 3) + '点生命值，增加1TP，回复后的生命值将不超过' + str(hp_enemy_battle) + '。你最多储存5TP。。下一回合对方可能对你造成' + str(((attack_battle + lv * weakness) * (100 - defend_enemy_battle)) // 100) + '点伤害。请你输出你这回合需要发动的技能。如果要发动1技能，请输出1。如果要发动2技能请输出2。请输出一个数字。'
                                    },
                                    {
                                        'role': 'user',
                                        'content': "Output the number of your chosen skill",
                                    }
                                ],
                                model='llama3.2',
                            )
                            # print(chat_completion.choices[0].message.content)
                        if chat_completion.choices[0].message.content == '3':
                            causeattack = 3 * (attack_enemy_battle * (100 - defend_battle)) // 100
                            tp_enemy = 0
                            row += 1
                            hp_battle -= causeattack
                        elif chat_completion.choices[0].message.content == '1':
                            causeattack = (attack_enemy_battle * (100 - defend_battle)) // 100
                            hp_battle -= causeattack
                            row += 1
                        else:
                            hp_enemy_battle += ((sword + 1) * attack_enemy_battle) // 3
                            if hp_enemy_battle >= hp_enemy:
                                hp_enemy_battle = hp_enemy
                            row += 3
                        
                    if row == -1:
                        battleinst = ['An enemy approached you!']
                    elif row == 1:
                        battleinst = ['','','','']
                        if xingtai == 0:
                            battleinst[0] = 'Press X - Use fire attack (Restore 1 TP)'
                        else:
                            battleinst[0] = 'Press X - Use ice attack (Restore 1 TP)'
                        battleinst[1] = 'Press C - Switch form (Restore 1 TP)'
                        battleinst[2] = 'Press V - Release end technique (5 TP needed)'
                        battleinst[3] = '(Now you have ' + str(tp) + '/5 TP)'
                    elif row == 6 or row == 7 or row == 8:
                        battleinst = ['','']
                        if chat_completion.choices[0].message.content == '1':
                            if enemytype < 4:
                                battleinst[0] = 'The enemy attacked you and you lost ' + str(causeattack) + ' HP!'
                            else:
                                battleinst[0] = 'Kamek attacked you and you lost ' + str(causeattack) + ' HP!'
                            if tp_enemy < 5:
                                tp_enemy += 1
                        elif chat_completion.choices[0].message.content == '3':
                            if enemytype < 4:
                                battleinst[0] = 'The enemy released end technique to you and you lost'
                                battleinst[1] = str(causeattack) + ' HP!'
                            else:
                                battleinst[0] = 'Kamek released end technique to you and you lost'
                                battleinst[1] = str(causeattack) + ' HP!'
                            tp_enemy -= 5
                        else:
                            if enemytype < 4:
                                battleinst[0] = 'The enemy recovered ' + str(((sword + 1) * attack_enemy_battle) // 3) + ' HP!'
                            else:
                                battleinst[0] = 'Kamek recovered ' + str(((sword + 1) * attack_enemy_battle) // 3) + ' HP!'
                            if tp < 5:
                                tp_enemy += 1

                    elif row == 10:
                        pygame.mixer.music.load('assets/Y.mp3')
                        pygame.mixer.music.play(-1, 0.0)
                        coingained = random.randint(coin_min, coin_max)
                        coins += coingained
                        exp += 30
                        if exp >= 699:
                            exp = 699
                        battleinst = ['','','','']
                        battleinst[0] = 'The enemy fled away!'
                        battleinst[1] = 'You gained 30 EXP and ' + str(coingained) + ' coins!'
                        if exp % 100 <= 29:
                            battleinst[2] = 'Your LV upgraded!'
                            battleinst[3] = '(Press Z again to continue...)'
                        elif exp >= 699:
                            battleinst[2] = 'Your EXP was maxed out!'
                            battleinst[3] = '(Press Z again to continue...)'
                        else:
                            battleinst[2] = '(Press Z again to continue...)'
                        row += 1

                    elif row == 11:
                        interact_object == 0
                        battlemode = 0
                        world = 2
                        pygame.mixer.music.load('assets/spacelab.mp3')
                        pygame.mixer.music.play(-1, 0.0)
                        move = 1
                        buff = 0

                        player = Player('assets/wall_lab.png', (710, 125))

                        player_rect = [710, 125]

                        pygame.display.update()

                    else:
                        pass

            if event.key == pygame.K_x:
                if battlemode == 0:
                    if dialog == 1:
                        dialog = 2
                    elif dialog == 2:
                        dialog = 4
                    elif dialog == 11 and sword == 0:
                        dialog = 12
                    elif dialog == 11 and sword == 1:
                        dialog = 16
                    elif dialog == 11 and sword == 2:
                        dialog = 20
                    elif dialog == 11 and sword == 3:
                        dialog = 24
                    elif dialog == 11 and sword == 4:
                        dialog = 72
                    elif dialog == 11 and sword == 5:
                        dialog = 31
                    elif dialog == 15 and coins >= 15:
                        coins -= 15
                        sword = 1
                        dialog = 28
                    elif dialog == 19 and coins >= 30:
                        coins -= 30
                        sword = 2
                        dialog = 28
                    elif dialog == 23 and coins >= 50:
                        coins -= 50
                        sword = 3
                        dialog = 28
                    elif dialog == 27 and coins >= 70:
                        coins -= 70
                        sword = 4
                        dialog = 28
                    elif dialog == 75 and coins >= 110:
                        coins -= 110
                        sword = 5
                        dialog = 28
                    elif (dialog == 15 and coins < 15) or (dialog == 19 and coins < 30) or (dialog == 23 and coins < 50) or (dialog == 27 and coins < 70) or (dialog == 75 and coins < 110):
                        dialog = 29
                    elif dialog == 34:
                        dialog = 35
                    elif dialog == 39 and coins >= 26:
                        coins -= 26
                        buff = 1
                        dialog = 49
                    elif dialog == 44 and coins >= 36:
                        coins -= 36
                        buff = 2
                        dialog = 49
                    elif dialog == 48:
                        buff = 3
                        dialog = 49
                    elif (dialog == 39 and coins <= 26) or (dialog == 44 and coins <= 36):
                        dialog = 50
                    elif dialog == 76:
                        dialog = 58
                        coins -= 10
                    elif dialog == 79:
                        dialog = 80
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {
                                    'role': 'system',
                                    'content': 'You are a helpful teaching assitant of computer science lessons, \
                                        you should help CS freshman with teaching \
                                        how to use LLM to design and create games better. '
                                },
                                {
                                    'role': 'user',
                                    'content': "How we can involve LLM into a part of game?Please answer within 4 sentances, each of which has no more than 8 words, and each sentence ending by #.",
                                }
                            ],
                            model='llama3.2',
                        )

                        dialogAI = chat_completion.choices[0].message.content.split('#')
                        dialogAI[1] = dialogAI[1][2::]
                        dialogAI[2] = dialogAI[2][2::]
                        dialogAI[3] = dialogAI[3][2::]
                        
                    elif dialog == 59:
                        if random.randint(1,10) >= 6:
                            dialog = 60
                        elif random.randint(1,5) >= 3:
                            dialog = 61
                        else:
                            dialog = 62

                else:
                    if row == 1:
                        if xingtai == 0:
                            fired = True
                        else:
                            iced = True
                        if fired and iced:
                            weakness += 1
                            fired = False
                            iced = False
                            rongbao = 1
                        causeattack = ((attack_battle + lv * lv * weakness) * (100 - defend_enemy_battle)) // 100
                        hp_enemy_battle -= causeattack
                        row += 1
                        tp += 1

                    if tp >= 5:
                        tp = 5

                    if row == 2 or row == 3 or row == 4:
                        battleinst = ['','','']
                        if rongbao == 1:
                            rongbao = 0
                            if enemytype < 4:
                                battleinst[0] = 'The enemy was weakened because of melting explosion!'
                                if xingtai == 0:
                                    battleinst[1] = 'You used fire attack and caused ' + str(causeattack) + ' damage to the'
                                    battleinst[2] = 'enemy!'
                                else:
                                    battleinst[1] = 'You used ice attack and caused ' + str(causeattack) + ' damage to the'
                                    battleinst[2] = 'enemy!'
                            else:
                                battleinst[0] = 'Kamek was weakened because of melting explosion!'
                                if xingtai == 0:
                                    battleinst[1] = 'You used fire attack and caused ' + str(causeattack) + ' damage to Kamek!'
                                else:
                                    battleinst[1] = 'You used ice attack and caused ' + str(causeattack) + ' damage to Kamek!'
        
                        else:
                            if enemytype < 4:
                                if xingtai == 0:
                                    battleinst[0] = 'You used fire attack and caused ' + str(causeattack) + ' damage to the'
                                    battleinst[1] = 'enemy!'
                                else:
                                    battleinst[0] = 'You used ice attack and caused ' + str(causeattack) + ' damage to the'
                                    battleinst[1] = 'enemy!'
                            else:
                                if xingtai == 0:
                                    battleinst[0] = 'You used fire attack and caused ' + str(causeattack) + ' damage to Kamek!'
                                else:
                                    battleinst[0] = 'You used ice attack and caused ' + str(causeattack) + ' damage to Kamek!'

            if event.key == pygame.K_c:
                if battlemode == 0:
                    if dialog == 1:
                        dialog = 3
                    elif dialog == 2:
                        dialog = 5
                    elif dialog == 11 or dialog == 15 or dialog == 19 or dialog == 23 or dialog == 27:
                        dialog = 30
                    elif dialog == 34 or dialog == 48:
                        dialog = 51
                    elif dialog == 39:
                        dialog = 40
                    elif dialog == 44:
                        dialog = 45
                    elif dialog == 76:
                        dialog = 77
                    elif dialog == 59:
                        if random.randint(1,10) >= 7:
                            dialog = 63
                        elif random.randint(1,6) >= 4:
                            dialog = 64
                        else:
                            dialog = 65
                    elif dialog == 79:
                        dialog = 80
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {
                                    'role': 'system',
                                    'content': 'You\'re gabing on a spaceship race. There are 3 spaceships.  \
                                        The first spaceship, the light particle ramjet engine has 50 percent possibility to be the first,\
                                        30 percent possibility to be the second and 20 percent possibility to be the last.\
                                        The second spaceship, the sublight speed spacecraft has 40 percent possibility to be the first,\
                                        30 percent possibility to be the second and 30 percent possibility to be the last.\
                                        The third spaceship, the sushi spaceship has 10 percent possibility to be the first,\
                                        40 percent possibility to be the second and 50 percent possibility to be the last.\
                                        If the spaceship you choose wins the first, you\'ll gain $9. \
                                        If the spaceship you choose wins the second, you\'ll gain $30. \
                                        If the spaceship you choose wins the third, you\'ll gain $0. '
                                },
                                {
                                    'role': 'user',
                                    'content': "How to bid to make the most profit? Please answer within 4 sentances, each of which has no more than 8 words, and each sentence ending by #.",
                                }
                            ],
                            model='llama3.2',
                        )

                        dialogAI = chat_completion.choices[0].message.content.split('#')
                        dialogAI[1] = dialogAI[1][2::]
                        dialogAI[2] = dialogAI[2][2::]
                        dialogAI[3] = dialogAI[3][2::]

                else:
                    if row == 1:
                        if tp <= 4:
                            tp += 1
                        if xingtai == 0:
                            xingtai = 1
                            battleinst = ['You changed your form to ice!']
                        else:
                            xingtai = 0
                            battleinst = ['You changed your form to fire!']
                        row = 4

            if event.key == pygame.K_v:
                if battlemode == 0:
                    if dialog == 59:
                        if random.randint(1,10) >= 10:
                            dialog = 66
                        elif random.randint(1,9) >= 6:
                            dialog = 67
                        else:
                            dialog = 68

                else:
                    if row == 1:
                        if tp <= 4:
                            row = 0
                        else:
                            xingtai += 2
                            causeattack = 3 * ((attack_battle + lv * weakness) * (100 - defend_enemy_battle)) // 100
                            hp_enemy_battle -= causeattack
                            battleinst = ['','']
                            battleinst[0] = 'You released end technique and caused ' + str(causeattack) + ' damage to'
                            if enemytype < 4:
                                battleinst[1] = 'the enemy!'
                            else:
                                battleinst[1] = 'Kamek!'
                            tp = 0
                            row = 2

                    if row == 0:
                        battleinst = ['Not enough TP']

            if event.key == pygame.K_F1:
                if battlemode == 0:
                    exp = 699
                    sword = 5

            if event.key == pygame.K_F2:
                coins = 5000

            if event.key == pygame.K_F3:
                if battlemode == 1:
                    hp_enemy_battle = 1

    keys = pygame.key.get_pressed()

    if keys[pygame.K_z] and (world == 0 or world == 318): # check press z
        #print("Z key pressed. Starting...")
        world = 2
        pygame.mixer.music.load('assets/spacelab.mp3')
        pygame.mixer.music.play(-1, 0.0)
        move = 1

        player = Player('assets/wall_lab.png', (710, 125))
        
        player_rect = [710, 125]
        
        pygame.display.update() # 1st refresh

    if (keys[pygame.K_w] or keys[pygame.K_UP]) and move == 1:
        player_rect[1] -= speed
        if (check_wall_lab() and world == 2) or (check_wall_edge() and world != 2):
            #print("YES")
            player_rect[1] += speed

    if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and move == 1:
        player_rect[1] += speed
        if (check_wall_lab() and world == 2) or (check_wall_edge() and world != 2):
            #print("YES")
            player_rect[1] -= speed

    if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and move == 1:
        player_rect[0] -= speed
        if (check_wall_lab() and world == 2) or (check_wall_edge() and world != 2):
            #print("YES")
            player_rect[0] += speed

    if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and move == 1:
        player_rect[0] += speed
        if (check_wall_lab() and world == 2) or (check_wall_edge() and world != 2):
            #print("YES")
            player_rect[0] -= speed

    def check_wall_lab():
        if player_rect[0] <= 32 or player_rect[0] >= 962 or player_rect[1] <= 32 or player_rect[1] >= 728:
            return True
        elif player_rect[0] >= 386 and player_rect[0] <= 448 and player_rect[1] >= 352:
            return True
        elif player_rect[0] <= 448 and player_rect[1] <= 160:
            return True
        elif player_rect[0] >= 770 and player_rect[1] >= 312 and player_rect[1] <= 384:
            return True
        elif player_rect[0] >= 386 and player_rect[0] <= 608 and player_rect[1] >= 312 and player_rect[1] <= 384:
            return True
        else:
            return False

    def check_wall_edge():
        if player_rect[0] <= 32 or player_rect[0] >= 962 or player_rect[1] <= 32 or player_rect[1] >= 728:
            return True
        else:
            return False

    def check_dialog_purple(x, y):
        distance_purple = ((x - 925) ** 2 + (y - 416) ** 2) ** (1 / 2)
        if distance_purple <= 120 and world == 2:
            return True
        else:
            return False

    def check_dialog_green(x, y):
        distance_green = ((x - 480) ** 2 + (y - 416) ** 2) ** (1 / 2)
        if distance_green <= 120 and world == 2:
            return True
        else:
            return False

    def check_dialog_banana(x, y):
        distance_banana = ((x - 216) ** 2 + (y - 96) ** 2) ** (1 / 2)
        if distance_banana <= 120 and world == 2:
            return True
        else:
            return False
        
    def check_dialog_Aventurine(x, y):
        distance_Aventurine = ((x - 64) ** 2 + (y - 720) ** 2) ** (1 / 2)
        if distance_Aventurine <= 120 and world == 2:
            return True
        else:
            return False

    def check_dialog_machine(x, y):
        distance_machine = ((x - 344) ** 2 + (y - 720) ** 2) ** (1 / 2)
        if distance_machine <= 120 and world == 2:
            return True
        else:
            return False

    def check_battle_enemy(x, y):
        distance_enemy = ((x - enemyx) ** 2 + (y - enemyy) ** 2) ** (1 / 2)
        if distance_enemy <= 120 and (world == 1 or world == 3):
            return True
        else:
            return False

    if check_dialog_purple(player_rect[0], player_rect[1]):
        interactive = True
        interact_object = 1
    elif check_dialog_green(player_rect[0], player_rect[1]):
        interactive = True
        interact_object = 2
    elif check_dialog_banana(player_rect[0], player_rect[1]):
        interactive = True
        interact_object = 3
    elif check_battle_enemy(player_rect[0], player_rect[1]):
        interactive = True
        interact_object = 10
    elif check_dialog_Aventurine(player_rect[0], player_rect[1]):
        interactive = True
        interact_object = 4
    elif check_dialog_machine(player_rect[0], player_rect[1]):
        interactive = True
        interact_object = 5
    else: 
        interactive = False
        interact_object = 0

    match world:
        case 0:
            bg = image_title
            wall = sprite_wall0
        case 1:
            bg = image_forest
            wall = sprite_wall1
        case 2:
            bg = image_lab
            wall = sprite_wall_lab
        case 3:
            bg = image_castle
            wall = sprite_wall0
        case 307:
            bg = image_forest_battle
            wall = sprite_wall0
        case 308:
            bg = image_forest_battle
            wall = sprite_wall0
        case 309:
            bg = image_forest_battle
            wall = sprite_wall0
        case 316:
            bg = image_castle_battle
            wall = sprite_wall0
        case 318:
            bg = image_lose
            wall = sprite_wall0

    if world != 1:
        window.blit(bg, (0, 0))
        window.blit(wall.image, (0, 0))
    else:
        window.blit(bg, (-player_rect[0], -player_rect[1]))
        window.blit(wall.image, (-player_rect[0]+512, -player_rect[1]+400))
    
    match world:
        case 0:
            window.blit(image_red, (100, 403))

            font_title = pygame.font.Font('assets/DTM-Mono-1.otf', 70) # set a font
            text_title = font_title.render('Spaceman Blast Demo', True, (0, 0, 0)) # create a text
            window.blit(text_title, (120, 10)) # display title text
            
            font_title = pygame.font.Font('assets/DTM-Mono-1.otf', 24)
            text_title = font_title.render('A Game Bade By Kim Xie', True, (0, 0, 0))
            window.blit(text_title, (365, 130))
            text_title = font_title.render('Press Z to Begin', True, (0, 0, 0))
            window.blit(text_title, (410, 180))
            
            text_title = font_title.render('When you play:', True, (0, 0, 0))
            window.blit(text_title, (425, 230))
            text_title = font_title.render('Press arrow keys or WASD to move', True, (0, 0, 0))
            window.blit(text_title, (290, 280))
            text_title = font_title.render('Press Z to interact', True, (0, 0, 0))
            window.blit(text_title, (390, 330))

        case 1:
            player = pygame.image.load("assets/red.png")
            player = pygame.transform.scale(player, (30, 40))
            window.blit(player, (497, 380))
            if enemytype == 1:
                window.blit(image_enemy1, (-player_rect[0]+enemyx+512, -player_rect[1]+enemyy+400))
            elif enemytype == 2:
                window.blit(image_enemy2, (-player_rect[0]+enemyx+512, -player_rect[1]+enemyy+400))
            else:
                window.blit(image_enemy3, (-player_rect[0]+enemyx+512, -player_rect[1]+enemyy+400))

        case 2:
            window.blit(sprite_wall_lab.image, (0, 0))

            player = pygame.image.load("assets/red.png")
            player = pygame.transform.scale(player, (30, 40))
            window.blit(player, player_rect)
            
            window.blit(image_green_ingame, (480, 416))
            window.blit(image_purple_ingame, (925, 416))
            window.blit(image_banana_ingame, (216, 96))
            window.blit(image_Aventurine_ingame, (64, 720))
            window.blit(image_machine_ingame, (344, 720))

        case 3:
            player = pygame.image.load("assets/red.png")
            player = pygame.transform.scale(player, (30, 40))
            window.blit(player, player_rect)
            window.blit(image_boss, (enemyx, enemyy))

        case 307:
            if xingtai == 0:
                battle_hero = pygame.image.load("assets/red.png")
            elif xingtai == 1:
                battle_hero = pygame.image.load("assets/ice.png")
            else:
                battle_hero = pygame.image.load("assets/endt.png")
            battle_enemy = pygame.image.load("assets/enemy1.png")
            battle_enemy = pygame.transform.scale(battle_enemy, (228, 233))
            window.blit(battle_hero, hero_rect)
            window.blit(battle_enemy, enemy_rect)

        case 308:
            if xingtai == 0:
                battle_hero = pygame.image.load("assets/red.png")
            elif xingtai == 1:
                battle_hero = pygame.image.load("assets/ice.png")
            else:
                battle_hero = pygame.image.load("assets/endt.png")
            battle_enemy = pygame.image.load("assets/enemy2.png")
            battle_enemy = pygame.transform.scale(battle_enemy, (218, 162))
            window.blit(battle_hero, hero_rect)
            window.blit(battle_enemy, enemy_rect)

        case 309:
            if xingtai == 0:
                battle_hero = pygame.image.load("assets/red.png")
            elif xingtai == 1:
                battle_hero = pygame.image.load("assets/ice.png")
            else:
                battle_hero = pygame.image.load("assets/endt.png")
            battle_enemy = pygame.image.load("assets/enemy3.png")
            battle_enemy = pygame.transform.scale(battle_enemy, (180, 219))
            window.blit(battle_hero, hero_rect)
            window.blit(battle_enemy, enemy_rect)
        
        case 316:
            if xingtai == 0:
                battle_hero = pygame.image.load("assets/red.png")
            elif xingtai == 1:
                battle_hero = pygame.image.load("assets/ice.png")
            else:
                battle_hero = pygame.image.load("assets/endt.png")
            battle_enemy = pygame.image.load("assets/boss.png")
            battle_enemy = pygame.transform.scale(battle_enemy, (194, 233))
            window.blit(battle_hero, hero_rect)
            window.blit(battle_enemy, enemy_rect)

    if dialog != -1:
        window.blit(ingame_dialogblock, (12, 538))
        font_dialog = pygame.font.Font('assets/DTM-Mono-1.otf', 30)
        if dialog < 80:
            text_dialog = font_dialog.render(dialoglist[dialog][0], True, (255, 255, 255))
            window.blit(text_dialog, (40, 566))
            if len(dialoglist[dialog]) >= 2:
                text_dialog2 = font_dialog.render(dialoglist[dialog][1], True, (255, 255, 255))
                window.blit(text_dialog2, (40, 616))
            if len(dialoglist[dialog]) >= 3:
                text_dialog2 = font_dialog.render(dialoglist[dialog][2], True, (255, 255, 255))
                window.blit(text_dialog2, (40, 666))
            if len(dialoglist[dialog]) >= 4:
                text_dialog2 = font_dialog.render(dialoglist[dialog][3], True, (255, 255, 255))
                window.blit(text_dialog2, (40, 716))
        else:
            text_dialog = font_dialog.render(dialogAI[0], True, (255, 255, 255))
            window.blit(text_dialog, (40, 566))
            if len(dialogAI) >= 2:
                text_dialog2 = font_dialog.render(dialogAI[1], True, (255, 255, 255))
                window.blit(text_dialog2, (40, 616))
            if len(dialogAI) >= 3:
                text_dialog2 = font_dialog.render(dialogAI[2], True, (255, 255, 255))
                window.blit(text_dialog2, (40, 666))
            if len(dialogAI) >= 4:
                text_dialog2 = font_dialog.render(dialogAI[3], True, (255, 255, 255))
                window.blit(text_dialog2, (40, 716))

    if battlemode == 1:
        window.blit(ingame_dialogblock, (12, 538))
        font_battle = pygame.font.Font('assets/DTM-Mono-1.otf', 30)
        text_battle = font_battle.render(battleinst[0], True, (255, 255, 255))
        window.blit(text_battle, (40, 566))
        if len(battleinst) >= 2:
            text_battle2 = font_dialog.render(battleinst[1], True, (255, 255, 255))
            window.blit(text_battle2, (40, 616))
        if len(battleinst) >= 3:
            text_battle3 = font_dialog.render(battleinst[2], True, (255, 255, 255))
            window.blit(text_battle3, (40, 666))
        if len(battleinst) >= 4:
            text_battle4 = font_dialog.render(battleinst[3], True, (255, 255, 255))
            window.blit(text_battle4, (40, 716))
        window.blit(ingame_hp_bar_player, (12, 12))
        if enemytype == 1:
            window.blit(ingame_hp_bar_enemy1, (732, 12))
        elif enemytype == 2:
            window.blit(ingame_hp_bar_enemy2, (732, 12))
        elif enemytype == 3:
            window.blit(ingame_hp_bar_enemy3, (732, 12))
        else:
            window.blit(ingame_hp_bar_boss, (732, 12))

        if row == 3:
            window.blit(image_blast, (502, 240))
            row = 4
        if row == 7:
            window.blit(image_blast, (152, 240))
            row = 8

        font_inst = pygame.font.Font('assets/DTM-Mono-1.otf', 20)
        image_lv_player = pygame.image.load('assets/lv' + str(lv) + '.png')
        image_lv_enemy = pygame.image.load('assets/lv' + str(lv_enemy) + '.png')
        myhp = font_inst.render(('HP ' + str(hp_battle) + '/' + str(hp)), True, (255, 255, 255))
        enemyhp = font_inst.render(('HP ' + str(hp_enemy_battle) + '/' + str(hp_enemy)), True, (255, 255, 255))
        window.blit(myhp, (100, 56))
        window.blit(enemyhp, (820, 56))
        window.blit(image_lv_player, (100, 24))
        window.blit(image_lv_enemy, (820, 24))

    if interactive:
        if move == 1:
            font_ingame = pygame.font.Font('assets/DTM-Mono-1.otf', 12)
            if interact_object == 10:
                text_interact = font_ingame.render('Press Z to battle', True, (0, 0, 0))
                window.blit(text_interact, (447, 355))
            else:
                text_interact = font_ingame.render('Press Z to interact', True, (0, 0, 0))
                window.blit(text_interact, ((player_rect[0] - 50), (player_rect[1] - 25)))

    if dialog == 35 or dialog == 36:
        window.blit(image_food3, (404, 255))
    if dialog == 40 or dialog == 41:
        window.blit(image_food1, (454, 207))
    if dialog == 45 or dialog == 46:
        window.blit(image_food2, (454, 223))

    if battlemode == 0 and world != 0 and world != 318:
        window.blit(ingame_hp_bar_player, (12, 12))
        font_inst = pygame.font.Font('assets/DTM-Mono-1.otf', 20)
        image_lv_player = pygame.image.load('assets/lv' + str(lv) + '.png')
        if lv <= 5:
            myexp = font_inst.render(('EXP ' + str(exp) + '/' + str((lv * 100 + 100))), True, (255, 255, 255))
        else:
            myexp = font_inst.render(('EXP ' + str(exp) + '/699'), True, (255, 255, 255))
        window.blit(image_lv_player, (100, 24))
        window.blit(myexp, (100, 56))

    if world != 0 and world != 318:
        window.blit(image_coinbar, (326, 12))
        font_coin = pygame.font.Font('assets/DTM-Mono-1.otf', 40)
        text_coin = font_coin.render(str(coins), True, (255, 255, 255))
        window.blit(text_coin, ((512 - 14 * (len(str(coins)))), 22))

    # Update the screen display
    pygame.display.update()

    clock.tick(30)
