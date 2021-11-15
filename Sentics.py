# Importing the necessary python libraries
import spacy
import senticnet6 as sentic  # A module for sentiment analysis
import senticnet6_polarity as polarity

from sense2vec import Sense2Vec

# English language loaded for reading the text files with spacy.
nlp = spacy.load("en_core_web_sm")


# Defining the "Sentics Class" for all the  sentic rules found at "https://sentic.net/senticnet-6.pdf"

'''class Sentics:

    def __init__(self, text):
        self.text = text

    # Defining get_tokens function

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
        return out

    # Defining a function to check all combinations of tokens in senticnet6 and polarity
    @staticmethod
    def check_combinaison(elem1, elem2):
        combine = str(elem1) + '_' + str(elem2)
        _temp_sentics = list()
        combine_sentics = list()
        match = True

        if combine in sentic.senticnet.keys():
            if combine in polarity.senticnet6.keys():
                _temp_sentics.append([sentic.senticnet[combine[:4]], polarity.senticnet6[combine[:4]]])
            else:
                _temp_sentics.append([sentic.senticnet[combine[:4]], 1])
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

    def find_root(self):
        tokens = self.get_tokens()

        for token in tokens:
            if token[2] == 'ROOT':
                return token

    def link_with_child(self, list_of_childs):
        match = False
        combi_sent = list_of_childs()
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

    @staticmethod
    def apply_rule(dependancy, elem, link_elem='None', merge=None):
        if merge is None:
            merge = [[0, 0, 0, 0], 1]
        out = list()
        pol = int()
        if merge != [[0, 0, 0, 0], 1]:
            if dependancy in ['nsubj', 'nsubjpass', 'obj', 'iobj', 'csubj', 'csubjpass', 'ccomp', 'xcomp', 'nummod',
                              'appos', 'nmod', 'acl', 'acl:relcl', 'amod', 'det', 'nmod', 'nmod:npmod', 'nmod:tmod',
                              'nmod:poss', 'advcl', 'advmod', 'conj', 'cc', 'cc:preconj']:
                pol = merge[1]
            elif dependancy in ['neg']:
                pol = merge[1] * -1

            sentiment = merge[0]
        else:
            if dependancy in ['nsubj', 'nsubjpass', 'obj', 'iobj', 'csubj', 'csubjpass', 'ccomp', 'xcomp', 'nummod',
                              'appos', 'nmod', 'acl', 'acl:relcl', 'amod', 'det', 'nmod', 'nmod:npmod', 'nmod:tmod',
                              'nmod:poss', 'advcl', 'advmod', 'conj', 'cc', 'cc:preconj']:
                if link_elem in polarity.senticnet6.keys():
                    pol = polarity.senticnet6[link_elem]
                else:
                    pol = 1
            elif dependancy in ['neg']:
                if link_elem in polarity.senticnet6.keys():
                    pol = polarity.senticnet6[link_elem] * -1
                else:
                    pol = -1
            if elem in sentic.senticnet.keys():
                sentiment = sentic.senticnet[elem][:4]
            else:
                if link_elem in sentic.senticnet.keys():
                    sentiment = sentic.senticnet[link_elem][:4]
                else:
                    sentiment = [1, 1, 1, 1]

        for sent in sentiment:
            value = sent * pol
            out.append(value)

        return out

    @staticmethod
    def compute_all_sentics(sent):
        sent1 = sent2 = sent3 = sent4 = 1
        for elem in sent:
            sent1 = sent1 * elem[0]
            sent2 = sent2 * elem[1]
            sent3 = sent3 * elem[2]
            sent4 = sent4 * elem[3]

        final = [sent1, sent2, sent3, sent4]
        return final

    def main(self):
        tokens = self.get_tokens()
        sent = list()
        for token in tokens:
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
class Sentics:

    def __init__(self, text):
        self.text = text

    # Defining get_tokens function
    def Tokens(self):
        doc = nlp(self.text)
        linked = list()
        for token in doc:
            assemble = list()

            children = [child for child in token.children]
            if children != []:
                assemble = self.Assemble(doc, children)
            if assemble != []:
                linked.append([token.lemma_, token.dep_, assemble])

        for elem in linked:
            if elem[1] == 'prep':
                self.Ignore_prep(linked)
        return linked

    def Assemble(self, doc , childs):
        assemble = list()
        for child in childs:
            to_get = list()
            for token in doc:
                if child.text == token.text:
                    if token.dep_ not in ['punct', 'NUM', 'det', 'cc', 'cc:preconj', 'list', 'dislocated', 'parataxis',
                                          'orphan', 'reparandum', 'case']:
                        to_get = [token.lemma_, token.pos_, token.dep_]
            if to_get != []:
                assemble.append(to_get)
        return assemble

    def Ignore_prep(self, linked):
        remember_elem = None
        remember = None
        remember_pos = int()
        count = int()
        for elem in linked:
            if remember == None:
                if elem[1] != 'prep':
                    count_child = 0
                    for child in elem[2]:
                        if child[2] == 'prep':
                            remember_elem = count
                            remember_pos = count_child
                            remember = child
                        count_child += 1
            if remember != None:
                if remember[0] == elem[0]:
                    if len(elem[2]) == 1:
                        linked[remember_elem][2][remember_pos] = elem[2][0]
                        linked.pop(count)
                        remember_elem = None
                        remember = None
                        remember_pos = int()
            count += 1

    def link_with_child(self, root, list_of_childs):
        list_of_combinaison = list()

        for child in list_of_childs:
            combinaison, match = self.check_combinaison(root, child)
            list_of_combinaison.append(combinaison)

        return list_of_combinaison, match

    # Defining a function to check all combinations of tokens in senticnet6 and polarity
    def check_combinaison(self, root, child):
        check_sent = False
        check_pol = False
        match = False
        sentics = list()
        polar = int()

        # combine is a combination of two elements (tokens) that are connected with underscore in datasets.
        combine = str(root) + '_' + str(child[0])

        check_sent, check_pol = self.check_dict(combine)

        if not (check_sent or check_pol):
            combine = str(child[0]) + '_' + str(root)
            check_sent, check_pol = self.check_dict(combine)
            if not (check_sent or check_pol):
                #most value ....
                pass

        if check_sent:
            match = True
            sentics.append(sentic.senticnet[combine][:4])
        else:
            sentics.append([0,0,0,0])

        if check_pol:
            match = True
            polar = polarity.senticnet6[combine]
        else:
            polar = 1

        merge = [sentics, polar]

        return merge, match

    def check_dict(self, to_check):
        check_sent = False
        check_pol = False

        if to_check in sentic.senticnet.keys():
            check_sent = True
        else:
            check_sent = False

        if to_check in polarity.senticnet6.keys():
            check_pol = True
        else:
            check_pol = False

        return check_sent, check_pol

    def raw_sentics(self, root):
        check_sent = False
        check_pol = False
        match = False
        sentics = list()
        polar = int()

        check_sent, check_pol = self.check_dict(root)

        if check_sent:
            match = True
            sentics.append(sentic.senticnet[root][:4])
        else:
            sentics.append([0,0,0,0])

        if check_pol:
            match = True
            polar = polarity.senticnet6[root]
        else:
            polar = 1

        merge = [sentics, polar]

        return merge, match

    def Is_neg(self, list_of_child):
        for child in list_of_child:
            if child[2] == 'neg':
                return -1
            else:
                return 1

    def most_similar(self, out= list(), root= str()):
        #query = str()
        s2v = Sense2Vec().from_disk("s2v_reddit_2015_md/s2v_old")
        if root:
            #on suppose que root c est toujours soit un VERB soit NOUN --> meme si cest pas vrai (car marche root, mais pas entre les childs)
            token_deps = ['VERB', 'NOUN']
            for token_dep in token_deps:
                query = str(root) + "|" + str(token_dep)
                vector = s2v[query]
                return vector
        if out:
            token = out[0]
            token_dep = out[1]
            #if token not in list((sentic.senticnet.keys())):
            query = str(token) + "|" + str(token_dep)
            vector = s2v[query]
            return vector[0]

    # Main function
    def main(self):
        datas = self.Tokens()
        sentics = list()
        match = False
        IsNeg = 1

        for data in datas:
            print(data)
        print(len(datas))

        for data in datas:
            # Work to get sentics when the element is a conjuct. Has prep have been remove, conj childs are to be
            # treaten separatly, if found they prevail over the conj senitcs
            if data[1] in ['conj']:
                conj_value = data[0]
                conj_children = [child for child in data[2]]
                match = False
                Meta_match = False

                IsNeg = self.Is_neg(Root_chilrdren)

                for child in conj_children:
                    conj_child_checks, match = self.raw_sentics(child[0])

                    if match:
                        sentics.append([[check * IsNeg for check in conj_child_checks], match])
                        Meta_match = True

                if not Meta_match:
                    conj_checks, match = self.raw_sentics(conj_value)

                    sentics.append([[check * IsNeg for check in conj_checks], match])

            # Work to get sentics when the element (data) is the Root element of the phrase
            else:
                Root_value = data[0]
                Root_chilrdren = [child for child in data[2]]

                IsNeg = self.Is_neg(Root_chilrdren)

                Root_checks, match = self.link_with_child(Root_value, Root_chilrdren)

                if not match:
                    Root_checks, match = self.raw_sentics(Root_value)

                sentics.append([[check*IsNeg for check in Root_checks], match])

        return sentics
