# Игра - Камень, ножницы, бумага, ящерица, спок.
import random
moves = ["бумага", "ножницы", "камень", "ящерица", "спок"]
moves_and_wins = {
    "камень": ["ножницы", "ящерица"],
    "ножницы": ["бумага", "ящерица"],
    "бумага": ["камень", "спок"],
    "ящерица": ["бумага", "спок"],
    "спок": ["камень", "ножницы"]
}

player_wins = 0
computer_wins = 0
play_again = "да"

while play_again == "да":
    computer_move = random.choice(moves)
    player_move = input("Камень, ножницы, бумага, ящерица, спок? ")

    if computer_move in moves_and_wins[player_move]:
        print("Компьютер выбрал ", computer_move, ", вы победили!")
        player_wins = player_wins + 1
    elif player_move == computer_move:
        print("У вас ничья!")
    else:
        print("Компьютер выбрал ", computer_move, " вы проиграли!")
        computer_wins = computer_wins + 1
    print("Компьютер - ", computer_wins, ", игрок - ", player_wins)
    play_again = input("Сыграем еще? ")

print("Игра заверешена, приходите еще!")
