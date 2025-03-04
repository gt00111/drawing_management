from app import db, Drawing

db.create_all()

drawing1 = Drawing("test会社1", "test機種1", "test1-test1-test1", "1", "1")
drawing2 = Drawing("test会社2", "test機種2", "test2-test2-test2", "1", "1")

db.session.add_all([drawing1, drawing2])
db.session.commit()
print(drawing1.id)
print(drawing2.id)

# drawing3 = Drawing("test会社3", "test機種3", "test3-test3-test3", "1", "1")
# db.session.add(drawing3)
# db.session.commit()

# all_rawings = Drawing.query.all()
# print(all_rawings)

# drawingid_1 = Drawing.query.get(1)
# print(drawingid_1)

# drawingname_drawing2 = Drawing.query.filter_by(drawingnumber="test1-test1-test1")
# print(drawingname_drawing2.all())

# db.session.add_all()
# db.session.commit()

# drawingid_1 = Drawing.query.get(2)

# db.session.delete(drawingid_1)
# db.session.commit()

# all_drawings = Drawing.query.all()
# print(all_drawings)

# データベース削除###################################
# import os

# db_path = "drawing.sqlite"
# if os.path.exists(db_path):
#     os.remove(db_path)
#     print("データベースを削除しました。")
# else:
#     print("データベースが見つかりませんでした。")
