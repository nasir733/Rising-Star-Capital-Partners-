from django.contrib.auth import get_user
from django.shortcuts import render, redirect

from dashboard.models import ApplyLoanPlan
from .forms import ContactForm
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
import stripe
import json
from pprint import pprint
from icecream import ic
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()


def about(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    return render(request, 'about.html', {})


def case_studies(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    return render(request, 'case-studies.html', {})


def contact(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()

    return render(request, 'contact.html', {})


def send_email(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    return render(request, 'send_email.html', {})


def sendesta(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    return render(request, 'sendesta.html', {})


def vukode(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    return render(request, 'vukode.html', {})


def ziteso(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    return render(request, 'ziteso.html', {})


def bradstreet(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    return render(request, 'bradstreet.html', {})


def services(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    return render(request, 'services.html', {})


def team(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    return render(request, 'team.html', {})


def testimonial(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    return render(request, 'testimonial.html', {})


def index(request):
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    return render(request, 'index.html', {})


@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {"publicKey": settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@login_required(login_url="dashboard/login")
def Createloanoriginfeesession(request, plan_id):
    if request.method == "GET":
        plan = ApplyLoanPlan.objects.get(id=plan_id)
        domain_url = "https://www.risingstarcapitalpartners.org/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=str(request.user.id)
                if request.user.is_authenticated
                else None,
                success_url=domain_url + f"success-loan-origin-fee/{plan_id}/",
                cancel_url=domain_url,
                payment_method_types=["card"],
                mode="payment",
                line_items=[
                    {
                        "price": plan.origin_fee_stripe_id,
                        "quantity": 1,
                    }
                ],
            )
            print(checkout_session)
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            print(e, "this is the error")
            return JsonResponse({"error": str(e)})


@login_required(login_url="dashboard/login")
def Createloansubcriptionsession(request, plan_id):
    if request.method == "GET":
        plan = ApplyLoanPlan.objects.get(id=plan_id)
        domain_url = "https://www.risingstarcapitalpartners.org/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=str(request.user.id)
                if request.user.is_authenticated
                else None,
                success_url=domain_url +
                f"success-loan-subscription/{plan_id}/",
                cancel_url=domain_url,
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "price": plan.subscription_stripe_id,
                        "quantity": 1,
                    }
                ],
            )
            print(checkout_session)
            return JsonResponse({"sessionId": checkout_session["id"]})
        except Exception as e:
            print(e, "this is the error")
            return JsonResponse({"error": str(e)})


def CreateloanoriginfeesessionSucess(request, plan_id):
    loan_plan = ApplyLoanPlan.objects.get(id=plan_id)
    request.user.loan_origin_paid = True
    request.user.loan_subscription_type = loan_plan
    request.user.save()
    return redirect('dashboard:apply_for_loan', step="subscription"+loan_plan.loan_type)


def CreateloansubscriptionSucess(request, plan_id):
    loan_plan = ApplyLoanPlan.objects.get(id=plan_id)
    request.user.loan_subscription_added = True
    request.user.loan_subscription_type = loan_plan
    request.user.loan_subscription_added_date = datetime.datetime.now()

    request.user.save()
    return redirect('dashboard:home')


@csrf_exempt
def webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body

    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    pprint("WebHook Recived")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret)
        print("*****************************")
        print(event["type"])

    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        print("event happening -----------")
        session = event["data"]["object"]
        # Fetch all the required data from session
        client_reference_id = session.get("client_reference_id")
        payment_mode = session.get("mode")

        if payment_mode == "subscription":
            stripe_customer_id = session.get("customer")
            stripe_subscription_id = session.get("subscription")
            upcoming_invoice = stripe.Invoice.upcoming(
                customer=stripe_customer_id)
            # Get the user and create a new StripeCustomer

            user = User.objects.get(id=client_reference_id)
            # pprint(user)

            pprint(user.username + " just subscribed.")

            price_id = upcoming_invoice.get("lines").data[0].get("plan").id
            loan_sub_plans = ApplyLoanPlan.objects.all()
            for x in loan_sub_plans:
                loan_price_id = x.subscription_stripe_id

                if loan_price_id == price_id:

                    ic(loan_price_id)
                    ic(price_id)
                    ic(stripe_customer_id)
                    ic(stripe_subscription_id)
                    user.loan_subscription_id = stripe_subscription_id
                    user.save()
                    print("user updated")
                    # if StripeCustomer.objects.filter(user=user).exists():
                    #     stripe_customer = StripeCustomer.objects.get(user=user)
                    #     stripe_customer.leads_subsription_id = stripe_subscription_id
                    #     stripe_customer.save()
                    #     pprint("if1")
                    # else:
                    #     StripeCustomer.objects.create(
                    #         user=user,
                    #         stripe_customer_id=stripe_customer_id,
                    #         leads_subsription_id=stripe_subscription_id,
                    #     )

                    #     print("if2")
                # else:
                #     print("elif")
                #     if StripeCustomer.objects.filter(user=user).exists():
                #         stripe_customer = StripeCustomer.objects.get(user=user)
                #         stripe_customer.sendesta_subscription_id = stripe_subscription_id
                #         stripe_customer.save()
                #         pprint("elif1")
                #     else:
                #         StripeCustomer.objects.create(
                #             user=user,
                #             stripe_customer_id=stripe_customer_id,
                #             sendesta_subscription_id=stripe_subscription_id,
                #         )

                #         pprint("else4")
        elif payment_mode == "payment":
            pprint("else4")

    return HttpResponse(status=200)
