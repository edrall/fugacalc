from flatlib import const
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

ELEMENTS = {const.FIRE, const.EARTH, const.WATER, const.AIR}

ELEMENT_OF_SIGN = {
    const.ARIES:        const.FIRE,
    const.TAURUS:       const.EARTH,
    const.GEMINI:       const.AIR,
    const.CANCER:       const.WATER,
    const.LEO:          const.FIRE,
    const.VIRGO:        const.EARTH,
    const.LIBRA:        const.AIR,
    const.SCORPIO:      const.WATER,
    const.SAGITTARIUS:  const.FIRE,
    const.CAPRICORN:    const.EARTH,
    const.AQUARIUS:     const.AIR,
    const.PISCES:       const.WATER
}

BAD_PLANETS = {
    const.PLUTO,
    const.SATURN,
    const.MARS
}

INTEREST_PLANETS = {
    const.MOON,
    const.MERCURY,
    const.VENUS,
    const.SUN,
    const.MARS,
    const.JUPITER,
    const.SATURN,
    const.NEPTUNE,
    const.URANUS,
    const.PLUTO
}

BAD_ASPECTS = {
    90, 270, # kvadratures
    150, 210 # kvinkunxs
}

INTEREST_OBJECTS = [
    const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS,
    const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO]

class MagicChart(Chart):
    def __init__(self, date: Datetime, pos: GeoPos):
        Chart.__init__(self, date, pos, IDs=INTEREST_OBJECTS)

    def lonInRange(self, what: float, left: float, right: float):
        l = left + 180
        r = right + 180
        w = what + 180
        return bool(l < w < r)

    def find_borders(self, lon: float):
        w = lon +180
        borders = list(h.lon + 180 for h in self.houses) + list(x * 30 + 180 for x in range(13))
        left =  max(b for b in borders if b < w)
        right = min(b for b in borders if b > w)
        return left - 180, right - 180

    def fixTo360(self, lon: float):
        return lon
    def canElement(self, elm):
        # input validation
        if (elm not in ELEMENTS):
            return False
        # The ninth house in element
        if bool(ELEMENT_OF_SIGN[self.get(const.HOUSE9).sign] != elm):
            return False
        # no bad planet in the sign of ninth house
        l = const.LIST_SIGNS.index(self.get(const.HOUSE9).sign) * 30
        r = l + 30
        if any(self.lonInRange(self.get(p).lon, l, r) for p in BAD_PLANETS):
            return False
        # no bad aspects on the ninth house
        h9 = self.get(const.HOUSE9).lon
        for p in INTEREST_PLANETS:
            l, r = self.find_borders(self.get(p).lon)
            w = ((h9 + a) % 360 for a in BAD_ASPECTS)
            return any(self.lonInRange(a, l, r) for a in w)
        return True