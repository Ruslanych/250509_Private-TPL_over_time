import functools
import math
from multiprocessing.reduction import duplicate
from typing import Callable

import flet
import flet.canvas
import datetime
from custom_types import *

class App(object):
    def main(self, page: flet.Page):
        def on_keyboard(e: flet.KeyboardEvent):
            if e.key == "Escape":
                page.window.close()

        def start_animation():
            page.clean()
            page.add(
                canvas:=flet.canvas.Canvas(shapes=[], expand=True, width=float("inf"))
            )
            page.update()

        def start_reverse_engineering():
            make_container = lambda i, _date_id: flet.Container(
                padding=flet.Padding(top=0, bottom=0, left=3, right=3),
                margin=flet.Margin(0, 0, 0, 0),
                content=flet.Container(content=flet.Row(
                    [
                        # flet.Container(width=4),
                        flet.Text(f"#{i + 1}", size=12, weight=flet.FontWeight.BOLD, width=35,
                                  text_align=flet.TextAlign.END),
                        flet.Text(f"{final_top[dates[_date_id]][i]}", size=10, width=120),

                    ] + ([
                             flet.Button(
                                 content=flet.Text(">", rotate=flet.Rotate(math.pi / 2)),
                                 height=15, width=15,
                                 style=flet.ButtonStyle(
                                     padding=flet.Padding(left=7, top=0, right=0, bottom=0),
                                     shape=flet.RoundedRectangleBorder(radius=4),
                                 ),
                                 on_click=lambda e: swap_levels_movedown(int(e.control.parent.controls[0].value[1:]) - 1)),
                             flet.Button(
                                 content=flet.Text("<", rotate=flet.Rotate(math.pi / 2)),
                                 height=15, width=15,
                                 style=flet.ButtonStyle(
                                     padding=flet.Padding(left=7, top=0, right=0, bottom=0),
                                     shape=flet.RoundedRectangleBorder(radius=4),
                                 ),
                                 on_click=lambda e: swap_levels_moveup(int(e.control.parent.controls[0].value[1:]) - 1)),
                             flet.Button(
                                 content=flet.Text("X", rotate=flet.Rotate(math.pi*0), size=12, height=14),
                                 height=15, width=15,
                                 expand=False,
                                 style=flet.ButtonStyle(
                                     padding=flet.Padding(left=0, top=0, right=0, bottom=0),
                                     shape=flet.RoundedRectangleBorder(radius=4),
                                 ),
                                 on_click=lambda e: delete_level(int(e.control.parent.controls[0].value[1:]) - 1)),
                         ] if self.current_date_id == _date_id and self.current_date_id < len(dates) - 1 else []),
                    alignment=flet.VerticalAlignment.CENTER,)
                )
            )

            def swap_levels(i, j):
                tmp = final_top[dates[self.current_date_id]][i]
                final_top[dates[self.current_date_id]][i], final_top[dates[self.current_date_id]][j] = final_top[dates[self.current_date_id]][j], tmp
                this_levels.controls = [make_container(i, self.current_date_id) for i in range(len(final_top[dates[self.current_date_id]]))]
                this_levels.update()
            def swap_levels_movedown(i): return swap_levels(i, i+1)
            def swap_levels_moveup(i): return swap_levels(i, i-1)

            def delete_level(i):
                final_top[dates[self.current_date_id]] = final_top[dates[self.current_date_id]][:i] + final_top[dates[self.current_date_id]][i+1:]
                this_levels.controls = [make_container(i, self.current_date_id) for i in range(len(final_top[dates[self.current_date_id]]))]
                this_levels.update()

            def add_level(event: flet.ControlEvent):
                if self.current_date_id >= len(dates) - 1:
                    return
                parent: flet.Row = event.control.parent
                i = parent.controls[1].value
                if not i.isnumeric():
                    return
                i = int(i)
                final_top[dates[self.current_date_id]] = final_top[dates[self.current_date_id]][:i-1] + [parent.controls[0].value] + final_top[dates[self.current_date_id]][i-1:]
                this_levels.controls = [make_container(i, self.current_date_id) for i in range(len(final_top[dates[self.current_date_id]]))]
                this_levels.update()

            def duplicate_prev_dates():
                for date_id in range(len(dates)):
                    pass
                    if date_id == self.current_date_id:
                        break
                    final_top[dates[date_id]] = [e for e in final_top[dates[self.current_date_id]]]
                prev_levels.controls = [make_container(i, self.current_date_id - 1) for i in range(len(final_top[dates[self.current_date_id - 1]]))] if self.current_date_id > 0 else []
                prev_levels.update()

            def duplicate_next_dates():
                for date_id in range(len(dates)-1, -1, -1):
                    pass
                    if date_id == self.current_date_id:
                        break
                    final_top[dates[date_id]] = [e for e in final_top[dates[self.current_date_id]]]
                next_levels.controls = [make_container(i, self.current_date_id + 1) for i in range(len(final_top[dates[self.current_date_id + 1]]))] if self.current_date_id > 0 else []
                next_levels.update()

            def show_tops():
                prev_levels.controls = [make_container(i, self.current_date_id - 1) for i in range(len(final_top[dates[self.current_date_id - 1]]))] if self.current_date_id > 0 else []
                prev_day.value = dates[self.current_date_id - 1].split()[0] if self.current_date_id > 0 else ""
                this_levels.controls = [make_container(i, self.current_date_id)     for i in range(len(final_top[dates[self.current_date_id]]))]
                this_day.value = dates[self.current_date_id].split()[0]
                next_levels.controls = [make_container(i, self.current_date_id + 1) for i in range(len(final_top[dates[self.current_date_id + 1]]))] if self.current_date_id < len(dates) - 1 else []
                next_day.value = dates[self.current_date_id + 1].split()[0] if self.current_date_id < len(dates) - 1 else ""


                markdown.controls = ([
                    flet.Row([
                        flet.Button(
                            "Save top history",
                            on_click=lambda e: save_finaltop(),
                        ),
                        flet.Button(
                            "Apply to the previous dates",
                            disabled=True,
                            on_click=lambda e: page_open(ad1 := flet.AlertDialog(
                                modal=True,
                                title="Confirmation Dialogue",
                                actions=[
                                    flet.Button("Yes", on_click=lambda e: (duplicate_prev_dates(), page.close(e.control.parent))),
                                    flet.Button("Cancel", on_click=lambda e: page.close(e.control.parent)),
                                ]
                            )),
                        ),
                        flet.Button(
                            "Apply to the next dates",
                            on_click=lambda e: page_open(ad1 := flet.AlertDialog(
                                modal=True,
                                title="Confirmation Dialogue",
                                actions=[
                                    flet.Button("Yes", on_click=lambda e: (duplicate_next_dates(), page.close(e.control.parent))),
                                    flet.Button("Cancel", on_click=lambda e: page.close(e.control.parent)),
                                ]
                            )),
                        )
                    ])
                ] + [flet.Row([
                       flet.Button(
                           "Go to",
                           on_click=lambda e: page_open((ad2 := flet.AlertDialog(
                                modal=True,
                                # title="Confirmation Dialogue",
                                actions=[
                                    flet.Column([
                                        flet.Button(f"{i} | {dates[i]}", on_click=lambda e: (goto(int(e.control.text.split("|")[0])), page.close(e.control.parent.parent)))
                                        for i in range(len(dates))
                                    ], width=170, height=600, scroll=flet.ScrollMode.AUTO),
                                    flet.Button("Cancel", on_click=lambda e: page.close(e.control.parent)),
                                ],
                            )),)
                       ),
                ] + [flet.Container(width=50, content=
                        flet.Button(
                            "<",
                            on_click=lambda e: goto(self.current_date_id - 1),
                        )
                        if self.current_date_id > 0 else None
                )] + [flet.Container(width=50, content=
                        flet.Button(
                            ">",
                            on_click=lambda e: goto(self.current_date_id + 1),
                        )
                        if self.current_date_id < len(dates) - 1 else None
                )])] + (
                    [
                        flet.Container(margin=flet.Margin(10, 5, 10, 5), width=650, height=3, bgcolor="#36618E"),
                        # flet.Markdown(),
                        flet.Container(flet.Column([
                            flet.Markdown(markdowns[dates[self.current_date_id]].replace("<@&1187636497470472192>", "**@List Update Notifications**"), selectable=True),
                        ], scroll=flet.ScrollMode.AUTO),
                            height=600, width=670, padding=flet.Padding(3, 0, 3, 0),
                            border_radius=4, border=flet.Border(*[flet.BorderSide(width=1, color="#000000") for i in "1234"])),
                    ]
                ))
                page.update()

            def goto(date_id: int):
                if not 0 <= date_id < len(dates):
                    pass
                self.current_date_id = date_id
                show_tops()

            def save_finaltop():
                with open("final_top_2.txt", "w") as final_top_output:
                    # final_top[dates[0]] = []
                    # final_top[dates[1]] = [line[:-1] for line in open("og_top_2.txt", "r").readlines()]
                    for date in dates:
                        final_top_output.write(f"{date}\n{functools.reduce(lambda a, b: str(a) + '|' + str(b), final_top[date]) if len(final_top[date]) != 0 else ''}\n")

            page.clean()
            page.add(flet.Row([
                flet.Column([
                    prev_day:=flet.Text("", text_align=flet.TextAlign.CENTER, width=260),
                    flet.Container(
                        prev_levels:=flet.Column([], scroll=flet.ScrollMode.ALWAYS, height=780, width=260),
                        border=flet.Border(top=flet.BorderSide(2), bottom=flet.BorderSide(2), left=flet.BorderSide(2), right=flet.BorderSide(2)),
                        border_radius=5,
                    ),
                    flet.Container(height=50),
                ]),
                flet.Column([
                    this_day:=flet.Text("", text_align=flet.TextAlign.CENTER, width=260, weight=flet.FontWeight.BOLD),
                    flet.Container(
                        this_levels:=flet.Column([], scroll=flet.ScrollMode.ALWAYS, height=780, width=260),
                        border=flet.Border(top=flet.BorderSide(2), bottom=flet.BorderSide(2), left=flet.BorderSide(2), right=flet.BorderSide(2)),
                        border_radius=5,
                    ),
                    flet.Container(height=50, width=260, content=flet.Row([
                        flet.TextField(text_style=flet.TextStyle(size=14),
                                       content_padding=flet.Padding(1, 1, 1, 1), scroll_padding=flet.Padding(1, 1, 1, 1),
                                       height=20, width=150),
                        flet.TextField(text_style=flet.TextStyle(size=14),
                                       content_padding=flet.Padding(1, 1, 1, 1), scroll_padding=flet.Padding(1, 1, 1, 1),
                                       height=20, width=30),
                        flet.Button(
                            content=flet.Text("add", style=flet.TextStyle(size=13, weight=flet.FontWeight.W_600, color="#000000")),
                            height=20, width=40,
                            style=flet.ButtonStyle(
                                padding=flet.Padding(left=0, top=0, right=0, bottom=0)),
                            on_click=add_level),
                    ], alignment=flet.MainAxisAlignment.CENTER, vertical_alignment=flet.CrossAxisAlignment.START)),
                ]),
                flet.Column([
                    next_day:=flet.Text("", text_align=flet.TextAlign.CENTER, width=260),
                    flet.Container(
                        next_levels:=flet.Column([], scroll=flet.ScrollMode.ALWAYS, height=780, width=260),
                        border=flet.Border(top=flet.BorderSide(2), bottom=flet.BorderSide(2), left=flet.BorderSide(2), right=flet.BorderSide(2)),
                        border_radius=5,
                    ),
                    flet.Container(height=50),
                ]),
                flet.Container(width=10),
                markdown:=flet.Column(width=670, alignment=flet.MainAxisAlignment.START, height=700),
            ]))
            with open("all_levels.txt", "r") as all_levels_file:
                all_levels = [line[:-1] for line in all_levels_file.readlines()]
            with open("markdowns.txt", "r", encoding="utf-8") as markdowns_file:
                markdowns: dict[Date: str] = dict()
                next_line_is_date = False
                last_date: Date = None
                for line in markdowns_file.readlines():
                    if line == ">>>>>>>>>>\n":
                        next_line_is_date = True
                        continue
                    if next_line_is_date:
                        last_date = line[:-1]
                        markdowns[last_date] = ""
                        next_line_is_date = False
                        continue
                    markdowns[last_date] += line
                markdowns[today] = "**Current day**"

            dates = list(markdowns.keys())[::-1]
            if today not in dates: dates.append(today)
            dates = sorted(dates, key=lambda e: tuple(map(int, (e[6:10], e[3:5], e[0:2], e.split()[1][:-3], e[-2:]))))
            self.current_date_id = len(dates) - 1
            def next_date() -> Date | None: return None if self.current_date_id == len(dates) - 1 else dates[self.current_date_id + 1]
            def curr_date() -> Date | None: return dates[self.current_date_id]
            def prev_date() -> Date | None: return None if self.current_date_id == 0 else dates[self.current_date_id - 1]

            with open("final_top_2.txt", "r") as final_top_file:
                final_top: dict[Date: list[Level]] = dict()
                last_date: Date = None
                i = 0
                for line in final_top_file.readlines():
                    if i % 2 == 0:
                        last_date = line[:-1]
                        final_top[last_date] = list()
                    else:
                        final_top[last_date] = line[:-1].split("|") if line != "\n" else []
                    i += 1
                final_top[today] = all_levels
                for date in dates:
                    if date not in final_top:
                        final_top[date] = [lv for lv in all_levels]
            show_tops()

        def page_open(control: flet.Control) -> flet.Page:
            return page.open(control)
        page.on_keyboard_event = on_keyboard
        page.Title = "TPL over time"
        page.window.full_screen = True
        page.add(
            flet.Container(
                padding=flet.Padding(top=40, left=75, right=0, bottom=0), content=
                flet.Button(
                    content=flet.Container(
                        flet.Text("Start the animation", font_family="Helvetica", size=30),
                        padding=flet.Padding(top=10, left=10, right=10, bottom=10)
                    ),
                    style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=20)),
                    on_click=lambda event: start_animation(),
                ),
            )
        )
        page.add(
            flet.Container(
                padding=flet.Padding(top=40, left=75, right=0, bottom=0), content=
                flet.Button(
                    content=flet.Container(
                        flet.Text("Start Reverse Engineering", font_family="Helvetica", size=30),
                        padding=flet.Padding(top=10, left=10, right=10, bottom=10)
                    ),
                    style=flet.ButtonStyle(shape=flet.RoundedRectangleBorder(radius=20)),
                    on_click=lambda event: start_reverse_engineering(),
                ),
            )
        )
        page.update()

flet.app(App().main)

