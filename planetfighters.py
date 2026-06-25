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

	def DispararTeledirigido(self, enemigo, disparo):			
		if enemigo.check_colisiones(disparo):
			enemigo.vidas -= 5
			disparo.x = 10000   
		if disparo.x != 10000:       
			disparo.MovimientoTeledirigido(enemigo)

	def PonerTrampa(self, enemigo, trampa):
		if enemigo.check_colisiones(trampa):
			enemigo.vidas -= 3
			trampa.x = 10000
		trampa.DibujarObjeto()

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

def barra_hp(screen, x, y, hp, color):
	largo = 165
	ancho = 10
	calculo_barra = int((hp / 100)*largo)
	draw.rect(screen, color, Rect(x, y, calculo_barra, ancho))

plataforma = Bola(300,350,40,40, 1, 1, 0, (0,0,255), 100, 0)
enemigo = Bola(940,350,40,40, 1, 1, 0, (255,0,0), 100, 1)
timer = 0

while True:
	screen.fill((0, 0, 0)) 
	
	plataforma.Movimiento(enemigo)
	enemigo.Movimiento(plataforma)
	Chocar(plataforma, enemigo)

	barra_hp(screen, 1060, 40, enemigo.vidas, (255,0,0))
	barra_hp(screen, 50, 40, plataforma.vidas, (0,0,255))

	timer += 1
	if timer >= 3000:
		if timer == 3000:
			plataforma.puntuacion = 0
			direccionx = choice([1, -1])
			direcciony = choice([1, -1])
			disparo1 = Bola(plataforma.x, plataforma.y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, plataforma.team)
			disparo2 = Bola(plataforma.x, plataforma.y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, plataforma.team)
			disparo3 = Bola(plataforma.x, plataforma.y, 10, 10, direccionx, direcciony, 0, (255, 255, 0), 1, plataforma.team)
			disparo = Bola(enemigo.x, enemigo.y, 20, 20, enemigo.direccionx, enemigo.direcciony, 0, (0, 255, 255), 1, enemigo.team)
			trampa = Bola(plataforma.x, plataforma.y, 25, 25, plataforma.direccionx, plataforma.direcciony, 0, (255, 125, 125), 1, plataforma.team)
			congelacion = Bola(enemigo.x, enemigo.y, 20, 20, -enemigo.direccionx, -enemigo.direcciony, 0, (0, 255, 0), 1, enemigo.team)
			area = Bola(plataforma.x, plataforma.y, 60, 60, plataforma.direccionx, plataforma.direcciony, 0, (125, 255, 125), 1, plataforma.team)
		plataforma.GolpearEnArea(enemigo, area)
		enemigo.DispararCongelacion(plataforma, congelacion)

	for evento in event.get():
		if evento.type==QUIT:
				quit()
				exit()
		if evento.type==KEYDOWN:
			if evento.key == K_ESCAPE:
				quit()
				exit()
	display.flip()