

def get_user_topic():
    """Get topic input from user with validation"""
    while True:
        topic = input("Please enter a topic for the overview: ").strip()
        if topic:  # Check if input is not empty
            return topic
        else:
            print("Please enter a valid topic (cannot be empty).")





def read_file_robust(file_path, encodings=['utf-8', 'utf-16', 'latin-1', 'cp1252']):
    """
    Read a file with multiple encoding attempts and return content as string.
    
    Args:
        file_path (str): Path to the file to read
        encodings (list): List of encodings to try
    
    Returns:
        tuple: (content as string, successful encoding used) or (None, None) if failed
    """
    import os
    
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return None, None
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                return content, encoding
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error with encoding '{encoding}': {str(e)}")
            continue
    
    print(f"Error: Could not read file with any encoding: {encodings}")
    return None, None

# Example usage:
# content, encoding_used = read_file_robust("example.txt")
# if content is not None:
#     print(f"File read successfully with encoding: {encoding_used}")
#     print(content)


import json

def get_config_value(config_path, key_path):
    """
    Reads a value from a JSON config file by following the key path.
    Args:
        config_path (str): Path to the config JSON file.
        key_path (list): List of keys describing the path to the desired config value.
    Returns:
        The value if found, else raises a KeyError.
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    value = config
    for key in key_path:
        value = value[key]
    return value

# Example usage:
# val = get_config_value('config.json', ['vector_store', 'qdrant', 'api_key'])
# print(val)
