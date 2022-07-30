DEBUG = True


def GET_FAISS_RESOURCES():
    return None


def GET_FAISS_INDEX():
    raise NotImplementedError


def GET_FAISS_ID_TO_VECTOR():
    raise NotImplementedError


UPDATE_FAISS_AFTER_SECONDS = None

train_image_dir = "/images/0001e8b70ae2307593a59be324f3ad15"
index_path = "/faiss-web-service/resources/index"
ids_vectors_path = '/faiss-web-service/resources/ids_paths_vectors'

# ---------------------  Search

