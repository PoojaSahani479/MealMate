from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello world!")

def thankyou(request):
    return HttpResponse("Thank you for your order!")