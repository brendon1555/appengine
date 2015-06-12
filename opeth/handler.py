import cgi
import webapp2
import json
from webapp2_extras import jinja2

import opeth.model


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


class MainHandler(Base):

    def get(self):
        self.render_template("form")

    def post(self):
        comment_store = opeth.model.Comment(content=self.request.POST['content'])
        comment_store.put()

        ctx = opeth.model.ndb.get_context()
        ctx.clear_cache()

        comments = opeth.model.Comment.query().order(opeth.model.Comment.date_added)

        template_values = {'comments': comments}
        self.render_template("output", template_values)

#------------------------------#
#----Working with XHR below----#
#------------------------------#


class XhrHandler(Base):

    def get(self):
        comments = opeth.model.Comment.query().order(opeth.model.Comment.date_added)

        template_values = {'comments': comments, 'ids': comments}
        self.render_template("xhr_form", template_values)

    def post(self):

        json_comment = json.loads(self.request.body)

        if "delete" in json_comment:
            opeth.model.ndb.Key("Comment", int(json_comment["delete"])).delete()

        else:
            comment_store = opeth.model.Comment(content=json_comment["content"])
            comment_key = comment_store.put()

            comment_id = comment_key.id()

            ctx = opeth.model.ndb.get_context()
            ctx.clear_cache()

            comments = opeth.model.Comment.query()

            self.response.write(comment_id)

app = webapp2.WSGIApplication([
    ('/form', MainHandler),
    ('/xhrform', XhrHandler)
], debug=True)