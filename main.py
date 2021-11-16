import Sentics
import re
import os
from langdetect import detect

class Songs:

    def __init__(self, path):
        self.path = path

    def Cut_song(self, lines):
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
                              instru = re.search(r'^\[.*\]$',line)
                              if instru != None:
                                    pass
                              else:
                                    lower = line[:-1].lower()
                                    clean1 = re.sub(r'[^a-zA-Z\d\s:]','', lower)
                                    clean2 = re.sub(r'\\u2005',' ',clean1)
                                    is_embed = re.search(r'embedshare urlcopyembedcopy',clean2)
                                    if is_embed == None:
                                        _temp.add(clean2)
                                    else:
                                        unembed = re.sub(r'embedshare urlcopyembedcopy$','',clean2)
                                        _temp.add(unembed)
            if Is_End != None and len(_temp) != 0:
                out[title] = list(_temp)
        return out

    def read_text_file(self, file_path):
        with open(file_path, 'r', encoding='UTF-8') as file:
            Lines = file.readlines()
            out = self.Cut_song(Lines)
            return out

    def get_all_file(self, path):
        Dico = dict()
        for file in os.listdir(path):
            # Check whether file is in text format or not
            if file.endswith(".txt"):

                file_path = f"{path}/{file}"
                Dict = dict()
                # call read text file function
                Dict = self.read_text_file(file_path)

                Dico[file[:-4]] = Dict

        return Dico

    def moy_sentics(self, list_of_list):
        sent1 = sent2 = sent3 = sent4 = int(0)
        for elem in list_of_list:
            sent1 = (float(elem[0]) + sent1)
            sent2 = (float(elem[1]) + sent2)
            sent3 = (float(elem[2]) + sent3)
            sent4 = (float(elem[3]) + sent4)

        if sent1 != 0:
            sent1 = sent1 / len(list_of_list)
        elif sent2 != 0:
            sent2 = sent2 / len(list_of_list)
        elif sent3 != 0:
            sent3 = sent3 / len(list_of_list)
        elif sent4 != 0:
            sent4 = sent4 / len(list_of_list)
        return [sent1, sent2, sent3, sent4]

    def main(self):
        dic = self.get_all_file(self.path)
        artist_sentics = list()
        for artist in dic:
            Song_sentics = list()
            for songs in dic[artist]:
                lines = list()
                for line in dic[artist][songs]:
                    if detect(line) == 'en':
                        l = Sentics.Sentics(line)
                        lines.append(l.main())
                Song_sentics.append(self.moy_sentics(lines))
            artist_sentics.append([artist, Song_sentics])

        return artist_sentics