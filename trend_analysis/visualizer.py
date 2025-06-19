import matplotlib.pyplot as plt
from wordcloud import WordCloud

def plot_bar(data, title, xlabel, ylabel, top_n=10):
    items = data[:top_n]
    labels, values = zip(*items) if items else ([],[])
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color='skyblue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_wordcloud(words, title):
    text = ' '.join(words)
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.show() 