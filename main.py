import os

import pygame,sys

import Engel

from Kahraman import Kahraman
from Laser import Laser
from Mahlukatlar import Mahlukat, Extra
from random import *



class Game:
    def __init__(self):
        #Kahraman sinifina ait metodlar can ve skor
        #screen_w silindi
        self.kahraman_can = 3
        self.can_gosterge=pygame.image.load("grafikler/player.png")
        self.can_gosterge_pos_x=160- (self.can_gosterge.get_size()[0] * 2 + 20) #tek deger ile x deki konumunu aldık
        self.skor= 0
        self.level=1
        self.font=pygame.font.Font(os.path.join(f'grafikler/Pixeled.ttf'),20)
        kahraman_sprite=Kahraman((screen_w / 2, screen_h), screen_w, 5,self.kahraman_can)
        self.kahraman=pygame.sprite.GroupSingle(kahraman_sprite)

        #engel sinifinin uygulanmasi
        self.sekil=Engel.sekil
        self.blok_boyutu=7
        self.bloklar=pygame.sprite.Group()  #Blokların yaratılması ve konumlandırılması
        self.Engel_miktari=5
        self.Engel_x_pos=[num*(screen_w/self.Engel_miktari) for num in range(self.Engel_miktari)] #Aralıklı olarak engelleri tek seferde tanimladik
        self.coklu_engel_yarat(*self.Engel_x_pos,xbaslangic=screen_w/15,ybaslangic=600)

        #Mahlukat sinifinin uygulanmasi
        self.mahlukatlar=pygame.sprite.Group()
        self.satir = 4
        self.sutun = 4
        # self.mahlukat_yarat(self.satir,self.sutun)
        self.mahlukat_carpti=False
        self.mahlukat_yon=1
        self.mahlukat_lazer=pygame.sprite.Group()
        #Ekstra sinifinin uygulanmasi
        self.extra=pygame.sprite.GroupSingle()
        self.extra_canlanma_suresi=randint(400,800)
        self.sayac=0

        #Ses dosyalarinin eklenmesi
        self.lazer_ses=pygame.mixer.Sound("sesler/laser.wav")
        self.lazer_ses.set_volume(0.02)
        self.kill_ses=pygame.mixer.Sound("sesler/explosion.wav")
        self.kill_ses.set_volume(0.02)
        self.gameover = pygame.mixer.Sound("sesler/gameover.mp3")
        self.gameover.set_volume(1)

        self.oyun_sonu=False
        if os.path.exists('skor.txt'):
            with open('skor.txt', 'r') as file:
                self.high_score = int(file.read())
        else:
            self.high_score = 0

    def engel_yarat(self,xbaslangic,ybaslangic,offset_x):
        for satir_index,row in enumerate(self.sekil):
            for sutun_index, col in enumerate(row):
                if col=="x":             #engelleri x olarak gorup spriteları daha sonra gruba ekleyecek
                    x=xbaslangic+sutun_index * self.blok_boyutu + offset_x
                    y=ybaslangic+satir_index * self.blok_boyutu
                    blok=Engel.Blok(self.blok_boyutu,(240,80,80),x,y)
                    self.bloklar.add(blok)   #Bloklara blok eklenmesi

    def coklu_engel_yarat(self,*offset,xbaslangic,ybaslangic):
        for offset_x in offset:
            self.engel_yarat(xbaslangic,ybaslangic,offset_x)

    def mahlukat_yarat(self,satir,sutun):  #offset ekrandaki pozisyonu
        xuzaklik=60
        yuzaklik = 48
        xoffset = 70
        yoffset = 100
        for satir_index, row in enumerate(range(satir)):
            for sutun_index, col in enumerate(range(sutun)):
                x=sutun_index * xuzaklik + xoffset
                y=satir_index * yuzaklik + yoffset
                if satir_index==0: mahlukat_sprite=Mahlukat('sari',x,y)    #sıraya göre renk ataması
                elif 1<=satir_index<=2: mahlukat_sprite=Mahlukat('yesil',x,y)
                else: mahlukat_sprite=Mahlukat('kirmizi',x,y)
                self.mahlukatlar.add(mahlukat_sprite)                      #spriteların gruba eklenmesi
        screen.fill("green")

    def mahlukat_pos_kontrol(self):
        mahlukat_grubu=self.mahlukatlar.sprites()
        for mahlukat in mahlukat_grubu:
            if mahlukat.rect.right>=screen_w:  #ekranın sagi kontrol
                self.mahlukat_yon=-1         #mahlukatların hizi assagida yone de bagli
                self.mahlukat_asagi_hareket(2) #asagi haraket edecegi blok sayisi
            elif mahlukat.rect.left<=0:        #ekranın solu kontrol
                self.mahlukat_yon=1
                self.mahlukat_asagi_hareket(2)
            # elif mahlukat.rect.bottom >= screen_h-30:
            #     self.mahlukat_carpti = True   #mahlukatlarin ekranın altina carpmasi
            #     self.oyun_sonu=True

    def mahlukat_asagi_hareket(self,uzaklik):
        if self.mahlukatlar:
            for mahlukat in self.mahlukatlar.sprites():
                mahlukat.rect.y+=uzaklik   #verilen uzaklik kadar y ekseninde hareket sagliyor

    def mahlukat_ates(self):
        if self.mahlukatlar.sprites():
            random_mahlukat=choice(self.mahlukatlar.sprites())
            lazer_sprite=Laser(random_mahlukat.rect.center,6,screen_h)    #lazerin atis hizi
            self.mahlukat_lazer.add(lazer_sprite) #mahlukat lazer sprite grubuna rastgele ates eden lazerin eklenmesi
            self.lazer_ses.play()

    def extra_mahlukat_sayac(self):
        self.extra_canlanma_suresi-=1
        if self.extra_canlanma_suresi<=0:
            self.extra.add(Extra(choice(['sag','sol']),screen_w))  #Extra mahlukatın sagdan soldan gelmesini ayarladım
            self.extra_canlanma_suresi = randint(300, 500)

    def carpisma_kontrol(self,can):
        #Kahraman lazer

        if self.kahraman.sprite.lazerler:
            for lazer in self.kahraman.sprite.lazerler:
                # Engel carpismalari
                if pygame.sprite.spritecollide(lazer,self.bloklar,True):
                    lazer.kill()
                mahlukat_vurulma=pygame.sprite.spritecollide(lazer, self.mahlukatlar, True)
                if mahlukat_vurulma:                        #carpisma gerceklestirildiginde renke gore deger eklenmesi
                    for mahlukat in mahlukat_vurulma:
                        self.skor+=mahlukat.deger
                    if (self.sayac != 0):
                            self.sayac-=1
                            print(self.sayac)
                            pass
                        # if not (self.sayac == 0):
                        #     self.sayac-=1
                    else:
                        lazer.kill()
                        # pass

                    self.kill_ses.play()
                if pygame.sprite.spritecollide(lazer,self.extra,True):
                    self.skor+=500
                    lazer.kill()
                    self.sayac=6   #extrayı vurusak arka arkaya vurabilmek icin

        if self.mahlukat_lazer:
            for lazer in self.mahlukat_lazer:
                # mahlukat lazer olayları
                if pygame.sprite.spritecollide(lazer,self.bloklar,True):
                    lazer.kill()

                if pygame.sprite.spritecollide(lazer,self.kahraman,False):
                    lazer.kill()
                    screen.fill("#FF6347")
                    self.kahraman_can-=1
                    self.can_kontrol()
                    print("Vuruldun")

        #mahlukatların bloklara carpmasi
        if self.mahlukatlar:
            for mahlukat in self.mahlukatlar:
                pygame.sprite.spritecollide(mahlukat, self.bloklar, True)
                if  pygame.sprite.spritecollide(mahlukat,self.kahraman,False):
                    self.mahlukat_carpti=True
                    self.oyun_sonu=True

    def can_kontrol(self):  #can kontrol icin biseyler deniyecem
        if self.kahraman_can == 0:
            return True

    def can_goster(self):
        for can in range(self.kahraman_can - 1):
            x=self.can_gosterge_pos_x + (can * (self.can_gosterge.get_size()[0] + 10))          #pozisyon ataması
            screen.blit(self.can_gosterge,(x,8))

    def level_goster(self):
        level_gosterge=self.font.render(f'LeveL {self.level}',False,'white')
        level_rect=level_gosterge.get_rect(topleft=(20,25))
        screen.blit(level_gosterge,level_rect)

    def skor_goster(self):
        skor_gosterge=self.font.render(f'SKOR :{self.skor}',False,'white')
        skor_rect=skor_gosterge.get_rect(topright=(screen_w-20,-10))
        screen.blit(skor_gosterge,skor_rect)
        high_skor_gosterge=self.font.render(f'HS :{self.high_score}',False,'white')
        high_skor_rect=high_skor_gosterge.get_rect(topright=(screen_w-20,20))
        screen.blit(high_skor_gosterge,high_skor_rect)

    def win_lose(self):
        if not (self.level == 10)and(self.kahraman_can!=0):
            if not self.mahlukatlar.sprites():
                    self.level += 1
                    print(self.level)
                    self.kahraman_can+=1
                    print(self.kahraman_can)
                    self.can_kontrol()
                    self.mahlukat_yon*=1.2
                    self.mahlukat_yon*=1.2
                    if self.satir<=10:    #her seviyedeki mahlukat sayisini arttirma
                        self.satir*=1.2
                        self.sutun*=1.2
                    self.mahlukat_yarat(int(self.satir),int(self.sutun))
        else:
            self.post_screen()
            if self.skor > self.high_score:
                self.high_score = self.skor
                with open('skor.txt', 'w') as file:
                    file.write(str(self.high_score))

    def post_screen(self):

        if self.kahraman_can==0 or self.mahlukat_carpti==True:
            lose_ekran = self.font.render("Oyun Bitti :( !", False, "white")
            lose_rect = lose_ekran.get_rect(center=(screen_w / 2, screen_h / 2))
            screen.blit(lose_ekran, lose_rect)
            if (self.skor < self.high_score):
                skor_gosterge = self.font.render(f'SKOR :{self.skor}', False, 'white')
                skor_rect = skor_gosterge.get_rect(center=(screen_w / 2, screen_h / 3))
                screen.blit(skor_gosterge, skor_rect)
            else:
                skor_gosterge = self.font.render(f'YENI REKOR :{self.skor}', False, 'white')
                skor_rect = skor_gosterge.get_rect(center=(screen_w / 2, screen_h / 3))
                screen.blit(skor_gosterge, skor_rect)
        else:
            win_ekran = self.font.render("KAZANDIN !", False, "white")
            win_rect = win_ekran.get_rect(center=(screen_w / 2, screen_h / 2))
            screen.blit(win_ekran, win_rect)
            if(self.skor<self.high_score):
                skor_gosterge = self.font.render(f'SKOR :{self.skor}', False, 'white')
                skor_rect = skor_gosterge.get_rect(center=(screen_w / 2, screen_h / 3))
                screen.blit(skor_gosterge, skor_rect)
            else:
                skor_gosterge = self.font.render(f'YENI REKOR :{self.skor}', False, 'white')
                skor_rect = skor_gosterge.get_rect(center=(screen_w / 2, screen_h / 3))
                screen.blit(skor_gosterge, skor_rect)

    def calistir(self):
        # sprite grupların update ve draw islemleri
        self.kahraman.update()
        self.kahraman.sprite.lazerler.draw(screen)
        self.kahraman.draw(screen)
        self.can_goster()
        self.skor_goster()
        self.level_goster()

        self.mahlukat_lazer.update()
        self.mahlukat_lazer.draw(screen)
        self.mahlukatlar.draw(screen)
        self.mahlukatlar.update(self.mahlukat_yon)
        self.mahlukat_pos_kontrol()

        self.extra_mahlukat_sayac()
        self.extra.draw(screen)
        self.extra.update()

        self.carpisma_kontrol(self.kahraman)
        self.bloklar.draw(screen)

        self.win_lose()
class Arkaplan:
    #arkaplan gozunumlerinin uygulanmasi
    def __init__(self):
        self.arkaplan = pygame.image.load("grafikler/background-black.png")
        self.arkaplan=pygame.transform.scale(self.arkaplan,(screen_w, screen_h)).convert_alpha()

    def goster(self):
        self.arkaplan.set_alpha(randint(55,100))
        self.cizgi()
        screen.blit(self.arkaplan, (0, 0))

    def cizgi(self):   #daha retro bir hava katması icin ekrana yatay cizgiler olusturdum
        cizgi_yukseklik=5
        cizgi_aralik=int(screen_h/cizgi_yukseklik)
        for cizgi in range(cizgi_aralik):
            y_pos=cizgi * cizgi_yukseklik
            pygame.draw.line(self.arkaplan,"black",(0,y_pos),(screen_w,y_pos),1)

    def arkaplanmuzik(self):
        muzik = pygame.mixer.Sound("sesler/arkaplan.mp3")
        muzik.set_volume(0.5)
        muzik.play(loops=-1)

if __name__ == '__main__':

    pygame.init()
    screen_w=1000
    screen_h=768
    screen=pygame.display.set_mode((screen_w,screen_h))
    pygame.display.set_caption("Uzat Mahlukatları")

    clock=pygame.time.Clock()
    game=Game()
    oyun_son = game.oyun_sonu
    arkaplan=Arkaplan()
    Mahlukat_Lazer=pygame.USEREVENT+1
    pygame.time.set_timer(Mahlukat_Lazer,800)
    game.mahlukat_yarat(game.satir, game.sutun)
    arkaplan.arkaplanmuzik()

    while True:
        oyun_son=game.oyun_sonu
        if oyun_son == False:
            game.calistir()
            arkaplan.goster()

            if (game.level == 10):
                game.oyun_sonu = True

            if (game.kahraman_can == 0):
                game.oyun_sonu = True

            if game.skor > game.high_score:   #canli high skor
                game.high_score = game.skor
                with open('skor.txt', 'w+') as file:
                    file.write(str(game.high_score))
                    if (game.skor > game.high_score):
                        game.high_score = game.skor
        else:
            game.post_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game.level == 10 and game.kahraman_can!=0 and game.mahlukat_carpti != True: #Game over ekranında lazerleri durdurduk
                if event.type == Mahlukat_Lazer:
                    if game.level<=4:    #level 5 den sonra atislar 2 li
                        game.mahlukat_ates()
                    else:
                        game.mahlukat_ates()
                        game.mahlukat_ates()


        clock.tick(60)
        pygame.display.flip()

















