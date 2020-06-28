'''
This is a Black jack game
'''

import random 

''' Defining Decks with Suits and Ranks'''

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

'''Defining all the classess'''

'''Card class'''

class Card():

	def __init__(self, suit, rank):

		self.suit = suit
		self.rank = rank

	def __str__(self):

		return f'{self.rank} of {self.suit}'

'''Deck Class'''

class Deck():

	def __init__(self):

		self.deck = []
		for suit in suits:
			for rank in ranks:
				self.deck.append(Card(suit, rank))

	def __str__(self):
		deck_comp = ''
		for card in self.deck:
		    deck_comp += '\n '+card.__str__()
		return 'The deck has:' + deck_comp

	def shuffle(self):
		random.shuffle(self.deck)

	def deal(self):
		single_card = self.deck.pop()
		return single_card

'''Hand Class'''

class Hand():

	def __init__(self):

		self.cards = []
		self.value = 0
		self.aces = 0

	def add_card(self,card):

		self.cards.append(card)
		self.value += values[card.rank]

	def adjust_for_ace(self):

		while self.value > 21 and self.aces:
			self.value -= 10
			self.aces -= 1

'''Chips Class'''

class Chips():

	def __init__(self):

		self.total = 100
		self.bet = 0

	def win_bet(self):

		self.total += self.bet

	def lose_bet(self):

		self.total -= self.bet

'''Defining functions'''

'''Bet placing function'''

def take_bet(chips):

	while True:
		try:
			chips.bet = int(input("How many chips would you like to bet?"))
		except ValueError:
			print('You need to give an integer value!')
		else:
			if chips.bet > chips.total:
				print("Sorry, your bet cant exceed: ", chips.total)
			else:
				break

'''Hit taking Function'''

def hit(deck, hand):

	hand.add_card(deck.deal())
	hand.adjust_for_ace()

'''User input for Hit or Stand function'''

def hit_or_stand(deck, hand):

	global playing

	while True:
		x = input("Would you like to Hit or Stand, Enter 'h' or's': ").lower()

		if x[0] == 'h':
			hit(deck, hand)
		elif x[0] == 's':
			print("Player Stands, Its dealer's turn")
			playing = False
		else:
			print('Wrong Input, Please try again!')
			continue
		break

'''Card displaying functions'''

def show_some(player, dealer):
	print("\nDealer's Hand: ")
	print(" < HIDDEN CARD >")
	print(" ", dealer.cards[1])
	print("\nPlayer's Hand: ", *player.cards, sep='\n ')
	print("")

def show_all(player, dealer):
	print("Dealer's Hand: ", *dealer.cards, sep='\n ')
	print("Dealer's Hand= ", dealer.value)
	print("\nPlayer's Hand: ", *player.cards, sep='\n ')
	print("Player's Hand= ", player.value)
	print("")

'''End game scenario functions'''

def player_busts(player,dealer,chips):

	print("Player Busts!")
	chips.lose_bet()

def player_wins(player,dealer,chips):

	print("Player Wins!")
	chips.win_bet()

def dealer_busts(player,dealer,chips):

	print("Dealer Busts!")
	chips.win_bet()

def dealer_wins(player,dealer,chips):

	print("Dealer Wins!")
	chips.lose_bet()

def push(player,dealer):

	print("Player and Dealer tied, its a push!!!")


""" The main Game Block """

while True:

	print("<------WELCOME TO BLACKJACK------>\n\nGet as close to 21 as you can without going over!")
	print("Dealer hits until she reaches 17. Aces count as 1 or 11.")
	
	deck = Deck()
	deck.shuffle() #Creating and shuffling the deck

	player_hand = Hand() #Creating Player's Hand
	player_hand.add_card(deck.deal())
	player_hand.add_card(deck.deal()) #Dealing two cards to player

	dealer_hand = Hand() #Creating Dealers's Hand
	dealer_hand.add_card(deck.deal())
	dealer_hand.add_card(deck.deal()) #Dealing two cards to dealer

	player_chip = Chips() #Setting up player's chips

	take_bet(player_chip) #Prompting user for placing bet

	show_some(player_hand,dealer_hand) #Displaying cards while keeping one of thr dealer's card hidden

	while playing:

		hit_or_stand(deck,player_hand) #Prompting user to hit or stand

		show_some(player_hand,dealer_hand)

		if player_hand.value > 21:
			player_busts(player_hand,dealer_hand,player_chip) #stoping the loop when player busts
			break

	if player_hand.value <= 21: #checking if player did not bust

		while dealer_hand.value < 17:

			hit(deck,dealer_hand) #Dealing cards to dealer

			show_all(player_hand,dealer_hand) #Show all cards

			if dealer_hand.value > 21:
				dealer_busts(player_hand,dealer_hand,player_chip)
			elif dealer_hand.value > player_hand.value:
				dealer_wins(player_hand,dealer_hand,player_chip)   #Running different game-end scenarios
			elif dealer_hand.value < player_hand.value:
				player_wins(player_hand,dealer_hand,player_chip)
			else:
				push(player_hand,dealer_hand)

	print("\nPlayer's winnings stant at: ", player_chip.total) #Informing about current chip count

	game_on = input("Would you like to keep playing (reply with y to play): ").lower()

	if game_on == 'y':
		playing = True
		continue
	else:
		print("Thanks for playing")
		break

