# Welcome to MusicOnto Project

MusicOnto is a class project where the top 50 English songs in europeen countries are extracted in order to analyse the overall sentiment of each song using ``Senticnet-6`` dataset.

Defining the "Sentics Class" for all the  sentic rules found at "https://sentic.net/senticnet-6.pdf"

This page is created by MkDocs.

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.




This project contains two python files. The first one is Sentics.py that uses modules & a defined class for sentiment analysis of a sentence.
## Functions

#### The Functions of sentics.py are as follows:
For every function, Arg is the input of that function and Return is the output of that function.

* `Tokens`: is a function for nlp analysis  

        Returns:
            (1)children of each root,
            (2)lemma & dependency of each child,
            (3)ignores the tokens with preposition dependency

* `Assemble`: is a function that creates a list of children whose dependency is excluded
        of the list defined in the function (like punctuations and determinations)

        Args:
            doc: nlp analyzed sentence
            childs: the children of the root in each doc

        Returns:
            list: assemble --> a list of selected tokens (children)

* `Ignore_prep`: is a function that reformats the new doc variables and remove prep elements as those carries over their sementicals
        values to their child

        Args:
            linked: a list that contains lemma, dependency and the child (token)

        Returns:
            The reformated linked (list) where the prepositions are deleted.

* `link_with_child`: is a function that uses ``check_combinaison``function in order to iterate over each child
        of a root token to create a list meaningful combinations of roots and their children. It also returns the sentiment
        value of each combination found in ``Senticnet``dataset.

        Args:
            root: a token that other tokens are dependent to it.
            list_of_childs: a list of children for every root.

        Returns:
            list_of_combinaison: a list with all combinations of root & its children
            match: bool: True if successful, False otherwise.
            sentiments: Values for the combinations found in Senticnet dataset

* `check_combinaison`: is a function that verifies all the combinations of tokens in ``Senticnet6``& ``Polarity``
        Datasets.

        Args:
            root: Token whose dependency in nlp is root
            child: the token which is dependent to root

        Returns:
            merge: A list of ``Senticnet`` & ``Polarity`` values for every combination
            match: bool: True if successful, False otherwise.
            sentiments: A list of two first sentiments  for the combinations found in Senticnet dataset

* `Check_dict`: is a simple function for verifying the existence of a token in ``Senticnet`` & ``Polarity``
        datasets.

        Args:
            to_check: Tokens and combinations that their exsitence will be checked in ``Senticnet`` & ``Polarity``
        datasets.

        Returns:
            check_sent : bool: True if successful, False otherwise.
            check_pol : bool: True if successful, False otherwise.

* `Raw_sentics`: is a function that checks the existence of a single token in in ``Senticnet`` & ``Polarity``
        datasets.

        Args:
            root: A token whose presence will be checked in the two datasets.

        Returns:
            merge: A list of ``Senticnet`` & ``Polarity`` values for every combination
            match: bool: True if successful, False otherwise.
            sentiments: A list of two first sentiments  for the combinations found in Senticnet dataset

* `Is_neg`: is a function that will reverse the senticnet value when the child has a neg dependency.

        Args:
            list_of_child: A list of all childs of a root

        Returns:
            int: -1,1

* `most_similar`: is a function that uses the Sense2Vec module in order to find similar words. For the
        simplicity of the work, we assumed that the word that we are searching for its similar meaning is either
        noun or verb.


        Args:
            child: the child of a token root.
            root: The root token

        Returns:
            similar words

* `Compute_all_sentics`: This function will calculate the overall sentiment of a sentence by using the mean calculation.

        Args:
            dic: All of the necessary tokens of the sentence

        Returns:
            The average of sentiments of tokens (and combinations) for a sentence.

* `main`: is a function that analyses a sentence as an input and calculates its
        overall sentiment.

        Returns:
            The overall sentiment of the sentence

## Example