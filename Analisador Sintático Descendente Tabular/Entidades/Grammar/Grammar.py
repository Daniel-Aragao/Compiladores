from collections import deque
from Entidades.Term import Term
from Entidades.Term import TermUnit
from Entidades.Grammar.TextGrammar import TextGrammar


class Grammar:
    STREAM_END_UNIT = TermUnit(TermUnit.STREAM_END, TermUnit.STREAM_END)

    def __init__(self, text):
        self.textGrammar = TextGrammar(text)
        self.StartSimbol = self.textGrammar.getStartSimbol()

        self.Terms = self.textGrammar.get_terms()
        self.AnalysisTable = {}

        self.build_grammar_routine()
        
    
    def build_grammar_routine(self):

        self.build_first()

        self.build_follow()

    def build_first(self):
        for term in self.Terms:
            self.first(term)

    def first(self, p) :
        p_type = type(p)
        retorno = None

        if(p_type is list):
            retorno = self.first_of_stream(p)

        elif(p_type is TermUnit):
            term = self.get_term(p)
            retorno = self.first_of_non_terminal(term)
        
        elif(p_type is Term):
            retorno = self.first_of_non_terminal(p)

        return retorno     

    def first_of_non_terminal(self, term):
        if(len(term.first) is not 0):
            return term.first

        first = term.first
        for stream in term.right:
            if(len(stream) is 1 and stream[0] is self.textGrammar.EMPTY_UNIT):
                first |= {self.textGrammar.EMPTY_UNIT}
            else:    
                first |= self.first(stream) - {self.textGrammar.EMPTY_UNIT}
        
        term.first = first

        return first

    def first_of_stream(self, stream):
        retorno = set()
        
        for index, item in enumerate(stream):
            if(item.type is TermUnit.NONTERMINAL):
                term = self.get_term(item.text)

                retorno |= self.first(term)
                
                if(self.term_has_empty(term)):
                    continue
                else:                
                    break

            elif(index is 0 and item.type is TermUnit.TERMINAL or item is TextGrammar.EMPTY_UNIT):
                retorno.add(item)
                break
        
        return retorno

    def get_term(self, termString):
        for i in self.Terms:
            if(i.left == termString):
                return i

    def term_has_empty(self, term):
        for stream in term.right:
            for item in stream:
                if(item is TextGrammar.EMPTY_UNIT):
                    return True

        return False

    @staticmethod
    def remove_empty(term_first):
        retorno = []
        for item in term_first:
            if(item is not TextGrammar.EMPTY_UNIT):
                retorno.append(item)
        
        return retorno

    def build_follow(self):
        """
        Routine that creates follow sets of the given grammar
        """
        self.apply_follow_first_rule()
        self.apply_follow_second_rule()
        self.apply_follow_third_rule()
    
    def apply_follow_first_rule(self):
        """
        S.follow = $
        """
        self.StartSimbol.follow.add(self.STREAM_END_UNIT)

    def apply_follow_second_rule(self):
        """
        A -> Alfa B Beta, B.follow += first(Beta) - {ɛ}
        Alfa is any stream
        Beta is a not empty stream
        """
        for term in self.Terms:
            for stream in term.right:
                streamLen = len(stream)

                for index, unit in enumerate(stream):
                    if(unit.type is TermUnit.NONTERMINAL):
                        termB = self.get_term(unit.text)

                        if(streamLen > index + 1):
                            beta = stream[index + 1::]
                            firstBeta = self.first(beta)
                            
                            termB.follow |= set(firstBeta) - {self.textGrammar.EMPTY_UNIT}
                            
    def apply_follow_third_rule(self):
        """
        A -> Alfa B Beta, B.follow += A.follow
        Alfa is any stream
        Beta is a empty stream
        """
        calls = deque()

        for A in self.Terms:
            for stream in A.right:
                streamLen = len(stream)

                for index, unit in enumerate(stream):
                    if(unit.type is TermUnit.NONTERMINAL):
                        B = self.get_term(unit.text)

                        if(A is B):
                            continue

                        if(streamLen > index + 1):
                            beta = stream[index + 1::]

                            firstBeta = self.first(beta)

                            if(TextGrammar.EMPTY_UNIT not in firstBeta):
                                continue
                        
                        # B.follow |= A
                        calls.append((B, A))
        
        while(len(calls) is not 0):
            tupleBA = calls.popleft()
            B, A = tupleBA

            AinStack = next((x for x in calls if x[0] is A), None)

            if(AinStack):
                calls.append(tupleBA)
                continue

            # print(B.left,"___", A.left)

            B.follow |= A.follow

    def __str__(self):
        return str(self.textGrammar.Premises)
# ɛ