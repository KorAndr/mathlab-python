import matplotlib.pyplot as plt
import numpy as np
#import math
from matplotlib.animation import FuncAnimation
#plt.style.use('seaborn-pastel')

# Построение графиков
#plt.figure(figsize=(9, 9))
#plt.subplot(2, 1, 1)
#plt.plot(x, y1)                # построение графика
#plt.title("Зависимости: y1 = x, y2 = x^2") # заголовок
#plt.ylabel("y1", fontsize=14) # ось ординат
#plt.grid(True)                # включение отображение сетки
#plt.subplot(2, 1, 2)
#plt.plot(x, y2)                # построение графика
#plt.xlabel("x", fontsize=14)  # ось абсцисс
#plt.ylabel("y2", fontsize=14) # ось ординат
#plt.grid(True)                # включение отображение сетки



class GraphBase(object):
    def __init__(self):
        self.mk, = plt.plot([], [], 'ro', ms =10) #маркер
        line, = plt.plot([], [], 'k-', lw=1)

class Pendulum(object): #Объявление класса маятника
    def __init__(self): #Начальные данные
        self.x = 1
        self.y = 0
        self.p = 1
        self.t = 0
        self.dt = 0.02
        self.x = self.x - self.p*self.dt/2

        self.staticPointX = 0
        self.staticPointY = 3
        self.l = self.staticPointY - self.y
        self.lineX = [0]
        self.lineY = [0]

        self.E_kin = 0
        self.E_pot = 0

    def nextFrameCalc(self, i):
        self.t = self.dt * i #Изменение времени
        self.x = self.x + self.p*self.dt  #Вычисление угла отклонения
        self.p = self.p - np.sin(self.x)*self.dt  #и импульса через время dt
        #self.y = (self.x**2)/(2*self.l)
        self.y = -np.sqrt((self.l-self.x)*(self.l+self.x))+self.l

        self.lineX = [self.x, self.staticPointX]
        self.lineY = [self.y, self.staticPointY]

        self.E_kin = self.p**2/2
        self.E_pot = self.y*2.3


pdl = Pendulum()
 
fig = plt.figure()
plt.subplot(2, 3, 1)
plt.title("Визуализаия") # заголовок
plt.ylabel("координата y", fontsize=10) # ось ординат
plt.xlabel("координата х", fontsize=10) # ось ординат

plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.grid(ls='solid', lw=0.2) 
mk, = plt.plot([], [], 'ro', ms =10) #маркер
line, = plt.plot([], [], 'k-', lw=1)

def animate(i):
    pdl.nextFrameCalc(i)

    line.set_data(pdl.lineX, pdl.lineY)
    mk.set_data(pdl.x, pdl.y)

    return mk, line,
 
anim = FuncAnimation(fig, animate, frames=200, interval=pdl.dt*1000, blit=True)

############################################################

plt.subplot(2, 3, 3)
plt.title("Фазовая плоскость") # заголовок
plt.ylabel("импульс p", fontsize=10) # ось ординат
plt.xlabel("координата х", fontsize=10) # ось ординат

plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.grid(ls='solid', lw=0.2) 
mk_2, = plt.plot([], [], 'ro', ms =3)
line_2, = plt.plot([], [], 'k-', lw=1)

xdata, pdata = [], []

def animate_2(i):
    pdl.nextFrameCalc(i)

    xdata.append(pdl.x)
    pdata.append(pdl.p)

    line_2.set_data(xdata, pdata)
    mk_2.set_data(pdl.x, pdl.p)

    return mk_2, line_2,
 
anim = FuncAnimation(fig, animate_2, frames=200, interval=pdl.dt*1000, blit=True)

################################################################################

plt.subplot(2, 3, 2)
plt.title("Кинетическая энергия") # заголовок
plt.ylabel("энергия Eк", fontsize=10) # ось ординат
plt.xlabel("время t", fontsize=10) # ось ординат

plt.xlim(0, np.pi*6)
plt.ylim(0, 1)
plt.grid(ls='solid', lw=0.2) 
mk_3, = plt.plot([], [], 'ro', ms =3)
line_3, = plt.plot([], [], 'k-', lw=1)

tdata, ekdata = [], []

def animate_3(i):
    pdl.nextFrameCalc(i)

    #print(pdl.t)

    tdata.append(pdl.t)
    ekdata.append(pdl.E_kin)

    line_3.set_data(tdata, ekdata)
    mk_3.set_data(pdl.t, pdl.E_kin)

    return mk_3, line_3,
 
anim = FuncAnimation(fig, animate_3, frames=2000, interval=pdl.dt*1000, blit=True)

################################################################################

plt.subplot(2, 3, 4)
plt.title("Потенциальная энергия") # заголовок
plt.ylabel("энергия Eп", fontsize=10) # ось ординат
plt.xlabel("время t", fontsize=10) # ось ординат

plt.xlim(0, np.pi*6)
plt.ylim(0, 1)
plt.grid(ls='solid', lw=0.2) 
mk_4, = plt.plot([], [], 'ro', ms =3)
line_4, = plt.plot([], [], 'k-', lw=1)

epdata = []

def animate_4(i):
    pdl.nextFrameCalc(i)

    epdata.append(pdl.E_pot)

    line_4.set_data(tdata, epdata)
    mk_4.set_data(pdl.t, pdl.E_pot)

    return mk_4, line_4,
 
anim = FuncAnimation(fig, animate_4, frames=2000, interval=pdl.dt*1000, blit=True)

################################################################################

plt.subplot(2, 3, 5)
plt.title("Общая энергия") # заголовок
plt.ylabel("энергия E", fontsize=10) # ось ординат
plt.xlabel("время t", fontsize=10) # ось ординат

plt.xlim(0, np.pi*6)
plt.ylim(0, 2)
plt.grid(ls='solid', lw=0.2) 
mk_5, = plt.plot([], [], 'ro', ms =3)
line_5, = plt.plot([], [], 'k-', lw=1)

edata = []

def animate_5(i):
    pdl.nextFrameCalc(i)

    edata.append(pdl.E_pot + pdl.E_kin)

    line_5.set_data(tdata, edata)
    mk_5.set_data(pdl.t, pdl.E_pot + pdl.E_kin)

    return mk_5, line_5,
 
anim = FuncAnimation(fig, animate_5, frames=2000, interval=pdl.dt*1000, blit=True)

plt.show()