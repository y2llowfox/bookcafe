from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from models import db, Book, Rental, Member

bp = Blueprint('books', __name__, url_prefix='/books')


@bp.route('/')
def list_books():
    q = request.args.get('q', '')
    category = request.args.get('category', '')
    query = Book.query
    if q:
        query = query.filter(
            db.or_(Book.title.contains(q), Book.author.contains(q))
        )
    if category:
        query = query.filter_by(category=category)
    books = query.order_by(Book.title).all()
    categories = db.session.query(Book.category).distinct().all()
    categories = sorted([c[0] for c in categories if c[0]])
    return render_template('books/list.html', books=books, q=q, category=category, categories=categories)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title'].strip()
        author = request.form['author'].strip()
        isbn = request.form.get('isbn', '').strip()
        category = request.form.get('category', '').strip()
        total_qty = int(request.form.get('total_qty', 1))
        if not title or not author:
            flash('제목과 저자는 필수입니다.', 'danger')
            return render_template('books/create.html')
        book = Book(title=title, author=author, isbn=isbn, category=category,
                    total_qty=total_qty, available_qty=total_qty)
        db.session.add(book)
        db.session.commit()
        flash(f'"{title}" 도서가 등록되었습니다.', 'success')
        return redirect(url_for('books.list_books'))
    return render_template('books/create.html')


@bp.route('/<int:id>')
def detail(id):
    book = Book.query.get_or_404(id)
    active_rentals = Rental.query.filter_by(book_id=id, returned_at=None).all()
    return render_template('books/detail.html', book=book, active_rentals=active_rentals)


@bp.route('/rental', methods=['GET', 'POST'])
def rental():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'rent':
            member_id = request.form.get('member_id')
            book_id = request.form.get('book_id')
            if not member_id or not book_id:
                flash('회원과 도서를 선택해주세요.', 'danger')
            else:
                member = Member.query.get(member_id)
                book = Book.query.get(book_id)
                if not member or not member.is_active:
                    flash('유효하지 않은 회원입니다.', 'danger')
                elif not book or book.available_qty <= 0:
                    flash('대출 가능한 도서가 없습니다.', 'danger')
                else:
                    rental = Rental(member_id=member.id, book_id=book.id)
                    book.available_qty -= 1
                    db.session.add(rental)
                    db.session.commit()
                    flash(f'{member.name}님에게 "{book.title}" 대출 완료!', 'success')

        elif action == 'return':
            rental_id = request.form.get('rental_id')
            rental = Rental.query.get(rental_id)
            if rental and not rental.returned_at:
                rental.returned_at = datetime.now()
                rental.book.available_qty += 1
                db.session.commit()
                flash(f'"{rental.book.title}" 반납 완료!', 'success')

        return redirect(url_for('books.rental'))

    members = Member.query.filter_by(is_active=True).order_by(Member.name).all()
    books = Book.query.filter(Book.available_qty > 0).order_by(Book.title).all()
    active_rentals = Rental.query.filter_by(returned_at=None).order_by(Rental.due_date).all()
    return render_template('books/rental.html', members=members, books=books, active_rentals=active_rentals)
