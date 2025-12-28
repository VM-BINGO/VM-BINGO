import random
import json

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

RESULTATER = [r for r, _ in DATA]
VÆGTE = [w for _, w in DATA]

ANTAL_PLADER = 50
FELTER_PR_PLADE = 15
MAKS_DUBLETTER = 2

OUTPUT = "vm_plader_50_15felter_2dubletter_unikke.json"


def lav_plade():
    while True:
        felter = random.choices(RESULTATER, weights=VÆGTE, k=FELTER_PR_PLADE)
        dubletter = FELTER_PR_PLADE - len(set(felter))
        if dubletter <= MAKS_DUBLETTER:
            return tuple(felter)


def main():
    plader = {}
    sete = set()
    nr = 1
    forsøg = 0

    while nr <= ANTAL_PLADER:
        plade = lav_plade()
        forsøg += 1

        if plade not in sete:
            sete.add(plade)
            plader[str(nr)] = list(plade)
            nr += 1

        if forsøg > 500_000:
            raise RuntimeError("For mange forsøg – kravene er måske for stramme")

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(plader, f, ensure_ascii=False, indent=2)

    print(f"Gemt {ANTAL_PLADER} unikke plader i {OUTPUT}")


if __name__ == "__main__":
    main()
