# Import required libraries
import glob
import os
import time  # For time-related operations
from bs4 import BeautifulSoup  # For parsing HTML data
from bs4.element import Tag  # For representing HTML tags
from googletrans import Translator  # For language translation
import traceback  # For printing detailed error information

# Define constants for the time to sleep on timeout errors
SLEEP_ON_TIMEOUT = 1
SLEEP_FACTOR = 2

# User needs to change:
# ---------------------
# Name of the directory containing HTML files to be translated
DIR_NAME = "www.classcentral.com"
# Destination language to translate the content
DEST = "hi"


def translate_node(node, translator, lang_dest):
    """
    Recursively translate the given HTML node and its
    children.

    :param node: HTML node to be translated
    :param translator: GoogleTrans Translator object
    :param lang_dest: Destination language code
    """
    # If the node is an HTML tag, recursively translate its children
    if isinstance(node, Tag):
        for child in node.children:
            translate_node(child, translator, lang_dest)
    else:
        # If the node is a text node, translate its text content
        if node.text == r"\n" or node.text.strip() == "":
            return None
        state = False
        multiplier = 1
        # Retry the translation until it succeeds, with an increasing delay
        # between retries
        while not state:
            try:
                # print(node.text)
                # Translate the text of the node using the Google Translate API
                translation = translator.translate(node.text, dest=lang_dest).text
                # print(translation)
            except IndexError:
                return None
            except TypeError:
                return None
            except Exception as e:
                # If an error occurs, print the error message and wait for a
                # bit before retrying
                print(e, type(e), multiplier)
                # traceback.print_tb(e.__traceback__)
                time.sleep(SLEEP_ON_TIMEOUT * multiplier)
                multiplier *= SLEEP_FACTOR
            else:
                # If the translation is successful, replace the text content of
                # the node with the translated text
                state = True
        # Replace the original text of the node with the translated text
        node.replace_with(translation)
        write_to_file(fname, soup)


def write_to_file(fname, soup):
    """
    Write the given soup object to the specified file

    :param fname: Path of the output file
    :param soup: BeautifulSoup object to be written to the file
    """
    with open(fname, "w") as f:
        f.write(str(soup))


# Find all the HTML files in the specified directory
# --------------------------------------------------
dir_name = DIR_NAME
# Create a list of all the file paths in the directory
path_list = glob.glob(dir_name + "/**/**", recursive=True)
# Remove all the files that are not in HTML format and directories
html_list = []
for element in path_list:
    # Ignore some type of files
    if not element.endswith(
        (".woff2", ".png", ".svg", ".js", ".txt", ".webmanifest")
    ) and not os.path.isdir(element):
        html_list.append(element)
html_list = set(html_list)

# Save the paths of the HTML files to a file
with open("html-file-path.md", "w") as f:
    f.write("\n".join(html_list))
print("Number of HTML files to be translate:", len(html_list), "\n")

# Initialize the translator object
# --------------------------------
raise_exception = False
translator = Translator(raise_exception=raise_exception)
translator.raise_Exception = False

# Translate all the HTML files in the path list
# ---------------------------------------------
for fname in html_list:
    print(f"Start translation of {fname}. \n")
    with open(fname, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    # print(soup)
    translate_node(soup.head, translator, lang_dest=DEST)
    translate_node(soup.body, translator, lang_dest=DEST)
    # Write the translated HTML back to the original file
    write_to_file(fname, soup)
    print(f"{fname} has been translated and saved. \n")
