

from flask import Blueprint, request

from app.services import CodeAssessorService
from app.utils.validators.request_decorated_function import require_binary_data

bp = Blueprint('assessment', __name__, url_prefix='/api')


@bp.route('/rate_app', methods=['POST'])
@require_binary_data
def rate_app():
    
    code_zip = request.get_data()
    
    service = CodeAssessorService()
    result = service.rate_app(code_zip)
    
    return result


@bp.route('/get_report', methods=['POST'])
@require_binary_data
def get_report():
    
    code_zip = request.get_data()
    query_string = str(request.query_string, 'utf-8')
    
    service = CodeAssessorService()
    report = service.get_report(code_zip, query_string)
    
    return report


@bp.route('/test_rate_app', methods=['GET'])
def test_rate_app():
    
    service = CodeAssessorService()
    response = service.get('/')
    return response.text