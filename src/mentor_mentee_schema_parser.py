
import os
from langchain.text_splitter import MarkdownHeaderTextSplitter
from papago import papago_api
from langchain.document_loaders.text import TextLoader






def mentee_parser():

    loader_mentee = TextLoader("/tmp/data/mentee_info.txt")

    data_mentee = loader_mentee.load()

    mentee_markdown_doc = data_mentee[0].page_content

    headers_to_split_on = [
        ("#", "Name"),

    ]
    #mentee_dict = {}
    mentee_doc_dict = {}
    mentee_attr_dic = {}

    mentee_markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    mentee_md_header_splits = mentee_markdown_splitter.split_text(mentee_markdown_doc)

    papago_api(mentee_md_header_splits,mentee_doc_dict,mentee_attr_dic)

    return mentee_attr_dic


def mentor_parser():
    loader_mentee = TextLoader("/tmp/data/mentor_info.txt")
    data_mentor = loader_mentee.load()




    mentor_markdown_doc = data_mentor[0].page_content
    headers_to_split_on = [
        ("#", "Name"),
    ]

    #mentor_dict = {}
    mentor_doc_dict = {}
    mentor_attribute_dic = {}

    mentor_markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    mentor_md_header_splits = mentor_markdown_splitter.split_text(mentor_markdown_doc)

    papago_api(mentor_md_header_splits,mentor_doc_dict,mentor_attribute_dic)

    return mentor_attribute_dic


