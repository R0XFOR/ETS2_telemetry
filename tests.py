from telemetry_data import SCS_Trailer

trailer = [SCS_Trailer(), SCS_Trailer(), SCS_Trailer(), SCS_Trailer(), SCS_Trailer(), SCS_Trailer(), SCS_Trailer(), SCS_Trailer(), SCS_Trailer(), SCS_Trailer()]

ii = 1

for tr in trailer:
    tr.name = f"tr{ii}"
    ii += 1

for tr in trailer:
    print(tr.name)