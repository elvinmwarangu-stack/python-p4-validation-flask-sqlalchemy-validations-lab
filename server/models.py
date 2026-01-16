from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name field is required.")

        # Check for duplicate name (exclude self for updates)
        query = db.session.query(Author).filter_by(name=name)
        if self.id is not None:
            query = query.filter(Author.id != self.id)

        if query.first() is not None:
            raise ValueError("Name must be unique.")

        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if phone_number:
            # Strip all non-digits
            digits = re.sub(r'\D', '', phone_number)
            if len(digits) != 10:
                raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'<Author {self.name}>'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    summary = db.Column(db.String)
    category = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        allowed = ['Fiction', 'Non-Fiction']
        if category and category not in allowed:
            raise ValueError(f"Category must be either 'Fiction' or 'Non-Fiction'.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        required_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in required_phrases):
            raise ValueError(
                "Title must contain at least one of: 'Won't Believe', 'Secret', 'Top', 'Guess'"
            )
        return title

    def __repr__(self):
        return f'<Post {self.title}>'