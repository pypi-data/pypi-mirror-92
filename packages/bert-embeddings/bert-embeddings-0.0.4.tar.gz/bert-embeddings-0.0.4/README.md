# Bert Embeddings
Create super fast bert embeddings for any NLP usecase!

## Installation
**With pip**  
```pip install bert-embeddings```

**With Git**  
```
git clone https://github.com/sorcely/BertEmbeddings.git
virtualenv venv
cd venv/scripts; activate; cd ../../
pip install -r requirements.txt --find-links https://download.pytorch.org/whl/torch_stable.html
```


## Example
```python
bert_embeddings = BertEmbeddings()

text = "After stealing money from the bank vault, the bank robber was seen fishing on the Mississippi river bank."

output = bert_embeddings([text])
```