

from app.routes import health, generation, assessment

def register_blueprints(app):
    app.register_blueprint(health.bp)
    app.register_blueprint(generation.bp)
    app.register_blueprint(assessment.bp)