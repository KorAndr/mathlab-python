import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

class GraphBase(object): #Класс графического окна. Используется для графиков и для визуализации
    def __init__(self, xmin = -1, xmax = 1, ymin = -1, ymax = 1, title = '', xlabel = '', ylabel = '', r=3):

        plt.xlim(xmin, xmax) #ограничение осей
        plt.ylim(ymin, ymax)
        plt.grid(ls='solid', lw=0.2) #включение сетки

        plt.title(title, fontsize=8) #заголовок
        plt.xlabel(xlabel, fontsize=6) #названия осей
        plt.ylabel(ylabel, fontsize=6)

        self.mk, = plt.plot([], [], 'ro', ms=r) #маркер
        self.line, = plt.plot([], [], 'k-', lw=1) #линия графика

        self.xData, self.yData = [], [] #Кортежи для записи всех точек графика
    
    def animate(self, i, calsFunc, argsFunc): #Функция, рисующая визуализацию
        calsFunc(i) #Функия, изменяющая все папаметры маятника

        line_x, line_y, mk_x, mk_y = argsFunc() #Функция, передающая нужные данные о маятнике
        self.line.set_data(line_x, line_y)      #Рисование подвеса (палки)
        self.mk.set_data(mk_x, mk_y)            #Рисование груза

        return self.mk, self.line,  #Для обновления не всей области рисования, а только изменённой

    def animate_plot(self, i, argsFunc): #Функция, рисующая графики
        x, y = argsFunc()   #Функция, передающая нужные данные о маятнике
        self.xData.append(x) #Записываем историю изменения точек графика
        self.yData.append(y)
        self.line.set_data(self.xData, self.yData) #Рисование линии графика
        self.mk.set_data(x, y)  #Рисование красной точки

        return self.mk, self.line,


class Pendulum(object): #Объявление класса маятника
    def __init__(self, title = ''): #Начальные данные
        self.x = 1 #координаты
        self.y = 0
        self.p = 1 #импульс
        self.t = 0 #время
        self.dt = 0.02 #шаг времени
        self.x = self.x - self.p*self.dt/2 #вычисление начального х

        self.staticPointX = 0 #Точка, куда прикреплена палка маятника
        self.staticPointY = 3
        self.l = self.staticPointY - self.y #Длина палки
        self.lineX = [0] #кортежи для координат палки маятника
        self.lineY = [0]

        self.E_kin = 0 #энергии
        self.E_pot = 0
        self.E = 0

        self.friction = False
        self.kFric = 0.1

        self.fig = plt.figure() #окно для рисования
        self.fig.suptitle(title)
        

    def nextFrameCalc(self, i):

        self.t = self.dt * i #Изменение времени
        self.x = self.x + self.p*self.dt  #Вычисление угла отклонения
        self.p = self.p - np.sin(self.x)*self.dt  #и импульса через время dt
        #self.y = (self.x**2)/(2*self.l)
        self.y = -np.sqrt((self.l-self.x)*(self.l+self.x))+self.l #Вычисление у при известном х

        if (self.friction):
            self.p = self.p - self.p*self.kFric*self.dt

        self.lineX = [self.x, self.staticPointX]    #Координаты палки маятника
        self.lineY = [self.y, self.staticPointY]    #Содержат её начало и конец

        self.E_kin = self.p**2/2  #Подсчёт
        self.E_pot = self.y*2.3   #энергий
        self.E = self.E_kin + self.E_pot
    
    #Функции, передающие нужные аргументы соответствующей animate() или animate_plot()

    def visualisation_args(self): #Для визуализации маятника
        return self.lineX, self.lineY, self.x, self.y

    def eKinPlot_args(self): #Для кинетической энергии
        return self.t, self.E_kin

    def ePotPlot_args(self): #Для потенциальной энергии
        return self.t, self.E_pot
    
    def ePlot_args(self): #Для полной энергии
        return self.t, self.E

    def phasePlot_args(self): #Для фазовой плоскости
        return self.x, self.p
        

    def startDraw(self): #Создание экземпляров графических областей и запуск рисования в них

        #Запуск визуализации маятника
        plt.subplot(2, 3, 1) #Выбор места на self.fig
        self.visualisation = GraphBase(xmin=-2, xmax=2, ymin=-0.5, ymax=2, r=10,
            title='Визуализация', xlabel='координата х', ylabel='координата у') #Создание объекта. Указан размер графика и радиус шарика
        anim = FuncAnimation(self.fig, self.visualisation.animate, fargs=(self.nextFrameCalc, self.visualisation_args),
            frames=2000, interval=pdl.dt*1000, blit=True) #Запуск рисование на этом графике
            #В аргументах передаётся считающая функция, которая изменяет все параметры маятника,
            #и функция, передающая нужные данные в функцию self.visualisation.animate

        #График кинетической энергии
        plt.subplot(2, 3, 2) #Всё аналогично описанию выше
        self.eKinPlot = GraphBase(xmin=0, xmax=np.pi*12, ymin=0, ymax=1,
            title='Кинетическая энергия', xlabel='время t', ylabel='энергия Екин')
        anim = FuncAnimation(self.fig, self.eKinPlot.animate_plot, fargs=(self.eKinPlot_args, ),
            frames=2000, interval=pdl.dt*1000, blit=True, repeat=False)

        #График потенциальной энергии
        plt.subplot(2, 3, 5) 
        self.ePotPlot = GraphBase(xmin=0, xmax=np.pi*12, ymin=0, ymax=1,
            title='Потенцальная энергия', xlabel='время t', ylabel='энергия Епот')
        anim = FuncAnimation(self.fig, self.ePotPlot.animate_plot, fargs=(self.ePotPlot_args, ),
            frames=2000, interval=pdl.dt*1000, blit=True, repeat=False)

        #График полной энергии
        plt.subplot(2, 3, 3) 
        self.ePlot = GraphBase(xmin=0, xmax=np.pi*12, ymin=0, ymax=1.2,
            title='Полная энергия', xlabel='время t', ylabel='энергия Е')
        anim = FuncAnimation(self.fig, self.ePlot.animate_plot, fargs=(self.ePlot_args, ),
            frames=2000, interval=pdl.dt*1000, blit=True, repeat=False)

        #Фазовая плоскость
        plt.subplot(2, 3, 4)
        self.phasePlot = GraphBase(xmin=-2, xmax=2, ymin=-2, ymax=2,
            title='Фазовая плоскость', xlabel='координата х', ylabel='импульс р')
        anim = FuncAnimation(self.fig, self.phasePlot.animate_plot, fargs=(self.phasePlot_args, ),
            frames=2000, interval=pdl.dt*1000, blit=True)

        


pdl = Pendulum(title = 'Без трения') #Создаём 1 экземпляр класса маятника
pdl.startDraw()  #Функция, запускающая рисование на графиках
plt.subplots_adjust(wspace=0.5, hspace=0.5) #расстояние между графиками

pdl2 = Pendulum(title = 'С трением') #Создаём 2 экземпляр класса маятника
pdl2.friction = True #трение вкл.
pdl2.startDraw()  #Функция, запускающая рисование на графиках

plt.subplots_adjust(wspace=0.5, hspace=0.5) #расстояние между графиками
plt.show() #Отображения окна mathplotlib