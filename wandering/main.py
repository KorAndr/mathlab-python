#Ex.3 — Random wandering

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec

import GraphBaseLib as gbl #Импорт интерфейса для matplotlib (см. в этой же папке)

class Visualisation(gbl.GraphBase): #Класс окна визуализации
    def __init__(self, nomber, xmin = -1, xmax = 1, ymin = -1, ymax = 1, title = '', xlabel = '', ylabel = '', r=3):
        gbl.GraphBase.__init__(self, xmin, xmax, ymin, ymax, title, xlabel, ylabel, r)
        self.nomber = nomber
        self.particles = []
        for i in range(0, self.nomber):
            prt = gbl.Circle(r=self.r, color='#1D1764')
            self.particles.append(prt) 
    
    def animate(self, i, calsFunc, argsFunc): #Функция, рисующая визуализацию
        calsFunc(i) #Функия, изменяющая все папаметры системы

        particles = argsFunc() #Функция, передающая нужные данные о системе
        rtn = []
        for i in range(0, self.nomber):
            self.particles[i].changeXY(particles[i].x, particles[i].y)
            self.particles[i].draw()
            rtn.append(self.particles[i].point)

        return rtn
          #Для обновления не всей области рисования, а только изменённой


class Particle(object):
    def __init__(self, x=0, y=0, vx=0, vy=0):
        self.x, self.y = x, y #координаты
        self.vx, self.vy = vx, vy #Безразмерная скорость - количество пикселей смещения 

        self.r = 3
        #self.graph = gbl.Circle(r=self.r, color='#1D1764') 
    
    def binaryRand(self):
        rand = np.random.randint(low=0, high=2) #число 0 до 1
        #rand = int(rand*10) % 2 #число 0 или 1
        if (rand == 0):
            rand = -1
        return rand #число 1 или -1

    def moving(self):
        self.x += self.vx*self.binaryRand()
        self.y += self.vy*self.binaryRand()


class Surface(object): #Объявление класса частицы
    def __init__(self, title = ''): #Начальные данные
        self.t = 0 #время
        self.dt = 0.05 #шаг времени

        self.pNomber = 100

        n = 2 #коэффициент масштабирования
        self.fig = plt.figure(figsize=(3*n, 3*n)) #окно для рисования
        self.fig.suptitle(title) #подзаголовок окна
        self.grs = gridspec.GridSpec(nrows=1, ncols=1, figure=self.fig) #Средство размещения графиков
        plt.gcf().canvas.set_window_title('Задание 3 — одномерные блуждания') #Заголовок окна

        self.particles = []
        for i in range(0, self.pNomber):
            x = 0
            y = -1*self.pNomber/2 + i
            prt = Particle(x, y, vx=0.1, vy=0)
            self.particles.append(prt)
    
    def nextFrameCalc(self, i): #Вычисление параметров системы
        self.t = self.dt * i #Изменение времени

        for prt in self.particles:
            prt.moving()
    
    #Функции, передающие нужные аргументы соответствующей animate()

    def visualisation_args(self): #Для визуализации
        return self.particles   #массив частиц     

    def startDraw(self): #Создание экземпляров графических областей и запуск рисования в них

        #Запуск визуализации
        limit = self.pNomber/2 + 1

        self.fig_ax_1 = self.fig.add_subplot(self.grs[0, 0]) #Выбор места на self.fig
        self.visualisation = Visualisation(self.pNomber, xmin=-10, xmax=10, ymin=-limit, ymax=limit, r = 3,
            title='Визуализация', xlabel='координата х', ylabel='координата у') #Создание объекта. Указан размер графика
        FuncAnimation(self.fig, self.visualisation.animate, fargs=(self.nextFrameCalc, self.visualisation_args),
            frames=3000, interval=self.dt*1000, blit=True) #Запуск рисование на этом графике
            #В аргументах передаётся считающая функция, которая изменяет все параметры системы,
            #и функция, передающая нужные данные в функцию self.visualisation.animate
     



sfc = Surface(title = 'Блуждания') #Создаём экземпляр класса планеты
sfc.startDraw()  #Функция, запускающая рисование на графиках
plt.subplots_adjust(wspace=0.5, hspace=0.5) #расстояние между графиками

#sfc.fig.show()
plt.show() #Отображения окна mathplotlib