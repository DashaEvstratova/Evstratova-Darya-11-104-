subs = dict()

def create_topic(topic_name: str):
    subs[topic_name] = {'users': [],'top': [],}

def subscribe(topic: str, user_id: int):
    if not topic in subs:
        subs[topic] = []
    subs[topic].append(user_id)

def post_feed(topic: str, feed_id: int):
    if not topic in subs:
        return
    subs[topic]['top'].append(feed_id)
    for fn in subs[topic]['users']:
        result = ''.join(['пользователь ', fn, ' получил новость ', feed_id])
        print(result)
