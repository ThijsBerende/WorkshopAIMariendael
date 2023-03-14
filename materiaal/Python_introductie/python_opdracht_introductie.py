"""
    welkom bij deze introductie/herhaling van de programmeertaal Python,
    Deze korte opdrachten zijn bedoeld om er voor te zorgen dat je (weer) bekend raakt
    met de meeste gebruikte functies van Python

    Als je er niet uit komt, klaar bent, of andere vragen hebt, laat het ons weten,
    Wij zullen zoveel mogelijk rondlopen en helpen!
"""

def strings():
    """
        1.1 maak een een variable aan voor een string en print deze uit met print()
        1.2 maak nog een string aan, en voeg deze toe aan de vorige string, print het resultaat
    """





"""
1.3 vind de fouten in de volgende regels:
print ( " Een boodschap " ).

print ( " Een boodschap ')

print ( ' Een boodschap " ' )




"""




def rekenen_met_integers():
    """
        Je hebt een driehoek met een hoogte van 3 en een breedte van 4, gebruik de stelling van
        Pythagoras(A^2 + B^2 = C^2) en Python om te berekenen wat de lengte van de schuine zijde is.

        2.1 Maak eerst variablen aan voor alle drie de zijdes van de driehoek
        2.2 Vul de formule in
        2.3 print de lengte van de schuine zijde
    """




def waar_of_niet_waar():
    """
      vervang de komma in de volgende prints om het kloppend te maken
      je kunt and, or en not gebruiken

    """
    a = True
    b = False


    print(a , b == False)
    print(a, b == True)
    #print(, a == False)


def lists():
    """
        4.1 creeër een list()
        4.2 vul de list met minstens 2 getallen
        4.3 voeg het eerste element van de lijst toe aan de laatste
        4.4 sla het resultaat op in een variable en print dit uit
    """

def tuples():
    """
        5.1 creeër een tuple met daarin een integer en een string
        5.2 print de tweede variable in de tuple
        5.3 probeer de waarde van een van beide variables in de string te veranderen, wat gaat er mis?

    """


def if_else():
    """
        6.1 maak een Boolean met als waarde True
        6.2 maak een if-else-statement die alleen waar is als je Boolean False is
        6.3 print "De Boolean is niet waar" als je in de if-statement komt
        6.4 print "De boolean is waar" als je in de else-statement komt
    """


def for_loops():
    """
        7.1 maak een for-loop die tien keer "hello world" uitprint
        7.2 maak een variable genaamd resultaat, en maak de waarde 0
        7.3 tel elke keer de waarde van loop op bij de waarde van resultaat
        7.4 print het resultaat uit als de loop klaar is
    """


def while_loops():
    """
        8.1 maak een Boolean aan genaamd ga_door met als waarde True en een Integer genaamd teller met als waarde 0
        8.2 creeër een while-loop die stop als ga_door niet meer waar is
        8.3 creeër een if-statement die kijkt of teller groter of gelijk aan 7 is
        8.4 maak ga_door False als de if-statement waar is
        8.5 maak teller 1 hoger als de if-statement niet waar is en print daarna teller
    """


"""
    8.6 wat denk je dat er gebeurd als je while True gebruikt?
    
    
"""


def voer_functies_uit():
    strings()
    rekenen_met_integers()
    waar_of_niet_waar()
    lists()
    tuples()
    if_else()
    for_loops()
    while_loops()


if __name__ == '__main__':
    voer_functies_uit()
