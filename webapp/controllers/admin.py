from flask_admin import BaseView,expose
from flask_admin.contrib.sqla import ModelView
'''views function of falsk-admin for custom page'''

class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/custom.html')

    @expose('/second_page')
    def second_page(self):
        return self.render('admin/second_page_html')

class CustomModelView(ModelView):
    pass