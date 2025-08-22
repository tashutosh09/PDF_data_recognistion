import pymupdf4llm
import pathlib
from typing import Optional, List

def pdf_to_markdown_pymupdf4llm(
    pdf_path: str, 
    output_path: Optional[str] = None,
    pages: Optional[List[int]] = None,
    write_images: bool = False,
    dpi: int = 150
) -> str:
    """
    Convert PDF to Markdown using pymupdf4llm.
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_path (str, optional): Path to save the markdown file
        pages (List[int], optional): List of 0-based page numbers to process
        write_images (bool): Whether to extract and save images
        dpi (int): Resolution for image extraction
    
    Returns:
        str: Markdown content as string
    """
    try:
        # Convert PDF to markdown
        if pages:
            md_text = pymupdf4llm.to_markdown(pdf_path, pages=pages)
        else:
            md_text = pymupdf4llm.to_markdown(
                pdf_path, 
                write_images=write_images,
                dpi=dpi
            )
        
        # Save to file if output path is provided
        if output_path:
            pathlib.Path(output_path).write_bytes(md_text.encode('utf-8'))
            print(f"Markdown saved to: {output_path}")
        
        return md_text
    
    except Exception as e:
        print(f"Error converting PDF to Markdown: {e}")
        return ""
