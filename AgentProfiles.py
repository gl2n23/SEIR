
careers = []

work_places = []

list1 = [70, 70, 10, 150, 75, 25, 50, 50]

list2 = ['primary school student', 'high school student', 'medical worker', 'office worker', 'commercial area worker', 'entertainment area worker', 'old person', 'unemployed person']


for number, name in zip(list1, list2):
    for i in range(1, number+1):
        careers.append(name)


list3 = [70, 70, 10, 50, 25, 30, 45, 50, 25, 15, 10, 100]

list4 = ['primary school', 'high school', 'hospital', 'office area 1', 'office area 2', 'office area 3', 'office area 4',
         'commercial area 1', 'commercial area 2', 'entertainment area 1', 'entertainment area 2', 'not certain destination']


for number, name in zip(list3, list4):
    for i in range(1, number+1):
        work_places.append(name)

home_locations = []


n = 1

for i in range(2, 25):
    for j in range(2, 148):
        if n > 500:
            break
        home_locations.append((j,i))
        n += 1



