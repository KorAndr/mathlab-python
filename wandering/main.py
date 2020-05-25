#Ex.3 — Random wandering

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec

import GraphBaseLib as gbl #Импорт интерфейса для matplotlib (см. в этой же папке)

class Visualisation(gbl.GraphBase): #Класс окна визуализации
    def __init__(self, nomber, xmin = -1, xmax = 1, ymin = -1, ymax = 1, title = '', xlabel = '', ylabel = '', r=3):
        gbl.GraphBase.__init__(self, xmin, xmax, ymin, ymax, title, xlabel, ylabel, r) #Родительский конструктор
        self.nomber = nomber #количество частиц
        self.particles = [] #кортеж для отрисовки частиц
        for i in range(0, self.nomber): #Создаём объекты для рисования из класса Circle
            prt = gbl.Circle(r=self.r, color='#1D1764')
            self.particles.append(prt) 

        #Гистограмма
        self.hist, = plt.plot([], [], 'k-', lw=1, color = '#AD584E') #Создаём объект рисования
        self.hist_x, self.hist_y = [], [] #Кортежи с точками на Х и У
        self.hist_count = 20 #На сколько частей будет разделена гистограмма
        self.xmin = xmin #Лимиты осей
        self.xmax = xmax
        self.ymin = ymin
        self.hist_unit = (-xmin+xmax)/self.hist_count #Длина одного кусочка гистограммы
        
        #Распределение Гаусса (теоретическое)
        self.gaus, = plt.plot([], [], 'k-', lw=1, color = '#E0914E') #создание объекта рисования
        self.gausX = np.linspace(self.xmin, self.xmax, 200) #Точки на оси х
    
    def animate(self, i, calsFunc, argsFunc): #Функция, рисующая визуализацию
        calsFunc(i) #Функия, изменяющая все папаметры системы

        particles = argsFunc() #Функция, передающая нужные данные о системе
        rtn = [] #кортеж возврата

        #Частицы
        for j in range(0, self.nomber): #Пробегаем по всем
            self.particles[j].changeXY(particles[j].x, particles[j].y) #Передаём данные в кортеж для рисования частиц
            self.particles[j].draw() #Рисуем частицу
            rtn.append(self.particles[j].point) #Добавляем в возвратный кортеж

        #Гистограмма
        self.hist_x, self.hist_y = [], [] #Обнуляем данные
        for j in range(0, self.hist_count): #Пробегаем по всем кусочкам гистограммы
            x = self.hist_unit*j + self.xmin #Начальная координата полки
            count = 0 #Счётчик частиц
            for prt in particles: #Назодим частицы в диапазоне кусочка
                if prt.x > x and prt.x < x+self.hist_unit:
                    count+=1 #считаем их
            self.hist_x.append(x) #Добавляем кооржинаты полки
            self.hist_x.append(x+self.hist_unit)
            self.hist_y.append(count + self.ymin)
            self.hist_y.append(count + self.ymin)
        
        #Отправляем данные в окно рисования
        self.hist.set_data(self.hist_x, self.hist_y)
        rtn.append(self.hist) #Добавляем к возвратному кортежу

        #Гаусс
        #Рассчёт по формуле
        self.gausY = 1/np.sqrt(2*np.pi*(i+1)*particles[0].vx**2)*np.exp(-1*self.gausX**2/(2*(i+1)*particles[0].vx**2))*len(particles)+self.ymin
        self.gaus.set_data(self.gausX, self.gausY) #Рисуем
        rtn.append(self.gaus) #Добавляем в кортеж возврата

        return rtn #Для обновления не всей области рисования, а только изменённой


class Particle(object): #Класс частицы
    def __init__(self, x=0, y=0, vx=0, vy=0): #начальные данные
        self.x, self.y = x, y #координаты
        self.vx, self.vy = vx, vy #Безразмерная скорость - количество пикселей смещения 

        self.r = 3 #Радиус частицы (для отображения)
    
    def binaryRand(self): #Функция, возвращающая 1 или -1
        rand = np.random.randint(low=0, high=2) #число 0 до 1
        #rand = int(rand*10) % 2 #число 0 или 1
        if (rand == 0):
            rand = -1
        return rand #число 1 или -1

    def moving(self): #Функция, перемещающая частицу
        self.x += self.vx*self.binaryRand() #Направляем смещенеие в случайную сторону
        self.y += self.vy*self.binaryRand() #и складываем с координатами


class Surface(object): #Объявление класса поверхности
    def __init__(self, title = ''):
        self.t = 0 #время
        self.dt = 0.05 #шаг времени

        self.pNomber = 100 #Колличество частиц (можно менять)

        self.averageX, self.averageXX = 0, 0 #Среднее и среднеквадратичное значнение координаты

        n = 3 #коэффициент масштабирования
        self.fig = plt.figure(figsize=(3*n, 2*n)) #окно для рисования
        self.fig.suptitle(title) #подзаголовок окна
        self.grs = gridspec.GridSpec(nrows=2, ncols=3, figure=self.fig) #Средство размещения графиков
        plt.gcf().canvas.set_window_title('Задание 3.1 — одномерные блуждания') #Заголовок окна

        self.particles = [] #Кортеж частиц

        for i in range(0, self.pNomber): #Создание частиц
            x = 0 
            y = -1*self.pNomber/2 + i #для равномерного распределение около нуля
            prt = Particle(x, y, vx=0.1, vy=0) #Создаём экземпляр частицы
            self.particles.append(prt) #Добавляем в кортеж
        
    
    def nextFrameCalc(self, i): #Вычисление параметров системы
        self.t = self.dt * i #Изменение времени

        for prt in self.particles: #Двигаем все частицы
            prt.moving()

        self.averageX = 0 #Обнуление показателей
        self.averageXX = 0
        for prt in self.particles: #Считыаем новые
            self.averageX += prt.x
            self.averageXX += prt.x**2
        self.averageX = self.averageX/self.pNomber 
        self.averageXX = self.averageXX/self.pNomber       
    
    #Функции, передающие нужные аргументы соответствующей animate()

    def visualisation_args(self): #Для визуализации
        return self.particles   #массив частиц     

    def averageX_args(self): #Для средней координаты
        return self.t, self.averageX

    def averageXX_args(self): #Для среднеквадратичной координаты
        return self.t, self.averageXX



    def startDraw(self): #Создание экземпляров графических областей и запуск рисования в них

        #Запуск визуализации
        limit = self.pNomber/2 + 1

        self.fig_ax_1 = self.fig.add_subplot(self.grs[:, :2]) #Выбор места на self.fig
        self.visualisation = Visualisation(self.pNomber, xmin=-10, xmax=10, ymin=-limit, ymax=limit, r = 3,
            title='Визуализация', xlabel='координата х', ylabel='координата у') #Создание объекта. Указан размер графика
        FuncAnimation(self.fig, self.visualisation.animate, fargs=(self.nextFrameCalc, self.visualisation_args),
            frames=3000, interval=self.dt*1000, blit=True) #Запуск рисования на этом графике
            #В аргументах передаётся считающая функция, которая изменяет все параметры системы,
            #и функция, передающая нужные данные в функцию self.visualisation.animate

        #Средняя координата
        #Всё аналогично
        self.fig_ax_2 = self.fig.add_subplot(self.grs[0, 2])
        self.averageXPlot = gbl.Plot(xmin=0, xmax=30, ymin=-1, ymax=1, r = 3,
            title='Среднее смещение', xlabel='время t', ylabel='<x(t)>') 
        FuncAnimation(self.fig, self.averageXPlot.animate, fargs=(self.averageX_args, ),
            frames=3000, interval=self.dt*1000, blit=True) 
        
        #Среднеквадратичная координата
        self.fig_ax_3 = self.fig.add_subplot(self.grs[1, 2])
        self.averageXXPlot = gbl.Plot(xmin=0, xmax=30, ymin=0, ymax=5, r = 3,
            title='Среднеквадратичное смещение', xlabel='время t', ylabel='<x^2(t)>') 
        FuncAnimation(self.fig, self.averageXXPlot.animate, fargs=(self.averageXX_args, ),
            frames=3000, interval=self.dt*1000, blit=True)
     



sfc = Surface(title = 'Блуждания') #Создаём экземпляр класса поверхности
sfc.startDraw()  #Функция, запускающая рисование на графиках
plt.subplots_adjust(wspace=0.5, hspace=0.5) #расстояние между графиками

plt.show() #Отображения окна mathplotlib