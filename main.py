from steem import Steem
import random

node = ["https://api.steemit.com"]

#private posting key | private active key
keys=["----", "---"]

s = Steem(node,keys=keys)

#your steemit account
account = "wil1liam"

# if you want to send SBD or STEEM
#asset = "STEEM"
asset = "SBD"

#rewards pool --> total rewards sent out
reward_pool = 0.002

#winner message (MEMO)
random_memo = "Congratulations! You are the random winner from @wil1liam comment contest! Here is your reward :)"
community_memo = "Congratulations! You wrote the most upvoted comment at @wil1liam last post! Here is your reward :)"
memo = [random_memo,community_memo]


url = input("Your Steemit Post Url: ")

#url = "https://steemit.com/utopian-io/@wil1liam/steem-power-delegations-sale-blocktrades-what-are-people-doing-with-their-sp-analysis"

def get_all_comments(url):
    comments = s.get_content_replies(account,url.split("/")[5])
    for i in comments:
        if i["children"]>0:
            for i in s.get_content_replies(i["author"],i["permlink"]):
                comments.append(i)
    return comments

def random_winner(comments):
    commentators = []
    for i in comments:
        if i["author"] not in commentators:
            commentators.append(i["author"])
    randome_number = random.randrange(len(commentators))

    return commentators[randome_number]

def community_winner(comments):
    highest_comment = comments[0]
    for i in comments:
        if (i["net_votes"]>highest_comment["net_votes"]):
            highest_comment = i

    return highest_comment["author"]

def reward_winners(winners,asset,reward_pool,memo):
    for i in range(len(winners)):
        s.transfer(winners[i], (1/len(winners))*reward_pool, asset, memo=memo[i], account=account)
    return "send " + str(reward_pool) + asset


"""
main programm
"""
#get comments
comments = get_all_comments(url)
#choose winners
#random winner first | community winner second
winners = [random_winner(comments),community_winner(comments)]

#send rewards
print(reward_winners(winners,asset,reward_pool,memo))
