from flask import Flask

from internal.blueprint import blueprint as InternalBlueprint
from faiss_index.blueprint import blueprint as FaissIndexBlueprint
from test.blueprint import blueprint as TestBlueprint

app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('FAISS_WEB_SERVICE_CONFIG')

app.register_blueprint(InternalBlueprint)
app.register_blueprint(FaissIndexBlueprint)
app.register_blueprint(TestBlueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
