# Tasik Bot
Discord bot built with python/Flask and deployed via Replit, in combination with Uptime Robot to keep the free version running forever!

## Why was Tasik Bot created?
This was during the beginning of the pandemic. Me and my friends spent a lot of time on Discord. We were interested in stocks, crypto, etc, and we played a lot of Dota 2 and CS:GO.
I wanted to create a bot that could cater to all of these things. So, Tasik Bot was built with the intention of accomplishing:
### Stocks/Crypto: 
Using chat commands to retrieve stock price data
### Dota hero counters:
Using chat commands to get a list of hero counters in Dota 2. If you haven't played Dota 2, here's a short explanation: Heroes are the characters you choose to use for the duration of the game. The hero you choose to fight enemy heroes significantly impacts your chance of victory. Websites like [dotabuff.com](https://www.dotabuff.com/) aggregate lots of data about the game, including suggestions of best hero counterpicks. So I wanted Tasik Bot to scrape dotabuff.com and output relevant data for me and my friends to prompt in the chat.
### CS:GO crosshair:
In CSGO, you can change crosshairs by entering a command into the console. There are websites that countain a complete repository of crosshair commands that pro CS:GO players use. Me and my friends are CS:GO newbies, and we love to copy what the pros use. So I wanted Tasik Bot to scrape websites for the crosshairs of pros we prompt for.
### Extras:
This project was made shortly after my exposure to Python. Instead of doing the usual python projects like tictactoe, blackjack, etc, and running it locally, I wanted to share the experience with my friends. So for instance, instead of creating Black Jack to play locally by myself, I implemented in on Tasik Bot so that me and my friends could play Black Jack using chat commands.

## How was all of this achieved?
With regards to Stocks/Crypto, I used free public APIs provided by market data aggregators. If they weren't available/free, I would use webscrappers instead. The Beautiful Soup library was used for everything related to webscrapping.
### Black Jack
This is were things really worked great with the chat bot model. Two players could play Black Jack against each other on the Discord server. To deliver the cards to each player privately, Tasik Bot would DM each player their cards.

## Screenshot example use
![image](https://user-images.githubusercontent.com/88143539/232332779-f8b6cae4-5c45-4fd8-b1da-4945a3eec87c.png)
![image](https://user-images.githubusercontent.com/88143539/232333107-dae551d0-72c6-4701-92aa-a8882944dafa.png)
