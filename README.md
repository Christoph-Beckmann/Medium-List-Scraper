# Medium List Scraper

## Table of Contents
1. [Description](#description)
2. [Functionality](#functionality)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Limitations](#limitations)

## Description

Are you a heavy user of Zotero and Medium? Do you want to apply your Zotero color coding to Medium articles and export the notes to Obsidian? This tool makes it possible!

This Python script allows you to scrape articles from multiple lists on [Medium.com](https://medium.com/me/lists) and save them into a *library.csv*. The library serves as a local database, and the script checks for differences between the library and scraped articles for every scrape attempt, saving new articles into the library.

Additionally, this web scraper downloads each article as a PDF using [scribe.rip](https://scribe.rip), an alternative frontend for Medium articles, for more beautifully formatted PDFs. This process uses [Percollate](https://github.com/danburzo/percollate), a command-line tool that turns web pages into elegant PDFs.

The downloaded PDFs are saved into separate folders (one for each list) within a *downloads* folder.

Finally, you can add these downloaded PDFs to Zotero to begin your note-taking and color-coding process.

## Functionality

- **Scraping Medium Lists**: The script scrapes articles from your specified Medium lists and saves them into a local *library.csv* file.
- **PDF Generation**: The scraper downloads each article as a PDF using [scribe.rip](https://scribe.rip) and [Percollate](https://github.com/danburzo/percollate) for a visually appealing format.
- **File Organization**: The downloaded PDFs are organized into separate folders for each list within a *downloads* folder.
- **Zotero Integration**: You can import the downloaded PDFs into Zotero for note-taking and color-coding.

## Requirements

- Python 3.x
- [Brave Browser](https://brave.com/)
- [Percollate](https://github.com/danburzo/percollate)

## Installation

1. Clone or download the repository.
2. Set up a virtual environment by running `python3 -m venv .venv` and activate it.
3. Install all dependencies with `pip install -r requirements.txt`.
4. Install **Percollate** by following the instructions [here](https://github.com/danburzo/percollate#installation).
5. Edit the *medium_lists.csv* file to add your own public lists.

## Usage

Run the scraper with the following command: `python3 -m medium_scraper.py`.
## Limitations

- This scraper is built for the [Brave Browser](https://brave.com/). You must install this browser to use the scraper, or edit the code to use Chrome (for more information, read [this](https://github.com/SergeyPirogov/webdriver_manager)).
- The scraper will only work with public lists.
