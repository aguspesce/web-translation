import glob
import os
import time
from bs4 import BeautifulSoup
from bs4.element import Tag
from googletrans import Translator
import traceback

SLEEP_ON_TIMEOUT = 1
SLEEP_FACTOR = 2


def translate_node(node, translator, lang_dest):
    """Function to translate"""
    if isinstance(node, Tag):
        for child in node.children:
            translate_node(child, translator, lang_dest)
    else:
        if node.text == r"\n" or node.text.strip() == "":
            return None
        state = False
        multiplier = 1
        while not state:
            try:
                # print(node.text)
                translation = translator.translate(node.text, dest=lang_dest).text
                # print(translation)
            except IndexError:
                return None
            except TypeError:
                return None
            except Exception as e:
                print(e, type(e), multiplier)
                # traceback.print_tb(e.__traceback__)
                time.sleep(SLEEP_ON_TIMEOUT * multiplier)
                multiplier *= SLEEP_FACTOR
            else:
                state = True
        node.replace_with(translation)
        write_to_file(fname, soup)


def write_to_file(fname, soup):
    """Save data in a file"""
    with open(fname, "w") as f:
        f.write(str(soup))


# Find all the html file in dir_name
dir_name = "www.classcentral.com"
# Create a list of all the file path in the dire_name directory
path_list = glob.glob(dir_name + "/**/**", recursive=True)
# Remove all the file that are not html format and directories
html_list = []
for element in path_list:
    # Ignore some type of files
    if not element.endswith(
        (".woff2", ".png", ".svg", ".js", ".txt", ".webmanifest")
    ) and not os.path.isdir(element):
        html_list.append(element)
html_list = set(html_list)
# Save the path of the html files
with open("html-file-names.md", "w") as f:
    f.write("\n".join(html_list))
print("Len of the files: \n", len(html_list), "\n")

# Define the translator
raise_exception = False
translator = Translator(raise_exception=raise_exception)
translator.raise_Exception = False

# Translate all the html files form the path list
for fname in html_list:
    print(f"Start translation of {fname}. \n")
    with open(fname, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    # print(soup)
    translate_node(soup.head, translator, "hi")
    translate_node(soup.body, translator, "hi")
    write_to_file(fname, soup)
    print(f"{fname} has been translated and saved. \n")
