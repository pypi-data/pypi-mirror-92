### DATA FORMAT

```
{
    "title": "title of a paper",
 	"authors": [
        {
            "firstName": "firstName of an author",
            "lastName": "lastName of an author "
        }
    ],
    "keywords":["keyword1","keyword2"],
    "abstract": "abstract of a paper",
    "paperContent":{
        "text": "all content of a paper (This is also a concatenation of subtexts)",
        "subtitles": ["Introduction", "Model"],
        "subtexts": ["section1Content", "section2Content"]
    },
    "references":[
        {
            "refTitle": "title of a reference paper",
            "refAuthors": [
                {
                    "firstName": "firstName of an author",
                    "lastName": "lastName of an author "
                }
            ],
            "refYear": "publised year of a reference paper",
            "refPublisher": "publised journal of a reference paper"
        }
    ]
}
```