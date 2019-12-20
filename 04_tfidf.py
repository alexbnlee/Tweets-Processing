def get_tfidf(corpus):
    from sklearn.feature_extraction.text import TfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer
    import nltk
    from nltk.corpus import stopwords

    vectorizer=CountVectorizer()
    transformer = TfidfTransformer()
    # tfidf
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))

    # words vector
    names_list = vectorizer.get_feature_names()

    # get tfidf array
    tfidf_array = tfidf.toarray()
    
    # get stopwords
    stopwords = stopwords.words('english')
    
    # get part of speech
    tokens = nltk.word_tokenize(' '.join(corpus))
    tagged = dict(nltk.pos_tag(tokens))
    # lists of dropping part of speech
    d_pos = ['IN', 'CC', 'CD', 'JJ', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS']
    
    # get the specific name of matrix
    words_ranking = []
    for i in range(len(tfidf_array)):
        for j in range(len(tfidf_array[i])):
            if tfidf_array[i][j] != 0 and names_list[j] not in stopwords and \
            names_list[j] in tagged.keys() and tagged[names_list[j]] not in d_pos:
                words_ranking.append((names_list[j], tfidf_array[i][j]))

    # sort the tfidf from max to min
    import operator
    words_ranking.sort(key=operator.itemgetter(1), reverse=True)
    print(len(words_ranking))
    for wr in words_ranking:
        print(wr)
        
article2 = """
Flu trends in Australia
Influenza, or 'the flu', is a highly contagious respiratory illness. It's a common cause of hospitalisation and leads to thousands more GP visits every year. Many people die annually from complications of the flu in Australia.
While you can catch the flu at any time, it's more likely to happen in the colder months of the year (April to October). The flu season typically peaks in August, but laboratory-confirmed cases of influenza have been higher than usual so far this year — as have calls about flu-related symptoms to the healthdirect helpline.
Early signs of the flu can include cough, sore throat, sinusitis or fever. 
Flu-related calls to healthdirect
Healthdirect Australia collects data based on flu-related calls to the healthdirect helpline (1800 022 222). This information is used to publish the flu 'trend' graph, below.
The blue line in the graph shows flu-related calls to the helpline for the current year, in proportion to all calls. The grey shaded area in the graph shows the range of flu-related calls between 2013 and 2018.
If the blue line is above the grey area, then this may indicate an increased risk of colds and flu in the community.
Flu trend report for health professionals
Health professionals can use this interactive report to get more data on flu-related calls to the healthdirect helpline, from January 2012 to the present.
The influenza syndromic surveillance report is updated twice a week between April and October, and less frequently during the warmer months.
7 ways to fight the flu
Follow these easy tips to help prevent the spread of flu.
Get a flu shot
It is important to get the influenza vaccination each year to continue to be protected, since it wears off after 3 to 4 months and flu strains (types) change over time.
Wash your hands
In addition to vaccination, good hygiene is one of the best ways to help prevent flu and other illnesses from spreading. Wash your hands regularly.
Cover coughs and sneezes
Cover your mouth and nose when coughing or sneezing.
Bin your tissues
Throw used tissues in the bin immediately.
Avoid sharing
Don't share cups, plates, cutlery and towels with other people, if you can.
Keep surfaces clean
Clean surfaces such as your keyboard, phone and door handles regularly to get rid of germs.
Self-care at home
In most cases, you can treat mild flu or cold symptoms at home.
NOTE: Antibiotics won't help
Antibiotics do not reduce symptoms of flu or a cold, as these illnesses are caused by viruses. Antibiotics only work for bacterial infections.
"""
articles = [article2]
get_tfidf(articles)
