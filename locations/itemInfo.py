import typing
from checkMetadata import checkMetadataTable


class ItemInfo:
    OPTIONS = []
    MULTIWORLD = False

    def __init__(self, room=None):
        self.item = None
        self._location = None
        self.room = room
        self.metadata = checkMetadataTable.get(self.nameId, checkMetadataTable["None"])
        self.forced_item = None

    @property
    def location(self):
        return self._location

    def setLocation(self, location):
        self._location = location

    def getOptions(self):
        return self.OPTIONS

    def configure(self, options):
        if options.dungeon_items in {'localkeys', 'localnightmarekey', 'keysanity'}:
            # Add items that can be anywhere due to dungeon items setting
            self.OPTIONS = self.OPTIONS.copy()
            for n in range(10):
                self.OPTIONS += ["MAP%d" % (n), "COMPASS%d" % (n), "STONE_BEAK%d" % (n)]
                if options.dungeon_items in {'localnightmarekey', 'keysanity'}:
                    self.OPTIONS += ["KEY%d" % (n)]
                if options.dungeon_items == 'keysanity':
                    self.OPTIONS += ["NIGHTMARE_KEY%d" % (n)]

        if self._location.dungeon is not None and options.dungeon_items in {'standard', 'localkeys', 'localnightmarekey', 'keysy'}:
            # Add items specific to this dungeon
            self.OPTIONS = self.OPTIONS.copy()
            d = self._location.dungeon
            if options.dungeon_items in {'standard', 'keysy'}:
                self.OPTIONS += ["MAP%d" % (d), "COMPASS%d" % (d), "STONE_BEAK%d" % (d)]
            if options.dungeon_items in {'standard', 'localkeys'}:
                self.OPTIONS += ["KEY%d" % (d)]
            self.OPTIONS += ["NIGHTMARE_KEY%d" % (d)]

    def read(self, rom):
        raise NotImplementedError()

    def patch(self, rom, option, *, multiworld=None):
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__
    
    @property
    def nameId(self):
        return "0x%03X" % self.room if self.room is not None else "None"
