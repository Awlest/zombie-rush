import qrcode, json, os
URL = "https://awlest.github.io/zombie-rush/"
q = qrcode.QRCode(border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
q.add_data(URL); q.make(fit=True)
m = q.get_matrix()
n = len(m)
# construit un attribut path: 1 sous-chemin "M x y h1 v1 h-1 z" par module noir
parts = []
for y, row in enumerate(m):
    for x, val in enumerate(row):
        if val:
            parts.append(f"M{x} {y}h1v1h-1z")
d = "".join(parts)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qr_path.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump({"n": n, "d": d}, f)
print("modules", n, "len(d)", len(d))
