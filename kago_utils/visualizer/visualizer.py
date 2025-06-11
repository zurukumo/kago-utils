import os
import tkinter as tk
from typing import Literal

from PIL import Image, ImageTk

from kago_utils.game import Game
from kago_utils.player import Player


class PaiImageLoader:
    def __init__(self) -> None:
        self.image_refs: list[ImageTk.PhotoImage] = []

    def load(
        self, name: str, size: Literal["small", "medium"] = "medium", is_rotated: bool = False
    ) -> ImageTk.PhotoImage:
        if size == "small":
            new_size = (30, 45)
        elif size == "medium":
            new_size = (40, 60)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(
            current_dir, "../resources/images", name + ("-rotated" if is_rotated else "") + ".png"
        )
        img = Image.open(image_path).resize(new_size)
        photo = ImageTk.PhotoImage(img)
        self.image_refs.append(photo)
        return photo

    def clear(self) -> None:
        self.image_refs.clear()


class TenbouImageLoader:
    def __init__(self) -> None:
        self.image_refs: list[ImageTk.PhotoImage] = []

    def load(self, name: str) -> ImageTk.PhotoImage:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "../resources/images", name + ".png")
        img = Image.open(image_path).resize((58, 5))
        photo = ImageTk.PhotoImage(img)
        self.image_refs.append(photo)
        return photo

    def clear(self) -> None:
        self.image_refs.clear()


class PlayerFrame:
    def __init__(
        self, master: tk.Tk, player: Player, hai_image_loader: PaiImageLoader, tenbou_image_loader: TenbouImageLoader
    ) -> None:
        self.frame = tk.Frame(master)
        self.frame.pack(fill="x", padx=10, pady=10, anchor="w")

        self.hai_image_loader = hai_image_loader
        self.tenbou_image_loader = tenbou_image_loader
        self.player = player
        self.content_widgets: list[tk.Widget] = []

    def update(self, game_state: str, is_teban: bool) -> None:
        for widget in self.frame.winfo_children():
            widget.destroy()

        bg = "yellow" if is_teban else self.frame.master.cget("bg")
        self.frame.config(bg=bg)

        # Info
        self.info_frame = tk.Frame(self.frame)
        self.info_frame.pack(side=tk.LEFT)

        # Info -> Jikaze
        self.jikaze_label = tk.Label(self.info_frame, width=12)
        self.jikaze_label.pack()

        # Info -> Ten
        self.score_label = tk.Label(self.info_frame, font=("Arial", 10))
        self.score_label.pack()

        self.info_frame.config(bg=bg)
        self.jikaze_label.config(text=self.player.jikaze, bg=bg)
        self.score_label.config(text=f"{self.player.ten} 点", bg=bg)

        # Info -> Riichi bou
        if self.player.is_riichi_completed:
            img = self.tenbou_image_loader.load("2t")
            tk.Label(self.info_frame, image=img, bg=bg).pack()

        # Main
        main_frame = tk.Frame(self.frame, bg=bg)
        main_frame.pack(fill="x", pady=3)

        # Main -> Tehai
        tehai_frame = tk.Frame(main_frame, bg=bg)
        tehai_frame.pack(fill="x")

        # Main -> Tehai -> Juntehai
        juntehai_frame = tk.Frame(tehai_frame, bg=bg)
        juntehai_frame.grid(row=0, column=0, sticky="w")

        # Main -> Tehai -> Huuro
        huuros_frame = tk.Frame(tehai_frame, bg=bg)
        huuros_frame.grid(row=0, column=1, sticky="e")

        # Main -> Kawa
        kawa_frame = tk.Frame(main_frame, bg=bg)
        kawa_frame.pack(anchor="w")

        # Tehai Details
        for hai in self.player.juntehai:
            if is_teban and game_state in ("tsumo", "rinshan_tsumo", "riichi") and hai == self.player.last_tsumo:
                continue
            img = self.hai_image_loader.load(hai.code)
            tk.Label(juntehai_frame, image=img, bg=bg).pack(side=tk.LEFT)

        if is_teban and game_state in ("tsumo", "rinshan_tsumo", "riichi") and self.player.last_tsumo:
            img = self.hai_image_loader.load(self.player.last_tsumo.code)
            tk.Label(juntehai_frame, image=img, bg=bg).pack(side=tk.LEFT, padx=(10, 0))

        # Huuro Details
        for huuro in self.player.huuros:
            huuro_frame = tk.Frame(huuros_frame, bg=bg)
            huuro_frame.pack(side=tk.RIGHT)

            spacer = tk.Frame(huuros_frame, width=10, bg=bg)
            spacer.pack(side=tk.RIGHT)

            for hai in huuro.hais:
                img = self.hai_image_loader.load(hai.code, size="small")
                tk.Label(huuro_frame, image=img, bg=bg).pack(side=tk.LEFT)

        # Kawa Details
        for hai in self.player.kawa:
            img = self.hai_image_loader.load(hai.code, size="small")
            tk.Label(kawa_frame, image=img, bg=bg).pack(side=tk.LEFT)


class Visualizer:
    def __init__(self, game: Game) -> None:
        self.game = game
        self.root = tk.Tk()
        self.root.title("Visualizer")
        self.root.geometry("1000x700")

        self.hai_image_loader = PaiImageLoader()
        self.tenbou_image_loader = TenbouImageLoader()

        self.next_button = tk.Button(self.root, text="Next", command=self.next_step)
        self.next_button.pack(pady=10)

        self.state_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.state_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.rest_tsumo_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.rest_tsumo_label.pack(anchor="w", padx=10, pady=(0, 10))

        self.player_frames: list[PlayerFrame] = [
            PlayerFrame(self.root, player, self.hai_image_loader, self.tenbou_image_loader)
            for player in self.game.players
        ]

    def start(self) -> None:
        self.update_display()
        self.root.mainloop()

    def next_step(self) -> None:
        self.game.step()
        while self.game.prev_state in (
            "register_teban_action",
            "wait_teban_action",
            "register_non_teban_action",
            "wait_non_teban_action",
            "register_chankan_action",
            "wait_chankan_action",
            "skip",
        ):
            self.game.step()
        self.update_display()

    def update_display(self) -> None:
        self.state_label.config(text=f"state: {self.game.prev_state}")
        self.rest_tsumo_label.config(text=f"rest_tsumo_count: {self.game.yama.rest_tsumo_count}")
        self.hai_image_loader.clear()

        for player, frame in zip(self.game.players, self.player_frames):
            frame.update(self.game.prev_state, player.is_teban)
