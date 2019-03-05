import random

class Experiment:
    def __init__ (self, list_params):
        self.num_rows_up = list_params[0]
        self.num_rows_down = list_params[1]
        self.rand_value_min = Time(list_params[2])
        self.rand_value_max = Time(list_params[3])
        self.curr_time = list_params[4]
        self.step = list_params[5]
        self.start_time = list_params[4]
        self.airport = Airport(list_params)


class Airport:

    def __init__(self, list_params):
        self.list_rows = []
        self.queue = []
        self.executing_bids = []
        self.schedule = []
        self.random_values = []
        tic = Time("0:01")

        self.num_rows_up = list_params[0]
        self.num_rows_down = list_params[1]
        self.rand_value_min = Time(list_params[2])
        self.rand_value_max = Time(list_params[3])
        self.curr_time = list_params[4]
        self.step = list_params[5]
        self.start_time = list_params[4]

        for i in range(0, list_params[0]):
            self.list_rows.append(Row('Up', 'Свободна'))
        for i in range(0, list_params[1]):
            self.list_rows.append(Row('Down', 'Свободна'))

        self.airplane_dict = {}
        file_airplanes = open("time_aiplanes.txt", 'r')
        for line in file_airplanes:
            a = line.split(" ")
            self.airplane_dict[a[0]] = Time(a[1])
        file_airplanes.close()

        tmp_time = Time(list_params[2])
        while(tmp_time <= Time(list_params[3])):
            self.random_values.append(tmp_time)
            tmp_time += tic

    def gen_bids(self):
        ops = ['+', '-']
        file_schedule = open("schedule.txt", 'r')
        for line in file_schedule:
            a = line.split(" ")
            rand_time = random.choice(self.random_values)
            if a[2].replace("\n", "") == 'Down':
                op = random.choice(ops)
            else:
                op = '+'
            self.schedule.append((Bid(Time(a[0]),a[2].replace("\n",""), a[1],self.airplane_dict[a[1]], rand_time, op)))
        file_schedule.close()

    def free_row(self,type):
        ret_row = 'Empty'
        i = 0
        for row in self.list_rows:
            if (row.type == type) and (row.is_occupied == "Свободна"):
                ret_row = row
                break
            i += 1
        return [ret_row,i]

    def num_occupied_rows(self):
        num = 0
        for row in self.list_rows:
            if(row.is_occupied == 'Занята'):
                num += 1
        return num



    def handle(self, data):
        new_data = data
        curr_time = self.curr_time
        self.curr_time += self.step
        tic = Time("0:01")

        while (curr_time < self.curr_time):

            for bid in self.schedule:
                if (bid.time_with_delay == curr_time):
                    self.queue.append(bid)
                    new_data.is_changed_queue = True

            for bid in self.executing_bids:
                if (bid[0].end_time > curr_time):
                    continue

                if (bid[0].delay != Time("0:00")):
                    new_data.all_delay += bid[0].delay
                    new_data.num_delayed_bids += 1
                    new_data.common_delay = new_data.all_delay / new_data.num_delayed_bids

                self.list_rows[bid[1]].is_occupied = 'Свободна'
                data.executed_bids.append(bid[0])
                self.executing_bids.remove(bid)
                new_data.total_bids += 1


                new_data.is_changed_rows = True


            for bid in self.queue:

                row = self.free_row(bid.type)

                if (row[0] != 'Empty'):
                    self.executing_bids.append([bid,row[1]])
                    self.list_rows[row[1]].is_occupied = 'Занята'

                    new_data.is_changed_rows = True
                    new_data.is_changed_queue = True
                    continue

                else:
                    bid.delay += tic
                    bid.start_time += tic
                    bid.end_time += tic

                    if (new_data.max_delay < bid.delay):
                        new_data.max_delay = bid.delay

            for instance in self.executing_bids:
                if instance[0] in self.queue:
                    self.queue.remove(instance[0])

            if (new_data.max_queue < len(self.queue)):
                new_data.max_queue = len(self.queue)

            if (new_data.is_changed_queue):
                if (len(self.queue) != 0):
                    new_data.common_queue *= new_data.count_queue
                    new_data.common_queue += len(self.queue)
                    new_data.count_queue += 1
                    new_data.common_queue /= new_data.count_queue
                    new_data.is_changed_queue = False

            if (new_data.is_changed_rows):
                if (self.num_occupied_rows() != 0):
                    new_data.common_occupied_rows *= new_data.count_rows
                    new_data.common_occupied_rows += self.num_occupied_rows()
                    new_data.count_rows += 1
                    new_data.common_occupied_rows /= new_data.count_rows
                    new_data.is_changed_rows = False

            curr_time += tic
        return new_data




class Data:
    def __init__(self, total_bids, max_delay, common_delay, common_occupied_rows, max_queue, common_queue):
        self.total_bids = total_bids
        self.max_delay = max_delay
        self.common_delay = common_delay
        self.common_occupied_rows = common_occupied_rows
        self.max_queue = max_queue
        self.common_queue = common_queue
        self.all_delay = Time("0:00")
        self.executed_bids = []
        self.num_delayed_bids = 0
        self.is_changed_rows = False
        self.is_changed_queue = False
        self.count_queue = 0
        self.count_rows = 0



class Row:
    def __init__(self, type, is_occupied):
        self.type = type
        self.is_occupied = is_occupied


class Airplane:
    def __init__(self, name, time_of_execution):
        self.name = name
        self.time_of_execution = time_of_execution


class Bid(Airplane):
    def __init__(self,time_in_schedule,type,name, time_of_execution, delay_time, op):
        Airplane.__init__(self,name, time_of_execution)
        self.type = type
        self.time_in_schedule = time_in_schedule
        self.delay = Time("0:00")
        if (op == '+'):
            self.end_time = time_in_schedule + time_of_execution + delay_time
            self.start_time = time_in_schedule + delay_time
            self.time_with_delay = time_in_schedule + delay_time
        else:
            self.end_time = time_in_schedule + time_of_execution - delay_time
            self.start_time = time_in_schedule - delay_time
            self.time_with_delay = time_in_schedule - delay_time


    def __str__(self):
        return self.name +"\n" +  self.type + "\n" + str(self.time_in_schedule) + "\n" + str(self.time_with_delay)

    def __repr__(self):
        return self.__str__()


class Time:

    def __init__(self, string):
        a = string.split(":")
        if (a[0] != "0"):
            self.hour = eval(a[0].lstrip("0"))
        else:
            self.hour = 0
        if (a[1] != "00"):
            self.minute = eval(a[1].lstrip("0"))
        else:
            self.minute = 0

    def __lt__(self,other):
        if (self.hour == other.hour):
            return self.minute < other.minute
        else:
            return self.hour < other.hour

    def __gt__(self, other):
        if (self.hour == other.hour):
            return self.minute > other.minute
        else:
            return self.hour > other.hour

    def __add__(self, other):
        if ((self.minute + other.minute) % 60 < 10):
            minute_str = "0" + str((self.minute + other.minute)%60)
        else:
            minute_str =  str((self.minute + other.minute)%60)
        return Time(str((self.hour + other.hour + (self.minute + other.minute)//60) % 24) +":" + minute_str)

    def __str__(self):
        if (self.minute < 10):
            return str(self.hour) + ":0" + str(self.minute)
        else:
            return  str(self.hour) + ":" +  str(self.minute)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.hour == other.hour) and (self.minute == other.minute)

    def __ge__(self, other):
        return not(self < other)

    def __truediv__(self, other):
        tmp = self.hour*60 + self.minute
        tmp_div = tmp //other
        hour = tmp_div // 60
        min = tmp_div % 60
        if (min < 10):
            return Time(str(hour) + ":0" + str(min))
        else:
            return Time(str(hour) + ":" + str(min))

    def __mul__(self, other):
        tmp = self.hour * 60 + self.minute
        tmp_div = tmp * other
        hour = tmp_div // 60
        min = tmp_div % 60
        if (min < 10):
            return Time(str(hour) + ":0" + str(min))
        else:
            return Time(str(hour) + ":" + str(min))

    def __sub__(self, other):
        tmp = self.hour * 60 + self.minute
        tmp_other = other.hour * 60 + other.minute
        tmp_div = tmp - tmp_other
        hour = tmp_div // 60
        min = tmp_div % 60
        if (min < 10):
            return Time(str(hour) + ":0" + str(min))
        else:
            return Time(str(hour) + ":" + str(min))