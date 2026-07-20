## Chunking Strategy

The chatbot uses a **Recursive Character Text Splitter** to divide PDF documents into smaller, overlapping chunks before generating embeddings. This approach preserves semantic meaning while improving retrieval accuracy.

### Chunk Size

- **Chunk Size:** 500 characters

A chunk size of **500 characters** provides sufficient context for the embedding model to capture the meaning of a passage while keeping each chunk focused on a specific topic or event. This balance helps improve semantic retrieval without producing unnecessarily large chunks.

### Chunk Overlap

- **Chunk Overlap:** 100 characters

An overlap of **100 characters** ensures that information spanning chunk boundaries is preserved. Without overlap, important sentences could be split between two chunks, reducing retrieval accuracy. The overlap maintains context continuity while minimizing redundant information.

### Retrieval Strategy

- **Vector Database:** Qdrant
- **Similarity Metric:** Cosine Similarity
- **Top-K Retrieved Chunks:** 5

For every user query, the embedding of the query is compared against the embeddings stored in Qdrant using **Cosine Similarity**. The **top 5 most similar chunks** are retrieved and provided as context to the language model.

A value of **Top-K = 5** was selected as it provides a good balance between retrieval quality and context size. During testing, retrieving five chunks consistently provided enough relevant context for the language model while avoiding excessive or irrelevant information.

### Why This Strategy?

This configuration was chosen to balance retrieval accuracy, embedding efficiency, and language model performance.

- Maintains semantic context within each chunk.
- Preserves continuity using overlapping chunks.
- Improves the likelihood of retrieving relevant information.
- Keeps the context sent to the language model concise while providing sufficient information for accurate responses.



## Test Cases

The chatbot was evaluated using different categories of user queries to verify retrieval quality and response generation. The following test cases were used during testing.

| Test Case | Sample Question | Result |
|-----------|-----------------|---------------|
| **Relevant Question** | Why did Della cut her hair? | Della cut her hair off and sold it because she couldn't have lived through Christmas without giving Jim a present. Sources: the_gift_of_the_magi.pdf |
| **Irrelevant Question** | Who won the FIFA World Cup in 2022? | I couldn't find that information in the provided documents. |
| **Ambiguous Question** | Who died? | The bird, Mr. Behrman, and the Happy Prince died. Sources: the_velveteen_rabbit.pdf, the_happy_prince.pdf, the_last_leaf.pdf|
| **Empty Query** | *(No input provided)* | I couldn't find that information in the provided documents. |
| **Multi-Document Question** | How do the main characters in The Gift of the Magi and The Happy Prince demonstrate selflessness? | In "The Gift of the Magi," Jim and Della demonstrate selflessness by selling their most prized possessions to buy each other Christmas gifts. Jim sells his watch to buy Della combs for her hair, while Della sells her hair to buy Jim a chain for his watch. Their actions show they are willing to sacrifice their most valuable items for each other, indicating a deep love and selflessness.

In "The Happy Prince," the statue (the Happy Prince) and the swallow demonstrate selflessness. The Happy Prince allows the swallow to take his gold and ruby to help the poor, showing he is willing to give up his beauty and wealth for the benefit of others. The swallow, despite being sick and cold, continues to help the poor and stays with the Happy Prince until the end, showing loyalty and selflessness. Sources: the_gift_of_the_magi.pdf, the_velveteen_rabbit.pdf, the_happy_prince.pdf |


## Debug Logging

2026-07-20 17:02:02,258 - INFO - HTTP Request: POST https://ebdc18e8-2e90-4535-b053-0807521677e6.eu-west-1-0.aws.cloud.qdrant.io:6333/collections/knowledge_base/points/query "HTTP/1.1 200 OK"
2026-07-20 17:02:02,259 - INFO - ================================================================================
2026-07-20 17:02:02,259 - INFO - Query: why did della cut her hair?
2026-07-20 17:02:02,259 - INFO - Retrieved 10 chunks
2026-07-20 17:02:02,260 - INFO - Chunk 1 | Score: 0.7134 | Source: the_gift_of_the_magi.pdf
2026-07-20 17:02:02,260 - INFO - Text: page 1    |    pennymagic.co
pluck at his beard from envy.
So now Della’s beautiful hair fell about her rippling and shining like a cascade of brown waters. It reached 
below her knee and made itself ...
2026-07-20 17:02:02,260 - INFO - Chunk 2 | Score: 0.6232 | Source: the_gift_of_the_magi.pdf
2026-07-20 17:02:02,260 - INFO - Text: sparkle still in her eyes, she fluttered out the door and down the stairs to the street.
Where she stopped the sign read: “Mme. Sofronie. Hair Goods of All Kinds.” One flight up Della ran, and 
collec...
2026-07-20 17:02:02,260 - INFO - Chunk 3 | Score: 0.6227 | Source: the_gift_of_the_magi.pdf
2026-07-20 17:02:02,260 - INFO - Text: why you had me going a while at first.”
White fingers and nimble tore at the string and paper. And then an ecstatic scream of joy; and then, alas! a 
quick feminine change to hysterical tears and wail...
2026-07-20 17:02:02,260 - INFO - Chunk 4 | Score: 0.5586 | Source: the_gift_of_the_magi.pdf
2026-07-20 17:02:02,260 - INFO - Text: nor disapproval, nor horror, nor any of the sentiments that she had been prepared for. He simply stared at her 
fixedly with that peculiar expression on his face.
Della wriggled off the table and went...
2026-07-20 17:02:02,260 - INFO - Chunk 5 | Score: 0.5576 | Source: the_gift_of_the_magi.pdf
2026-07-20 17:02:02,261 - INFO - Text: obtain a fairly accurate conception of his looks. Della, being slender, had mastered the art.
Suddenly she whirled from the window and stood before the glass. Her eyes were shining brilliantly, but he...
2026-07-20 17:02:02,261 - INFO - Chunk 6 | Score: 0.5115 | Source: the_gift_of_the_magi.pdf
2026-07-20 17:02:02,261 - INFO - Text: and eighty-seven cents. And the next day would be Christmas.
There was clearly nothing to do but flop down on the shabby little couch and howl. So Della did it. Which 
instigates the moral reflection ...
2026-07-20 17:02:02,261 - INFO - Chunk 7 | Score: 0.5060 | Source: the_gift_of_the_magi.pdf
2026-07-20 17:02:02,262 - INFO - Text: she whispered: “Please God, make him think I am still pretty.”
The door opened and Jim stepped in and closed it. He looked thin and very serious. Poor fellow, he was only 
twenty-two—and to be burdene...
2026-07-20 17:02:02,262 - INFO - Chunk 8 | Score: 0.5046 | Source: the_gift_of_the_magi.pdf
2026-07-20 17:02:02,262 - INFO - Text: had to do it. My hair grows awfully fast. Say ‘Merry Christmas!’ Jim, and let’s be happy. You don’t know what a 
nice—what a beautiful, nice gift I’ve got for you.”
“You’ve cut off your hair?” asked J...
2026-07-20 17:02:02,262 - INFO - Chunk 9 | Score: 0.4976 | Source: the_gift_of_the_magi.pdf
2026-07-20 17:02:02,264 - INFO - Text: “My hair grows so fast, Jim!”
And then Della leaped up like a little singed cat and cried, “Oh, oh!”
Jim had not yet seen his beautiful present. She held it out to him eagerly upon her open palm. The ...
2026-07-20 17:02:02,265 - INFO - Chunk 10 | Score: 0.4717 | Source: the_gift_of_the_magi.pdf
2026-07-20 17:02:02,266 - INFO - Text: time in any company. Grand as the watch was, he sometimes looked at it on the sly on account of the old 
leather strap that he used in place of a chain.
When Della reached home her intoxication gave w...
2026-07-20 17:02:02,267 - INFO - AFC is enabled with max remote calls: 10.
2026-07-20 17:02:04,302 - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent "HTTP/1.1 200 OK"
2026-07-20 17:02:04,303 - INFO - Model Used: gemini
2026-07-20 17:02:04,303 - INFO - Answer: Della cut her hair off and sold it because she couldn't have lived through Christmas without giving Jim a present.
2026-07-20 17:02:04,303 - INFO - ================================================================================
INFO:     127.0.0.1:50548 - "POST /chat HTTP/1.1" 200 OK