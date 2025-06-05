from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app import db # Import db instance from app package
from app.models.user import User # Import User model

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home')) # Or wherever authenticated users should go

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        is_admin_str = request.form.get('is_admin', 'false') # Default to 'false' if not present
        is_admin = is_admin_str.lower() in ['true', 'yes', '1', 'on']


        error = False
        if not username:
            flash('اسم المستخدم مطلوب.', 'danger')
            error = True
        if not email:
            flash('البريد الإلكتروني مطلوب.', 'danger')
            error = True
        if not password:
            flash('كلمة المرور مطلوبة.', 'danger')
            error = True
        if password != confirm_password:
            flash('كلمتا المرور غير متطابقتين.', 'danger')
            error = True

        if User.query.filter_by(username=username).first():
            flash('اسم المستخدم هذا موجود بالفعل. الرجاء اختيار اسم آخر.', 'danger')
            error = True
        if User.query.filter_by(email=email).first():
            flash('هذا البريد الإلكتروني مسجل بالفعل.', 'danger')
            error = True

        if error:
            return render_template('register.html')

        new_user = User(username=username, email=email, is_admin=is_admin)
        new_user.set_password(password)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash(f'تم إنشاء حساب {username} بنجاح! يمكنك الآن تسجيل الدخول.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء إنشاء الحساب: {str(e)}', 'danger')
            return render_template('register.html')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home')) # Redirect to dashboard if already logged in

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = True if request.form.get('remember_me') else False

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            flash('تم تسجيل الدخول بنجاح!', 'success')
            # Attempt to redirect to the 'next' page if it was provided (e.g., by @login_required)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.home'))
        else:
            flash('فشل تسجيل الدخول. الرجاء التحقق من اسم المستخدم وكلمة المرور.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required # Ensure only logged-in users can access logout
def logout():
    logout_user()
    flash('تم تسجيل الخروج بنجاح.', 'info')
    return redirect(url_for('auth.login'))

# Example of a protected route (can be moved to another blueprint)
@auth_bp.route('/profile')
@login_required
def profile():
    return f"<h1>ملف المستخدم {current_user.username}</h1><p>هذه صفحة محمية.</p><p><a href='{url_for('auth.logout')}'>تسجيل الخروج</a></p>"
