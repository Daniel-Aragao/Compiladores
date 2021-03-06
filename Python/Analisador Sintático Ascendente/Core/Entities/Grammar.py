from Core.Services.TextGrammar import TextToGrammar
from Core.Entities.TermUnit import TermUnit
from Core.Entities.Production import Production


class Grammar:
    STREAM_END_UNIT = TermUnit(TermUnit.STREAM_END, TermUnit.STREAM_END)
    
    def __init__(self, text):

        if(type(text) is TextToGrammar):
            self.textGrammar = text
        else:
            self.textGrammar = TextToGrammar(text)

        self.Premises = self.textGrammar.get_premises()

        self.StartSimbol = self.textGrammar.getStartSimbol()
        self.StartSimbolUnit = self.textGrammar.getStartSimbolUnit()
        
        self.Alphabet = [unit for unit in self.textGrammar.get_term_units() if unit.type is TermUnit.TERMINAL]
        self.NonTerminals = [unit for unit in self.textGrammar.get_term_units() if unit.type is TermUnit.NONTERMINAL]       

        self.load_productions()

    def load_productions(self):
        self.productions = []

        for premise in self.Premises:
            for i in range(len(premise.right)):
                self.productions.append(Production(premise, i))

    def get_production(self, id):
        for production in self.productions:
            if production.id == id:
                return production

    def get_premise(self, termString):
            for i in self.Premises:
                if(i.left == termString):
                    return i

    def __str__(self):
        retorno = 'Alphabet: ' + str(self.Alphabet) + '\n'
        retorno += 'Non Terminals: ' + str(self.NonTerminals) + '\n'
        retorno += 'Start Simbol: ' + str(self.StartSimbol) + '\n'
        retorno += 'Premises:' + str(self.Premises)
        return retorno
