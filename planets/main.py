#Ex.2 — Planets

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec

class GBCircle(object): #Круглый объект - для визуализации или отрисовки графиков
    def __init__(self, r=3):
        self.x = 0 #Координаты
        self.y = 0
        self.color = 'k-' #Цвет
        self.r = r #Радиус
        self.point, = plt.plot([], [], self.color, ms=self.r) #средство отображение объекта
        self.track = False #След откл.
        self.xData, self.yData = [], [] #Данные для рисования следа
    
    def draw(self, x, y): #Рисующая функция
        if (self.track): #Если след включён
            self.xData.append(x) #Добавление новой точки к траектории
            self.yData.append(y)
            self.point.set_data(self.xData, self.yData) #Отображение этих данных
        else: #Если след отключен
            self.point.set_data(x, y) #Отображение текущих координат

class GraphBase(object): #Общий класс графического окна. Используется для графиков и визуализации
    def __init__(self, xmin = -1, xmax = 1, ymin = -1, ymax = 1, title = '', xlabel = '', ylabel = '', r=3):

        plt.xlim(xmin, xmax) #ограничение осей
        plt.ylim(ymin, ymax)
        plt.grid(ls='solid', lw=0.2) #включение сетки

        plt.title(title, fontsize=8) #заголовок
        plt.xlabel(xlabel, fontsize=6) #названия осей
        plt.ylabel(ylabel, fontsize=6)

        self.r = r #Радиус точки графика/объекта визуализации

class GBVisualisation(GraphBase): #Класс окна визуализации
    def __init__(self, xmin = -1, xmax = 1, ymin = -1, ymax = 1, title = '', xlabel = '', ylabel = '', r=3):
        GraphBase.__init__(self, xmin, xmax, ymin, ymax, title, xlabel, ylabel, r)

        self.planet = GBCircle(self.r) #Создание планеты
    
    def animate(self, i, calsFunc, argsFunc): #Функция, рисующая визуализацию
        calsFunc(i) #Функия, изменяющая все папаметры системы

        x, y = argsFunc() #Функция, передающая нужные данные о системе
        self.planet.draw(x, y) #Рисование планеты

        return self.planet.point,  #Для обновления не всей области рисования, а только изменённой

class GBPlot(GraphBase): #Класс окна графика
    def __init__(self, xmin = -1, xmax = 1, ymin = -1, ymax = 1, title = '', xlabel = '', ylabel = '', r=3):
        GraphBase.__init__(self, xmin, xmax, ymin, ymax, title, xlabel, ylabel, r)

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


class Planet(object): #Объявление класса планеты
    def __init__(self, title = ''): #Начальные данные
        self.x = 1 #координаты
        self.y = 0
        self.p = 1 #импульс
        self.t = 0 #время
        self.dt = 0.02 #шаг времени

        self.staticPointX = 0 #Центр вращения
        self.staticPointY = 7
        #self.r = self.staticPointY - self.y #Длина палки

        self.E_kin = 0 #энергии
        self.E_pot = 0
        self.E = 0

        n = 3
        self.fig = plt.figure(figsize=(3*n, 3*n)) #окно для рисования
        self.fig.suptitle(title) #подзаголовок окна
        self.grs = gridspec.GridSpec(nrows=3, ncols=3, figure=self.fig) #Средство размещения графиков
        plt.gcf().canvas.set_window_title('Задание 2 — планеты') #Заголовок окна
        

    def nextFrameCalc(self, i):
        
        pass
        #self.t = self.dt * i #Изменение времени
        #self.x = self.x + self.p*self.dt  #Вычисление угла отклонения
        #self.p = self.p - np.sin(self.x)*self.dt  #и импульса через время dt
        #self.y = (self.x**2)/(2*self.l)
        #self.y = -np.sqrt((self.l-self.x)*(self.l+self.x))+self.l #Вычисление у при известном х

        #if (self.friction): #если трение включено
        #    self.p = self.p - self.p*self.kFric*self.dt #рассчёт трения

        #self.lineX = [self.x, self.staticPointX]    #Координаты палки маятника
        #self.lineY = [self.y, self.staticPointY]    #Содержат её начало и конец

        #self.E_kin = self.p**2/2  #Подсчёт
        #self.E_pot = self.y*5.75   #энергий
        #self.E = self.E_kin + self.E_pot
    
    #Функции, передающие нужные аргументы соответствующей animate() или animate_plot()

    def visualisation_args(self): #Для визуализации
        return self.x, self.y

    #def eKinPlot_args(self): #Для кинетической энергии
    #    return self.t, self.E_kin

    #def ePotPlot_args(self): #Для потенциальной энергии
    #    return self.t, self.E_pot
    
    #def ePlot_args(self): #Для полной энергии
    #    return self.t, self.E

    #def phasePlot_args(self): #Для фазовой плоскости
    #    return self.x, self.p
        

    def startDraw(self): #Создание экземпляров графических областей и запуск рисования в них

        #Запуск визуализации
        self.fig_ax_1 = self.fig.add_subplot(self.grs[0:2, 0:2]) #Выбор места на self.fig
        self.visualisation = GBVisualisation(xmin=-2, xmax=2, ymin=-2, ymax=2, r=10,
            title='Визуализация', xlabel='координата х', ylabel='координата у') #Создание объекта. Указан размер графика и радиус планеты
        FuncAnimation(self.fig, self.visualisation.animate, fargs=(self.nextFrameCalc, self.visualisation_args),
            frames=2000, interval=self.dt*1000, blit=True) #Запуск рисование на этом графике
            #В аргументах передаётся считающая функция, которая изменяет все параметры системы,
            #и функция, передающая нужные данные в функцию self.visualisation.animate

        #График кинетической энергии
        #Всё аналогично описанию выше
        self.fig_ax_2 = self.fig.add_subplot(self.grs[0,2])
        self.eKinPlot = GBPlot(xmin=0, xmax=np.pi*12, ymin=0, ymax=1,
            title='Кинетическая энергия', xlabel='время t', ylabel='энергия Екин')
        #FuncAnimation(self.fig, self.eKinPlot.animate_plot, fargs=(self.eKinPlot_args, ),
        #    frames=2000, interval=self.dt*1000, blit=True, repeat=False)

        #График потенциальной энергии
        self.fig_ax_3 = self.fig.add_subplot(self.grs[1,2])
        self.ePotPlot = GBPlot(xmin=0, xmax=np.pi*12, ymin=0, ymax=1,
            title='Потенцальная энергия', xlabel='время t', ylabel='энергия Епот')
        #FuncAnimation(self.fig, self.ePotPlot.animate_plot, fargs=(self.ePotPlot_args, ),
        #    frames=2000, interval=self.dt*1000, blit=True, repeat=False)

        #График полной энергии
        self.fig_ax_4 = self.fig.add_subplot(self.grs[2,2])
        self.ePlot = GBPlot(xmin=0, xmax=np.pi*12, ymin=0, ymax=1.2,
            title='Полная энергия', xlabel='время t', ylabel='энергия Е')
        #FuncAnimation(self.fig, self.ePlot.animate_plot, fargs=(self.ePlot_args, ),
        #   frames=2000, interval=self.dt*1000, blit=True, repeat=False)

        #Фазовая плоскость
        self.fig_ax_5 = self.fig.add_subplot(self.grs[2,1])
        self.phasePlot = GBPlot(xmin=-2, xmax=2, ymin=-2, ymax=2,
            title='Фазовая плоскость', xlabel='координата х', ylabel='импульс р')
        #FuncAnimation(self.fig, self.phasePlot.animate_plot, fargs=(self.phasePlot_args, ),
        #    frames=2000, interval=self.dt*1000, blit=True)

        


planet = Planet(title = 'Планета') #Создаём 1 экземпляр класса планеты
planet.startDraw()  #Функция, запускающая рисование на графиках
plt.subplots_adjust(wspace=0.5, hspace=0.5) #расстояние между графиками

plt.show() #Отображения окна mathplotlib