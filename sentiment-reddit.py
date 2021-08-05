# This is a reddit sentiment tracker for stocks and events/news that can influence a particular sector

import requests
import requests.auth
import praw
import pandas as pd

# client_auth = requests.auth.HTTPBasicAuth("Xy7vBGv3UujCmntmelz6zw","vWCGi4UQhA-nR2vqlzddibdF0Ite7A")
# post_data = {"grant_type":"password","username":"Ginni679","password":"Ginnipb41@"}
# headers = {"User-Agent": "Ginni679/0.1"}
# response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)



headers = {"Authorization": "bearer 471078083660-iH-qkUZNIJRupS0rHtrVW-bA_lhNsg", "User-Agent": "Ginni679/0.1"}
response = requests.get("https://oauth.reddit.com/api/v1/me",headers=headers)


reddit = praw.Reddit(
    client_id="Xy7vBGv3UujCmntmelz6zw",
    client_secret = "vWCGi4UQhA-nR2vqlzddibdF0Ite7A",
    user_agent = "Ginni679/0.1"
)

print(reddit.read_only)

subreddit = "wallstreetbets"
posts = reddit.subreddit(subreddit).new(limit=10)
#load the posts into a pandas dataframe
p = []
for post in posts:
    p.append([post.title, post.score, post.selftext])
posts_df = pd.DataFrame(p,columns=['title', 'score', 'post'])
    
print(posts_df.iloc[:5,:])