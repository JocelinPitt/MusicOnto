# Importing the necessary python libraries
import spacy
import senticnet6 as sentic  # A module for sentiment analysis
import senticnet6_polarity as polarity

from sense2vec import Sense2Vec

# English language loaded for reading the text files with spacy.
nlp = spacy.load("en_core_web_sm")


# Defining the "Sentics Class" for all the  sentic rules found at "https://sentic.net/senticnet-6.pdf"

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

    # this function remove non-semantics elements from the phrase and reformat the doc variable from nlp() to in a
    # more usefull shape
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

    # This function reshape the new doc variable and remove prep elements as those carries over their sementicals
    # values to their child
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

    # this function iterate through every child of an meaningful element and try to catch a combine value from the
    # Senticnet dict
    def link_with_child(self, root, list_of_childs):
        global match, sentiments
        list_of_combinaison = list()
        for child in list_of_childs:
            combinaison, match, sentiments = self.check_combinaison(root, child)
            list_of_combinaison.append(combinaison)
        return list_of_combinaison, match, sentiments

    # Defining a function to check all combinations of tokens in senticnet6 and polarity
    def check_combinaison(self, root, child):
        check_sent = False
        check_pol = False
        match = False
        sentics = list()
        sentiments = list()
        polar = int()

        # combine is a combination of two elements (tokens) that are connected with underscore in datasets.
        combine = str(root) + '_' + str(child[0])
        check_sent, check_pol = self.check_dict(combine)

        # This part check for every placement possible between the root and his child (root_child / child_root). If
        # it's not found it will call the most_similar function to get another version of root, then child
        if not (check_sent or check_pol):
            combine = str(child[0]) + '_' + str(root)
            check_sent, check_pol = self.check_dict(combine)
            if not (check_sent or check_pol):
                Ms_root = self.most_similar(root=root)
                combine = str(Ms_root) + '_' + str(child[0])
                check_sent, check_pol = self.check_dict(combine)
                if not (check_sent or check_pol):
                    combine = str(child[0]) + '_' + str(Ms_root)
                    check_sent, check_pol = self.check_dict(combine)
                    if not (check_sent or check_pol):
                        Ms_childs = self.most_similar(child=child)
                        combine = str(Ms_root) + '_' + str(Ms_childs)
                        check_sent, check_pol = self.check_dict(combine)
                        if not (check_sent or check_pol):
                            combine = str(Ms_childs) + '_' + str(Ms_root)
                            check_sent, check_pol = self.check_dict(combine)

        # If something is found the values from the senticnet dict will be passed, otherwise it will pass the null
        # values (0,0,0,0) and polarity = 1. If found, it will also get the major sentiments relatives to the
        # senticnet dict and pass them
        if check_sent:
            match = True
            sentics.append(sentic.senticnet[combine][:4])
            for elem in sentic.senticnet[root][4:6]:
                sentiments.append(elem)
        else:
            sentics.append([0,0,0,0])
        if check_pol:
            match = True
            polar = polarity.senticnet6[combine]
        else:
            polar = 1
        merge = [sentics, polar]
        return merge, match, sentiments

    # This simple function will check if an element exist in the senticnet dict
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

    # This function does the same as check_combinaison but works on single word input
    def raw_sentics(self, root):
        check_sent = False
        check_pol = False
        match = False
        sentics = list()
        sentiments = list()
        polar = int()
        check_sent, check_pol = self.check_dict(root)
        if check_sent:
            match = True
            sentics.append(sentic.senticnet[root][:4])
            for elem in sentic.senticnet[root][4:6]:
                sentiments.append(elem)
        else:
            sentics.append([0,0,0,0])
        if check_pol:
            match = True
            polar = polarity.senticnet6[root]
        else:
            polar = 1
        merge = [sentics, polar]
        return merge, match, sentiments

    # This function will reverse the value we get from the senticnet dict if it found a child with a 'neg' depedancy
    # value
    def Is_neg(self, list_of_child):
        for child in list_of_child:
            if child[2] == 'neg':
                return -1
            else:
                return 1

    # this function will get the most similar value from a given word via the Sense2Vec module. His out is the first
    # match, splited to give back only the word without the pos value. It can work from a single word, we'll then
    # assume that this word is a verb or a noun. Or it can work with a list witch include the Pos value.
    def most_similar(self, child=list(), root=str()):
        s2v = Sense2Vec().from_disk("s2v_reddit_2015_md/s2v_old")
        if root:
            # We suppose ta
            token_deps = ['VERB', 'NOUN']
            best = list()
            for token_dep in token_deps:
                query = str(root) + "|" + str(token_dep)
                if s2v.__contains__(query):
                    out = s2v.most_similar(query)
                    best.append([out[0][0].split('|')[0], out[0][1]])
            if best != []:
                best_conf = max(map(lambda x: x[1], best))
                for elem in best:
                    if elem[1] == best_conf:
                        return elem[0]
            else:
                return root
        if child:
            token = child[0]
            token_dep = child[1]
            # if token not in list((sentic.senticnet.keys())):
            query = str(token) + "|" + str(token_dep)
            if s2v.__contains__(query):
                out = s2v.most_similar(query)
                if out[0][0].split('|')[0]:
                    return out[0][0].split('|')[0]
                else:
                    return child
            else:
                return child

    # This function will get all the sentics values we found and calculate the meanings of those.
    # This procedure may be improve as it's not proven that the mean value as any real utilities.
    def compute_all_sentics(self, dic):
        sent1 = sent2 = sent3 = sent4 = int(0)
        for elem in dic:
            if dic[elem][0] != []:
                sent1 = (float(dic[elem][0][0][0]) + sent1) * int(dic[elem][1])
                sent2 = (float(dic[elem][0][0][1]) + sent2) * int(dic[elem][1])
                sent3 = (float(dic[elem][0][0][2]) + sent3) * int(dic[elem][1])
                sent4 = (float(dic[elem][0][0][3]) + sent4) * int(dic[elem][1])
        if sent1 != 0:
            sent1 = sent1 / len(dic)
        if sent2 != 0:
            sent2 = sent2 / len(dic)
        if sent3 != 0:
            sent3 = sent3 / len(dic)
        if sent4 != 0:
            sent4 = sent4 / len(dic)
        return [sent1, sent2, sent3, sent4]

    # Main function. It get a sentance as input and give out the sentics values calculated and a list of all
    # sentiments found in the sentance
    def main(self):
        datas = self.Tokens()
        sentics = dict()
        all_sentiments = list()
        match = False
        IsNeg = 1
        for data in datas:
            # Work to get sentics when the element is a conjuct. Has prep have been remove, conj childs are to be
            # treaten separatly, if found they prevail over the conj sentics
            if data[1] in ['conj']:
                conj_value = data[0]
                conj_children = [child for child in data[2]]
                match = False
                Meta_match = False
                sentiments = list()
                IsNeg = self.Is_neg(Root_chilrdren)
                for child in conj_children:
                    conj_child_checks, match, sentiments = self.raw_sentics(child[0])
                    if match:
                        if (conj_child_checks != [[[0,0,0,0]], 1]) and (child[0] not in sentics.keys()):
                            sentics[child[0]] = [check * IsNeg for check in conj_child_checks]
                            Meta_match = True
                            for senti in sentiments:
                                all_sentiments.append(senti)
                if not Meta_match:
                    conj_checks, match, sentiments = self.raw_sentics(conj_value)
                    if (conj_checks != [[[0,0,0,0]], 1]) and (conj_value not in sentics.keys()):
                        sentics[conj_value] = [check * IsNeg for check in conj_checks]
                        for senti in sentiments:
                            all_sentiments.append(senti)
            # Work to get sentics when the element (data) is the Root element of the phrase
            else:
                Root_value = data[0]
                Root_chilrdren = [child for child in data[2]]
                sentiments = list()
                IsNeg = self.Is_neg(Root_chilrdren)
                Root_checks, match, sentiments = self.link_with_child(Root_value, Root_chilrdren)
                if not match:
                    Root_checks, match, sentiments = self.raw_sentics(Root_value)
                    if (Root_checks != [[[0,0,0,0]], 1]) and (Root_value not in sentics.keys()):
                        sentics[Root_value] = [check * IsNeg for check in Root_checks]
                        for senti in sentiments:
                            all_sentiments.append(senti)
                    for child in Root_chilrdren:
                        child_checks, match, sentiments = self.raw_sentics(child[0])
                        if (child_checks != [[[0,0,0,0]], 1]) and (child[0] not in sentics.keys()):
                            sentics[child[0]] = [check * IsNeg for check in child_checks]
                            for senti in sentiments:
                                all_sentiments.append(senti)
                else:
                    for child, checks in zip(Root_chilrdren, Root_checks):
                        if (checks != [[[0,0,0,0]], 1]) and (child[0] not in sentics.keys()):
                            sentics[child[0]] = [check * IsNeg for check in checks]
                            for senti in sentiments:
                                all_sentiments.append(senti)

        return self.compute_all_sentics(sentics), all_sentiments
