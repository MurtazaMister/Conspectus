import re
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np

# file = "article.txt"
    # This function will be used to convert a text file into clean sentences, removing all the non letter token
    # including newlines and tabspaces

def clean_text(document):
    # document = ""
    # with open(file) as my_file:
    #     document = my_file.read()
    sentences = document.split(".")
    cleaned_sentences = []
    for sen in sentences:
        temp = re.sub('[^a-zA-Z0-9]', " ", str(sen))
        temp = re.sub('[\s+]', " ", temp)
        temp = re.sub(' +', ' ', temp)
        temp = temp.lower()
        cleaned_sentences.append(temp)
    cleaned_sentences.pop()
    return cleaned_sentences

def original_sentences(document):
    sentences = document.split(".")
    return sentences

def extractor(document):
    print("REceived: ",document)
    corpus = clean_text(document)
    orig_sentences = original_sentences(document)
    print("Length: ", len(corpus))

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)

    # print(vectorizer.get_feature_names_out())
    # print()
    # print(X.toarray())

    word_counts = X.toarray()

    # creating DataFrame of countvectorizer  
    df = pd.DataFrame(word_counts, columns=vectorizer.get_feature_names_out())
    # df

    #  calculating the word count for each word in document
    total_wc = df.sum()
    # type(total_wc)

    total_wc_df = pd.DataFrame(total_wc[total_wc.index], columns = ["Sum"])
    print("total_wc_df", total_wc_df)

    total_wc_sentences = df.sum(axis=1)
    # total_wc_sentences
    total_wc_sentence_df = df.copy(deep=True)

    total_wc_sentence_df["Total_wc"] = total_wc_sentences
    print("total_wc_sentence_df.head()", total_wc_sentence_df.head())

    # df.iloc[0][1]

    print("len(df)",len(df))

    # calculating TF value
    # df.iloc[0][1]

    tf_df = pd.DataFrame(columns=vectorizer.get_feature_names_out(), index=np.arange(0,len(df),1) )

    for sentence in range(len(df)):
        for word in range(len(df.iloc[sentence])):
            tf_df.iloc[sentence][word] = df.iloc[sentence][word] / total_wc_sentence_df.iloc[sentence]["Total_wc"]
        

    # tf_df
    idf_helper_df = pd.DataFrame(columns = vectorizer.get_feature_names_out())

    for column in idf_helper_df.columns:
        idf_helper_df[column] = df[column] > 0
        
    idf_helper_df

    idf_helper_df.sum()

    idf_df = pd.DataFrame(index = vectorizer.get_feature_names_out())
    idf_df["word_occurance"] = idf_helper_df.sum()

    # idf_df

    idf_df["idf"] = np.log((len(df) + 1) / (idf_df["word_occurance"] + 1))
    # idf_df

    tf_idf_df = pd.DataFrame(columns = vectorizer.get_feature_names_out(), index=np.arange(0,len(df),1))

    for sentence in range(len(df)):
        for word in range(len(df.iloc[sentence])):
            tf_idf_df.iloc[sentence][word] = tf_df.iloc[sentence][word] * idf_df["idf"][word]
    #           tf_idf_helper_df.iloc[sentence][word] = 0

    # tf_idf_df

    tf_idf_df["Sentence_weight"] = tf_idf_df.sum(axis=1)
    print("tf_idf_df.head()",tf_idf_df.head())

    avg_sentence_weights = tf_idf_df["Sentence_weight"].median()
    # avg_sentence_weights

    selection_factor = 0.9
    selected_sentences = tf_idf_df[tf_idf_df["Sentence_weight"] > selection_factor * avg_sentence_weights].index.values
    # selected_sentences

    summary = ". ".join([orig_sentences[i] for i in selected_sentences])
    print("Returning: ", summary)
    return summary

# summary = extractor("""Five terrorists neutralised, 4 including 2 police personnel killed in attack on police chief's office in Pak's Karachi World News Published on Feb 18, 2023 05:49 AM IST There were conflicting reports on the number of terrorists who attacked and entered the building but police sources put their number down to eight. Five heavily-armed militants of the Tehreek-e-Taliban (Pakistan) have been killed after security forces managed to secure back control of the head office building of the Karachi Police Chief which came under a daring attack by the militants in the country's most populous city. The nearly four-hour-long operation to seize back control of the five-storey building came to a dramatic end around 10.50 pm with four other people including two police constables, a rangers personnel and a civilian also killed in the heavy exchange of firing that took place between the TTP militants and security forces. Also Read| 3 militants among seven killed in attack on Karachi police station; operation concludes A senior security source said five terrorists were killed during the operation. He said three were killed in the long gun battle while two blew themselves up which also caused some damage to one floor of the building. Sindh government spokesperson Murtaza Wahab said on Twitter he could confirm that the Karachi Police Office (KPO) building has been cleared. "Three terrorists have been neutralised," he said. He added four other people comprising the two policemen, rangers personnel and a civilian had been killed while 17 others were admitted to hospital with injuries. There were conflicting reports on the number of terrorists who attacked and entered the building but police sources put their number down to eight. "A clear picture will be known tomorrow as the combing and clean up operation is being carried out meticulously in the building after taking control," a senior police official said. "But the identification process is still going on it will be a while before we can say exactly how many terrorists attacked the building," he said. Senior Police Official, DIG South Irfan Baloch said they also found two cars with their doors open one at the back entrance of the building and one at the front in which the terrorists came around 7.10 pm on Friday," he said. Baloch said the bomb disposal squad had combed both cars for explosive devices and also the suicide vests of the terrorists. "They came prepared for a stand off and had sophisticated weapons and explosives, They managed to get into the building wearing police uniforms". The attack comes as a big concern and embarrassment for the provincial government as the Karachi Police Chief office and the Saddar police station are located on the main Shahrah-e-Faisal road which serves as Karachi's main thoroughfare with a number of strategic installations, including the Pakistan Airforce's Faisal Base — and five star hotels in close proximity. Overseas cricket players who are currently competing in the Pakistan Super League are staying in these hotels with Karachi to host matches on Saturday and Sunday. But the Sindh Chief Minister, Syed Murad Ali Shah said the PSL matches would not be affected by the incident. A senior police official said as soon as the terror attack took place, security had been increased at the team hotels and also at the National Stadium where matches are taking place. The police closed down the Shahrah-e-Faisal road which links downtown Karachi to the airport during the operation to clear the building but the road was reopened at midnight. Since the ceasefire agreement between the TTP and government broke down last year in November, terrorists have stepped up attacks on security forces and installations and even on mosques and markets in different parts of the country but Karachi has for some time now not witnessed any major incident. The last major incident had come in June 2020 when four militants of the banned insurgent group Baloch Liberation Army had attacked the Karachi Stock Exchange, killing three people but were killed themselves as they unsuccessfully tried to enter the stock exchange premises. The outlawed TTP which has claimed Friday's attack has in the past carried out daring terror attacks on security installations in Karachi most notably when they attacked the PNS Mehran base in 2011. The attack and clearance operation lasted for 17 hours and resulted in the deaths of 10 security personnel. Two US-manufactured surveillance planes were also destroyed in the attack. In 2014, the TTP also struck at the Jinnah International Airport old terminal in which 24 lives were lost and property damaged.""")
# print(summary)