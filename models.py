from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# In-memory user list (replace with a database later)
users = [
    User(1, 'user1', 'password1'),
    User(2, 'user2', 'password2'),
]
