import prettytable as prettytable
import random as rnd

KICHTHUOCQUANTHE = 9	
SOLICHUUTU = 1
TOURNAMENT_SELECTION_SIZE = 4
MUTATION_RATE= 0.1
class Data:
    ROOMS = [["R1", 20], ["R2", 15], ["R3", 22], ["R4", 22], ["R5", 15]]
    INSTRUCTORS = [["I1", "Le Thi An"], ["I2", "Nguyen Binh"], ["I3", "Dang Van DUng"], ["I4", "Nguyen van Hoang"]]
    MEETING_TIMES = [["MT1", "HTS 8:00 10:00"], ["MT2", "HTS 10:00 12:00"], ["MT3", "BN 8:00 10:00"], ["MT4", "BN 10:00 12:00"]]

    def __init__(self):
        self._cacPhongHoc = []
        self._cacGiaoVien = []
        self._cacGioHoc = []
        for i in range(0, len(self.ROOMS)):
            self._cacPhongHoc.append(PhongHoc(self.ROOMS[i][0], self.ROOMS[i][1]))
        for i in range(0, len(self.INSTRUCTORS)):
            self._cacGiaoVien.append(GiaoVien(self.INSTRUCTORS[i][0], self.INSTRUCTORS[i][1]))
        for i in range(0, len(self.MEETING_TIMES)):
         	self._cacGioHoc.append(GioHoc(self.MEETING_TIMES[i][0], self.MEETING_TIMES[i][1]))
        lop1 = Lop("C1", "SL1", [self._cacGiaoVien[0], self._cacGiaoVien[1]], 20)
        lop2 = Lop("C2", "SL2", [self._cacGiaoVien[0], self._cacGiaoVien[1], self._cacGiaoVien[2]], 12)
        lop3 = Lop("C3", "SL3", [self._cacGiaoVien[1], self._cacGiaoVien[2], self._cacGiaoVien[3]], 12)
        lop4 = Lop("C4", "SL4", [self._cacGiaoVien[0], self._cacGiaoVien[3]], 20)
        lop5 = Lop("C5", "WR1", [self._cacGiaoVien[2], self._cacGiaoVien[3]], 22)
        lop6 = Lop("C6", "WR2", [self._cacGiaoVien[0], self._cacGiaoVien[1]], 22)
        lop7 = Lop("C7", "WR3", [self._cacGiaoVien[2], self._cacGiaoVien[3]], 22)
        self._cacLop = [lop1, lop2, lop3, lop4, lop5, lop6, lop7]
        khoaHoc1 = KhoaHoc("IE1", [lop1, lop5])
        khoaHoc2 = KhoaHoc("IE2", [lop2, lop3, lop6])
        khoaHoc3 = KhoaHoc("IE3", [lop4, lop7])
        self._cacKhoaHoc = [khoaHoc1, khoaHoc2, khoaHoc3]
        self._soLopHocHoanChinh = 0
        for i in range(0, len(self._cacKhoaHoc)):
            self._soLopHocHoanChinh += len(self._cacKhoaHoc[i].get_cacLop())

    def get_cacPhongHoc(self):
        return self._cacPhongHoc

    def get_cacGiaoVien(self):
        return self._cacGiaoVien

    def get_cacLop(self):
        return self._cacLop

    def get_cacKhoaHoc(self):
        return self._cacKhoaHoc

    def get_cacGioHoc(self):
    	return self._cacGioHoc

    def get_soLopHocHoanChinh(self):
        return self._soLopHocHoanChinh
class Lich:
    def __init__(self):
        self._data = data
        self._cacLopHocHoanChinh = []
        self._soXungDot = 0
        self._doThichNghi = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_cacLopHocHoanChinh(self):
        self._isFitnessChanged = True
        return self._cacLopHocHoanChinh

    def get_soXungDot(self):
        return self._soXungDot

    def get_doThichNghi(self):
        if (self._isFitnessChanged == True):
            self._doThichNghi = self.tinhDoThichNghi
            self._isFitnessChanged = False
        return self._doThichNghi

    def initialize(self):
        cacKhoaHoc = self._data.get_cacKhoaHoc()
        for i in range(0, len(cacKhoaHoc)):
            cacLop = cacKhoaHoc[i].get_cacLop()
            for j in range(0, len(cacLop)):
                newClass = LopHocHoanChinh(self._classNumb, cacKhoaHoc[i], cacLop[j])
                self._classNumb += 1
                newClass.set_gioHoc(data.get_cacGioHoc()[rnd.randrange(0, len(data.get_cacGioHoc()))])
                newClass.set_phongHoc(data.get_cacPhongHoc()[rnd.randrange(0, len(data.get_cacPhongHoc()))])
                newClass.set_giaoVien(data.get_cacGiaoVien()[rnd.randrange(0, len(cacLop[j].get_cacGiaoVien()))])
                self._cacLopHocHoanChinh.append(newClass)
        return self

    @property
    def tinhDoThichNghi(self):
        self._soXungDot = 0
        cacLopHocHoanChinh = self.get_cacLopHocHoanChinh()
        for i in range(0, len(cacLopHocHoanChinh)):
            if (cacLopHocHoanChinh[i].get_phongHoc().get_soCho() < cacLopHocHoanChinh[i].get_lop().get_soHocSinhToiDa ()):
                self._soXungDot += 1
            for j in range(0, len(cacLopHocHoanChinh)):
                if (j >= i):
                    if(cacLopHocHoanChinh[i].get_gioHoc() == cacLopHocHoanChinh[j].get_gioHoc() and cacLopHocHoanChinh[i].get_idLopHocHoanChinh() != cacLopHocHoanChinh[j].get_idLopHocHoanChinh()):
                        if(cacLopHocHoanChinh[i].get_phongHoc() == cacLopHocHoanChinh[j].get_phongHoc()):
                            self._soXungDot += 1
                        if(cacLopHocHoanChinh[i].get_giaoVien() == cacLopHocHoanChinh[j].get_giaoVien()):
                            self._soXungDot += 1
        return 1 / (1.0 * self._soXungDot + 1)

    def __str__(self):
        returnValue = ""
        for i in range(0, len(self._cacLopHocHoanChinh) - 1):
            returnValue += str(self._cacLopHocHoanChinh[i]) + ","
        returnValue += str(self._cacLopHocHoanChinh[len(self._cacLopHocHoanChinh) - 1])
        return returnValue
class QuanThe:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._cacLich = []
        for i in range(0, size):
            self._cacLich.append(Lich().initialize())

    def get_cacLich(self): return self._cacLich


class Ga:
	def envolve(self, quanThe):return self._dotBien_quanThe(self._lai_quanThe(quanThe))
	def _lai_quanThe(self, qt): #lai tao
		lai_qt= QuanThe(0)
		for i in range(SOLICHUUTU):
			lai_qt.get_cacLich().append(qt.get_cacLich()[i])
		i = SOLICHUUTU
		while i< KICHTHUOCQUANTHE:
			lich1 =self._select_tournament_population(qt).get_cacLich()[0]
			lich2 =self._select_tournament_population(qt).get_cacLich()[0]
			lai_qt.get_cacLich().append(self._lai_lich(lich1, lich2))
			i+=1
		return lai_qt

	def _dotBien_quanThe(self, quanThe): 
		for i in range(SOLICHUUTU,KICHTHUOCQUANTHE): 
			self._dotBien_lich(quanThe.get_cacLich()[i])
		return quanThe
	def _lai_lich(self, lich1, lich2):
		laiGhep =Lich().initialize()
		for i in range(0,len(laiGhep.get_cacLopHocHoanChinh())):
			if(rnd.random() > 0.5): laiGhep.get_cacLopHocHoanChinh()[i] = lich1.get_cacLopHocHoanChinh()[i]
			else:laiGhep.get_cacLopHocHoanChinh()[i] = lich2.get_cacLopHocHoanChinh()[i]
		return laiGhep
	def _dotBien_lich(self, dotBienLich):
		lich = Lich().initialize()
		for i in range(0, len(dotBienLich.get_cacLopHocHoanChinh())):
			if (MUTATION_RATE > rnd.random()):
				dotBienLich.get_cacLopHocHoanChinh()[i] = lich.get_cacLopHocHoanChinh()[i]
		return dotBienLich

	def _select_tournament_population(self, qt):
		tournament_qt = QuanThe(0)
		i = 0
		while i< TOURNAMENT_SELECTION_SIZE:
			tournament_qt.get_cacLich().append(qt.get_cacLich()[rnd.randrange(0, KICHTHUOCQUANTHE)])
			i +=1
		tournament_qt.get_cacLich().sort(key= lambda x: x.get_doThichNghi(), reverse= True)
		return tournament_qt


class Lop:
    def __init__(self, number, ten, cacGiaoVien, soHocSinhToiDa ):
        self._number = number
        self._ten = ten
        self._cacGiaoVien = cacGiaoVien
        self._soHocSinhToiDa  = soHocSinhToiDa 

    def get_number(self): return self._number

    def get_ten(self): return self._ten

    def get_cacGiaoVien(self): return self._cacGiaoVien

    def get_soHocSinhToiDa (self): return self._soHocSinhToiDa 

    def __str__(self): return self._ten


class GiaoVien:
    def __init__(self, idIns, ten):
        self._idIns = idIns
        self._ten = ten

    def get_idIns(self): return self._idIns

    def get_ten(self): return self._ten

    def __str__(self): return self._ten


class PhongHoc:
    def __init__(self, number, soCho):
        self._number = number
        self._soCho = soCho

    def get_number(self): return self._number

    def get_soCho(self): return self._soCho


class GioHoc:
	def __init__(self, idMT, thoiGian):
		self._idMT= idMT
		self._thoiGian = thoiGian
	def get_idMT(self): return self._idMT
	def get_thoiGian(self): return self._thoiGian
class KhoaHoc:
    def __init__(self, ten, cacLop):
        self._ten = ten
        self._cacLop = cacLop

    def get_ten(self): return self._ten

    def get_cacLop(self): return self._cacLop
class LopHocHoanChinh:
    def __init__(self, idLopHocHoanChinh, khoaHoc, lop):
        self._idLopHocHoanChinh = idLopHocHoanChinh
        self._khoaHoc = khoaHoc
        self._lop = lop
        self._giaoVien = None
        self._phongHoc = None
        self._gioHoc = None

    def get_idLopHocHoanChinh(self): return self._idLopHocHoanChinh

    def get_khoaHoc(self): return self._khoaHoc

    def get_lop(self): return self._lop

    def get_giaoVien(self): return self._giaoVien

    def get_phongHoc(self): return self._phongHoc

    def get_gioHoc(self): return self._gioHoc

    def set_giaoVien(self, giaoVien):
        self._giaoVien = giaoVien

    def set_phongHoc(self, phongHoc):
        self._phongHoc = phongHoc
    def set_gioHoc(self, gioHoc):
        self._gioHoc= gioHoc
    def __str__(self):
        return str(self._khoaHoc.get_ten()) + "," + str(self._lop.get_ten()) + "," + str(self._phongHoc.get_number()) + "," + \
               str(self._giaoVien.get_idIns()) + "," + str(self._gioHoc.get_idMT()) + " | "
class Display:
    def print_available_data(self):
        print("> All available data")
        self.print_khoaHoc()
        self.print_lop()
        self.print_phongHoc()
        self.print_giaoVien()

    def print_khoaHoc(self):
        cacKhoaHoc = data.get_cacKhoaHoc()
        bangCacKhoaHoc = prettytable.PrettyTable(['khoaHoc', 'cacLop'])
        for i in range(0, len(cacKhoaHoc)):
            cacLop = cacKhoaHoc.__getitem__(i).get_cacLop()
            tempStr = "["
            for j in range(0, len(cacLop) - 1):
                tempStr += cacLop[j].__str__() + ","
            tempStr += cacLop[len(cacLop) - 1].__str__() + "]"
            bangCacKhoaHoc.add_row([cacKhoaHoc.__getitem__(i).get_ten(), tempStr])
        print(bangCacKhoaHoc)

    def print_lop(self):
        cacLop = data.get_cacLop()
        bangCacLop = prettytable.PrettyTable(['id', 'lop #', 'so hoc sinh toi da', 'cacGiaoVien'])
        for i in range(0, len(cacLop)):
            cacGiaoVien = cacLop[i].get_cacGiaoVien()
            tempStr = " "
            for j in range(0, len(cacGiaoVien)-1):
                tempStr += cacGiaoVien[j].__str__() + ","
            tempStr += cacGiaoVien[len(cacGiaoVien)-1].__str__()
            bangCacLop.add_row(
                [cacLop[i].get_number(), cacLop[i].get_ten(), str(cacLop[i].get_soHocSinhToiDa ()), tempStr])
        print(bangCacLop)

    def print_phongHoc(self):
        cacPhongHoc = data.get_cacPhongHoc()
        bangCacPhongHoc = prettytable.PrettyTable(['phongHoc', 'so cho toi da'])
        for i in range(0, len(cacPhongHoc)):
            bangCacPhongHoc.add_row([str(cacPhongHoc[i].get_number()), str(cacPhongHoc[i].get_soCho())])
        print(bangCacPhongHoc)

    def print_giaoVien(self):
        cacGiaoVien = data.get_cacGiaoVien()
        bangCacGiaoVien = prettytable.PrettyTable(['id', 'giaoVien'])
        for i in range(0, len(cacGiaoVien)):
            bangCacGiaoVien.add_row([cacGiaoVien[i].get_idIns(), cacGiaoVien[i].get_ten()])
        print(bangCacGiaoVien)

    def print_theHe(self, quanThe):
        table1 = prettytable.PrettyTable(
            ['lich', 'do thich nghi', 'so xung dot', 'giaoVien(lop, class, phongHoc, giaoVien, gio hoc)'])
        cacLich = quanThe.get_cacLich()
        for i in range(0, len(cacLich)):
            table1.add_row([str(i), round(cacLich[i].get_doThichNghi(), 3), cacLich[i].get_soXungDot(), cacLich[i].__str__()])
        print(table1)

    def print_lich_as_table(self, lich):
        cacLopHocHoanChinh = lich.get_cacLopHocHoanChinh()
        table = prettytable.PrettyTable(
            ['class', 'khoaHoc', 'lop[number, max of student]', 'phongHoc(cho ngoi)', 'giaoVien', 'gio hoc'])
        for i in range(0, len(cacLopHocHoanChinh)):
            table.add_row([str(i), cacLopHocHoanChinh[i].get_khoaHoc().get_ten(), cacLopHocHoanChinh[i].get_lop().get_ten() + "(" +
                           cacLopHocHoanChinh[i].get_lop().get_number() + "," + str(cacLopHocHoanChinh[
                               i].get_lop().get_soHocSinhToiDa ()) + ")",
                           str(cacLopHocHoanChinh[i].get_phongHoc().get_number()) + "(" + str(cacLopHocHoanChinh[i].get_phongHoc().get_soCho()) + ")",
                           cacLopHocHoanChinh[i].get_giaoVien().get_ten(), cacLopHocHoanChinh[i].get_gioHoc().get_thoiGian()])
        print(table)
data = Data()
display = Display()
display.print_available_data()
theHeThu = 0
print("\n> The he " + str(theHeThu))
quanThe = QuanThe(KICHTHUOCQUANTHE)
quanThe.get_cacLich().sort(key=lambda x: x.get_doThichNghi(), reverse=True)
display.print_theHe(quanThe)
display.print_lich_as_table(quanThe.get_cacLich()[0])
gA = Ga()
while (quanThe.get_cacLich()[0].get_doThichNghi() != 1.0):
	theHeThu += 1
	print("\n> The he  "+ str(theHeThu))
	quanThe= gA.envolve(quanThe)
	quanThe.get_cacLich().sort(key= lambda x: x.get_doThichNghi(), reverse = True)
	display.print_theHe(quanThe)
	display.print_lich_as_table(quanThe.get_cacLich()[0])
print("\n\n")
