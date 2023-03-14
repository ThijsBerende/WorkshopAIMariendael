def print_board(board):
    """
    Deze functie print het speelbord op een duidelijke manier
    """
    print("-------------")
    print("| " + board[0] + " | " + board[1] + " | " + board[2] + " |")
    print("-------------")
    print("| " + board[3] + " | " + board[4] + " | " + board[5] + " |")
    print("-------------")
    print("| " + board[6] + " | " + board[7] + " | " + board[8] + " |")
    print("-------------")


def check_win(board, player):
    """
    Dit is een functie die gegeven de speler, checkt of deze speler heeft gewonnen.
    """
    if (board[0] == player and board[1] == player and board[2] == player) or \
       (board[3] == player and board[4] == player and board[5] == player) or \
       (board[6] == player and board[7] == player and board[8] == player) or \
       (board[0] == player and board[3] == player and board[6] == player) or \
       (board[1] == player and board[4] == player and board[7] == player) or \
       (board[2] == player and board[5] == player and board[8] == player) or \
       (board[0] == player and board[4] == player and board[8] == player) or \
       (board[2] == player and board[4] == player and board[6] == player):
        return True

    else:
        return False

def minimax(board, is_maximizing):
    """
    Het minimax algoritme is een manier van bepalen welke move het beste is om te maken gebaseerd op een recursieve formule.

    Een recursieve functie bestaat uit 2 delen, de basis situatie en de recursieve situatie.
    De basis situatie hebben we alvast voor jullie gemaakt. Deze zorgt ervoor dat zodra het potje voorbij is, hij niet
    dieper zoekt.

    Dan de recursie stap, deze moeten jullie zelf creëeren. Het idee van deze stap is dat hij rekening houdt met welke speler
    hij is, en vanuit daar alle moves probeert en van deze de toekomst weer evalueert door deze zelfde functie nog een keer
    te gebruiken. Zo simuleert hij een game tot het einde en kan hij uitvinden met welke move de uitkomst optimaal is.

    """
    # Basis stap

    if check_win(board, "X"):
        return -1
    elif check_win(board, "O"):
        return 1
    elif " " not in board:
        return 0

    # Recursieve stap
    # Hier jouw code
    return 0



def find_best_move(board):
    """
    Deze functie gebruikt de minmaxfunctie om de beste move voor de computer te berekenen. Hij kijkt naar bij welke move
    de evaluatie van de toekomst het beste is, en geeft de index van deze move terug aan de main functie. Hier hoef je
    niks aan aan te passen
    """
    best_score = -float("inf")
    best_move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    return best_move


def tic_tac_toe():
    """
    Dit is de main functie die de game runt. Hij laat jou(de speler) en move kiezen en speelt dan de beste robot move die
    hij doorkrijgt van de andere functies. Hij doet dit om en om tot het spel is afgelopen. Hier hoef je niks aan aan te
    passen.
    :return:
    """
    board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
    player = "X"
    game_over = False

    print("Welkom bij Boter Kaas en Eieren!")
    print_board(board)

    while not game_over:
        if player == "X":
            position = int(input("Voer een getal in tussen 1 en 9: ")) - 1
            if board[position] != " ":
                print("Die positie is al bezet, probeer een ander vakje!")
                continue
        else:
            position = find_best_move(board)
            print("Computer kiest een zet!", position + 1)

        board[position] = player
        print_board(board)

        if check_win(board, player):
            print(player + " heeft gewonnen!")
            game_over = True
        elif " " not in board:
            print("Gelijkspel!")
            game_over = True
        else:
            player = "O" if player == "X" else "X"

    replay = input("Wil je opnieuw spelen? (Y/N): ")
    if replay.upper() == "Y":
        tic_tac_toe()
    else:
        print("Bedankt voor het spelen!")

# Dit is de main
tic_tac_toe()
