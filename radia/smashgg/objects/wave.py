class Wave:
    def __init__(self, wave_data: dict):
        self._raw = wave_data
        self.id: int = self._raw.get("id", None)
        self.identifier = self._raw.get("identifier", "")

