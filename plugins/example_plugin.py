from bot.plugins.base import Plugin


class Plugin(Plugin):
    name = "example"

    def after_response(self, response_text: str) -> str:
        return response_text + "\n\n(Example plugin appended this line.)"
