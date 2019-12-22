import sys
import re

class Dealer:
	def __init__(self, size, file_str = None):
		self.size = size
		self.deck = [card for card in range(size)]

		if file_str:
			self.read_instructions(file_str)

	def print_deck(self):
		for i in range(self.size):
			print('%d ' % i, end='')
		print('\n', end='')

		for i in range(self.size):
			print('%d ' % self.deck[i], end='')
		print('\n', end='')

	def deal_into_stack(self):
		self.deck.reverse()

	def deal_with_increment(self, inc):
		print('Inc %d' % inc)
		cur_pos = 0
		new_deck = [None for card in self.deck]

		for card in self.deck:
			new_deck[cur_pos] = card
			cur_pos += inc

			while cur_pos >= self.size:
				cur_pos -= self.size

		self.deck = new_deck

	def cut_deck(self, amount):
		print('Cut %d' % amount)
		new_deck = []

		front = self.deck[:amount]
		back = self.deck[amount:]

		self.deck = [card for card in back]
		self.deck.extend([card for card in front])

	def read_instructions(self, file_str):
		with open(file_str) as file:
			for line in file.readlines():
				m_deal_into_stack = re.match('(deal into new stack)', line)
				m_deal_with_inc = re.match('(deal with increment )(-{0,1}[0-9]+)', line)
				m_cut_deck = re.match('(cut )(-{0,1}[0-9]+)', line)

				if m_deal_into_stack:
					self.deal_into_stack()
				elif m_deal_with_inc:
					inc = int(m_deal_with_inc.group(2))
					self.deal_with_increment(inc)
				elif m_cut_deck:
					cut = int(m_cut_deck.group(2))
					self.cut_deck(cut)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('No File Given')
	elif len(sys.argv) < 3:
		print('No Size Given')
	else:
		file = sys.argv[1]
		size = int(sys.argv[2])

		dealer = Dealer(size)
		dealer.read_instructions(file)
	
		for i, card in enumerate(dealer.deck):
			if card == 2019:
				print(i)
				break