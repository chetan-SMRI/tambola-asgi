# for converting text to 3 layer text https://patorjk.com/software/taag/#p=display&h=0&c=bash&f=Standard&t=S.%20Full%20House
def run_game():
    #    _       _   _
    #   | |     (_) | |__    ___
    #   | |     | | | '_ \  / __|
    #   | |___  | | | |_) | \__ \
    #   |_____| |_| |_.__/  |___/
    import os
    import random
    #
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Tambola.settings")
    #
    import django
    django.setup()
    
    from django.core.management import call_command
    from game.models import TicketDailyData as ticket_daily_data
    import json
    import time
    import random
    from game.models import Ticket

    #   __     __
    #   \ \   / /   __ _   _ __   ___
    #    \ \ / /   / _` | | '__| / __|
    #     \ V /   | (_| | | |    \__ \
    #      \_/     \__,_| |_|    |___/

    # Abbreviation GAN = Gone At Number
    to_be_count_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                        27, 28,
                        29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52,
                        53, 54,
                        55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78,
                        79, 80,
                        81, 82, 83, 84, 85, 86, 87, 88, 89, 90]
    counted_list = []
    second_full_house_winner = []
    full_house_winner = []
    first_line_winner = []
    second_line_winner = []
    third_line_winner = []
    quickfive_winner = []
    star_winner = []
    half_sheet_winner = []
    second_full_house_winner_GAN = None
    full_house_winner_GAN = None
    first_line_winner_GAN = None
    second_line_winner_GAN = None
    third_line_winner_GAN = None
    quickfive_winner_GAN = None
    star_winner_GAN = None
    half_sheet_winner_GAN = None

    #    ____
    #   |  _ \   _   _   _ __
    #   | |_) | | | | | | '_ \
    #   |  _ <  | |_| | | | | |
    #   |_| \_\  \__,_| |_| |_|

    for i in range(1, 90):
        # For Stopping Process When Second Full House Gone
        if second_full_house_winner == []:
            selected_number = random.choice(to_be_count_list)  # Choosing Random No.
            counted_list.append(selected_number)
            ticket_data_obj = ticket_daily_data.objects.first()
            ticket_data_obj.ticket_digits = str(counted_list)
            ticket_data_obj.save()  # Inserting it to DB
            # print(counted_list)
            to_be_count_list.remove(selected_number)  # Removing No. From List For Avoiding Repetition

            #   __        __  _
            #   \ \      / / (_)  _ __    _ __     ___   _ __
            #    \ \ /\ / /  | | | '_ \  | '_ \   / _ \ | '__|
            #     \ V  V /   | | | | | | | | | | |  __/ | |
            #      \_/\_/    |_| |_| |_| |_| |_|  \___| |_|

            for ticket in Ticket.objects.all():
                ticket_no = ticket.ticket_no
                ticket_digits = json.loads(ticket.ticket_digits)
                filtered_ticket = list(
                    filter(lambda a: a != 0, ticket_digits))  # Removing Zeroes in Ticket Data For Winner Selecting Algo

                #    ____          _____           _   _     _   _
                #   / ___|        |  ___|  _   _  | | | |   | | | |   ___    _   _   ___    ___
                #   \___ \        | |_    | | | | | | | |   | |_| |  / _ \  | | | | / __|  / _ \
                #    ___) |  _    |  _|   | |_| | | | | |   |  _  | | (_) | | |_| | \__ \ |  __/
                #   |____/  (_)   |_|      \__,_| |_| |_|   |_| |_|  \___/   \__,_| |___/  \___|

                if not second_full_house_winner or second_full_house_winner_GAN == counted_list[len(counted_list) - 1]:
                    if full_house_winner:
                        check = all(item in counted_list for item in filtered_ticket)
                        if ticket_no not in full_house_winner:
                            if check:
                                # print("2nd full house gone to " + str(ticket_no))
                                second_full_house_winner.append(ticket_no)
                                second_full_house_winner_GAN = counted_list[len(counted_list) - 1]

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

                #     ___            _          _        _____   _
                #    / _ \   _   _  (_)   ___  | | __   |  ___| (_) __   __   ___
                #   | | | | | | | | | |  / __| | |/ /   | |_    | | \ \ / /  / _ \
                #   | |_| | | |_| | | | | (__  |   <    |  _|   | |  \ V /  |  __/
                #    \__\_\  \__,_| |_|  \___| |_|\_\   |_|     |_|   \_/    \___|

                if not quickfive_winner or quickfive_winner_GAN == counted_list[len(counted_list) - 1]:
                    checked_in_ticket = 0
                    for k in range(15):
                        if filtered_ticket[k] in counted_list:
                            checked_in_ticket = checked_in_ticket + 1
                        else:
                            pass
                    if checked_in_ticket == 5:  # Five Numbers Are Atleast Required For QF
                        # print("Quick Five gone to " + str(ticket_no))
                        quickfive_winner.append(ticket_no)
                        quickfive_winner_GAN = counted_list[len(counted_list) - 1]

                #    ____    _
                #   / ___|  | |_    __ _   _ __
                #   \___ \  | __|  / _` | | '__|
                #    ___) | | |_  | (_| | | |
                #   |____/   \__|  \__,_| |_|

                if not star_winner or star_winner_GAN == counted_list[len(counted_list) - 1]:
                    to_be_checked_no = [filtered_ticket[0], filtered_ticket[4], filtered_ticket[7], filtered_ticket[10],
                                        filtered_ticket[14]]
                    check = all(item in counted_list for item in to_be_checked_no)
                    if check:
                        # print("1st Line gone to " + str(ticket_no))
                        star_winner.append(ticket_no)
                        star_winner_GAN = counted_list[len(counted_list) - 1]

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
            #   __        __  _           _   _               _   _
            #   \ \      / / (_)  _ __   | | | |  _ __     __| | | |_
            #    \ \ /\ / /  | | | '_ \  | | | | | '_ \   / _` | | __|
            #     \ V  V /   | | | | | | | |_| | | |_) | | (_| | | |_
            #      \_/\_/    |_| |_| |_|  \___/  | .__/   \__,_|  \__|
            #                                    |_|
            if quickfive_winner and quickfive_winner_GAN == counted_list[len(counted_list)-1]:
                print("Quick Five gone to " + str(quickfive_winner) + ' at '+str(quickfive_winner_GAN))
            if star_winner and star_winner_GAN == counted_list[len(counted_list)-1]:
                print("Star gone to " + str(star_winner) + ' at '+str(star_winner_GAN))
            if first_line_winner and first_line_winner_GAN == counted_list[len(counted_list)-1]:
                print("1st line gone to " + str(first_line_winner) + ' at '+str(first_line_winner_GAN))
            if second_line_winner and second_line_winner_GAN == counted_list[len(counted_list)-1]:
                print("2nd line gone to " + str(second_line_winner) + ' at '+str(second_line_winner_GAN))
            if third_line_winner and third_line_winner_GAN == counted_list[len(counted_list)-1]:
                print("3rd line gone to " + str(third_line_winner) + ' at '+str(third_line_winner_GAN))
            if full_house_winner and full_house_winner_GAN == counted_list[len(counted_list)-1]:
                print("1st f.house gone to " + str(full_house_winner) + ' at '+str(full_house_winner_GAN))
            if second_full_house_winner and second_full_house_winner_GAN == counted_list[len(counted_list)-1]:
                print("2nd f.house gone to " + str(second_full_house_winner) + ' at '+str(second_full_house_winner_GAN))
            time.sleep(10)
        else:
            return

if __name__ == '__main__':
    run_game()
