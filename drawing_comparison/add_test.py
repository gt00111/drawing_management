from app import db, Drawing

drawing_list = []
for i in range(60):
    drawing_list.append(Drawing(f"test会社{i}", f"機種{i}", f"test{i}", "1", "1"))
db.session.add_all(drawing_list)
db.session.commit()