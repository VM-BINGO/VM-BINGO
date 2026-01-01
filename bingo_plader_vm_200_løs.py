import random
import json
from collections import Counter

DATA = [
    ("1-0", 10.625), ("2-1", 10.625), ("0-1", 10.3125), ("0-0", 9.0625),
    ("1-1", 8.75), ("2-0", 7.8125), ("1-2", 7.5), ("0-2", 6.25),
    ("2-2", 3.75), ("3-1", 3.75), ("0-3", 3.4375), ("3-0", 3.125),
    ("2-3", 1.875), ("4-1", 1.5625), ("1-3", 1.5625), ("3-2", 1.25),
    ("3-3", 0.9375), ("0-4", 0.9375), ("1-4", 0.9375), ("4-0", 0.9375),
    ("4-2", 0.625), ("2-4", 0.625), ("6-1", 0.625), ("7-0", 0.625),
    ("5-0", 0.3125), ("5-2", 0.3125), ("6-0", 0.3125), ("6-2", 0.3125),
    ("1-5", 0.3125), ("1-7", 0.3125), ("2-5", 0.3125), ("4-3", 0.3125)
]

ANTAL_PLADER = 200
FELTER_PR_PLADE = 15

DUP_THRESHOLD = 5.0   # >5 %
MAX_DUP = 3

OUTPUT = "vm_plader_200_15felter_15_loest.json"


# --- Forbered data ---
PROCENTER = {r: p for r, p in DATA}
RESULTATER_SORTERET = sorted(DATA, key=lambda x: x[1], reverse=True)


def lav_plade():
    felter = []
    tæller = Counter()

    # Top-tung pulje
    pool = []
    for r, p in RESULTATER_SORTERET:
        if p > 8:
            vægt = 6
        elif p > 5:
            vægt = 4
        else:
            vægt = 1
        pool.extend([r] * vægt)

    random.shuffle(pool)

    for r in pool:
        nu = tæller[r]

        if PROCENTER[r] > DUP_THRESHOLD:
            if nu < MAX_DUP:
                felter.append(r)
                tæller[r] += 1
        else:
            if nu == 0:
                felter.append(r)
                tæller[r] += 1

        if len(felter) == FELTER_PR_PLADE:
            break

    # Fallback (sikkerhed)
    for r, p in RESULTATER_SORTERET:
        if len(felter) == FELTER_PR_PLADE:
            break

        nu = tæller[r]
        if p > DUP_THRESHOLD and nu < MAX_DUP:
            felter.append(r)
            tæller[r] += 1
        elif p <= DUP_THRESHOLD and nu == 0:
            felter.append(r)
            tæller[r] += 1

    # 🔒 SORTERING = sikrer indholds-unikhed
    return tuple(sorted(felter))


def main():
    plader = {}
    sete = set()
    nr = 1

    while nr <= ANTAL_PLADER:
        plade = lav_plade()

        # Hård garanti
        assert len(plade) == FELTER_PR_PLADE

        if plade not in sete:
            sete.add(plade)
            plader[str(nr)] = list(plade)
            nr += 1

    # Ekstra global validering
    assert len(set(tuple(v) for v in plader.values())) == ANTAL_PLADER

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("{\n")
        total = len(plader)

        for i, (nr, felter) in enumerate(plader.items(), start=1):
            linje = f'  "{nr}": {json.dumps(felter, ensure_ascii=False)}'
            if i < total:
                linje += ","
            f.write(linje + "\n")

        f.write("}\n")

 
    print(f"Gemt {ANTAL_PLADER} plader i {OUTPUT}")


if __name__ == "__main__":
    main()
