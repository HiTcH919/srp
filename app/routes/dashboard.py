from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.service_order import ServiceOrder
from app.models.user import User
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta, timezone # Ensure all are imported

dashboard_bp = Blueprint('dashboard', __name__) # url_prefix is set in app/__init__.py

@dashboard_bp.route('/')
@dashboard_bp.route('/home')
@login_required
def home():
    dashboard_title = ""
    is_admin_view = False

    # Define start and end of today for "today's stats"
    # Ensure timezone awareness if your created_at fields are timezone-aware
    # If created_at is naive, use datetime.now() and datetime.today().replace(...)
    today_start_utc = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    # For SQLite, which doesn't store timezone info, you might need to ensure consistency
    # or use a simpler date comparison if all times are stored in UTC.
    # For this example, let's use SQLAlchemy's func.date for date comparison if fields are DateTime.
    # If ServiceOrder.created_at is stored as naive datetime (e.g. from datetime.utcnow() without timezone),
    # then use datetime.date(ServiceOrder.created_at) == datetime.date.today()

    if current_user.is_admin:
        service_orders = ServiceOrder.query.order_by(ServiceOrder.created_at.desc()).limit(20).all()
        dashboard_title = "جميع أوامر الخدمة الأخيرة"
        is_admin_view = True

        # Admin quick stats
        # Count of orders created today (system-wide)
        # Assuming ServiceOrder.created_at is a DateTime field
        system_orders_today_count = db.session.query(func.count(ServiceOrder.id)).filter(
            ServiceOrder.created_at >= today_start_utc,
            ServiceOrder.created_at < (today_start_utc + timedelta(days=1))
        ).scalar()

        quick_stats_data = {
            "today": system_orders_today_count,
            "week": 0,  # Placeholder for system-wide weekly count
            "month": 0, # Placeholder for system-wide monthly count
            "total": ServiceOrder.query.count() # System-wide total
        }
    else:
        # Regular user view
        service_orders = ServiceOrder.query.filter_by(user_id=current_user.id)                                         .order_by(ServiceOrder.created_at.desc())                                         .limit(5).all()
        dashboard_title = "أحدث أوامر خدمتك" # Title for user's own orders
        is_admin_view = False

        # User-specific quick stats
        user_orders_today_count = db.session.query(func.count(ServiceOrder.id)).filter(
            ServiceOrder.user_id == current_user.id,
            ServiceOrder.created_at >= today_start_utc,
            ServiceOrder.created_at < (today_start_utc + timedelta(days=1))
        ).scalar()

        user_total_orders_count = ServiceOrder.query.filter_by(user_id=current_user.id).count()

        quick_stats_data = {
            "today": user_orders_today_count,
            "week": 0, # Placeholder for user's weekly count
            "month": 0, # Placeholder for user's monthly count
            "user_total": user_total_orders_count # Total for the current user
        }

    return render_template(
        'dashboard.html',
        service_orders=service_orders,
        quick_stats_data=quick_stats_data,
        dashboard_title=dashboard_title,
        is_admin_view=is_admin_view
    )
