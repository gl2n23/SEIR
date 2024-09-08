
def past_schedules(agent_id):
    file_path = "Agents/Agent{}_Response.txt".format(agent_id)
    with open(file_path, 'r') as file:
        lines1 = file.readlines()[-7:]
    lines2 = [line.strip() for line in lines1]
    return lines2


def dict_combine(system_content, user_content, agent_id,
                 career, work_place, characteristics, weekday, infected_met=0):

    weekdays = {'Monday': ['Last Monday', 'Last Tuesday', 'Last Wednesday', 'Last Thursday', 'Last Friday', 'Last Saturday', 'Last Sunday'],
                'Tuesday': ['Last Tuesday', 'Last Wednesday', 'Last Thursday', 'Last Friday', 'Last Saturday', 'Last Sunday', 'Last Monday'],
                'Wednesday': ['Last Wednesday', 'Last Thursday', 'Last Friday', 'Last Saturday', 'Last Sunday', 'Last Monday', 'Last Tuesday'],
                'Thursday': ['Last Thursday', 'Last Friday', 'Last Saturday', 'Last Sunday', 'Last Monday', 'Last Tuesday', 'Last Wednesday'],
                'Friday': ['Last Friday', 'Last Saturday', 'Last Sunday', 'Last Monday', 'Last Tuesday', 'Last Wednesday', 'Last Thursday'],
                'Saturday': ['Last Saturday', 'Last Sunday', 'Last Monday', 'Last Tuesday', 'Last Wednesday', 'Last Thursday', 'Last Friday'],
                'Sunday': ['Last Sunday', 'Last Monday', 'Last Tuesday', 'Last Wednesday', 'Last Thursday', 'Last Friday', 'Last Saturday']}

    pasts = past_schedules(agent_id)
    weekday_schedule = {}


    days = weekdays[weekday][7-len(pasts):]

    for x, y in zip(days, pasts):
        weekday_schedule[x] = y

    str_weekday_schedule = str(weekday_schedule)

    dict1 = {"role": "system", "content": system_content.format(career, work_place, characteristics, str_weekday_schedule)}
    dict2 = {"role": "user", "content": user_content.format(weekday, infected_met)}
    list1 = [dict1, dict2]
    return list1

def message_select(infecting_number, agent_number, infected, infected_time, recovered,
                   career, work_place, characteristics, weekday, agent_id, know,
                   infected_met=0, other_illness=False, severe=False, lockdown=False):

    if not lockdown:

        if infecting_number/agent_number > 1: # < 0.1:
            if infected:  # 染病状态 没有考虑同时得传染病和其他疾病的情况
                if severe:
                    message = dict_combine(system_content1, user_content3, agent_id, career, work_place, characteristics, weekday)
                else:
                    if infected_time >= 96:
                        message = dict_combine(system_content1, user_content2, agent_id, career, work_place, characteristics, weekday)
                    else:
                        message = dict_combine(system_content1, user_content1, agent_id, career, work_place, characteristics, weekday)

            elif recovered:  # 康复状态
                if other_illness:
                    message = dict_combine(system_content1, user_content4, agent_id, career, work_place, characteristics, weekday)
                else:
                    message = dict_combine(system_content1, user_content5, agent_id, career, work_place, characteristics, weekday)

            else:  # 易感状态和潜伏状态
                if infected_met == 0:
                    if other_illness:
                        message = dict_combine(system_content1, user_content6, agent_id, career, work_place, characteristics, weekday)
                    else:
                        message = dict_combine(system_content1, user_content7, agent_id, career, work_place, characteristics, weekday)

                else:
                    if other_illness:
                        message = dict_combine(system_content1, user_content8, agent_id, career, work_place, characteristics, weekday, infected_met)
                    else:
                        message = dict_combine(system_content1, user_content9, agent_id, career, work_place, characteristics, weekday, infected_met)

        else:
            if infected:  # 染病状态
                if severe:
                    message = dict_combine(system_content1, user_content21, agent_id, career, work_place,
                                           characteristics, weekday)
                else:
                    if infected_time >= 96:
                        message = dict_combine(system_content1, user_content20, agent_id, career, work_place,
                                               characteristics, weekday)
                    else:
                        message = dict_combine(system_content1, user_content19, agent_id, career, work_place,
                                               characteristics, weekday)

            elif recovered:  # 康复状态
                if other_illness:
                    message = dict_combine(system_content1, user_content22, agent_id, career, work_place,
                                           characteristics, weekday)

                else:
                    message = dict_combine(system_content1, user_content23, agent_id, career, work_place,
                                           characteristics, weekday)

            else:  # 易感状态和潜伏状态
                if know:
                    if infected_met == 0:
                        if other_illness:
                            message = dict_combine(system_content1, user_content24, agent_id, career, work_place,
                                                   characteristics, weekday)

                        else:
                            message = dict_combine(system_content1, user_content25, agent_id, career, work_place,
                                                   characteristics, weekday)
                    else:
                        if other_illness:
                            message = dict_combine(system_content1, user_content26, agent_id, career, work_place,
                                                   characteristics, weekday, infected_met)

                        else:
                            message = dict_combine(system_content1, user_content27, agent_id, career, work_place,
                                                   characteristics, weekday, infected_met)

                else:
                    if other_illness:
                        message = dict_combine(system_content1, user_content28, agent_id, career, work_place,
                                               characteristics, weekday, infected_met)

                    else:
                        message = dict_combine(system_content1, user_content29, agent_id, career, work_place,
                                               characteristics, weekday, infected_met)

    else:  # 执行封控
        if infected:  # 染病状态
            if severe:
                message = dict_combine(system_content1, user_content12, agent_id, career, work_place,characteristics, weekday)
            else:
                if infected_time >= 96:
                    message = dict_combine(system_content1, user_content11, agent_id, career, work_place,characteristics, weekday)
                else:
                    message = dict_combine(system_content1, user_content10, agent_id, career, work_place,characteristics, weekday)

        elif recovered:  # 康复状态
            if other_illness:
                message = dict_combine(system_content1, user_content13, agent_id, career, work_place,characteristics, weekday)

            else:
                message = dict_combine(system_content1, user_content14, agent_id, career, work_place,characteristics, weekday)

        else:  # 易感状态和潜伏状态
            if infected_met == 0:
                if other_illness:
                    message = dict_combine(system_content1, user_content15, agent_id, career, work_place,characteristics, weekday)
                else:
                    message = dict_combine(system_content1, user_content16, agent_id, career, work_place,characteristics, weekday)

            else:
                if other_illness:
                    message = dict_combine(system_content1, user_content17, agent_id, career, work_place,characteristics, weekday, infected_met)
                else:
                    message = dict_combine(system_content1, user_content18, agent_id, career, work_place,characteristics, weekday, infected_met)

    return message


system_dict = {
    "role": "system",
    "content": "There is a society with the following main areas: office area 1, office area 2, office area 3, office area 4, commercial area 1, commercial area 2, entertainment area 1, entertainment area 2, high school, primary school, park, home." +
               "Here are descriptions of these areas:" +
               "Office area 1 is an office area where employees mainly engage in technical work, with working hours usually from 09:00 to 17:00." +
               "Office area 2 is an office area primarily for financial companies and banks with working hours typically from 08:00 to 18:00." +
               "Office area 3 is an office area which is home to creative companies and startups where employees have flexible working hours." +
               "Office area 4 is an office area for traditional manufacturing companies where employees usually work from 08:00 to 17:00." +
               "Commercial area 1 is a commercial area which includes shopping malls, supermarkets and restaurants." +
               "Commercial area 2 is a commercial area which primarily consists of whole sale markets and large warehouses. " +
               "Entertainment area 1 is an entertainment district with cinemas, karaoke bars, pubs and nightclubs." +
               "Entertainment area 2 is an entertainment district focusing on multiple people entertainment including amusement parks, children's activity centers, and trendy restaurants." +
               "High school is a learning place for high school students." +
               "Primary school is where pupils attend classes." +
               "Hospital is a place for treating illnesses. There is no need to come here for people who are not sick." +
               "Park is a large open space designed for residents to enjoy leisure and exercise. The park features lawns, flower beds, paths, a children's playground, fitness equipment areas, and a small lake." +
               f"In this society, you are a {1} whose daily working destination is {2}. And you are a person who values freedom. At normal times there is no need to wear a mask." +
               f"You are a person with these characteristics {3}" +
               "Your output can only and just need to be a Python dictionary composed of a sub-dictionary. The dictionary format is as the following:" +
               "{'mask': bool, 'schedule': {'time': 'destination',...}}, " +
               "where the value for bool can only be True or False, " +
               "time format can only be digital form like 09:30 and only include whole hours with half hours or whole hours, " +
               "and values for 'destination' in the sub-dict can only be selected from the following names: office area 1, office area 2, office area 3, office area 4, commercial area 1, commercial area 2, entertainment area 1, entertainment area 2, high school, primary school, park, home. " +
               "The first key-value pair in the dictionary is to describe whether you will wear a mask, the second key-subdict pair in the dictionary is to describe your schedule today."
}

user_dict = {
    "role": "user",
    "content": f"Today is {1}. You feel you have been infected by an epidemic last day and can barely manage to do daily activities. " +
               "Now due to impact of epidemic, the government advise everyone to wear masks and gather less. " +
               "Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon." +
               f"This is your action destinations at last day {2}" +  # 注意这句是否需要删掉，有可能影响第一天的输出
               "Do not give any additional descriptions, just return the dict."
}

system_content1 = '''
There is a society with the following main areas: office area 1, office area 2, office area 3, office area 4, commercial area 1, commercial area 2, entertainment area 1, entertainment area 2, high school, primary school, park, home. +
Here are descriptions of these areas:
Office area 1 is an office area where employees mainly engage in technical work, with working hours usually from 09:00 to 17:00.
Office area 2 is an office area primarily for financial companies and banks with working hours typically from 08:00 to 18:00.
Office area 3 is an office area which is home to creative companies and startups where employees have flexible working hours.
Office area 4 is an office area for traditional manufacturing companies where employees usually work from 08:00 to 17:00.
Commercial area 1 is a commercial area which includes shopping malls, supermarkets and restaurants.
Commercial area 2 is a commercial area which primarily consists of whole sale markets and large warehouses.
Entertainment area 1 is an entertainment district with cinemas, karaoke bars, pubs and nightclubs.
Entertainment area 2 is an entertainment district focusing on multiple people entertainment including amusement parks, children's activity centers, and trendy restaurants.
High school is a learning place for high school students.
Primary school is where pupils attend classes.
Hospital is a place for treating illnesses. There is no need to come here for people who are not sick.
Park is a large open space designed for residents to enjoy leisure and exercise. The park features lawns, flower beds, paths, a children's playground, fitness equipment areas, and a small lake.
You are a resident in this society and you are a {} whose daily working destination is {}. At normal times there is no need to wear a mask.
You are a person with these personality characteristics {}.
In this society, Monday, Tuesday, Wednesday, Thursday, Friday are workdays, while Saturday and Sunday are rest days.
At work days, people usually work at white day and can go out for eating, go out for entertainment, go shopping, take a walk at park, rest at home, or do any other relaxing things after they finish today's work.
Most residents do not need to work on Saturday and Sunday, especially primary and high school students. Some workers might need to work overtime on Saturday and Sunday, but the chances are very low.
At rest days, people can go out for eating, go out for entertainment, go shopping, have fun in the park, rest at home, or do any other relaxing things.
Your output can only and just need to be a Python dictionary composed of a sub-dictionary. The dictionary format is as the following:
{{'mask': bool, 'schedule': {{'time': 'destination',...}}}},
where the value for bool can only be True or False,
time format can only be digital form like 09:30 and only include whole hours with half hours or whole hours,
and values for 'destination' in the sub-dict can only be selected from the following names: office area 1, office area 2, office area 3, office area 4, commercial area 1, commercial area 2, entertainment area 1, entertainment area 2, high school, primary school, park, hospital, home.
The first key-value pair in the dictionary is to describe whether you will wear a mask, the second key-subdict pair in the dictionary is to describe your schedule today
These are your schedules you have finished over the past few days: 
{}
'''

system_content2 = '''
There is a society with the following main areas: office area 1, office area 2, office area 3, office area 4, commercial area 1, commercial area 2, entertainment area 1, entertainment area 2, high school, primary school, park, home. +
Here are descriptions of these areas:
Office area 1 is an office area where employees mainly engage in technical work, with working hours usually from 09:00 to 17:00.
Office area 2 is an office area primarily for financial companies and banks with working hours typically from 08:00 to 18:00.
Office area 3 is an office area which is home to creative companies and startups where employees have flexible working hours.
Office area 4 is an office area for traditional manufacturing companies where employees usually work from 08:00 to 17:00.
Commercial area 1 is a commercial area which includes shopping malls, supermarkets and restaurants.
Commercial area 2 is a commercial area which primarily consists of whole sale markets and large warehouses.
Entertainment area 1 is an entertainment district with cinemas, karaoke bars, pubs and nightclubs.
Entertainment area 2 is an entertainment district focusing on multiple people entertainment including amusement parks, children's activity centers, and trendy restaurants.
High school is a learning place for high school students.
Primary school is where pupils attend classes.
Hospital is a place for treating illnesses. There is no need to come here for people who are not sick.
Park is a large open space designed for residents to enjoy leisure and exercise. The park features lawns, flower beds, paths, a children's playground, fitness equipment areas, and a small lake.
You are a resident in this society and you are a {} whose daily working destination is {}. At normal times there is no need to wear a mask.
You are a person with these characteristics {}.
Your output can only and just need to be a Python dictionary composed of a sub-dictionary. The dictionary format is as the following:
{'mask': bool, 'schedule': {'time': 'destination',...}},
where the value for bool can only be True or False,
time format can only be digital form like 09:30 and only include whole hours with half hours or whole hours,
and values for 'destination' in the sub-dict can only be selected from the following names: office area 1, office area 2, office area 3, office area 4, commercial area 1, commercial area 2, entertainment area 1, entertainment area 2, high school, primary school, park, hospital, home.
The first key-value pair in the dictionary is to describe whether you will wear a mask, the second key-subdict pair in the dictionary is to describe your schedule today
These are your schedules you have finished over the past few days: 
{}
'''

#注意是否要加上very low




# 政府建议
# 刚被感染 轻症
user_content1 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You feel you have been infected by the contagious disease and can barely manage to do daily activities.
Now due to impact of the contagious disease, the government advise everyone to wear masks and gather less.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time when you are at home.
Do not give any additional descriptions, just return the dict.
'''

# 被感染几天后 轻症
user_content2 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have been infected by the contagious disease several days ago. You have not been fully recovered but able to do daily activities. 
Now due to impact of the contagious disease, the government advise everyone to wear masks and gather less.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time when you are at home.
Do not give any additional descriptions, just return the dict.
'''

# 被感染 重症
user_content3 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You feel you have been infected by the contagious disease and feel very unwell.
You fell you should go to the hospital to get treated. This will take approximately five hours.
Now due to impact of the contagious disease, the government advise everyone to wear masks and gather less.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time when you are at home.
Do not give any additional descriptions, just return the dict.
'''

# 已经康复 但得了其他病
user_content4 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have already get recovered from the contagious disease and will not be infected again.
But you have come down with another illness, it is best to go to the hospital today to get treated. This will take approximately one hour. 
Now due to impact of the contagious disease, the government advise everyone to wear masks and gather less.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time when you are at home.
Do not give any additional descriptions, just return the dict.
'''

# 已经康复
user_content5 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have already get recovered from the contagious disease and will not be infected again.
Now due to impact of the contagious disease, the government advise everyone to wear masks and gather less.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time when you are at home.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 没有遇见传染病患者 得了其他病
user_content6 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have come down with an another illness, it is best to go to the hospital today to get treated. This will take approximately one hour. 
Now due to impact of the contagious disease, the government advise everyone to wear masks and gather less.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time when you are at home.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 没有遇见传染病患者
user_content7 = '''
Today is {}.
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
Now due to the impact of the contagious disease, the government advise everyone to wear masks and gather less.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time when you are at home.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 遇见了传染病患者 得了其他病
user_content8 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
At last day, you have met {} people who look like being infected by a contagious disease.
You have come down with an another illness, it is best to go to the hospital today to get treated. This will take approximately one hour. 
Now due to impact of the contagious disease, the government advise everyone to wear masks and gather less.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time when you are at home.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 遇见了传染病患者
user_content9 = '''
Today is {}.
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
At last day, you have met {} people who look like being infected by a contagious disease.
Now due to the impact of the contagious disease, the government advise everyone to wear masks and gather less.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time when you are at home.
Do not give any additional descriptions, just return the dict.
'''


# 政府封控

# 刚被感染 轻症
user_content10 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You feel you have been infected by the contagious disease and can barely manage to do daily activities.
Now due to the severe impact of the contagious disease, the government has to implement lockdown measures. 
Except medical workers, other residents are not allowed to leave home for work or other activities at work days or rest days in normal situations due to the impact of the contagious disease. Now residents except medical workers should stay at home. Only if they have severe symptoms because of the contagious disease or significant symptoms because of other illnesses, should they go to the hospital. Medical workers have to go out for work.
The government will deliver essential supplies to every household to ensure that residents can maintain their normal lives.
Please provide your today's action schedules and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries.
Do not give any additional descriptions, just return the dict.
'''

# 被感染几天后 轻症
user_content11 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have been infected by the contagious disease several days ago. You have not been fully recovered but able to do daily activities. 
Now due to the severe impact of the contagious disease, the government has to implement lockdown measures. 
Except medical workers, other residents are not allowed to leave home for work or other activities at work days or rest days in normal situations due to the impact of the contagious disease. Now residents except medical workers should stay at home. Only if they have severe symptoms because of the contagious disease or significant symptoms because of other illnesses, should they go to the hospital. Medical workers have to go out for work.
The government will deliver essential supplies to every household to ensure that residents can maintain their normal lives.
Please provide your today's action schedules and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries.
Do not give any additional descriptions, just return the dict.
'''

# 被感染 重症
user_content12 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You feel you have been infected by the contagious disease and feel very unwell.
You fell you should go to the hospital to get treated. This will take approximately five hours.
Now due to the severe impact of the contagious disease, the government has to implement lockdown measures. 
Except medical workers, other residents are not allowed to leave home for work or other activities at work days or rest days in normal situations due to the impact of the contagious disease. Now residents except medical workers should stay at home. Only if they have severe symptoms because of the contagious disease or significant symptoms because of other illnesses, should they go to the hospital. Medical workers have to go out for work.
The government will deliver essential supplies to every household to ensure that residents can maintain their normal lives.
Please provide your today's action schedules and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries.
Do not give any additional descriptions, just return the dict.
'''

# 已经康复 但得了其他病
user_content13 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have already get recovered from the contagious disease and will not be infected again.
But you have come down with another illness, it is best to go to the hospital today to get treated. This will take approximately one hour. 
Now due to the severe impact of the contagious disease, the government has to implement lockdown measures. 
Except medical workers, other residents are not allowed to leave home for work or other activities at work days or rest days in normal situations due to the impact of the contagious disease. Now residents except medical workers should stay at home. Only if they have severe symptoms because of the contagious disease or significant symptoms because of other illnesses, should they go to the hospital. Medical workers have to go out for work.
The government will deliver essential supplies to every household to ensure that residents can maintain their normal lives.
Please provide your today's action schedules and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries.
Do not give any additional descriptions, just return the dict.
'''

# 已经康复
user_content14 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have already get recovered from the contagious disease and will not be infected again.
Now due to the severe impact of the contagious disease, the government has to implement lockdown measures. 
Except medical workers, other residents are not allowed to leave home for work or other activities at work days or rest days in normal situations due to the impact of the contagious disease. Now residents except medical workers should stay at home. Only if they have severe symptoms because of the contagious disease or significant symptoms because of other illnesses, should they go to the hospital. Medical workers have to go out for work.
The government will deliver essential supplies to every household to ensure that residents can maintain their normal lives.
Please provide your today's action schedules and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 没有遇见传染病患者 得了其他病
user_content15 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have come down with another illness, it is best to go to the hospital today to get treated. This will take approximately one hour. 
Now due to the severe impact of the contagious disease, the government has to implement lockdown measures. 
Except medical workers, other residents are not allowed to leave home for work or other activities at work days or rest days in normal situations due to the impact of the contagious disease. Now residents except medical workers should stay at home. Only if they have severe symptoms because of the contagious disease or significant symptoms because of other illnesses, should they go to the hospital. Medical workers have to go out for work.
The government will deliver essential supplies to every household to ensure that residents can maintain their normal lives.
Please provide your today's action schedules and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 没有遇见传染病患者
user_content16 = '''
Today is {}.
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
Now due to the severe impact of the contagious disease, the government has to implement lockdown measures. 
Except medical workers, other residents are not allowed to leave home for work or other activities at work days or rest days in normal situations due to the impact of the contagious disease. Now residents except medical workers should stay at home. Only if they have severe symptoms because of the contagious disease or significant symptoms because of other illnesses, should they go to the hospital. Medical workers have to go out for work.
The government will deliver essential supplies to every household to ensure that residents can maintain their normal lives.
Please provide your today's action schedules and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 遇见了传染病患者 得了其他病
user_content17 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
At last day, you have met {} people who look like being infected by the contagious disease.
You have come down with another illness, it is best to go to the hospital today to get treated. This will take approximately one hour. 
Now due to the severe impact of the contagious disease, the government has to implement lockdown measures. 
Except medical workers, other residents are not allowed to leave home for work or other activities at work days or rest days in normal situations due to the impact of the contagious disease. Now residents except medical workers should stay at home. Only if they have severe symptoms because of the contagious disease or significant symptoms because of other illnesses, should they go to the hospital. Medical workers have to go out for work.
The government will deliver essential supplies to every household to ensure that residents can maintain their normal lives.
Please provide your today's action schedules and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 遇见了传染病患者
user_content18 = '''
Today is {}.
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of this contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
At last day, you have met {} people who look like being infected by the contagious disease.
Now due to the severe impact of the contagious disease, the government has to implement lockdown measures. 
Except medical workers, other residents are not allowed to leave home for work or other activities at work days or rest days in normal situations due to the impact of the contagious disease. Now residents except medical workers should stay at home. Only if they have severe symptoms because of the contagious disease or significant symptoms because of other illnesses, should they go to the hospital. Medical workers have to go out for work.
The government will deliver essential supplies to every household to ensure that residents can maintain their normal lives.
Please provide your today's action schedules and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries.
Do not give any additional descriptions, just return the dict.
'''


#无政府措施

# 刚被感染 轻症
user_content19 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of the contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You feel you have been infected by the contagious disease and can barely manage to do daily activities.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon.
Do not give any additional descriptions, just return the dict.
'''

# 被感染几天后 轻症
user_content20 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of the contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have been infected by an the contagious disease several days ago. You have not been fully recovered but able to do daily activities. 
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon.
Do not give any additional descriptions, just return the dict.
'''

# 被感染 重症
user_content21 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of the contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You feel you have been infected by the contagious disease and feel very unwell.
You fell you should go to the hospital to get treated. This will take approximately five hours.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon.
Do not give any additional descriptions, just return the dict.
'''

# 已经康复 但得了其他病
user_content22 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of the contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have already get recovered from the contagious disease and will not be infected again.
But you have come down with another illness, it is best to go to the hospital today to get treated. This will take approximately one hour. 
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon.
Do not give any additional descriptions, just return the dict.
'''

# 已经康复
user_content23 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of the contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have already get recovered from the contagious disease and will not be infected again.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 没有遇见传染病患者 得了其他病 但是知道有这个病
user_content24 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of the contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
You have come down with an another illness, it is best to go to the hospital today to get treated. This will take approximately one hour. 
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 没有遇见传染病患者 但是知道有这个病
user_content25 = '''
Today is {}.
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of the contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 遇见了传染病患者 得了其他病
user_content26 = '''
Today is {}. 
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of the contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
At last day, you have met {} people who look like being infected by the contagious disease.
You have come down with an another illness, it is best to go to the hospital today to get treated. This will take approximately one hour. 
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 遇见了传染病患者
user_content27 = '''
Today is {}.
You have noticed that recently there has been a contagious disease in the society.
The fatality rate of the contagious disease is very low, but the symptoms typically make people feel unwell for several days after they appear.
At last day, you have met {} people who look like being infected by the contagious disease.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 没有遇见传染病患者 得了其他病
user_content28 = '''
Today is {}. 
You have come down with an illness, it is best to go to the hospital today to get treated. This will take approximately one hour. 
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon.
Do not give any additional descriptions, just return the dict.
'''

# 正常状态 没有遇见传染病患者
user_content29 = '''
Today is {}.
Please provide your today's action destinations and if you will wear a mask today in the format of a Python dictionary composed of two sub-dictionaries and remember to provide the time to go home at night or evening or afternoon.
Do not give any additional descriptions, just return the dict.
'''


