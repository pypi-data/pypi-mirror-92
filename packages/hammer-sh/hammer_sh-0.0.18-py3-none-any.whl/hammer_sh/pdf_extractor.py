import io
import os

# import pdfplumber
import fitz  # PyMuPDF
import nltk
import pandas as pd
import pyocr.builders
from PIL import Image
from nltk.corpus import stopwords
from pdf2image import convert_from_path
from pdfminer import high_level as pdf_extractor
import pickle
import pkg_resources

nltk.download('stopwords')
stop_words = stopwords.words("english")
lookup = {0: "Chemistry", 1: "Computer Sience", 2: "Medicine"}
__name__ = "hammer_sh"

def load_saved_text():
    """

    :return:
    """
    stream = pkg_resources.resource_filename(__name__, 'sample_data/articles.pickle')
    with open(stream, 'rb') as file:
        df = pickle.load(file)
    return df


def extract_images(rootdir):
    """

    :param rootdir:
    :return:
    """
    data = []
    files = __get_files(rootdir);

    for idx, category in enumerate(files):
        for file in category:
            data.append([lookup[idx], __extract_images(file)])
    df = pd.DataFrame(data)
    return df


def __extract_images(path):
    """

    :param path:
    :return:
    """
    file = fitz.open(path)
    images = []
    for page_index in range(len(file)):
        # get the page itself
        page = file[page_index]
        image_list = page.getImageList()
        # printing number of images found in this page
        if image_list:
            print(f"[+] Found a total of {len(image_list)} images in page {page_index + 1}")
        else:
            print("[!] No images found on page", page_index + 1)
        for image_index, img in enumerate(page.getImageList(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = file.extractImage(xref)
            image_bytes = base_image["image"]
            # get the image extension
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
            # save it to local disk
            image.save(open(f"image{page_index + 1}_{image_index}.{image_ext}", "wb"))
    return images


def __get_files(rootdir):
    """

    :param rootdir:
    :return:
    """
    subfolders = [f.path for f in os.scandir(rootdir) if f.is_dir()]
    files = []
    for subfolder in subfolders:
        files.append(__list_files(subfolder))
    return files


def extract_text(rootdir, ocr=False):
    """

    :param rootdir:
    :param ocr:
    :return:
    """
    files = __get_files(rootdir)
    data = []
    if ocr is True:
        for idx, category in enumerate(files):
            for file in category:
                data.append([lookup[idx], __extract_text_ocr(file)])
    else:
        for idx, category in enumerate(files):
            for file in category:
                data.append([lookup[idx], __extract_text(file)])
    df = pd.DataFrame(data)
    return df


def __extract_text(path):
    """

    :param path:
    :return:
    """
    text = pdf_extractor.extract_text(path)
    return text


def __extract_text_ocr(path):
    """

    :param path:
    :return:
    """
    pages = convert_from_path(path, 500)
    image_counter = 1
    for page in pages:
        filename = "page_" + str(image_counter) + ".jpg"
        # Save the image of the page in system
        page.save("temp/" + filename, 'JPEG')
        # Increment the counter to update filename
        image_counter = image_counter + 1

    # Variable to get count of total number of pages
    filelimit = image_counter - 1

    # Iterate from 1 to total number of pages
    complete_text = ""
    for i in range(1, filelimit + 1):
        filename = "page_" + str(i) + ".jpg"

        # Recognize the text as string in image using pytesserct
        tools = pyocr.get_available_tools()[0]
        text = tools.image_to_string(Image.open(filename), builder=pyocr.tesseract.builders.TextBuilder())
        text = text.replace('-\n', '')
        complete_text = complete_text + text

    return complete_text


def __list_files(directory):
    """

    :param directory:
    :return:
    """
    r = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            r.append(os.path.join(root, name))
    return r
