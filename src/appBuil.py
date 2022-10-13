from mtranslate import translate
import streamlit as st
from PIL import Image
from textblob import TextBlob
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Judul
st.title("Natural Language Processing")

# Memilih Layanan NLP
st.sidebar.subheader("Pilih tipe layanan yang kamu inginkan")
option = st.sidebar.selectbox('Layanan NLP', ('Pilih disini', 'Sentimen Analisis', 'Rangkum Teks'))

# Fungsi untuk mengambil dictionary dari entitas, tipe entitas dan
def entRecognizer(entDict, typeEnt):
    entList = [ent for ent in entDict if entDict[ent] == typeEnt]
    return entList

if option == 'Pilih disini':
    img = Image.open('Enjoy!.png')
    st.image(img)

# Sentimen Analisis
if option == 'Sentimen Analisis':
    # Textboxt untuk pengguna
    st.subheader("Masukan Text yang mau di analisis")
    # Menampilkan hasil dari NLP
    text = st.text_input('Masukan Text')
    st.warning("Pilih Bahasa etc jika bukan bahasa inggris")
    # Pilih Bahasa yang digunakan
    st.sidebar.subheader("Pilih Bahasa yang dimassukan")
    bahasa = st.sidebar.selectbox("Bahasa Text input", ("Pilih Bahasa", "En","etc"))
    if bahasa == 'etc':
        text = translate(text, 'en')
    # buat graf untuk sentimen tiap kalimat di text input
    st.header("Result")
    sents = sent_tokenize(text)
    entireText = TextBlob(text)
    sentScores = []
    for sent in sents:
        text = TextBlob(sent)
        score = text.sentiment[0]
        sentScores.append(score)

    # Plot sentimen score
    st.line_chart(sentScores)

    # Polarity dan subjektivity pada text inputan
    sentimentTotal = entireText.sentiment
    st.write("Polarity :",sentimentTotal.polarity)
    st.write("Subjektivitas :",sentimentTotal.subjectivity*100,"%")
    polarity = sentimentTotal.polarity
    if polarity < 0:
        st.error('Text tersebut bersentimen NEGATIF')
    elif polarity > 0:
        st.success('Text tersebut bersentimen POSITIF')
    elif polarity == 0:
        st.write('Text tersebut bersentimen NETRAL')

# Rangkum Teks
if option == 'Rangkum Teks':
    st.markdown('**Pilih Bahasa dulu**')
    text = st.text_input('Masukkan teks yang akan dirangkum')
    option = st.sidebar.selectbox('Pilih Bahasa', ('Pilih Disini', 'English', 'Indonesia'))
    
    if option == 'English':
        stopWords = set(stopwords.words("english"))
    if option == 'Indonesia':
        stopWords = set(stopwords.words("indonesian"))
    words = word_tokenize(text)

    freqTable = dict()
    for word in words:
        word = word.lower()
        if word in stopWords:
            continue
        elif word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = sent_tokenize(text)
    sentenceValue = dict()

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    
    sumValue = 0
    for sentence in sentenceValue:
        sumValue += sentenceValue[sentence]

    try:
        avarage = int(sumValue / len(sentenceValue))
    except ZeroDivisionError:
        avarage = 0

    summary = ''
    for sentence in sentences:
        if(sentence in sentenceValue) and (sentenceValue[sentence] > (1.2*avarage)):
            summary += " " + sentence
    
    if option == 'Pilih Disini':
        st.error('Pilih Bahasa terlebih dahulu')
    summary
