from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Sale, Member

bp = Blueprint('sales', __name__, url_prefix='/sales')


@bp.route('/', methods=['GET', 'POST'])
def list_sales():
    if request.method == 'POST':
        item_name = request.form['item_name'].strip()
        amount = int(request.form['amount'])
        member_id = request.form.get('member_id') or None
        points_used = int(request.form.get('points_used', 0))

        if not item_name or amount <= 0:
            flash('상품명과 금액을 입력해주세요.', 'danger')
            return redirect(url_for('sales.list_sales'))

        points_earned = 0
        member = None
        if member_id:
            member = Member.query.get(member_id)
            if member:
                if points_used > member.points:
                    flash(f'포인트가 부족합니다. (보유: {member.points}P)', 'danger')
                    return redirect(url_for('sales.list_sales'))
                points_earned = int(amount * 0.05)
                member.points = member.points - points_used + points_earned
                member.total_points += points_earned
                member.update_membership()

        sale = Sale(
            member_id=member.id if member else None,
            item_name=item_name,
            amount=amount,
            points_used=points_used,
            points_earned=points_earned,
        )
        db.session.add(sale)
        db.session.commit()
        msg = f'{item_name} {amount:,}원 매출 등록!'
        if member:
            msg += f' ({member.name}님 +{points_earned}P)'
        flash(msg, 'success')
        return redirect(url_for('sales.list_sales'))

    sales = Sale.query.order_by(Sale.created_at.desc()).limit(100).all()
    members = Member.query.filter_by(is_active=True).order_by(Member.name).all()
    return render_template('sales/list.html', sales=sales, members=members)
