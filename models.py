from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), default='')
    membership = db.Column(db.String(20), default='BASIC')  # BASIC, SILVER, GOLD, VIP
    points = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)  # 누적 포인트 (등급 산정용)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)

    rentals = db.relationship('Rental', backref='member', lazy=True)
    sales = db.relationship('Sale', backref='member', lazy=True)

    def update_membership(self):
        if self.total_points >= 5000:
            self.membership = 'VIP'
        elif self.total_points >= 3000:
            self.membership = 'GOLD'
        elif self.total_points >= 1000:
            self.membership = 'SILVER'
        else:
            self.membership = 'BASIC'


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(20), default='')
    category = db.Column(db.String(50), default='')
    total_qty = db.Column(db.Integer, default=1)
    available_qty = db.Column(db.Integer, default=1)

    rentals = db.relationship('Rental', backref='book', lazy=True)


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    rented_at = db.Column(db.DateTime, default=datetime.now)
    due_date = db.Column(db.DateTime)
    returned_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.due_date:
            self.due_date = (self.rented_at or datetime.now()) + timedelta(days=14)

    @property
    def is_overdue(self):
        if self.returned_at:
            return False
        return datetime.now() > self.due_date


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=True)
    item_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    points_used = db.Column(db.Integer, default=0)
    points_earned = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
