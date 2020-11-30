import pandas as pd


class MarkerReader2:
    def __init__(self, marker_filename, final_frame):
        self.df = pd.read_csv(marker_filename)
        # self.markers = self.convert_markers(self.df["Attacco"].tolist(), fps)
        self.markers = self.df['0'].to_numpy()
        self.markers = self.markers+1
        self.markers = list(self.markers)

        if self.markers[0] != 0:
            self.markers = [0] + self.markers
        if self.markers[-1] is not final_frame:
            self.markers = self.markers + [final_frame]

        self.numMarkers = len(self.markers)



