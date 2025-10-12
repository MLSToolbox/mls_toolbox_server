

from flask import Blueprint, jsonify
from datetime import datetime,timezone

from app.services import CodeGeneratorService, CodeAssessorService

bp = Blueprint('health', __name__)


@bp.route('/', methods=['GET'])
def home():
    """Health check simple"""
    return jsonify({
        'status': 'healthy',
        'service': 'mls_toolbox_server',
        'timestamp': datetime.now(timezone.utc).isoformat()

    })


@bp.route('/health', methods=['GET'])
def health():
    """Health check comprehensivo con verificación de servicios"""
    status = {
        'status': 'healthy',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'services': {}
    }
    
    
    code_gen = CodeGeneratorService()
    code_gen_healthy = code_gen.health_check()
    status['services']['code_generator'] = {
        'status': 'up' if code_gen_healthy else 'down',
        'url': code_gen.base_url
    }
    

    code_assess = CodeAssessorService()
    code_assess_healthy = code_assess.health_check()
    status['services']['code_assessor'] = {
        'status': 'up' if code_assess_healthy else 'down',
        'url': code_assess.base_url
    }
    
    
    if not (code_gen_healthy and code_assess_healthy):
        status['status'] = 'degraded'
    
    status_code = 200 if status['status'] == 'healthy' else 503
    
    return jsonify(status), status_code


@bp.route('/health/live', methods=['GET'])
def liveness():
    """Kubernetes liveness probe"""
    return jsonify({'status': 'alive'}), 200


@bp.route('/health/ready', methods=['GET'])
def readiness():
    """Kubernetes readiness probe"""
    
    code_gen = CodeGeneratorService()
    code_assess = CodeAssessorService()
    
    if code_gen.health_check() and code_assess.health_check():
        return jsonify({'status': 'ready'}), 200
    
    return jsonify({'status': 'not ready'}), 503