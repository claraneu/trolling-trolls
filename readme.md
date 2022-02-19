# TROLLING TROLLS - Hatespeech Detection

## TABLE OF CONTENTS

1. Introduction
2. Technologies
3. Setup
4. ToDo
5. Credit Where Credit is Due

## 1. Introduction

Currently, the 'website' scrapes Twitter for tweets including the user input, analyzes it for hatespeech and offensive language, and outputs a graph of the last N tweets.

Trolling Trolls (TT) is - at the current state- a proof of concept aiming at a platform that supports moderators to detect hate speech and offensive content on online platforms.
TT is a project that started in TechLabs' Digital Shaper project. To learn particular digital skills, four people completed the DataScience track, one the WebDevelopment (backend) track, and one the UserExperience track. Thus, the project served the purpose to learn and explore within these fields.

After the conclusion of the TechLabs semester, we decided to continue the work on TT.

## 2. Technologies

Languages
- Python 3.8.8
- JavaScript

Packages (ordered by length, as it should be):
- matplotlib
- seaborn
- pandas
- numpy
- json
- csv
- re
- os
- sys
- html
- tqdm
- tweepy
- dotenv

- Zero-Shot algorithm: valhalla/distilbart-mnli-12-1

- **Only runs with twitter API access**

## 3. Setup

To run this project ...


## 4. ToDo

There are a lot of things to do, obviously.

1. Split scripts
2. Include search parameters (location, timeframe, etc.)
3. Add visualizations of correlations (hatespeech per search parameter)
4. Remove CSV-musical chairs
5. And many more

## 5. Credit Where Credit is Due

Majority of Tweepy scraping code from Sarah Warren:
https://github.com/SarahRWarren/twitter-scraper
https://www.youtube.com/watch?v=1M03-yiR-FU