import os
import re
# from constants import openai_key
import openai
from langchain import PromptTemplate
from langchain.chains import LLMChain

import streamlit as st
## streamlit framework

# os.environ['OPENAI_API_KEY']=openai_key
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.title("Book Search")
input_text=st.text_input("Tell us your favourite book, so that we can suggest you the next best book you can read!")

##prompt template


template = """\
My favourite book is '{input}' give me a numbered list of the next 10 best books I can read
with a description of minimum 3 lines about them and a amazon link to buy the book at the end. 
It should be in the format of "Title: Description; link-to-amazon". if you didnt find the amazon link, just send a link of googles search result page for the book.
"""

prompt = PromptTemplate.from_template(template)
prompt.format(input=input_text)


##OPENAI LLM MODELS

llm=OpenAI(temperature=0.8)
chain=LLMChain(llm=llm, prompt=prompt, verbose=True)

if input_text:

    output = chain.run(input_text)
    # st.write(output)
    book_entries = []

    # Split the string by newline character to get individual lines
    lines = output.split('\n')

    # Process each line and extract book entries
    current_entry = ""
    for line in lines:
        if line.strip().startswith(str(len(book_entries) + 1) + ". "):
            # Start of a new book entry
            book_entries.append(current_entry.strip())
            current_entry = line.strip()
        else:
            # Continue adding lines to the current entry
            current_entry += " " + line.strip()

    # Add the last book entry to the list
    book_entries.append(current_entry.strip())
    col1, col2, col3 = st.columns([1,6,1])
    for i in range(1, len(book_entries)):
        parts = book_entries[i].split(":",1)
        title = parts[0].strip()
        desc = parts[1].strip()
        # parts2 = desc.split(";",1)
        # d = parts2[0].strip()
        # link = parts2[1].strip()
        # with col2:
        #     if st.button(f'##### {title} \n {d}'):
        #         st.markdown(f'<a href="{link}">Buy Now</a>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'##### {title}\n {desc}')


st.markdown('---') 

st.markdown(f'Made with ❤️ by [Sidhanti](https://github.com/Sid2202)')
        