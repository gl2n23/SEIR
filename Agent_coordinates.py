import random

random.seed(37)


agent_counts = [70, 70, 10, 150, 75, 25, 50, 50]
occupations = ['primary school student', 'high school student', 'medical worker', 'office worker', 'commercial area worker', 'entertainment area worker', 'old person', 'unemployed person']

def assign_traits(occupation):
    if occupation in ['primary school student', 'high school student']:
        return {
            'accept_change': random.choices([True, False], weights=[0.7, 0.3])[0],
            'dislike_masks': random.choices([True, False], weights=[0.6, 0.4])[0],
            'care_others': random.choices([True, False], weights=[0.6, 0.4])[0]
        }
    elif occupation == 'old person':
        return {
            'accept_change': random.choices([True, False], weights=[0.3, 0.7])[0],
            'dislike_masks': random.choices([True, False], weights=[0.4, 0.6])[0],
            'care_others': random.choices([True, False], weights=[0.7, 0.3])[0]
        }
    elif occupation == 'medical worker':
        return{
            'accept_change': True,
            'dislike_masks': False,
            'care_others': True
        }
    else:  # Adults
        return {
            'accept_change': random.choices([True, False], weights=[0.5, 0.5])[0],
            'dislike_masks': random.choices([True, False], weights=[0.5, 0.5])[0],
            'care_others': random.choices([True, False], weights=[0.5, 0.5])[0]
        }


agents = []
agent_id = 0
for count, occupation in zip(agent_counts, occupations):
    for _ in range(count):
        traits = assign_traits(occupation)
        agent = {
            'id': agent_id,
            'occupation': occupation,
            **traits
        }
        agents.append(agent)
        agent_id += 1


original_agents = agents.copy()


random.shuffle(agents)

# Define a function to distribute agents into families with constraints
def distribute_agents_to_families(agents, max_family_size=5):
    families = []
    family_ids = [None] * len(agents)  # To keep track of family assignments
    family_counter = 0

    while agents:
        family_size = random.randint(2, max_family_size)  # Ensure at least 2 members per family for constraints to apply
        family = []
        children_count = 0
        old_people_count = 0

        while family_size > 0 and agents:
            for i, agent in enumerate(agents):
                if 'student' in agent['occupation'] and children_count < 3:
                    family.append(agent)
                    children_count += 1
                    family_ids[agent['id']] = family_counter  # Assign family ID
                    agents.pop(i)
                    family_size -= 1
                    break
                elif agent['occupation'] == 'old person' and old_people_count < 2:
                    family.append(agent)
                    old_people_count += 1
                    family_ids[agent['id']] = family_counter  # Assign family ID
                    agents.pop(i)
                    family_size -= 1
                    break
                elif 'student' not in agent['occupation'] and agent['occupation'] != 'old person':
                    family.append(agent)
                    family_ids[agent['id']] = family_counter  # Assign family ID
                    agents.pop(i)
                    family_size -= 1
                    break

        # If there are still slots left in the family, fill with any available agents
        while family_size > 0 and agents:
            agent = agents.pop(0)
            family.append(agent)
            family_ids[agent['id']] = family_counter  # Assign family ID
            family_size -= 1

        families.append(family)
        family_counter += 1

    return families, family_ids

# Distribute the agents into families
families, family_ids = distribute_agents_to_families(agents)

# Prepare the output lists in the original order
occupations_list = [agent['occupation'] for agent in original_agents]
accept_change_list = [agent['accept_change'] for agent in original_agents]
dislike_masks_list = [agent['dislike_masks'] for agent in original_agents]
care_others_list = [agent['care_others'] for agent in original_agents]
ordered_family_ids = [family_ids[agent['id']] for agent in original_agents]


class family:

    def __init__(self, zuobiao, id):
        self.zuobiao = zuobiao
        self.id = id
        self.number = 0
        self.candidates = []



a = 1
b = 1
families = []
c = 0

for b in range(9):
    for a in range(37):

        zuobiao0 = (a*4+1, b*4+1)
        id0 = c
        c += 1

        families.append(family(zuobiao0, id0))

for uniquefamily in families:
    for b1 in range(uniquefamily.zuobiao[1], uniquefamily.zuobiao[1] + 2):
        for a1 in range(uniquefamily.zuobiao[0], uniquefamily.zuobiao[0] + 3):
            uniquefamily.candidates.append((a1, b1))


coordinates = []

# number_record = []

for i in range(len(ordered_family_ids)):
    for j in families:
        if j.id == ordered_family_ids[i]:
            coordinates.append(j.candidates[j.number])
            j.number += 1



if __name__ == '__main__':

    # Display the results
    print("Family IDs:", ordered_family_ids)
    #print("Occupations:", occupations_list)
    #print("Accept Change:", accept_change_list)
    #print("Dislike Masks:", dislike_masks_list)
    #print("Dislike Hospitals:", dislike_hospitals_list)
    print(max(ordered_family_ids))
    print(coordinates)
    print(len(ordered_family_ids))
    print(len(coordinates))
#    print(number_record)
#    print(len(number_record))

    for z in families:
        if z.id == 0:
            print(z.candidates)

    for z in range(len(ordered_family_ids)):
        if ordered_family_ids[z] == 0:
            print(z)
            print(coordinates[z])