# text-to-KG
> Python library to convert text documents into knowledge graph components

## general steps
1. create project
    - course name
2. load data
    - specify directory to load transcripts from
    - specify file loader to extract transcript text only
    - {filename, text}
3. partition data
    - character text splitter
4. invoke model
    - ex. gemma2b, gpt
    - feed each data partition into AI model
5. JSON parser
6. store in DB

Can repeat steps 3-4 multiple times (ex. summarize -> key concepts -> json KG)

### data structures
#### project
- name
- model

#### document
- text
- source_file

#### node
main - ai generated
- id
- label
- abstraction

metadata - human + system modified
- notes
- source_files []
- contributors []
- date_created
- date_edited

#### edge
- source node ID
- target node ID

## example usage
```py
from text2kg.core import Pipeline
from text2kg.tasks import (
    CombineKnowledgeGraphs,
    CreateKnowledgeGraph,
    FormatAsJson,
    LoadTranscripts,
    SummarizeTranscripts,
)

summary_prompt = "..."
create_kg_prompt = "..."
combine_kg_prompt = "..."

def group_by_lecture():
    pass

pipeline = Pipeline(
    tasks=[
        LoadTranscripts(directory="/transcripts/comp1405/F19"),
        SummarizeTranscripts(model="gemma2b", prompt=summary_prompt),
        CreateKnowledgeGraph(model="chatgpt", prompt=create_kg_prompt),
        CombineKnowledgeGraphs(model="gemma2b", prompt=combine_kg_prompt),
        FormatAsJson(),
    ],
)
pipeline.run()
```