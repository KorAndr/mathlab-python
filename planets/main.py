#Ex.2 — Planets

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec

class GBCircle(object): #Круглый объект - для визуализации или отрисовки графиков
    def __init__(self, r=3, color='r'):
        self.x = 0 #Координаты
        self.y = 0
        self.color = color #Цвет
        self.r = r #Радиус
        self.point, = plt.plot([], [], 'ro', ms=self.r, color=self.color) #средство отображение объекта
        self.line, = plt.plot([], [], 'k-', lw=0.2) #След
        self.track = False #След откл.
        self.xData, self.yData = [], [] #Данные для рисования следа
        self.visible = True #Видимость
    
    def draw(self): #Рисующая функция
        if (self.track): #Если след включён
            self.xData.append(self.x) #Добавление новой точки к траектории
            self.yData.append(self.y)
            self.line.set_data(self.xData, self.yData) #Отображение этих данных

        self.point.set_data(self.x, self.y) #Отображение текущих координат

    def changeXY(self, x, y): #Функция изменения координат
        self.x = x
        self.y = y

class GraphBase(object): #Общий класс графического окна. Используется для графиков и визуализации
    def __init__(self, xmin = -1, xmax = 1, ymin = -1, ymax = 1, title = '', xlabel = '', ylabel = '', r=3):

        plt.xlim(xmin, xmax) #ограничение осей
        plt.ylim(ymin, ymax)
        plt.grid(ls='solid', lw=0.2) #включение сетки

        plt.title(title, fontsize=8) #заголовок
        plt.xlabel(xlabel, fontsize=6) #названия осей
        plt.ylabel(ylabel, fontsize=6)

        self.r = r #Радиус точки графика/объекта визуализации

class GBPlot(GraphBase): #Класс окна графика
    def __init__(self, xmin = -1, xmax = 1, ymin = -1, ymax = 1, title = '', xlabel = '', ylabel = '', r=3):
        GraphBase.__init__(self, xmin, xmax, ymin, ymax, title, xlabel, ylabel, r) #Конструктор родительского класса

        self.point, = plt.plot([], [], 'ro', ms=self.r) #текущая точка на графике
        self.line, = plt.plot([], [], 'k-', lw=1) #линия графика

        self.xData, self.yData = [], [] #Кортежи для записи всех точек графика
        
    def animate(self, i, argsFunc): #Функция, рисующая графики
        x, y = argsFunc()   #Функция, передающая нужные данные о маятнике
        self.xData.append(x) #Записываем историю изменения точек графика
        self.yData.append(y)
        self.line.set_data(self.xData, self.yData) #Рисование линии графика
        self.point.set_data(x, y)  #Рисование текущей точки

        return self.point, self.line, #Для обновления не всей области рисования, а только изменённой

class GBVisualisation(GraphBase): #Класс окна визуализации
    def __init__(self, xmin = -1, xmax = 1, ymin = -1, ymax = 1, title = '', xlabel = '', ylabel = '', r=3):
        GraphBase.__init__(self, xmin, xmax, ymin, ymax, title, xlabel, ylabel, r)

        self.planet = GBCircle(r=self.r, color='#1D1764') #Создание планеты
        self.planet.track = True #След планеты вкл.
        self.sun = GBCircle(r=15, color='#FFE354') #Создание солнца
        self.sun.changeXY(0, 0) #Координаты солнца

        self.apohel = GBCircle(r=3, color='#49BAB8')  #Создание точек
        self.apohel.visible = False                   #апогелия и перигелия
        self.perihel = GBCircle(r=3, color='#FF94CD') #с выключенной
        self.perihel.visible = False                  #видимостью
    
    def animate(self, i, calsFunc, argsFunc): #Функция, рисующая визуализацию
        calsFunc(i) #Функия, изменяющая все папаметры системы

        x, y = argsFunc() #Функция, передающая нужные данные о системе
        self.planet.changeXY(x, y)
        self.planet.draw() #Рисование планеты
        self.sun.draw() #Рисование солнца

        #Рисования точек апогелия и перигелия
        if (self.apohel.visible): 
            self.apohel.draw()
        if (self.perihel.visible):
            self.perihel.draw()

        return self.planet.point, self.planet.line, self.sun.point, self.perihel.point, self.apohel.point,
          #Для обновления не всей области рисования, а только изменённой


class Planet(object): #Объявление класса планеты
    def __init__(self, title = ''): #Начальные данные
        self.x, self.y = 1.5, 0 #координаты
        self.vx, self.vy = 0, 0.6 #Скорость
        self.t = 0 #время
        self.dt = 0.01 #шаг времени
        self.T = 0 #период
        self.r = 0 #Модуль радиус-вектора
        self.alpha = 1 #коэффициент
        self.ax, self.ay = 0, 0 #ускорение

        self.max_r = 0 #Максимальный радиус (апогелий)
        self.last_max_r = 0 #Предыдущее значение апогелия
        
        self.min_r = self.x #аналогично для минимального
        self.last_min_r = 0

        self.last_x, self.last_y = self.x, self.y #координаты в момент предыдущего апогелия/перигелия
        self.detectedTime = 0 #Время предыдущего апогелия/перигелия

        self.E_kin = 0 #энергии
        self.E_pot = 0
        self.E = 0
        self.L = self.x*self.vy-self.y*self.vx #Момент импульса

        n = 2.5 #коэффициент масштабирования
        self.fig = plt.figure(figsize=(3*n, 3*n)) #окно для рисования
        self.fig.suptitle(title) #подзаголовок окна
        self.grs = gridspec.GridSpec(nrows=3, ncols=3, figure=self.fig) #Средство размещения графиков
        plt.gcf().canvas.set_window_title('Задание 2 — планеты') #Заголовок окна
        

    def nextFrameCalc(self, i): #Вычисление параметров системы
        
        self.t = self.dt * i #Изменение времени
        self.x = self.x - self.vx*self.dt/2 #Отступ назад
        self.y = self.y - self.vy*self.dt/2

        self.x = self.x + self.vx*self.dt #Новые координаты
        self.y = self.y + self.vy*self.dt

        self.r = np.sqrt(self.x**2 + self.y**2) #Радиус-вектор
        self.ax = -self.alpha*self.x/self.r**3 #Ускорение
        self.ay = -self.alpha*self.y/self.r**3

        self.vx = self.vx + self.ax*self.dt #Скорости
        self.vy = self.vy + self.ay*self.dt

        self.E_kin = (self.vx**2+self.vy**2)/2/2 #Энергии
        #self.E_pot = np.log(np.abs(self.r))
        self.E_pot = -1/self.r
        self.E = self.E_kin + self.E_pot


        #Нахождение периода
        self.startPointX = self.x #Начальные точки
        self.startPointY = self.y
        self.startTime = self.t #Время старта
        if (self.t!=self.startTime and self.x==self.startPointX and self.y==self.startPointY): #Момент возвращения в начальную точку
            self.T = self.t-self.startTime


        #апогелий и перигелий  
        #апогелий
        if (self.r > self.max_r): #Находим максимальный радиус
            self.last_max_r = self.max_r #Запоминаем предыдущий
            self.max_r = self.r 
            self.last_x = self.x #Координаты предыдущего
            self.last_y = self.y
            self.detectedTime = self.t #Время предыдущего
        if (round(self.last_max_r, 2) == round(self.max_r, 2) and (self.t-self.detectedTime)>1 and not self.visualisation.apohel.visible):
            self.visualisation.apohel.visible = True #Отображение точки на графике
            self.visualisation.apohel.changeXY(self.last_x, self.last_y)

        #перигелий
        if (self.r < self.min_r): #Аналогично апогелию
            self.last_min_r = self.min_r
            self.min_r = self.r
            self.last_x = self.x
            self.last_y = self.y
            self.detectedTime = self.t
        if (round(self.last_min_r, 2) == round(self.min_r, 2) and (self.t-self.detectedTime)>1 and not self.visualisation.perihel.visible):
            self.visualisation.perihel.visible = True
            self.visualisation.perihel.changeXY(self.last_x, self.last_y)
        
    
    #Функции, передающие нужные аргументы соответствующей animate() или animate_plot()

    def visualisation_args(self): #Для визуализации
        return self.x, self.y

    def eKinPlot_args(self): #Для кинетической энергии
        return self.t, self.E_kin

    def ePotPlot_args(self): #Для потенциальной энергии
        return self.t, self.E_pot
    
    def ePlot_args(self): #Для полной энергии
        return self.t, self.E

    def lPlot_args(self): #Для момента импульса
        return self.t, self.L
        

    def startDraw(self): #Создание экземпляров графических областей и запуск рисования в них

        #Запуск визуализации
        self.fig_ax_1 = self.fig.add_subplot(self.grs[0:2, 0:2]) #Выбор места на self.fig
        self.visualisation = GBVisualisation(xmin=-2, xmax=2, ymin=-2, ymax=2, r=5,
            title='Визуализация', xlabel='координата х', ylabel='координата у') #Создание объекта. Указан размер графика и радиус планеты
        FuncAnimation(self.fig, self.visualisation.animate, fargs=(self.nextFrameCalc, self.visualisation_args),
            frames=3000, interval=self.dt*1000, blit=True) #Запуск рисование на этом графике
            #В аргументах передаётся считающая функция, которая изменяет все параметры системы,
            #и функция, передающая нужные данные в функцию self.visualisation.animate

        #График кинетической энергии
        #Всё аналогично описанию выше
        self.fig_ax_2 = self.fig.add_subplot(self.grs[0,2])
        self.eKinPlot = GBPlot(xmin=0, xmax=20, ymin=0, ymax=4,
            title='Кинетическая энергия', xlabel='время t', ylabel='энергия Екин')
        FuncAnimation(self.fig, self.eKinPlot.animate, fargs=(self.eKinPlot_args, ),
            frames=3000, interval=self.dt*1000, blit=True, repeat=False)

        #График потенциальной энергии
        self.fig_ax_3 = self.fig.add_subplot(self.grs[1,2])
        self.ePotPlot = GBPlot(xmin=0, xmax=20, ymin=-5, ymax=0,
            title='Потенцальная энергия', xlabel='время t', ylabel='энергия Епот')
        FuncAnimation(self.fig, self.ePotPlot.animate, fargs=(self.ePotPlot_args, ),
            frames=3000, interval=self.dt*1000, blit=True, repeat=False)

        #График полной энергии
        self.fig_ax_4 = self.fig.add_subplot(self.grs[2,2])
        self.ePlot = GBPlot(xmin=0, xmax=20, ymin=-1, ymax=0,
            title='Полная энергия', xlabel='время t', ylabel='энергия Е')
        FuncAnimation(self.fig, self.ePlot.animate, fargs=(self.ePlot_args, ),
           frames=3000, interval=self.dt*1000, blit=True, repeat=False)

        #Момент импульса
        self.fig_ax_5 = self.fig.add_subplot(self.grs[2,:2])
        self.lPlot = GBPlot(xmin=0, xmax=20, ymin=0.8, ymax=1,
            title='Момент импульса', xlabel='время t', ylabel='Момент импульса L')
        FuncAnimation(self.fig, self.lPlot.animate, fargs=(self.lPlot_args, ),
            frames=3000, interval=self.dt*1000, blit=True, repeat=False)

        


planet = Planet(title = 'Солнечная система') #Создаём экземпляр класса планеты
planet.startDraw()  #Функция, запускающая рисование на графиках
plt.subplots_adjust(wspace=0.5, hspace=0.5) #расстояние между графиками

plt.show() #Отображения окна mathplotlib