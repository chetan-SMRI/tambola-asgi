from Tambola import celery_app


@celery_app.task(bind=True)
def test_task(self):
    x = f"Task id is: {self.request}\n----------------------\nThis TASK worked\n-------------------------"
    return x

@celery_app.task(bind=True)
def run_game(args):
    #    _       _   _
    #   | |     (_) | |__    ___
    #   | |     | | | '_ \  / __|
    #   | |___  | | | |_) | \__ \
    #   |_____| |_| |_.__/  |___/    
    from game.models import TicketDailyData as ticket_daily_data
    from game.models import WhoWillWin as who_will_win
    from game.models import WinnerData, GameplayStatus, HalfSheet, FullSheet
    import json
    import time
    import random
    from game.models import Ticket, SetDivident, TicketLimit, SetGameDelay, BookTicket
    from collections import Iterable
    def flatten(lis):
        for item in lis:
            if isinstance(item, Iterable) and not isinstance(item, str):
                for x in flatten(item):
                    yield x
            else:
                yield item
    def show_sheets():

        def checkIfQueued(l):
            total = 0
            minimum = float('+inf')
            maximum = float('-inf')
            seen = set()
            for n in l:
                if n in seen:
                    return False
                seen.add(n)
                if n < minimum:
                    minimum = n
                if n > maximum:
                    maximum = n
                total += n
            if 2 * total != maximum * (maximum + 1) - minimum * (minimum - 1):
                return False
        
            return True
    
        def indices(lst, element):
            result = []
            offset = -1
            while True:
                try:
                    offset = lst.index(element, offset+1)
                except ValueError:
                    return result
                result.append(offset)

    
        fullsheet_list = []
        halfsheet_list = []
        username_list = []
        user_username_list = []
        ticket_id = []
        #Getting All Booked Ticket's Phone
        for ticket in BookTicket.objects.all().order_by('ticket__ticket_no'):
            username_list.append(ticket.username)
            ticket_id.append(ticket.ticket.ticket_no)
        
        #Removing Duplicate Combination Of Username
        for i in username_list:
            if i not in user_username_list:
                user_username_list.append(i)
        
        #Getting Fullsheet And Halfsheet
        for user in user_username_list:
            last_value = ticket_id[ len(username_list) - username_list[::-1].index(user) - 1]
            if username_list.count(user) == 6 and last_value % 6 == 0:
                lis = []
                for index in indices(username_list, user):
                    lis.append(ticket_id[index])
                if checkIfQueued(lis):
                    fullsheet_list.append(user)
            if username_list.count(user) == 3:
                lis = []
                for index in indices(username_list, user):
                    lis.append(ticket_id[index])
                if checkIfQueued(lis):
                    halfsheet_list.append(user)
        return {"halfsheet":halfsheet_list, "fullsheet":fullsheet_list}
    def HalfSheet():
        halfsheet_usernamed = json.loads(json.dumps(show_sheets()))['halfsheet']
        halfsheet_tickets = []
        for halfsheet_usernamess in halfsheet_usernamed:
            myArr = []
            for i in BookTicket.objects.filter(username=halfsheet_usernamess):
                myArr.append(str(i.ticket.ticket_no))
            res = str(myArr)[1:-1]
            res = res.replace("'", "")
            res = res.replace(",", "-")
            res = res.replace(" ", "")
            halfsheet_tickets.append(res)
        return halfsheet_tickets
    def FullSheet():
        fullsheet_usernamed = json.loads(json.dumps(show_sheets()))['fullsheet']
        fullsheet_tickets = []
        for fullsheet_usernamess in fullsheet_usernamed:
            myArr = []
            for i in BookTicket.objects.filter(username=fullsheet_usernamess):
                myArr.append(str(i.ticket.ticket_no))
            res = str(myArr)[1:-1]
            res = res.replace("'", "")
            res = res.replace(",", "-")
            res = res.replace(" ", "")
            fullsheet_tickets.append(res)
        return fullsheet_tickets

    #   __     __
    #   \ \   / /   __ _   _ __   ___
    #    \ \ / /   / _` | | '__| / __|
    #     \ V /   | (_| | | |    \__ \
    #      \_/     \__,_| |_|    |___/

    # Abbreviation GAN = Gone At Number
    divident_obj = SetDivident.objects.first()
    to_be_count_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                        27, 28,
                        29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
                        53, 54,
                        55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78,
                        79, 80,
                        81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
    counted_list = []
    third_full_house_winner = []
    second_full_house_winner = []
    full_house_winner = []
    first_line_winner = []
    second_line_winner = []
    third_line_winner = []
    quickfive_winner = []
    quickseven_winner = []
    star_winner = []
    corner_winner = []
    half_sheet_winner = []
    full_sheet_winner = []

    third_full_house_winner_GAN = None
    second_full_house_winner_GAN = None
    full_house_winner_GAN = None
    first_line_winner_GAN = None
    second_line_winner_GAN = None
    third_line_winner_GAN = None
    quickfive_winner_GAN = None
    quickseven_winner_GAN = None
    star_winner_GAN = None
    corner_winner_GAN = None
    half_sheet_winner_GAN = None
    full_sheet_winner_GAN = None
    
    #Setting game delay
    try:
        time_delay = SetGameDelay.objects.first().Delay
    except:
        delay_obj = SetGameDelay.objects.create(Delay=10)
        time_delay = delay_obj.Delay


    def save_win(tickets,achievement,last_called_no):
        for no in tickets:
            if achievement == 'half_sheet':
                WinnerData.objects.create(achievement=achievement,half_sheet=no , last_called_no=last_called_no)
            elif achievement == "full_sheet":
                WinnerData.objects.create(achievement=achievement,full_sheet=no , last_called_no=last_called_no)
            else:
                ticket = Ticket.objects.get(ticket_no=int(no))
                WinnerData.objects.create(ticket = ticket, achievement=achievement, last_called_no=last_called_no)
    #    ____
    #   |  _ \   _   _   _ __
    #   | |_) | | | | | | '_ \
    #   |  _ <  | |_| | | | | |
    #   |_| \_\  \__,_| |_| |_|

    try:
        ticket_daily_data.objects.first().ticket_digits="[]"
    except:
        ticket_daily_data.objects.create(ticket_digits="[]")
    WinnerData.objects.all().delete()
    match_fix_list = []
    if who_will_win.objects.all().count() > 0:
        number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                       27, 28,
                       29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
                       53, 54,
                       55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78,
                       79, 80,
                       81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
        qf_arr = []
        l1_arr = []
        l2_arr = []
        l3_arr = []
        star_arr = []
        h1_arr = []
        h2_arr = []
        for i in who_will_win.objects.all():
            j = Ticket.objects.get(ticket_no=str(i.winner_ticket.ticket_no)).ticket_digits
            td = json.loads(j)
            td = list(filter(lambda a: a != 0, td))
            if i.winner_type == "quick_five":
                line = [td[10],
                        td[4],
                        random.randint(1, 90),
                        td[7],
                        td[1],
                        td[8]
                        ]
                qf_arr.append(line)
            if i.winner_type == "line_1":
                line = [td[0],
                        td[1],
                        td[2],
                        td[3],
                        td[4]
                        ]
                l1_arr.append(line)
            if i.winner_type == "line_2":
                line = [td[5],
                        td[6],
                        td[7],
                        td[8],
                        td[9]
                        ]
                l2_arr.append(line)
            if i.winner_type == "line_3":
                line = [td[10],
                        td[11],
                        random.randint(1, 90),
                        td[12],
                        td[13],
                        td[14]
                        ]
                l3_arr.append(line)
            if i.winner_type == "star":
                starvalues = [
                    td[0],
                    td[4],
                    td[7],
                    td[10],
                    td[14],
                    random.randint(1, 90)
                ]
                star_arr.append(starvalues)
            if i.winner_type == "full_house":
                h1_arr = [
                    td[0],
                    td[1],
                    random.randint(1, 90),
                    td[2],
                    td[3],
                    td[4],
                    td[6],
                    td[7],
                    td[8],
                    td[9],
                    td[10],
                    td[11],
                    td[12],
                    td[13],
                    td[14]
                ]
            if i.winner_type == "second_full_house":
                h2_arr = [
                    td[0],
                    td[1],
                    random.randint(1, 90),
                    td[2],
                    td[3],
                    td[4],
                    td[6],
                    td[7],
                    td[8],
                    td[9],
                    td[10],
                    td[11],
                    td[12],
                    td[13],
                    td[14]
                ]
        random.shuffle(qf_arr)
        random.shuffle(l1_arr)
        random.shuffle(l2_arr)
        random.shuffle(l3_arr)
        random.shuffle(star_arr)
        random.shuffle(h1_arr)
        all_line_star_arr = [l1_arr, l2_arr, l3_arr, star_arr]
        all_line_star_arr = list(flatten(all_line_star_arr))
        random.shuffle(all_line_star_arr)
        if len(all_line_star_arr) < 24:
            for q in range(0, 24 - len(all_line_star_arr)):
                all_line_star_arr.append(random.randint(1, 90))
        if len(qf_arr) == 0:
            qf_arr.append(random.randint(1, 90))
            qf_arr.append(random.randint(1, 90))
            qf_arr.append(random.randint(1, 90))
            qf_arr.append(random.randint(1, 90))
            qf_arr.append(random.randint(1, 90))
        if len(h1_arr) == 0:
            h1_arr = [random.randint(1, 90), random.randint(1, 90), random.randint(1, 90), random.randint(1, 90),
                      random.randint(1, 90), random.randint(1, 90), random.randint(1, 90), random.randint(1, 90),
                      random.randint(1, 90), random.randint(1, 90), random.randint(1, 90), random.randint(1, 90),
                      random.randint(1, 90), random.randint(1, 90)]
        if len(h2_arr) == 0:
            h2_arr = [random.randint(1, 90), random.randint(1, 90), random.randint(1, 90), random.randint(1, 90),
                      random.randint(1, 90), random.randint(1, 90), random.randint(1, 90), random.randint(1, 90),
                      random.randint(1, 90), random.randint(1, 90), random.randint(1, 90), random.randint(1, 90),
                      random.randint(1, 90), random.randint(1, 90)]
        random.shuffle(all_line_star_arr)
        random.shuffle(all_line_star_arr)
        random.shuffle(all_line_star_arr)
        # print(all_line_star_arr)
        main_arr1 = list(flatten([qf_arr + all_line_star_arr]))
        # print(h1_arr)
        # print(main_arr1)
        for k in range(1, 21):
            main_arr1.append(random.randint(1, 90))
        house_arr = h1_arr + h2_arr
        # random.shuffle(house_arr)
        main_arr2 = main_arr1 + house_arr
        main_arr2 = list(flatten(main_arr2))
        # print(main_arr2)
        res = []
        for o in main_arr2:
            if o not in res:
                res.append(o)
        for w in res:
            number_list.remove(w)
        main_list = res + number_list
        # print(len(main_list))
        match_fix_list = main_list
    game_play = GameplayStatus.objects.all().last()
    game_play.game_started = True
    game_play.game_over = False
    game_play.save()
    quickfive_flag = False
    quickseven_flag = False
    star_flag = False
    corner_flag = False
    first_line_flag = False
    second_line_flag = False
    third_line_flag = False
    half_sheet_flag = False
    full_sheet_flag = False
    full_house_flag = 0
    for i in range(1, 90):
        selected_number = 1
        if match_fix_list:
            selected_number = match_fix_list[i]
            # print("Match is fixed")
        else:
            selected_number = random.choice(to_be_count_list)  # Choosing Random No.
            # print("Match is not fixed")
        counted_list.append(selected_number)
        ticket_data_obj = ticket_daily_data.objects.first()
        ticket_data_obj.ticket_digits = str(counted_list)
        ticket_data_obj.save()  # Inserting it to DB        
        print(counted_list)
        to_be_count_list.remove(selected_number)  # Removing No. From List For Avoiding Repetition

        #   __        __  _
        #   \ \      / / (_)  _ __    _ __     ___   _ __
        #    \ \ /\ / /  | | | '_ \  | '_ \   / _ \ | '__|
        #     \ V  V /   | | | | | | | | | | |  __/ | |
        #      \_/\_/    |_| |_| |_| |_| |_|  \___| |_|
        ticket_limit = TicketLimit.objects.all().last()
        if not ticket_limit:
            limit = 600
        else:
            limit = ticket_limit.limit_value
        for ticket in Ticket.objects.all()[:limit]:
            ticket_no = ticket.ticket_no
            ticket_digits = json.loads(ticket.ticket_digits)
            filtered_ticket = list(
                filter(lambda a: a != 0, ticket_digits))  # Removing Zeroes in Ticket Data For Winner Selecting Algo


            #    _____           _   _     _   _
            #   |  ___|  _   _  | | | |   | | | |   ___    _   _   ___    ___
            #   | |_    | | | | | | | |   | |_| |  / _ \  | | | | / __|  / _ \
            #   |  _|   | |_| | | | | |   |  _  | | (_) | | |_| | \__ \ |  __/
            #   |_|      \__,_| |_| |_|   |_| |_|  \___/   \__,_| |___/  \___|

            if not full_house_winner or full_house_winner_GAN == counted_list[len(counted_list) - 1]:
                check = all(item in counted_list for item in filtered_ticket)
                if ticket_no not in full_house_winner:
                    if check:
                        # print("full house gone to " + str(ticket_no))
                        full_house_winner.append(ticket_no)
                        full_house_winner_GAN = counted_list[len(counted_list) - 1]


            #    ____          _____           _   _     _   _
            #   / ___|        |  ___|  _   _  | | | |   | | | |   ___    _   _   ___    ___
            #   \___ \        | |_    | | | | | | | |   | |_| |  / _ \  | | | | / __|  / _ \
            #    ___) |  _    |  _|   | |_| | | | | |   |  _  | | (_) | | |_| | \__ \ |  __/
            #   |____/  (_)   |_|      \__,_| |_| |_|   |_| |_|  \___/   \__,_| |___/  \___|

            if not second_full_house_winner or second_full_house_winner_GAN == counted_list[len(counted_list) - 1]:
                if full_house_winner:
                    check = all(item in counted_list for item in filtered_ticket)
                    if ticket_no not in full_house_winner:
                        if counted_list[len(counted_list) - 1] in filtered_ticket:
                            if check:
                                # print("2nd full house gone to " + str(ticket_no))
                                second_full_house_winner.append(ticket_no)
                                second_full_house_winner_GAN = counted_list[len(counted_list) - 1]


            #    _____              _     _____           _   _     _   _
            #   |___ /   _ __    __| |   |  ___|  _   _  | | | |   | | | |   ___    _   _   ___    ___
            #     |_ \  | '__|  / _` |   | |_    | | | | | | | |   | |_| |  / _ \  | | | | / __|  / _ \
            #    ___) | | |    | (_| |   |  _|   | |_| | | | | |   |  _  | | (_) | | |_| | \__ \ |  __/
            #   |____/  |_|     \__,_|   |_|      \__,_| |_| |_|   |_| |_|  \___/   \__,_| |___/  \___|

            if not third_full_house_winner or third_full_house_winner_GAN == counted_list[len(counted_list) - 1]:
                if full_house_winner and second_full_house_winner:
                    check = all(item in counted_list for item in filtered_ticket)
                    in_1stHouse = ticket_no not in full_house_winner
                    in_2ndHouse = ticket_no not in second_full_house_winner
                    if in_1stHouse and in_2ndHouse:
                        if counted_list[len(counted_list) - 1] in filtered_ticket:
                            if check:
                                # print(second_full_house_winner)
                                # print(full_house_winner)
                                # print("3rd full house gone to " + str(ticket_no))
                                third_full_house_winner.append(ticket_no)
                                third_full_house_winner_GAN = counted_list[len(counted_list) - 1]

           #     ___            _          _        _____   _
            #    / _ \   _   _  (_)   ___  | | __   |  ___| (_) __   __   ___
            #   | | | | | | | | | |  / __| | |/ /   | |_    | | \ \ / /  / _ \
            #   | |_| | | |_| | | | | (__  |   <    |  _|   | |  \ V /  |  __/
            #    \__\_\  \__,_| |_|  \___| |_|\_\   |_|     |_|   \_/    \___|

            if not quickfive_winner or quickfive_winner_GAN == counted_list[len(counted_list) - 1]:
                checked_in_ticket = len([key for key, val in enumerate(counted_list) if val in set(filtered_ticket)])
                if checked_in_ticket == 5:  # Five Numbers Are At Least Required For QF
                    # print("Quick Five gone to " + str(ticket_no))
                    quickfive_winner.append(ticket_no)
                    quickfive_winner_GAN = counted_list[len(counted_list) - 1]

            #     ___            _          _        ____
            #    / _ \   _   _  (_)   ___  | | __   / ___|    ___  __   __   ___   _ __
            #   | | | | | | | | | |  / __| | |/ /   \___ \   / _ \ \ \ / /  / _ \ | '_ \
            #   | |_| | | |_| | | | | (__  |   <     ___) | |  __/  \ V /  |  __/ | | | |
            #    \__\_\  \__,_| |_|  \___| |_|\_\   |____/   \___|   \_/    \___| |_| |_|

            if not quickseven_winner or quickseven_winner_GAN == counted_list[len(counted_list) - 1]:
                checked_in_ticket = len(
                    [key for key, val in enumerate(counted_list) if val in set(filtered_ticket)])
                if checked_in_ticket == 7:  # Five Numbers Are At Least Required For QF
                    # print("Quick Seven gone to " + str(ticket_no))
                    quickseven_winner.append(ticket_no)
                    quickseven_winner_GAN = counted_list[len(counted_list) - 1]

            #    ____    _
            #   / ___|  | |_    __ _   _ __
            #   \___ \  | __|  / _` | | '__|
            #    ___) | | |_  | (_| | | |
            #   |____/   \__|  \__,_| |_|

            if not star_winner or star_winner_GAN == counted_list[len(counted_list) - 1]:
                to_be_checked_no = [
                                    filtered_ticket[0],
                                    filtered_ticket[4],
                                    filtered_ticket[7],
                                    filtered_ticket[10],
                                    filtered_ticket[14]
                                   ]
                check = all(item in counted_list for item in to_be_checked_no)
                if check:
                    # print("Star gone to " + str(ticket_no))
                    star_winner.append(ticket_no)
                    star_winner_GAN = counted_list[len(counted_list) - 1]

            #     ____
            #    / ___|   ___    _ __   _ __     ___   _ __
            #   | |      / _ \  | '__| | '_ \   / _ \ | '__|
            #   | |___  | (_) | | |    | | | | |  __/ | |
            #    \____|  \___/  |_|    |_| |_|  \___| |_|

            if not corner_winner or corner_winner_GAN == counted_list[len(counted_list) - 1]:
                to_be_checked_no = [
                                    filtered_ticket[0],
                                    filtered_ticket[4],
                                    filtered_ticket[10],
                                    filtered_ticket[14]
                                    ]
                check = all(item in counted_list for item in to_be_checked_no)
                if check:
                    # print("Corner gone to " + str(ticket_no))
                    corner_winner.append(ticket_no)
                    corner_winner_GAN = counted_list[len(counted_list) - 1]

            #    _           _       _       _
            #   / |    ___  | |_    | |     (_)  _ __     ___
            #   | |   / __| | __|   | |     | | | '_ \   / _ \
            #   | |   \__ \ | |_    | |___  | | | | | | |  __/
            #   |_|   |___/  \__|   |_____| |_| |_| |_|  \___|

            if not first_line_winner or first_line_winner_GAN == counted_list[len(counted_list) - 1]:
                to_be_checked_no = [filtered_ticket[0], filtered_ticket[1], filtered_ticket[2], filtered_ticket[3],
                                    filtered_ticket[4]]
                check = all(item in counted_list for item in to_be_checked_no)
                if check:
                    # print("1st Line gone to " + str(ticket_no))
                    first_line_winner.append(ticket_no)
                    first_line_winner_GAN = counted_list[len(counted_list) - 1]

            #    ____                  _     _       _
            #   |___ \     _ __     __| |   | |     (_)  _ __     ___
            #     __) |   | '_ \   / _` |   | |     | | | '_ \   / _ \
            #    / __/    | | | | | (_| |   | |___  | | | | | | |  __/
            #   |_____|   |_| |_|  \__,_|   |_____| |_| |_| |_|  \___|

            if not second_line_winner or second_line_winner_GAN == counted_list[len(counted_list) - 1]:
                to_be_checked_no = [filtered_ticket[5], filtered_ticket[6], filtered_ticket[7], filtered_ticket[8],
                                    filtered_ticket[9]]
                check = all(item in counted_list for item in to_be_checked_no)
                if check:
                    # print("2nd Line gone to " + str(ticket_no))
                    second_line_winner.append(ticket_no)
                    second_line_winner_GAN = counted_list[len(counted_list) - 1]

            #    _____                _     _       _
            #   |___ /     _ __    __| |   | |     (_)  _ __     ___
            #     |_ \    | '__|  / _` |   | |     | | | '_ \   / _ \
            #    ___) |   | |    | (_| |   | |___  | | | | | | |  __/
            #   |____/    |_|     \__,_|   |_____| |_| |_| |_|  \___|

            if not third_line_winner or third_line_winner_GAN == counted_list[len(counted_list) - 1]:
                to_be_checked_no = [filtered_ticket[10], filtered_ticket[11], filtered_ticket[12],
                                    filtered_ticket[13], filtered_ticket[14]]
                check = all(item in counted_list for item in to_be_checked_no)
                if check:
                    # print("3rd Line gone to " + str(ticket_no))
                    third_line_winner.append(ticket_no)
                    third_line_winner_GAN = counted_list[len(counted_list) - 1]

        #    _   _         ____    _                     _
        #   | | | |       / ___|  | |__     ___    ___  | |_
        #   | |_| |       \___ \  | '_ \   / _ \  / _ \ | __|
        #   |  _  |  _     ___) | | | | | |  __/ |  __/ | |_
        #   |_| |_| (_)   |____/  |_| |_|  \___|  \___|  \__|

        if not half_sheet_winner or half_sheet_winner_GAN == counted_list[len(counted_list) - 1]:
            #print(HalfSheet())
            for hs_tkts in HalfSheet():
                tkt_comp = 0
                for ticket in str(hs_tkts).split("-"):
                    tkt = int(ticket)
                    tkt_data = json.loads(Ticket.objects.get(ticket_no=tkt).ticket_digits)
                    tkt_data = list(filter(lambda a: a != 0, tkt_data))
                    checked_in_ticket = len([key for key, val in enumerate(counted_list) if val in set(tkt_data)])
                    if checked_in_ticket >= 2:
                        tkt_comp = tkt_comp+1
                if tkt_comp==3:
                    half_sheet_winner.append(hs_tkts)
                    half_sheet_winner_GAN = counted_list[len(counted_list) - 1]

        if not full_sheet_winner or full_sheet_winner_GAN == counted_list[len(counted_list) - 1]:
            #print(FullSheet())
            for fs_tkts in FullSheet():
                tkt_comp = 0
                for ticket in str(fs_tkts).split("-"):
                    tkt = int(ticket)
                    tkt_data = json.loads(Ticket.objects.get(ticket_no=tkt).ticket_digits)
                    tkt_data = list(filter(lambda a: a != 0, tkt_data))
                    checked_in_ticket = len([key for key, val in enumerate(counted_list) if val in set(tkt_data)])
                    if checked_in_ticket >= 2:
                        tkt_comp = tkt_comp+1
                if tkt_comp==6:
                    full_sheet_winner.append(fs_tkts)
                    full_sheet_winner_GAN = counted_list[len(counted_list) - 1]

        #   __        __  _           _   _               _   _
        #   \ \      / / (_)  _ __   | | | |  _ __     __| | | |_
        #    \ \ /\ / /  | | | '_ \  | | | | | '_ \   / _` | | __|
        #     \ V  V /   | | | | | | | |_| | | |_) | | (_| | | |_
        #      \_/\_/    |_| |_| |_|  \___/  | .__/   \__,_|  \__|
        #                                    |_|    
        if quickfive_winner and quickfive_winner_GAN == counted_list[len(counted_list)-1]:
            if SetDivident.objects.first().quickfive:                
                tickets = quickfive_winner 
                last_called_no = quickfive_winner_GAN
                achievement = 'quick_five'                
                quickfive_flag = True
                save_win(tickets,achievement,last_called_no)  
        if quickseven_winner and quickseven_winner_GAN == counted_list[len(counted_list) - 1]:
            if SetDivident.objects.first().quickseven:                
                tickets = quickseven_winner 
                last_called_no = quickseven_winner_GAN
                achievement = 'quick_seven'                
                quickseven_flag = True
                save_win(tickets,achievement,last_called_no)
        if star_winner and star_winner_GAN == counted_list[len(counted_list)-1]:
            if SetDivident.objects.first().star:                
                tickets = star_winner 
                last_called_no = star_winner_GAN
                achievement = 'star'                
                star_flag = True
                save_win(tickets,achievement,last_called_no)    
        if corner_winner and corner_winner_GAN == counted_list[len(counted_list) - 1]:
            if SetDivident.objects.first().corner:                
                tickets = corner_winner 
                last_called_no = corner_winner_GAN
                achievement = 'corner'                
                corner_flag = True
                save_win(tickets,achievement,last_called_no)
        if first_line_winner and first_line_winner_GAN == counted_list[len(counted_list)-1]:
            if SetDivident.objects.first().first_line:                
                tickets = first_line_winner 
                last_called_no = first_line_winner_GAN
                achievement = 'line_1'                
                first_line_flag = True
                save_win(tickets,achievement,last_called_no)
        if second_line_winner and second_line_winner_GAN == counted_list[len(counted_list)-1]:
            if SetDivident.objects.first().second_line:                
                tickets = second_line_winner 
                last_called_no = second_line_winner_GAN
                achievement = 'line_2'                
                second_line_flag = True
                save_win(tickets,achievement,last_called_no)
        if third_line_winner and third_line_winner_GAN == counted_list[len(counted_list)-1]:
            if SetDivident.objects.first().third_line:                
                tickets = third_line_winner 
                last_called_no = third_line_winner_GAN
                achievement = 'line_3'                
                third_line_flag = True
                save_win(tickets,achievement,last_called_no)
                
        if half_sheet_winner and half_sheet_winner_GAN == counted_list[len(counted_list)-1]:
            if SetDivident.objects.first().half_sheet:                
                tickets = half_sheet_winner 
                last_called_no = half_sheet_winner_GAN
                achievement = 'half_sheet'
                save_win(tickets,achievement,last_called_no)
                half_sheet_flag = True
        if full_sheet_winner and full_sheet_winner_GAN == counted_list[len(counted_list)-1]:
            if SetDivident.objects.first().full_sheet:                
                tickets = full_sheet_winner
                last_called_no = full_sheet_winner_GAN
                achievement = 'full_sheet'
                save_win(tickets,achievement,last_called_no)
                full_sheet_flag = True        
        if full_house_winner and full_house_winner_GAN == counted_list[len(counted_list)-1]:            
            tickets = full_house_winner
            last_called_no = full_house_winner_GAN
            achievement = 'full_house'            
            save_win(tickets,achievement,last_called_no)
            if SetDivident.objects.first().full_house == 1:                
                full_house_flag = 1
        if second_full_house_winner and second_full_house_winner_GAN == counted_list[len(counted_list)-1]:            
            tickets = second_full_house_winner 
            last_called_no = second_full_house_winner_GAN
            achievement = 'second_full_house'
            save_win(tickets,achievement,last_called_no)
            if SetDivident.objects.first().full_house == 2:                
                full_house_flag = 2
        if third_full_house_winner and third_full_house_winner_GAN == counted_list[len(counted_list)-1]:            
            tickets = third_full_house_winner 
            last_called_no = third_full_house_winner_GAN
            achievement = 'third_full_house'
            save_win(tickets,achievement,last_called_no)
            if SetDivident.objects.first().full_house == 3:
                full_house_flag = 3
        if divident_obj.full_house == full_house_flag and divident_obj.first_line == first_line_flag and divident_obj.second_line == second_line_flag and divident_obj.third_line == third_line_flag and divident_obj.quickfive == quickfive_flag and divident_obj.quickseven == quickseven_flag and divident_obj.star == star_flag and divident_obj.corner == corner_flag:
            game_play = GameplayStatus.objects.all().last()                
            game_play.game_over = True
            game_play.save()
            return
        time.sleep(time_delay)
