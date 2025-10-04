import datetime
from custom_types import *

if __name__ == "__main__":
    DO_REWRITE = True

    with open("parsing2.txt", "r") as input2, open("all_levels.txt", "w") as output2:
        readlines2 = input2.readlines()[2::3]
        output2.writelines(readlines2)
    with (open("og_parsing.txt", "r") as input_file,
          open("all_levels.txt", "r") as levels_file):
        readlines = input_file.readlines()
        levels: list[Level] = [line[:-1] for line in levels_file.readlines()]
        print(readlines2)
        # print(readlines[-2:])
        i = 0
        placements: dict[Date: list[Entry]]    = dict()
        movements:  dict[Date: list[Movement | Swap]] = dict()
        removals:   dict[Date: list[Removal]]  = dict()
        last_date:  Date | None                = None
        for line in readlines:
            if line == "*\n":
                pass
            index_date = line.find("â€”")
            if index_date != -1:
                i += 1
                # print(f"{i:<4}|", line[index_date+4:-1])
                last_date = line[index_date+4:-1]
                if last_date not in placements:
                    placements[last_date] = list()
                    movements[last_date] = list()
                    removals[last_date] = list()

            index_placement = line.find("has been placed at")
            if index_placement != -1:
                placements[last_date].append((
                    line[:index_placement - 1],
                    int(line[line.find("#"):].split(",")[0][1:].split(" ")[0])
                ))

            index_movement = line.find("has been moved")
            if index_movement != -1:
                print(f'{last_date} | {line[line.find("from #"):][6:].split(" ")[0]}')
                movements[last_date].append((
                    line[:index_movement - 1],
                    int(line[line.find("from #"):][6:].split(" ")[0].split(",")[0])
                ))

            index_removal = line.find("has been removed from")
            if index_removal != -1:
                removals[last_date].append((
                    line[:index_removal - 1],
                    int(line[line.find("#"):][1:].split(" ")[0])
                ))

            index_swap = line.find("have swapped")
            if index_swap != -1:
                print("   ", line[:-1])
                print("   ", tuple(line[:index_swap-1].split(" and ")))
                movements[last_date].append(tuple(line[:index_swap-1].split(" and ")))

            index_swap = line.find("have been swapped")
            if index_swap != -1:
                print("   ", line[:-1])
                print("   ", tuple(line[:index_swap-1].split(" and ")))
                movements[last_date].append(tuple(line[:index_swap-1].split(" and ")))
        if DO_REWRITE:
            with (open("placements.txt", "w") as placements_file,
                  open("movements.txt",  "w") as movements_file,
                  open("swaps.txt",      "w") as swaps_file,
                  open("removals.txt",   "w") as removals_file):
                for k, v in placements.items():
                    placements_file.write(f"{k}\n")
                    for e in v:
                        placements_file.write(f"{e[0]};{e[1]}|")
                    placements_file.write(f"\n")
                for k, v in movements.items():
                    movements_file.write(f"{k}\n")
                    for e in v:
                        movements_file.write(f"{e[0]};{e[1]}|")
                    movements_file.write(f"\n")
                for k, v in removals.items():
                    removals_file.write(f"{k}\n")
                    for e in v:
                        removals_file.write(f"{e[0]};{e[1]}|")
                    removals_file.write(f"\n")
        for key in [e for e in placements.keys()]:
            if len(placements[key]) == 0 and len(movements[key]) == 0:
                placements.pop(key); movements.pop(key)
        for key in placements:
            print(key)
            for v in placements[key]:
                print("   ", v)
                # # if v[0] not in levels:
                # #     print("        !!!")
                # if not v[1].isnumeric():
                #     # print("        !!!")
                #     pass
    print("-----")
    # print(max([len(e) for e in levels]))  # 20 chars
    final_top: dict[Date: list[Level]] = {today: levels}
    last_date = today
    for date in list(placements.keys())[::-1]:
        final_top[date] = [level for level in final_top[last_date]]
        for r in removals[date]:
            final_top[date] = final_top[date][:r[1]-1] + [r[0]] + final_top[date][r[1]-1:]
        for m in list(movements[date])[::-1]:
            # print(m)
            if type(m[1]) is int:
                m0_index = final_top[date].index(m[0])
                print("            MOVE:", m, ";", m0_index)
                final_top[date].remove(m[0])
                final_top[date] = final_top[date][:m[1]-1] + [m[0]] + final_top[date][m[1]-1:]
            else:
                print("            SWAP:", m)
                index1, index2 = final_top[date].index(m[0]), final_top[date].index(m[1])
                if index2 - index1 not in (1, -1):
                    pass
                tmp = final_top[date][index1]
                final_top[date][index1], final_top[date][index2] = final_top[date][index2], tmp
                # final_top[date][final_top[date].index(m[0])], final_top[date][final_top[date].index(m[1])] = \
                #     final_top[date][final_top[date].index(m[1])], final_top[date][final_top[date].index(m[0])]
        for p in placements[date][::-1]:
            print("            ADD: ", p)
            if final_top[date].index(p[0]) + 1 != p[1]:
                pass
            final_top[date].remove(p[0])
        print(date)
        print("                     ", *[f"{e:<20}" for e in final_top[date][:]], sep=" | ")
        last_date = date
        if date == "04.01.2024 6:19":
            pass
    print()
    print(*final_top[last_date], sep="\n")
    print(len(final_top[last_date]))

    with (open("final_top_legacy.txt", "w") as final_top_file,
          open("output3.txt", "w") as final_output):
        for k, v in list(final_top.items())[::-1]:
            final_top_file.write(f"{k}\n")
            final_output.write(f"{k}\n")
            for e in v:
                final_top_file.write(f"{e}|")
                final_output.write(f"{e:<20} | ")
            final_top_file.write(f"\n")
            final_output.write(f"\n")
