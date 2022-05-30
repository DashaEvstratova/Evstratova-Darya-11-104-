import requests

def get_mails(username):
    data = {'username': username}
    users = requests.get('https://jsonplaceholder.typicode.com/users', data).json()
    id = users[0]['id']
    data_posts = {
        'userId': id
    }
    posts = requests.get('https://jsonplaceholder.typicode.com/posts', data_posts).json()
    posts_ids = []
    for post in posts:
        posts_ids.append(post['id'])
    data_comments = {'postId': posts_ids}
    comments = requests.get('https://jsonplaceholder.typicode.com/comments', data_comments).json()
    emails=[]
    for comment in comments:
        emails.append(comment['email'])
    print(emails)

get_mails('Bret')