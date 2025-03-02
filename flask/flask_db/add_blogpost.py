from app import db, BlogPost

# blog_post1 = BlogPost("blog Title1", "Blog Test1", "Image1.png", 1, "Summary1")
# blog_post2 = BlogPost("blog Title2", "Blog Test2", "Image2.png", 1, "Summary2")
# blog_post3 = BlogPost("blog Title3", "Blog Test3", "Image3.png", 3, "Summary3")
blog_post4 = BlogPost("blog Title4", "Blog Test4", "Image4.png", 4, "Summary4")

# db.session.add_all([blog_post1, blog_post2, blog_post3])
db.session.add_all(blog_post4)
db.session.commit()