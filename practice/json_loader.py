import json

from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_loaders import JSONLoader
from pydantic import BaseModel, Field

from dotenv import load_dotenv

load_dotenv()


class Word(BaseModel):
    Frequency: str = Field(description="Rank (based on frequency of use)")
    Expression: str = Field(description="Original Japanese text")
    Furigana: str = Field(
        description="Extract the exact hiragana reading of 'Expression' from Example_jp (e.g. for '彼の声はとても大きい' → 'こえ')"
    )
    Meaning: str = Field(
        description="Korean translation (multiple meanings separated by ( · ) , The word part is always the noun.)"
    )


llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0)
loader = JSONLoader(
    file_path="./files/words.json",
    jq_schema=".[]",
    text_content=False,
)

documents = loader.load()

# 프롬프트 템플릿
system_prompt_template = """Complete this JSON file using the provided format.

Format rules:
{format_instructions}

Reference JSON structure:
{reference_json}
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt_template),
        ("human", "Complete the JSON structure based on the reference provided."),
    ]
)

# Parser 설정
parser = JsonOutputParser(pydantic_object=Word)
prompt = prompt.partial(format_instructions=parser.get_format_instructions())

# Chain 구성
chain = prompt | llm | parser

json_list = []

for document in documents:
    # json_data = chain.invoke({"reference_json": document})

    #     # 리스트에 저장
    #     json_list.append(json_data)
    print(f"Frequency: {document.page_content}")


# with open("./files/d_words.json", "w", encoding="utf-8") as f:
#     json.dump(json_list, f, ensure_ascii=False, indent=2)
