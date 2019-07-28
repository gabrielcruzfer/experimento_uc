from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random


class Constants(BaseConstants):
    name_in_url = "public_goods"
    players_per_group = 2
    num_rounds = 1
    endowment = c(100)
    multiplier = 2
    AdminReport_template = "public_goods/AdminReport.html"
    instructions_template = "public_goods/instructions.html"
    gamescripts = "public_goods/gamescripts.html"
    answerinput = "public_goods/answerinput.html"


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        contributions = [
            p.contribution for p in self.get_players()
            if p.contribution is not None
        ]
        if contributions:
            return {
                "avg_contribution": sum(contributions) / len(contributions),
                "min_contribution": min(contributions),
                "max_contribution": max(contributions),
            }
        else:
            return {
                "avg_contribution": "(no data)",
                "min_contribution": "(no data)",
                "max_contribution": "(no data)",
            }


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_payoffs(self):
        # self.total_contribution = sum(
        #     [p.contribution for p in self.get_players()]
        # )
        # self.individual_share = (
        #     self.total_contribution * Constants.multiplier /
        #     Constants.players_per_group
        # )
        for p in self.get_players():
            # p.payoff = (
            #     Constants.endowment - p.contribution
            # ) + self.individual_share
            p.payoff = 1


class Player(BasePlayer):
    # contribution = models.CurrencyField(
    #     doc="The amount contributed by the player",
    #     max=Constants.endowment, min=0
    # )
    correct_answers_practice = models.IntegerField(initial=0)
    correct_answers_round_one = models.IntegerField(initial=0)
    correct_answers_round_two = models.IntegerField(initial=0)
    correct_answers_round_three = models.IntegerField(initial=0)

    probabilities_round_five_0 = models.IntegerField(initial=25)
    probabilities_round_five_1 = models.IntegerField(initial=25)
    probabilities_round_five_2 = models.IntegerField(initial=25)
    probabilities_round_five_3 = models.IntegerField(initial=25)

    round_two_mode = models.StringField(
        choices=[
            ["por respuesta", "Pago por respuesta ($0.5 por cada suma correcta)"],
            ["torneo", "Torneo ($2 por cada suma correcta si resuelves más sumas correctas que los otros miembros en la Tarea 1, en caso contrario recibes $0)."]
        ],
        widget=widgets.RadioSelect
    )

    round_four_mode = models.StringField(
        choices=[
            ["por respuesta", "Pago por Pregunta ($0.5 por cada suma correcta en Etapa 3)"],
            ["torneo", "Torneo ($2 por cada suma correcta si resolviste más sumas correctas que el resto de los participantes en la Etapa 3. En caso contrario, recibirás $0)"]
        ],
        widget=widgets.RadioSelect
    )