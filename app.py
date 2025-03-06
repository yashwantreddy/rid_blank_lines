import streamlit as st
import io

def remove_blank_lines(text):
    """Remove blank lines from the text."""
    non_empty_lines = [line for line in text.splitlines() if line.strip() != ""]
    return "\n".join(non_empty_lines)

def rearrange_string(input_string):
    lines = input_string.strip().split('\n')
    result_lines = []
    
    for line in lines:
        if not line.strip():
            result_lines.append(line)
            continue
            
        # Split the line at the first occurrence of double quotes
        parts = line.split('"', 1)
        if len(parts) < 2:
            result_lines.append(line)
            continue
            
        prefix = parts[0]  # Q48r1                
        # Check if there's a closing quote and separate it
        if '"' in parts[1]:
            content, closing = parts[1].rsplit('"', 1)
        else:
            content = parts[1]
            closing = ""
        
        # Extract the code (e.g., Q48r1)
        code = content.split(' - ')[0]
        
        # Extract the middle and last parts
        middle_and_last = content.split(' - ')[1:]
        if len(middle_and_last) < 2:
            result_lines.append(line)
            continue
            
        # Swap the middle and last parts
        middle = middle_and_last[-1]
        last = ' - '.join(middle_and_last[:-1])
        
        # Reconstruct the line with the closing quote at the end
        new_line = f'{prefix}"{code} - {middle} - {last}"{closing}'
        result_lines.append(new_line)
    
    return '\n'.join(result_lines)

st.title("Remove Blank Lines & Dashes Formatting Tool")

uploaded_file = st.file_uploader("Choose a text file", type=["txt"])
if uploaded_file is not None:
    try:
        # Assuming file encoding is cp1252
        file_content = uploaded_file.read().decode("cp1252")
    except Exception as e:
        st.error("Error reading file: " + str(e))
    else:
        processed_content = remove_blank_lines(file_content)

        # Show processed text in a text area (optional)
        st.text_area("Processed file content", processed_content, height=300)

        # Create a download button
        original_name = uploaded_file.name
        if "." in original_name:
            base = original_name.rsplit(".", 1)[0]
        else:
            base = original_name
        output_filename = f"{base}_no_blank_spaces.txt"

        st.download_button(
            label="Download processed file",
            data=processed_content,
            file_name=output_filename,
            mime="text/plain"
        )

# Input text area
input_text = st.text_area("Paste your dash formatted text here:", height=200)

# Process the text when user inputs something
if input_text:
 rearranged_text = rearrange_string(input_text)
 
 st.subheader("Rearranged Text:")
 st.text_area("Result:", rearranged_text, height=200)
 
 # Create a download button for the processed text
 buffer = io.BytesIO()
 buffer.write(rearranged_text.encode())
 buffer.seek(0)
 
 st.download_button(
     label="Download as .txt file",
     data=buffer,
     file_name="rearranged_text.txt",
     mime="text/plain"
 )
