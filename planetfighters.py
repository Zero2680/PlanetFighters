from pygame import *
init()
from random import *
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
		if disparo1.puntuacion >= 200 and disparo2.x != 10000:
			disparo2.Movimiento(enemigo)
		if disparo1.puntuacion >= 300 and disparo3.x != 10000:
			disparo3.Movimiento(enemigo)

	#LA TIERRA
	def DispararTeledirigido(self, enemigo, disparo):			
		if enemigo.check_colisiones(disparo):
			enemigo.vidas -= 5
			disparo.x = 10000  
		if disparo.x != 10000:       
			disparo.MovimientoTeledirigido(enemigo)

	#VENUS
	def PonerTrampa(self, enemigo, trampa):
		if enemigo.check_colisiones(trampa):
			enemigo.vidas -= 3
			trampa.x = 10000
		trampa.DibujarObjeto()

	#URANO
	def DispararCongelacion(self, enemigo, disparo):
		if enemigo.check_colisiones(disparo):
			enemigo.vidas -= 3
			disparo.x = 10000
		if disparo.x != 10000:
			disparo.Movimiento(enemigo)
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
			self.puntuacion = 1
		secundaria.Movimiento(enemigo)
		Chocar(secundaria, enemigo)
		if self.color == (0,0,255):
			barra_hp_izquierda(screen, 50, 60, secundaria.vidas, plataforma_color)
		elif self.color == (255,0,0):
			barra_hp_derecha(screen, 1060, 60, secundaria.vidas, enemigo_color)

	#JUPITER
	def Aumentar(self, enemigo):
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
		if self.check_colisiones(enemigo):
			if self.ancho >= 65 and self.ancho < 80:
				enemigo.vidas -= 2.5
			elif self.ancho >= 80 and self.ancho < 100:
				enemigo.vidas -= 5
			elif self.ancho >= 100:
				enemigo.vidas -= 10
	
	#NEPTUNO
	def LluviaDeDiamantes(self, enemigo, diamante1, diamante2):
		diamante1.Movimiento_Diamante(enemigo)
		diamante2.Movimiento_Diamante(enemigo)

def Chocar(plataforma, enemigo):
	if plataforma.check_colisiones(enemigo):
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
		#if ((plataforma.x + plataforma.ancho) > enemigo.x and (plataforma.x + plataforma.ancho) < (enemigo.x + enemigo.ancho)) or ((enemigo.x + enemigo.ancho) > plataforma.x and (enemigo.x + enemigo.ancho) < (plataforma.x + plataforma.ancho)):
			#plataforma.direcciony = -plataforma.direcciony
			#enemigo.direcciony = -enemigo.direcciony


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

plataforma = Bola(300,350,55,55, 1, 1, 0, (0,0,255), 100, 0)
enemigo = Bola(940,350,55,55, 1, 1, 0, (255,0,0), 100, 1)
timer = 0
timer_plataforma = 0
timer_enemigo = 0
inicial = True
personaje1 = "Neptuno"
personaje2 = "Marte"
mercurio = transform.scale(image.load("planetfighters_images/Mercurio.png"), (75, 75))
secundaria_mercurio = transform.scale(image.load("planetfighters_images/Mercurio.png"), (50, 50))
minimercurio = transform.scale(image.load("planetfighters_images/Mercurio.png"), (25, 25))
venus = transform.scale(image.load("planetfighters_images/Venus.png"), (75, 75))
minivenus = transform.scale(image.load("planetfighters_images/Venus.png"), (25, 25))
latierra = transform.scale(image.load("planetfighters_images/LaTierra.png"), (75, 75))
minilatierra = transform.scale(image.load("planetfighters_images/LaTierra.png"), (25, 25))
marte = transform.scale(image.load("planetfighters_images/Marte.png"), (75, 75))
minimarte = transform.scale(image.load("planetfighters_images/Marte.png"), (25, 25))
jupiter = transform.scale(image.load("planetfighters_images/Jupiter.png"), (75, 75))
minijupiter = transform.scale(image.load("planetfighters_images/Jupiter.png"), (25, 25))
saturno = transform.scale(image.load("planetfighters_images/Saturno.png"), (125, 125))
minisaturno = transform.scale(image.load("planetfighters_images/Saturno.png"), (62, 62))
urano = transform.scale(image.load("planetfighters_images/Urano.png"), (75, 75))
miniurano = transform.scale(image.load("planetfighters_images/Urano.png"), (25, 25))
neptuno = transform.scale(image.load("planetfighters_images/Neptuno.png"), (75, 75))
minineptuno = transform.scale(image.load("planetfighters_images/Neptuno.png"), (25, 25))
space = transform.scale(image.load("planetfighters_images/Space.png").convert(), (1280, 720))
cohete1 = transform.scale(image.load("planetfighters_images/Cohete1.png"), (50, 50))
cohete2 = transform.scale(image.load("planetfighters_images/Cohete2.png"), (50, 50))
hielo1 = transform.scale(image.load("planetfighters_images/Hielo1.png"), (50, 50))
hielo2 = transform.scale(image.load("planetfighters_images/Hielo2.png"), (50, 50))
roca = transform.scale(image.load("planetfighters_images/Roca.png"), (30, 30))
saturno2 = transform.scale(image.load("planetfighters_images/Saturno2.png"), (125, 125))
totem = transform.scale(image.load("planetfighters_images/Totem.png"), (75, 75))
diamante = transform.scale(image.load("planetfighters_images/Diamante.png"), (75, 75))
barra = transform.scale(image.load("planetfighters_images/Bar.png"), (175, 20))
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

while True:
	screen.blit(space, [0, 0]) 
	
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
					plataforma_color = (138, 129, 120)
					secundaria_x = plataforma.x
					secundaria_y = plataforma.y
					secundaria_ancho = plataforma.ancho/2
					secundaria_largo = plataforma.largo/2
					secundaria_direccionx = -plataforma.direccionx
					secundaria_direcciony = -plataforma.direcciony
					secundaria_color = plataforma.color
				elif personaje2 == "Mercurio" and secundaria_x == 10001:
					minienemigo = minimercurio
					enemigo_color = (138, 129, 120)
					secundaria_x = enemigo.x
					secundaria_y = enemigo.y
					secundaria_ancho = enemigo.ancho/2
					secundaria_largo = enemigo.largo/2
					secundaria_direccionx = -enemigo.direccionx
					secundaria_direcciony = -enemigo.direcciony
					secundaria_color = enemigo.color
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

	if personaje1 == "Mercurio": 
		plataforma.Separarse(enemigo, secundaria)
		screen.blit(secundaria_mercurio, [plataforma.x-10, plataforma.y-10])
		screen.blit(secundaria_mercurio, [secundaria.x-10, secundaria.y-10])
	elif personaje1 == "Venus": 
		if timer_plataforma >= 0 and timer_plataforma <= 6000:
			plataforma.PonerTrampa(enemigo, trampa1)	
			if timer_plataforma >= 6000 and trampa1.x != 10000:
				trampa1.x = 10000
		if timer_plataforma >= 2000 and timer_plataforma <= 8000:
			plataforma.PonerTrampa(enemigo, trampa2)	
			if timer_plataforma >= 8000 and trampa2.x != 10000:
				trampa2.x = 10000
		if timer_plataforma >= 4000 and timer_plataforma <= 10000:
			plataforma.PonerTrampa(enemigo, trampa3)	
			if timer_plataforma >= 10000 and trampa3.x != 10000:
				trampa3.x = 10000
		if timer_plataforma >= 10000:
			timer_plataforma = 0
		screen.blit(venus, [plataforma.x-10, plataforma.y-10])
		if trampa1.x != 10000 and timer_plataforma >= 0:
			screen.blit(totem, [trampa1.x-25, trampa1.y-30])
		if trampa2.x != 10000 and timer_plataforma >= 2000:
			screen.blit(totem, [trampa2.x-25, trampa2.y-30])
		if trampa3.x != 10000 and timer_plataforma >= 4000:
			screen.blit(totem, [trampa3.x-25, trampa3.y-30])
	elif personaje1 == "La Tierra": 
		if timer_plataforma >= 0 and timer_plataforma <= 6000:
			plataforma.DispararTeledirigido(enemigo, disparo1)
			if timer_plataforma >= 6000 and disparo1.x != 10000:
				disparo1.x = 10000
		if timer_plataforma >= 2000 and timer_plataforma <= 8000:
			plataforma.DispararTeledirigido(enemigo, disparo2)
			if timer_plataforma >= 8000 and disparo2.x != 10000:
				disparo2.x = 10000
		if timer_plataforma >= 4000 and timer_plataforma <= 10000:
			plataforma.DispararTeledirigido(enemigo, disparo3)
			if timer_plataforma >= 10000 and disparo3.x != 10000:
				disparo3.x = 10000
		if timer_plataforma >= 10000:
			timer_plataforma = 0
		screen.blit(latierra, [plataforma.x-10, plataforma.y-10])
		if disparo1.x != 10000 and timer_plataforma >= 0:
			if disparo1.direccionx == -1:
				screen.blit(cohete2, [disparo1.x-15, disparo1.y-15])
			else:
				screen.blit(cohete1, [disparo1.x-15, disparo1.y-15])
		if disparo2.x != 10000 and timer_plataforma >= 2000:
			if disparo2.direccionx == -1:
				screen.blit(cohete2, [disparo2.x-15, disparo2.y-15])
			else:
				screen.blit(cohete1, [disparo2.x-15, disparo2.y-15])
		if disparo3.x != 10000 and timer_plataforma >= 4000:
			if disparo3.direccionx == -1:
				screen.blit(cohete2, [disparo3.x-15, disparo3.y-15])
			else:
				screen.blit(cohete1, [disparo3.x-15, disparo3.y-15])
	elif personaje1 == "Marte": 
		if timer_plataforma >= 0 and timer_plataforma <= 6000:
			plataforma.Disparar(enemigo, meteorito1, meteorito2, meteorito3)
			if timer_plataforma >= 6000 and (meteorito1.x != 10000 or meteorito2.x != 10000 or meteorito3.x != 10000):
				meteorito1.x = 10000
				meteorito2.x = 10000
				meteorito3.x = 10000
		if timer_plataforma >= 2000 and timer_plataforma <= 8000:
			plataforma.Disparar(enemigo, meteorito4, meteorito5, meteorito6)
			if timer_plataforma >= 8000 and (meteorito4.x != 10000 or meteorito5.x != 10000 or meteorito6.x != 10000):
				meteorito4.x = 10000
				meteorito5.x = 10000
				meteorito6.x = 10000
		if timer_plataforma >= 4000 and timer_plataforma <= 10000:
			plataforma.Disparar(enemigo, meteorito7, meteorito8, meteorito9)
			if timer_plataforma >= 10000 and (meteorito7.x != 10000 or meteorito8.x != 10000 or meteorito9.x != 10000):
				meteorito7.x = 10000
				meteorito8.x = 10000
				meteorito9.x = 10000
		if timer_plataforma >= 10000:
			timer_plataforma = 0
		screen.blit(marte, [plataforma.x-10, plataforma.y-10])
		if meteorito1.x != 10000 and timer_plataforma >= 0: screen.blit(roca, [meteorito1.x-10, meteorito1.y-10])
		if meteorito2.x != 10000 and timer_plataforma >= 0: screen.blit(roca, [meteorito2.x-10, meteorito2.y-10])
		if meteorito3.x != 10000 and timer_plataforma >= 0: screen.blit(roca, [meteorito3.x-10, meteorito3.y-10])
		if meteorito4.x != 10000 and timer_plataforma >= 2000: screen.blit(roca, [meteorito4.x-10, meteorito4.y-10])
		if meteorito5.x != 10000 and timer_plataforma >= 2000: screen.blit(roca, [meteorito5.x-10, meteorito5.y-10])
		if meteorito6.x != 10000 and timer_plataforma >= 2000: screen.blit(roca, [meteorito6.x-10, meteorito6.y-10])
		if meteorito7.x != 10000 and timer_plataforma >= 4000: screen.blit(roca, [meteorito7.x-10, meteorito7.y-10])
		if meteorito8.x != 10000 and timer_plataforma >= 4000: screen.blit(roca, [meteorito8.x-10, meteorito8.y-10])
		if meteorito9.x != 10000 and timer_plataforma >= 4000: screen.blit(roca, [meteorito9.x-10, meteorito9.y-10])
	elif personaje1 == "Jupiter": 
		plataforma.Aumentar(enemigo)
		screen.blit(jupiter, [plataforma.x-10, plataforma.y-10])
	elif personaje1 == "Saturno": 
		if timer_plataforma >= 3000:
			plataforma.GolpearEnArea(enemigo, area)
			screen.blit(saturno2, [plataforma.x-35, plataforma.y-35])
			if timer_plataforma >= 6000:
				timer_plataforma = 0
		screen.blit(saturno, [plataforma.x-35, plataforma.y-35])
	elif personaje1 == "Urano": 
		if timer_plataforma >= 0 and timer_plataforma <= 6000:
			plataforma.DispararCongelacion(enemigo, congelacion1)
			if timer_plataforma >= 6000 and congelacion1.x != 10000:
				congelacion1.x = 10000
		if timer_plataforma >= 2000 and timer_plataforma <= 8000:
			plataforma.DispararCongelacion(enemigo, congelacion2)
			if timer_plataforma >= 8000 and congelacion2.x != 10000:
				congelacion2.x = 10000
		if timer_plataforma >= 4000 and timer_plataforma <= 10000:
			plataforma.DispararCongelacion(enemigo, congelacion3)
			if timer_plataforma >= 10000 and congelacion3.x != 10000:
				congelacion3.x = 10000
		if timer_plataforma >= 10000:
			timer_plataforma = 0
		screen.blit(urano, [plataforma.x-10, plataforma.y-10])
		if congelacion1.x != 10000 and timer_plataforma >= 0:
			if congelacion1.direccionx == -1:
				screen.blit(hielo2, [congelacion1.x-17.5, congelacion1.y-15])
			else:
				screen.blit(hielo1, [congelacion1.x-12.5, congelacion1.y-15])
		if congelacion2.x != 10000 and timer_plataforma >= 2000:
			if congelacion2.direccionx == -1:
				screen.blit(hielo2, [congelacion2.x-17.5, congelacion2.y-15])
			else:
				screen.blit(hielo1, [congelacion2.x-12.5, congelacion2.y-15])
		if congelacion3.x != 10000 and timer_plataforma >= 4000:
			if congelacion3.direccionx == -1:
				screen.blit(hielo2, [congelacion3.x-17.5, congelacion3.y-15])
			else:
				screen.blit(hielo1, [congelacion3.x-12.5, congelacion3.y-15])
	elif personaje1 == "Neptuno": 
		plataforma.LluviaDeDiamantes(enemigo, diamante1, diamante2)
		screen.blit(neptuno, [plataforma.x-10, plataforma.y-10])
		screen.blit(diamante, [diamante1.x-35, diamante1.y-20])
		screen.blit(diamante, [diamante2.x-35, diamante2.y-20])

	if personaje2 == "Mercurio": 
		enemigo.Separarse(plataforma, secundaria)
		screen.blit(secundaria_mercurio, [enemigo.x-10, enemigo.y-10])
		screen.blit(secundaria_mercurio, [secundaria.x-10, secundaria.y-10])
	elif personaje2 == "Venus": 
		if timer_enemigo >= 0 and timer_enemigo <= 6000:
			enemigo.PonerTrampa(plataforma, trampa1)	
			if timer_enemigo >= 6000 and trampa1.x != 10000:
				trampa1.x = 10000
		if timer_enemigo >= 2000 and timer_enemigo <= 8000:
			enemigo.PonerTrampa(plataforma, trampa2)	
			if timer_enemigo >= 8000 and trampa2.x != 10000:
				trampa2.x = 10000
		if timer_enemigo >= 4000 and timer_enemigo <= 10000:
			enemigo.PonerTrampa(plataforma, trampa3)	
			if timer_enemigo >= 10000 and trampa3.x != 10000:
				trampa3.x = 10000
		if timer_enemigo >= 10000:
			timer_enemigo = 0
		screen.blit(venus, [enemigo.x-10, enemigo.y-10])
		if trampa1.x != 10000 and timer_enemigo >= 0:
			screen.blit(totem, [trampa1.x-25, trampa1.y-30])
		if trampa2.x != 10000 and timer_enemigo >= 2000:
			screen.blit(totem, [trampa2.x-25, trampa2.y-30])
		if trampa3.x != 10000 and timer_enemigo >= 4000:
			screen.blit(totem, [trampa3.x-25, trampa3.y-30])
	elif personaje2 == "La Tierra": 
		if timer_enemigo >= 0 and timer_enemigo <= 6000:
			enemigo.DispararTeledirigido(plataforma, disparo1)
			if timer_enemigo >= 6000 and disparo1.x != 10000:
				disparo1.x = 10000
		if timer_enemigo >= 2000 and timer_enemigo <= 8000:
			enemigo.DispararTeledirigido(plataforma, disparo2)
			if timer_enemigo >= 8000 and disparo2.x != 10000:
				disparo2.x = 10000
		if timer_enemigo >= 4000 and timer_enemigo <= 10000:
			enemigo.DispararTeledirigido(plataforma, disparo3)
			if timer_enemigo >= 10000 and disparo3.x != 10000:
				disparo3.x = 10000
		if timer_enemigo >= 10000:
			timer_enemigo = 0
		screen.blit(latierra, [enemigo.x-10, enemigo.y-10])
		if disparo1.x != 10000 and timer_enemigo >= 0:
			if disparo1.direccionx == -1:
				screen.blit(cohete2, [disparo1.x-15, disparo1.y-15])
			else:
				screen.blit(cohete1, [disparo1.x-15, disparo1.y-15])
		if disparo2.x != 10000 and timer_enemigo >= 2000:
			if disparo2.direccionx == -1:
				screen.blit(cohete2, [disparo2.x-15, disparo2.y-15])
			else:
				screen.blit(cohete1, [disparo2.x-15, disparo2.y-15])
		if disparo3.x != 10000 and timer_enemigo >= 4000:
			if disparo3.direccionx == -1:
				screen.blit(cohete2, [disparo3.x-15, disparo3.y-15])
			else:
				screen.blit(cohete1, [disparo3.x-15, disparo3.y-15])
	elif personaje2 == "Marte": 
		if timer_enemigo >= 0 and timer_enemigo <= 6000:
			enemigo.Disparar(plataforma, meteorito1, meteorito2, meteorito3)
			if timer_enemigo >= 6000 and (meteorito1.x != 10000 or meteorito2.x != 10000 or meteorito3.x != 10000):
				meteorito1.x = 10000
				meteorito2.x = 10000
				meteorito3.x = 10000
		if timer_enemigo >= 2000 and timer_enemigo <= 8000:
			enemigo.Disparar(plataforma, meteorito4, meteorito5, meteorito6)
			if timer_enemigo >= 8000 and (meteorito4.x != 10000 or meteorito5.x != 10000 or meteorito6.x != 10000):
				meteorito4.x = 10000
				meteorito5.x = 10000
				meteorito6.x = 10000
		if timer_enemigo >= 4000 and timer_enemigo <= 10000:
			enemigo.Disparar(plataforma, meteorito7, meteorito8, meteorito9)
			if timer_enemigo >= 10000 and (meteorito7.x != 10000 or meteorito8.x != 10000 or meteorito9.x != 10000):
				meteorito7.x = 10000
				meteorito8.x = 10000
				meteorito9.x = 10000
		if timer_enemigo >= 10000:
			timer_enemigo = 0
		screen.blit(marte, [enemigo.x-10, enemigo.y-10])
		if meteorito1.x != 10000 and timer_enemigo >= 0: screen.blit(roca, [meteorito1.x-10, meteorito1.y-10])
		if meteorito2.x != 10000 and timer_enemigo >= 0: screen.blit(roca, [meteorito2.x-10, meteorito2.y-10])
		if meteorito3.x != 10000 and timer_enemigo >= 0: screen.blit(roca, [meteorito3.x-10, meteorito3.y-10])
		if meteorito4.x != 10000 and timer_enemigo >= 2000: screen.blit(roca, [meteorito4.x-10, meteorito4.y-10])
		if meteorito5.x != 10000 and timer_enemigo >= 2000: screen.blit(roca, [meteorito5.x-10, meteorito5.y-10])
		if meteorito6.x != 10000 and timer_enemigo >= 2000: screen.blit(roca, [meteorito6.x-10, meteorito6.y-10])
		if meteorito7.x != 10000 and timer_enemigo >= 4000: screen.blit(roca, [meteorito7.x-10, meteorito7.y-10])
		if meteorito8.x != 10000 and timer_enemigo >= 4000: screen.blit(roca, [meteorito8.x-10, meteorito8.y-10])
		if meteorito9.x != 10000 and timer_enemigo >= 4000: screen.blit(roca, [meteorito9.x-10, meteorito9.y-10])
	elif personaje2 == "Jupiter": 
		enemigo.Aumentar(plataforma)
		screen.blit(jupiter, [enemigo.x-10, enemigo.y-10])
	elif personaje2 == "Saturno": 
		if timer_enemigo >= 3000:
			enemigo.GolpearEnArea(plataforma, area)
			screen.blit(saturno2, [enemigo.x-35, enemigo.y-35])
			if timer_enemigo >= 6000:
				timer_enemigo = 0
		screen.blit(saturno, [enemigo.x-35, enemigo.y-35])
	elif personaje2 == "Urano": 
		if timer_enemigo >= 0 and timer_enemigo <= 6000:
			enemigo.DispararCongelacion(plataforma, congelacion1)
			if timer_enemigo >= 6000 and congelacion1.x != 10000:
				congelacion1.x = 10000
		if timer_enemigo >= 2000 and timer_enemigo <= 8000:
			enemigo.DispararCongelacion(plataforma, congelacion2)
			if timer_enemigo >= 8000 and congelacion2.x != 10000:
				congelacion2.x = 10000
		if timer_enemigo >= 4000 and timer_enemigo <= 10000:
			enemigo.DispararCongelacion(plataforma, congelacion3)
			if timer_enemigo >= 10000 and congelacion3.x != 10000:
				congelacion3.x = 10000
		if timer_enemigo >= 10000:
			timer_enemigo = 0
		screen.blit(urano, [enemigo.x-10, enemigo.y-10])
		if congelacion1.x != 10000 and timer_enemigo >= 0:
			if congelacion1.direccionx == -1:
				screen.blit(hielo2, [congelacion1.x-17.5, congelacion1.y-15])
			else:
				screen.blit(hielo1, [congelacion1.x-12.5, congelacion1.y-15])
		if congelacion2.x != 10000 and timer_enemigo >= 2000:
			if congelacion2.direccionx == -1:
				screen.blit(hielo2, [congelacion2.x-17.5, congelacion2.y-15])
			else:
				screen.blit(hielo1, [congelacion2.x-12.5, congelacion2.y-15])
		if congelacion3.x != 10000 and timer_enemigo >= 4000:
			if congelacion3.direccionx == -1:
				screen.blit(hielo2, [congelacion3.x-17.5, congelacion3.y-15])
			else:
				screen.blit(hielo1, [congelacion3.x-12.5, congelacion3.y-15])
	elif personaje2 == "Neptuno": 
		enemigo.LluviaDeDiamantes(plataforma, diamante1, diamante2)
		screen.blit(neptuno, [enemigo.x-10, enemigo.y-10])
		screen.blit(diamante, [diamante1.x-35, diamante1.y-20])
		screen.blit(diamante, [diamante2.x-35, diamante2.y-20])

	for evento in event.get():
		if evento.type==QUIT:
				quit()
				exit()
		if evento.type==KEYDOWN:
			if evento.key == K_ESCAPE:
				quit()
				exit()
	display.flip()
