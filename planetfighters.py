from pygame import *
init()
from random import *
from button import Button
screen = display.set_mode((1280, 720), FULLSCREEN)
display.set_caption('Planet Fighters')
screen.fill((0, 0, 0)) 

class Objeto(sprite.Sprite):
	def __init__(self, x, y, ancho, largo, direccionx, direcciony, puntuacion, color, vidas, team):
		sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.ancho = ancho
		self.largo = largo
		self.direccionx = direccionx
		self.direcciony = direcciony
		self.puntuacion = puntuacion
		self.color = color
		self.vidas = vidas
		self.team = team

	def DibujarObjeto(self):
		draw.rect(screen, self.color, (self.x,self.y,self.ancho,self.largo))

	def check_colisiones(sprite1, sprite2):
		xsprite1 = sprite1.x
		ysprite1 = sprite1.y
		anchosprite1 = sprite1.ancho
		largosprite1 = sprite1.largo
		xsprite2 = sprite2.x
		ysprite2 = sprite2.y
		anchosprite2 = sprite2.ancho
		largosprite2 = sprite2.largo
		if (ysprite1 + largosprite1) > ysprite2 and ysprite1 < (ysprite2 + largosprite2) and (xsprite1 + anchosprite1) > xsprite2 and xsprite1 < (xsprite2 + anchosprite2):
			return True

class Bola(Objeto):
	def __init__(self, x, y, ancho, largo, direccionx, direcciony, puntuacion, color, vidas, team):
		Objeto.__init__(self, x, y, ancho, largo, direccionx, direcciony, puntuacion, color, vidas, team)
	
	def Movimiento(self, enemigo):
			#TOCA EL BORDE
			if self.x <= 15:
				self.direccionx = 1
			elif self.x >= 1280-self.ancho:
				self.direccionx = -1
			if self.y <= 0:
				self.direcciony = 1
			elif self.y >= 720-self.largo:
				self.direcciony = -1 
			#MOVIMIENTO
			if self.direccionx == 1:
				self.x = self.x + 0.25
				if self.direcciony == -1:
					self.y = self.y - 0.25
				else:
					self.y = self.y + 0.25
			elif self.direccionx == -1:
				self.x = self.x - 0.25
				if self.direcciony == -1:
					self.y = self.y - 0.25
				else:
					self.y = self.y + 0.25
			self.DibujarObjeto()

	def MovimientoTeledirigido(self, enemigo):
			#TOCA EL BORDE
			if self.x <= enemigo.x:
				self.direccionx = 1
			elif self.x >= enemigo.x:
				self.direccionx = -1
			if self.y <= enemigo.y:
				self.direcciony = 1
			elif self.y >= enemigo.y:
				self.direcciony = -1 
			#MOVIMIENTO
			if self.direccionx == 1:
				self.x = self.x + 0.1875
				if self.direcciony == -1:
					self.y = self.y - 0.1875
				else:
					self.y = self.y + 0.1875
			elif self.direccionx == -1:
				self.x = self.x - 0.1875
				if self.direcciony == -1:
					self.y = self.y - 0.1875
				else:
					self.y = self.y + 0.1875
			self.DibujarObjeto()
	
	def Movimiento_Diamante(self, enemigo):
		if self.check_colisiones(enemigo):
			enemigo.vidas -= 1
			self.y = -100
		if self.y < 750:
			if self.y == -100:
				self.x = randrange(1, 13) * 100
				neptuno_sound.play()
			self.y += 0.25
		if self.y >= 750:
			self.y = -100
		self.DibujarObjeto()

	#MARTE
	def Disparar(self, enemigo, disparo1, disparo2, disparo3):			
		disparo1.puntuacion += 1
		if enemigo.check_colisiones(disparo1):
			enemigo.vidas -= 1
			disparo1.x = 10000
		if enemigo.check_colisiones(disparo2):
			enemigo.vidas -= 1
			disparo2.x = 10000
		if enemigo.check_colisiones(disparo3):
			enemigo.vidas -= 1
			disparo3.x = 10000            
		if disparo1.puntuacion >= 100 and disparo1.x != 10000:
			disparo1.Movimiento(enemigo)
			if disparo1.puntuacion == 100:
				marte_sound.play()
		if disparo1.puntuacion >= 200 and disparo2.x != 10000:
			disparo2.Movimiento(enemigo)
			if disparo1.puntuacion == 200:
				marte_sound.play()
		if disparo1.puntuacion >= 300 and disparo3.x != 10000:
			disparo3.Movimiento(enemigo)
			if disparo1.puntuacion == 300:
				marte_sound.play()

	#LA TIERRA
	def DispararTeledirigido(self, enemigo, disparo):			
		if enemigo.check_colisiones(disparo):
			enemigo.vidas -= 5
			disparo.x = 10000  
		if disparo.x != 10000:       
			disparo.MovimientoTeledirigido(enemigo)
			if disparo.puntuacion == 0:
				latierra_sound.play()
				disparo.puntuacion = 1

	#VENUS
	def PonerTrampa(self, enemigo, trampa):
		if enemigo.check_colisiones(trampa):
			enemigo.vidas -= 3
			trampa.x = 10000
		if trampa.puntuacion == 0:
			venus_sound.play()
			trampa.puntuacion = 1
		trampa.DibujarObjeto()

	#URANO
	def DispararCongelacion(self, enemigo, disparo):
		if enemigo.check_colisiones(disparo):
			enemigo.vidas -= 3
			disparo.x = 10000
		if disparo.x != 10000:
			disparo.Movimiento(enemigo)
			if disparo.puntuacion == 0:
				urano_sound.play()
				disparo.puntuacion = 1
		else:
			disparo.puntuacion += 1
			disparo.direccionx = enemigo.direccionx
			disparo.direcciony = enemigo.direcciony
			enemigo.direccionx = 0
			enemigo.direcciony = 0
			if disparo.puntuacion >= 5000:
				enemigo.direccionx = disparo.direccionx
				enemigo.direcciony = disparo.direcciony

	#SATURNO	
	def GolpearEnArea(self, enemigo, area):
		area.x = self.x - 10
		area.y = self.y - 10
		area.puntuacion += 1
		if area.puntuacion == 1:
			saturno_sound.play()
		if area.puntuacion >= 200:
			area.puntuacion = 0
		area.DibujarObjeto()
		if enemigo.check_colisiones(area):
			enemigo.vidas -= 5
			if self.direccionx == 1:
				self.direccionx = -1
			else:
				self.direccionx = 1
			if enemigo.direccionx == 1:
				enemigo.direccionx = -1
			else:
				enemigo.direccionx = 1

	#MERCURIO
	def Separarse(self, enemigo, secundaria):
		if self.puntuacion == 0:
			self.ancho = self.ancho / 2
			self.largo = self.largo / 2
			self.vidas = self.vidas / 2
			mercurio_sound.play()
			self.puntuacion = 1
		secundaria.Movimiento(enemigo)
		Chocar(secundaria, enemigo)
		if self.color == (0,0,255):
			barra_hp_izquierda(screen, 50, 60, secundaria.vidas, self.color)
		elif self.color == (255,0,0):
			barra_hp_derecha(screen, 1060, 60, secundaria.vidas, enemigo.color)

	#JUPITER
	def Aumentar(self, enemigo):
		global colision
		if self.x <= 15:
			self.ancho += 2
			self.largo += 2
		elif self.x >= 1265:
			self.ancho += 2
			self.largo += 2
		if self.y <= 0:
			self.ancho += 2
			self.largo += 2
		elif self.y >= 700:
			self.ancho += 2
			self.largo += 2
		if self.check_colisiones(enemigo) and colision == False:
			if self.ancho >= 65 and self.ancho < 80:
				enemigo.vidas -= 2.5
			elif self.ancho >= 80 and self.ancho < 100:
				enemigo.vidas -= 5
			elif self.ancho >= 100:
				enemigo.vidas -= 10
		if self.ancho >= 65 and self.puntuacion == 0:
			jupiter_sound2.play()
			self.puntuacion = 1
		elif self.ancho >= 80 and self.puntuacion == 1:
			jupiter_sound2.play()
			self.puntuacion = 2
		elif self.ancho >= 100 and self.puntuacion == 2:
			jupiter_sound2.play()
			self.puntuacion = 3
	
	#NEPTUNO
	def LluviaDeDiamantes(self, enemigo, diamante1, diamante2):
		diamante1.Movimiento_Diamante(enemigo)
		diamante2.Movimiento_Diamante(enemigo)

def Chocar(plataforma, enemigo):
	global colision
	if plataforma.check_colisiones(enemigo) == True and colision == False:
		plataforma.vidas -= 5
		enemigo.vidas -= 5
		if plataforma.direccionx == 1:
			plataforma.direccionx = -1
		else:
			plataforma.direccionx = 1
		if enemigo.direccionx == 1:
			enemigo.direccionx = -1
		else:
			enemigo.direccionx = 1
		colision = True
	if plataforma.check_colisiones(enemigo) is not True and colision == True:
		colision = False


def barra_hp_izquierda(screen, x, y, hp, color):
	largo = 165
	ancho = 10
	calculo_barra = int((hp / 100)*largo)
	draw.rect(screen, color, Rect(x, y, calculo_barra, ancho))

def barra_hp_derecha(screen, x, y, hp, color):
	largo = 165
	ancho = 10
	calculo_barra = int((hp / 100)*largo)
	x_barra = x + (largo - calculo_barra)
	draw.rect(screen, color, Rect(x_barra, y, calculo_barra, ancho))

def get_font(size):
    return font.Font("menu_assets/font.ttf", size)

mercurio1 = transform.scale(image.load("planetfighters_images/Mercurio1.png"), (50, 50))
mercurio2 = transform.scale(image.load("planetfighters_images/Mercurio2.png"), (50, 50))
mercurio3 = transform.scale(image.load("planetfighters_images/Mercurio3.png"), (50, 50))
mercurio4 = transform.scale(image.load("planetfighters_images/Mercurio4.png"), (50, 50))
mercurio5 = transform.scale(image.load("planetfighters_images/Mercurio5.png"), (50, 50))
secundaria_mercurio = transform.scale(image.load("planetfighters_images/Mercurio1.png"), (50, 50))
minimercurio = transform.scale(image.load("planetfighters_images/Mercurio1.png"), (25, 25))
venus1 = transform.scale(image.load("planetfighters_images/Venus1.png"), (75, 75))
venus2 = transform.scale(image.load("planetfighters_images/Venus2.png"), (75, 75))
venus3 = transform.scale(image.load("planetfighters_images/Venus3.png"), (75, 75))
venus4 = transform.scale(image.load("planetfighters_images/Venus4.png"), (75, 75))
venus5 = transform.scale(image.load("planetfighters_images/Venus5.png"), (75, 75))
minivenus = transform.scale(image.load("planetfighters_images/Venus1.png"), (25, 25))
latierra1 = transform.scale(image.load("planetfighters_images/LaTierra1.png"), (75, 75))
latierra2 = transform.scale(image.load("planetfighters_images/LaTierra2.png"), (75, 75))
latierra3 = transform.scale(image.load("planetfighters_images/LaTierra3.png"), (75, 75))
latierra4 = transform.scale(image.load("planetfighters_images/LaTierra4.png"), (75, 75))
latierra5 = transform.scale(image.load("planetfighters_images/LaTierra5.png"), (75, 75))
minilatierra = transform.scale(image.load("planetfighters_images/LaTierra5.png"), (25, 25))
marte1 = transform.scale(image.load("planetfighters_images/Marte1.png"), (75, 75))
marte2 = transform.scale(image.load("planetfighters_images/Marte2.png"), (75, 75))
marte3 = transform.scale(image.load("planetfighters_images/Marte3.png"), (75, 75))
marte4 = transform.scale(image.load("planetfighters_images/Marte4.png"), (75, 75))
marte5 = transform.scale(image.load("planetfighters_images/Marte5.png"), (75, 75))
minimarte = transform.scale(image.load("planetfighters_images/Marte5.png"), (25, 25))
jupiter1 = transform.scale(image.load("planetfighters_images/Jupiter1.png"), (75, 75))
jupiter2 = transform.scale(image.load("planetfighters_images/Jupiter2.png"), (75, 75))
jupiter3 = transform.scale(image.load("planetfighters_images/Jupiter3.png"), (75, 75))
jupiter4 = transform.scale(image.load("planetfighters_images/Jupiter4.png"), (75, 75))
jupiter5 = transform.scale(image.load("planetfighters_images/Jupiter5.png"), (75, 75))
minijupiter = transform.scale(image.load("planetfighters_images/Jupiter3.png"), (25, 25))
saturno1 = transform.scale(image.load("planetfighters_images/Saturno1.png"), (125, 125))
saturno2 = transform.scale(image.load("planetfighters_images/Saturno2.png"), (125, 125))
saturno3 = transform.scale(image.load("planetfighters_images/Saturno3.png"), (125, 125))
saturno4 = transform.scale(image.load("planetfighters_images/Saturno4.png"), (125, 125))
saturno5 = transform.scale(image.load("planetfighters_images/Saturno5.png"), (125, 125))
minisaturno = transform.scale(image.load("planetfighters_images/Saturno1.png"), (62, 62))
urano1 = transform.scale(image.load("planetfighters_images/Urano1.png"), (75, 75))
urano2 = transform.scale(image.load("planetfighters_images/Urano2.png"), (75, 75))
urano3 = transform.scale(image.load("planetfighters_images/Urano3.png"), (75, 75))
urano4 = transform.scale(image.load("planetfighters_images/Urano4.png"), (75, 75))
urano5 = transform.scale(image.load("planetfighters_images/Urano5.png"), (75, 75))
miniurano = transform.scale(image.load("planetfighters_images/Urano3.png"), (25, 25))
neptuno1 = transform.scale(image.load("planetfighters_images/Neptuno1.png"), (75, 75))
neptuno2 = transform.scale(image.load("planetfighters_images/Neptuno2.png"), (75, 75))
neptuno3 = transform.scale(image.load("planetfighters_images/Neptuno3.png"), (75, 75))
neptuno4 = transform.scale(image.load("planetfighters_images/Neptuno4.png"), (75, 75))
neptuno5 = transform.scale(image.load("planetfighters_images/Neptuno5.png"), (75, 75))
minineptuno = transform.scale(image.load("planetfighters_images/Neptuno1.png"), (25, 25))
space = transform.scale(image.load("planetfighters_images/Space.png").convert(), (1280, 720))
cohete1 = transform.scale(image.load("planetfighters_images/Cohete1.png"), (50, 50))
cohete2 = transform.scale(image.load("planetfighters_images/Cohete2.png"), (50, 50))
hielo1 = transform.scale(image.load("planetfighters_images/Hielo1.png"), (50, 50))
hielo2 = transform.scale(image.load("planetfighters_images/Hielo2.png"), (50, 50))
roca = transform.scale(image.load("planetfighters_images/Roca.png"), (30, 30))
saturnorev = transform.scale(image.load("planetfighters_images/SaturnoRev.png"), (125, 125))
totem = transform.scale(image.load("planetfighters_images/Totem.png"), (75, 75))
diamante = transform.scale(image.load("planetfighters_images/Diamante.png"), (75, 75))
barra = transform.scale(image.load("planetfighters_images/Barra.png"), (175, 20))
explosion_cohete = transform.scale(image.load("planetfighters_images/ExplosionCohete.png"), (50, 50))
explosion_cohete2 = transform.scale(image.load("planetfighters_images/ExplosionCohete2.png"), (50, 50))
explosion_cohete3 = transform.scale(image.load("planetfighters_images/ExplosionCohete3.png"), (50, 50))
explosion_roca = transform.scale(image.load("planetfighters_images/ExplosionRoca.png"), (25, 25))
explosion_roca2 = transform.scale(image.load("planetfighters_images/ExplosionRoca2.png"), (25, 25))
explosion_roca3 = transform.scale(image.load("planetfighters_images/ExplosionRoca3.png"), (25, 25))
explosion_hielo = transform.scale(image.load("planetfighters_images/ExplosionHielo.png"), (50, 50))
explosion_hielo2 = transform.scale(image.load("planetfighters_images/ExplosionHielo2.png"), (50, 50))
explosion_hielo3 = transform.scale(image.load("planetfighters_images/ExplosionHielo3.png"), (50, 50))
explosion_trampa = transform.scale(image.load("planetfighters_images/ExplosionTrampa.png"), (50, 50))
explosion_trampa2 = transform.scale(image.load("planetfighters_images/ExplosionTrampa2.png"), (50, 50))
explosion_trampa3 = transform.scale(image.load("planetfighters_images/ExplosionTrampa3.png"), (50, 50))
BG = transform.scale(image.load("menu_assets/Menu.jpg").convert(), (1280, 720))
BG2 = transform.scale(image.load("menu_assets/Menu2.jpg").convert(), (1280, 720))
BG3 = transform.scale(image.load("menu_assets/Menu3.jpg").convert(), (1280, 720))
marco_azul = transform.scale(image.load("menu_assets/MarcoAzul.png"), (187, 300))
marco_verde = transform.scale(image.load("menu_assets/MarcoVerde.png"), (187, 300))
marco_morado = transform.scale(image.load("menu_assets/MarcoMorado.png"), (187, 300))
marco_rojo = transform.scale(image.load("menu_assets/MarcoRojo.png"), (187, 300))
marco_amarillo = transform.scale(image.load("menu_assets/MarcoAmarillo.png"), (187, 300))
linea1 = transform.scale(image.load("menu_assets/Linea1.png"), (100, 100))
linea2 = transform.scale(image.load("menu_assets/Linea2.png"), (100, 100))
mercurio_sound = mixer.Sound('planetfighters_sounds/Mercurio.ogg')
mercurio_sound.set_volume(0.5)
venus_sound = mixer.Sound('planetfighters_sounds/Venus.ogg')
venus_sound.set_volume(0.5)
latierra_sound = mixer.Sound('planetfighters_sounds/LaTierra.ogg')
latierra_sound.set_volume(0.5)
marte_sound = mixer.Sound('planetfighters_sounds/Marte.ogg')
marte_sound.set_volume(0.5)
jupiter_sound = mixer.Sound('planetfighters_sounds/Jupiter.ogg')
jupiter_sound.set_volume(0.5)
jupiter_sound2 = mixer.Sound('planetfighters_sounds/Jupiter2.ogg')
jupiter_sound2.set_volume(0.5)
saturno_sound = mixer.Sound('planetfighters_sounds/Saturno.ogg')
saturno_sound.set_volume(0.5)
urano_sound = mixer.Sound('planetfighters_sounds/Urano.ogg')
urano_sound.set_volume(0.5)
neptuno_sound = mixer.Sound('planetfighters_sounds/Neptuno.ogg')
neptuno_sound.set_volume(0.5)

def play(p1, p2, tourney, cont):
	plataforma = Bola(300,350,55,55, 1, 1, 0, (0,0,255), 100, 0)
	enemigo = Bola(940,350,55,55, 1, 1, 0, (255,0,0), 100, 1)
	timer = 0
	timer_plataforma = 0
	timer_enemigo = 0
	timer_planeta1 = 0
	timer_planeta2 = 0
	inicial = True
	personaje1 = p1
	personaje2 = p2
	disparo_x = 10001
	cohete_x = 10001
	trampa_x = 10001
	congelacion_x = 10001
	area_x = 10001
	secundaria_x = 10001
	miniplataforma = "Nulo"
	minienemigo = "Nulo"
	plataforma_color = (0,0,255)
	enemigo_color = (255,0,0)
	z = -1
	name = {"Mercurio": "MERCURY", "Venus": "VENUS", "La Tierra": "EARTH", "Marte": "MARS", "Jupiter": "JUPITER", "Saturno": "SATURN", "Urano": "URANUS", "Neptuno": "NEPTUNE"}
	while True:
		global colision, musica

		if z == -1:
			if musica != "Batalla":
				mixer.music.set_volume(0.25)
				mixer.music.load('planetfighters_sounds/Batalla.ogg')
				mixer.music.set_volume(mixer.music.get_volume())
				mixer.music.play(-1)
				musica = "Batalla"
			colision = False
			z = 0

		screen.blit(space, [0, 0]) 
		
		if plataforma.vidas > 0 and enemigo.vidas > 0:
			plataforma.Movimiento(enemigo)
			enemigo.Movimiento(plataforma)
			Chocar(plataforma, enemigo)

		barra_hp_derecha(screen, 1060, 40, enemigo.vidas, enemigo_color)
		barra_hp_izquierda(screen, 50, 40, plataforma.vidas, plataforma_color)
		screen.blit(barra, [44, 35])
		screen.blit(barra, [1054, 35])
		if miniplataforma != "Nulo" and minienemigo != "Nulo":
			if miniplataforma == minisaturno:
				screen.blit(miniplataforma, [12, 10])
				screen.blit(minienemigo, [1221, 30])
			elif minienemigo == minisaturno:
				screen.blit(miniplataforma, [27, 30])
				screen.blit(minienemigo, [1196, 10])
			else:
				screen.blit(miniplataforma, [27, 30])
				screen.blit(minienemigo, [1221, 30])

		timer += 1
		timer_plataforma += 1
		timer_enemigo += 1
		timer_planeta1 += 1
		timer_planeta2 += 1

		if timer == 1 or timer >= 2000:
			if timer == 1 or timer == 2000 or timer == 3000 or timer == 4000 or timer == 10000:
				plataforma.puntuacion = 0
				if personaje1 == "Marte" or personaje2 == "Marte":
					direccionx = choice([1, -1])
					direcciony = choice([1, -1])
					if personaje1 == "Marte":
						miniplataforma = minimarte
						plataforma_color = (167, 67, 42)
						disparo_x = plataforma.x
						disparo_y = plataforma.y
						disparo_team = plataforma.team
					elif personaje2 == "Marte":
						minienemigo = minimarte
						enemigo_color = (167, 67, 42)
						disparo_x = enemigo.x
						disparo_y = enemigo.y
						disparo_team = plataforma.team
					if inicial == True:
						meteorito1 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito2 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito3 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito4 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito5 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito6 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito7 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito8 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito9 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
					elif timer == 1:
						meteorito1 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito2 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito3 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
					elif timer == 2000:
						meteorito4 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito5 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito6 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
					elif timer == 4000:
						meteorito7 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito8 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
						meteorito9 = Bola(disparo_x, disparo_y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, disparo_team)
				if personaje1 == "La Tierra" or personaje2 == "La Tierra":
					if personaje1 == "La Tierra":
						miniplataforma = minilatierra
						plataforma_color = (27, 102, 201)
						cohete_x = plataforma.x
						cohete_y = plataforma.y
						cohete_direccionx = plataforma.direccionx
						cohete_direcciony = plataforma.direcciony
						cohete_team = plataforma.team
					elif personaje2 == "La Tierra":
						minienemigo = minilatierra
						enemigo_color = (27, 102, 201)
						cohete_x = enemigo.x
						cohete_y = enemigo.y
						cohete_direccionx = enemigo.direccionx
						cohete_direcciony = enemigo.direcciony
						cohete_team = plataforma.team
					if inicial == True:
						disparo1 = Bola(cohete_x, cohete_y, 20, 20, cohete_direccionx, cohete_direcciony, 0, (0, 255, 255), 1, cohete_team)
						disparo2 = Bola(cohete_x, cohete_y, 20, 20, cohete_direccionx, cohete_direcciony, 0, (0, 255, 255), 1, cohete_team)
						disparo3 = Bola(cohete_x, cohete_y, 20, 20, cohete_direccionx, cohete_direcciony, 0, (0, 255, 255), 1, cohete_team)
					elif timer == 1:
						disparo1 = Bola(cohete_x, cohete_y, 20, 20, cohete_direccionx, cohete_direcciony, 0, (0, 255, 255), 1, cohete_team)
					elif timer == 2000:
						disparo2 = Bola(cohete_x, cohete_y, 20, 20, cohete_direccionx, cohete_direcciony, 0, (0, 255, 255), 1, cohete_team)
					elif timer == 4000:
						disparo3 = Bola(cohete_x, cohete_y, 20, 20, cohete_direccionx, cohete_direcciony, 0, (0, 255, 255), 1, cohete_team)
				if personaje1 == "Venus" or personaje2 == "Venus":
					if personaje1 == "Venus":
						miniplataforma = minivenus
						plataforma_color = (216, 161, 76)
						trampa_x = plataforma.x
						trampa_y = plataforma.y
					elif personaje2 == "Venus":
						minienemigo = minivenus
						enemigo_color = (216, 161, 76)
						trampa_x = enemigo.x
						trampa_y = enemigo.y
					if inicial == True:
						trampa1 = Bola(trampa_x, trampa_y, 25, 25, 0, 0, 0, (255, 125, 125), 1, plataforma.team)
						trampa2 = Bola(trampa_x, trampa_y, 25, 25, 0, 0, 0, (255, 125, 125), 1, plataforma.team)
						trampa3 = Bola(trampa_x, trampa_y, 25, 25, 0, 0, 0, (255, 125, 125), 1, plataforma.team)
					elif timer == 1:
						trampa1 = Bola(trampa_x, trampa_y, 25, 25, 0, 0, 0, (255, 125, 125), 1, plataforma.team)
					elif timer == 2000:
						trampa2 = Bola(trampa_x, trampa_y, 25, 25, 0, 0, 0, (255, 125, 125), 1, plataforma.team)
					elif timer == 4000:
						trampa3 = Bola(trampa_x, trampa_y, 25, 25, 0, 0, 0, (255, 125, 125), 1, plataforma.team)
				if personaje1 == "Urano" or personaje2 == "Urano":
					if personaje1 == "Urano":
						miniplataforma = miniurano
						plataforma_color = (138, 221, 229)
						congelacion_x = plataforma.x
						congelacion_y = plataforma.y
						congelacion_direccionx = -plataforma.direccionx
						congelacion_direcciony = -plataforma.direcciony
					elif personaje2 == "Urano":
						minienemigo = miniurano
						enemigo_color = (138, 221, 229)
						congelacion_x = enemigo.x
						congelacion_y = enemigo.y
						congelacion_direccionx = -enemigo.direccionx
						congelacion_direcciony = -enemigo.direcciony
					if inicial == True:
						congelacion1 = Bola(congelacion_x, congelacion_y, 20, 20, congelacion_direccionx, congelacion_direcciony, 0, (0, 255, 0), 1, enemigo.team)
						congelacion2 = Bola(congelacion_x, congelacion_y, 20, 20, congelacion_direccionx, congelacion_direcciony, 0, (0, 255, 0), 1, enemigo.team)
						congelacion3 = Bola(congelacion_x, congelacion_y, 20, 20, congelacion_direccionx, congelacion_direcciony, 0, (0, 255, 0), 1, enemigo.team)
					elif timer == 1:
						congelacion1 = Bola(congelacion_x, congelacion_y, 20, 20, congelacion_direccionx, congelacion_direcciony, 0, (0, 255, 0), 1, enemigo.team)
					elif timer == 2000:
						congelacion2 = Bola(congelacion_x, congelacion_y, 20, 20, congelacion_direccionx, congelacion_direcciony, 0, (0, 255, 0), 1, enemigo.team)
					elif timer == 4000:
						congelacion3 = Bola(congelacion_x, congelacion_y, 20, 20, congelacion_direccionx, congelacion_direcciony, 0, (0, 255, 0), 1, enemigo.team)
				if personaje1 == "Saturno" or personaje2 == "Saturno":
					if personaje1 == "Saturno" and area_x == 10001:
						miniplataforma = minisaturno
						plataforma_color = (153, 128, 101)
						area_x = plataforma.x
						area_y = plataforma.y
					elif personaje2 == "Saturno" and area_x == 10001:
						minienemigo = minisaturno
						enemigo_color = (153, 128, 101)
						area_x = enemigo.x
						area_y = enemigo.y
					area = Bola(area_x-7.5, area_y-7.5, 75, 75, 0, 0, 0, (125, 255, 125), 1, plataforma.team)
				if personaje1 == "Mercurio" or personaje2 == "Mercurio":
					if personaje1 == "Mercurio" and secundaria_x == 10001:
						miniplataforma = minimercurio
						plataforma_color = (230, 221, 209)
						secundaria_x = plataforma.x
						secundaria_y = plataforma.y
						secundaria_ancho = plataforma.ancho/2
						secundaria_largo = plataforma.largo/2
						secundaria_direccionx = -plataforma.direccionx
						secundaria_direcciony = -plataforma.direcciony
						secundaria_color = plataforma.color
					elif personaje2 == "Mercurio" and secundaria_x == 10001:
						minienemigo = minimercurio
						enemigo_color = (230, 221, 209)
						secundaria_x = enemigo.x
						secundaria_y = enemigo.y
						secundaria_ancho = enemigo.ancho/2
						secundaria_largo = enemigo.largo/2
						secundaria_direccionx = -enemigo.direccionx
						secundaria_direcciony = -enemigo.direcciony
						secundaria_color = enemigo.color
					if inicial == True:
						secundaria = Bola(secundaria_x, secundaria_y, secundaria_ancho, secundaria_largo, secundaria_direccionx, secundaria_direcciony, 0, secundaria_color, enemigo.vidas/2, enemigo.team)
				if (personaje1 == "Neptuno" or personaje2 == "Neptuno") and inicial == True:
					if personaje1 == "Neptuno" and miniplataforma == "Nulo":
						miniplataforma = minineptuno
						plataforma_color = (13, 49, 117)
					elif personaje2 == "Neptuno" and minienemigo == "Nulo":
						minienemigo = minineptuno
						enemigo_color = (13, 49, 117)
					diamante1 = Bola(0, -100, 10, 10, 0, 0, 0, (255, 125, 255), 1, plataforma.team)
					diamante2 = Bola(0, -100, 10, 10, 0, 0, 0, (255, 125, 255), 1, plataforma.team)
				if personaje1 == "Jupiter" or personaje2 == "Jupiter":
					if personaje1 == "Jupiter" and miniplataforma == "Nulo":
						miniplataforma = minijupiter
						plataforma_color = (244, 222, 194)
					elif personaje2 == "Jupiter" and minienemigo == "Nulo":
						minienemigo = minijupiter
						enemigo_color = (244, 222, 194)
				if timer >= 10000:
					timer = 0
				if timer == 1 and inicial == True:
					inicial = False

		#PLATAFORMA
		if personaje1 == "Mercurio": 
			plataforma.Separarse(enemigo, secundaria)
			if timer_planeta1 <= 150:
				screen.blit(mercurio1, [plataforma.x-10, plataforma.y-10])
				screen.blit(mercurio1, [secundaria.x-10, secundaria.y-10])
			elif timer_planeta1 <= 300:
				screen.blit(mercurio2, [plataforma.x-10, plataforma.y-10])
				screen.blit(mercurio2, [secundaria.x-10, secundaria.y-10])
			elif timer_planeta1 <= 450:
				screen.blit(mercurio3, [plataforma.x-10, plataforma.y-10])
				screen.blit(mercurio3, [secundaria.x-10, secundaria.y-10])
			elif timer_planeta1 <= 600:
				screen.blit(mercurio4, [plataforma.x-10, plataforma.y-10])
				screen.blit(mercurio4, [secundaria.x-10, secundaria.y-10])
			else:
				screen.blit(mercurio5, [plataforma.x-10, plataforma.y-10])
				screen.blit(mercurio5, [secundaria.x-10, secundaria.y-10])
				if timer_planeta1 >= 750:
					timer_planeta1 = 0
		elif personaje1 == "Venus": 
			if timer_plataforma >= 0 and timer_plataforma <= 6000:
				plataforma.PonerTrampa(enemigo, trampa1)	
				if timer_plataforma >= 5750:
					if timer_plataforma <= 5825:
						screen.blit(explosion_trampa, [trampa1.x-15, trampa1.y-15])
					elif timer_plataforma <= 5900:
						screen.blit(explosion_trampa2, [trampa1.x-15, trampa1.y-15])
					else:
						screen.blit(explosion_trampa3, [trampa1.x-15, trampa1.y-15])
				if timer_plataforma >= 6000 and trampa1.x != 10000:
					trampa1.x = 10000
			if timer_plataforma >= 2000 and timer_plataforma <= 8000:
				plataforma.PonerTrampa(enemigo, trampa2)	
				if timer_plataforma >= 7750:
					if timer_plataforma <= 7825:
						screen.blit(explosion_trampa, [trampa2.x-15, trampa2.y-15])
					elif timer_plataforma <= 7900:
						screen.blit(explosion_trampa2, [trampa2.x-15, trampa2.y-15])
					else:
						screen.blit(explosion_trampa3, [trampa2.x-15, trampa2.y-15])
				if timer_plataforma >= 8000 and trampa2.x != 10000:
					trampa2.x = 10000
			if timer_plataforma >= 4000 and timer_plataforma <= 10000:
				plataforma.PonerTrampa(enemigo, trampa3)
				if timer_plataforma >= 9750:
					if timer_plataforma <= 9825:
						screen.blit(explosion_trampa, [trampa3.x-15, trampa3.y-15])
					elif timer_plataforma <= 9900:
						screen.blit(explosion_trampa2, [trampa3.x-15, trampa3.y-15])
					else:
						screen.blit(explosion_trampa3, [trampa3.x-15, trampa3.y-15])
				if timer_plataforma >= 10000 and trampa3.x != 10000:
					trampa3.x = 10000
			if timer_plataforma >= 10000:
				timer_plataforma = 0
			if timer_planeta1 <= 150:
				screen.blit(venus1, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 300:
				screen.blit(venus2, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 450:
				screen.blit(venus3, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 600:
				screen.blit(venus4, [plataforma.x-10, plataforma.y-10])
			else:
				screen.blit(venus5, [plataforma.x-10, plataforma.y-10])
				if timer_planeta1 >= 750:
					timer_planeta1 = 0
			if trampa1.x != 10000 and timer_plataforma >= 0 and timer_plataforma <= 5750:
				screen.blit(totem, [trampa1.x-25, trampa1.y-30])
			if trampa2.x != 10000 and timer_plataforma >= 2000 and timer_plataforma <= 7750:
				screen.blit(totem, [trampa2.x-25, trampa2.y-30])
			if trampa3.x != 10000 and timer_plataforma >= 4000 and timer_plataforma <= 9750:
				screen.blit(totem, [trampa3.x-25, trampa3.y-30])
		elif personaje1 == "La Tierra": 
			if timer_plataforma >= 0 and timer_plataforma <= 6000:
				plataforma.DispararTeledirigido(enemigo, disparo1)
				if timer_plataforma >= 5750:
					if timer_plataforma <= 5825:
						screen.blit(explosion_cohete, [disparo1.x-15, disparo1.y-15])
					elif timer_plataforma <= 5900:
						screen.blit(explosion_cohete2, [disparo1.x-15, disparo1.y-15])
					else:
						screen.blit(explosion_cohete3, [disparo1.x-15, disparo1.y-15])
				if timer_plataforma >= 6000 and disparo1.x != 10000:
					disparo1.x = 10000
			if timer_plataforma >= 2000 and timer_plataforma <= 8000:
				plataforma.DispararTeledirigido(enemigo, disparo2)
				if timer_plataforma >= 7750:
					if timer_plataforma <= 7825:
						screen.blit(explosion_cohete, [disparo2.x-15, disparo2.y-15])
					elif timer_plataforma <= 7900:
						screen.blit(explosion_cohete2, [disparo2.x-15, disparo2.y-15])
					else:
						screen.blit(explosion_cohete3, [disparo2.x-15, disparo2.y-15])
				if timer_plataforma >= 8000 and disparo2.x != 10000:
					disparo2.x = 10000
			if timer_plataforma >= 4000 and timer_plataforma <= 10000:
				plataforma.DispararTeledirigido(enemigo, disparo3)
				if timer_plataforma >= 9750:
					if timer_plataforma <= 9825:
						screen.blit(explosion_cohete, [disparo3.x-15, disparo3.y-15])
					elif timer_plataforma <= 9900:
						screen.blit(explosion_cohete2, [disparo3.x-15, disparo3.y-15])
					else:
						screen.blit(explosion_cohete3, [disparo3.x-15, disparo3.y-15])
				if timer_plataforma >= 10000 and disparo3.x != 10000:
					disparo3.x = 10000
			if timer_plataforma >= 10000:
				timer_plataforma = 0
			if timer_planeta1 <= 150:
				screen.blit(latierra1, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 300:
				screen.blit(latierra2, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 450:
				screen.blit(latierra3, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 600:
				screen.blit(latierra4, [plataforma.x-10, plataforma.y-10])
			else:
				screen.blit(latierra5, [plataforma.x-10, plataforma.y-10])
				if timer_planeta1 >= 750:
					timer_planeta1 = 0
			if disparo1.x != 10000 and timer_plataforma >= 0 and timer_plataforma <= 5750:
				if disparo1.direccionx == -1:
					screen.blit(cohete2, [disparo1.x-15, disparo1.y-15])
				else:
					screen.blit(cohete1, [disparo1.x-15, disparo1.y-15])
			if disparo2.x != 10000 and timer_plataforma >= 2000 and timer_plataforma <= 7750:
				if disparo2.direccionx == -1:
					screen.blit(cohete2, [disparo2.x-15, disparo2.y-15])
				else:
					screen.blit(cohete1, [disparo2.x-15, disparo2.y-15])
			if disparo3.x != 10000 and timer_plataforma >= 4000 and timer_plataforma <= 9750:
				if disparo3.direccionx == -1:
					screen.blit(cohete2, [disparo3.x-15, disparo3.y-15])
				else:
					screen.blit(cohete1, [disparo3.x-15, disparo3.y-15])
		elif personaje1 == "Marte": 
			if timer_plataforma >= 0 and timer_plataforma <= 6000:
				plataforma.Disparar(enemigo, meteorito1, meteorito2, meteorito3)
				if timer_plataforma >= 5750:
					if timer_plataforma <= 5825:
						screen.blit(explosion_roca, [meteorito1.x-10, meteorito1.y-10])
						screen.blit(explosion_roca, [meteorito2.x-10, meteorito2.y-10])
						screen.blit(explosion_roca, [meteorito3.x-10, meteorito3.y-10])
					elif timer_plataforma <= 5900:
						screen.blit(explosion_roca2, [meteorito1.x-10, meteorito1.y-10])
						screen.blit(explosion_roca2, [meteorito2.x-10, meteorito2.y-10])
						screen.blit(explosion_roca2, [meteorito3.x-10, meteorito3.y-10])
					else:
						screen.blit(explosion_roca3, [meteorito1.x-10, meteorito1.y-10])
						screen.blit(explosion_roca3, [meteorito2.x-10, meteorito2.y-10])
						screen.blit(explosion_roca3, [meteorito3.x-10, meteorito3.y-10])
				if timer_plataforma >= 6000 and (meteorito1.x != 10000 or meteorito2.x != 10000 or meteorito3.x != 10000):
					meteorito1.x = 10000
					meteorito2.x = 10000
					meteorito3.x = 10000
			if timer_plataforma >= 2000 and timer_plataforma <= 8000:
				plataforma.Disparar(enemigo, meteorito4, meteorito5, meteorito6)
				if timer_plataforma >= 7750:
					if timer_plataforma <= 7825:
						screen.blit(explosion_roca, [meteorito4.x-10, meteorito4.y-10])
						screen.blit(explosion_roca, [meteorito5.x-10, meteorito5.y-10])
						screen.blit(explosion_roca, [meteorito6.x-10, meteorito6.y-10])
					elif timer_plataforma <= 7900:
						screen.blit(explosion_roca2, [meteorito4.x-10, meteorito4.y-10])
						screen.blit(explosion_roca2, [meteorito5.x-10, meteorito5.y-10])
						screen.blit(explosion_roca2, [meteorito6.x-10, meteorito6.y-10])
					else:
						screen.blit(explosion_roca3, [meteorito4.x-10, meteorito4.y-10])
						screen.blit(explosion_roca3, [meteorito5.x-10, meteorito5.y-10])
						screen.blit(explosion_roca3, [meteorito6.x-10, meteorito6.y-10])
				if timer_plataforma >= 8000 and (meteorito4.x != 10000 or meteorito5.x != 10000 or meteorito6.x != 10000):
					meteorito4.x = 10000
					meteorito5.x = 10000
					meteorito6.x = 10000
			if timer_plataforma >= 4000 and timer_plataforma <= 10000:
				plataforma.Disparar(enemigo, meteorito7, meteorito8, meteorito9)
				if timer_plataforma >= 9750:
					if timer_plataforma <= 9825:
						screen.blit(explosion_roca, [meteorito7.x-10, meteorito7.y-10])
						screen.blit(explosion_roca, [meteorito8.x-10, meteorito8.y-10])
						screen.blit(explosion_roca, [meteorito9.x-10, meteorito9.y-10])
					elif timer_plataforma <= 9900:
						screen.blit(explosion_roca2, [meteorito7.x-10, meteorito7.y-10])
						screen.blit(explosion_roca2, [meteorito8.x-10, meteorito8.y-10])
						screen.blit(explosion_roca2, [meteorito9.x-10, meteorito8.y-10])
					else:
						screen.blit(explosion_roca3, [meteorito7.x-10, meteorito7.y-10])
						screen.blit(explosion_roca3, [meteorito8.x-10, meteorito8.y-10])
						screen.blit(explosion_roca3, [meteorito9.x-10, meteorito9.y-10])
				if timer_plataforma >= 10000 and (meteorito7.x != 10000 or meteorito8.x != 10000 or meteorito9.x != 10000):
					meteorito7.x = 10000
					meteorito8.x = 10000
					meteorito9.x = 10000
			if timer_plataforma >= 10000:
				timer_plataforma = 0
			if timer_planeta1 <= 150:
				screen.blit(marte1, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 300:
				screen.blit(marte2, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 450:
				screen.blit(marte3, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 600:
				screen.blit(marte4, [plataforma.x-10, plataforma.y-10])
			else:
				screen.blit(marte5, [plataforma.x-10, plataforma.y-10])
				if timer_planeta1 >= 750:
					timer_planeta1 = 0
			if meteorito1.x != 10000 and timer_plataforma >= 0 and timer_plataforma <= 5750: screen.blit(roca, [meteorito1.x-10, meteorito1.y-10])
			if meteorito2.x != 10000 and timer_plataforma >= 0 and timer_plataforma <= 5750: screen.blit(roca, [meteorito2.x-10, meteorito2.y-10])
			if meteorito3.x != 10000 and timer_plataforma >= 0 and timer_plataforma <= 5750: screen.blit(roca, [meteorito3.x-10, meteorito3.y-10])
			if meteorito4.x != 10000 and timer_plataforma >= 2000 and timer_plataforma <= 7750: screen.blit(roca, [meteorito4.x-10, meteorito4.y-10])
			if meteorito5.x != 10000 and timer_plataforma >= 2000 and timer_plataforma <= 7750: screen.blit(roca, [meteorito5.x-10, meteorito5.y-10])
			if meteorito6.x != 10000 and timer_plataforma >= 2000 and timer_plataforma <= 7750: screen.blit(roca, [meteorito6.x-10, meteorito6.y-10])
			if meteorito7.x != 10000 and timer_plataforma >= 4000 and timer_plataforma <= 9750: screen.blit(roca, [meteorito7.x-10, meteorito7.y-10])
			if meteorito8.x != 10000 and timer_plataforma >= 4000 and timer_plataforma <= 9750: screen.blit(roca, [meteorito8.x-10, meteorito8.y-10])
			if meteorito9.x != 10000 and timer_plataforma >= 4000 and timer_plataforma <= 9750: screen.blit(roca, [meteorito9.x-10, meteorito9.y-10])
		elif personaje1 == "Jupiter": 
			plataforma.Aumentar(enemigo)
			if timer_planeta1 <= 150:
				screen.blit(jupiter1, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 300:
				screen.blit(jupiter2, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 450:
				screen.blit(jupiter3, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 600:
				screen.blit(jupiter4, [plataforma.x-10, plataforma.y-10])
			else:
				screen.blit(jupiter5, [plataforma.x-10, plataforma.y-10])
				if timer_planeta1 >= 750:
					timer_planeta1 = 0
		elif personaje1 == "Saturno": 
			if timer_plataforma >= 3000:
				plataforma.GolpearEnArea(enemigo, area)
				screen.blit(saturnorev, [plataforma.x-35, plataforma.y-35])
				if timer_plataforma >= 6000:
					timer_plataforma = 0
			if timer_planeta1 <= 150:
				screen.blit(saturno1, [plataforma.x-35, plataforma.y-35])
			elif timer_planeta1 <= 300:
				screen.blit(saturno2, [plataforma.x-35, plataforma.y-35])
			elif timer_planeta1 <= 450:
				screen.blit(saturno3, [plataforma.x-35, plataforma.y-35])
			elif timer_planeta1 <= 600:
				screen.blit(saturno4, [plataforma.x-35, plataforma.y-35])
			else:
				screen.blit(saturno5, [plataforma.x-35, plataforma.y-35])
				if timer_planeta1 >= 750:
					timer_planeta1 = 0
		elif personaje1 == "Urano": 
			if timer_plataforma >= 0 and timer_plataforma <= 6000:
				plataforma.DispararCongelacion(enemigo, congelacion1)
				if timer_plataforma >= 5750:
					if timer_plataforma <= 5825:
						screen.blit(explosion_hielo, [congelacion1.x-12.5, congelacion1.y-15])
					elif timer_plataforma <= 5900:
						screen.blit(explosion_hielo2, [congelacion1.x-12.5, congelacion1.y-15])
					else:
						screen.blit(explosion_hielo3, [congelacion1.x-12.5, congelacion1.y-15])
				if timer_plataforma >= 6000 and congelacion1.x != 10000:
					congelacion1.x = 10000
			if timer_plataforma >= 2000 and timer_plataforma <= 8000:
				plataforma.DispararCongelacion(enemigo, congelacion2)
				if timer_plataforma >= 7750:
					if timer_plataforma <= 7825:
						screen.blit(explosion_hielo, [congelacion2.x-12.5, congelacion2.y-15])
					elif timer_plataforma <= 7900:
						screen.blit(explosion_hielo2, [congelacion2.x-12.5, congelacion2.y-15])
					else:
						screen.blit(explosion_hielo3, [congelacion2.x-12.5, congelacion2.y-15])
				if timer_plataforma >= 8000 and congelacion2.x != 10000:
					congelacion2.x = 10000
			if timer_plataforma >= 4000 and timer_plataforma <= 10000:
				plataforma.DispararCongelacion(enemigo, congelacion3)
				if timer_plataforma >= 9750:
					if timer_plataforma <= 9825:
						screen.blit(explosion_hielo, [congelacion3.x-12.5, congelacion3.y-15])
					elif timer_plataforma <= 9900:
						screen.blit(explosion_hielo2, [congelacion3.x-12.5, congelacion3.y-15])
					else:
						screen.blit(explosion_hielo3, [congelacion3.x-12.5, congelacion3.y-15])
				if timer_plataforma >= 10000 and congelacion3.x != 10000:
					congelacion3.x = 10000
			if timer_plataforma >= 10000:
				timer_plataforma = 0
			if timer_planeta1 <= 150:
				screen.blit(urano1, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 300:
				screen.blit(urano2, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 450:
				screen.blit(urano3, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 600:
				screen.blit(urano4, [plataforma.x-10, plataforma.y-10])
			else:
				screen.blit(urano5, [plataforma.x-10, plataforma.y-10])
				if timer_planeta1 >= 750:
					timer_planeta1 = 0
			if congelacion1.x != 10000 and timer_plataforma >= 0 and timer_plataforma <= 5750:
				if congelacion1.direccionx == -1:
					screen.blit(hielo2, [congelacion1.x-17.5, congelacion1.y-15])
				else:
					screen.blit(hielo1, [congelacion1.x-12.5, congelacion1.y-15])
			if congelacion2.x != 10000 and timer_plataforma >= 2000 and timer_plataforma <= 7750:
				if congelacion2.direccionx == -1:
					screen.blit(hielo2, [congelacion2.x-17.5, congelacion2.y-15])
				else:
					screen.blit(hielo1, [congelacion2.x-12.5, congelacion2.y-15])
			if congelacion3.x != 10000 and timer_plataforma >= 4000 and timer_plataforma <= 9750:
				if congelacion3.direccionx == -1:
					screen.blit(hielo2, [congelacion3.x-17.5, congelacion3.y-15])
				else:
					screen.blit(hielo1, [congelacion3.x-12.5, congelacion3.y-15])
		elif personaje1 == "Neptuno": 
			plataforma.LluviaDeDiamantes(enemigo, diamante1, diamante2)
			if timer_planeta1 <= 150:
				screen.blit(neptuno1, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 300:
				screen.blit(neptuno2, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 450:
				screen.blit(neptuno3, [plataforma.x-10, plataforma.y-10])
			elif timer_planeta1 <= 600:
				screen.blit(neptuno4, [plataforma.x-10, plataforma.y-10])
			else:
				screen.blit(neptuno5, [plataforma.x-10, plataforma.y-10])
				if timer_planeta1 >= 750:
					timer_planeta1 = 0
			screen.blit(diamante, [diamante1.x-35, diamante1.y-20])
			screen.blit(diamante, [diamante2.x-35, diamante2.y-20])

		#ENEMIGO
		if personaje2 == "Mercurio": 
			enemigo.Separarse(plataforma, secundaria)		
			if timer_planeta2 <= 150:
				screen.blit(mercurio1, [enemigo.x-10, enemigo.y-10])
				screen.blit(mercurio1, [secundaria.x-10, secundaria.y-10])
			elif timer_planeta2 <= 300:
				screen.blit(mercurio2, [enemigo.x-10, enemigo.y-10])
				screen.blit(mercurio2, [secundaria.x-10, secundaria.y-10])
			elif timer_planeta2 <= 450:
				screen.blit(mercurio3, [enemigo.x-10, enemigo.y-10])
				screen.blit(mercurio3, [secundaria.x-10, secundaria.y-10])
			elif timer_planeta2 <= 600:
				screen.blit(mercurio4, [enemigo.x-10, enemigo.y-10])
				screen.blit(mercurio4, [secundaria.x-10, secundaria.y-10])
			else:
				screen.blit(mercurio5, [enemigo.x-10, enemigo.y-10])
				screen.blit(mercurio5, [secundaria.x-10, secundaria.y-10])
				if timer_planeta2 >= 750:
					timer_planeta2 = 0
		elif personaje2 == "Venus": 
			if timer_enemigo >= 0 and timer_enemigo <= 6000:
				enemigo.PonerTrampa(plataforma, trampa1)	
				if timer_enemigo >= 5750:
					if timer_enemigo <= 5825:
						screen.blit(explosion_trampa, [trampa1.x-15, trampa1.y-15])
					elif timer_enemigo <= 5900:
						screen.blit(explosion_trampa2, [trampa1.x-15, trampa1.y-15])
					else:
						screen.blit(explosion_trampa3, [trampa1.x-15, trampa1.y-15])
				if timer_enemigo >= 6000 and trampa1.x != 10000:
					trampa1.x = 10000
			if timer_enemigo >= 2000 and timer_enemigo <= 8000:
				enemigo.PonerTrampa(plataforma, trampa2)
				if timer_enemigo >= 7750:
					if timer_enemigo <= 7825:
						screen.blit(explosion_trampa, [trampa2.x-15, trampa2.y-15])
					elif timer_enemigo <= 7900:
						screen.blit(explosion_trampa2, [trampa2.x-15, trampa2.y-15])
					else:
						screen.blit(explosion_trampa3, [trampa2.x-15, trampa2.y-15])	
				if timer_enemigo >= 8000 and trampa2.x != 10000:
					trampa2.x = 10000
			if timer_enemigo >= 4000 and timer_enemigo <= 10000:
				enemigo.PonerTrampa(plataforma, trampa3)
				if timer_enemigo >= 9750:
					if timer_enemigo <= 9825:
						screen.blit(explosion_trampa, [trampa3.x-15, trampa3.y-15])
					elif timer_enemigo <= 9900:
						screen.blit(explosion_trampa2, [trampa3.x-15, trampa3.y-15])
					else:
						screen.blit(explosion_trampa3, [trampa3.x-15, trampa3.y-15])
				if timer_enemigo >= 10000 and trampa3.x != 10000:
					trampa3.x = 10000
			if timer_enemigo >= 10000:
				timer_enemigo = 0
			if timer_planeta2 <= 150:
				screen.blit(venus1, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 300:
				screen.blit(venus2, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 450:
				screen.blit(venus3, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 600:
				screen.blit(venus4, [enemigo.x-10, enemigo.y-10])
			else:
				screen.blit(venus5, [enemigo.x-10, enemigo.y-10])
				if timer_planeta2 >= 750:
					timer_planeta2 = 0
			if trampa1.x != 10000 and timer_enemigo >= 0 and timer_enemigo <= 5750:
				screen.blit(totem, [trampa1.x-25, trampa1.y-30])
			if trampa2.x != 10000 and timer_enemigo >= 2000 and timer_enemigo <= 7750:
				screen.blit(totem, [trampa2.x-25, trampa2.y-30])
			if trampa3.x != 10000 and timer_enemigo >= 4000 and timer_enemigo <= 9750:
				screen.blit(totem, [trampa3.x-25, trampa3.y-30])
		elif personaje2 == "La Tierra": 
			if timer_enemigo >= 0 and timer_enemigo <= 6000:
				enemigo.DispararTeledirigido(plataforma, disparo1)
				if timer_enemigo >= 5750:
					if timer_enemigo <= 5825:
						screen.blit(explosion_cohete, [disparo1.x-15, disparo1.y-15])
					elif timer_enemigo <= 5900:
						screen.blit(explosion_cohete2, [disparo1.x-15, disparo1.y-15])
					else:
						screen.blit(explosion_cohete3, [disparo1.x-15, disparo1.y-15])
				if timer_enemigo >= 6000 and disparo1.x != 10000:
					disparo1.x = 10000
			if timer_enemigo >= 2000 and timer_enemigo <= 8000:
				enemigo.DispararTeledirigido(plataforma, disparo2)
				if timer_enemigo >= 7750:
					if timer_enemigo <= 7825:
						screen.blit(explosion_cohete, [disparo2.x-15, disparo2.y-15])
					elif timer_enemigo <= 7900:
						screen.blit(explosion_cohete2, [disparo2.x-15, disparo2.y-15])
					else:
						screen.blit(explosion_cohete3, [disparo2.x-15, disparo2.y-15])
				if timer_enemigo >= 8000 and disparo2.x != 10000:
					disparo2.x = 10000
			if timer_enemigo >= 4000 and timer_enemigo <= 10000:
				enemigo.DispararTeledirigido(plataforma, disparo3)
				if timer_enemigo >= 9750:
					if timer_enemigo <= 9825:
						screen.blit(explosion_cohete, [disparo3.x-15, disparo3.y-15])
					elif timer_enemigo <= 9900:
						screen.blit(explosion_cohete2, [disparo3.x-15, disparo3.y-15])
					else:
						screen.blit(explosion_cohete3, [disparo3.x-15, disparo3.y-15])
				if timer_enemigo >= 10000 and disparo3.x != 10000:
					disparo3.x = 10000
			if timer_enemigo >= 10000:
				timer_enemigo = 0
			if timer_planeta2 <= 150:
				screen.blit(latierra1, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 300:
				screen.blit(latierra2, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 450:
				screen.blit(latierra3, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 600:
				screen.blit(latierra4, [enemigo.x-10, enemigo.y-10])
			else:
				screen.blit(latierra5, [enemigo.x-10, enemigo.y-10])
				if timer_planeta2 >= 750:
					timer_planeta2 = 0
			if disparo1.x != 10000 and timer_enemigo >= 0 and timer_enemigo <= 5750:
				if disparo1.direccionx == -1:
					screen.blit(cohete2, [disparo1.x-15, disparo1.y-15])
				else:
					screen.blit(cohete1, [disparo1.x-15, disparo1.y-15])
			if disparo2.x != 10000 and timer_enemigo >= 2000 and timer_enemigo <= 7750:
				if disparo2.direccionx == -1:
					screen.blit(cohete2, [disparo2.x-15, disparo2.y-15])
				else:
					screen.blit(cohete1, [disparo2.x-15, disparo2.y-15])
			if disparo3.x != 10000 and timer_enemigo >= 4000 and timer_enemigo <= 9750:
				if disparo3.direccionx == -1:
					screen.blit(cohete2, [disparo3.x-15, disparo3.y-15])
				else:
					screen.blit(cohete1, [disparo3.x-15, disparo3.y-15])
		elif personaje2 == "Marte": 
			if timer_enemigo >= 0 and timer_enemigo <= 6000:
				enemigo.Disparar(plataforma, meteorito1, meteorito2, meteorito3)
				if timer_enemigo >= 5750:
					if timer_enemigo <= 5825:
						screen.blit(explosion_roca, [meteorito1.x-10, meteorito1.y-10])
						screen.blit(explosion_roca, [meteorito2.x-10, meteorito2.y-10])
						screen.blit(explosion_roca, [meteorito3.x-10, meteorito3.y-10])
					elif timer_enemigo <= 5900:
						screen.blit(explosion_roca2, [meteorito1.x-10, meteorito1.y-10])
						screen.blit(explosion_roca2, [meteorito2.x-10, meteorito2.y-10])
						screen.blit(explosion_roca2, [meteorito3.x-10, meteorito3.y-10])
					else:
						screen.blit(explosion_roca3, [meteorito1.x-10, meteorito1.y-10])
						screen.blit(explosion_roca3, [meteorito2.x-10, meteorito2.y-10])
						screen.blit(explosion_roca3, [meteorito3.x-10, meteorito3.y-10])
				if timer_enemigo >= 6000 and (meteorito1.x != 10000 or meteorito2.x != 10000 or meteorito3.x != 10000):
					meteorito1.x = 10000
					meteorito2.x = 10000
					meteorito3.x = 10000
			if timer_enemigo >= 2000 and timer_enemigo <= 8000:
				enemigo.Disparar(plataforma, meteorito4, meteorito5, meteorito6)
				if timer_enemigo >= 7750:
					if timer_enemigo <= 7825:
						screen.blit(explosion_roca, [meteorito4.x-10, meteorito4.y-10])
						screen.blit(explosion_roca, [meteorito5.x-10, meteorito5.y-10])
						screen.blit(explosion_roca, [meteorito6.x-10, meteorito6.y-10])
					elif timer_enemigo <= 7900:
						screen.blit(explosion_roca2, [meteorito4.x-10, meteorito4.y-10])
						screen.blit(explosion_roca2, [meteorito5.x-10, meteorito5.y-10])
						screen.blit(explosion_roca2, [meteorito6.x-10, meteorito6.y-10])
					else:
						screen.blit(explosion_roca3, [meteorito4.x-10, meteorito4.y-10])
						screen.blit(explosion_roca3, [meteorito5.x-10, meteorito5.y-10])
						screen.blit(explosion_roca3, [meteorito6.x-10, meteorito6.y-10])
				if timer_enemigo >= 8000 and (meteorito4.x != 10000 or meteorito5.x != 10000 or meteorito6.x != 10000):
					meteorito4.x = 10000
					meteorito5.x = 10000
					meteorito6.x = 10000
			if timer_enemigo >= 4000 and timer_enemigo <= 10000:
				enemigo.Disparar(plataforma, meteorito7, meteorito8, meteorito9)
				if timer_enemigo >= 9750:
					if timer_enemigo <= 9825:
						screen.blit(explosion_roca, [meteorito7.x-10, meteorito7.y-10])
						screen.blit(explosion_roca, [meteorito8.x-10, meteorito8.y-10])
						screen.blit(explosion_roca, [meteorito9.x-10, meteorito9.y-10])
					elif timer_enemigo <= 9900:
						screen.blit(explosion_roca2, [meteorito7.x-10, meteorito7.y-10])
						screen.blit(explosion_roca2, [meteorito8.x-10, meteorito8.y-10])
						screen.blit(explosion_roca2, [meteorito9.x-10, meteorito9.y-10])
					else:
						screen.blit(explosion_roca3, [meteorito7.x-10, meteorito7.y-10])
						screen.blit(explosion_roca3, [meteorito8.x-10, meteorito8.y-10])
						screen.blit(explosion_roca3, [meteorito9.x-10, meteorito9.y-10])
				if timer_enemigo >= 10000 and (meteorito7.x != 10000 or meteorito8.x != 10000 or meteorito9.x != 10000):
					meteorito7.x = 10000
					meteorito8.x = 10000
					meteorito9.x = 10000
			if timer_enemigo >= 10000:
				timer_enemigo = 0
			if timer_planeta2 <= 150:
				screen.blit(marte1, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 300:
				screen.blit(marte2, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 450:
				screen.blit(marte3, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 600:
				screen.blit(marte4, [enemigo.x-10, enemigo.y-10])
			else:
				screen.blit(marte5, [enemigo.x-10, enemigo.y-10])
				if timer_planeta2 >= 750:
					timer_planeta2 = 0
			if meteorito1.x != 10000 and timer_enemigo >= 0 and timer_enemigo <= 5750: screen.blit(roca, [meteorito1.x-10, meteorito1.y-10])
			if meteorito2.x != 10000 and timer_enemigo >= 0 and timer_enemigo <= 5750: screen.blit(roca, [meteorito2.x-10, meteorito2.y-10])
			if meteorito3.x != 10000 and timer_enemigo >= 0 and timer_enemigo <= 5750: screen.blit(roca, [meteorito3.x-10, meteorito3.y-10])
			if meteorito4.x != 10000 and timer_enemigo >= 2000 and timer_enemigo <= 7750: screen.blit(roca, [meteorito4.x-10, meteorito4.y-10])
			if meteorito5.x != 10000 and timer_enemigo >= 2000 and timer_enemigo <= 7750: screen.blit(roca, [meteorito5.x-10, meteorito5.y-10])
			if meteorito6.x != 10000 and timer_enemigo >= 2000 and timer_enemigo <= 7750: screen.blit(roca, [meteorito6.x-10, meteorito6.y-10])
			if meteorito7.x != 10000 and timer_enemigo >= 4000 and timer_enemigo <= 9750: screen.blit(roca, [meteorito7.x-10, meteorito7.y-10])
			if meteorito8.x != 10000 and timer_enemigo >= 4000 and timer_enemigo <= 9750: screen.blit(roca, [meteorito8.x-10, meteorito8.y-10])
			if meteorito9.x != 10000 and timer_enemigo >= 4000 and timer_enemigo <= 9750: screen.blit(roca, [meteorito9.x-10, meteorito9.y-10])
		elif personaje2 == "Jupiter": 
			enemigo.Aumentar(plataforma)
			if timer_planeta2 <= 150:
				screen.blit(jupiter1, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 300:
				screen.blit(jupiter2, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 450:
				screen.blit(jupiter3, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 600:
				screen.blit(jupiter4, [enemigo.x-10, enemigo.y-10])
			else:
				screen.blit(jupiter5, [enemigo.x-10, enemigo.y-10])
				if timer_planeta2 >= 750:
					timer_planeta2 = 0
		elif personaje2 == "Saturno": 
			if timer_enemigo >= 3000:
				enemigo.GolpearEnArea(plataforma, area)
				screen.blit(saturnorev, [enemigo.x-35, enemigo.y-35])
				if timer_enemigo >= 6000:
					timer_enemigo = 0
			if timer_planeta2 <= 150:
				screen.blit(saturno1, [enemigo.x-35, enemigo.y-35])
			elif timer_planeta2 <= 300:
				screen.blit(saturno2, [enemigo.x-35, enemigo.y-35])
			elif timer_planeta2 <= 450:
				screen.blit(saturno3, [enemigo.x-35, enemigo.y-35])
			elif timer_planeta2 <= 600:
				screen.blit(saturno4, [enemigo.x-35, enemigo.y-35])
			else:
				screen.blit(saturno5, [enemigo.x-35, enemigo.y-35])
				if timer_planeta2 >= 750:
					timer_planeta2 = 0
		elif personaje2 == "Urano": 
			if timer_enemigo >= 0 and timer_enemigo <= 6000:
				enemigo.DispararCongelacion(plataforma, congelacion1)
				if timer_enemigo >= 5750:
					if timer_enemigo <= 5825:
						screen.blit(explosion_hielo, [congelacion1.x-17.5, congelacion1.y-15])
					elif timer_enemigo <= 5900:
						screen.blit(explosion_hielo2, [congelacion1.x-17.5, congelacion1.y-15])
					else:
						screen.blit(explosion_hielo3, [congelacion1.x-17.5, congelacion1.y-15])
				if timer_enemigo >= 6000 and congelacion1.x != 10000:
					congelacion1.x = 10000
			if timer_enemigo >= 2000 and timer_enemigo <= 8000:
				enemigo.DispararCongelacion(plataforma, congelacion2)
				if timer_enemigo >= 7750:
					if timer_enemigo <= 7825:
						screen.blit(explosion_hielo, [congelacion2.x-17.5, congelacion2.y-15])
					elif timer_enemigo <= 7900:
						screen.blit(explosion_hielo2, [congelacion2.x-17.5, congelacion2.y-15])
					else:
						screen.blit(explosion_hielo3, [congelacion2.x-17.5, congelacion2.y-15])
				if timer_enemigo >= 8000 and congelacion2.x != 10000:
					congelacion2.x = 10000
			if timer_enemigo >= 4000 and timer_enemigo <= 10000:
				enemigo.DispararCongelacion(plataforma, congelacion3)
				if timer_enemigo >= 9750:
					if timer_enemigo <= 9825:
						screen.blit(explosion_hielo, [congelacion3.x-17.5, congelacion3.y-15])
					elif timer_enemigo <= 9900:
						screen.blit(explosion_hielo2, [congelacion3.x-17.5, congelacion3.y-15])
					else:
						screen.blit(explosion_hielo3, [congelacion3.x-17.5, congelacion3.y-15])
				if timer_enemigo >= 10000 and congelacion3.x != 10000:
					congelacion3.x = 10000
			if timer_enemigo >= 10000:
				timer_enemigo = 0
			if timer_planeta2 <= 150:
				screen.blit(urano1, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 300:
				screen.blit(urano2, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 450:
				screen.blit(urano3, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 600:
				screen.blit(urano4, [enemigo.x-10, enemigo.y-10])
			else:
				screen.blit(urano5, [enemigo.x-10, enemigo.y-10])
				if timer_planeta2 >= 750:
					timer_planeta2 = 0
			if congelacion1.x != 10000 and timer_enemigo >= 0 and timer_enemigo <= 5750:
				if congelacion1.direccionx == -1:
					screen.blit(hielo2, [congelacion1.x-17.5, congelacion1.y-15])
				else:
					screen.blit(hielo1, [congelacion1.x-12.5, congelacion1.y-15])
			if congelacion2.x != 10000 and timer_enemigo >= 2000 and timer_enemigo <= 7750:
				if congelacion2.direccionx == -1:
					screen.blit(hielo2, [congelacion2.x-17.5, congelacion2.y-15])
				else:
					screen.blit(hielo1, [congelacion2.x-12.5, congelacion2.y-15])
			if congelacion3.x != 10000 and timer_enemigo >= 4000 and timer_enemigo <= 9750:
				if congelacion3.direccionx == -1:
					screen.blit(hielo2, [congelacion3.x-17.5, congelacion3.y-15])
				else:
					screen.blit(hielo1, [congelacion3.x-12.5, congelacion3.y-15])
		elif personaje2 == "Neptuno": 
			enemigo.LluviaDeDiamantes(plataforma, diamante1, diamante2)
			if timer_planeta2 <= 150:
				screen.blit(neptuno1, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 300:
				screen.blit(neptuno2, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 450:
				screen.blit(neptuno3, [enemigo.x-10, enemigo.y-10])
			elif timer_planeta2 <= 600:
				screen.blit(neptuno4, [enemigo.x-10, enemigo.y-10])
			else:
				screen.blit(neptuno5, [enemigo.x-10, enemigo.y-10])
				if timer_planeta2 >= 750:
					timer_planeta2 = 0
			screen.blit(diamante, [diamante1.x-35, diamante1.y-20])
			screen.blit(diamante, [diamante2.x-35, diamante2.y-20])
		
		if plataforma.vidas <= 0:
			finish("enemigo", p1, name[p2], enemigo_color, tourney, cont)

		if enemigo.vidas <= 0:
			finish("plataforma", p1, name[p1], plataforma_color, tourney, cont)

		for evento in event.get():
			if evento.type==QUIT:
					quit()
					exit()
			if evento.type==KEYDOWN:
				if evento.key == K_ESCAPE:
					quit()
					exit()
		display.flip()

def finish(win, p1, name, color, tourney, cont):
	while True:
		FINISH_MOUSE_POS = mouse.get_pos()

		WIN_TEXT = get_font(75).render(name + " WINS", True, color)
		WIN_RECT = WIN_TEXT.get_rect(center=(640, 100))
		screen.blit(WIN_TEXT, WIN_RECT)

		if tourney == True:
			QUIT_BUTTON = Button(image=image.load("menu_assets/Options Rect.png"), pos=(640, 550), 
				text_input="CONTINUE", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
		else:
			QUIT_BUTTON = Button(image=image.load("menu_assets/Quit Rect.png"), pos=(640, 550), 
				text_input="QUIT", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))

		QUIT_BUTTON.changeColor(FINISH_MOUSE_POS)
		QUIT_BUTTON.update(screen)

		for evento in event.get():
			if evento.type == QUIT:
				quit()
				exit()
			if evento.type == MOUSEBUTTONDOWN:
				if QUIT_BUTTON.checkForInput(FINISH_MOUSE_POS):
					if QUIT_BUTTON.checkForInput(FINISH_MOUSE_POS) and win == "plataforma":
						if tourney == True:
							if cont == 1:
								semifinales(p1)
							elif cont == 2:
								final(p1)
							elif cont == 3:
								ganador(p1, name, color)
						else: select_player_vs()
					if QUIT_BUTTON.checkForInput(FINISH_MOUSE_POS) and win == "enemigo":
						if tourney == True: select_player_tourney()
						else: select_player_vs()

		display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = mouse.get_pos()

        screen.fill((255, 255, 255))

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, (0, 0, 0))
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color=(0, 0, 0), hovering_color=(0, 255, 0))

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for evento in event.get():
            if evento.type == QUIT:
                quit()
                exit()
            if evento.type == MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        display.update()

def main_menu(inicio):
    z = -1
    while True:
        global musica
        if z == -1 and inicio == True:
            mixer.music.set_volume(0.25)
            mixer.music.load('planetfighters_sounds/Menu.ogg')
            mixer.music.set_volume(mixer.music.get_volume())
            mixer.music.play(-1)
            musica = "Menu"
            inicio = False
            z = 0

        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = mouse.get_pos()

        MENU_TEXT = get_font(75).render("PLANET FIGHTERS", True, (178, 64, 182))
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=image.load("menu_assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        OPTIONS_BUTTON = Button(image=image.load("menu_assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        QUIT_BUTTON = Button(image=image.load("menu_assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for evento in event.get():
            if evento.type == QUIT:
                quit()
                exit()
            if evento.type == MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    select_mode()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    quit()
                    exit()
            if evento.type==KEYDOWN:
                if evento.key == K_ESCAPE:
                    quit()
                    exit()

        display.update()

def select_mode():
    z = -1
    while True:
        global musica
        if z == -1 and musica != "Menu":
            mixer.music.set_volume(0.25)
            mixer.music.load('planetfighters_sounds/Menu.ogg')
            mixer.music.set_volume(mixer.music.get_volume())
            mixer.music.play(-1)
            musica = "Menu"
            z = 0
		
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = mouse.get_pos()

        MENU_TEXT = get_font(75).render("SELECT MODE", True, (178, 64, 182))
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        VS_BUTTON = Button(image=image.load("menu_assets/Play Rect.png"), pos=(640, 250), 
                            text_input="1VS1", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        TOURNEY_BUTTON = Button(image=image.load("menu_assets/Options Rect.png"), pos=(640, 400), 
                            text_input="TOURNEY", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        QUIT_BUTTON = Button(image=image.load("menu_assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [VS_BUTTON, TOURNEY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for evento in event.get():
            if evento.type == QUIT:
                quit()
                exit()
            if evento.type == MOUSEBUTTONDOWN:
                if VS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    select_player_vs()
                if TOURNEY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    select_player_tourney()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #menu_main()
                    quit()
                    exit()
            if evento.type==KEYDOWN:
                if evento.key == K_ESCAPE:
                    main_menu(False)
        display.update()

def select_player_vs():
    timer_menu = 0
    p1 = ""
    p2 = ""
    z = -1
    while True:
        global musica
        if z == -1 and musica != "Menu":
            mixer.music.set_volume(0.25)
            mixer.music.load('planetfighters_sounds/Menu.ogg')
            mixer.music.set_volume(mixer.music.get_volume())
            mixer.music.play(-1)
            musica = "Menu"
            z = 0

        if p1 == p2:
            p2 = ""

        if p1 != "" and p2 != "":
            play(p1, p2, False, 0)
        
        screen.blit(BG2, (0, 0))

        MENU_MOUSE_POS = mouse.get_pos()

        screen.blit(marco_azul, (112, 40))
        screen.blit(marco_azul, (112, 380))
        screen.blit(marco_amarillo, (411, 40))
        screen.blit(marco_amarillo, (411, 380))
        screen.blit(marco_verde, (710, 40))
        screen.blit(marco_verde, (710, 380))
        screen.blit(marco_rojo, (1009, 40))
        screen.blit(marco_rojo, (1009, 380))

        MERCURIO_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(207, 317), 
                            text_input="MERCURY", font=get_font(20), base_color=(42, 66, 193), hovering_color=(162, 245, 247))
        VENUS_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(504, 317), 
                            text_input="VENUS", font=get_font(20), base_color=(238, 211, 71), hovering_color=(244, 237, 171))
        LATIERRA_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(803, 317), 
                            text_input="EARTH", font=get_font(20), base_color=(43, 192, 180), hovering_color=(160, 246, 181))
        MARTE_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(1102, 317), 
                            text_input="MARS", font=get_font(20), base_color=(255, 59, 60), hovering_color=(255, 126, 106))
        JUPITER_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(207, 657), 
                            text_input="JUPITER", font=get_font(20), base_color=(42, 66, 193), hovering_color=(162, 245, 247))
        SATURNO_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(504, 657), 
                            text_input="SATURN", font=get_font(20), base_color=(238, 211, 71), hovering_color=(244, 237, 171))
        URANO_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(803, 657), 
                            text_input="URANUS", font=get_font(20), base_color=(43, 192, 180), hovering_color=(160, 246, 181))
        NEPTUNO_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(1102, 657), 
                            text_input="NEPTUNE", font=get_font(20), base_color=(255, 59, 60), hovering_color=(255, 126, 106))

        timer_menu += 1

        if timer_menu <= 25:
            screen.blit(mercurio1, (180, 165))
        elif timer_menu <= 50:
            screen.blit(mercurio2, (180, 165))
        elif timer_menu <= 75:
            screen.blit(mercurio3, (180, 165))
        elif timer_menu <= 100:
            screen.blit(mercurio4, (180, 165))
        else:
            screen.blit(mercurio5, (180, 165))
            if timer_menu > 125:
                timer_menu = 0
        
        if timer_menu <= 25:
            screen.blit(jupiter1, (168, 493))
        elif timer_menu <= 50:
            screen.blit(jupiter2, (168, 493))
        elif timer_menu <= 75:
            screen.blit(jupiter3, (168, 493))
        elif timer_menu <= 100:
            screen.blit(jupiter4, (168, 493))
        else:
            screen.blit(jupiter5, (168, 493))
            if timer_menu > 125:
                timer_menu = 0
        
        if timer_menu <= 25:
            screen.blit(venus1, (467, 153))
        elif timer_menu <= 50:
            screen.blit(venus2, (467, 153))
        elif timer_menu <= 75:
            screen.blit(venus3, (467, 153))
        elif timer_menu <= 100:
            screen.blit(venus4, (467, 153))
        else:
            screen.blit(venus5, (467, 153))
            if timer_menu > 125:
                timer_menu = 0

        if timer_menu <= 25:
            screen.blit(saturno1, (442, 468))
        elif timer_menu <= 50:
            screen.blit(saturno2, (442, 468))
        elif timer_menu <= 75:
            screen.blit(saturno3, (442, 468))
        elif timer_menu <= 100:
            screen.blit(saturno4, (442, 468))
        else:
            screen.blit(saturno5, (442, 468))
            if timer_menu > 125:
                timer_menu = 0
	
        if timer_menu <= 25:
            screen.blit(latierra1, (766, 153))
        elif timer_menu <= 50:
            screen.blit(latierra2, (766, 153))
        elif timer_menu <= 75:
            screen.blit(latierra3, (766, 153))
        elif timer_menu <= 100:
            screen.blit(latierra4, (766, 153))
        else:
            screen.blit(latierra5, (766, 153))
            if timer_menu > 125:
                timer_menu = 0

        if timer_menu <= 25:
            screen.blit(urano1, (766, 493))
        elif timer_menu <= 50:
            screen.blit(urano2, (766, 493))
        elif timer_menu <= 75:
            screen.blit(urano3, (766, 493))
        elif timer_menu <= 100:
            screen.blit(urano4, (766, 493))
        else:
            screen.blit(urano5, (766, 493))
            if timer_menu > 125:
                timer_menu = 0

        if timer_menu <= 25:
            screen.blit(marte1, (1065, 153))
        elif timer_menu <= 50:
            screen.blit(marte2, (1065, 153))
        elif timer_menu <= 75:
            screen.blit(marte3, (1065, 153))
        elif timer_menu <= 100:
            screen.blit(marte4, (1065, 153))
        else:
            screen.blit(marte5, (1065, 153))
            if timer_menu > 125:
                timer_menu = 0

        if timer_menu <= 25:
            screen.blit(neptuno1, (1065, 493))
        elif timer_menu <= 50:
            screen.blit(neptuno2, (1065, 493))
        elif timer_menu <= 75:
            screen.blit(neptuno3, (1065, 493))
        elif timer_menu <= 100:
            screen.blit(neptuno4, (1065, 493))
        else:
            screen.blit(neptuno5, (1065, 493))
            if timer_menu > 125:
                timer_menu = 0

        for button in [MERCURIO_BUTTON, VENUS_BUTTON, LATIERRA_BUTTON, MARTE_BUTTON, JUPITER_BUTTON, SATURNO_BUTTON, URANO_BUTTON, NEPTUNO_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for evento in event.get():
            if evento.type == QUIT:
                quit()
                exit()
            if evento.type==KEYDOWN:
                if evento.key == K_ESCAPE:
                    select_mode()
            if evento.type == MOUSEBUTTONDOWN:
                if MERCURIO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Mercurio"
                    elif p2 == "": p2 = "Mercurio"
                if VENUS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Venus"
                    elif p2 == "": p2 = "Venus"
                if LATIERRA_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "La Tierra"
                    elif p2 == "": p2 = "La Tierra"
                if MARTE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Marte"
                    elif p2 == "": p2 = "Marte"
                if JUPITER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Jupiter"
                    elif p2 == "": p2 = "Jupiter"
                if SATURNO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Saturno"
                    elif p2 == "": p2 = "Saturno"
                if URANO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Urano"
                    elif p2 == "": p2 = "Urano"
                if NEPTUNO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Neptuno"
                    elif p2 == "": p2 = "Neptuno"
        display.update()

def select_player_tourney():
    timer_menu = 0
    p1 = ""
    z = -1
    while True:
        global musica
        if z == -1 and musica != "Menu":
            mixer.music.set_volume(0.25)
            mixer.music.load('planetfighters_sounds/Menu.ogg')
            mixer.music.set_volume(mixer.music.get_volume())
            mixer.music.play(-1)
            musica = "Menu"
            z = 0
        if p1 != "":
            cuartos(p1)
        
        screen.blit(BG2, (0, 0))

        MENU_MOUSE_POS = mouse.get_pos()

        screen.blit(marco_azul, (112, 40))
        screen.blit(marco_azul, (112, 380))
        screen.blit(marco_amarillo, (411, 40))
        screen.blit(marco_amarillo, (411, 380))
        screen.blit(marco_verde, (710, 40))
        screen.blit(marco_verde, (710, 380))
        screen.blit(marco_rojo, (1009, 40))
        screen.blit(marco_rojo, (1009, 380))

        MERCURIO_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(207, 317), 
                            text_input="MERCURY", font=get_font(20), base_color=(42, 66, 193), hovering_color=(162, 245, 247))
        VENUS_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(504, 317), 
                            text_input="VENUS", font=get_font(20), base_color=(238, 211, 71), hovering_color=(244, 237, 171))
        LATIERRA_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(803, 317), 
                            text_input="EARTH", font=get_font(20), base_color=(43, 192, 180), hovering_color=(160, 246, 181))
        MARTE_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(1102, 317), 
                            text_input="MARS", font=get_font(20), base_color=(255, 59, 60), hovering_color=(255, 126, 106))
        JUPITER_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(207, 657), 
                            text_input="JUPITER", font=get_font(20), base_color=(42, 66, 193), hovering_color=(162, 245, 247))
        SATURNO_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(504, 657), 
                            text_input="SATURN", font=get_font(20), base_color=(238, 211, 71), hovering_color=(244, 237, 171))
        URANO_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(803, 657), 
                            text_input="URANUS", font=get_font(20), base_color=(43, 192, 180), hovering_color=(160, 246, 181))
        NEPTUNO_BUTTON = Button(image=image.load("menu_assets/Marco Rect.png"), pos=(1102, 657), 
                            text_input="NEPTUNE", font=get_font(20), base_color=(255, 59, 60), hovering_color=(255, 126, 106))

        timer_menu += 1

        if timer_menu <= 25:
            screen.blit(mercurio1, (180, 165))
        elif timer_menu <= 50:
            screen.blit(mercurio2, (180, 165))
        elif timer_menu <= 75:
            screen.blit(mercurio3, (180, 165))
        elif timer_menu <= 100:
            screen.blit(mercurio4, (180, 165))
        else:
            screen.blit(mercurio5, (180, 165))
            if timer_menu > 125:
                timer_menu = 0
        
        if timer_menu <= 25:
            screen.blit(jupiter1, (168, 493))
        elif timer_menu <= 50:
            screen.blit(jupiter2, (168, 493))
        elif timer_menu <= 75:
            screen.blit(jupiter3, (168, 493))
        elif timer_menu <= 100:
            screen.blit(jupiter4, (168, 493))
        else:
            screen.blit(jupiter5, (168, 493))
            if timer_menu > 125:
                timer_menu = 0
        
        if timer_menu <= 25:
            screen.blit(venus1, (467, 153))
        elif timer_menu <= 50:
            screen.blit(venus2, (467, 153))
        elif timer_menu <= 75:
            screen.blit(venus3, (467, 153))
        elif timer_menu <= 100:
            screen.blit(venus4, (467, 153))
        else:
            screen.blit(venus5, (467, 153))
            if timer_menu > 125:
                timer_menu = 0

        if timer_menu <= 25:
            screen.blit(saturno1, (442, 468))
        elif timer_menu <= 50:
            screen.blit(saturno2, (442, 468))
        elif timer_menu <= 75:
            screen.blit(saturno3, (442, 468))
        elif timer_menu <= 100:
            screen.blit(saturno4, (442, 468))
        else:
            screen.blit(saturno5, (442, 468))
            if timer_menu > 125:
                timer_menu = 0
	
        if timer_menu <= 25:
            screen.blit(latierra1, (766, 153))
        elif timer_menu <= 50:
            screen.blit(latierra2, (766, 153))
        elif timer_menu <= 75:
            screen.blit(latierra3, (766, 153))
        elif timer_menu <= 100:
            screen.blit(latierra4, (766, 153))
        else:
            screen.blit(latierra5, (766, 153))
            if timer_menu > 125:
                timer_menu = 0

        if timer_menu <= 25:
            screen.blit(urano1, (766, 493))
        elif timer_menu <= 50:
            screen.blit(urano2, (766, 493))
        elif timer_menu <= 75:
            screen.blit(urano3, (766, 493))
        elif timer_menu <= 100:
            screen.blit(urano4, (766, 493))
        else:
            screen.blit(urano5, (766, 493))
            if timer_menu > 125:
                timer_menu = 0

        if timer_menu <= 25:
            screen.blit(marte1, (1065, 153))
        elif timer_menu <= 50:
            screen.blit(marte2, (1065, 153))
        elif timer_menu <= 75:
            screen.blit(marte3, (1065, 153))
        elif timer_menu <= 100:
            screen.blit(marte4, (1065, 153))
        else:
            screen.blit(marte5, (1065, 153))
            if timer_menu > 125:
                timer_menu = 0

        if timer_menu <= 25:
            screen.blit(neptuno1, (1065, 493))
        elif timer_menu <= 50:
            screen.blit(neptuno2, (1065, 493))
        elif timer_menu <= 75:
            screen.blit(neptuno3, (1065, 493))
        elif timer_menu <= 100:
            screen.blit(neptuno4, (1065, 493))
        else:
            screen.blit(neptuno5, (1065, 493))
            if timer_menu > 125:
                timer_menu = 0

        for button in [MERCURIO_BUTTON, VENUS_BUTTON, LATIERRA_BUTTON, MARTE_BUTTON, JUPITER_BUTTON, SATURNO_BUTTON, URANO_BUTTON, NEPTUNO_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for evento in event.get():
            if evento.type == QUIT:
                quit()
                exit()
            if evento.type==KEYDOWN:
                if evento.key == K_ESCAPE:
                    select_mode()
            if evento.type == MOUSEBUTTONDOWN:
                if MERCURIO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Mercurio"
                if VENUS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Venus"
                if LATIERRA_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "La Tierra"
                if MARTE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Marte"
                if JUPITER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Jupiter"
                if SATURNO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Saturno"
                if URANO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Urano"
                if NEPTUNO_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if p1 == "": p1 = "Neptuno"
        display.update()

def cuartos(p1):
    planetas = ["Mercurio", "Venus", "La Tierra", "Marte", "Jupiter", "Saturno", "Urano", "Neptuno"]
    planetas.remove(p1)
    p2 = choice(planetas)
    planetas.remove(p2)
    p3 = choice(planetas)
    planetas.remove(p3)
    p4 = choice(planetas)
    planetas.remove(p4)
    p5 = choice(planetas)
    planetas.remove(p5)
    p6 = choice(planetas)
    planetas.remove(p6)
    p7 = choice(planetas)
    planetas.remove(p7)
    p8 = choice(planetas)
    planetas.remove(p8)
    images1 = {"Mercurio": mercurio1, "Venus": venus1, "La Tierra": latierra1, "Marte": marte1, "Jupiter": jupiter1, "Saturno": saturno1, "Urano": urano1, "Neptuno":  neptuno1}
    images2 = {"Mercurio": mercurio2, "Venus": venus2, "La Tierra": latierra2, "Marte": marte2, "Jupiter": jupiter2, "Saturno": saturno2, "Urano": urano2, "Neptuno":  neptuno2}
    images3 = {"Mercurio": mercurio3, "Venus": venus3, "La Tierra": latierra3, "Marte": marte3, "Jupiter": jupiter3, "Saturno": saturno3, "Urano": urano3, "Neptuno":  neptuno3}
    images4 = {"Mercurio": mercurio4, "Venus": venus4, "La Tierra": latierra4, "Marte": marte4, "Jupiter": jupiter4, "Saturno": saturno4, "Urano": urano4, "Neptuno":  neptuno4}
    images5 = {"Mercurio": mercurio5, "Venus": venus5, "La Tierra": latierra5, "Marte": marte5, "Jupiter": jupiter5, "Saturno": saturno5, "Urano": urano5, "Neptuno":  neptuno5}    
    images_x1 = {"Mercurio": 62, "Venus": 50, "La Tierra": 50, "Marte": 50, "Jupiter": 50, "Saturno": 25, "Urano": 50, "Neptuno":  50}
    images_x2 = {"Mercurio": 1162, "Venus": 1150, "La Tierra": 1150, "Marte": 1150, "Jupiter": 1150, "Saturno": 1125, "Urano": 1150, "Neptuno":  1150}
    images_y1 = {"Mercurio": 62, "Venus": 50, "La Tierra": 50, "Marte": 50, "Jupiter": 50, "Saturno": 25, "Urano": 50, "Neptuno":  50}
    images_y2 = {"Mercurio": 245, "Venus": 233, "La Tierra": 233, "Marte": 233, "Jupiter": 233, "Saturno": 208, "Urano": 233, "Neptuno":  233}
    images_y3 = {"Mercurio": 429, "Venus": 417, "La Tierra": 417, "Marte": 417, "Jupiter": 417, "Saturno": 392, "Urano": 417, "Neptuno":  417}
    images_y4 = {"Mercurio": 612, "Venus": 600, "La Tierra": 600, "Marte": 600, "Jupiter": 600, "Saturno": 575, "Urano": 600, "Neptuno":  600}
    timer_menu = 0
    z = -1
    while True:
        global pq, musica

        if z == -1:
            if musica != "Menu":
                mixer.music.set_volume(0.25)
                mixer.music.load('planetfighters_sounds/Menu.ogg')
                mixer.music.set_volume(mixer.music.get_volume())
                mixer.music.play(-1)
                musica = "Menu"
            pq = [p1, p2, p3, p4, p5, p6, p7, p8]
            z = 0

        screen.blit(BG3, (0, 0))

        MENU_MOUSE_POS = mouse.get_pos()

        PLAY_BUTTON = Button(image=image.load("menu_assets/Play Rect.png"), pos=(640, 550), 
                            text_input="PLAY", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        
        screen.blit(linea1, (37, 130))
        screen.blit(linea2, (87, 130))
        screen.blit(linea1, (37, 497))
        screen.blit(linea2, (87, 497))
        screen.blit(linea1, (1137, 130))
        screen.blit(linea2, (1087, 130))
        screen.blit(linea1, (1137, 497))
        screen.blit(linea2, (1087, 497))

        timer_menu += 1

        if timer_menu <= 75:
            screen.blit(images1[p1], (images_x1[p1], images_y1[p1]))
            screen.blit(images1[p2], (images_x1[p2], images_y2[p2]))
            screen.blit(images1[p3], (images_x1[p3], images_y3[p3]))
            screen.blit(images1[p4], (images_x1[p4], images_y4[p4]))
            screen.blit(images1[p5], (images_x2[p5], images_y1[p5]))
            screen.blit(images1[p6], (images_x2[p6], images_y2[p6]))
            screen.blit(images1[p7], (images_x2[p7], images_y3[p7]))
            screen.blit(images1[p8], (images_x2[p8], images_y4[p8]))
        elif timer_menu <= 150:
            screen.blit(images2[p1], (images_x1[p1], images_y1[p1]))
            screen.blit(images2[p2], (images_x1[p2], images_y2[p2]))
            screen.blit(images2[p3], (images_x1[p3], images_y3[p3]))
            screen.blit(images2[p4], (images_x1[p4], images_y4[p4]))
            screen.blit(images2[p5], (images_x2[p5], images_y1[p5]))
            screen.blit(images2[p6], (images_x2[p6], images_y2[p6]))
            screen.blit(images2[p7], (images_x2[p7], images_y3[p7]))
            screen.blit(images2[p8], (images_x2[p8], images_y4[p8]))
        elif timer_menu <= 225:
            screen.blit(images3[p1], (images_x1[p1], images_y1[p1]))
            screen.blit(images3[p2], (images_x1[p2], images_y2[p2]))
            screen.blit(images3[p3], (images_x1[p3], images_y3[p3]))
            screen.blit(images3[p4], (images_x1[p4], images_y4[p4]))
            screen.blit(images3[p5], (images_x2[p5], images_y1[p5]))
            screen.blit(images3[p6], (images_x2[p6], images_y2[p6]))
            screen.blit(images3[p7], (images_x2[p7], images_y3[p7]))
            screen.blit(images3[p8], (images_x2[p8], images_y4[p8]))
        elif timer_menu <= 300:
            screen.blit(images4[p1], (images_x1[p1], images_y1[p1]))
            screen.blit(images4[p2], (images_x1[p2], images_y2[p2]))
            screen.blit(images4[p3], (images_x1[p3], images_y3[p3]))
            screen.blit(images4[p4], (images_x1[p4], images_y4[p4]))
            screen.blit(images4[p5], (images_x2[p5], images_y1[p5]))
            screen.blit(images4[p6], (images_x2[p6], images_y2[p6]))
            screen.blit(images4[p7], (images_x2[p7], images_y3[p7]))
            screen.blit(images4[p8], (images_x2[p8], images_y4[p8]))
        else:
            screen.blit(images5[p1], (images_x1[p1], images_y1[p1]))
            screen.blit(images5[p2], (images_x1[p2], images_y2[p2]))
            screen.blit(images5[p3], (images_x1[p3], images_y3[p3]))
            screen.blit(images5[p4], (images_x1[p4], images_y4[p4]))
            screen.blit(images5[p5], (images_x2[p5], images_y1[p5]))
            screen.blit(images5[p6], (images_x2[p6], images_y2[p6]))
            screen.blit(images5[p7], (images_x2[p7], images_y3[p7]))
            screen.blit(images5[p8], (images_x2[p8], images_y4[p8]))
            if timer_menu > 375:
                timer_menu = 0

        for button in [PLAY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for evento in event.get():
            if evento.type == QUIT:
                quit()
                exit()
            if evento.type == MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play(p1, p2, True, 1)
            if evento.type==KEYDOWN:
                if evento.key == K_ESCAPE:
                    main_menu(False)
        display.update()

def semifinales(p1):
	global pq, musica
	p2 = choice([pq[2], pq[3]])
	p3 = choice([pq[4], pq[5]])
	p4 = choice([pq[6], pq[7]])
	images1 = {"Mercurio": mercurio1, "Venus": venus1, "La Tierra": latierra1, "Marte": marte1, "Jupiter": jupiter1, "Saturno": saturno1, "Urano": urano1, "Neptuno":  neptuno1}
	images2 = {"Mercurio": mercurio2, "Venus": venus2, "La Tierra": latierra2, "Marte": marte2, "Jupiter": jupiter2, "Saturno": saturno2, "Urano": urano2, "Neptuno":  neptuno2}
	images3 = {"Mercurio": mercurio3, "Venus": venus3, "La Tierra": latierra3, "Marte": marte3, "Jupiter": jupiter3, "Saturno": saturno3, "Urano": urano3, "Neptuno":  neptuno3}
	images4 = {"Mercurio": mercurio4, "Venus": venus4, "La Tierra": latierra4, "Marte": marte4, "Jupiter": jupiter4, "Saturno": saturno4, "Urano": urano4, "Neptuno":  neptuno4}
	images5 = {"Mercurio": mercurio5, "Venus": venus5, "La Tierra": latierra5, "Marte": marte5, "Jupiter": jupiter5, "Saturno": saturno5, "Urano": urano5, "Neptuno":  neptuno5}    
	images_x1 = {"Mercurio": 62, "Venus": 50, "La Tierra": 50, "Marte": 50, "Jupiter": 50, "Saturno": 25, "Urano": 50, "Neptuno":  50}
	images_x2 = {"Mercurio": 1162, "Venus": 1150, "La Tierra": 1150, "Marte": 1150, "Jupiter": 1150, "Saturno": 1125, "Urano": 1150, "Neptuno":  1150}
	images_y1 = {"Mercurio": 62, "Venus": 50, "La Tierra": 50, "Marte": 50, "Jupiter": 50, "Saturno": 25, "Urano": 50, "Neptuno":  50}
	images_y2 = {"Mercurio": 245, "Venus": 233, "La Tierra": 233, "Marte": 233, "Jupiter": 233, "Saturno": 208, "Urano": 233, "Neptuno":  233}
	images_y3 = {"Mercurio": 429, "Venus": 417, "La Tierra": 417, "Marte": 417, "Jupiter": 417, "Saturno": 392, "Urano": 417, "Neptuno":  417}
	images_y4 = {"Mercurio": 612, "Venus": 600, "La Tierra": 600, "Marte": 600, "Jupiter": 600, "Saturno": 575, "Urano": 600, "Neptuno":  600}
	images_x11 = {"Mercurio": 212, "Venus": 200, "La Tierra": 200, "Marte": 200, "Jupiter": 200, "Saturno": 175, "Urano": 200, "Neptuno":  200}
	images_x22 = {"Mercurio": 1012, "Venus": 1000, "La Tierra": 1000, "Marte": 1000, "Jupiter": 1000, "Saturno": 975, "Urano": 1000, "Neptuno":  1000}
	images_y11 = {"Mercurio": 165, "Venus": 153, "La Tierra": 153, "Marte": 153, "Jupiter": 153, "Saturno": 128, "Urano": 153, "Neptuno":  153}
	images_y22 = {"Mercurio": 532, "Venus": 520, "La Tierra": 520, "Marte": 520, "Jupiter": 520, "Saturno": 495, "Urano": 520, "Neptuno":  520}
	timer_menu = 0
	z = -1
	while True:
		global ps

		if z == -1:
			if musica != "Menu":
				mixer.music.set_volume(0.25)
				mixer.music.load('planetfighters_sounds/Menu.ogg')
				mixer.music.set_volume(mixer.music.get_volume())
				mixer.music.play(-1)
				musica = "Menu"
			ps = [p1, p2, p3, p4]
			z = 0

		screen.blit(BG3, (0, 0))

		MENU_MOUSE_POS = mouse.get_pos()

		PLAY_BUTTON = Button(image=image.load("menu_assets/Play Rect.png"), pos=(640, 550), 
						text_input="PLAY", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        
		screen.blit(linea1, (37, 130))
		screen.blit(linea2, (87, 130))
		screen.blit(linea1, (37, 497))
		screen.blit(linea2, (87, 497))
		screen.blit(linea1, (1137, 130))
		screen.blit(linea2, (1087, 130))
		screen.blit(linea1, (1137, 497))
		screen.blit(linea2, (1087, 497))

		screen.blit(images1[pq[0]], (images_x1[pq[0]], images_y1[pq[0]]))
		screen.blit(images1[pq[1]], (images_x1[pq[1]], images_y2[pq[1]]))
		screen.blit(images1[pq[2]], (images_x1[pq[2]], images_y3[pq[2]]))
		screen.blit(images1[pq[3]], (images_x1[pq[3]], images_y4[pq[3]]))
		screen.blit(images1[pq[4]], (images_x2[pq[4]], images_y1[pq[4]]))
		screen.blit(images1[pq[5]], (images_x2[pq[5]], images_y2[pq[5]]))
		screen.blit(images1[pq[6]], (images_x2[pq[6]], images_y3[pq[6]]))
		screen.blit(images1[pq[7]], (images_x2[pq[7]], images_y4[pq[7]]))

		screen.blit(linea1, (187, 233))
		screen.blit(linea1, (187, 333))
		screen.blit(linea1, (187, 417))
		screen.blit(linea2, (237, 325))
		screen.blit(linea1, (987, 233))
		screen.blit(linea1, (987, 333))
		screen.blit(linea1, (987, 417))
		screen.blit(linea2, (937, 325))

		timer_menu += 1

		if timer_menu <= 75:
			screen.blit(images1[p1], (images_x11[p1], images_y11[p1]))
			screen.blit(images1[p2], (images_x11[p2], images_y22[p2]))
			screen.blit(images1[p3], (images_x22[p3], images_y11[p3]))
			screen.blit(images1[p4], (images_x22[p4], images_y22[p4]))
		elif timer_menu <= 150:
			screen.blit(images2[p1], (images_x11[p1], images_y11[p1]))
			screen.blit(images2[p2], (images_x11[p2], images_y22[p2]))
			screen.blit(images2[p3], (images_x22[p3], images_y11[p3]))
			screen.blit(images2[p4], (images_x22[p4], images_y22[p4]))
		elif timer_menu <= 225:
			screen.blit(images3[p1], (images_x11[p1], images_y11[p1]))
			screen.blit(images3[p2], (images_x11[p2], images_y22[p2]))
			screen.blit(images3[p3], (images_x22[p3], images_y11[p3]))
			screen.blit(images3[p4], (images_x22[p4], images_y22[p4]))
		elif timer_menu <= 300:
			screen.blit(images4[p1], (images_x11[p1], images_y11[p1]))
			screen.blit(images4[p2], (images_x11[p2], images_y22[p2]))
			screen.blit(images4[p3], (images_x22[p3], images_y11[p3]))
			screen.blit(images4[p4], (images_x22[p4], images_y22[p4]))
		else:
			screen.blit(images5[p1], (images_x11[p1], images_y11[p1]))
			screen.blit(images5[p2], (images_x11[p2], images_y22[p2]))
			screen.blit(images5[p3], (images_x22[p3], images_y11[p3]))
			screen.blit(images5[p4], (images_x22[p4], images_y22[p4]))
			if timer_menu > 375:
				timer_menu = 0

		for button in [PLAY_BUTTON]:
			button.changeColor(MENU_MOUSE_POS)
			button.update(screen)
        
		for evento in event.get():
			if evento.type == QUIT:
				quit()
				exit()
			if evento.type == MOUSEBUTTONDOWN:
				if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
					play(p1, p2, True, 2)
			if evento.type==KEYDOWN:
				if evento.key == K_ESCAPE:
					main_menu(False)
		display.update()

def final(p1):
	global pq, ps, musica
	p2 = choice([ps[2], ps[3]])
	images1 = {"Mercurio": mercurio1, "Venus": venus1, "La Tierra": latierra1, "Marte": marte1, "Jupiter": jupiter1, "Saturno": saturno1, "Urano": urano1, "Neptuno":  neptuno1}
	images2 = {"Mercurio": mercurio2, "Venus": venus2, "La Tierra": latierra2, "Marte": marte2, "Jupiter": jupiter2, "Saturno": saturno2, "Urano": urano2, "Neptuno":  neptuno2}
	images3 = {"Mercurio": mercurio3, "Venus": venus3, "La Tierra": latierra3, "Marte": marte3, "Jupiter": jupiter3, "Saturno": saturno3, "Urano": urano3, "Neptuno":  neptuno3}
	images4 = {"Mercurio": mercurio4, "Venus": venus4, "La Tierra": latierra4, "Marte": marte4, "Jupiter": jupiter4, "Saturno": saturno4, "Urano": urano4, "Neptuno":  neptuno4}
	images5 = {"Mercurio": mercurio5, "Venus": venus5, "La Tierra": latierra5, "Marte": marte5, "Jupiter": jupiter5, "Saturno": saturno5, "Urano": urano5, "Neptuno":  neptuno5}    
	images_x1 = {"Mercurio": 62, "Venus": 50, "La Tierra": 50, "Marte": 50, "Jupiter": 50, "Saturno": 25, "Urano": 50, "Neptuno":  50}
	images_x2 = {"Mercurio": 1162, "Venus": 1150, "La Tierra": 1150, "Marte": 1150, "Jupiter": 1150, "Saturno": 1125, "Urano": 1150, "Neptuno":  1150}
	images_y1 = {"Mercurio": 62, "Venus": 50, "La Tierra": 50, "Marte": 50, "Jupiter": 50, "Saturno": 25, "Urano": 50, "Neptuno":  50}
	images_y2 = {"Mercurio": 245, "Venus": 233, "La Tierra": 233, "Marte": 233, "Jupiter": 233, "Saturno": 208, "Urano": 233, "Neptuno":  233}
	images_y3 = {"Mercurio": 429, "Venus": 417, "La Tierra": 417, "Marte": 417, "Jupiter": 417, "Saturno": 392, "Urano": 417, "Neptuno":  417}
	images_y4 = {"Mercurio": 612, "Venus": 600, "La Tierra": 600, "Marte": 600, "Jupiter": 600, "Saturno": 575, "Urano": 600, "Neptuno":  600}
	images_x11 = {"Mercurio": 212, "Venus": 200, "La Tierra": 200, "Marte": 200, "Jupiter": 200, "Saturno": 175, "Urano": 200, "Neptuno":  200}
	images_x22 = {"Mercurio": 1012, "Venus": 1000, "La Tierra": 1000, "Marte": 1000, "Jupiter": 1000, "Saturno": 975, "Urano": 1000, "Neptuno":  1000}
	images_y11 = {"Mercurio": 165, "Venus": 153, "La Tierra": 153, "Marte": 153, "Jupiter": 153, "Saturno": 128, "Urano": 153, "Neptuno":  153}
	images_y22 = {"Mercurio": 532, "Venus": 520, "La Tierra": 520, "Marte": 520, "Jupiter": 520, "Saturno": 495, "Urano": 520, "Neptuno":  520}
	images_x111 = {"Mercurio": 362, "Venus": 350, "La Tierra": 350, "Marte": 350, "Jupiter": 350, "Saturno": 325, "Urano": 350, "Neptuno":  350}
	images_x222 = {"Mercurio": 862, "Venus": 850, "La Tierra": 850, "Marte": 850, "Jupiter": 850, "Saturno": 825, "Urano": 850, "Neptuno":  850}
	images_y111 = {"Mercurio": 348, "Venus": 336, "La Tierra": 336, "Marte": 336, "Jupiter": 336, "Saturno": 311, "Urano": 336, "Neptuno":  336}
	timer_menu = 0
	z = -1
	while True:
		global pf

		if z == -1:
			if musica != "Menu":
				mixer.music.set_volume(0.25)
				mixer.music.load('planetfighters_sounds/Menu.ogg')
				mixer.music.set_volume(mixer.music.get_volume())
				mixer.music.play(-1)
				musica = "Menu"
			pf = [p1, p2]
			z = 0

		screen.blit(BG3, (0, 0))

		MENU_MOUSE_POS = mouse.get_pos()

		PLAY_BUTTON = Button(image=image.load("menu_assets/Play Rect.png"), pos=(640, 550), 
						text_input="PLAY", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        
		screen.blit(linea1, (37, 130))
		screen.blit(linea2, (87, 130))
		screen.blit(linea1, (37, 497))
		screen.blit(linea2, (87, 497))
		screen.blit(linea1, (1137, 130))
		screen.blit(linea2, (1087, 130))
		screen.blit(linea1, (1137, 497))
		screen.blit(linea2, (1087, 497))

		screen.blit(images1[pq[0]], (images_x1[pq[0]], images_y1[pq[0]]))
		screen.blit(images1[pq[1]], (images_x1[pq[1]], images_y2[pq[1]]))
		screen.blit(images1[pq[2]], (images_x1[pq[2]], images_y3[pq[2]]))
		screen.blit(images1[pq[3]], (images_x1[pq[3]], images_y4[pq[3]]))
		screen.blit(images1[pq[4]], (images_x2[pq[4]], images_y1[pq[4]]))
		screen.blit(images1[pq[5]], (images_x2[pq[5]], images_y2[pq[5]]))
		screen.blit(images1[pq[6]], (images_x2[pq[6]], images_y3[pq[6]]))
		screen.blit(images1[pq[7]], (images_x2[pq[7]], images_y4[pq[7]]))

		screen.blit(linea1, (187, 233))
		screen.blit(linea1, (187, 333))
		screen.blit(linea1, (187, 417))
		screen.blit(linea2, (237, 325))
		screen.blit(linea1, (987, 233))
		screen.blit(linea1, (987, 333))
		screen.blit(linea1, (987, 417))
		screen.blit(linea2, (937, 325))

		screen.blit(images1[ps[0]], (images_x11[ps[0]], images_y11[ps[0]]))
		screen.blit(images1[ps[1]], (images_x11[ps[1]], images_y22[ps[1]]))
		screen.blit(images1[ps[2]], (images_x22[ps[2]], images_y11[ps[2]]))
		screen.blit(images1[ps[3]], (images_x22[ps[3]], images_y22[ps[3]]))

		screen.blit(linea2, (438, 325))
		screen.blit(linea2, (538, 325))
		screen.blit(linea2, (638, 325))
		screen.blit(linea2, (738, 325))
		screen.blit(linea1, (588, 275))

		timer_menu += 1

		if timer_menu <= 75:
			screen.blit(images1[p1], (images_x111[p1], images_y111[p1]))
			screen.blit(images1[p2], (images_x222[p2], images_y111[p2]))
		elif timer_menu <= 150:
			screen.blit(images2[p1], (images_x111[p1], images_y111[p1]))
			screen.blit(images2[p2], (images_x222[p2], images_y111[p2]))
		elif timer_menu <= 225:
			screen.blit(images3[p1], (images_x111[p1], images_y111[p1]))
			screen.blit(images3[p2], (images_x222[p2], images_y111[p2]))
		elif timer_menu <= 300:
			screen.blit(images4[p1], (images_x111[p1], images_y111[p1]))
			screen.blit(images4[p2], (images_x222[p2], images_y111[p2]))
		else:
			screen.blit(images5[p1], (images_x111[p1], images_y111[p1]))
			screen.blit(images5[p2], (images_x222[p2], images_y111[p2]))
			if timer_menu > 375:
				timer_menu = 0

		for button in [PLAY_BUTTON]:
			button.changeColor(MENU_MOUSE_POS)
			button.update(screen)
        
		for evento in event.get():
			if evento.type == QUIT:
				quit()
				exit()
			if evento.type == MOUSEBUTTONDOWN:
				if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
					play(p1, p2, True, 3)
			if evento.type==KEYDOWN:
				if evento.key == K_ESCAPE:
					main_menu(False)
		display.update()

def ganador(p1, name, color):
	global pq, ps, pf, musica
	images1 = {"Mercurio": mercurio1, "Venus": venus1, "La Tierra": latierra1, "Marte": marte1, "Jupiter": jupiter1, "Saturno": saturno1, "Urano": urano1, "Neptuno":  neptuno1}
	images2 = {"Mercurio": mercurio2, "Venus": venus2, "La Tierra": latierra2, "Marte": marte2, "Jupiter": jupiter2, "Saturno": saturno2, "Urano": urano2, "Neptuno":  neptuno2}
	images3 = {"Mercurio": mercurio3, "Venus": venus3, "La Tierra": latierra3, "Marte": marte3, "Jupiter": jupiter3, "Saturno": saturno3, "Urano": urano3, "Neptuno":  neptuno3}
	images4 = {"Mercurio": mercurio4, "Venus": venus4, "La Tierra": latierra4, "Marte": marte4, "Jupiter": jupiter4, "Saturno": saturno4, "Urano": urano4, "Neptuno":  neptuno4}
	images5 = {"Mercurio": mercurio5, "Venus": venus5, "La Tierra": latierra5, "Marte": marte5, "Jupiter": jupiter5, "Saturno": saturno5, "Urano": urano5, "Neptuno":  neptuno5}    
	images_x1 = {"Mercurio": 62, "Venus": 50, "La Tierra": 50, "Marte": 50, "Jupiter": 50, "Saturno": 25, "Urano": 50, "Neptuno":  50}
	images_x2 = {"Mercurio": 1162, "Venus": 1150, "La Tierra": 1150, "Marte": 1150, "Jupiter": 1150, "Saturno": 1125, "Urano": 1150, "Neptuno":  1150}
	images_y1 = {"Mercurio": 62, "Venus": 50, "La Tierra": 50, "Marte": 50, "Jupiter": 50, "Saturno": 25, "Urano": 50, "Neptuno":  50}
	images_y2 = {"Mercurio": 245, "Venus": 233, "La Tierra": 233, "Marte": 233, "Jupiter": 233, "Saturno": 208, "Urano": 233, "Neptuno":  233}
	images_y3 = {"Mercurio": 429, "Venus": 417, "La Tierra": 417, "Marte": 417, "Jupiter": 417, "Saturno": 392, "Urano": 417, "Neptuno":  417}
	images_y4 = {"Mercurio": 612, "Venus": 600, "La Tierra": 600, "Marte": 600, "Jupiter": 600, "Saturno": 575, "Urano": 600, "Neptuno":  600}
	images_x11 = {"Mercurio": 212, "Venus": 200, "La Tierra": 200, "Marte": 200, "Jupiter": 200, "Saturno": 175, "Urano": 200, "Neptuno":  200}
	images_x22 = {"Mercurio": 1012, "Venus": 1000, "La Tierra": 1000, "Marte": 1000, "Jupiter": 1000, "Saturno": 975, "Urano": 1000, "Neptuno":  1000}
	images_y11 = {"Mercurio": 165, "Venus": 153, "La Tierra": 153, "Marte": 153, "Jupiter": 153, "Saturno": 128, "Urano": 153, "Neptuno":  153}
	images_y22 = {"Mercurio": 532, "Venus": 520, "La Tierra": 520, "Marte": 520, "Jupiter": 520, "Saturno": 495, "Urano": 520, "Neptuno":  520}
	images_x111 = {"Mercurio": 362, "Venus": 350, "La Tierra": 350, "Marte": 350, "Jupiter": 350, "Saturno": 325, "Urano": 350, "Neptuno":  350}
	images_x222 = {"Mercurio": 862, "Venus": 850, "La Tierra": 850, "Marte": 850, "Jupiter": 850, "Saturno": 825, "Urano": 850, "Neptuno":  850}
	images_y111 = {"Mercurio": 348, "Venus": 336, "La Tierra": 336, "Marte": 336, "Jupiter": 336, "Saturno": 311, "Urano": 336, "Neptuno":  336}
	images_x1111 = {"Mercurio": 612, "Venus": 600, "La Tierra": 600, "Marte": 600, "Jupiter": 600, "Saturno": 575, "Urano": 600, "Neptuno":  600}
	images_y1111 = {"Mercurio": 200, "Venus": 187, "La Tierra": 187, "Marte": 187, "Jupiter": 187, "Saturno": 162, "Urano": 187, "Neptuno":  187}	
	timer_menu = 0
	z = -1
	while True:
		if z == -1:
			if musica != "Win":
				mixer.music.set_volume(0.25)
				mixer.music.load('planetfighters_sounds/Win.ogg')
				mixer.music.set_volume(mixer.music.get_volume())
				mixer.music.play(-1)
				musica = "Win"
			z = 0

		screen.blit(BG3, (0, 0))

		MENU_MOUSE_POS = mouse.get_pos()

		QUIT_BUTTON = Button(image=image.load("menu_assets/Quit Rect.png"), pos=(640, 550), 
							text_input="QUIT", font=get_font(75), base_color=(215, 252, 212), hovering_color=(255, 255, 255))
        
		screen.blit(linea1, (37, 130))
		screen.blit(linea2, (87, 130))
		screen.blit(linea1, (37, 497))
		screen.blit(linea2, (87, 497))
		screen.blit(linea1, (1137, 130))
		screen.blit(linea2, (1087, 130))
		screen.blit(linea1, (1137, 497))
		screen.blit(linea2, (1087, 497))

		screen.blit(images1[pq[0]], (images_x1[pq[0]], images_y1[pq[0]]))
		screen.blit(images1[pq[1]], (images_x1[pq[1]], images_y2[pq[1]]))
		screen.blit(images1[pq[2]], (images_x1[pq[2]], images_y3[pq[2]]))
		screen.blit(images1[pq[3]], (images_x1[pq[3]], images_y4[pq[3]]))
		screen.blit(images1[pq[4]], (images_x2[pq[4]], images_y1[pq[4]]))
		screen.blit(images1[pq[5]], (images_x2[pq[5]], images_y2[pq[5]]))
		screen.blit(images1[pq[6]], (images_x2[pq[6]], images_y3[pq[6]]))
		screen.blit(images1[pq[7]], (images_x2[pq[7]], images_y4[pq[7]]))

		screen.blit(linea1, (187, 233))
		screen.blit(linea1, (187, 333))
		screen.blit(linea1, (187, 417))
		screen.blit(linea2, (237, 325))
		screen.blit(linea1, (987, 233))
		screen.blit(linea1, (987, 333))
		screen.blit(linea1, (987, 417))
		screen.blit(linea2, (937, 325))

		screen.blit(images1[ps[0]], (images_x11[ps[0]], images_y11[ps[0]]))
		screen.blit(images1[ps[1]], (images_x11[ps[1]], images_y22[ps[1]]))
		screen.blit(images1[ps[2]], (images_x22[ps[2]], images_y11[ps[2]]))
		screen.blit(images1[ps[3]], (images_x22[ps[3]], images_y22[ps[3]]))

		screen.blit(linea2, (438, 325))
		screen.blit(linea2, (538, 325))
		screen.blit(linea2, (638, 325))
		screen.blit(linea2, (738, 325))
		screen.blit(linea1, (588, 275))

		screen.blit(images1[pf[0]], (images_x111[pf[0]], images_y111[pf[0]]))
		screen.blit(images1[pf[1]], (images_x222[pf[1]], images_y111[pf[1]]))

		WIN_TEXT = get_font(75).render(name + " WINS", True, color)
		WIN_RECT = WIN_TEXT.get_rect(center=(640, 100))
		screen.blit(WIN_TEXT, WIN_RECT)

		timer_menu += 1

		if timer_menu <= 75:
			screen.blit(images1[p1], (images_x1111[p1], images_y1111[p1]))
		elif timer_menu <= 150:
			screen.blit(images2[p1], (images_x1111[p1], images_y1111[p1]))
		elif timer_menu <= 225:
			screen.blit(images3[p1], (images_x1111[p1], images_y1111[p1]))
		elif timer_menu <= 300:
			screen.blit(images4[p1], (images_x1111[p1], images_y1111[p1]))
		else:
			screen.blit(images5[p1], (images_x1111[p1], images_y1111[p1]))
			if timer_menu > 375:
				timer_menu = 0

		for button in [QUIT_BUTTON]:
			button.changeColor(MENU_MOUSE_POS)
			button.update(screen)
        
		for evento in event.get():
			if evento.type == QUIT:
				quit()
				exit()
			if evento.type == MOUSEBUTTONDOWN:
				if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
					quit()
					exit()
			if evento.type==KEYDOWN:
				if evento.key == K_ESCAPE:
					main_menu(False)
		display.update()

main_menu(True)
