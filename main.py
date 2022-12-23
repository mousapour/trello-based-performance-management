from trello import TrelloClient, Member
import time
import csv
import datetime


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def get_consumed_points(card_name):
    p1 = card_name.find('(')
    p2 = card_name.find(')')
    b1 = card_name.find('[')
    b2 = card_name.find(']')

    if p2 > p1:
        p1, p2 = p2, p1
    if b2 > b1:
        b1, b2 = b2, b1

    if b1 > -1 and b2 > -1 and is_number(card_name[b2 + 1:b1]):
        consumed_time = float(card_name[b2 + 1:b1])
        # print(consumed_time)
    else:
        consumed_time = 0
        # print('in kart [] ro ghalat dare: ' + card_name)

    if p1 > -1 and p2 > -1 and is_number(card_name[p2 + 1:p1]):
        estimated_time = float(card_name[p2 + 1:p1])
        # print(estimated_time)
    else:
        estimated_time = 0
        # print('in kart () ro ghalat dare: ' + card_name)

    return consumed_time, estimated_time


def print_all_boards(client):
    print('\nall boards:\n')
    all_boards = client.list_boards()
    for board in all_boards:
        print(board.name + ': ' + board.id)
    print('\n')


def print_all_lists_in_board(board):
    print('all lists in ' + board.name + ':\n')
    for list_ in board.list_lists():
        print(list_.name + ': ' + list_.id)
    print('\n')


def all_cards_of_member_in_board(member, board, list_id=-1, label=-1):
    cards = []
    if list_id == -1 and label == -1:
        for card in member.fetch_cards():
            if card['idBoard'] == board.id:
                cards.append(card)
    elif list_id != -1 and label == -1:
        for card in member.fetch_cards():
            if card['idBoard'] == board.id and card['idList'] == list_id:
                cards.append(card)
    elif list_id != -1 and label != -1:
        for card in member.fetch_cards():
            if card['idBoard'] == board.id and card['idList'] == list_id and label in card['idLabels']:
                cards.append(card)

    return cards


def total_consumed_and_estimated_time_for_member(member, board, my_list, label=-1):
    cards = all_cards_of_member_in_board(member, board, my_list, label)
    consumed_time = 0
    estimated_time = 0
    for card in cards:
        ct, et = get_consumed_points(card['name'])
        consumed_time += ct
        estimated_time += et
        # print(card)
    return consumed_time, estimated_time


def write_in_csv(name, data, header):
    with open(name, mode='w+') as report_file:
        report_writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        report_writer.writerow(header)
        for row in data:
            report_writer.writerow(row)


def get_all_labels_in_board(board):
    labels_raw = board.get_labels()
    labels = {}
    for label in labels_raw:
        labels[label.id] = label.name
    return labels


class Card:
    def __init__(self, card):
        self.id = card['id']
        self.description = card['desc']
        self.idBoard = card['idBoard']
        self.idList = card['idList']
        self.idMembers = card['idMembers']
        self.labels_information = card['labels']
        self.name = card['name']
        labels = []
        for label in self.labels_information:
            labels.append(label['name'])
        self.lables = labels.copy()
        del labels
        self.consumed_time, self.estimated_time = get_consumed_points(self.name)

    def __repr__(self):
        print('card name: ' + self.name)
        print('label(s): ' + str(self.lables))
        print('cons. time, est. time: (' + str(self.consumed_time) + ', ' + str(self.estimated_time) + ')')

        return ''





start = time.time()

client = TrelloClient(
    api_key='your-api-key',
    token='your-token')

# BOARD_ID = ''  Performance Management:
BOARD_ID = 'your-board-id'
# LIST_ID = 'your-list-id'

# print_all_boards(client)

all_boards = client.list_boards()
board = all_boards[0]
# board = all_boards[2]

# print_all_lists_in_board(board)

lists = board.list_lists()
my_list = lists[5]
# my_list = board.get_list('your-list')

members = board.all_members()
labels = get_all_labels_in_board(board)

# for a in members:
#     print(a.full_name)

# print(members[3].fetch_cards()[0])

############################################################

reza = []
for card in members[3].fetch_cards():
    new_card = Card(card)
    if new_card.idBoard == BOARD_ID:
        reza.append(new_card)

# print(reza[2])

# print(*board.get_labels(), sep='\n')

all_lables = []
for l in board.get_labels():
    all_lables.append(l.name)

# print(*all_lables, sep='\n')
#
wanted = [['Bug'], ['Unplanned', 'Non-OKR'], ['Unplanned', 'OKR'], ['OKR', 'Back-End'], ['OKR', 'Front-End']]
# for card in board.get_cards():

a = board.get_cards(card_filter='closed')
print(len(a))
total = 0
dic = {}
# for b in a:
#     if b.idMembers:
#         # date = b.created_date[:10].split('-')
#         # print(str(b.created_date)[:10])
#         y1, m1, d1 = [int(x) for x in str(b.date_last_activity)[:10].split('-')]
#         b1 = datetime.date(y1, m1, d1)
#         if b1 > datetime.date(2019, 3, 22):
#             total += 1
#             c = client.get_member(b.idMembers[0]).full_name
#             if c not in dic.keys():
#                 dic[c] = 1
#             else:
#                 dic[c] += 1
# print(total)
# print(dic)

for b in a:
    y1, m1, d1 = [int(x) for x in str(b.date_last_activity)[:10].split('-')]
    b1 = datetime.date(y1, m1, d1)
    if b1 > datetime.date(2019, 6, 22):
        total += 1
print(total)



end = time.time()

print('time: ' + str((end - start)))





# data = []
# for member in members:
#     consumed_time, estimateD_time = total_consumed_and_estimated_time_for_member(member, board, my_list.id)
#     data.append([member.full_name, consumed_time, estimateD_time])
#     print(member.full_name + ':\n' + 'consumed_time:' + str(consumed_time) + '\n' + 'estimateD_time:' + str(estimateD_time) + '\n')
#
# write_in_csv('report.csv', data, ['name', 'consumed_time', 'estimated_time'])


# print('board name: ' + board.name)
# print_all_lists_in_board(board)
# total = []
# for member in members:
#     ct_total = []
#     et_total = []
#     for label in labels.keys():
#         consumed_time, estimateD_time = total_consumed_and_estimated_time_for_member(member, board, my_list.id, label)
#         ct_total.append(consumed_time)
#         et_total.append(estimateD_time)
#     temp = [member.full_name]
#     temp.extend(ct_total)
#     temp.extend(et_total)
#     total.append(temp)
#     # print(temp)
# header = [s + ' consumed' for s in labels.values()]
# header.extend([s + ' estimated' for s in labels.values()])
# write_in_csv('full report.csv', total, header)


