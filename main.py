#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        body {float:left;background-color:tan;}
        .error {color: red;}
        .form {width:200px;background-color:#ccc;padding:7px;}
        label {margin:25px 0px 0px 0px;}
        div {float:left;}
        .error {float:left;color:red;display:inline;}

    </style>
</head>
<body>
    <h3>
        <a href="/">User Signup</a>
    </h3>
"""

signup_form = """
<form action="/signup" method="POST" class="form">
    <div>
        <label>Username:
            <input type="text" name="username" value="%(username)s" />
            <span class="error"> %(e_username)s</span>
        </label>
    </div>
    <div>
        <label>Password:
            <input type="password" name="password" value="%(password)s" />
            <span class="error"> %(e_password)s</span>
        </label>
    </div>
    <div>
        <label>Verify Password:
            <input type="password" name="verify" value="%(verify)s" />
            <span class="error"> %(e_verify)s</span>
        </label>
    </div>
    <div>
        <label>Email(optional):
            <input type="text" name="email" value="%(email)s" />
            <span class="error"> %(e_email)s</span>
        </label>
    </div>
    <input type="submit" value="Submit Info" /><br />
</form>
"""


# html boilerplate for the bottom of every page
page_footer = """
</body>copyright 2016
</html>
"""


class Index(webapp2.RequestHandler):

    def write_form(self, e_username="", e_password="", e_verify="", e_email="", username="", password="", verify="", email=""):
        self.response.out.write(page_header + signup_form % {"e_username": e_username,
                                                "e_password": e_password,
                                                "e_verify": e_verify,
                                                "e_email": e_email,
                                                "username": username,
                                                "password": password,
                                                "verify": verify,
                                                "email": email} + page_footer)

    def get(self):
        #PUT FORM ON SCREEN
        #response = page_header + rotate_form_input + page_footer
        self.write_form()
        #self.response.write('You Must Signup To Use Our Site')

class Output(webapp2.RequestHandler):
    def post(self):
        # look inside the request to figure out what the user typed
        input_username = self.request.get('username')
        input_password = self.request.get('password')
        input_verify = self.request.get('verify')
        input_email = self.request.get('email')

        # validation procedures
        e_username = "You must create a user name."
        if input_username == '':
            err_response = signup_form.format(e_username = e_username)
            self.redirect("/?error=" + err_response)


        error_pass_unmatch = "Your passwords do not match"
        if input_password != input_verify:
            self.redirect("/?error=" + error_pass_unmatch)

        # combine all the pieces to build the content of our response
        main_content = input_username + input_password + input_verify + input_email
        response = page_header + main_content + page_footer
        self.response.out.write(response)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/signup', Output)
], debug=True)
