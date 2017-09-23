from contrib.rules import CX310, ProtocolTrunk, ProtocolIP
from models.actions import link, group

cx310_1 = CX310('1321')
cx310_2 = CX310('1322')
cx310_3 = CX310('1323')

link(cx310_1, cx310_2, ProtocolTrunk)
link(group(cx310_1, cx310_2), cx310_3, ProtocolIP)
print(ProtocolTrunk.interfaces())
print(ProtocolTrunk.interfaces())
