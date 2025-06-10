import random

# setup
suits = ('hearts', 'diamonds', 'spades', 'clubs')
ranks = ('two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king', 'ace')
values = {'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9,
          'ten':10, 'jack':10, 'queen':10, 'king':10, 'ace':11}

playing = True

# card class
class card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit

# deck class
class deck:
    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

# hand class
class hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# chips class
class chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

# function to take a bet
def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("how many chips would you like to bet? "))
        except:
            print("please enter a number.")
        else:
            if chips.bet > chips.total:
                print("you don't have enough chips!")
            else:
                break

# function to deal a card
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# function to choose hit or stand
def hit_or_stand(deck, hand):
    global playing
    while True:
        choice = input("do you want to hit or stand? (h or s): ")
        if choice.lower() == 'h':
            hit(deck, hand)
        elif choice.lower() == 's':
            print("you chose to stand. dealer's turn.")
            playing = False
        else:
            print("please enter 'h' or 's'.")
            continue
        break

# show cards with one dealer card hidden
def show_some(player, dealer):
    print("\ndealer's hand:")
    print(" <card hidden>")
    print(" ", dealer.cards[1])
    print("\nyour hand:")
    for card in player.cards:
        print(" ", card)

# show all cards
def show_all(player, dealer):
    print("\ndealer's hand:")
    for card in dealer.cards:
        print(" ", card)
    print("value =", dealer.value)
    print("\nyour hand:")
    for card in player.cards:
        print(" ", card)
    print("value =", player.value)

# result functions
def player_busts(chips):
    print("you busted!")
    chips.lose_bet()

def player_wins(chips):
    print("you win!")
    chips.win_bet()

def dealer_busts(chips):
    print("dealer busted!")
    chips.win_bet()

def dealer_wins(chips):
    print("dealer wins!")
    chips.lose_bet()

def push():
    print("it's a tie!")

# main game loop
while True:
    print("welcome to blackjack!")
    print("try to get as close to 21 as you can without going over.")
    print("dealer hits until 17. aces count as 1 or 11.")

    # create and shuffle deck
    game_deck = deck()
    game_deck.shuffle()

    # create hands
    player_hand = hand()
    player_hand.add_card(game_deck.deal())
    player_hand.add_card(game_deck.deal())

    dealer_hand = hand()
    dealer_hand.add_card(game_deck.deal())
    dealer_hand.add_card(game_deck.deal())

    # set chips
    player_chips = chips()
    take_bet(player_chips)

    # show cards
    show_some(player_hand, dealer_hand)

    while playing:
        hit_or_stand(game_deck, player_hand)
        show_some(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_busts(player_chips)
            break

    # dealer plays if player didn't bust
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(game_deck, dealer_hand)

        show_all(player_hand, dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_chips)
        else:
            push()

    print("chips left:", player_chips.total)

    new_game = input("play another round? (y or n): ")
    if new_game.lower() == 'y':
        playing = True
        continue
    else:
        print("thanks for playing!")
        break
