from models import db, User, Comment
from flask import g


class UserComment():

    def __init__(self, form, rating, user_to_id):
        """Instantiate comment Class"""

        self.title = form.title.data,
        self.comment = form.comment.data,
        self.rating = rating,
        self.user_to_id = user_to_id

    def add_comment(self):
        """Handles adding of comments to database"""
        comment = Comment(
            title=self.title,
            comment=self.comment,
            rating=self.rating,
            user_from_id=g.user.id,
            user_to_id=self.user_to_id
        )
        db.session.add(comment)
        db.session.commit()
        return comment

    def add_rating(self):
        """Handles rating computation and updating"""
        ratings = Comment.query.filter(
            Comment.user_to_id == self.user_to_id).all()
        rate = 0
        tot = 0
        ave = 0
        for r in ratings:
            if r.rating:
                tot += 1
                rate += r.rating
        ave = rate / tot
        user = User.query.get_or_404(self.user_to_id)
        user.rating = ave
        db.session.add(user)
        db.session.commit()
        return user
