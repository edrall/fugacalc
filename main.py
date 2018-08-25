from MagicChart import MagicChart, ELEMENTS

from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

from datetime import datetime, timedelta

MOST = GeoPos('50n50', '13e64')
ROZTOKY = GeoPos('50n17', '14e38')

dNow = datetime.now()

elmStarted = False
elmStartD = dNow
for d in (dNow + timedelta(minutes=1 * i) for i in range(60*24*60)):
    date = Datetime(d.__format__('%y/%m/%d'), d.__format__('%H:%M'), '+2:00')
    pos = GeoPos('50n50', '13e64')
    chart = MagicChart(date, ROZTOKY)
    for elm in ELEMENTS:
        if chart.canElement(elm):
            if not elmStarted:
                elmStarted = True
                elmStartD = d
                elmStart = elm
        else:
            if elmStarted and elm == elmStart:
                print('{:<10} {:02d}.{:02d}.{:04d} {:02d}:{:02d}-{:02d}:{:02d} ({:<3} min.)'.format(
                                elm,
                                elmStartD.day, elmStartD.month, elmStartD.year, elmStartD.hour, elmStartD.minute,
                                d.hour, d.minute,
                                (d - elmStartD).seconds//60
                             ))
                elmStarted = False
                







