# Example

```
from core import RedditUser as ru
from core import RedditReport as rr
from utils import export

# Your Reddit API credentials.
# More info: https://www.geeksforgeeks.org/python-praw-python-reddit-api-wrapper/
client_id = 'your-client-id'
client_secret = 'your-client-secret'
user_agent = 'your-user-agent'
reddit_user = ru.RedditUser(client_id, client_secret, user_agent)

# Reddit object instance from praw library
reddit_instance = reddit_user.get_reddit_instance()

# RedditReport instance
subs_list = ['pics', 'askreddit']   # must be a list
lines_per_sub = 3   # must be an integer
reddit_report = rr.RedditReport(reddit_instance, subs_list, lines_per_sub)

# Pulls data from Reddit
report_data = reddit_report.generate_data()

# Uses utils module to export data to Excel file format
filename = 'reddit_report_excel.xlsx'
export.to_excel(report_data, filename)

```