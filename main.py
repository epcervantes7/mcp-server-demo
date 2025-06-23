import os

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("AI Notes")
NOTES_FILE = os.path.join(os.path.dirname(__file__),'notes.txt')

def ensure_file_exist():
    if not os.path.exists(NOTES_FILE):
        with open (NOTES_FILE,'w') as f:
            f.write("")
    

@mcp.tool()
def add_note(message:str) -> str:
    """This tool append a new note to the note file.

    Args:
        message (str): The note content to be added

    Returns:
        str: Confirmation message indicating the note was saved 
    """
    ensure_file_exist()
    with open (NOTES_FILE,'a') as f:
        f.write(message+'\n')
    return "Note saved!"


@mcp.tool()
def read_notes(message:str) -> str:
    """This tool read and returns all notes from the note file.

    Returns:
        str: All notes as a single string separeted by line breaks.
            If no notes exist, a default message is returned.
    """
    ensure_file_exist()
    with open (NOTES_FILE,'r') as f:
        content = f.read().strip()
    return content or "No notes yet"


@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """Get the most recently added note from the sticky note file.

    Returns:
        str: The last note entry, If no notes exist, a default message is returned.
    """
    ensure_file_exist()
    with open (NOTES_FILE,'r') as f:
        lines = f.readline()
    return lines[-1].strip() if lines else "No notes yet"


@mcp.prompt()
def note_summary() -> str:
    """Generates as prompt asking IA to summarize all the current notes

    Returns:
        str: A prompt string that includes all the notes asn asks for a summary.
            If no notes exist, a message will be shown indicating that.
    """
    with open (NOTES_FILE,'r') as f:
        content = f.read().strip()
    if not content:
        return "There are no notes yet"
    return f"summarize the current notes: {content}"