from app.main import bp

@bp.route('/')
def index():
    return '<h1>We got the index</h1>'