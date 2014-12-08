import os
import MySQLdb
import json
from google.appengine.ext import endpoints

from protorpc import messages
from protorpc import message_types
from protorpc import remote

package = 'hello'
class Greeting(messages.Message):
    message = messages.StringField(1)

class GreetingCollection(messages.Message):
    items = messages.MessageField(Greeting, 1, repeated=True)

STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='Hello World!'),
    Greeting(message='Goodbye Cruel World!'),
])

env = os.getenv('SERVER_SOFTWARE')
if env and env.startswith('Google App Engine/') or os.getenv('SETTINGS_MODE') == 'prod':
    # Connecting from App Engine
    db = MySQLdb.connect(
        unix_socket='/cloudsql/striking-berm-771:django-test',
        db='pong',
        user='root',
    )
else:
    # Connecting from an external network.
    # Make sure your network is whitelisted
    db = MySQLdb.connect(host='127.0.0.1', port=3306, db='test', user='root')

class DBItem(messages.Message):
    id = messages.IntegerField(1)
    content = messages.StringField(2)
    date = messages.StringField(3)

class DBItemList(messages.Message):
    items = messages.MessageField(DBItem, 1, repeated=True)

@endpoints.api(name='gae_endpoints', version='v1',)
class GAE_Endpoints_API(remote.Service):

    MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
        Greeting,
        times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                    required=True))
    @endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
                      path='hellogreeting/{times}', http_method='POST',
                      name='greetings.mulitply')
    def greetings_multiply(self, request):
        return Greeting(message=request.message * request.times)

    @endpoints.method(message_types.VoidMessage, DBItemList,
                      path='hellogreeting', http_method='GET',
                      name='greetings.listGreeting',)
    def greetings_list(self, unused_request):
        cursor = db.cursor()
        cursor.execute('SELECT id, content, date FROM testapp_greeting;')
        data = []
        for row in cursor.fetchall():
            data.append(DBItem(id=row[0],
                               content=row[1],
                               date=row[2].isoformat()))

        return DBItemList(items=data)

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))
    @endpoints.method(ID_RESOURCE, DBItem,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        try:
            cursor = db.cursor()
            cursor.execute('SELECT id, content, date FROM testapp_greeting where id=%s;' % request.id)
            row = cursor.fetchone()
            return DBItem(id=row[0], content=row[1], date=row[2].isoformat())
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' % (request.id,))

    @endpoints.method(message_types.VoidMessage, Greeting,
                      path='hellogreetings/authed', http_method='POST',
                      name='greetings.authed',)
    def greeting_authed(self, request):
        current_user = endpoints.get_current_user()
        email = (current_user.email() if current_user is not None else 'Anonymous')
        return Greeting(message='Hello %s' % (email,))



APPLICATION = endpoints.api_server([GAE_Endpoints_API])