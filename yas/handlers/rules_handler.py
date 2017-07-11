from yas import RegexHandler

class RulesHandler(RegexHandler):
    """Returns Asimov's Three Laws of Robotics."""
    triggers = ['rules']

    def __init__(self, bot):
        super().__init__(r'^rules', bot)

    def handle(self, _, reply):
        for rule, description in self.get_rules().items():
            reply(f"*{rule}*: {description} \n\n")

    def get_rules(self):
        return {
            "The First Law" : "A robot may not injure a human being or, " +
                "through inaction, allow a human being to come to harm.",
            "The Second Law" : "A robot must obey the orders given it by " +
                "human beings except where such orders would conflict with " +
                "the First Law.",
            "The Third Law" : "A robot must protect its own existence as " +
                "long as such protection does not conflict with the First or " +
                "Second Laws."
        }
