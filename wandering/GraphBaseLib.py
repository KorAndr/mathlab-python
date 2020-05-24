import matplotlib.pyplot as plt

class Circle(object): #Круглый объект - для визуализации или отрисовки графиков
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

class Plot(GraphBase): #Класс окна графика
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

class Hist(GraphBase):
    pass