from Maze import Maze
from Candidate import Candidate


def depthFirst(candidates):
    """
    //TODO: Implementeer een depth first algoritme wat in een while loop
            vanaf de startpositie mogelijke zetten evalueert om de snelste route naar
            het eindpunt te vinden met gebruik van de 'last in first out' methodiek.
            .
            Als het eindpunt van het doolhof is bereikt moet de while loop eindigen,
            en moet de gevonden route uitgeprint worden,
            dit kan met behulp van de maze.drawRoute() methode
    :param candidates: Een lijst met daarin alle bekende posities in het doolhof tot nu toe.
    :return: Een string met de uitgestippelde route door het doolhof.
    """
    while True:
    #   Your code here
        break

    return ""

def breadthFirst(candidates):
    """
    //TODO: Implementeer een breadth first algoritme wat in een while loop
            vanaf de startpositie mogelijke zetten evalueert om de snelste route naar
             het eindpunt te vinden met gebruik van de 'first in first out' methodiek.
             .
             Als het eindpunt van het doolhof is bereikt moet de while loop eindigen,
             en moet de gevonden route uitgeprint worden,
             dit kan met behulp van de maze.drawRoute() methode
    :param candidates: Een lijst met daarin alle bekende posities in het doolhof tot nu toe.
    :return: Een string met de uitgestippelde route door het doolhof.
        """
    while True:
    #   Your code here
        break

    return ""



if __name__ == '__main__':
    # Declaratie van een nieuw (leeg) maze object.
    maze = Maze()
    print(maze)

    # Declaratie van een lijst candidaten, met daarin de startpositie
    candidates = [Candidate(1, 7, -1)]

    print(depthFirst(candidates))

    # Declaratie van een nieuw (leeg) maze object.
    maze = Maze()

    # Declaratie van een lijst candidaten, met daarin de startpositie
    candidates = [Candidate(1, 7, -1)]

    # Deze variablen declareren we opnieuw om de waardes te resetten

    print(breadthFirst(candidates))

    # Om te visualiseren welke posities de algoritmes hebben bekeken,
    # voeg de volgende regels code toe aan de zoek algoritmes:
    """
    for i in maze.beenHere:
        print(i)
    """