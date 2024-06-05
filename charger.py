from typing import List


class GeoCoord:
    def __init__(self, lat, lng):
        self.lat = float(lat)
        self.lng = float(lng)

class Charger:
    def __init__(self, name, addr, coord, state, type, parking, limit, limit_detail, note, output, method):
        self.name: str = name
        self.addr: str = addr
        self.coord: GeoCoord = coord
        self.state: str = state
        self.type: str = type
        self.parking: str = parking
        self.limit: str = limit
        self.limit_detail: str = limit_detail
        self.note: str = note
        self.output: str = output
        self.method: str = method

    def getState(self):
        if self.state == '0':
            return '알수없음'
        elif self.state == '1':
            return '통신이상'
        elif self.state == '2':
            return '사용가능'
        elif self.state == '3':
            return '충전중'
        elif self.state == '4':
            return '운영중지'
        elif self.state == '5':
            return '점검중'
        else:
            return '미확인'

    def getType(self):
        if self.type == '01':
            return 'DC차데모'
        elif self.type == '02':
            return 'AC완속'
        elif self.type == '03':
            return 'DC차데모+AC3상'
        elif self.type == '04':
            return 'DC콤보'
        elif self.type == '05':
            return 'DC차데모+DC콤보'
        elif self.type == '06':
            return 'DC차데모+AC3상+DC콤보'
        elif self.type == '07':
            return 'AC3상'
        elif self.type == '08':
            return 'DC콤보(완속)'
        elif self.type == '89':
            return "H2"
        else:
            return '기타'
        
    def getParking(self):
        if self.parking == 'Y':
            return '무료'
        elif self.parking == 'N':
            return '유료'
        else:
            return '미확인'
        
    def getLimit(self):
        if self.limit == 'Y':
            return '제한: ' + self.limit_detail
        elif self.limit == 'N':
            return '무제한'
        else:
            return '미확인' + self.limit_detail
        
    def getOutput(self):
        return self.output + 'kW'
    



class ChargerGroup:
    def __init__(self, addr, chargers: List[Charger] = []):
        self.addr: str = addr
        self.names = set()
        self.chargers: List[Charger] = []
        self.available: int = 0
        self.occupied: int = 0

    def addCharger(self, charger: Charger):
        self.chargers.append(charger)
        self.names.add(charger.name)
        if charger.getState() == '사용가능':
            self.available += 1
        elif charger.getState() == '사용중':
            self.occupied += 1

    def getNames(self):
        return ', '.join(self.names)

    def getAverageCoord(self) -> GeoCoord:
        lat = 0
        lng = 0

        for charger in self.chargers:
            lat += charger.coord.lat
            lng += charger.coord.lng

        return GeoCoord(lat / len(self.chargers), lng / len(self.chargers))
