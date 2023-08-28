import os
from flaskblog import app
from flask_login import current_user 
def like_control():
    like = request.args.get('like')
    if like:
        liked_post = Post.query.get(like)
        if current_user not in liked_post.likes:
            liked_post.likes.append(current_user)
        else:
            liked_post.likes.remove(current_user)
        db.session.add(liked_post)
        db.session.commit()
        return redirect(request.referrer)

def save_picture(form_picture):
    _, ext = os.path.splitext(form_picture.filename)
    pic_name = str(current_user.id) + ext
    pic_path = os.path.join(app.root_path, 'static/profile_pics', pic_name)
    form_picture.save(pic_path)
    return pic_name
