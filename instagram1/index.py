import instaloader

L = instaloader.Instaloader()

influencers = ["agasthya.shah"]

for user in influencers:
    profile = instaloader.Profile.from_username(L.context, user)
    if profile.followers >= 30000:
        for post in profile.get_posts():
            L.download_pic(filename=post.date_local.strftime(r"%Y-%m-%d %H_%M_%S") + ".jpg", url=post.url, mtime=post.date_local)
            post_data = {
                "date": post.date_local,
                "hashtags": post.caption_hashtags,
                "followers": profile.followers
            }
            print(post_data)
