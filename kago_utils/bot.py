from kago_utils.player import Player


class Bot(Player):
    def select_teban_action(self) -> None:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def select_non_teban_action(self) -> None:
        raise NotImplementedError("This method should be implemented by subclasses.")

    def select_chankan_action(self) -> None:
        raise NotImplementedError("This method should be implemented by subclasses.")
