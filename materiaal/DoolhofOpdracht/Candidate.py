class Candidate:
    def __init__(self, row, col, parentCandidate):
        """
        Een object dat een berijkbaar vak in het doolhof aangeeft aan de hand van row(rij) en col(kolom) posities
        :param row: De rij waarin het vak zich bevindt  (hoogte)
        :param col: De kolom waarin het vak zich bevindt (breedte)
        :param parentCandidate: Het aanliggende vak waaruit het mogelijke vak bereikt is.
        """
        self.row = row
        self.col = col
        self.parentCandidate = parentCandidate
