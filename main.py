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
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        body {background-color:tan;margin-left:150px;}
        .form {width:600px;background-color:#ccc;padding:7px;}
        div {}
        label {margin:25px 0px 0px 0px;}
        input {float;left;}
        .error {float:right;color:red;display:inline;}
        .clear {clear:both;}

    </style>
</head>
<body>
    <h3>
        <a href="/">User Signup</a>
    </h3>
"""
signup_form = """
<form action="/" method="POST" class="form">
    <table>
        <tr>
            <td><label>Username:</td>
            <td><input type="text" name="username" value="" /></td>
            <td><span class="error"> %(e_username)s</span></td>
            </label>
        </tr>
        <tr>
            <td><label>Password:</td>
            <td><input type="password" name="password" value="" /></td>
            <td><span class="error"> %(e_password)s</span</td>
            </label>
        </tr>
        <tr>
            <td><label>Verify Password:</td>
            <td><input type="password" name="verify" value="" /></td>
            <td><span class="error"> %(e_verify)s</span></td>
            </label>
        </tr>
        <tr>
            <td><label>Email(optional):</td>
            <td><input type="text" name="email" value="" /></td>
            <td><span class="error"> %(e_email)s</span></td>
            </label>
        </tr>
    </table>
    <input type="submit" value="Submit Info" /><br />
</form>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body><br />copyright 2016
</html>
"""
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
    #  look inside for and acccess input and/or use to post errors
    def write_form(self, e_username="", e_password="", e_verify="", e_email="", username="", password="", verify="", email=""):
        self.response.out.write(page_header + signup_form % {"e_username": e_username,
                                                "e_password": e_password,
                                                "e_verify": e_verify,
                                                "e_email": e_email,
                                                "username": username,
                                                "password": password,
                                                "verify": verify,
                                                "email": email} + page_footer)
                                                # "name" to value

    #  print blank form on initial page load
    def get(self):
        self.write_form()

    #  pull out the inputs
    def post(self):
        # look inside the request to figure out what the user typed and store here
        input_username = self.request.get('username')
        input_password = self.request.get('password')
        input_verify = self.request.get('verify')
        input_email = self.request.get('email')

        # my own simple check to see if anything was put in username
        if input_username == '':
            e_username = "You must create a user name"
            self.write_form(e_username)

        #   check RegEx for username
        elif not valid_username(input_username):
            e_username = "You must create a valid user name"
            self.write_form(e_username)

        # my own simple check to see if anything was put in password #1
        elif input_password == '':
            e_password = "You must create a password"
            self.write_form(e_password)

        #   check RegEx for password
        elif not valid_password(input_password):
            e_password = "That's not a valid password"
            self.write_form(e_password)

        # my own simple check to see if anything was put in password #2
        elif input_verify == '':
            e_verify = "You must create a matching password"
            self.write_form(e_verify)

        #   check RegEx for passwords verify matching
        elif input_verify != input_password:
            e_verify = "Your passwords do not match"
            self.write_form(e_verify)

        #   check RegEx for proper email
        elif not valid_email(input_email):
            e_email = "That's not a valid email, dude"
            self.write_form(e_email)
        #   if no errors have been thrown, then send a big, warm welcome!
        else:
            success = "Welcome, " + input_username
            greeting = page_header + success + page_footer
            self.response.out.write(greeting)

app = webapp2.WSGIApplication([
    ('/', Index),
], debug=True)
