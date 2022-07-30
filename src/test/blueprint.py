from jsonschema import validate, ValidationError
from flask import Blueprint, jsonify, request
from werkzeug.exceptions import BadRequest
#from src.test.faiss_index import CreateIndex
from faiss_index import CreateIndex

#import faiss_index
# try:
#     import uwsgi
# except ImportError:
#     print('Failed to load python module uwsgi')
#     print('Periodic faiss index updates isn\'t enabled')
#
#     uwsgi = None

blueprint = Blueprint('faiss_index', __name__)


# @blueprint.record_once
# def record(setup_state):
#     manage_faiss_index(
#         setup_state.app.config.get('GET_FAISS_RESOURCES'),
#         setup_state.app.config['GET_FAISS_INDEX'],
#         setup_state.app.config['GET_FAISS_ID_TO_VECTOR'],
#         setup_state.app.config.get('UPDATE_FAISS_AFTER_SECONDS'))


@blueprint.route('/add', methods=['POST'])
def add_to_index():
    try:
        json = request.get_json(force=True)
        #print(json)
        #json = request.json()
        validate(json, {
            'type': 'object',
            'required': ['image', 'k', 'id'],
            'properties': {
                'image': {'type': 'string'},
                'k': {'type': 'integer', 'minimum': 1},
                'id': {'type': 'integer'}
            }
        })
        faissTest = CreateIndex()
        id, test = faissTest.add_to_index(base64_img=json['image'], id=json['id'])
        return test #"element added successfully!"

    except (BadRequest, ValidationError) as e:
        print('Bad request', e)
        return 'Bad request', 400

    except Exception as e:
        print('Server error', e)
        return 'Server error', 500

@blueprint.route('/search', methods=['POST'])
def search_image():
    try:
        json = request.get_json(force=True)
        validate(json, {
            'type': 'object',
            'required': ['k', 'image', 'id'],
            'properties': {
                'k': {'type': 'integer', 'minimum': 1},
                'image': {'type': 'string'},
                'id': {'type': 'integer'}
            }
        })
        faissTest = CreateIndex()
        distances, indices = faissTest.search(base64_img=json['image'], k=json['k'])
        indices = str(indices)
        distances = str(distances)
        return indices #"distances and indices are done"

    except (BadRequest, ValidationError) as e:
        print('Bad request', e)
        return 'Bad request', 400

    except Exception as e:
        print('Server error', e)
        return 'Server error', 500


@blueprint.route('/delete', methods=['POST'])
def delete_el():
    try:
        json = request.get_json(force=True)
        validate(json, {
            'type': 'object',
            'required': ['image', 'k', 'id'],
            'properties': {
                'image': {'type': 'string'},
                'k': {'type': 'integer', 'minimum': 1},
                'id': {'type': 'integer'}
            }
        })
        faissTest = CreateIndex()
        id = faissTest.delete_from_index(img_id=json['id'])
        return "element deleted successfully!"

    except (BadRequest, ValidationError) as e:
        print('Bad request', e)
        return 'Bad request', 400

    except Exception as e:
        print('Server error', e)
        return 'Server error', 500
