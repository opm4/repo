#  from https://www.askpython.com/python/examples/rock-paper-scissors-in-python
#
from random import randint
# define dictionary for game options
game_map = {0: "rock", 1: "paper", 2: "scissors", 3: "lizard", 4: "spock"}
# define result matrix - according to the example in the link
rpsls_table = [[-1, 1, 0, 0, 4], [1, -1, 2, 3, 1],
               [0, 2, -1, 2, 4], [0, 3, 2, -1, 3], [4, 1, 4, 3, -1]]
# Define main frame for game
menu_opt = {1: 'Play Game', 2: 'Get the rules', 3: 'Exit'}
# print(menu_opt)
# define all results for printing and for game result
results = {'21': "Scissors cuts Paper",
           '10': "Paper covers Rock",
           '03': "Rock crushes Lizard",
           '34': "Lizard poisons Spock",
           '42': "Spock smashes Scissors",
           '23': "Scissors decapitates Lizard",
           '31': "Lizard eats Paper",
           '14': "Paper disproves Spock",
           '40': "Spock vaporizes Rock",
           '02': "Rock crushes Scissors",
           }
# define result matrix with reference to the dictionary so it can be used to decide winner and help print results
map_mess_res = [[-1, '10', '02',	'03',	'40'],
                ['10',  -1, '21',	'31',	'14'],
                ['02', '21',   -1,  '23',   '42'],
                ['03', '31', '23',    -1,   '34'],
                ['40', '14', '42',   '34',    -1]]

# function to det the key from value in a dictioary


def get_key(val, choices):
    for key, value in choices.items():
        if val == value:
            return key

# funtion for deciding the winner


def get_results(user_choice, comp_choice, index_round, score):
    #  get global used variables
    global map_mess_res, results
    print(
        f'You chose {game_map.get(user_choice)} and Computer chose {game_map.get(comp_choice)}')
    # game logic for deciding the results

    if int(map_mess_res[int(user_choice)][comp_choice]) == -1:
        print(f'Draw Game round {index_round}')
        print(f'~~~~~~~~~~~~~~~~')
        score[2] += 1
        return score
    elif int(map_mess_res[int(user_choice)][comp_choice][0]) == int(user_choice):
        print(f'You win round {index_round}!')
        print(f' {results.get( map_mess_res[int(user_choice)][comp_choice])}')
        print(f'~~~~~~~~~~~~~~~~')
        score[0] += 1
        return score
    else:
        print(f'Computer wins round {index_round}')
        print(f' {results.get( map_mess_res[int(user_choice)][comp_choice])}')
        print(f'~~~~~~~~~~~~~~~~')
        score[1] += 1
        return score

# Start round

# function that is used to play rounds


def play_round():
    # define global variables to be used in the game
    global rpsls_table, game_map, name, map_mess_res, results
    # keep track of rounds
    index_round = 0
    # keep track of results: [user score, computer score, draw rounds]
    score = [0, 0, 0]
    print(
        f'Options for game \n {game_map} \n And q - to return to previous menu \n or h - to see the rules')
    print(f'\n ---------------------- \n')
    #  play round loop
    while True:

        print(f'Let the round begin ')

        # increment the round since we start with 0
        # maybe the round count should be updated after a valid choice and not as it is now
        index_round += 1

        # get inputs
        user_choice = input(f'Please select choice = ')
        comp_choice = randint(0, len(game_map)-1)

        # options for round play: q - exit, h - help, choice: str or int
        # it still needs some adjustments because if you input other options it will trow an error from time to time
        if user_choice == 'q':
            print(f'\n ---------------------- \n')
            print(
                f'the score is: \n {name}: {score[0]} \n Computer : {score[1]} \n Draw : {score[2]}')
            break
        elif user_choice == 'h':
            print(f'Explain rules \n {results} \n {game_map}')
        elif user_choice.lower() in game_map.values():
            # print(f' Valid Choice')
            user_choice = get_key(user_choice.lower(), game_map)
            score = get_results(user_choice, comp_choice, index_round, score)

        elif user_choice in ['0', '1', '2', '3', '4'] and int(user_choice) in game_map.keys():
            # print(f'Also a valid choice')
            # print(f'{choice} , {game_map.get(int(choice))}')
            user_choice = int(user_choice)
            score = get_results(user_choice, comp_choice, index_round, score)

        else:
            print('Not a good answer')
            print(f'\n ---------------------- \n')
            continue


#  Here starts the main program
# get user Name
print(f'\n Welcome to RPSLS - The Game \n')
name = input("Enter your name: ")
print(f'\n ---------------------- \n')
# main Game Loop
while True:
    # Master Game
    print(f'let \n  the games beggin \n {menu_opt}')

    # get options for main game
    # something like this needs to be implemented above as well in the get results and play round
    try:
        choice = int(input(f'Enter yor choice = '))
    except ValueError:
        # clear()
        print('Not a valid choice')
        print(f'\n ---------------------- \n')
        continue

    if choice == 1:
        print(f' Play the Game')
        play_round()

    elif choice == 2:
        print(f'Print the rules \n {results}')
        print(f'\n ---------------------- \n')

    elif choice == 3:
        print(f'See you! {name}')
        print(f'\n ---------------------- \n')
        break
    else:
        # clear()
        print(f'Wrong Input')
