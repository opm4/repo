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


standard_deck = create_deck()

# definim lista de jucatori - global passed to function
jucatori = [{
    'nume': 'Iulian',
    'carti': [],
    'doua_perechi': [],
    'buget': 500
},
    {
        'nume': 'Manu',
        'carti': [],
        'doua_perechi': [],
        'buget': 500
},
    {
        'nume': 'Adina',
        'carti': [],
        'doua_perechi': [],
        'buget': 500
}
]
#  pot should also be global and should reset with game not round
#  - Game last until we have a winner (last man standing)
pot = 0
game_on = True

while game_on:
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
        try:
            pair = max([int(card)
                        for card, counter in most_common if counter == 2])
        except ValueError:
            pair = 0
        jucator['doua_perechi'] = pair

    winner_pair = 0
    winner = None
    for jucator in jucatori:
        if int(jucator['doua_perechi']) > winner_pair:
            winner_pair = jucator['doua_perechi']
            winner = jucator

    winner['buget'] += pot
    nume = winner['nume']
    print(f"A castigat {nume} ")
    pprint(jucatori)

    players_in_game = len(jucatori)

    for jucator in jucatori:
        if jucator['buget'] == 0:
            players_in_game -= 1
        else:
            player = jucator['nume']
    if players_in_game == 1:
        print(f'The game winner is {player}')
        break
