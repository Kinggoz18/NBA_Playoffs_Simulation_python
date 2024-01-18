class Team:
    # Default constructor
    def __init__(self):
        self.playoffsPoints = 0
        self.playoffsWins = 0
        self.playoffsLosses = 0
        self.winRate = []
        self.name = ""
        self.mean_pts = 0
        self.sd_pts = 0
        self.mean_opp = 0
        self.sd_opp = 0

    # Resets the series variables
    def Reset(self):
        self.playoffsPoints = 0
        self.playoffsWins = 0
        self.playoffsLosses = 0

