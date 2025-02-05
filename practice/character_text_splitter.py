from langchain_text_splitters import CharacterTextSplitter

with open("./files/baseball.txt", encoding="utf-8") as f:
    file = f.read()


text_splitter = CharacterTextSplitter(chunk_size=90, chunk_overlap=0)
documents = text_splitter.create_documents([file])

for document in documents:
    print(document)
