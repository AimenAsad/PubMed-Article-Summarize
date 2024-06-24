from flask import Flask, render_template, request
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from preprocessing import preprocess  # Import the preprocessing function

app = Flask(__name__)
def summarize_text(text, sentence_count=5):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentence_count)
    return " ".join([str(sentence) for sentence in summary])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        f = request.files.get('file')
        if f:
            article_text = f.read().decode("utf-8")
            
            # Preprocess the article text
            preprocessed_text = preprocess(article_text)
            
            # Summarize the preprocessed text
            summarized_text = summarize_text(preprocessed_text)
            
            return render_template('result.html', article_text=article_text, summarized_text=summarized_text)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
