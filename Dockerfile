FROM public.ecr.aws/lambda/python:3.10


RUN pip install requests pandas mysql-connector-python langchain together FlagEmbedding unstructured cohere numpy regex sentence-transformers lxml pypdf
RUN pip install faiss-cpu


run [ "python", "-c", "import nltk; nltk.download(['punkt','wordnet','stopwords'])" ]

COPY src/data ${LAMBDA_TASK_ROOT}/src/data

COPY src/* ${LAMBDA_TASK_ROOT}

ENV TRANSFORMERS_CACHE=/tmp
ENV NLTK_DATA /tmp/nltk_data
CMD ["my_lambda_function.lambda_handler"]

