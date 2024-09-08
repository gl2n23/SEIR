import ollama
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
import random
from scipy.stats import lognorm
from scipy.stats import norm
from Image_transit import matrix
from AgentProfiles import work_places, careers, home_locations
from mesa.time import BaseScheduler
import time
import numpy as np
import csv
from Agent_coordinates import ordered_family_ids, accept_change_list, dislike_masks_list, care_others_list, coordinates
from prompts import past_schedules, dict_combine, message_select



infected_prob1 = 0.1  # 在一定距离内被传播的概率
infected_prob2 = 0.02  # 感染者戴口罩面对没戴口罩的普通人，传播的概率
infected_prob3 = 0.06  # 普通人戴口罩面对没戴口罩的感染者，被传播的概率
infected_prob4 = 0.005  # 双方都戴口罩时，普通人被传播的概率

illness_prob1 = 0.005
illness_prob2 = 0.01
illness_prob3 = 0.025

severe_prob1 = 0.01
severe_prob2 = 0.05
severe_prob3 = 0.15

infecting_number = 0  # 注意这个0是初始化用的
infected_number = 0
recovered_number = 0
expo_infe_number = 0
severe_number = 0

lockdown = False

agent_number = 500
column_names = [f"Agent{i}" for i in range(1, agent_number + 1)]
#file_path = 'Agents/agent_states.csv'

input("Press Enter to continue and clear file contents...")

for file_name in ['exposed_ids', 'infected_ids', 'recovered_ids', 'exposed_times', 'infected_times']:
    file_path = 'Results/{}.csv'.format(file_name)
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)

for agent_name in range(1, agent_number+1):
    file_path = "Agents/Agent{}_Response.txt".format(agent_name)
    with open(file_path, mode='w', newline='') as file:  # 清空重置文件夹内容
        pass

for file_name in ['infecting_number', 'infected_number', 'recovered_number', 'severe_number', 'expo_infe_number']:
    file_path = 'Results/{}.txt'.format(file_name)
    with open(file_path, mode='w', newline='') as file:
        pass

column_names1 = ['primary school', 'high school', 'office area 1', 'office area 2', 'office area 3', 'office area 4', 'commercial area 1', 'commercial area 2', 'entertainment area 1', 'entertainment area 2', 'park']
with open('Results/areas_record.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(column_names1)


def get_response(messages0, model0='llama3:8b-instruct-q6_K'):

    if messages0:

        response = ollama.chat(model=model0, messages=messages0)

        try:
            response1 = eval(response['message']['content'])['schedule']
            response2_0 = eval(response['message']['content'])['mask']

            if isinstance(response2_0, bool):
                response2 = response2_0
            else:
                response2 = False

        except:
            print(type(response['message']['content']))
            print(response['message']['content'])
            response1 = {'08:00': 'home'}
            response2 = False

        return [response1, response2]

    else:
        return[{}, False]

def get_time(response):

    time_list = []
    time_transferred = 0

    for key in response:
        # print(key)
        try:
            hours, minutes = map(int, key.split(':'))
            time_transferred = 2*(1*hours + minutes/60)
            time_list.append(time_transferred)
        except:
            time_list.append(time_transferred + 1)
            print('error', response)
            # raise AttributeError('Format')

    return time_list


def get_destination(response):

    destination_list = []
    for key in response:

        try:
            destination_list.append(response[key].lower())
        except:
            pass

    return destination_list


class TextAgent(Agent):
    def __init__(self, unique_id, model, text, text_color='black'):
        super().__init__(unique_id, model)
        self.text = text
        self.text_color = text_color

    def step(self):
        pass

class WallAgent(Agent):
    def __init__(self, pos, model, wall_type):
        super().__init__(pos, model)
        self.pos = pos
        self.wall_type = wall_type

    def step(self):
        pass


class MovingAgent(Agent):

    def __init__(self, unique_id, model, color='green'):
        """
        定义智能体属性，有起点坐标self.start，有终点坐标self.goal，移动路径暂时为空列表[]，path_index表示t时间步

        定义智能体属性，包含智能体位置，智能体状态，智能体当天行动地点

        """
        super().__init__(unique_id, model)

        self.career = ''  # 智能体职业
        self.work_place = ''  # 智能体日常工作地点
        self.current_location = ''  # 智能体当前地点
        self.current_coordinate = ''  # 智能体当前坐标（只影响可视化的效果）
        self.home_coordinate = ''  # 智能体每天结束后放置的坐标，所有智能体都放一块，方便观察感染情况（这也只影响可视化的效果）
        self.characteristics = ''  # 智能体个人特征
        self.last_location = 'home'
        self.home_site = ''
        self.illness_prob = 0
        self.severe_prob = 0

        self.today_time_table = []
        self.today_candidate_destinations = []
        self.destinations_reached_number = 0
        self.past_schedules = []

        self.color = color
        self.mask = False
        self.exposed = False
        self.infected = False
        self.recovered = False
        self.time_exposed = 0
        self.time_infected = 0
        self.other_illness = False
        self.severe = False
        self.time_severe = 0
        self.repeat = False
        self.tohospital = False
        self.know = False
        self.knowtime = 0

        self.met = 0
        self.infected_met = 0
        self.infected_people_met = []

        self.exposed_total_time = 0
        self.infected_total_time = 0
        self.severe_total_time = 0

        self.LLM_response = []
        self.number_added = False

    def step(self):

        pass

    def get_coordinate(self, destination):
        """
        需要修改具体坐标位置
        """
        dict_dest = {
            'office area 1': (random.randint(3, 22), random.randint(39, 58)),
            'office area 2': (random.randint(3, 22), random.randint(63, 82)),
            'commercial area 1': (random.randint(66, 95), random.randint(87, 116)),
            'commercial area 2': (random.randint(100, 129), random.randint(87, 116)),
            'office area 3': (random.randint(27, 46), random.randint(39, 58)),
            'office area 4': (random.randint(27, 46), random.randint(63, 82)),
            'entertainment area 1': (random.randint(51, 70), random.randint(39, 58)),
            'entertainment area 2': (random.randint(51, 70), random.randint(63, 82)),
            'primary school': (random.randint(3, 27), random.randint(89, 113)),
            'high school': (random.randint(32, 61), random.randint(87, 116)),
            'park': (random.randint(75, 114), random.randint(41, 80)),
            'hospital': (random.randint(121, 145), random.randint(49, 73)),
            'home': self.home_coordinate
        }

        return dict_dest[destination]


class SEIRModel(Model):

    """
    该模型中无症状感染者也可以传播疾病
    """

    def __init__(self, width, height, city_map):

        self.grid = MultiGrid(width, height, True)
        # self.schedule = RandomActivation(self)
        self.schedule = BaseScheduler(self)  # Mesa中的调度函数，用于在每个时间步长t按照随机顺序激活智能体行动
        self.map = city_map
        self.weekday = 'Monday'  # 规定星期几
        self.days = -1

        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if city_map[y][x] == 1:
                    wall_type = city_map[y][x]  # 注意：矩阵行列与网格坐标相反
                    wall = WallAgent((x, y), self, wall_type)
                    self.grid.place_agent(wall, (x, y))
                    self.schedule.add(wall)

        area_names = 'office area 1', 'office area 2', 'office area 3', 'office area 4', 'commercial area 1', 'commercial area 2', 'entertainment area 1', 'entertainment area 2', 'high school', 'primary school', 'park', 'hospital'
        name_starts = [(6, 48), (7, 72), (30, 48), (30, 72), (73, 101), (107, 101), (51, 48), (51, 72), (41, 101), (9, 101), (92, 60), (129, 60)]

        for name, start in zip(area_names, name_starts):
            n = 0
            start_x, start_y = start[0], start[1]  # Starting position of the word
            for i, word in enumerate(name):
                text_agent = TextAgent(n, self, word)
                self.grid.place_agent(text_agent, (start_x + i, start_y))
                n += 1

        for i in range(0, agent_number):
            agent = MovingAgent(i + 1, self)
            agent.career = careers[i]
            agent.work_place = work_places[i]
            agent.home_coordinate = coordinates[i]
            agent.home_site = ordered_family_ids[i]

            if agent.career == 'old person':
                agent.illness_prob = illness_prob3
                agent.severe_prob = severe_prob3

            elif agent.career == 'primary school student':
                agent.illness_prob = illness_prob2
                agent.severe_prob = severe_prob2

            else:
                agent.illness_prob = illness_prob1
                agent.severe_prob = severe_prob1

            if accept_change_list[i]:
                agent.characteristics = agent.characteristics + "open to change, "
            else:
                agent.characteristics = agent.characteristics + "not easily changed, "

            if dislike_masks_list[i]:
                agent.characteristics = agent.characteristics + "dislike masks, "
            else:
                agent.characteristics = agent.characteristics + "don't mind masks, "

            if care_others_list[i]:
                agent.characteristics = agent.characteristics + "care other people."
            else:
                agent.characteristics = agent.characteristics + "don't care other people."

            self.schedule.add(agent)
            self.grid.place_agent(agent, agent.home_coordinate)

            if i == 1:
                agent.exposed = True
                agent.exposed_total_time = int(np.round(np.random.normal(3, 1)*48))

                agent.color = 'yellow'

    def step(self):
        # print(f'当前步数为{self.schedule.steps}')
        self.agents_go_home()
        self.get_next_day_routines()
        self.agents_move()
        self.spread()
        self.repeat_initialize()
        self.state_transfer()
        self.results_record()
        self.schedule.step()  # 该函数是使得步数+1

    def agents_go_home(self):
        for agent in self.schedule.agents:
            if isinstance(agent, MovingAgent):

                if self.schedule.steps % 48 == 0:  # 保证每天开始时智能体一定在家
                    agent.current_location = 'home'
                    agent.current_coordinate = agent.get_coordinate(agent.current_location)
                    agent.model.grid.move_agent(agent, agent.current_coordinate)

    def agents_move(self):

        for agent in self.schedule.agents:
            if isinstance(agent, MovingAgent):

                if agent.destinations_reached_number < len(agent.today_candidate_destinations):


                    if self.schedule.steps % 48 == agent.today_time_table[agent.destinations_reached_number]:

                        try:
                            agent.current_coordinate = agent.get_coordinate(agent.today_candidate_destinations[agent.destinations_reached_number])
                            agent.current_location = agent.today_candidate_destinations[agent.destinations_reached_number]  # 如果能成功获取坐标则意味着提供的destination是正确的，那么此时再更改current_location的值
                        except KeyError:
                            agent.current_coordinate = agent.get_coordinate(agent.current_location)

                        agent.model.grid.move_agent(agent, agent.current_coordinate)  # 在可视化图中标出位置
                        agent.destinations_reached_number += 1

                    else:

                        if agent.current_location != 'home':
                            #possible coordinates at next time step
                            possible_newpos = [
                                (agent.current_coordinate[0], agent.current_coordinate[1]),
                                (agent.current_coordinate[0] + 1, agent.current_coordinate[1]),
                                (agent.current_coordinate[0] - 1, agent.current_coordinate[1]),
                                (agent.current_coordinate[0], agent.current_coordinate[1] + 1),
                                (agent.current_coordinate[0], agent.current_coordinate[1] - 1)
                            ]

                            valid_steps = []

                            #remove the coordinates not accessible

                            for new_pos in possible_newpos:

                                cell_contents = agent.model.grid.get_cell_list_contents(new_pos)
                                accessible = True

                                for i in cell_contents:
                                    if isinstance(i, WallAgent):
                                        accessible = False
                                        break

                                if accessible:
                                    valid_steps.append(new_pos)

                            # 过滤掉超出边界和撞墙的方向
                            #valid_steps = [new_pos for new_pos in possible_newpos if agent.model.grid.out_of_bounds(
                            #    new_pos) == False and agent.model.grid.get_cell_list_contents(new_pos)]

                            # 随机选择一个有效的方向移动
                            if valid_steps:
                                new_position = random.choice(valid_steps)
                                agent.model.grid.move_agent(agent, new_position)
                                agent.current_coordinate = new_position


    def spread(self):

        office_area_1_number = 0
        office_area_2_number = 0
        office_area_3_number = 0
        office_area_4_number = 0
        commercial_area_1_number = 0
        commercial_area_2_number = 0
        entertainment_area_1_number = 0
        entertainment_area_2_number = 0
        park_number = 0
        high_school_number = 0
        primary_school_number = 0
        home_number = 0
        hospital_number = 0

        areas_record_dict = {
            'office area 1': office_area_1_number,
            'office area 2': office_area_2_number,
            'office area 3': office_area_3_number,
            'office area 4': office_area_4_number,
            'commercial area 1': commercial_area_1_number,
            'commercial area 2': commercial_area_2_number,
            'entertainment area 1': entertainment_area_1_number,
            'entertainment area 2': entertainment_area_2_number,
            'park': park_number,
            'high school': high_school_number,
            'primary school': primary_school_number,
            'home': home_number,
            'hospital': hospital_number
        }

        for agent_x in self.schedule.agents:
            if isinstance(agent_x, MovingAgent):
                if agent_x.current_location == 'home':
                    continue

                for agent_y  in self.schedule.agents:
                    if isinstance(agent_y, MovingAgent):

                        if agent_x.unique_id == agent_y.unique_id:
                            continue
                        if agent_y.current_location == 'home':
                            continue

                        dist_xy = sum((np.array(agent_x.current_coordinate) - np.array(agent_y.current_coordinate)) ** 2)
                        if dist_xy <= 2:
                            agent_x.met += 1


        for agent_x in self.schedule.agents:

            if isinstance(agent_x, MovingAgent):

                if agent_x.repeat:  # 因为智能体被传播后首先视为无症状感染者，所以在这一步是不需要计入别人遇到的有症状的
                    continue
                if agent_x.exposed == False and agent_x.infected == False:  # 如果智能体x没有处于感染状态那么跳过（这里包括了未被感染的和已经康复的情况）
                    continue
                # if agent_x.current_location == 'home':
                #     continue

                for agent_y in self.schedule.agents:

                    if isinstance(agent_y, MovingAgent):

                        if agent_y.recovered:  # 如果智能体y已康复，跳过
                            continue
                        if agent_y.exposed == True or agent_y.infected == True:  # 判断y是否已经感染了，如果感染了就跳过
                            continue
                        if agent_x.unique_id == agent_y.unique_id:  # 如果遍历到的两个智能体是同一个，则跳过
                            continue

                        if agent_x.current_location == 'home' and agent_y.current_location == 'home':  # 判断x和y在这个时间点是不是都在家里

                            if agent_x.home_site == agent_y.home_site:  # 如果都在家里则判断这两个是否为一家的，是一家的则判断是否传播

                                agent_y.infected_people_met.append(agent_x.unique_id)

                                if random.random() <= 0.5:  # 在家中时每个时刻有0.5的概率有效接触

                                    if agent_x.mask == False and agent_y.mask == False:  # 其实这里可以用字典，使用键值组合来提取概率情况
                                        if random.random() <= infected_prob1:
                                            agent_y.exposed = True
                                            agent_y.exposed_total_time = int(np.round(np.random.normal(3, 1)*48))

                                            agent_y.color = 'yellow'
                                            agent_y.repeat = True
                                            areas_record_dict[agent_y.current_location] += 1

                                    elif agent_x.mask == True and agent_y.mask == False:
                                        if random.random() <= infected_prob2:
                                            agent_y.exposed = True
                                            agent_y.exposed_total_time = int(np.round(np.random.normal(3, 1)*48))

                                            agent_y.color = 'yellow'
                                            agent_y.repeat = True
                                            areas_record_dict[agent_y.current_location] += 1

                                    elif agent_x.mask == False and agent_y.mask == True:
                                        if random.random() <= infected_prob3:
                                            agent_y.exposed = True
                                            agent_y.exposed_total_time = int(np.round(np.random.normal(3, 1)*48))

                                            agent_y.color = 'yellow'
                                            agent_y.repeat = True
                                            areas_record_dict[agent_y.current_location] += 1

                                    elif agent_x.mask == True and agent_y.mask == True:
                                        if random.random() <= infected_prob4:
                                            agent_y.exposed = True
                                            agent_y.exposed_total_time = int(np.round(np.random.normal(3, 1)*48))

                                            agent_y.color = 'yellow'
                                            agent_y.repeat = True
                                            areas_record_dict[agent_y.current_location] += 1


                        elif agent_x.current_location != 'home':

                            if agent_y.current_location == 'home':
                                continue

                            dist_xy = sum((np.array(agent_x.current_coordinate) - np.array(agent_y.current_coordinate)) ** 2)

                            if agent_x.current_location == agent_y.current_location:

                                # dist_xy = sum((np.array(agent_x.current_coordinate) - np.array(agent_y.current_coordinate))**2)

                                if dist_xy <= 2:

                                    agent_y.infected_people_met.append(agent_x.unique_id)

                                    if agent_x.mask == False and agent_y.mask == False:  # 其实这里可以用字典，使用键值组合来提取概率情况
                                        if random.random() <= infected_prob1:
                                            agent_y.exposed = True
                                            agent_y.exposed_total_time = int(np.round(np.random.normal(3, 1)*48))

                                            agent_y.color = 'yellow'
                                            agent_y.repeat = True
                                            areas_record_dict[agent_y.current_location] += 1

                                    elif agent_x.mask == True and agent_y.mask == False:
                                        if random.random() <= infected_prob2:
                                            agent_y.exposed = True
                                            agent_y.exposed_total_time = int(np.round(np.random.normal(3, 1)*48))

                                            agent_y.color = 'yellow'
                                            agent_y.repeat = True
                                            areas_record_dict[agent_y.current_location] += 1

                                    elif agent_x.mask == False and agent_y.mask == True:
                                        if random.random() <= infected_prob3:
                                            agent_y.exposed = True
                                            agent_y.exposed_total_time = int(np.round(np.random.normal(3, 1)*48))

                                            agent_y.color = 'yellow'
                                            agent_y.repeat = True
                                            areas_record_dict[agent_y.current_location] += 1

                                    elif agent_x.mask == True and agent_y.mask == True:
                                        if random.random() <= infected_prob4:
                                            agent_y.exposed = True
                                            agent_y.exposed_total_time = int(np.round(np.random.normal(3, 1)*48))

                                            agent_y.color = 'yellow'
                                            agent_y.repeat = True
                                            areas_record_dict[agent_y.current_location] += 1

        with open('Results/areas_record.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            row_data = [areas_record_dict[key] for key in areas_record_dict]
            writer.writerow(row_data)

    def repeat_initialize(self):
        for agent in self.schedule.agents:
            if isinstance(agent, MovingAgent):
                agent.repeat = False

    def state_transfer(self):

        for agent in self.schedule.agents:
            if isinstance(agent, MovingAgent):

                if agent.exposed:
                    agent.time_exposed += 1
                    if agent.time_exposed >= agent.exposed_total_time:  # lognorm.pdf(agent.time_exposed/48, 0.5, scale=5):
                        agent.exposed = False
                        agent.infected = True
                        agent.infected_total_time = int(np.round(np.random.normal(5, 1)*48))

                        agent.color = 'red'

                        if random.random() <= agent.severe_prob:
                            agent.severe = True
                            agent.severe_total_time = int(np.round(np.random.normal(5, 1)*48))

                if agent.infected:
                    agent.time_infected += 1

                    if agent.severe:
                        agent.time_severe += 1
                        if agent.time_severe >= agent.severe_total_time:
                            agent.severe = False
                        # if random.random() <= 0.001:
                        #     agent.severe = False

                    else:
                        if (agent.time_infected - agent.time_severe) >= agent.infected_total_time:
                            agent.infected = False
                            agent.recovered = True
                            agent.color = 'grey'


    def get_next_day_routines(self):
        # 获取所有智能体下一天的时间目的地规划

        global lockdown

        if self.schedule.steps % 48 == 0:

            self.days += 1
            self.weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][self.days % 7]
            print(self.weekday)
            print('infecting rate', infecting_number / agent_number)

            sum_met = 0

            for agent in self.schedule.agents:
                if isinstance(agent, MovingAgent):
                    sum_met += agent.met

            print(sum_met/agent_number)

            for agent in self.schedule.agents:

                if isinstance(agent, MovingAgent):

                    agent.infected_met = len(list(set(agent.infected_people_met)))

                    if agent.infected_met != 0:
                        agent.know = True
                        agent.knowtime = 0
                    else:
                        agent.knowtime += 1

                    if agent.knowtime == 7:
                        agent.know = False
                        agent.knowtime = 0

                    if agent.tohospital:
                        if random.random() <= 0.5:
                            agent.severe = False
                        agent.tohospital = False

                    if random.random() <= agent.illness_prob:
                        agent.other_illness = True

                    # if infecting_number/agent_number >= 0.02:  # 设置封控 当症状率大于0.02时开始封控
                    #     lockdown = True
                    # elif infecting_number/agent_number == 0:  # 直到症状率为0
                    #     lockdown = False

                    message = message_select(infecting_number, agent_number, agent.infected, agent.time_infected, agent.recovered,
                                             agent.career, agent.work_place, agent.characteristics, self.weekday, agent.unique_id, agent.know,
                                             agent.infected_met, agent.other_illness, agent.severe, lockdown)

                    agent.LLM_response = get_response(message)

                    print(agent.unique_id, f'mask:{agent.LLM_response[1]}', agent.LLM_response[0], 'lockdown:', lockdown)
                    agent.today_time_table = get_time(agent.LLM_response[0])
                    agent.today_candidate_destinations = get_destination(agent.LLM_response[0])
                    agent.mask = agent.LLM_response[1]
                    agent.destinations_reached_number = 0



                    if 'hospital' in agent.today_candidate_destinations:
                        agent.tohospital = True
                    else:
                        agent.tohospital = False

                    agent.infected_met = 0
                    agent.met = 0

                    agent.other_illness = False

                    time.sleep(0.1)

            time.sleep(1)


    def results_record(self):

        if self.schedule.steps % 48 == 0:

            global expo_infe_number, infecting_number, infected_number, severe_number, recovered_number

            expo_infe_number = 0  # 当前感染传染病的人数，包括潜伏期和症状期
            infecting_number = 0  # 当前处于有症状感染的人数
            infected_number = 0  # 累计感染人数
            severe_number = 0  # 当前重症人数
            recovered_number = 0  # 累计康复人数

            exposed_ids = []
            infected_ids = []
            severe_ids = []
            recovered_ids = []

            exposed_times = []
            infected_times = []
            severe_times = []

            for agent in self.schedule.agents:
                if isinstance(agent, MovingAgent):

                    if agent.exposed:
                        expo_infe_number += 1
                        exposed_ids.append(1)
                    else:
                        exposed_ids.append(0)

                    if agent.infected:
                        infecting_number += 1
                        expo_infe_number += 1

                        infected_ids.append(1)
                    else:
                        infected_ids.append(0)

                    if agent.recovered:
                        recovered_number += 1
                        recovered_ids.append(1)
                    else:
                        recovered_ids.append(0)

                    if agent.exposed or agent.infected or agent.recovered:
                        infected_number += 1

                    if agent.severe:
                        severe_number += 1
                        severe_ids.append(1)
                    else:
                        severe_ids.append(0)

                    exposed_times.append(agent.time_exposed)
                    infected_times.append(agent.time_infected)
                    severe_times.append(agent.time_severe)

                    response_path = "Agents/Agent{}_Response.txt".format(agent.unique_id)
                    with open(response_path, mode='a', encoding='utf-8') as file1:
                        file1.write(str(agent.LLM_response) + "\n")


            with open("Results/expo_infe_number.txt", 'a') as f:
                f.write(f"{expo_infe_number}\n")

            with open("Results/infecting_number.txt", 'a') as f:
                f.write(f"{infecting_number}\n")

            with open("Results/recovered_number.txt", 'a') as f:
                f.write(f"{recovered_number}\n")

            with open("Results/infected_number.txt", 'a') as f:
                f.write(f"{infected_number}\n")

            with open("Results/severe_number.txt", 'a') as f:
                f.write(f"{severe_number}\n")

            for file_name, dataset in zip(['exposed_ids', 'infected_ids', 'recovered_ids', 'severe_ids', 'exposed_times', 'infected_times', 'severe_times'],
                                          [exposed_ids, infected_ids, recovered_ids, severe_ids, exposed_times, infected_times, severe_times]):
                with open("Results/{}.csv".format(file_name), mode='a', newline='') as file:
                    writer = csv.writer(file)
                    #for _ in range(agent_number):
                    row_data = [i for i in dataset]
                    writer.writerow(row_data)


def agent_portrayal(agent):
    if isinstance(agent, WallAgent):
        if agent.wall_type == 1:
            portrayal = {"Shape": "rect",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "orange",
                         "w": 1,
                         "h": 1}
        else:
            portrayal = {"Shape": "rect",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "white",
                         "w": 1,
                         "h": 1}
    elif isinstance(agent, MovingAgent):
        portrayal = {"Shape": "circle",
                     "Filled": ("{}".format(agent.mask)).lower(),
                     "Layer": 1,
                     "Color": agent.color,
                     "r": 0.5}
    elif isinstance(agent, TextAgent):
        portrayal = {
            "Shape": "rect",
            "Color": "white",  # Make the rectangle invisible
            "Filled": "true",
            "Layer": 1,
            "w": 1,
            "h": 1,
            "text": agent.text,
            "text_color": agent.text_color
        }

    return portrayal


def map_portrayal(wall):
    if wall == 1:
        return {"Shape": "rect", "w": 1, "h": 1, "Color": "black", "Filled": "true", "Layer": 0}
    else:
        return {"Shape": "rect", "w": 1, "h": 1, "Color": "white", "Filled": "true", "Layer": 0}


grid = CanvasGrid(agent_portrayal, 150, 120, 1500, 1200)

model_params = {
    "width": 150,
    "height": 120,
    "city_map": matrix
}

server = ModularServer(SEIRModel, [grid], "SEIR Model", model_params)
server.port = 8521
server.launch()


