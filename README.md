# Translate a website

This repository contains a solution for a technical test that involves
translating a website using the Google Translation API.
The solution involves scraping the website using `wget` and then translating
the scraped files using a Python script.

## Prerequisites

Before running the script, you need to install the following dependencies
using `pip`:

- `beautifulsoup4`
- `googletrans==4.0.0-rc1`

## Usage

Use `wget` to scrape a website with one level deep (`-l 1`):

```
wget -w 5 -l 1 -r -k -U mozzila "https://www.<web site>.com"
```

This command downloads the website with a wait time of 5 seconds between
requests (`-w 5`), recursively (`-r`), and converts the links in the HTML files
so that they point to local files (`-k`).
The user agent string is set to `mozzila` using the `-U` option.

Open the `translate.py` file and define the language to translate to in the
`DEST` variable and the name of the directory containing the HTML files in the
`DIR_NAME` variable.
Then, run the `translate.py` script which will translate all the HTML files in
the specified directory to the language specified in `DEST`:

```
python translation.py
```
