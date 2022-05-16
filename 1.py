import requests

def my_funk(username):
    emails = []
    user_name = {'username': username}
    users = requests.get('https://jsonplaceholder.typicode.com/users', user_name).json()

    user_id = users[0]['id']
    data_posts = {
        'userId': user_id
    }
    posts = requests.get('https://jsonplaceholder.typicode.com/posts', data_posts).json()
    for i in posts:
        post = i['id']
        data_comments = {'postId': post}
        comment = requests.get('https://jsonplaceholder.typicode.com/comments', data_comments).json()
        for j in comment:
            emails.append(j['email'])
    return emails

if __name__ == '__main__':
    print(my_funk('Bret'))