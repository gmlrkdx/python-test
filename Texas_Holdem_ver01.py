import random as r
import numpy as np
from collections import Counter

players = 2
#= int(input("게임을 할 플레이어 수를 입력하세요:\n"))
#players_num : 플레이어 인원수

cards = np.random.choice(52, (5+ players * 2, ), replace= False)
#cards = 52장 카드 구현

raw_Suit = np.floor_divide(cards, 13)
raw_Rank = np.mod(cards, 13)
#raw_ : 컴퓨터가 인지하는 카드 형식

Suit = raw_Suit #0~3
Rank = raw_Rank #0~12
#플레이어 인식용 카드 형식

Suit = Suit.astype("object") #플레이어 인식용 무늬 구현
Suit[Suit == 0] = "♠"
Suit[Suit == 1] = "♥"
Suit[Suit == 2] = "♦"
Suit[Suit == 3] = "♣"

Rank += 1 #플레이어 인식용 숫자 구현
Rank = Rank.astype("object")
Rank[Rank == 1] = "A"
Rank[Rank == 11] = "J"
Rank[Rank == 12] = "Q"
Rank[Rank == 13] = "K"

Field_cards = np.vstack((Suit, Rank)) #플레이어 인식 카드 2차원화 
# 0  1 2 3  4 5 6 7 8 
# 공 공 공 공 공 A A B B : 문양 suit
# 공 공 공 공 공 A A B B : 숫자 rank

#카드 시각화
 
#홀카드
print("플레이어 1의 홀카드:", end=" ")
for i in range(5,7):
    print(f"{Field_cards[0, i]}{Field_cards[1, i]}", end=" ")
print("\n")

print("커뮤니티 카드:", end=" ")
for i in range(0,3):
    print(f"{Field_cards[0, i]}{Field_cards[1, i]}", end=" ")
print("\n")

print("커뮤니티 카드:", end=" ")
for i in range(0,4):
    print(f"{Field_cards[0, i]}{Field_cards[1, i]}", end=" ")
print("\n")

print("커뮤니티 카드:", end=" ")
for i in range(0,5):
    print(f"{Field_cards[0, i]}{Field_cards[1, i]}", end=" ")
print("\n")

print("세븐 카드:", end=" ")
for i in range(0,7):
    print(f"{Field_cards[0, i]}{Field_cards[1, i]}", end=" ")
print("\n")

ip_cards = np.vstack((raw_Suit, raw_Rank)) #게임 분석 카드 2차원화
# 0  1 2 3  4 5 6 7 8 
# 공 공 공 공 공 A A B B : 문양 suit
# 공 공 공 공 공 A A B B : 숫자 rank

#is_ 함수에서 사용하는 매개변수들
#raw_Player_cards_rank = 판정하는 플레이어의 카드 숫자
#raw_Player_cards_suit = 판정하는 플레이어의 카드 문양

def get_player_card(players_num): #판정 함수에 사용되는 카드 플레이어별 지정
    if players_num == 1:
        raw_Player_cards_suit = ip_cards[0, np.r_[0:5, 5:7]]
        raw_Player_cards_rank = ip_cards[1, np.r_[0:5, 5:7]]

    if players_num == 2:
        raw_Player_cards_suit = ip_cards[0, np.r_[0:5, 7:9]]
        raw_Player_cards_rank = ip_cards[1, np.r_[0:5, 7:9]]

    return(raw_Player_cards_suit, raw_Player_cards_rank)

def is_Straight(players_num): #스트레이트 판정 함수

    _, raw_Player_cards_rank = get_player_card(players_num)

    raw_Player_cards_rank = sorted(set(raw_Player_cards_rank)) #중복 제거 및 내림차순

    if 0 in raw_Player_cards_rank:
            raw_Player_cards_rank.append(13) # A 10 J Q K와 같은 스트레이트 구현

    for i in range(len(raw_Player_cards_rank)-4):
        if raw_Player_cards_rank[i+4] - raw_Player_cards_rank[i] == 4:

            return True, raw_Player_cards_rank[i+4] #참, 같은 족보일 경우 벨류 체크
        
    return False, None

def final_value(players_num):
    target = [0, 9, 10, 11, 12]
    straight_check, _ = is_Straight(players_num)
    raw_Player_cards_suit, raw_Player_cards_rank = get_player_card(players_num)
    suit_counter = Counter(raw_Player_cards_suit)
    rank_counter = Counter(raw_Player_cards_rank)
    
    if straight_check and np.all(np.isin(target, raw_Player_cards_rank)):
        Player_values = 1 #로얄스트레이트 플러쉬

    elif straight_check and max(suit_counter.values()) >=5: #스트레이프 플러쉬 : 같은 모양, 스트레이트
        Player_values = 2
        
    elif 4 in rank_counter.values(): #포카드 : 같은 숫자 4개
        Player_values = 3

    elif 3 in rank_counter.values() and 2 in rank_counter.values(): #풀하우스 : 같은 숫자 3개 2개
        Player_values = 4
    
    elif max(suit_counter.values()) >= 5 : #플러쉬 : 같은 모양 5개
        Player_values = 5

    elif straight_check: #스트레이트 : 스트레이트
        Player_values = 6
    
    elif 3 in rank_counter.values(): #트리플 : 같은 숫자 3개
        Player_values = 7
    
    elif list(rank_counter.values()).count(2) == 2: #투페어 : 같은 숫자 2개가 2개
        Player_values = 8

    elif 2 in rank_counter.values(): #원페어 : 같은 숫자 2개
        Player_values = 9

    else:
        Player_values = 10

    return Player_values

Player1_values = final_value(1)

Player2_values = final_value(2)

if Player1_values < Player2_values:
    print(Player1_values, Player2_values)
    print("1")

elif Player1_values > Player2_values:
    print(Player1_values, Player2_values)
    print("2")

else:
    print("동점 ㅋㅋ")