from django.shortcuts import render
from bs4 import BeautifulSoup  #scrap data from webpage
import requests
from nltk.corpus import stopwords #remove common google words like you,yours,etc.
from collections import Counter
from data.models import url_data

def ActionFrequency(request):
    return render(request, 'frequency.html')

def ActionResult(request):

    if request.method == 'POST': #Post request 
 
        url = request.POST['url']
        if url_data.objects.filter( url  = url).exists(): #check if url data present in database or not
            obj = url_data.objects.get(url=url)
            d = obj.result
            d = convert_dict_to_list(d)   #function call
            msg = 'Result from database'
            return render(request, 'result.html', {'d': d,'msg':msg}) #parsing data to html page

        else:
            r = requests.get(url).text
            wordlist =[]
            soup = BeautifulSoup(r,'html.parser')
            for each_text in soup.findAll('div'):
                content = each_text.text

                # use split() to break the sentence into
                # words and convert them into lowercase
                words = content.lower().split()

                for each_word in words:
                    wordlist.append(each_word)
            d = remove_stopwords(wordlist) #remove_stopwords function call
            data = url_data(url = url, result = dict(d)) #object created in url_data model
            data.save()
            return render (request, 'result.html',{'d':d,'msg': 'New Result'})

def remove_stopwords(wordlist):
    en_stops = list(stopwords.words('english'))
    symbols = '''!@#$%^&*()_-+=~`:<>?|}{[],./;'"'''
    digits = '0123456789'
    articles = ['a','the','an']
    
    word_count = {}
    for word in wordlist:
        if word in en_stops:
            wordlist.remove(word)
        if word in symbols:
            wordlist.remove(word)
        if word in digits:
            wordlist.remove(word)
        if word in articles:
            wordlist.remove(word)

    for word in wordlist:  #counting frequency of each word in wordlist and adding it to dictionary
        if word in word_count:
            word_count[word] +=1
        else:
            word_count[word] = 1

    c = Counter(word_count)
    top = c.most_common(10) #getting top 10 most common words
    
    return(top)

def convert_dict_to_list(dict):  #converting dictionary to list
    l = list(dict.items())
    return (l)

