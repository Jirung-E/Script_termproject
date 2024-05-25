class GeoCoord:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

class Charger:
    def __init__(self, name, addr, coord, state, type):
        self.name: str = name
        self.addr: str = addr
        self.coord: GeoCoord = coord
        self.state: str = state
        self.type: str = type

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