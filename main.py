import Sentics
import re
import os
from collections import Counter
import statistics as stat
import tqdm
from langdetect import detect


class Songs:

    def __init__(self, path):
        self.path = path

    # This function will take a song from a file made of lists of songs lyrics we get with genius and spotipy API and
    # will cut it into a dict with the following structure: {artiste: [[set_of_line_of_song1],[set_of_line_of_song2],
    # [etc]]}
    def Cut_song(self, lines):
        """

                Args:
                    lines:

                Returns:

                """
        out = dict()
        for line in lines:
            if len(line) == 0:
                pass
            else:
                Is_title = re.search(r"^Song title:w*\n?", line)
                Is_End = re.search(" ?<!EndofText!>", line)
                if Is_title != None:
                    title = line[12:-1]
                    _temp = set()
                elif Is_title == None and Is_End == None:
                    if line == '' or line == '\n':
                        pass
                    else:
                        instru = re.search(r'^\[.*\]$', line)
                        if instru != None:
                            pass
                        else:
                            lower = line[:-1].lower()
                            clean1 = re.sub(r'[^a-zA-Z\d\s:]', '', lower)
                            clean2 = re.sub(r'\\u2005', ' ', clean1)
                            is_embed = re.search(r'embedshare urlcopyembedcopy', clean2)
                            if is_embed == None:
                                _temp.add(clean2)
                            else:
                                unembed = re.sub(r'embedshare urlcopyembedcopy$', '', clean2)
                                _temp.add(unembed)
            if Is_End != None and len(_temp) != 0:
                out[title] = list(_temp)
        return out

    # This function is a intermediary to sequentialy open files.
    def read_text_file(self, file_path):
        """

        Args:
            file_path:

        Returns:

        """
        with open(file_path, 'r', encoding='UTF-8') as file:
            Lines = file.readlines()
            out = self.Cut_song(Lines)
            return out

    # This function will iterate through a folder to catch any text file (songs) and pass them to the cut_song
    # function (via read_text_file funct)
    def get_all_file(self, path):
        """

        Args:
            path:

        Returns:

        """
        Dico = dict()
        for file in os.listdir(path):
            # Check whether file is in text format or not
            if file.endswith(".txt"):
                file_path = f"{path}/{file}"
                Dict = dict()
                # call read text file function
                Dict = self.read_text_file(file_path)

                Dico[file[:-4]] = Dict
        print("Dico done !")
        return Dico

    # This function does the same a the Sentics.compute_all_sentics() but is modify to work with a list of sentics
    # from all the lines of a song
    def moy_sentics(self, list_of_list):
        """

        Args:
            list_of_list:

        Returns:

        """
        sent1 = list()
        sent2 = list()
        sent3 = list()
        sent4 = list()
        for elem in list_of_list:
            if elem != []:
                sent1.append(float(elem[0]))
                sent2.append(float(elem[1]))
                sent3.append(float(elem[2]))
                sent4.append(float(elem[3]))
        if sent1 != []:
            sent1 = stat.mean(sent1)
        if sent2 != []:
            sent2 = stat.mean(sent2)
        if sent3 != []:
            sent3 = stat.mean(sent3)
        if sent4 != []:
            sent4 = stat.mean(sent4)
        return [sent1, sent2, sent3, sent4]

    # This is the main function. It will read the text files, make the dic of dic. Work through every song found. For
    # every line of every song, if the sentence is in english, it will pass it as a Sentics class elem. find the main()
    # value. Then append everything it has found in a single output, same goes for the sentiments found.
    def main(self):
        """

        Returns:

        """
        dic = self.get_all_file(self.path)
        artist_sentics = list()
        indice = 0
        for artist in tqdm.tqdm(dic):
            print("Start with " + str(artist))
            Song_sentics = list()
            Songs_sentiments = list()
            for songs in tqdm.tqdm(dic[artist]):
                print("Doing " + str(songs))
                lines = list()
                Song_sentiments = list()
                for line in dic[artist][songs]:
                    try:
                        if detect(line) == 'en':
                            l = Sentics.Sentics(line)
                            Line_sentics, line_sentiments = l.main()
                            lines.append(Line_sentics)
                            for elem in line_sentiments:
                                Song_sentiments.append(elem)
                    except:
                        pass
                Song_sentics.append(self.moy_sentics(lines))
                Songs_sentiments.append(Song_sentiments)
            artist_sentics.append([artist, Song_sentics])
            with open("Out_artist/" + str(artist) + ".txt", encoding="utf-8", mode='a') as f:
                for sentic, sentiments, songs in zip(Song_sentics, Songs_sentiments, dic[artist]):
                    Count = Counter(sentiments)
                    f.write(str(songs) + " :\n" +
                            "Sentics : " + str(sentic) + "\n" +
                            "Sentiments : " + str(sentiments) + "\n" +
                            str(Count) + "\n\n")
            f.close()
            print(str(artist) + " is done !\n" +
                  str(indice))
            indice += 1

        print()
