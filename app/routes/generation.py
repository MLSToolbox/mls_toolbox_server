

from flask import Blueprint, request, jsonify

from app.services import CodeGeneratorService
from app.utils.validators.request_decorated_function import require_json, require_fields

bp = Blueprint('generation', __name__, url_prefix='/api')


@bp.route('/create_app', methods=['POST'])
@require_json
@require_fields('code', 'nodes')
def create_app():
   
   
    data = request.json
    
    service = CodeGeneratorService()
    zip_content = service.create_app(
        code=data['code'],
        nodes=data['nodes']
    )
    
    return zip_content


@bp.route('/test_create_app', methods=['GET'])
def test_create_app():
    
    service = CodeGeneratorService()
    response = service.get('/')
    return response.text


@bp.route('/get_config', methods=['GET'])
def get_config():
    
    service = CodeGeneratorService()
    config = service.get_config()
    return jsonify(config)


@bp.route('/get_base_editor', methods=['GET'])
def get_base_editor():
    
    service = CodeGeneratorService()
    editor = service.get_base_editor()
    return jsonify(editor)


@bp.route('/get_editor', methods=['POST'])
def get_editor():
    
    template_name = request.data.decode('utf-8')
    
    service = CodeGeneratorService()
    editor = service.get_editor(template_name)
    return jsonify(editor)


@bp.route('/get_available_editor', methods=['GET'])
def get_available_editors():
   
    service = CodeGeneratorService()
    editors = service.get_available_editors()
    return jsonify(editors)