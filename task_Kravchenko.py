import datetime
import re
import math
import sys


def check_1_line():
    if dataset[0].isdigit():
        return int(dataset[0]), True
    else:
        print(f"{dataset[0]}")
        sys.exit()


def check_2_line():
    split_data = dataset[1].split(' ')
    if len(split_data[0]) != len(split_data[1]) or len(split_data[1]) != 5:
        print(f"{dataset[1]}")
        sys.exit()
    else:
        pass
    try:
        if datetime.datetime.strptime(split_data[0], "%H:%M") and datetime.datetime.strptime(split_data[1], "%H:%M"):
            return split_data[0], split_data[1], True
    except:
        print(f"{dataset[1]}")
        sys.exit()


def check_3_line():
    if dataset[2].isdigit():
        return int(dataset[2]), True
    else:
        print(f"{dataset[2]}")
        sys.exit()


def check_4_N_line(regex):
    generator_value = 0
    clear_data = dataset[3:]
    for line in clear_data:
        part_of_string = line.split(' ')
        m = re.compile(regex)
        if datetime.datetime.strptime(part_of_string[0], "%H:%M") and len(part_of_string[0]) == 5 and (
                part_of_string[1]) in ['1', '2', '3', '4'] and m.search(part_of_string[2]) is not None:
            yield generator_value + 1
        else:
            print(f"{line}")
            sys.exit()


def check_for_check_4_N_line(test3):
    counter = 0
    for gen_value in test3:
        if gen_value == 1:
            counter += 1
    if len(dataset[3:]) == counter:
        return True


def collect_time_list(pattern):
    time_list = list()
    clear_data = dataset[3:]
    for line in clear_data:
        match = re.search(pattern, line)
        if match:
            time_list.append(match.group(0))
    return time_list


def check_time_order():
    previous_time = None
    clear_data = dataset[3:]
    for i in range(len(clear_data)):
        parts_of_string = clear_data[i].split(' ')
        current_time = datetime.datetime.strptime(parts_of_string[0], "%H:%M").time()
        if previous_time and current_time <= previous_time and current_time.strftime("00:00"):
            print(f"{clear_data[i]}")
            sys.exit()
        previous_time = current_time
    return True


def validation_of_input_data_and_collect_data():
    n_table, test = check_1_line()
    time_start, time_end, test1 = check_2_line()
    money, test2 = check_3_line()
    test3 = check_4_N_line(regex=r"^[a-z0-9_\-]+$")
    test4 = check_for_check_4_N_line(test3)
    time_list = collect_time_list(pattern=r"\d{2}:\d{2}")
    test6 = check_time_order()
    if test == test1 and test1 == test2 and test2 == test4 and test4 == test6 and test6 is True:
        return int(n_table), time_start, time_end, int(money), list(time_list)


def action13(num_error, action, client_name):
    if num_error == 1:
        print(f"{action[0]} 1 {client_name}")
        print(f"{action[0]} 13 YouShallNotPass")
    elif num_error == 2:
        print(f"{action[0]} 1 {client_name}")
        print(f"{action[0]} 13 NotOpenYet")
    elif num_error == 3:
        print(f"{action[0]} 2 {client_name}")
        print(f"{action[0]} 13 ClientUnknown")
    elif num_error == 4:
        print(f"{action[0]} 2 {client_name} {action[3]}")
        print(f"{action[0]} 13 PlaceIsBusy")
    else:
        print(f"{action[0]} 3 {client_name}")
        print(f"{action[0]} 13 ICanWaitNoLonger!")


def action11(action, time_end, client_name, clients_in_club, waiting_clients, n_table, action_time,
             time_list, clients_at_table, time_on_table_start):
    if len(waiting_clients) >= n_table:
        clients_in_club.remove(client_name)
    last_value = time_list[-1]
    if time_end <= action_time or last_value == action[0]:
        for clients in sorted(clients_in_club):
            print(f"{time_end.strftime('%H:%M')} 11 {clients}")
        for client_name in clients_at_table:
            table_number = clients_at_table.get(client_name, None)
            time_on_table_start[table_number].append(time_end.strftime('%H:%M'))


def action12(action, clients_at_table, free_tables, waiting_clients, client_name, clients_in_club, time_on_table_start):
    table_number = clients_at_table.get(client_name, None)
    if table_number is not None:
        free_tables.append(table_number)
        clients_in_club.remove(client_name)
        time_on_table_start[table_number].append(action[0])
        if len(waiting_clients) > 0:
            next_client = waiting_clients.pop(0)
            free_tables.remove(table_number)
            clients_at_table[next_client] = table_number
            time_on_table_start[table_number].append(action[0])
            print(f"{action[0]} 12 {client_name} {table_number}")


def calculate_earnings(time_on_table_start, money):
    earnings_per_table = {}
    total_time_per_table = {}

    for table_num, time_values in time_on_table_start.items():
        total_time = 0
        earnings = 0
        for i in range(0, len(time_values) - 1, 2):
            session_start = time_values[i]
            session_end = time_values[i + 1]
            if len(session_start.split(':')) == 2:
                session_start_time = datetime.datetime.strptime(session_start, '%H:%M')
                session_end_time = datetime.datetime.strptime(session_end, '%H:%M')
            else:
                session_start_time = datetime.datetime.strptime(session_start, '%H:%M:%S').replace(second=0)
                session_end_time = datetime.datetime.strptime(session_end, '%H:%M:%S').replace(second=0)
            session_time = (session_end_time - session_start_time).total_seconds() / 60
            if session_time < 60:
                session_time = math.ceil(session_time)
            total_time += session_time

            hours = math.ceil(session_time / 60)
            earnings_per_session = money * hours
            earnings += earnings_per_session

        earnings_per_table[table_num] = round(earnings, 2)
        total_time_per_table[table_num] = int(total_time)

    results = []
    for table_num, earnings in earnings_per_table.items():
        total_time = total_time_per_table[table_num]
        total_time = datetime.timedelta(minutes=total_time)
        formatted_time = (datetime.datetime.min + total_time).strftime('%H:%M')
        results.append(f"{table_num} {earnings} {formatted_time}")

    return '\n'.join(results)


def internet_club_simulation(time_start, time_end):
    time_start = datetime.datetime.strptime(time_start, "%H:%M").time()
    time_end = datetime.datetime.strptime(time_end, "%H:%M").time()
    print(time_start.strftime('%H:%M'))
    waiting_clients = []
    clients_at_table = dict()
    free_tables = list(range(1, n_table + 1))
    time_on_table_start = {key: [] for key in free_tables}
    clear_data = dataset[3:]
    clients_in_club = list()

    for i in range(len(clear_data)):
        action = clear_data[i].split(' ')
        action_time = datetime.datetime.strptime(action[0], '%H:%M').time()
        client_name = str(action[2])

        if action[1] == '1':  # Client came
            if client_name in clients_in_club:
                action13(1, action, client_name)
            elif action_time < time_start or action_time >= time_end:
                action13(2, action, client_name)
            else:
                clients_in_club.append(client_name)
                print(f"{action[0]} 1 {client_name}")

        elif action[1] == '2':
            table_number = int(action[3])  # The client sat down at the table
            if client_name not in clients_in_club:
                action13(3, action, client_name)
            if table_number in clients_at_table.values() and clients_at_table.get(client_name, -1) != n_table:
                action13(4, action, client_name)
            if len(free_tables) > 0:
                if table_number in free_tables:
                    free_tables.remove(table_number)
                    clients_at_table[client_name] = table_number
                    time_on_table_start[table_number].append(action[0])
                    print(f"{action[0]} 2 {client_name} {table_number}")
            else:
                waiting_clients.append(client_name)

        elif action[1] == '3':  # The client is waiting
            if len(free_tables) > 0:
                action13(5, action, client_name)
            else:
                print(f"{action[0]} 3 {client_name}")
                action11(action, time_end, client_name, clients_in_club, waiting_clients, n_table, action_time,
                         time_list, clients_at_table, time_on_table_start)

        elif action[1] == '4':  # Client left
            if client_name not in clients_in_club:
                action13(3, action, client_name)
            else:
                print(f"{action[0]} 4 {client_name}")
                action12(action, clients_at_table, free_tables, waiting_clients, client_name, clients_in_club,
                         time_on_table_start)

        action11(action, time_end, client_name, clients_in_club, waiting_clients, n_table, action_time,
                 time_list, clients_at_table, time_on_table_start)
    results = calculate_earnings(time_on_table_start, money)
    print(time_end.strftime('%H:%M'))
    print(results)


if __name__ == '__main__':
    with open('test12.txt', "r") as data:
        dataset = [line.rstrip('\n') for line in data]
    n_table, time_start, time_end, money, time_list = validation_of_input_data_and_collect_data()
    internet_club_simulation(time_start, time_end)
