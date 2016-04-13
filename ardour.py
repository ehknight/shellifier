from __future__ import division
import nltk, re
from nltk.corpus import wordnet as wn
import nltk.data
from random import randrange
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from random import randrange
import unicodedata

loseTense=False #true if lose verbs
nltk.data.path.append('./nltk_data/')

def preProcess(txt):
    txt = txt.replace("\n",".\n")
    txt = txt.replace("..",".")
    txt = txt.replace("Im ","I'm ")
    return txt

def fixStuff(txt):
    txt = txt.replace(' ,',',')
    txt = txt.replace(" '","'")
    txt = txt.replace(" ;",";")
    txt = txt.replace(" :",":")
    txt = txt.replace(" i "," I ")
    txt = txt.replace("gon na","gonna")
    txt = txt.replace("got ta","gotta")
    txt = txt.replace(" n't","n't")
    txt = txt.replace("wan na ","wanna ")
    return txt

def penn2WN(tag):
    # see https://stackoverflow.com/questions/27591621/
    # nltk-convert-tokenized-sentence-to-synset-format
    if tag.startswith("J"):
        return wn.ADJ
    elif tag.startswith("N"):
        return wn.NOUN
    elif tag.startswith("R"):
        return wn.ADV
    elif tag.startswith("V"):
        if loseTense:
            return None
        else:
            return wn.VERB
    return None

def inferSynsets(sentence):
    tagged = pos_tag(word_tokenize(sentence))
    #print tagged
    synsets = []
    lemmatzr = WordNetLemmatizer()
    for token in tagged:
        wn_tag = penn2WN(token[1])
        if not wn_tag:
            synsets.append(token[0])
        else:
            lemma = lemmatzr.lemmatize(token[0], pos=wn_tag)
            try:
                synsets.append(wn.synsets(lemma, pos=wn_tag)[0])
            except IndexError:
                #must be unrecognized words
                synsets.append(str(token[0]))
    return synsets


def shelly(sentence):
    origSentence = sentence[:]
    syn = inferSynsets(sentence)
    newSentence=[]
    newSentence2=[]
    for i in syn:
        try:
            i.name()
            try:
                hypo = i.hyponyms()[randrange(0,len(i.hyponyms())//3+1)]
                lem = hypo.lemmas()[randrange(0,len(i.lemmas())//3+1)].synset()
                if len(str(hypo.name()))<len(str(lem.name())):
                    newSentence.append(lem.name()[:-5])
                else:
                    newSentence.append(str(hypo.name())[:-5])
            except IndexError:
                newSentence.append(str(i.name())[:-5])
        except AttributeError:
            newSentence.append(i)

    for i in syn:
        try:
            i.name()
            try:
                newSentence2.append(str((i.lemmas()[-1]).synset().name())[:-5])
            except IndexError:
                newSentence2.append(i.name()[:-5])
        except AttributeError:
            newSentence2.append(i)

    shellified=[]
    sentenceComp1=[]
    sentenceComp2=[]
    for i in range(len(newSentence)):
        if len(newSentence[i])>len(newSentence2[i]):
            sentenceComp1.append(newSentence[i])
            sentenceComp2.append(newSentence2[i])
        else:
            sentenceComp2.append(newSentence[i])
            sentenceComp1.append(newSentence2[i])
    for i in range(len(newSentence)):
        c1 = sentenceComp1[i]
        c2 = sentenceComp2[i]
        co = origSentence[i]
        if c1 == co:
            shellified.append(c2)
            continue
        if c2 == co:
            shellified.append(c1)
            continue
        if len(c1)>len(c2):
            shellified.append(c1)
            continue
        if len(c2)>=len(c1):
            shellified.append(c2)
            continue
        shellified.append(co)
    return " ".join(shellified)

def main(txt, adv, linebreaks):
    txt=unicodedata.normalize('NFKD', txt).encode('ascii','ignore').splitlines()
    txt = [i.decode("utf8") for i in txt]
    txt = preProcess("\n".join(txt))+" " #extra space bc cuts off last char
    # see https://stackoverflow.com/questions/5534926/
    # to-find-synonyms-defintions-and-example-sentences-using-wordnet
    global loseTense
    loseTense = adv
    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    data = txt
    tmp = tokenizer.tokenize(data)
    #print tmp
    lines=[]
    for x in enumerate(tmp):
        i=x[1]
        if i[-1:]=="\n" and x[0]!=len(tmp)-1:
            lines.append(i[:-2])
        else:
            lines.append(i[:-1])
    shellified=[]
    for i in lines:
        try:
            shellified.append(
                fixStuff(tokenizer.tokenize(shelly(i).replace('_',' '))[0].capitalize())+'.'
            )
        except IndexError:
            shellified.append("")
    if linebreaks==True:
        return "<br>".join(shellified)
    else:
        return " ".join(shellified)
