from enum import IntEnum

class Entity(IntEnum):

    # Components of the world
    TERRAIN = 1
    MAGIC_TERRAIN = 2
    CONWAY_CUBE = 3
    TREE = 4
    COLORFUL_TERRAIN = 5
    RABBIT = 10

    @classmethod
    def is_terrain(cls, entity):
        """Method to check if the given value is TERRAIN."""
        match entity:
            case Entity.TERRAIN:
                return True
            case Entity.MAGIC_TERRAIN:
                return True
            case Entity.COLORFUL_TERRAIN:
                return True
            case Entity.CONWAY_CUBE:
                return True
            case _:
                return False