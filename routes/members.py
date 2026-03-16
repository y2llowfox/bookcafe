from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Member

bp = Blueprint('members', __name__, url_prefix='/members')


@bp.route('/')
def list_members():
    q = request.args.get('q', '')
    membership = request.args.get('membership', '')
    query = Member.query.filter_by(is_active=True)
    if q:
        query = query.filter(
            db.or_(Member.name.contains(q), Member.phone.contains(q))
        )
    if membership:
        query = query.filter_by(membership=membership)
    members = query.order_by(Member.created_at.desc()).all()
    return render_template('members/list.html', members=members, q=q, membership=membership)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name'].strip()
        phone = request.form['phone'].strip()
        email = request.form.get('email', '').strip()
        if not name or not phone:
            flash('이름과 전화번호는 필수입니다.', 'danger')
            return render_template('members/create.html')
        if Member.query.filter_by(phone=phone).first():
            flash('이미 등록된 전화번호입니다.', 'danger')
            return render_template('members/create.html')
        member = Member(name=name, phone=phone, email=email)
        db.session.add(member)
        db.session.commit()
        flash(f'{name}님이 등록되었습니다.', 'success')
        return redirect(url_for('members.list_members'))
    return render_template('members/create.html')


@bp.route('/<int:id>')
def detail(id):
    member = Member.query.get_or_404(id)
    rentals = [r for r in member.rentals if not r.returned_at]
    history = sorted(member.rentals, key=lambda r: r.rented_at, reverse=True)[:10]
    return render_template('members/detail.html', member=member, rentals=rentals, history=history)


@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    member = Member.query.get_or_404(id)
    if request.method == 'POST':
        member.name = request.form['name'].strip()
        phone = request.form['phone'].strip()
        member.email = request.form.get('email', '').strip()
        existing = Member.query.filter(Member.phone == phone, Member.id != id).first()
        if existing:
            flash('이미 등록된 전화번호입니다.', 'danger')
            return render_template('members/detail.html', member=member, rentals=[], history=[])
        member.phone = phone
        db.session.commit()
        flash('회원 정보가 수정되었습니다.', 'success')
        return redirect(url_for('members.detail', id=id))
    return render_template('members/detail.html', member=member,
                           rentals=[r for r in member.rentals if not r.returned_at],
                           history=sorted(member.rentals, key=lambda r: r.rented_at, reverse=True)[:10])


@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    member = Member.query.get_or_404(id)
    member.is_active = False
    db.session.commit()
    flash(f'{member.name}님이 비활성화되었습니다.', 'warning')
    return redirect(url_for('members.list_members'))
