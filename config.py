import os
import jinja2

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
								autoescape=True)

SECRET = "fd5ts&*(hT^hr477hfdsb125dif6f9s9v9v9"