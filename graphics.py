from tkinter import *
from Classes import *


def window_deleted_param(param):
    param.destroy()
    exit(0)

def window_deleted(param):
    param.destroy()

def stop_experiment(root):
    print('Эксперимент окончен')
    root.quit()

def save_params(num_rows_up, num_rows_down,random_value_min, random_value_max, begining_time, step, list, window):
    list[0] = eval(num_rows_up)
    list[1] = eval(num_rows_down)
    list[2] = random_value_min.replace("\n", "")
    list[3] = random_value_max.replace("\n", "")
    list[4] = Time(begining_time)
    list[5] = Time(step)
    window.destroy()



def init_params():


    param = Tk()
    param.title('Параметры эксперимента')

    label = Label(param,text = 'Число взлетных полос:')
    label.grid(column = 0, row = 0)
    num_rows_up = Text(param, height = 1, width = 5)
    num_rows_up.grid(column = 1, row = 0)

    label = Label(param,text =  'Число посадочных полос:')
    label.grid(column = 0, row = 1)
    num_rows_down = Text(param, height = 1, width = 5)
    num_rows_down.grid(column = 1, row = 1)

    label = Label(param,text =  'Диапазон разброса случайной величины:')
    label.grid(column = 0, row = 2)
    random_value_max = Text(param, height = 1, width = 5)
    random_value_max.grid(column = 2, row = 2)
    random_value_min = Text(param, height = 1, width = 5)
    random_value_min.grid(column = 1, row = 2)

    label = Label(param,text =  'Шаг моделироания:')
    label.grid(column = 0, row = 3)
    step = Text(param, height = 1, width = 5)
    step.grid(column = 1, row = 3)

    label = Label(param,text =  'Начало рабочего дня:')
    label.grid(column = 0, row = 4)
    begining_time = Text(param, height = 1, width = 5)
    begining_time.grid(column = 1, row = 4)

    params = [0 for i in range(0, 6)]
    start_experiment = Button(param, text = 'Начать эксперимент!', width = 20, height = 1, bg = 'green', command =
    lambda : save_params(num_rows_up.get('1.0',END), num_rows_down.get('1.0', END), random_value_min.get('1.0', END), random_value_max.get('1.0', END),
                         begining_time.get('1.0',END), step.get('1.0',END), params, param))
    start_experiment.grid(row = 5)

    param.protocol('WM_DELETE_WINDOW', lambda: window_deleted_param(param))
    param.mainloop()
    return params

def draw(root,airport, data):
    #Инициализация фреймов
    rows_state_frame = Frame(root, bg = 'white',bd = 5, height = 20, width = 100)
    curr_time_frame = Frame(root, bg = 'white',bd = 5)
    queue_frame = Frame(root, bg = 'white',bd = 5)
    data_frame = Frame(root, bg = 'white', bd = 5)
    buttons_frame = Frame(root, bg = 'white', bd =5)

    #Иницинализация кнопок
    button_new_eperiment = Button(buttons_frame,text = 'Новый эксперимент',width = 20,height = 2,bg = 'red',fg = 'white', command = lambda: new_experiment(root))
    button_step = Button(buttons_frame, text = 'Шаг', width = 20, height = 2, bg = 'green', fg = 'black', command = lambda: update(root, airport, data))
    button_full_experiment = Button(buttons_frame, text = 'Эксперимент целиком', width = 20, height = 2, bg = 'green', fg = 'black', command = lambda : full_experiment(root,airport, data))
    button_full_experiment.pack()
    button_new_eperiment.pack()
    button_step.pack()

    # Заполнение окна "Полосы"
    rows = Label(rows_state_frame, text = 'Полосы')
    rows.grid(column = 0, row = 0)
    j = 0
    k = 0
    for i in range(0, len(airport.list_rows)):
        if (airport.list_rows[i].type == 'Up'):
            j += 1
            label = Label(rows_state_frame, text = 'Взлетная полоса №' + str(j) + ': ' + airport.list_rows[i].is_occupied)
            label.grid(column = 0, row = i + 1)
        else:
            k += 1
            label = Label(rows_state_frame, text='Посадочная полоса №' + str(k) + ': ' + airport.list_rows[i].is_occupied)
            label.grid(column = 0, row = i + 1)

    # Заполнение поля текущее время
    time = Label(curr_time_frame, text = 'Текующее время: ' + str(airport.curr_time))
    time.pack()


    # Заполнение очереди
    queue = Label(queue_frame, text = "Очередь заявок:")
    queue.grid(column=len(airport.queue) // 2, row=0)
    for i in range(0, len(airport.queue)):
        label = Label(queue_frame, text = airport.queue[i])
        label.grid(column = i+1, row = 1)

    # Заполнение данных
    num_fullfill_bids = Label(data_frame, text = "Общее количество обслуженных заявок: " )
    num_fullfill_bids.grid(row = 0, column = 0)
    label = Label(data_frame, text = str(data.total_bids))
    label.grid(row = 0, column = 1)

    label = Label(data_frame, text = "Максимальная задержка: ")
    label.grid(row = 1, column = 0)
    label = Label(data_frame, text = str(data.max_delay))
    label.grid(row = 1, column = 1)

    label = Label(data_frame, text="Средняя задержка: ")
    label.grid(row=2, column=0)
    label = Label(data_frame, text=str(data.common_delay))
    label.grid(row=2, column=1)

    label = Label(data_frame, text="Среднняя занятость полос: ")
    label.grid(row=3, column=0)
    label = Label(data_frame, text=str(round(data.common_occupied_rows,2)))
    label.grid(row=3, column=1)

    label = Label(data_frame, text="Максимальная длина очереди: ")
    label.grid(row=4, column=0)
    label = Label(data_frame, text=str(data.max_queue))
    label.grid(row=4, column=1)

    label = Label(data_frame, text="Средняя длина очереди: ")
    label.grid(row=5, column=0)
    label = Label(data_frame, text=str(round(data.common_queue,2)))
    label.grid(row=5, column=1)

    # Отрисовка фреймов
    rows_state_frame.grid(row = 0, column = 0, rowspan = 5, columnspan = 10)
    curr_time_frame.grid(row = 5, column = 0, columnspan = 10)
    queue_frame.grid(row = 6, column = 0, rowspan = 3, columnspan = 10)
    data_frame.grid(row = 0, column = 10, rowspan = 4, columnspan = 10)
    buttons_frame.grid(row = 4, column = 10, rowspan = 4, columnspan = 10)


def update(window, airport, data):
    if (airport.curr_time > Time("23:00")):
        window.destroy()
        params = Tk()
        params.title('Полученные данные:')
        draw_params(params, data)
        params.protocol('WM_DELETE_WINDOW', lambda: window_deleted(params))
        params.mainloop()
        execute_bid = Tk()
        execute_bid.title('Выполненные заявки:')
        draw_bids(execute_bid, data)
        execute_bid.protocol('WM_DELETE_WINDOW', lambda: window_deleted(execute_bid))
        execute_bid.mainloop()
        exit(0)

    for i in window.winfo_children():
        i.destroy()
    data = airport.handle(data)
    draw(window,airport, data)


def new_experiment(window):
    if (window != "First"):
        window.destroy()

    parametrs_exp = init_params()
    exp = Experiment(parametrs_exp)
    data = Data(0,Time("0:00"),Time("0:00"),0,0,0)
    root = Tk()
    root.protocol('WM_DELETE_WINDOW', lambda: stop_experiment(root))
    exp.airport.gen_bids()
    draw(root, exp.airport, data)
    root.mainloop()

def full_experiment(window, airport, data):
    while(airport.curr_time <= Time("23:00")):
        data = airport.handle(data)
    window.destroy()
    params = Tk()
    params.title('Полученные данные:')
    draw_params(params, data)
    params.protocol('WM_DELETE_WINDOW', lambda: window_deleted(params))
    params.mainloop()



def draw_params(data_frame, data):
    num_fullfill_bids = Label(data_frame, text="Общее количество обслуженных заявок: ")
    num_fullfill_bids.grid(row=0, column=0)
    label = Label(data_frame, text=str(data.total_bids))
    label.grid(row=0, column=1)

    label = Label(data_frame, text="Максимальная задержка: ")
    label.grid(row=1, column=0)
    label = Label(data_frame, text=str(data.max_delay))
    label.grid(row=1, column=1)

    label = Label(data_frame, text="Средняя задержка: ")
    label.grid(row=2, column=0)
    label = Label(data_frame, text=str(data.common_delay))
    label.grid(row=2, column=1)

    label = Label(data_frame, text="Среднняя занятость полос: ")
    label.grid(row=3, column=0)
    label = Label(data_frame, text=str(round(data.common_occupied_rows,2)))
    label.grid(row=3, column=1)

    label = Label(data_frame, text="Максимальная длина очереди: ")
    label.grid(row=4, column=0)
    label = Label(data_frame, text=str(data.max_queue))
    label.grid(row=4, column=1)

    label = Label(data_frame, text="Средняя длина очереди: ")
    label.grid(row=5, column=0)
    label = Label(data_frame, text=str(round(data.common_queue,2)))
    label.grid(row=5, column=1)

    button = Button(data_frame, text='Полные данные по заявкам', width=25, height=2, bg='green', fg='black',
                         command=lambda: draw_bids(data, data_frame))
    button.grid(row = 6)

def draw_bids(data, krot):
    krot.destroy()
    root = Tk()
    root.title('Выполненные заявки:')
    j = 0
    i = 0
    root.protocol('WM_DELETE_WINDOW', lambda: window_deleted(root))
    frame = Frame(root, bg = 'white',bd = 5)
    for bid in data.executed_bids:
        label = Label(frame, text = bid.name)
        label.grid(row = j, column = 0)
        label = Label(frame, text = bid.type)
        label.grid(row = j, column = 1)
        label = Label(frame, text = str(bid.time_in_schedule))
        label.grid(row = j, column = 2)
        label = Label(frame, text = str(bid.time_with_delay), fg = 'blue')
        label.grid(row = j, column = 3)
        if(bid.time_with_delay == bid.start_time):
            label = Label(frame, text = str(bid.start_time), fg = 'green')
        else:
            label = Label(frame, text = str(bid.start_time), fg = 'red')
        label.grid(row = j, column = 4)
        label = Label(frame, text=str(bid.end_time), bg = 'orange')
        label.grid(row=j, column=5)
        j += 1
        if (j == 30):
            frame.grid(row = 0, column = i)
            j = 0
            i += 1
            frame = Frame(root, bg='white', bd=5)
    frame.grid(row=0, column=i)
    root.mainloop()

new_experiment("First")