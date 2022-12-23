from trello import TrelloClient, Member
import time
import csv
import datetime

def get_all_labels_in_board(board):
    labels_raw = board.get_labels()
    labels = {}
    for label in labels_raw:
        labels[label.id] = label.name
    return labels

start = time.time()

BOARD_ID = 'your-board-id'
client = TrelloClient(
    api_key='your-api-key',
    token='your-token')


all_boards = client.list_boards()
board = all_boards[0]
members = board.all_members()
labels = get_all_labels_in_board(board)

wanted = [['Bug'], ['Unplanned', 'Non-OKR'], ['Unplanned', 'OKR'], ['OKR', 'Back-End'], ['OKR', 'Front-End']]
from_date = datetime.date(2019, 10, 1)

# cards = board.get_cards(card_filter='all')
# print(len(cards))
# hazfi = []
# for ind in range(len(cards)):
#     year_last_activity, month_last_activity, day_last_activity = [int(x) for x in str(cards[ind].card_created_date)[:10].split('-')]
#     date_last_activity = datetime.date(year_last_activity, month_last_activity, day_last_activity)
#     if date_last_activity < from_date:
#         hazfi.append(ind)
# print(len(hazfi))
# mosleh = 0
# for ind in hazfi:
#     del cards[ind - mosleh]
#     mosleh += 1
# print(len(cards))
# board.get_list().ca

for listt in board.get_lists('all'):
    print(listt)











end = time.time()
print('time: ' + str((end - start)))




