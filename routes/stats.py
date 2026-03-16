from flask import Blueprint, render_template
from datetime import datetime
from sqlalchemy import func, extract
from models import db, Member, Book, Rental, Sale

bp = Blueprint('stats', __name__, url_prefix='/stats')


@bp.route('/')
def dashboard():
    now = datetime.now()

    # 오늘 매출
    today_sales = db.session.query(func.coalesce(func.sum(Sale.amount), 0)).filter(
        func.date(Sale.created_at) == now.date()
    ).scalar()

    # 이번 달 매출
    month_sales = db.session.query(func.coalesce(func.sum(Sale.amount), 0)).filter(
        extract('year', Sale.created_at) == now.year,
        extract('month', Sale.created_at) == now.month,
    ).scalar()

    # 회원 등급별 분포
    membership_stats = db.session.query(
        Member.membership, func.count(Member.id)
    ).filter_by(is_active=True).group_by(Member.membership).all()
    membership_data = {m: c for m, c in membership_stats}

    # 총 회원 수
    total_members = Member.query.filter_by(is_active=True).count()

    # 대출 중인 도서 수
    active_rentals = Rental.query.filter_by(returned_at=None).count()

    # 연체 도서 수
    overdue_count = Rental.query.filter(
        Rental.returned_at.is_(None),
        Rental.due_date < now
    ).count()

    # 인기 도서 TOP 10
    popular_books = db.session.query(
        Book.title, func.count(Rental.id).label('cnt')
    ).join(Rental).group_by(Book.id).order_by(func.count(Rental.id).desc()).limit(10).all()

    # 최근 6개월 월별 매출
    monthly_sales = db.session.query(
        extract('year', Sale.created_at).label('year'),
        extract('month', Sale.created_at).label('month'),
        func.sum(Sale.amount).label('total')
    ).group_by('year', 'month').order_by('year', 'month').limit(6).all()
    monthly_labels = [f"{int(r.year)}-{int(r.month):02d}" for r in monthly_sales]
    monthly_values = [int(r.total) for r in monthly_sales]

    return render_template('stats/dashboard.html',
                           today_sales=today_sales,
                           month_sales=month_sales,
                           membership_data=membership_data,
                           total_members=total_members,
                           active_rentals=active_rentals,
                           overdue_count=overdue_count,
                           popular_books=popular_books,
                           monthly_labels=monthly_labels,
                           monthly_values=monthly_values)
