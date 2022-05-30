def send_email(email):
    print("ты зарегистрировался с почтой:"+email)

def send_del_email(email):
    print("пользователь с почтой:"+email +" удален")

def send_del_tg(email):
    print("tg: ты удалил аккаунт с почтой:"+email)

def send_tg(email):
    print("tg: зарегистрирован пользователь с почтой:" + email)

d = {
'register': [send_email, send_tg],
'delete': [send_del_email, send_del_tg]
}

def work(email, type):
  for i in d[type]:
    i(email)

if __name__=='__main__':
    work('Bred@mail.ru', 'register')
    work('Bred@mail.ru', 'delete')