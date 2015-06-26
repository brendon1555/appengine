import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users


class Base(webapp2.RequestHandler):
    #: Ensure we return a webapp2 singleton for caching
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    #: Wrapper to reneder jinja2 template, handles exception
    def render_template(self, template_name, template_values={}):
        template_values['IS_DEBUG'] = self.app.debug
        template_file_name = "%s.html" % template_name
        self.response.out.write(self.jinja2.render_template(template_file_name, **template_values))

#webapp2
class MainHandler(Base):
    def get(self):
        self.render_template("index")
