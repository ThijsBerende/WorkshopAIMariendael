from Candidate import Candidate
from Attempt import Attempt


class Maze:
    def __init__(self):
        """
        De constructor van het Maze object.
        Declareert de attributen van het doolhof, en geeft de beginstaat.
        """

        # Een attribuut waarin het doolhof wordt weergeven in een tweedimensionele lijst van string elementen.
        # In de beginstaat is er nog geen route uitgestippeld naar het eindpunt.
        self.maze = [
      ['█','█','█','█','█','█','█','█','█'],
      ['█','X','█',' ',' ',' ',' ','0','█'],
      ['█',' ','█',' ','█','█',' ',' ','█'],
      ['█',' ','█',' ','█','█','█',' ','█'],
      ['█',' ','█',' ',' ',' ','█',' ','█'],
      ['█',' ','█',' ','█',' ',' ',' ','█'],
      ['█',' ','█',' ','█','█','█',' ','█'],
      ['█',' ','█',' ',' ',' ','█',' ','█'],
      ['█',' ',' ',' ','█',' ',' ',' ','█'],
      ['█','█','█','█','█','█','█','█','█']]

        # Een attribuut waarin wordt weergeven welke posities van het doolhof al bezocht zijn.
        # In de beginstaat is alleen de startpositie bezocht.
        self.beenHere = [
      [" █ ", " █ ", " █ ", " █ ", " █ ", " █ ", " █ ", " █ ", " █ "],
      [" █ ", False, " █ ", False, False, False, False, True, " █ "],
      [" █ ", False, " █ ", False, " █ ", " █ ", False, False, " █ "],
      [" █ ", False, " █ ", False, " █ ", " █ ", " █ ", False, " █ "],
      [" █ ", False, " █ ", False, False, False, " █ ", False, " █ "],
      [" █ ", False, " █ ", False, " █ ", False, False, False, " █ "],
      [" █ ", False, " █ ", False, " █ ", " █ ", " █ ", False, " █ "],
      [" █ ", False, " █ ", False, False, False, " █ ", False, " █ "],
      [" █ ", False, False, False, " █ ", False, False, False, " █ "],
      [" █ ", " █ ", " █ ", " █ ", " █ ", " █ ", " █ ", " █ ", " █ "]]

    def __str__(self):
        """
        Bouwt een string object waarin het doolhof uitgebeeld wordt.

        :return: Het doolhof als string object.
        """
        string = ""
        for i in self.maze:
            for j in i:
                string = string + ("{}    ".format(j,end=""))
            string = string + "\n"
        return string

    def drawRoute(self, candidates, i):
        """
        Tekent vanaf de gegeven index 'i' het pad terug naar het starpunt in het doolhof door middel van recursie.

        :param candidates: De lijst van alle bekende mogelijke posities
        :param i: De index van het de positie waar je de weg naartoe wilt stippelen
        :return: De output van de maze.__str__() methode
        """
        if (i == 0):
            self.maze[candidates[i].row][candidates[i].col] = '0'
        else:
            self.drawRoute(candidates, candidates[i].parentCandidate)
            self.maze[candidates[i].row][candidates[i].col] = '.'
        return self.__str__()

    def isEndPoint(self, row, col):
        """
        Een functie die voor de meegegeven coordinaten kijkt of het de locatie van de haas is.

        :param row: De rij die meegegeven wordt bij het aanroepen van de functie.
                    (Een nummer tussen 0 en 8)
        :param col: De kolom die meegegeven wordt bij het aanroepen van de functie.
                    (Een nummer tussen 0 en 9)
        :return: True als op de positie een 'X' staat, anders False.
        """
        return self.maze [row][col] == 'X'

    def hasWall(self, row, col):
        """
        Een functie die voor de meegegeven coordinaten kijkt of er een muur (x) op die plek staat.

        :param row: De rij die meegegeven wordt bij het aanroepen van de functie.
                    (Een nummer tussen 0 en 8)
        :param col: De kolom die meegegeven wordt bij het aanroepen van de functie.
                    (Een nummer tussen 0 en 9)
        :return: True als het item in de maze op plek [row][col] overeenkomt met '█', anders False.
        """
        return self.maze [row][col] == '█'

    def visited(self, row, col):
        """
        Een functie die voor de meegegeven coordinaten de lijst beenHere aanpast naar True,
        om aan te geven dat het programma daar is geweest.

        :param row: De rij die meegegeven wordt bij het aanroepen van de functie.
                    (Een nummer tussen 0 en 8)
        :param col: De kolom die meegegeven wordt bij het aanroepen van de functie.
                    (Een nummer tussen 0 en 9)
        """
        self.beenHere[row][col] = True

    def hasVisited(self, row, col):
        """
        Een functie die voor de meegegeven coordinaten checkt of ze al eerder bezocht zijn.

        :param row: De rij die meegegeven wordt bij het aanroepen van de functie.
                    (Een nummer tussen 0 en 8)
        :param col: De kolom die meegegeven wordt bij het aanroepen van de functie.
                    (Een nummer tussen 0 en 9)
        :return: De waarde van de positie [row][col] in de lijst beenHere. True of False
        """
        return self.beenHere[row][col]

    def checkUp(self,candidates, c):
        """
        Een functie die kijkt of de plek boven de huidige positie mogelijk is.

        :param candidates: De lijst van alle bekende mogelijke posities
        :param c: De index van de huidige positie in de candidates lijst
        :return: True als de bekeken positie de eindpositie is, anders False
        """
        row = candidates[c].row - 1
        col = candidates[c].col

        return self.verifyCandidate(candidates,c, row, col)

    def checkDown(self,candidates, c):
        """
        Een functie die kijkt of de plek onder de huidige positie mogelijk is.

        :param candidates: De lijst van alle bekende mogelijke posities
        :param c: De index van de huidige positie in de candidates lijst
        :return: True als de bekeken positie de eindpositie is, anders False
        """
        row = candidates[c].row + 1
        col = candidates[c].col

        return self.verifyCandidate(candidates,c, row, col)


    def checkRight(self,candidates, c):
        """
        Een functie die kijkt of de plek rechts van de huidige positie mogelijk is.

        :param candidates: De lijst van alle bekende mogelijke posities
        :param c: De index van de huidige positie in de candidates lijst
        :return: True als de bekeken positie de eindpositie is, anders False
        """
        row = candidates[c].row
        col = candidates[c].col + 1

        return self.verifyCandidate(candidates,c, row, col)


    def checkLeft(self,candidates, c):
        """
        Een functie die kijkt of de plek links van de huidige positie mogelijk is.

        :param candidates: De lijst van alle bekende mogelijke posities
        :param c: De index van de huidige positie in de candidates lijst
        :return: True als de bekeken positie de eindpositie is, anders False
        """
        row = candidates[c].row
        col = candidates[c].col - 1

        return self.verifyCandidate(candidates,c, row, col)

    def verifyCandidate(self, candidates, c, row, col):
        """
        Een functie die kijkt of de meegegeven positie begaanbaar is,
        en die daarna bezoekt en toevoegd aan de candidates lijst.

        :param candidates: De lijst van alle bekende mogelijke posities
        :param c: De index van de huidige positie in de candidates lijst
        :param row: De rij van de mogelijke positie
        :param col: De kolom van de mogelijke positie
        :return: True als de bezochtte positie de eindpositie van het doolhof is, ander False
        """
        if (not self.hasWall(row, col) and not self.hasVisited(row, col)):
            self.visited(row, col)
            candidates.append(Candidate(row, col, c))

        return self.isEndPoint(row, col)