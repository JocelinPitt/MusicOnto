# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

* `mkdocs new [dir-name]` - Create a new project.
* `mkdocs serve` - Start the live-reloading docs server.
* `mkdocs build` - Build the documentation site.
* `mkdocs -h` - Print help message and exit.

## Project layout

    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.



## Functions

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

