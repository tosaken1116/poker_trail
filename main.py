from curses import pair_number
import random as rd
import json
from sympy import true

mark = ["spade","heart","crab","diamond"]
number = [1,2,3,4,5,6,7,8,9,10,11,12,13]

used_cards = []
def choose_card() ->dict:
    global used_cards
    card = {"mark":rd.choice(mark),"number":rd.choice(number),"index":len(used_cards)}
    while(not card_check(card)):
        # print(card)
        card = {"mark":rd.choice(mark),"number":rd.choice(number),"index":len(used_cards)}
    used_cards.append(card)
    return card

def card_check(card)-> bool:
    global used_cards
    for used_card in used_cards:
        if used_card["mark"] == card["mark"] and used_card["number"] == card["number"]:
            return False
    return True

def choose_holding_cards(choose_number)->list:
    holding_cards = [[],[]]
    global used_cards
    for i in range(choose_number):
        card = choose_card()
        holding_cards.append(card)
        holding_cards[0].append(card["number"])
        holding_cards[1].append(card["mark"])
    return holding_cards

def check_card_duplicate(holding_cards) ->list:
    duplicate_checked_list = []
    holding_cards[0].sort()
    card_number_list = holding_cards[0]
    partition = 0
    for i in range(1,len(card_number_list)):
        before_number = [card_number_list[i-1]]
        after_number = [card_number_list[i]]
        if before_number != after_number:
            duplicate_checked_list.append(card_number_list[partition:i])
            partition = i
        if i+1 == len(card_number_list):
            duplicate_checked_list.append(card_number_list[partition:i+1])
    return duplicate_checked_list

def change_card(card):
    used_cards[card["index"]] = None
    return choose_card()

def royal_straight_frash_check(holding_cards):
    card_list = holding_cards[2:6]
    mark = card_list[0]["mark"]
    number = [10, 11, 12, 13, 1]
    for card in card_list:
        if card["mark"] != mark:
            return False
        if not card["number"] in number:
            return False
    return True

def check_card_change(holding_cards):
    print(holding_cards[2:6])
    if  (10 in holding_cards[0] and
        11 in holding_cards[0] and
        12 in holding_cards[0] and
        13 in holding_cards[0] and
        1 in holding_cards[0]):
        royal_straight_frash_bool = royal_straight_frash_check(holding_cards)
        if royal_straight_frash_bool:
            return holding_cards
    pair_card_list = check_card_duplicate(holding_cards)
    if len(pair_card_list) == 5:
        holding_cards[0] = []
        holding_cards[1] = []
        for i in range(5):
            changed_card = change_card()
            holding_cards.append(changed_card)
            holding_cards[0].append(changed_card["number"])
            holding_cards[1].append(changed_card["mark"])
        return holding_cards
    if (len(pair_card_list) == 4 or
        len(pair_card_list) == 3 or
        len(pair_card_list) == 2):
        change_card_list = combine_non_pair_card(pair_card_list)
        for change_card in change_card_list:
            for i in range(2,len(holding_cards)):
                if holding_cards[i]["number"] == change_card:
                    holding_cards[0].remove(holding_cards[i]["number"])
                    holding_cards[1].remove(holding_cards[i]["mark"])
                    holding_cards.remove(holding_cards[i])
                    holding_cards.append(change_card)
                    return holding_cards

    if len(pair_card_list) == 1:
        return holding_cards

def combine_non_pair_card(duplicated_pair_list):
    combined_array = []
    for array in duplicated_pair_list:
        if len(array) == 1:
            combined_array.append(array[0])
    return combined_array

def main():
    holding_cards = choose_holding_cards(5)
    holding_cards = check_card_change(holding_cards)
    print(holding_cards[2:6])

main()
# print(choose_holding_cards(5))
# print(royal_straight_frash_check([[1,1,2,3,4],[],{"mark": "heart","number":1},{"mark": "heart","number":10},{"mark": "heart","number":11},{"mark": "heart","number":12},{"mark": "heart","number":13}]))