# aws-kendra-playground

learn [Amazon Kendra](https://aws.amazon.com/kendra/), intelligent search service powered by machine learning

## Concepts

* Index - two types. document (unstructured) and [FAQ (structured)](https://docs.aws.amazon.com/kendra/latest/dg/in-creating-faq.html)
    * You can add documents directly to an index using the BatchPutDocument operation
    * You can add questions and answers (FAQs) directly to your index using the console or the CreateFaq operation
* Data Source - s3, salesforce documents, sharepoint, *custom*
* Documents - html, ppt, doc, pdf, txt
    * custom fields - can define custom fields of types: Date, Number, String, String List
* Queries - natural language (NLP), keyword queries, Factoid questions — Simple
who, what, when, or where questions.
    * Facets are scoped views of a set of search results
    * By default, Query returns all search results. To filter responses, you can perform logical operations on the document attributes.
* Tags - can assign tags to indexes, data sources, and FAQs

* default encryption at rest with customer of AWS KMS keys

## General Steps

1. create index
1. add data sources for index
1. synchronize the data source
1. query/search the index

## Editions

* Developer
* Enterprise

You specify `Edition: DEVELOPER_EDITION | ENTERPRISE_EDITION` when you create an index

--

## Creating Example Index

see [`main.py`](main.py)

```sh
sam deploy --guided
# copy outputs into `.env`
python main.py
```

## Resources

* [Amazon Kendra Docs](https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html)
* [Getting started (AWS SDK for Python (Boto3)) - Amazon Kendra](https://docs.aws.amazon.com/kendra/latest/dg/gs-python.html) - shows create index, create data source for index, sync data source, all while waiting for each step to complete in between
* [Deploying Amazon Kendra](https://docs.aws.amazon.com/kendra/latest/dg/deploying.html) - pre-built react frontend for kendra.  provides `<search />` react component
    * <https://kendrasamples.s3.amazonaws.com/kendrasamples.zip>
* [aws-samples/enterprise-search-with-amazon-kendra-workshop](https://github.com/aws-samples/enterprise-search-with-amazon-kendra-workshop)
* [Kendra | Using a custom data source](https://docs.aws.amazon.com/kendra/latest/dg/data-source-custom.html)