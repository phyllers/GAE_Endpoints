import endpoints

from protorpc import messages
from protorpc import message_types
from protorpc import remote

WEB_CLIENT_ID = '1042486265945-f8rjf0ddd5cgmaaglsc7nk5n20qsoa8v.apps.googleusercontent.com'
AUDIENCE = WEB_CLIENT_ID

package = 'hello'
class Greeting(messages.Message):
    message = messages.StringField(1)

class GreetingCollection(messages.Message):
    items = messages.MessageField(Greeting, 1, repeated=True)

STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='Hello World!'),
    Greeting(message='Goodbye Cruel World!'),
])

@endpoints.api(name='gae_endpoints', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])
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

    @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      path='hellogreeting', http_method='GET',
                      name='greetings.listGreeting')
    def greetings_list(self, unused_request):
        return STORED_GREETINGS

    ID_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        id=messages.IntegerField(1, variant=messages.Variant.INT32))
    @endpoints.method(ID_RESOURCE, Greeting,
                      path='hellogreeting/{id}', http_method='GET',
                      name='greetings.getGreeting')
    def greeting_get(self, request):
        try:
            return STORED_GREETINGS.items[request.id]
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' % (request.id,))

    @endpoints.method(message_types.VoidMessage, Greeting,
                      path='hellogreetings/authed', http_method='POST',
                      name='greetings.authed')
    def greeting_authed(self, request):
        current_user = endpoints.get_current_user()
        email = (current_user.email() if current_user is not None else 'Anonymous')
        return Greeting(message='Hello %s' % (email,))



APPLICATION = endpoints.api_server([GAE_Endpoints_API])