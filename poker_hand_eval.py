import random
from enum import Enum

hand_size = 5


class Rank(Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

    def __str__(self):
        if self.value <= 10:
            return str(self.value)
        else:
            return self.name


class Suit(Enum):
    Spades = 1
    Clubs = 2
    Hearts = 3
    Diamonds = 4

    def __str__(self):
        return self.name


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return "[{} of {}]".format(self.rank, self.suit)


class Deck:
    def __init__(self):
        self.deck = []
        for suit in Suit:
            for rank in Rank:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        result = " "
        for card in self.deck:
            result += " " + card.__str__()
        return "Deck contains:" + result

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop(0)


class Hand:
    def __init__(self):
        self.hand = []

    def __iter__(self):
        self.list = []
        for x in self.hand:
            self.list.append(x)
        self.hand = self.list
        return iter(self.hand)

    def __str__(self):
        result = " "
        for card in self.hand:
            result += "\n     " + card.__str__()
        return "Player Hand:" + result

    def add_card(self, index, card):
        return self.hand.insert(index, card)

    def remove_card(self, index):
        return self.hand.pop(index)

    def get_index(self, index):
        return self.hand[index]


class Score:
    suits = []
    ranks = []

    def __init__(self, hand):
        for card in hand:
            self.suits.append(card.suit)
            self.ranks.append(card.rank.value)

    def is_flush(self):
        current_suit = self.suits[0]
        for suit in self.suits:
            if suit != current_suit:
                return False
            current_suit = suit
        return True

    def is_royal_flush(self):
        low = min(self.ranks)
        if low == 10 and (low + 1 in self.ranks) and (low + 2 in self.ranks) and (low + 3 in self.ranks) and (
                low + 4 in self.ranks):
            return True
        else:
            return False

    def is_four_of_a_kind(self):
        card_one_count = self.ranks.count(self.ranks[0])
        card_two_count = self.ranks.count(self.ranks[1])
        if card_one_count == 4 or card_two_count == 4:
            return True
        else:
            return False

    def is_straight(self):
        low = min(self.ranks)
        if (low + 1 in self.ranks) and (low + 2 in self.ranks) and (low + 3 in self.ranks) and (low + 4 in self.ranks):
            return True
        else:
            return False

    def is_three_of_a_kind(self):
        card_one_count = self.ranks.count(self.ranks[0])
        card_two_count = self.ranks.count(self.ranks[1])
        card_three_count = self.ranks.count(self.ranks[1])
        if card_one_count == 3 or card_two_count == 3 or card_three_count == 3:
            return True
        else:
            return False

    def is_two_pair(self):
        count = 0
        for rank in self.ranks:
            if self.ranks.count(rank) > 1:
                count += 1
            else:
                continue
        if count >= 3:
            return True
        else:
            return False

    def is_pair(self):
        for rank in self.ranks:
            if self.ranks.count(rank) > 1:
                return True
            else:
                continue
        return False

    def is_full_house(self):
        self.ranks.sort()
        card_one_count = self.ranks.count(self.ranks[0])
        card_two_count = self.ranks.count(self.ranks[len(self.ranks) - 1])

        if (card_one_count == 2 and card_two_count == 3) or (card_one_count == 3 and card_two_count == 2):
            return True
        else:
            return False

    def is_straight_flush(self):
        if self.is_flush() is True and self.is_straight() is True:
            return True
        else:
            return False


class Game:
    def __init__(self):
        print("Welcome to Five Card Draw!\n")

    def ready_deck(self):
        deck = Deck()
        deck.shuffle()
        return deck

    def deal_hand(self, deck):
        hand = Hand()
        for i in range(hand_size):
            hand.add_card(0, deck.deal_card())
        print(hand.__str__() + "\n")
        return hand

    def trade_in_cards(self, deck, hand):
        for i in range(hand_size):
            user_input = input("Would you like to keep the " + str(hand.get_index(i)) + " in your hand: (y/n) ")
            if user_input == "y":
                continue
            elif user_input == "n":
                hand.remove_card(i)
                hand.add_card(i, deck.deal_card())

        print("\nDealing cards\n\n" + hand.__str__() + "\n")

    def score_hand(self, hand):
        score = Score(hand)
        print("Hand evaluation:")
        if score.is_royal_flush() is True:
            print("Royal Flush!")
            return 10
        elif score.is_straight_flush() is True:
            print("Straight Flush!")
            return 9
        elif score.is_four_of_a_kind() is True:
            print("Four of a Kind!")
            return 8
        elif score.is_full_house() is True:
            print("Full House!")
            return 7
        elif score.is_flush() is True:
            print("Flush!")
            return 6
        elif score.is_straight() is True:
            print("Straight!")
            return 5
        elif score.is_three_of_a_kind() is True:
            print("Three of a Kind!")
            return 4
        elif score.is_two_pair() is True:
            print("Two Pair!")
            return 3
        elif score.is_pair() is True:
            print("Pair!")
            return 2
        else:
            print("High card")
            return 1


def main():
    game = Game()
    deck = game.ready_deck()
    hand = game.deal_hand(deck)
    game.trade_in_cards(deck, hand)
    game.score_hand(hand)


main()