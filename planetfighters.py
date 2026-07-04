from pygame import *
init()
from random import *
screen = display.set_mode((1280, 720), FULLSCREEN)
display.set_caption('Ping Pong')
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
			elif self.x >= 1265:
				self.direccionx = -1
			if self.y <= 0:
				self.direcciony = 1
			elif self.y >= 700:
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
			elif self.y >= enemigo.x:
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
		self.puntuacion += 1
		if enemigo.check_colisiones(disparo1):
			enemigo.vidas -= 1
			disparo1.x = 10000
		if enemigo.check_colisiones(disparo2):
			enemigo.vidas -= 1
			disparo2.x = 10000
		if enemigo.check_colisiones(disparo3):
			enemigo.vidas -= 1
			disparo3.x = 10000            
		if self.puntuacion >= 100 and disparo1.x != 10000:
			disparo1.Movimiento(enemigo)
		if self.puntuacion >= 200 and disparo2.x != 10000:
			disparo2.Movimiento(enemigo)
		if self.puntuacion >= 300 and disparo3.x != 10000:
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
		barra_hp(screen, 1060, 60, secundaria.vidas, self.color)

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
			self.ancho += 2
			self.largo += 2
	
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
personaje1 = "Venus"
personaje2 = "Urano"
mercurio = transform.scale(image.load("planetfighters_images/Mercurio.png"), (75, 75))
venus = transform.scale(image.load("planetfighters_images/Venus.png"), (75, 75))
latierra = transform.scale(image.load("planetfighters_images/LaTierra.png"), (75, 75))
minilatierra = transform.scale(image.load("planetfighters_images/LaTierra.png"), (25, 25))
marte = transform.scale(image.load("planetfighters_images/Marte.png"), (75, 75))
minimarte = transform.scale(image.load("planetfighters_images/Marte.png"), (25, 25))
jupiter = transform.scale(image.load("planetfighters_images/Jupiter.png"), (75, 75))
saturno = transform.scale(image.load("planetfighters_images/Saturno.png"), (125, 125))
urano = transform.scale(image.load("planetfighters_images/Urano.png"), (75, 75))
neptuno = transform.scale(image.load("planetfighters_images/Neptuno.png"), (75, 75))
space = transform.scale(image.load("planetfighters_images/Space.png").convert(), (1280, 720))
cohete1 = transform.scale(image.load("planetfighters_images/Cohete1.png"), (50, 50))
cohete2 = transform.scale(image.load("planetfighters_images/Cohete2.png"), (50, 50))
hielo1 = transform.scale(image.load("planetfighters_images/Hielo1.png"), (50, 50))
hielo2 = transform.scale(image.load("planetfighters_images/Hielo2.png"), (50, 50))
roca = transform.scale(image.load("planetfighters_images/Roca.png"), (30, 30))
saturno2 = transform.scale(image.load("planetfighters_images/Saturno2.png"), (125, 125))
totem = transform.scale(image.load("planetfighters_images/Totem.png"), (75, 75))
barra = transform.scale(image.load("planetfighters_images/Bar.png"), (175, 20))

while True:
	screen.blit(space, [0, 0]) 
	
	plataforma.Movimiento(enemigo)
	enemigo.Movimiento(plataforma)
	Chocar(plataforma, enemigo)

	barra_hp_derecha(screen, 1060, 40, enemigo.vidas, (255,0,0))
	barra_hp_izquierda(screen, 50, 40, plataforma.vidas, (0,0,255))
	screen.blit(barra, [44, 35])
	screen.blit(minilatierra, [27, 30])
	screen.blit(barra, [1054, 35])
	screen.blit(minimarte, [1221, 30])

	timer += 1

	if timer >= 3000:
		if timer == 3000:
			plataforma.puntuacion = 0
			if personaje1 == "Marte" or personaje2 == "Marte":
				direccionx = choice([1, -1])
				direcciony = choice([1, -1])
				disparo1 = Bola(plataforma.x, plataforma.y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, plataforma.team)
				disparo2 = Bola(plataforma.x, plataforma.y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, plataforma.team)
				disparo3 = Bola(plataforma.x, plataforma.y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, plataforma.team)
			if personaje1 == "La Tierra" or personaje2 == "La Tierra":
				disparo = Bola(enemigo.x, enemigo.y, 20, 20, enemigo.direccionx, enemigo.direcciony, 0, (0, 255, 255), 1, enemigo.team)
			if personaje1 == "Venus" or personaje2 == "Venus":
				trampa = Bola(plataforma.x, plataforma.y, 25, 25, plataforma.direccionx, plataforma.direcciony, 0, (255, 125, 125), 1, plataforma.team)
			if personaje1 == "Urano" or personaje2 == "Urano":
				congelacion = Bola(enemigo.x, enemigo.y, 20, 20, -enemigo.direccionx, -enemigo.direcciony, 0, (0, 255, 0), 1, enemigo.team)
			if personaje1 == "Saturno" or personaje2 == "Saturno":
				area = Bola(plataforma.x-7.5, plataforma.y-7.5, 75, 75, plataforma.direccionx, plataforma.direcciony, 0, (125, 255, 125), 1, plataforma.team)
			if personaje1 == "Mercurio" or personaje2 == "Mercurio":
				secundaria = Bola(enemigo.x, enemigo.y, enemigo.ancho/2, enemigo.largo/2, -enemigo.direccionx, -enemigo.direcciony, 0, enemigo.color, enemigo.vidas/2, enemigo.team)
			if personaje1 == "Neptuno" or personaje2 == "Neptuno":
				diamante1 = Bola(0, -100, 10, 10, plataforma.direccionx, plataforma.direcciony, 0, (255, 125, 255), 1, plataforma.team)
				diamante2 = Bola(0, -100, 10, 10, plataforma.direccionx, plataforma.direcciony, 0, (255, 125, 255), 1, plataforma.team)

		if personaje1 == "Mercurio": 
			plataforma.Separarse(enemigo, secundaria)
			screen.blit(mercurio, [plataforma.x-10, plataforma.y-10])
		elif personaje1 == "Venus": 
			plataforma.PonerTrampa(enemigo, trampa)	
			screen.blit(venus, [plataforma.x-10, plataforma.y-10])
			screen.blit(totem, [trampa.x-25, trampa.y-30])
		elif personaje1 == "La Tierra": 
			plataforma.DispararTeledirigido(enemigo, disparo)
			screen.blit(latierra, [plataforma.x-10, plataforma.y-10])
			if disparo.direccionx == -1:
				screen.blit(cohete2, [disparo.x-15, disparo.y-15])
			else:
				screen.blit(cohete1, [disparo.x-15, disparo.y-15])
		elif personaje1 == "Marte": 
			plataforma.Disparar(enemigo, disparo1, disparo2, disparo3)
			screen.blit(marte, [plataforma.x-10, plataforma.y-10])
			screen.blit(roca, [disparo1.x-10, disparo1.y-10])
			screen.blit(roca, [disparo2.x-10, disparo2.y-10])
			screen.blit(roca, [disparo3.x-10, disparo3.y-10])
		elif personaje1 == "Jupiter": 
			plataforma.Aumentar(enemigo)
			screen.blit(jupiter, [plataforma.x-10, plataforma.y-10])
		elif personaje1 == "Saturno": 
			plataforma.GolpearEnArea(enemigo, area)
			screen.blit(saturno2, [plataforma.x-35, plataforma.y-35])
			screen.blit(saturno, [plataforma.x-35, plataforma.y-35])
		elif personaje1 == "Urano": 
			plataforma.DispararCongelacion(enemigo, congelacion)
			screen.blit(urano, [plataforma.x-10, plataforma.y-10])
			if congelacion.direccionx == -1:
				screen.blit(hielo2, [congelacion.x-15, congelacion.y-15])
			else:
				screen.blit(hielo1, [congelacion.x-15, congelacion.y-15])
		elif personaje1 == "Neptuno": 
			plataforma.LluviaDeDiamantes(enemigo, diamante1, diamante2)
			screen.blit(neptuno, [plataforma.x-10, plataforma.y-10])

		if personaje2 == "Mercurio": 
			enemigo.Separarse(plataforma, secundaria)
			screen.blit(mercurio, [enemigo.x-10, enemigo.y-10])
		elif personaje2 == "Venus": 
			enemigo.PonerTrampa(plataforma, trampa)	
			screen.blit(venus, [enemigo.x-10, enemigo.y-10])
			screen.blit(totem, [trampa.x, trampa.y])
		elif personaje2 == "La Tierra": 
			enemigo.DispararTeledirigido(plataforma, disparo)
			screen.blit(latierra, [enemigo.x-10, enemigo.y-10])
			if disparo.direccionx == -1:
				screen.blit(cohete2, [disparo.x-15, disparo.y-15])
			else:
				screen.blit(cohete1, [disparo.x-15, disparo.y-15])
		elif personaje2 == "Marte": 
			enemigo.Disparar(plataforma, disparo1, disparo2, disparo3)
			screen.blit(marte, [enemigo.x-10, enemigo.y-10])
			screen.blit(roca, [disparo1.x-10, disparo1.y-10])
			screen.blit(roca, [disparo2.x-10, disparo2.y-10])
			screen.blit(roca, [disparo3.x-10, disparo3.y-10])
		elif personaje2 == "Jupiter": 
			enemigo.Aumentar(plataforma)
			screen.blit(jupiter, [enemigo.x-10, enemigo.y-10])
		elif personaje2 == "Saturno": 
			enemigo.GolpearEnArea(plataforma, area)
			screen.blit(saturno2, [plataforma.x-35, plataforma.y-35])
			screen.blit(saturno, [enemigo.x-35, enemigo.y-35])
		elif personaje2 == "Urano": 
			enemigo.DispararCongelacion(plataforma, congelacion)
			screen.blit(urano, [enemigo.x-10, enemigo.y-10])
			if congelacion.direccionx == -1:
				screen.blit(hielo2, [congelacion.x-17.5, congelacion.y-15])
			else:
				screen.blit(hielo1, [congelacion.x-12.5, congelacion.y-15])
		elif personaje2 == "Neptuno": 
			enemigo.LluviaDeDiamantes(plataforma, diamante1, diamante2)
			screen.blit(neptuno, [enemigo.x-10, enemigo.y-10])

	for evento in event.get():
		if evento.type==QUIT:
				quit()
				exit()
		if evento.type==KEYDOWN:
			if evento.key == K_ESCAPE:
				quit()
				exit()
	display.flip()
