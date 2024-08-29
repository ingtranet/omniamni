from textwrap import dedent

import uvicorn
from loguru import logger
from fastapi import FastAPI
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from omniamni.config import AppContext
from omniamni.model import SimpleText, SimpleBool

app = FastAPI()



@app.post("/is_bad_words")
async def is_bad_language(text: SimpleText):
    prompt = ChatPromptTemplate([(
        "human",
        dedent("""
            Does this text contain serious profanity?
            Please consider offensive but common expressions not to be profanity.
            Please answer YES or NO. You don't need to say anything else.
            {text}
        """),)
    ])

    model = ChatOllama(model="aya", temperature=0)

    class BooleanOutputParser(BaseOutputParser[bool]):
        def parse(self, text: str) -> bool:
            cleaned_text = text.strip().lower()
            print(cleaned_text)
            if "yes" in cleaned_text:
                return True
            elif "no" in cleaned_text:
                return False
            else:
                raise OutputParserException("There is no yes or no in the text")

        @property
        def _type(self) -> str:
            return "boolean_output_parser"

    chain = prompt | model | BooleanOutputParser()
    chain = chain.with_retry()
    try:
        result = await chain.ainvoke({"text": text.value})
    except Exception as e:
        logger.error(f"Error: {e}")
        result = False
    logger.info(f"[is_bad_words] {text.value} -> {result}")
    return SimpleBool(value=result)

@app.post("/scold_for_using_bad_words")
async def scold_for_using_bad_words(text: SimpleText):
    prompt = ChatPromptTemplate([(
        "human",
        dedent("""
            You need to give the person who uses the above profanity a good scolding.
            First, show the swear word as it is and explain why it's wrong.
            Then explain what people who say these things are usually lacking in
                and how they are judged by those around them.
            Just don't make it too long(In 8 sentences or less).
            Keep your answers in Korean.
            {text}
        """),)
    ])

    model = ChatOllama(model="aya", temperature=0.5)
    chain = prompt | model
    try:
        result = (await chain.ainvoke({"text": text.value})).content
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e
    logger.info(f"[scold_for_using_bad_words] {text.value} -> {result}")
    return SimpleText(value=result)


async def start(context: AppContext):
    config = uvicorn.Config(app, port=context.port, log_level=context.log_level)
    server = uvicorn.Server(config)
    await server.serve()
