from app import create_app, db
from app.models.user import User
from app.models.service_order import ServiceOrder

# Create an app instance using the factory
app = create_app()

@app.shell_context_processor
def make_shell_context():
    """
    Makes additional variables available in the Flask shell context.
    Allows direct access to db, User, ServiceOrder without importing.
    """
    return {'db': db, 'User': User, 'ServiceOrder': ServiceOrder}

if __name__ == '__main__':
    # Note: For production, use a WSGI server like Gunicorn or uWSGI
    # The debug mode should ideally be controlled by an environment variable
    app.run(debug=True, host='0.0.0.0', port=5000)
