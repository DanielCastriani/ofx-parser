from ofx_parse import OFX

ofx = OFX.read_ofx('data/2021_Jan_21.ofx')

print(ofx.to_string())
