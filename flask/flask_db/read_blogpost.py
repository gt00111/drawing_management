from app import db, User, BlogPost

all_post = BlogPost.query.all()
print(all_post)