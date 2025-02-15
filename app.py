import streamlit as st

def remove_blank_lines(text):
    """Remove blank lines from the text."""
    non_empty_lines = [line for line in text.splitlines() if line.strip() != ""]
    return "\n".join(non_empty_lines)

st.title("Remove Blank Lines from Text File")

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