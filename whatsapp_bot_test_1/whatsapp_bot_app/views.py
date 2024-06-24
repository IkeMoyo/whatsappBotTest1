from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from twilio.twiml.messaging_response import MessagingResponse
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def bot(request):
    if request.method == 'POST':
        session = request.session
        incoming_msg = request.POST.get('Body', '').strip()
        from_number = request.POST.get('From', '').strip()

        logger.info(f"Message received from {from_number}: {incoming_msg}")

        resp = MessagingResponse()

        # Check the session to determine the state of the conversation
        if 'state' not in session:
            session['state'] = 'start'
            session['name'] = ''
            session['fruit'] = ''

        if session['state'] == 'start':
            if incoming_msg.lower() == 'hi':
                response_msg = 'Hello! What is your name?'
                session['state'] = 'asked_name'
            else:
                response_msg = 'Please say "hi" to start the conversation.'
        elif session['state'] == 'asked_name':
            session['name'] = incoming_msg
            response_msg = f'Nice to meet you, {session["name"]}! What is your favorite fruit?'
            session['state'] = 'asked_fruit'
        elif session['state'] == 'asked_fruit':
            session['fruit'] = incoming_msg
            response_msg = f'{session["fruit"]} is a great choice, {session["name"]}! It is good for your health.'
            session['state'] = 'start'  # Reset the state to start for new conversations

        resp.message(response_msg)
        logger.info(f"Response sent: {response_msg}")

        return HttpResponse(str(resp), content_type='application/xml')
    logger.warning("Invalid request method")
    return HttpResponse("Invalid request method.", status=405)
