import os

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from helper import get_config_value,get_first_available_llm_key
                         

get_llm_details = get_first_available_llm_key(get_config_value('config.json', []))



def generate_resume_answer(resume_markdown, topic) :
    """
    Generate an answer to a user's question based solely on the provided resume markdown data.
    
    Args:
        resume_markdown (str): The resume content in markdown format
        topic (str): The user's question about the resume
        api_key (str, optional): Your Google Gemini API key. If None, uses global api_key
    
    Returns:
        str: An answer based exclusively on the resume content
    """
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    # Use provided api_key or fall back to global one
    if get_llm_details:
        # print("Using provider:", result['provider'])
        api_key = get_llm_details['api_key']
        Model = get_llm_details['model']
    else:
        print("No configured LLM API key found.")
    
    if not api_key:
        raise ValueError("API key is required. Please provide it or set GOOGLE_API_KEY environment variable.")
    
    # Initialize the Google Gemini LLM
    llm = ChatGoogleGenerativeAI(
        api_key=api_key,
        model=Model,
        temperature=0.3  # Lower temperature for more factual, consistent responses
    )
    
    # Define the resume Q&A prompt template with two input variables
    template = PromptTemplate(
        input_variables=["resume_markdown", "topic"],
        template="""You are an AI assistant that answers questions about a person's resume. 
You must answer the question based ONLY on the information provided in the resume markdown below. 
Do not use any external knowledge or make assumptions beyond what is explicitly stated in the resume.

Resume Data:
{resume_markdown}

User Question: {topic}

Instructions:
- Answer the question using ONLY information from the resume above
- If the information is not available in the resume, respond with "I don't have that information in the provided resume"
- Be specific and cite relevant sections from the resume when possible
- Keep your answer concise and focused on the question asked

Answer:"""
    )
    
    # Build the chain using LCEL syntax
    chain = template | llm | StrOutputParser()
    
    # Generate and return the answer
    try:
        result = chain.invoke({
            "resume_markdown": resume_markdown,
            "topic": topic
        })
        return result
    except Exception as e:
        return f"Error generating answer: {str(e)}"
