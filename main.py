from call_llm import generate_resume_answer
from helper import get_user_topic,read_file_robust
from pdf_parser import pdf_to_markdown_pymupdf4llm

# Run the chain
if __name__ == "__main__":
    api_key = "AIzaSyA8ss5VY86BI8Hg2Mlk_5RsXl5tEG8frOE"
    #upload button should call below function and generate output.md 
    # pdf_to_markdown_pymupdf4llm("Anish_BigData_Engineer_Resume.pdf", output_path="output.md", write_images=True)
    markdown_data = read_file_robust("output.md")
    input_topic = get_user_topic() #ask user for topic with validationstrip()
    if not input_topic:
        print("No topic provided. Exiting.")
        exit(1)
    else:
        print(f"Generating overview for topic: {input_topic}")
        topic ={"topic": input_topic}
    result = generate_resume_answer(markdown_data,topic, api_key)
    print(result)
    # markdown_data = pdf_to_markdown_pymupdf4llm("Anish_BigData_Engineer_Resume.pdf", output_path="output.md", write_images=True)
                     