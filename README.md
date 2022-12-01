# Medium List Scraper

## Table of Contents
1. [Description](#description)
2. [How to install](#how-to-install)
3. [How to use](#how-to-use)
4. [License](#license)

## Description

You use Zotero and Medium heavily? You would prefer to apply your color coding from Zotero in Mediums Articles to export the notes to Obsidian? 
This tool makes this possible! 

This Python script allow to scrape articles from multiple lists at [Medium.com](https://medium.com/me/lists). 

These scraped articles are saved into a *library.csv*. This library serves as a local database, for every scrape attempt this script checks if there are differences between the library and scraped articles and save this new articles into this library. 

Nonetheless, this web scraper download every article into a PDF. Therefore, this script uses [scribe.rip](https://scribe.rip) (an alternative frontend for Medium articles, to download more beautiful formatted PDFs). For this purpose I use [Percollate](https://github.com/danburzo/percollate), which is a command-line tool, to turn web pages into beautiful PDFs. 

These PDFs are saved into separate folder (for each list) in a download folder which are located in a *downloads* folder.

Lastly, you can add these downloaded PDFs to Zotero to start you note taking and color coding process. 

## How to install 

1. For using this scraper, you should run your own environment.
Therefore use `python3 -m venv .venv` and install all dependencies: `pip install -r requirements.txt`.
2. You'll have to install **Percollate**. Follow instructions [here](https://github.com/danburzo/percollate#installation).
3. You'll also have to edit the *medium_lists.csv* and add your own public lists.

## How to use 

Run this scraper with `python3 -m medium_scraper.py`. 

> **Limitations** 
> - This scraper is build for using the [Brave Browser](https://brave.com/)! You'll have to install this Browser to make this scraper applicable or edit this code for Chrome using (for more information read [this](https://github.com/SergeyPirogov/webdriver_manager)).
> - It will only work with public lists!

## License

MIT License

Copyright © 2022 Christoph Beckmann

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
