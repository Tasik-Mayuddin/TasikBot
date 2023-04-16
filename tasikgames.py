import random

class Player21:

    def __init__(self, name, handinst):
        self.name = name
        self.playerhand = handinst
        self.playercards = self.playerhand.get_cards()
        self.ready = False

    def draw_from_deck(self, deck, n):
        for i in range(n):
            deck.draw(self.playerhand)

    def check_score(self):
        score = 0
        acecounter = 0

        for x in self.playercards:
            for y in self.playercards[x]:
                if y in ['J', 'Q', 'K']:
                    score += 10
                elif y == 'A':
                    acecounter += 1
                else:
                    score += int(y)

        for i in range(acecounter):
            if score + 11 <= 21:
                score += 11
            else:
                score += 1

        return score


class Deck:
    cardNum = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    cardType = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
    cards = {}
    for x in cardType:
        cards[x] = []
        for y in cardNum:
            cards[x].append(y)

    def get_cards(self):
        return self.cards

    def draw(self, handinst):
        randtype = random.randint(0, len(self.cards) - 1)
        dictkey = list(self.cards.keys())[randtype]

        # finds non empty type
        while len(self.cards[dictkey]) == 0:
            randtype += -1
            try:
                dictkey = list(self.cards.keys())[randtype]
            except:
                return 'Empty deck!'

        randnum = random.randint(0, len(self.cards[dictkey]) - 1)
        handinst.receive(dictkey,self.cards[dictkey][randnum])
        del self.cards[dictkey][randnum]


    def add(self, intypenum):
        rel = intypenum.split()
        self.cards[rel[1]].append(rel[0])


class Hand:
    def __init__(self):
        self.cardType = ['Clubs', 'Spades', 'Hearts', 'Diamonds']
        self.cards = {}
        for x in self.cardType:
            self.cards[x] = []

    def get_cards(self):
        return self.cards

    def receive(self,dictkey,cardnum):
        self.cards[dictkey].append(cardnum)

    def draw(self,dictkey,cardnum):
        for x in self.cards[dictkey]:
            if x == cardnum:
                return dictkey, self.cards[dictkey][self.cards[dictkey].index(x)]
                del self.cards[dictkey][self.cards[dictkey].index(x)]

# 21 game

def check_winner(player1, player2):

    player1score = player1.check_score()
    player2score = player2.check_score()

    if player1score > 21 and player2score <= 21:
        return f'{player2.name} wins with {player2score} vs {player1score}'
    elif player2score > 21 and player1score <= 21:
        return f'{player1.name} wins with {player1score} vs {player2score}'
    elif player1score > player2score and player1score <= 21:
        return f'{player1.name} wins with {player1score} vs {player2score}'
    elif player1score < player2score and player2score <= 21:
        return f'{player2.name} wins with {player2score} vs {player1score}'
    else:
        return f'Tie!\n{player1.name} has {player1score}\n{player2.name} has {player2score}'
