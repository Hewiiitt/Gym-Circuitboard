class Colors:

    _colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (0, 0, 112),
        (0, 112, 0),
        (112, 0, 0),
        (112, 112, 0),
        (0, 112, 112),
        (112, 0, 112),
    ]

    def __getitem__(self, item):
        return self._colors[item]
