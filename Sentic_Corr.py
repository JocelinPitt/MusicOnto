# Importing the necessary python libraries
import spacy
import senticnet6 as sentic  # A module for sentiment analysis
import senticnet6_polarity as polarity

# English language loaded for reading the text files with spacy.
nlp = spacy.load("en_core_web_sm")


# Defining the "Sentics Class" for all the  sentic rules found at "https://sentic.net/senticnet-6.pdf"

class Sentics:

    def __init__(self, text):
        self.text = text

    # Defining get_tokens function
    def Tokens(self):
        doc = nlp(self.text)
        global hierarchy, KeepGoing, to_get, CoC
        hierarchy = []
        KeepGoing = True
        To_Get = []
        CoC = []

        for token in doc:

            if token.dep_ == 'ROOT':

                Root_childs = [child for child in token.children]
                To_Get, CoC, KeepGoing = self.Assemble_and_COC(doc, Root_childs)
                print(To_Get)
                hierarchy.append(To_Get)
                for i in range(len(CoC)):
                    while KeepGoing != False:
                        to_get = []
                        coc = []
                        to_get, coc, KeepGoing = self.Assemble_and_COC(doc, coc)
                        print("While : " + str(to_get))
                        print(str(KeepGoing))
                        if to_get != None:
                            hierarchy.append(to_get)

        print(hierarchy)

    def Assemble_and_COC(self, doc, childs=None):
        to_get = []
        CoC = []
        KeepGoing = False
        if childs is None:
            childs = []
        for child in childs:
            position = 0
            for token in doc:
                if child.text == token.text:
                    if token.dep_ not in ['punct', 'det', 'conj', 'cc', 'cc:preconj', 'list', 'dislocated', 'parataxis',
                                          'orphan', 'reparandum', 'case']:
                        to_get = [position, token.lemma_, token.pos_, token.dep_]
                        CoC = [c for c in token.children]
                        print('Assemble : ' + str(CoC))
                        if CoC != []:
                            KeepGoing = True
                        else:
                            KeepGoing = False
                position += 1

        return to_get, CoC, KeepGoing

    def get_tokens(self):
        # Reading the sentence
        doc = nlp(self.text)
        # Dependancy parsing
        # Finding lemma of each token in the sentence
        token_lemma = [token.lemma_ for token in doc]
        # Tokenizing the sentence
        token_text = [token.text for token in doc]
        # Dependancy of each token in a sentence
        token_dep = [token.dep_ for token in doc]
        # Defining an empty list for all children of the root
        token_children = list()
        token_sentic = list()

        # Appending all children to the list
        for token in doc:
            token_children.append([child for child in token.children])
            # we will search each token in the senticnet6 data,
            if token in sentic.senticnet.keys():
                # if the token is found in both senticnet6 and polarity data,
                # the senticnet and polarity data of the token will be added to the token_sentic list.
                if token in polarity.senticnet6.keys():
                    token_sentic.append([sentic.senticnet[token[:4]], polarity.senticnet6[token[:4]]])
                # otherwise, if the token is just found at senticnet6, only the senticnet values will be added to the
                # list.
                else:
                    token_sentic.append([sentic.senticnet[token[:4]], 1])
            # if the token is not found in senticnet6 library:
            else:
                # if the token has a polarity, we will consider null values for the senticnet and we will add the
                # polarity values
                if token in polarity.senticnet6.keys():
                    token_sentic.append([[0, 0, 0, 0], polarity.senticnet6[token[:4]]])
                # if the token neither senticnet values nor polarity values, the token will added with senticnet null
                # values and is considered with polarity 1.
                else:
                    token_sentic.append([[0, 0, 0, 0], 1])
        # The out is defined to have a list of the analysis of all tokens in the sentence.

        out = [token_lemma, token_text, token_dep, token_children, token_sentic]

        # Remove elem that are not useful in sentics analysis
        count = 0
        for elem in out[2]:
            if elem != ['punct', 'det', 'conj', 'cc', 'cc:preconj', 'list', 'dislocated', 'parataxis', 'orphan',
                        'reparandum', 'case']:
                count += 1
            else:
                for type in out:
                    type.pop(count)
                    count += 1

        # Transform children value to index in sentance
        count = 0
        my_dict = dict()
        for elem in token_text:
            my_dict[elem] = count
            count += 1

        print(out)

        child_by_index = list()
        for elem in out[3]:
            count = 0
            for child in elem:
                if child.text in list(my_dict.keys()):
                    child_by_index.append(my_dict[child.text])
                count += 1
                out.append(child_by_index)
            child_by_index = list()

        print(out)

        return out

    def find_first(self, input):
        pass

    # Defining a function to check all combinations of tokens in senticnet6 and polarity
    @staticmethod
    def check_combinaison(elem1, elem2):
        combine = str(elem1) + '_' + str(elem2)
        _temp_sentics = list()
        combine_sentics = list()
        match = True
        # If the combination exists in enticnet & polarity, the both data will be appended to the list.
        if combine in sentic.senticnet.keys():
            if combine in polarity.senticnet6.keys():
                _temp_sentics.append([sentic.senticnet[combine[:4]], polarity.senticnet6[combine[:4]]])
            # If the combination is not found in polarity, the porilty is assumed 1.
            else:
                _temp_sentics.append([sentic.senticnet[combine[:4]], 1])
        # When the combination is found in neither datasets:
        else:
            match = False
            _temp_sentics.append([[0, 0, 0, 0], 1])

        combine_sentics.append(_temp_sentics)

        return match, combine_sentics

    def try_with_lemma(self, elem1, elem2):
        tokens = self.get_tokens()

        for token in tokens:
            if token[1] == str(elem1):
                elem1 = token[0]
            elif token[1] == str(elem2):
                elem2 = token[0]
            else:
                pass

        return elem1, elem2

    # Finding the ROOT in tokens
    def find_root(self):
        tokens = self.get_tokens()

        for token in tokens:
            if token[2] == 'ROOT':
                return token

    # Finding the combination of childs:
    def link_with_child(self, list_of_childs):
        match = False
        combi_sent = list_of_childs
        tok_lem = [list_of_childs[1], list_of_childs[0]]
        for test in tok_lem:
            for child in list_of_childs[3]:
                match, combi_sent = self.check_combinaison(test, child)
                if match:
                    break

            if not match:
                for child in list_of_childs[3]:
                    match, combi_sent = self.check_combinaison(child, test)
                    if match:
                        break

        return match, combi_sent

    # applyrule function:
    @staticmethod
    def apply_rule(dependancy, elem, link_elem='None', merge=None):
        # 1. when the combination is not not in datasets:
        if merge is None:
            merge = [[0, 0, 0, 0], 1]
        out = list()
        pol = int()
        # 2. when the combination is in the dataset:
        if merge != [[0, 0, 0, 0], 1]:
            # checking the dependancy type:
            if dependancy in ['nsubj', 'nsubjpass', 'obj', 'iobj', 'csubj', 'csubjpass', 'ccomp', 'xcomp', 'nummod',
                              'appos', 'nmod', 'acl', 'acl:relcl', 'amod', 'det', 'nmod', 'nmod:npmod', 'nmod:tmod',
                              'nmod:poss', 'advcl', 'advmod', 'conj', 'cc', 'cc:preconj']:
                pol = merge[1]
            elif dependancy in ['neg']:
                pol = merge[1] * -1

            sentiment = merge[0]
        # when combination is in senticnet6 & polarity Datasets:
        else:
            if dependancy in ['nsubj', 'nsubjpass', 'obj', 'iobj', 'csubj', 'csubjpass', 'ccomp', 'xcomp', 'nummod',
                              'appos', 'nmod', 'acl', 'acl:relcl', 'amod', 'det', 'nmod', 'nmod:npmod', 'nmod:tmod',
                              'nmod:poss', 'advcl', 'advmod', 'conj', 'cc', 'cc:preconj']:
                if link_elem in list(polarity.senticnet6.keys()):
                    pol = polarity.senticnet6[link_elem]
                else:
                    pol = 1
            elif dependancy in ['neg']:
                if link_elem in list(polarity.senticnet6.keys()):
                    pol = polarity.senticnet6[link_elem] * -1
                else:
                    pol = -1
            if elem in list(sentic.senticnet.keys()):
                sentiment = sentic.senticnet[elem][:4]
            else:
                if link_elem in list(sentic.senticnet.keys()):
                    sentiment = sentic.senticnet[link_elem][:4]
                else:
                    sentiment = [1, 1, 1, 1]
        # Sentiment Calculation:
        for sent in sentiment:
            value = sent * pol
            out.append(value)

        return out

    @staticmethod
    # Calculating the overall sentiment:
    def compute_all_sentics(sent):
        sent1 = sent2 = sent3 = sent4 = 1
        for elem in sent:
            sent1 = sent1 * elem[0]
            sent2 = sent2 * elem[1]
            sent3 = sent3 * elem[2]
            sent4 = sent4 * elem[3]

        final = [sent1, sent2, sent3, sent4]
        return final

    # Main function
    def main(self):
        tokens = self.get_tokens()
        sent = list()
        # For combination of root and the childs, if the match is found in datasets, the overall sentiment
        # is calculated using the functions previously defined.
        for token in tokens:
            if len(token[3]) == 1:
                sent_value = self.apply_rule(token[2], token, link_elem=token[3][0])
                sent.append(sent_value)
            if len(token[3]) >= 1 and token[2] != 'ROOT':
                dep = token[2]

                match, combi_sent = self.link_with_child(token)
                if match:
                    sent_value = self.apply_rule(dep, token, merge=combi_sent)
                    sent.append(sent_value)
                else:
                    for child in token[3]:
                        sent_value = self.apply_rule(dep, token, link_elem=child)
                        sent.append(sent_value)

        out = self.compute_all_sentics(sent)
        return out


'''
    def most_similar(self, out):
        s2v = Sense2Vec().from_disk("s2v_reddit_2015_md/s2v_old")
        for token, token_dep in out:
            if token not in list((sentic.senticnet.keys()):
               query = str(token) + "|" + str(token_dep)
               vector = s2v[query]

        return vector


POS tag

test ' je mange une pomme'
token=[[je, [[mange, ROOT, VERB]],[mange, [[je, pron, POS], [pomme, DET, POS]]],]]

for elem in token:
    elem1 = [ROOT, je, [[CHIDS - DEP - POS]]]
    elem2 = mange [CHIDS - DEP -POS]

    je je pron [Child], [Sentics] [position] [POS]

    mange -> child pomme et je --> que prendre je car je 1st


    cherche ROOT -> child Root -> child child
    --> 1st [ROOT]
    [Root child1 ]
    coc1 1
    coc1 2
    [root child2]
    coc2 1
    coc2 2
    
    1
        2
        2
            3
            3
        2
            3
            
    '''
