#TRABALHO C3, INTEGRANTES: Lucas Xavier, Ana Julia, Luis Otávio.
# ESTE CÓDIGO PODE TER FICADO UM POUCO GRANDE PORQUE ADICIONEI MUITOS COMENTÁRIOS.
# TODAS AS IMAGENS DO JOGADOR, ATAQUES E MAPA EU PEGUEI DA INTERNET.
# AS IMAGENS QUE FICAM NA HUD DO PLAYER E AS IMAGENS DE MENU, GAMEOVER E WIN, EU MESMO FIZ NO PAINT.

#BIBLIOTECAS USADAS:
import arcade
import arcade.gui
import os
import random
import time
import arcade.sound
import pyglet


# VALORES E DEFICIÇÕES INICIAIS DO JOGO:

SPRITE_SCALING_BOX = 0.5
SPRITE_SCALING_PLAYER = 0.2
SPRITE_SCALING_SPELL = 0.05
SPRITE_SCALING_ENEMY = 0.15
SPRITE_SCALING_COIN = 0.5

TILE_SCALING = 0.5
GRID_PIXEL_SIZE = 128
SPRITE_SIZE = int(GRID_PIXEL_SIZE * TILE_SCALING)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
SCREEN_TITLE = "OneLife!"

GRAVITY = 0.5
JUMP_SPEED =  8.1  
MOVEMENT_SPEED = 2.5 
SPELL_SPEED = 13

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
EXPLOSION_TEXTURE_COUNT = 60


#CLASSE QUE CRIA A EXPLOSÃO
class Explosion(arcade.Sprite):
    #INICIALIZAR EXPLOSÃO E CHAMAR "TEXTURE LIST"
    def __init__(self, texture_list):
        super().__init__()
        #TEXTURA INICIAL 0:
        self.current_texture = 0
        self.textures = texture_list
        
        
    #DAR UPDATE NA EXPLOSÃO
    def update(self):
        #A CADA UPDATE (FRAME) A TEXTURA AVANÇA
        self.current_texture += 1
        
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        
        #SE CHEGAR AO FIM DA TEXTURA, A ANIMAÇÃOA ACABA, E A EXPLOSÃO É APAGADA DO JOGO
        else:
            self.remove_from_sprite_lists()


#CLASS DE CRIAÇÃO DE BOTÃO DE QUITAAR
class QuitButton(arcade.gui.UIFlatButton):
    #QUANDO CLICAR, FECHA O JOGO
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()


#CLASSE DE CRIAÇÃO DO PLAYER
class Player(arcade.AnimatedWalkingSprite, arcade.Sprite):
    def __init__(self):
        #INICIALIZANDO OS VALORES DE TEXTURAS
        super().__init__()

        #AQUI SE CRIA LISTAS VAZIAS PARA ADICIONAR DIVERSAS TEXTURAS PARA FAZER A ANIMAÇÃO
        self.stand_right_textures = []
        self.stand_left_textures = []
        self.walk_right_textures = []
        self.walk_left_textures = []
        self.jump_right_textures = []
        self.jump_left_textures = []
        
        
        #COMEÇAR NA TEXTURA DA DIREITA
        self.direction = TEXTURE_RIGHT

        #TEXTURAS DO JOGADOR PARADO
        self.stand_right_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/1_IDLE_000.png"))
        self.stand_left_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/1_IDLE_000.png", flipped_horizontally= True))
        
        
        #TEXTURAS DO JOGADOR ANDANDO PARA DIREITA
        self.walk_right_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/3_RUN_000.png"))
        self.walk_right_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/3_RUN_001.png"))
        self.walk_right_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/3_RUN_002.png"))
        # self.walk_right_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/3_RUN_003.png"))d
        self.walk_right_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/3_RUN_004.png"))
        
        
        
        #TEXTURAS DO JOGADOR ANDANDO PARA ESQUERDA
        self.walk_left_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/3_RUN_000.png", flipped_horizontally= True))
        self.walk_left_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/3_RUN_001.png", flipped_horizontally= True))
        self.walk_left_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/3_RUN_002.png", flipped_horizontally= True))
        # self.walk_left_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/3_RUN_003.png", flipped_horizontally= True))
        self.walk_left_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/3_RUN_004.png", flipped_horizontally= True))


        #TEXTURAS DO JOGADOR PULANDO PARA ESQUERDA E DIREITA
        self.jump_left_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/4_JUMP_002.png", flipped_horizontally= True))
        self.jump_right_textures.append(arcade.load_texture(r"./PLAYER/PNG/wizard_fire/4_JUMP_002.png"))

        self.scale = SPRITE_SCALING_PLAYER

        #DEFINE ANIMAÇÃO PADRÃO COMO PARADO PARA DIREITA
        self.texture = self.stand_right_textures[0]
        self.set_hit_box(self.texture.hit_box_points)
        
        
    #DEF DE UPDATE DA ANIMAÇÃO (60FPS)
    def update_animation(self, delta_time: float = 1/60):
        #SE ELE NÃO ESTÁ PULANDO:
        if self.change_y == 0:
            if self.change_x < 0:
                #SE ANDA PRA ESQUERDA, RODA A LISTA DE TEXTURAS DA ESQUERDA PARA FAZER A ANIMAÇÃO
                self.texture = self.walk_left_textures[self.cur_texture_index]
                self.direction = TEXTURE_LEFT
            elif self.change_x > 0:
                #SE ANDA PRA DIREITA, RODA A LISTA DE TEXTURAS DA DIREITA PARA FAZER A ANIMAÇÃO
                self.texture = self.walk_right_textures[self.cur_texture_index]
                self.direction = TEXTURE_RIGHT
            else:
                #SE NÃO SE MOVE, FICA COM A TEXTURA PARADA, DEPENDENDO DE ONDE ESTÁ OLHANDO (DIRETA E ESQUERDA)
                if self.texture in self.walk_left_textures:
                    self.texture = self.stand_left_textures[0]
                else:
                    self.texture = self.stand_right_textures[0]
                    
        else:
            #SE ESTÁ PULANDO:
            if self.change_x < 0:
                #SE PULA PRA ESQUERDA, ANIMA O PULO PRA ESQUERDA, MESMA COISA PARA O PRÓXIMO ELIF
                self.texture = self.jump_left_textures[0]
                self.direction = TEXTURE_LEFT
            elif self.change_x > 0:
                self.texture = self.jump_right_textures[0]
                self.direction = TEXTURE_RIGHT
            elif self.change_x == 0:
                #SE PULA PARADO, FICA COM A TEXTURA DE PULO VIRADA PRA ONDE O JOGADOR TÁ OLHANDO
                if self.direction == TEXTURE_LEFT:
                    self.texture = self.jump_left_textures[0]
                    self.direction = TEXTURE_LEFT
                elif self.direction == TEXTURE_RIGHT:
                    self.texture = self.jump_right_textures[0]
                    self.direction = TEXTURE_RIGHT
                    

        super().update_animation(delta_time=delta_time)
        #ATUALIZA A ANIMAÇÃO EM 60FPS

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.update_animation()
        #ATUALIZA A ANIMAÇÃO E A MOVIMENTAÇÃO DO JOGADOR



class MenuView(arcade.View):
    #CLASSE CRIADA PARA CRIAR O MENU INICIAL (CAPA DO JOGO)
    
    def __init__(self):
        #DEF INIT PARA INICIALIZAR AS VARIAVEIS
        
        super().__init__()
        #INICIA BACKGROUND
        self.textureback = arcade.load_texture(r"./IMG/6054585.jpg")
        
        #INICIA TITULO DO GAME
        self.texture = arcade.load_texture(r"./IMG/titulo deinitivo.png")
        
        #INICIA O BOTAO DE START
        self.start_button_texture = arcade.load_texture(r"./IMG/start1.png")
        
        #INICIA O BOTAO DE QUITAR
        self.quit_button_texture = arcade.load_texture(r"./IMG/exit.png")
        
        #INICIA A POSIÇÃO DOS BOTOES
        self.start_button_pos = None
        self.quit_button_pos = None
        
        #INICIA A MUSICA
        music = arcade.sound.load_sound(":resources:music/funkyrobot.mp3")
        arcade.sound.play_sound(music)
        

    def on_resize(self, width: float, height: float):
        #QUANDO A TELA FOR AUMENTADA OU DIMINUIDA, AJUSTA A POSIÇÃO DOS BOTOES
        super().on_resize(width, height)
        self.start_button_pos = (self.window.width / 2, self.window.height / 2 - 110)
        self.quit_button_pos = (self.window.width / 2, self.window.height / 2 - 190)


    def on_draw(self):
        #PARA DESENHAR NA TELA:
        
        arcade.start_render()
        
        #DESENHA O TITULO E O BACKGROUND
        self.textureback.draw_sized(self.window.width / 2, self.window.height / 2, self.window.width, self.window.height)
        self.texture.draw_sized(self.window.width / 2, self.window.height / 2 + 140, 650, 450)
        
        #DESENHA O BOTAO DE START (X, Y, WIDTH, HEIGHT, TEXTURA)
        arcade.draw_texture_rectangle(
            self.start_button_pos[0], self.start_button_pos[1], self.start_button_texture.width, self.start_button_texture.height, self.start_button_texture
        )
        
        # DESENHA BOTAO DE QUITAR
        arcade.draw_texture_rectangle(
            self.quit_button_pos[0], self.quit_button_pos[1], self.quit_button_texture.width, self.quit_button_texture.height, self.quit_button_texture
        )
        

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # QUANDO O MOUSE É USADO
        if (
            # AQUI TIVE QUE DIZER ONDE O MOUSE PRECISARIA SER CLICADO PARA INICIAR O JOGO
            self.start_button_pos[0] - self.start_button_texture.width / 2 <= x <= self.start_button_pos[0] + self.start_button_texture.width / 2
            and self.start_button_pos[1] - self.start_button_texture.height / 2 <= y <= self.start_button_pos[1] + self.start_button_texture.height / 2
        ):
            # SE FOR CLICADO, INICIA O JOGO CHAMANDO A CLASSE "GAMEVIEW",  CHAMA A DEF "SETUP" E MOSTRA A TELA DE GAMEVIEW
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
            
            
        elif (
            # AQUI TIVE QUE DIZER ONDE O MOUSE PRECISARIA SER CLICADO PARA QUITAR DO JOGO
            self.quit_button_pos[0] - self.quit_button_texture.width / 2 <= x <= self.quit_button_pos[0] + self.quit_button_texture.width / 2
            and self.quit_button_pos[1] - self.quit_button_texture.height / 2 <= y <= self.quit_button_pos[1] + self.quit_button_texture.height / 2
        ):
            # SE OR CLICADO, FECHA O JOGO
            arcade.close_window()
        


class GameView(arcade.View):
    # CRIAÇÃO DA CLASSE PRINCIPAL (JOGO EM SI)
    def __init__(self):
        # PARA INICIALIZAR AS VARIAVEIS
        super().__init__()
        
        # CRIANDO LISTAS PARA ARMAZENAR PLAYER, PAREDES, PODERES, INIMIGOS E ETC...
        self.player_list = None
        self.wall_list = None
        self.dec_list = None
        self.spell_list = None
        self.explosion_list = None
        self.enemy_list = None
        self.coin_list = None
        
        # TODAS AS VARIAVEIS DEFINIDAS COMO "NONE", SÃO APENAS DE INICIALIZAÇÃO, MAIS PRA FRENTE RECEBERÃO VALORES E ATRIBUTOS
        
        # TODAS AS VARIAVEIS DEFINIDAS COMO "FALSE", SÃO APENAS DE INICIALIZAÇÃO, MAIS PRA FRENTE RECEBERÃO MODIFICAÇÕES QUANDO FOREM ATIVADAS
        
        # HUD DO JOGADOR
        self.hud_image = None
        self.hud_image2 = None
        
        # JOGADOR EM SI
        self.player_sprite = None
        
        # FISICA DO JOGO (GRAVIDADE, NÃO ATRAVESSAR BLOCOS, ETC...)
        self.physics_engine = None
        
        # SE TAL TECLA FOR APERTADA
        self.a_pressed = False
        self.d_pressed = False
        self.shift_pressed = False
        
        # GOD MODE (FICA IMORTAL, 2X VELOCIDADE, 2X PULO, SEM COOLDOWN)
        # COLOQUEI PARA DIVERSÃO, E PARA TESTES
        self.god_mode = False
        
        # PARA CRIAR GAME OVER, PAUSE E VITÓRIA
        # TIVE QUE CRIAR GAMEOVER 1 E 2, PARA MOSTRAR DIFERENTES IMAGENS AO MORRER (1 MORTE POR INIMIGO, 2 MORTE POR ESPINHOS)
        self.paused = False
        self.game_over = False
        self.game_over2 = False
        self.win = False
        
        # PONTUAÇÃO DE MOEDAS E KILLS INICIADAS COMO 0
        self.score = 0
        self.kills = 0
        
        # CAMERA QUE SEGUE JOGADOR E HUD
        self.camera_sprite = None
        self.camera_gui = None
        
        # VARIAVEIS PARA CRIAR COOLDOWN DA BOLA DE FOGO
        self.last_shot_time = 0.0
        self.last_sound_time = 0.0
        
        # CARREGUEI O BACKGROUND
        self.background_texture = arcade.load_texture(r"./IMG/6054585.jpg")
        
        # CRIANDO LISTA PARA ADICIONAR TEXTURA DA EXPLOSÃO
        self.explosion_texture_list = []
        columns = 16
        count = 400
        sprite_width = 256
        sprite_height = 256
        file_name = ":resources:images/spritesheets/explosion.png"
        self.explosion_texture_list = arcade.load_spritesheet(file_name, sprite_width, sprite_height, columns, count)
        
        
        

    # CONFIGURAÇÕES DO JOGO:
    def setup(self):
        # DEFININDO LISTAS DE VARIAVEIS COMO SPRITES (IMAGENS):
        
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.dec_list = arcade.SpriteList()
        self.spell_list = arcade.SpriteList()
        self.explosions_list = arcade.SpriteList()
        self.explosion_list = []
        self.enemy_list = arcade.SpriteList()
        self.coin_list = arcade.Sprite()
        
        # COLOCANDO OS DIVERSOS SONS DO JOGO:
        
        self.jump_sound = pyglet.media.load(r"./SOM/fast-simple-chop-5-6270.mp3")
        self.player = pyglet.media.Player()
        
        self.hit_sound1 = arcade.load_sound(r"./SOM/supernatural-explosion-104295.mp3")
        
        self.spell_sound = arcade.load_sound(r"./SOM/lighting-a-fire-14421.mp3")
        
        self.coin_sound = arcade.Sound(r"./SOM/mario-money.mp3")
        
        self.death_sound = arcade.load_sound(r"./SOM/male_hurt7-48124.mp3")
        
        self.win_sound = arcade.load_sound(r"./SOM/success-fanfare-trumpets-6185 (3).mp3")
        
        
        #COLOCANDO AS DIVERSAS IMAGENS PARA APARECEREM NA TELA:
        # (HUD DO JOGADOR, TELA DE PAUSE, MORTE, VITÓRIA, QUNADO ESTÁ COM O GODMODE ATIVADO)
        
        self.hud_image = arcade.load_texture(r"./IMG/HUD2.png")
        self.hud_image2 = arcade.load_texture(r"./IMG/HUDcount.png")
        
        self.god_mode_image = arcade.load_texture(r"./IMG/god mode.png")
        
        self.paused_image = arcade.load_texture(r"./IMG/pause.png")
        
        self.game_over_image = arcade.load_texture(r"./IMG/gameover.png")
        self.game_over_image2 = arcade.load_texture(r"./IMG/gameover2.png")
        
        self.win_image = arcade.load_texture(r"./IMG/win.png")
        
        
        # AINDA SIM COMEÇANDO COM A PONTUAÇÃO EM 0 (LÓGICAMENTE KKKK)
        self.score = 0
        self.kills = 0
        
        
        # CONIGURAÇÕES DO JOGADOR:
        
        # CHAMA A CLASSE "PLAYER" QUE JÁ TEM TODAS AS FUNÇÕES DO JOGADOR CRIADAS
        self.player_sprite = Player()   
        # ONDE ELE SPAWNA
        self.player_sprite.center_x = 290
        self.player_sprite.center_y = 600
        # ADICIONA ELE A LISTA DE JOGADORES
        self.player_list.append(self.player_sprite)
        
        # MAPA
        map_name = r"./MAPA/MAPA.tmx"
        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)
        
        # ADICIONA TODAS AS CAMADAS DO MAPA, AO CÓDIGO, E ADICIONA AS CAMADAS AS LISTAS
        self.wall_list = self.tile_map.sprite_lists['Walls']    #CHAO
        self.dec_list = self.tile_map.sprite_lists['decoracao']     
        self.morte_list = self.tile_map.sprite_lists['morte']
        self.coin_list = self.tile_map.sprite_lists['coin']
        self.star_list = self.tile_map.sprite_lists['star']
        self.dec2_list = self.tile_map.sprite_lists['decoracao2']
        self.background_list = self.tile_map.sprite_lists['background']
        self.win_list = self.tile_map.sprite_lists['win']
        
    
        # AS PRÓXIMAS 4 VARIAVEIS DE NOME "ENEMY", SÃO PARA A CRIAÇÃO DE INIMIGOS, POSICIONADOS EM LUGARES DIFERENTES, COM MUDANÇA DE MOVIMENTO, E ADICIONANDO ELES A LISTA DE INIMIGOS
        enemy = arcade.Sprite(r"./PLAYER/Minotaur_1/0_Minotaur_Slashing_011.png", SPRITE_SCALING_ENEMY)
        enemy.bottom = SPRITE_SIZE * 11
        enemy.left = SPRITE_SIZE * 70
        enemy.change_x = 2
        self.enemy_list.append(enemy)
        
        enemy = arcade.Sprite(r"./PLAYER/Minotaur_1/0_Minotaur_Slashing_011.png", SPRITE_SCALING_ENEMY)
        enemy.bottom = SPRITE_SIZE * 18
        enemy.left = SPRITE_SIZE * 71
        enemy.boundary_right = SPRITE_SIZE * 77
        enemy.boundary_left = SPRITE_SIZE * 70
        enemy.change_x = 2
        self.enemy_list.append(enemy)
        
        enemy = arcade.Sprite(r"./PLAYER/Minotaur_1/0_Minotaur_Slashing_011.png", SPRITE_SCALING_ENEMY)
        enemy.bottom = SPRITE_SIZE * 5
        enemy.left = SPRITE_SIZE * 105
        enemy.change_x = 2
        self.enemy_list.append(enemy)
        
        enemy = arcade.Sprite(r"./PLAYER/Minotaur_1/0_Minotaur_Slashing_011.png", SPRITE_SCALING_ENEMY)
        enemy.bottom = SPRITE_SIZE * 17
        enemy.left = SPRITE_SIZE * 166
        enemy.change_x = 2
        self.enemy_list.append(enemy)
        
        
        self.kills = 0
        
        # DEIXANDO O FUNDO TRANSPARENTE, PARA QUE APAREÇA A IMAGEM DE BACKGROUND QUE COLOCAMOS
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
        
        # CRIA A CAMERA COM BASE NO TAMANHO DA JANELA
        self.camera_sprite = arcade.Camera(self.window.width, self.window.height)
        self.camera_gui = arcade.Camera(self.window.width, self.window.height)
        
        # CONFIGURA A FISICA DAS PAREDES E GRAVIDADE, COMO DITO ANTERIORMENTE
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.wall_list, gravity_constant=GRAVITY
        )
        
        
        
    # DEF PARA DESENHAR TUDO NA TELA
    def on_draw(self):
        
        # SE DER GAME OVER, TELA DE GAME OVER DESENHADA NA TELA
        if self.game_over2:
            arcade.draw_texture_rectangle(
            self.window.width / 2, self.window.height / 2, self.game_over_image2.width, self.game_over_image2.height, self.game_over_image2
            )
        
        # SE DER GAME OVER, TELA DE GAME OVER DESENHADA NA TELA
        elif self.game_over:
            arcade.draw_texture_rectangle(
            self.window.width / 2, self.window.height / 2, self.game_over_image.width, self.game_over_image.height, self.game_over_image
            )
            
        # SE O JOGADOR GANHAR, TELA DE VITÓRIA DESENHADA NA TELA
        elif self.win:
            arcade.draw_texture_rectangle(
            self.window.width / 2, self.window.height / 2, self.win_image.width, self.win_image.height, self.win_image
            )
            
        
        # SE O JOGO ESTIVER NORMAL (SEM GAME OVER OU VITÓRIA):
        elif self.game_over == False and self.game_over2 == False and self.win == False:
            
        
            # SE O JOGO FOR PAUSADO, A TELA DE PAUSE APARECE
            if self.paused:
                arcade.draw_texture_rectangle(
                self.window.width / 2, self.window.height / 2, self.paused_image.width, self.paused_image.height, self.paused_image
            )
            
            
            # SE O JOGO ESTIVER SEM PAUSE, GAME OVER, OU VITÓRIA, ELE RODARÁ TUDO:
            elif not self.paused and self.game_over == False and self.game_over2 == False and self.win == False:
            
                arcade.start_render()
                
                arcade.draw_lrwh_rectangle_textured(0, 0, self.window.width, self.window.height, self.background_texture)
                
                # DEINE A CAMERA
                self.camera_sprite.use()
                
                # DESENHA A LISTA DE SPRITES
                
                self.background_list.draw()
                self.coin_list.draw()
                self.wall_list.draw()
                self.dec2_list.draw()
                self.dec_list.draw()
                self.win_list.draw()
                self.star_list.draw()
                self.morte_list.draw()
                self.player_list.draw()
                self.spell_list.draw()
                self.explosions_list.draw()
                self.enemy_list.draw()
                
                # DESENHA AS EXPLOSÕES
                for explosion in self.explosion_list:
                    explosion.draw()
                
            
                self.camera_gui.use()
                
                # DESENHA A HUD DO JOGADOR
                image_width = 280
                image_height = 150

                x = 135
                y = 80

                arcade.draw_texture_rectangle(155, 80, image_width, image_height, self.hud_image,)
                arcade.draw_texture_rectangle(350, 80, 90, 145, self.hud_image2)
                
                arcade.draw_text(self.score, 360, 105, arcade.color.BLACK, 18)
                arcade.draw_text(self.kills, 360, 30, arcade.color.BLACK, 18)
                
                if self.god_mode:
                    arcade.draw_texture_rectangle(100, 250, 200, 200, self.god_mode_image)
                    
        
        
    # SE ALGUMA TECLA FOR PRESSIONADA
    def on_key_press(self, key, modifiers):
        
        # PAUSA OU DESPAUSA (SE ESTIVER PAUSADO, TRAVA O MOVIMENTO DO JOGADOR)
        if key == arcade.key.ESCAPE:
            self.paused = not self.paused
        
        # SE ESTIVER PAUSADO E CLICAR ENTER, REINCIA
        if self.paused:
            if key == arcade.key.ENTER:
                self.setup()
                self.paused = False
                
            # SE ESTIVER PAUSADO E CLICAR G, ENTRA OU SAI DO GODMODE
            elif self.god_mode == True:
                if key == arcade.key.G:
                    self.god_mode = False
                    self.paused = not self.paused
            
            elif key == arcade.key.G:
                self.god_mode = True
                self.paused = not self.paused
                
        
        # SE DER GAMEOVER E CLICAR ENTER RENICIA, SE CLICAR ESC, FECHA O JOGO
        if self.game_over:
            if key == arcade.key.ENTER:
                self.setup()
                self.game_over = False
                
            elif key == arcade.key.ESCAPE:
                arcade.exit()
                
                
        # SE DER GAMEOVER E CLICAR ENTER RENICIA, SE CLICAR ESC, FECHA O JOGO
        if self.game_over2:
            if key == arcade.key.ENTER:
                self.setup()
                self.game_over2 = False
                
            elif key == arcade.key.ESCAPE:
                arcade.exit()
                
                
        # SE O JOGADOR GANHAR E CLICAR ENTER RENICIA, SE CLICAR ESC, FECHA O JOGO
        if self.win:
            if key == arcade.key.ENTER:
                self.setup()
                self.win = False
                
            elif key == arcade.key.ESCAPE:
                arcade.exit()
            
            
        # SE ESTÁ DESPAUSADO, SEM GAMEOVER OU VITÓRIA, O JOGO RODA NORMALMENTE (DESTRAVA O MOVIMENTO)
        if self.game_over == False and self.game_over2 == False and self.win == False:
            if not self.paused:
            
                # SE CLICA SPACO OU SETA PRA CIMA PULA, TIVE QUE USAR FUNÇÕES PARA INDENTIICAR SE O JOGADOR ESTÁ NO CHÃO PARA PULAR DENOVO
                if key == arcade.key.SPACE or key == arcade.key.UP:
                    
                    # SE ESTÁ NO GODMODE, PULO DUPLO
                    if self.god_mode:
                        if self.physics_engine.can_jump():
                            self.player_sprite.change_y = JUMP_SPEED + 4
                            self.player.queue(self.jump_sound)
                            self.player.volume = 5000 
                            self.player.play()
                            
                    # SE NÃO ESTÁ, PULO NORMAL
                    else:
                        if self.physics_engine.can_jump():
                            self.player_sprite.change_y = JUMP_SPEED
                            self.player.queue(self.jump_sound)
                            self.player.volume = 5000 
                            self.player.play()
                        
                        
                # SE CLICAR TAL TECLA, ATIVA AS SEGUINTES FUNÇÕES DE MOVIMENTO (SERÃO MOSTRADAS MAIS A FRENTE)
                elif key == arcade.key.A or key == arcade.key.LEFT:
                    self.a_pressed = True
                    
                elif key == arcade.key.D or key == arcade.key.RIGHT:
                    self.d_pressed = True
                    
                elif key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
                    self.shift_pressed = True
                    
                    
                # SE CLICA X, ATIRA A BOLA DE FOGO
                elif key == arcade.key.X or key == arcade.key.L:
                    current_time = time.time()
                    
                    # SE ESTIVER EM GODMODE, NÃO TEM COOLDOWN
                    if self.god_mode:
                        spell = arcade.Sprite(
                            r"./IMG/Fireball-PNG-Download-Image.png",
                            SPRITE_SCALING_SPELL * 2
                        )

                        # SE O JOGADOR OLHAR PARA ESQUERDA, O TIRO SAI PRA ESQUERDA, E VICE VERSA
                        if self.player_sprite.direction == TEXTURE_LEFT:
                            spell.change_x = -SPELL_SPEED - 13
                            spell.center_x = self.player_sprite.center_x - 40
                            spell.center_y = self.player_sprite.center_y + 10
                            
                            
                        elif self.player_sprite.direction == TEXTURE_RIGHT:
                            spell.change_x = SPELL_SPEED + 13
                            spell.center_x = self.player_sprite.center_x + 40
                            spell.center_y = self.player_sprite.center_y + 10
                            spell.angle = 180
                            
                        # ATIVA SOM DA BOLA DE OGO
                        self.spell_sound.play()

                        # ADICIONA O FEITIÇO A LISTA
                        self.spell_list.append(spell)
                        self.last_shot_time = current_time
                    
                    
                    # CRIA UM COOLDOWN QUE VERIFICA SE PASSOU DOIS SEGUNDOS DESDE O ULTIMO TIRO, PARA PODER ATIRAR NOVAMENTE (COOLDOWN DE 2 SEC)
                    elif current_time - self.last_shot_time >= 2.0:  
                        spell = arcade.Sprite(
                            r"./IMG/Fireball-PNG-Download-Image.png",
                            SPRITE_SCALING_SPELL
                        )

                        if self.player_sprite.direction == TEXTURE_LEFT:
                            spell.change_x = -SPELL_SPEED
                            spell.center_x = self.player_sprite.center_x - 40
                            spell.center_y = self.player_sprite.center_y
                            
                            
                        elif self.player_sprite.direction == TEXTURE_RIGHT:
                            spell.change_x = SPELL_SPEED
                            spell.center_x = self.player_sprite.center_x + 40
                            spell.center_y = self.player_sprite.center_y
                            spell.angle = 180
                            
                        self.spell_sound.play()

                        self.spell_list.append(spell)
                        self.last_shot_time = current_time
                                   
                    
                
    # DEF QUE INDENTIFICA AO SOLTAR TECLAS
    def on_key_release(self, key, modifiers):
        
        # SE SOLTAR TECLAS, DESATIVA TAL FUNÇÃO (DE MOVIMENTO)
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.a_pressed = False
            
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.d_pressed = False
            
        elif key == arcade.key.LSHIFT or key == arcade.key.RSHIFT:
            self.shift_pressed = False
            
            
    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        # AJUSTA A FUNÇÃO AO ALTERAR TAMANHO DA TELA
        self.camera_sprite.resize(self.window.width, self.window.height)
        self.camera_gui.resize(self.window.width, self.window.height)
        
        
        # MOVE A CAMERA PARA SEGUIR O JOGADOR
        lower_left_corner = (
            self.player_sprite.center_x - self.window.width / 2,
            self.player_sprite.center_y - self.window.height / 2
        )
        self.camera_sprite.move_to(lower_left_corner)



    # FUNÇÃO QUE ATUALIZA O JOGO TODO, SE NÃO TIVER, O JOGO FICA PARADO
    def on_update(self, delta_time):  
        
        # SE NÃO ESTIVER PAUSADO, EM GAME OUVER OU VITÓRIA, RODA NORMALMENTE
        if self.game_over == False and self.game_over2 == False and self.win == False:
        
            if not self.paused:
                # ATUALIZA AS LISTAS:
                self.physics_engine.update()
                self.player_list.update()
                self.spell_list.update()
                self.explosions_list.update()
                self.enemy_list.update()
                
                for explosion in self.explosion_list:
                    explosion.update()
                    
                
                for enemy in self.enemy_list:
                    # RESUMINDO, SE O INIMIGO ENCOSTAR NUMA PAREDE, ELE VOLTA, E ENTRA NUM LOOP (OU SE ELE CHEGAR A UMA POSIÇÃO ESPECIFICA)
                    if len(arcade.check_for_collision_with_list(enemy, self.wall_list)) > 0:
                        enemy.change_x *= -1
                        if enemy.change_x > 0:
                            self.direction = TEXTURE_RIGHT
                            if self.direction == TEXTURE_RIGHT:
                                enemy.texture = arcade.load_texture(r"./PLAYER/Minotaur_1/0_Minotaur_Slashing_011.png")
                                
                        else:
                            self.direction = TEXTURE_LEFT
                            if self.direction == TEXTURE_LEFT:
                                enemy.texture = arcade.load_texture(r"./PLAYER/Minotaur_1/0_Minotaur_Slashing_011.png", flipped_horizontally= True)
                        
                        
                    elif enemy.boundary_left is not None and enemy.left < enemy.boundary_left:
                        enemy.change_x *= -1
                        if enemy.change_x > 0:
                            self.direction = TEXTURE_RIGHT
                            if self.direction == TEXTURE_RIGHT:
                                enemy.texture = arcade.load_texture(r"./PLAYER/Minotaur_1/0_Minotaur_Slashing_011.png")
                                
                        else:
                            self.direction = TEXTURE_LEFT
                            if self.direction == TEXTURE_LEFT:
                                enemy.texture = arcade.load_texture(r"./PLAYER/Minotaur_1/0_Minotaur_Slashing_011.png", flipped_horizontally= True)
                        
                        
                    elif enemy.boundary_right is not None and enemy.right > enemy.boundary_right:
                        enemy.change_x *= -1
                        if enemy.change_x > 0:
                            self.direction = TEXTURE_RIGHT
                            if self.direction == TEXTURE_RIGHT:
                                enemy.texture = arcade.load_texture(r"./PLAYER/Minotaur_1/0_Minotaur_Slashing_011.png")
                                
                        else:
                            self.direction = TEXTURE_LEFT
                            if self.direction == TEXTURE_LEFT:
                                enemy.texture = arcade.load_texture(r"./PLAYER/Minotaur_1/0_Minotaur_Slashing_011.png", flipped_horizontally= True)
                
                
                # CRIA UMA VARIAVEL PARA DIZER SE O JOGADOR ENCOSTOU NA MOEDA
                coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                    self.coin_list) 
                
                # A CADA MOEDA ENCOSTADA, ELA SOME, AUMENTA A PONTUAÇÃO, E FAZ UM SOM
                for coin in coins_hit_list:
                    coin.remove_from_sprite_lists() 
                    self.score += 1 
                    self.coin_sound.play()
                    
                    
                # MESMA COISA DA MOEDA, SÓ QUE É UMA MOEDA ESPECIAL
                stars_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                                    self.star_list)  
                
                for star in stars_hit_list:
                    star.remove_from_sprite_lists() 
                    self.score += 10
                    for _ in range(10):
                        self.coin_sound.play()
                    
                    
                # ATUALIZA O PLAYER
                for player in self.player_list:
                    player.update()


                for spell in self.spell_list:
                    # CRIA VARIAVEL PARA DIZER SE O FEITIÇO ENCOSTOU NUMA PAREDE
                    hit_list = arcade.check_for_collision_with_list(spell, self.wall_list)

                    # SE ENCOSTOU NA PAREDE, CRIA EXPLOSÃO, O TIRO SOME, E FAZ SOM DA EXPLOSÃO
                    if len(hit_list) > 0:
                        explosion = Explosion(self.explosion_texture_list)
                        explosion.center_x = hit_list[0].center_x
                        explosion.center_y = hit_list[0].center_y
                        explosion.update()
                        self.explosions_list.append(explosion)
                        self.hit_sound1.play()
                        spell.remove_from_sprite_lists()
            
                    spell.center_x += spell.change_x * delta_time
                    
                
                for spell in self.spell_list:
                    # CRIA VARIAVEL SE O FEITIÇO ATINGIR INIMIGO
                    hit_enemies = arcade.check_for_collision_with_list(spell, self.enemy_list)
                    # MESMA COISA QUE SE ENCOSTAR NA PAREDE, MAS TAMMBÉM MATA O INIMIGO, E GANHA PONTOS DE KILL
                    for enemy in hit_enemies:
                        
                        explosion = Explosion(self.explosion_texture_list)
                        explosion.center_x = enemy.center_x
                        explosion.center_y = enemy.center_y
                        self.explosion_list.append(explosion)
                        self.hit_sound1.play()
                        
                        self.coin = arcade.Sprite(r"./IMG/coinGold.png", SPRITE_SCALING_COIN)
                        
                        
                        #ADICIONA UMA MOEDA QUANDO O INIMIGO MORRE
                        self.coin.center_x = enemy.center_x
                        self.coin.center_y = enemy.center_y
                                                
                        self.coin_list.append(self.coin)
                        
                        enemy.remove_from_sprite_lists()
                        
                       
                        spell.remove_from_sprite_lists()                    
                       
                        self.kills += 1
                        
                        
                if self.god_mode:
                    for player in self.player_list:
                        # CRIA VARIAVEL SE O FEITIÇO ATINGIR INIMIGO
                        hit_enemies = arcade.check_for_collision_with_list(player, self.enemy_list)
                        # MESMA COISA QUE SE ENCOSTAR NA PAREDE, MAS TAMMBÉM MATA O INIMIGO, E GANHA PONTOS DE KILL
                        for enemy in hit_enemies:
                            
                            explosion = Explosion(self.explosion_texture_list)
                            explosion.center_x = enemy.center_x
                            explosion.center_y = enemy.center_y
                            self.explosion_list.append(explosion)
                            self.hit_sound1.play()
                            
                            self.coin = arcade.Sprite(r"./IMG/coinGold.png", SPRITE_SCALING_COIN)
                            
                            
                            #ADICIONA UMA MOEDA QUANDO O INIMIGO MORRE
                            self.coin.center_x = enemy.center_x
                            self.coin.center_y = enemy.center_y
                                                    
                            self.coin_list.append(self.coin)
                            
                            enemy.remove_from_sprite_lists()
                                              
                        
                            self.kills += 1


                # MOVIMENTO DA CAMERA
                camera_speed = 1
                lower_left_corner = (
                    self.player_sprite.center_x - self.window.width / 2,
                    self.player_sprite.center_y - self.window.height / 2
                )
                
                map_left_limit = 0
                map_right_limit = (self.tile_map.width * GRID_PIXEL_SIZE) - 12800
                map_bottom_limit = 0
                map_top_limit = self.tile_map.height * GRID_PIXEL_SIZE
                
                
                # SE PRECISAR MUDA A POSIÇÃO DA CAMERA
                if lower_left_corner[0] < map_left_limit:
                    lower_left_corner = (map_left_limit, lower_left_corner[1])
                elif lower_left_corner[0] > map_right_limit - self.window.width:
                    lower_left_corner = (map_right_limit - self.window.width, lower_left_corner[1])
                
                
                if lower_left_corner[1] < map_bottom_limit:
                    lower_left_corner = (lower_left_corner[0], map_bottom_limit)
                elif lower_left_corner[1] > map_top_limit - self.window.height:
                    lower_left_corner = (lower_left_corner[0], map_top_limit - self.window.height)
            
                self.camera_sprite.move_to(lower_left_corner, camera_speed)
                
            
                # AGORA VOLTAMOS AS VARIAVEIS DE MOVIMENTO, QUE SE SÃO ATIVADAS, FAZ O JOGADOR ANDAR
                # TIVE QUE SEPARAR O MOVIMENTO EM ALGUMAS PARTES, POIS SEM ISSO, O MOVIMENTO ESTAVA BUGADO E LIMITADO
                self.player_sprite.change_x = 0
                if self.a_pressed and not self.d_pressed:
                    self.player_sprite.change_x = -MOVEMENT_SPEED
                elif self.d_pressed and not self.a_pressed:
                    self.player_sprite.change_x = MOVEMENT_SPEED
                    
                    
                # NÃO DEIXA O JOGADOR ATRAVESSAR O LIMITE DO MAPA
                if self.player_sprite.left < map_left_limit:
                    self.player_sprite.left = map_left_limit
                elif self.player_sprite.right > map_right_limit:
                    self.player_sprite.right = map_right_limit
            
            
                if self.player_sprite.bottom < map_bottom_limit:
                    self.player_sprite.bottom = map_bottom_limit            
                elif self.player_sprite.top > map_top_limit:
                    self.player_sprite.top = map_top_limit
                    
                # SE ESTÁ EM GODMODE, X2 DE VELOCIDADE
                if self.god_mode:
                    self.player_sprite.change_x *= 2
                    
                if self.shift_pressed:
                    self.player_sprite.change_x *= 1.5
                
                # ATUALIZA A ANIMAÇÃO DO JOGADOR
                self.player_sprite.update_animation(delta_time)
            
            # SE ESTÁ EM GODMODE, FICA BASICAMENTE IMORTAL, PRECISANDO DE 100000 HITS PRA MORRER
            if self.god_mode:
                if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) > 100000:
                    self.game_over = True
                    
                elif len(arcade.check_for_collision_with_list(self.player_sprite, self.morte_list)) > 100000:
                    self.game_over2 = True
                    
                elif len(arcade.check_for_collision_with_list(self.player_sprite, self.win_list)) == 1:
                    self.win_sound.play()
                    self.win = True
                
            # SE NÃO ESTIVER EM GODMODE
            else:
                
                # SE ENCOSTAR NO INIMIGO, ATIVA O GAMEOVER E FAZ SOM DE MORTE
                if len(arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)) == 1:
                    self.death_sound.play()
                    self.game_over = True
                    
                # SE ENCOSTAR NO ESPINHO, ATIVA O GAMEOVER E FAZ SOM DE MORTE
                elif len(arcade.check_for_collision_with_list(self.player_sprite, self.morte_list)) > 0:
                    self.death_sound.play()
                    self.game_over2 = True
                    
                # SE CHEGAR NO PONTO DE VITÓRIA, APARECE A TELA DE VITÓRIA E FAZ SOM
                elif len(arcade.check_for_collision_with_list(self.player_sprite, self.win_list)) == 1:
                    self.win_sound.play()
                    self.win = True
                    

        
        
def main():
    # CRIA DEINIÇÃO PRINCIPAL, PARA INICIAR JOGO
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
    start_view = MenuView()
    window.show_view(start_view)
    arcade.run()
 
# SÓ PRA CRIAR UMA CONDIÇÃO QUALQUER PARA INICIAR O JOGO
if __name__ == "__main__":
    main()