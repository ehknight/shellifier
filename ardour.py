from __future__ import division
import nltk, re
from nltk.corpus import wordnet as wn
import nltk.data
from random import randrange
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize
from random import randrange

loseTense=False #true if lose verbs
nltk.data.path.append('./nltk_data/')

def fixStuff(txt):
    txt = txt.replace(' ,',',')
    txt = txt.replace(" '","'")
    txt = txt.replace(" ;",";")
    txt = txt.replace(" :",":")
    txt = txt.replace(" i ","I")
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
    syn = inferSynsets(sentence)
    newSentence=[]
    newSentence2=[]
    for i in syn:
        try:
            i.name()
            try:
                hypo = i.hyponyms()[randrange(0,len(i.hyponyms()//3+1))]
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
    for i in range(len(newSentence)):
        if randrange(0,2)==1:
            if len(newSentence[i])>=len(newSentence2[i]):
                shellified.append(newSentence[i])
            else:
                shellified.append(newSentence2[i])
        else:
            shellified.append([newSentence[i],newSentence2[i]][randrange(0,2)])
    return " ".join(shellified)

def main(txt, adv):
    # see https://stackoverflow.com/questions/5534926/
    # to-find-synonyms-defintions-and-example-sentences-using-wordnet
    global loseTense
    loseTense = adv
    tokenizer = nltk.data.load("tokenizers/punkt/english.pickle")
    data = txt
    tmp = tokenizer.tokenize(data)
    #print tmp
    lines=[]
    for i in tmp:
        if i[-1:]=="\n":
            lines.append(i[:-2])
        else:
            lines.append(i[:-1])
    shellified=[]
    for i in lines:
        shellified.append(
            fixStuff(tokenizer.tokenize(shelly(i).replace('_',' '))[0].capitalize())+'.'
        )
    return '\n\n'.join(shellified)
