class InternalHardware: pass


class Attr:
    def __assign(self, description): raise NotImplementedError()


class DecimalAttr(Attr):
    pass


class YearAttr(Attr):
    pass


class CPU(InternalHardware):
    l1 = DecimalAttr()
    l2 = DecimalAttr()
    prod_year = YearAttr()


class GPU(InternalHardware):
    pass


class FPGA(InternalHardware):
    pass


class Power(InternalHardware):
    pass


class RAM(InternalHardware):
    pass


class RAID(InternalHardware):
    pass


class Storage(InternalHardware):
    pass
