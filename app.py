import os
from flask import Flask, render_template
from models import db, Member, Book, Rental

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bookcafe-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'bookcafe.db')

db.init_app(app)

# Blueprint 등록
from routes.members import bp as members_bp
from routes.books import bp as books_bp
from routes.sales import bp as sales_bp
from routes.stats import bp as stats_bp

app.register_blueprint(members_bp)
app.register_blueprint(books_bp)
app.register_blueprint(sales_bp)
app.register_blueprint(stats_bp)


@app.route('/')
def index():
    total_members = Member.query.filter_by(is_active=True).count()
    total_books = Book.query.count()
    active_rentals = Rental.query.filter_by(returned_at=None).count()
    from datetime import datetime
    overdue_count = Rental.query.filter(
        Rental.returned_at.is_(None),
        Rental.due_date < datetime.now()
    ).count()
    recent_rentals = Rental.query.order_by(Rental.rented_at.desc()).limit(5).all()
    return render_template('index.html',
                           total_members=total_members,
                           total_books=total_books,
                           active_rentals=active_rentals,
                           overdue_count=overdue_count,
                           recent_rentals=recent_rentals)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
