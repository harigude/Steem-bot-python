# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 20:38:28 2018

"""

from steem import Steem
from steem.account import Account
from steem.amount import Amount
from steem.post import Post
import steemfunc
import time
import re
from steem.blockchain import Blockchain

# Replace posting key and active key with keys from your Steemit account in both s and s1.
s = Steem(keys=['#Posting key','#Active key'])
s1 = Steem(nodes=['https://api.steemit.com'], keys=['#Posting key','#Active key'])

# Replace account name with your Steemit account name
account_name = 'account name'

# Get stats such as current Steem price, reward balance, recent claims and value of reward share. 
steem_price = Amount(s.get_current_median_history_price()["base"]).amount
reward_fund = s.get_reward_fund()
reward_balance = Amount(reward_fund["reward_balance"]).amount   
recent_claims = float(reward_fund["recent_claims"])
rshares_sbd_value = reward_balance / recent_claims

class bot:
    
    def post_upvote_stats(post_author,post_link):
    # Get upvote statisitcs given post author and post link. 
    # Returns - list of voters and their share of earnings.
        act_votes = s.get_active_votes(post_author,post_link)
        voter_names = []
        voter_sbd_value = []
        cnt=0
        for voter in act_votes:
            voter_names.append(voter['voter'])
            rshares = voter['rshares']
            voter_sbd_value.append(float(rshares) * rshares_sbd_value)
            cnt=cnt+1
        return voter_names,voter_sbd_value, cnt
    
    def post_comments_stats(post_author,post_link):
    # Get comment/reply statisitcs given post author and post link. 
    # Returns - list of commenters, comments and links.
        names=[]
        comments = []
        urls = []
        cmts = s.get_content_replies(post_author,post_link)
        for cmt in cmts:
            names.append(cmt['author'])
            comments.append(cmt['body'])
            urls.append(cmt['url'])
        return names,comments,urls
       
    def trending_posts(n):
    # Get current trending posts on steemit.
    # n - Limit for number of posts.
    # Returns post author and post links.
        authors=[]
        links = []
        query = {"limit": n} 
        data =[]
        for p in s.get_discussions_by_trending(query):
            data.append(p)
            authors.append(p["author"])
            links.append(p["permlink"])
        return data,authors,links
            
    def post_resteemers(post_author,post_link):
    # Get reposters 
    #Inputs - post author and post link. 
    # Output - list of reposters.
        resteemers = s.get_reblogged_by(post_author,post_link)
        resteemers.remove(post_author)
        return resteemers

    def post_create_upvote(post_author,post_link,voting_acccount):
    # Upvote a post
    # Inputs -post author and post link.
        link = '@' + post_author +'/'+ post_link  # Create a voting link using post author and link.
        s.vote(link, 100.0,voting_acccount)
        
    def post_create_reply(author,title,comment_title,comment_body,account_name):
    # parameters: author - author of the post, title - title of the post, 
    # comment_title - title of the comment 
    #comment_body - body for the comment
    #account_name - accocunt name
        link = '@' + author +'/'+ title
        s1.commit.post(
            comment_title,
            comment_body,
            account_name,
            reply_identifier=link,
            tags=["test",]
        )

    def create_post(post_title,post_body,account_name,tags):    
    #example tags = [python, bot, etc...]
        s1.commit.post(
            post_title,
            post_body,
            account_name,
            tags=[tags]
        )
            
    def voting_stats(account_name):
    # Get voting statistics given an account name.
    # Returns Steem Power, Voting Power, Time to recharge(min), Current Voting Power and Value of vote in Steem 
        account = Account(account_name)
        SP = steemfunc.calculateSP(account)
        print('Steem Power:', int(SP), 'SP')
        VP,recharge_time = steemfunc.getactiveVP(account)
        current_VP = account.voting_power()
        print('Voting Power:', int(VP))
        vote_value = steemfunc.getvotevalue(SP, VP, 100)
        return SP,VP,recharge_time,current_VP,vote_value
    
    def power_down(amount,account_name):
    # Power down given the amount of vests to be withdrawn and an account name.
        s.withdraw_vesting(amount, account_name)
        
    def upvote_trending_posts(n, voting_account):
    # Upvotes trending posts
        query = {"limit": n} 
        for p in s.get_discussions_by_trending(query):
            post_link = '@' + p["author"] +'/'+ p["permlink"]  # Create a voting link using post author and link
            s.vote(post_link, 100.0,voting_account)
        print('voting completed')
        
    
    def resteem_post(post_author,post_link, account):
    # Resteem posts 
    # Inputs - post author, post link and account name.
        link = '@' + post_author +'/'+ post_link  # Create a voting link using post author and link.
        s.resteem(link,account)
        print('successfully resteemed')
    
    def account_history(account):
    # Returns account history 
        history = s.get_account_history(account,index_from=-1, limit=1000)
        return history
    

bot1 = bot
account_name='aditya8003'
#get the authors of the post and the links to the post in the below variables
posts_data,post_authors,post_links = bot1.trending_posts(5)
#pass the above variable values to the below function to get the details of the upvotes.
names, money, cnt = bot1.post_upvote_stats(post_authors[0],post_links[0])
#get the comments of the post into the below variables.
commenter_names,comments,comment_urls = bot1.post_comments_stats(post_authors[0],post_links[0])
#get the details of the resteemers
resteemers = bot1.post_resteemers(post_authors[0],post_links[0])
#Reply to the post- currently giving an error
#bot1.post_create_reply(account_name)
#Given an account name, retrieve the voting power and other stats.
SP,VP,recharge_time,current_VP,vote_value = bot1.voting_stats(account_name)
print(cnt)
#Resteem a given post- currently giving an error
#bot1.resteem_post(post_authors[2],post_links[2],account_name)
#upvote a post 
bot1.post_create_upvote(post_authors[0],post_links[0], account_name)




