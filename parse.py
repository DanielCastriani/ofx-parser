from ofx_parse import OFX

ofx = OFX.read_ofx('../ofx/2021_Jan_21.ofx')

print(ofx)
