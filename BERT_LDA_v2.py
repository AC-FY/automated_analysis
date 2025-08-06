import os
import numpy as np
import pandas as pd
from docx import Document
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from gensim.corpora import Dictionary
from gensim.models.ldamodel import LdaModel
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import umap
import hdbscan
from bertopic import BERTopic
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def nltk_preprocess(text: str) -> list[str]:
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t.isalpha() and t not in stop_words]
    return [lemmatizer.lemmatize(t) for t in tokens]

def read_docx_sentences(folder_path: str) -> list[str]:
    sentences = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            doc_path = os.path.join(folder_path, filename)
            doc = Document(doc_path)
            for paragraph in doc.paragraphs:
                for sentence in sent_tokenize(paragraph.text):
                    if sentence.strip():
                        sentences.append(sentence.strip())
    return sentences

#Change directory location here#
if __name__ == "__main__":
    folder_path = "/Users/cpost/Documents/202507transcripts"

    raw_sentences = read_docx_sentences(folder_path)
    tokenized_sentences = [nltk_preprocess(sent) for sent in raw_sentences]
    docs_for_bert = [" ".join(tokens) for tokens in tokenized_sentences]

    bert_model = SentenceTransformer("all-MiniLM-L6-v2")
    bert_embeddings = bert_model.encode(docs_for_bert, show_progress_bar=True)

    dictionary = Dictionary(tokenized_sentences)
    corpus = [dictionary.doc2bow(text) for text in tokenized_sentences]
    lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=15, passes=25) #Change number of topics (k) at num_topics#
    lda_distributions = [
        lda_model.get_document_topics(doc, minimum_probability=0) for doc in corpus
    ]
    lda_array = np.array([[prob for _, prob in doc] for doc in lda_distributions])

    lda_array = normalize(lda_array)
    bert_array = normalize(bert_embeddings)
    hybrid_embeddings = np.hstack([lda_array, bert_array])

    umap_model = umap.UMAP(
        n_neighbors=15, n_components=10, metric="cosine"
    ).fit_transform(hybrid_embeddings)
    cluster_model = hdbscan.HDBSCAN(
        min_cluster_size=3, metric="euclidean", cluster_selection_method="eom"
    ).fit_predict(umap_model)

    topic_model = BERTopic(
        embedding_model=bert_model, min_topic_size=3, verbose=True
    )
    topics, _ = topic_model.fit_transform(docs_for_bert, embeddings=hybrid_embeddings)
    topic_info = topic_model.get_topic_info()
    topic_dict = {
        row["Topic"]: topic_model.get_topic(row["Topic"])
        for _, row in topic_info.iterrows()
    }

    topic_labels = []
    for t in topics:
        if t in topic_dict:
            label = ", ".join([word for word, _ in topic_dict[t][:5]])
        else:
            label = "-"
        topic_labels.append(label)

    df = pd.DataFrame(
        {
            "Sentence": raw_sentences,
            "Topic": topics,
            "Topic Words": topic_labels,
            "Cluster": cluster_model,
        }
    )
    df.to_csv("hybrid_docx_sentences_topics_output.csv", index=False, encoding="utf-8")
