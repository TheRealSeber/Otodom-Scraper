class Building:
    def __init__(self, properties: dict):
        self.type: str | None = properties.get("Building_type", [None])[0]
        self.floors: str | None = properties.get("Building_floors_num", [None])[0]
        self.build_year: int | None = properties.get("Build_year", None)

    def to_dict(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}
