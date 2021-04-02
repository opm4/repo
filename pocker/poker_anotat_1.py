from pprint import pprint
from collections import Counter

"""
Python Hold'em Poker

Vom crea un joc de poker, cu mai multe runde, cu reguli putin simplificate
Fiecare jucator isi cumpara intrarea in joc, cumparand jetoane. Buy-in-ul este 500 de dolari (jetoane)

Fiecare runda are urmatorii pasi:
1. Pachetul de carti complet se amesteca
2. Fiecare jucator primeste 2 carti din pachet
2.1 Runda de pariuri - suma minima
3. Se afiseaza "the flop" - din pachet se scot 3 carti si se pun pe masa
3.1 Runda de pariuri
4. Se afiseaza "the turn" - din pachet se mai scoate o carte si se pune pe masa
4.1 Runda de pariuri
5. Se afiseaza "the river" - din pachet se mai scoata o carte
5.1 runda de pariuri
6. Jucatorii ramasi trebuie sa faca prezinte cea mai buna combinatie care o pot face cu cartile din mana si cele de pe masa.
6.1 Castigatorul rundei ia toti banii (jetoanele) din runda respectiva in contul sau. In cazul in care sunt mai mult castigatori, castigul se impart egal intre ei

* In cazul in care un jucator ramane fara bani, este eliminat din concurs.
* In fiecare runda de pariuri toti jucatorii trebuie sa parieze aceeasi suma sau au optiunea sa se retraga din runda (fold)

Combinatii castigatoare in ordinea rangului:
2 perechi - un jucator are 2 perechi formate: de exemplu (A,A), (6,6)
Mai mult reguli sunt detaliate aici
https://www.pokerlistings.com/poker-rules-texas-holdem

La curs am ajuns sa simulam o runda.
Ca si tema
 - rezolvati problema compararii J,Q,K,A
 - rezolvati problema compararii a 2 perechi (programul sa aleaga cea mai avantajoasa pereche pentru jucator)
 - adaugati sistemul de pariere si urmarire a castigurilor
   - memorati cati bani are un jucator inainte de fiecare runda
 - adaugati posibilitatea jucarii de mai multe runde
    - pana cand ramane un singur jucator
To do:
 - daca exista perechi egale sau nimeni nu are combinatie castigatore sa castige cea mai avantajoasa carte din mana 
"""
# generam un pachet de carti complet
# define funtion to get the pack - reshuffle the pach for each round


def create_deck(opt='r'):
    if opt == 'r':
        # ,'J', 'Q', 'K', 'A']
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10']
        colors = ['spades', 'hearts', 'clubs', 'diamonds']
        standard_deck = set((card, color)
                            for card in cards for color in colors)
        return standard_deck
    elif opt == 'f':
        cards = ['2', '3', '4', '5', '6', '7',
                 '8', '9', '10', 'J', 'Q', 'K', 'A']
        colors = ['spades', 'hearts', 'clubs', 'diamonds']
        standard_deck = set((card, color)
                            for card in cards for color in colors)
        return standard_deck
    else:
        print('Not a known option')
        return None


cards_dict = {'2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6,
                      '8': 7, '9': 8, '10': 9, 'J': 10, 'Q': 11, 'K': 12, 'A': 13}


# definim lista de jucatori - global passed to function
jucatori = [{
    'nume': 'Iulian',
    'carti': [],
    # 'o_pereche': [],
    'doua_perechi': [],
    'trei_bucati': [],
    'buget': 500
},
    {
        'nume': 'Manu',
        'carti': [],
        # 'o_pereche': [],
        'doua_perechi': [],
        'trei_bucati': [],
        'buget': 500
},
    {
        'nume': 'Adina',
        'carti': [],
        # 'o_pereche': [],
        'doua_perechi': [],
        'trei_bucati': [],
        'buget': 500
}
]
#  pot should also be global and should reset with game not round
#  - Game last until we have a winner (last man standing)


standard_deck = create_deck('f')

while True:
    # reset pot on the table
    pot = 0
    # reshuffle the dech when there are less cards than required to play
    if len(standard_deck) < len(jucatori) * 2 + 5:
        standard_deck = create_deck('f')
    # function to give card to player
    for jucator in jucatori:
        if int(jucator['buget']) > 0:
            # pentru ca pachetul de carti (standard_deck) este un set .pop scoate aleatoriu un element - o carte
            jucator['carti'].append(standard_deck.pop())
            jucator['carti'].append(standard_deck.pop())
            nume = jucator['nume']
            buget = jucator['buget']
            print(jucator['carti'])
            print(f"{nume} cat vrei sa pariezi? Ai disponibil {buget}")
            # should be implemented with try except because you can input also non interger as string
            while True:
                pariu = input()
                if int(pariu) <= int(buget) and int(pariu) > 0:
                    jucator['buget'] -= int(pariu)
                    pot += int(pariu)
                    break
                else:
                    print(
                        f'Ai pariat {pariu}, care este o suma invalida, in banca mai ai disponibil {buget}')
                    print('Te rugam sa mai pariezi inca o data o suma valida.')
        else:
            # if there is no buget any more
            pass

    # The Flop, the turn si the river sunt compactate intr-o singura etapa aici
    # Check flop and river -  have function to give the card on the deck
    carti_masa = [standard_deck.pop() for _ in range(5)]
    pprint(carti_masa)
    for jucator in jucatori:
        print(jucator['nume'])
        # Punem impreuna cartile jucatorului cu cele de pe masa sa le putem evalua mai usor
        total_carti_jucator = []
        total_carti_jucator.extend(carti_masa)
        total_carti_jucator.extend(jucator['carti'])

        # Extragem doar numarul cartii, din lista de tuple de forma (numar, culoare)
        total_carti_jucator = [numar for numar, culoare in total_carti_jucator]

        # numaram cate carti de acelasi tip are jucatorul (ca sa identificam posibile 3 bucati sau 2 perechi)
        counter = Counter(total_carti_jucator)
        most_common = counter.most_common()

        print(most_common)
        # print(counter.most_common(3))
        # check hand to see who has higher value
        # count pairs and three of a kind, then the highest value card to decide winner
        for card, counter_no in most_common:
            # we found a pair or three of a kind
            if counter_no == 2:
                jucator['doua_perechi'].append(card)
            elif counter_no == 3:
                jucator['trei_bucati'].append(card)

    # decide winner
    # winner_pair = 0
    winner_hand = []
    winner = None
    #  Game logic: search for three of a kind,
    #  if somebody has it then compair it with who has also three of a kind
    # if nobody has three of a kind go to two pairs and compair who has the highest combination of pairs
    #  if nobody has two pairs then go to one pair and search who has the biggest combination og pairs
    #  you shoudl also check if multiple plaiers have the same combo to check the highest card
    # in the player hand
    winner_hand = []
    winner = {}
    for jucator in jucatori:
        hand = [jucator['trei_bucati'], jucator['doua_perechi']]
        name = jucator['nume']
        print(f'{name} has {hand}')

        # check for three pairs
        if len(hand[0]) != 0 and (winner_hand == [] or winner_hand[1] < 3):
            winner_hand = [hand, 3]
            winner = jucator
        elif len(hand[0]) != 0 and winner_hand[1] == 3:
            # introduce also min max for three of a kind
            if cards_dict[hand[0][0]] > cards_dict[winner_hand[0][0]]:
                winner_hand = [hand, 3]
                winner = jucator
            elif cards_dict[hand[0][0]] == cards_dict[winner_hand[0][0]]:
                print(f'Draw game between {winner} and {name}')

        # check for 2 pairs or three pairs
        if len(hand[1]) >= 2 and (winner_hand == [] or winner_hand[1] < 2 or len(winner_hand[0]) < 3):
            winner_hand = [hand, 2]
            winner = jucator
        elif len(hand[1]) == 2 and winner_hand[1] == 2:
            if max([cards_dict[i] for i in hand[1]]) > max([cards_dict[i] for i in winner_hand[0][1]]):
                winner_hand = [hand, 2]
                winner = jucator
            elif max([cards_dict[i] for i in hand[1]]) == max([cards_dict[i] for i in winner_hand[0][1]]):
                if min([cards_dict[i] for i in hand[1]]) > min([cards_dict[i] for i in winner_hand[0][1]]):
                    winner_hand = [hand, 2]
                    winner = jucator
                elif min([cards_dict[i] for i in hand[1]]) == min([cards_dict[i] for i in winner_hand[0][1]]):
                    print(f'Draw game between {winner} and {name}')

        # compare a single pair
        elif len(hand[1]) == 1 and (winner_hand == [] or winner_hand[1] < 1):
            winner_hand = [hand, 1]
            winner = jucator
        elif len(hand[1]) == 1 and winner_hand[1] == 1:
            if max([cards_dict[i] for i in hand[1]]) > max([cards_dict[i] for i in winner_hand[0][1]]):
                winner_hand = [hand, 1]
                winner = jucator
            elif max([cards_dict[i] for i in hand[1]]) == max([cards_dict[i] for i in winner_hand[0][1]]):
                print(f'Draw game between {winner} and {name}')

        # if nobody has nothing biggest card winns
        if len(hand[0]) == 0 and len(hand[1]) == 0 and winner_hand == []:
            total_carti_jucator = [numar for numar,
                                   culoare in total_carti_jucator]
            winner_hand = [total_carti_jucator, 0]
            winner = jucator
        elif len(hand[0]) == 0 and len(hand[1]) == 0 and winner_hand[1] == 0:
            total_carti_jucator = [numar for numar,
                                   culoare in total_carti_jucator]
            if max([cards_dict[i] for i in total_carti_jucator]) > max([cards_dict[i] for i in winner_hand[0]]):
                winner_hand = [total_carti_jucator, 0]
                winner = jucator
            elif max([cards_dict[i] for i in total_carti_jucator]) == max([cards_dict[i] for i in winner_hand[0]]):
                if min([cards_dict[i] for i in total_carti_jucator]) > min([cards_dict[i] for i in winner_hand[0]]):
                    winner_hand = [total_carti_jucator, 0]
                    winner = jucator
                elif min([cards_dict[i] for i in total_carti_jucator]) == min([cards_dict[i] for i in winner_hand[0]]):
                    print(f'Draw game between {winner} and {name}')
            # winner_hand = [0, 0]
            # winner = name

            # get the pot and show the winner
    winner['buget'] += pot
    nume = winner['nume']
    print(f"A castigat {nume} cu {winner_hand}")
    # pprint(jucatori)

    # Check game winner
    players_in_game = len(jucatori)
    for jucator in jucatori:
        # reset player hand
        jucator['carti'] = []
        jucator['doua_perechi'] = []
        # jucator['o_pereche'] = []
        jucator['trei_bucati'] = []
        # check how many players are still in the game
        if jucator['buget'] == 0:
            players_in_game -= 1
        else:
            winner = jucator['nume']
    if players_in_game == 1:
        # End game condition
        print(f'The game winner is {winner}')
        break
