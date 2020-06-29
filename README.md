# /r/BuyCanadian TLDR About Bot

## Using the bot via Reddit

The bot can be called in a reply to a comment or submission that contains a link, or supplied with a link in the same comment it is called. The command for calling the bot is `!about`. The bot will reply with a TLDR of the About page from the given link, or a unique error message. 

## Basics about the system

- Each error is unique and will tag /u/GlaucomysSabrinus when it occurs
- The bot only checks for calls every ten minutes, on the 7th minute (i.e. 10:07am, 10:17am, 10:27am, etc.)
- The bot only works on sites that have a `/robots.txt` file that points to a valid `sitemap` page
- From the sitemap the bot uses regex to find a page url containing either 'about' or 'story'
  - I don't know what happens if there is more than one page containing a key word. I think it will break
- The TLDR is generated using the [SMMRY](https://smmry.com/) API
- The the text is too short, the bot replies with the entire content of the about page by scraping text tags
  - p, span, h1, h2, h3, h4, h5, h6
  - sentences with 3 words or less are removed

## Working with the code

```
git clone https://github.com/ourcanadian/buycan-tldr
cd buycan-tldr
pip install requirements.txt
```

Need a `praw.ini` file in order to use the Reddit bot.
