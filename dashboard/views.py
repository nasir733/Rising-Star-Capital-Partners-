from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeForm, update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView

from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import CustomUpdateUserForm
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from .forms import LoanApplicationForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse

User = get_user_model()


class ProfileView(View):
    def get(self, request):
        profile = request.user
        return render(request, 'dashboard/profile.html', {"profile": profile})


@login_required
def profile_update(request):
    if request.method == "POST":
        user_form = CustomUpdateUserForm(
            request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'Your profile is updated successfully')
            return redirect('dashboard:profile-portal-home')
    else:
        user_form = CustomUpdateUserForm(instance=request.user)

    return render(request, 'dashboard/profile.html', {'user_form': user_form})


@login_required
def plans(request):
    if request.method == "GET":
        return render(request, 'dashboard/plans.html')


@login_required
def dashboard(request):

    print('from index.html')
    user = request.user
    if not user.loan_subscription_added :
        messages.warning(
            request, mark_safe('<p>Please fill up your bank details to continue <a href="/dashboard/apply_for_loan/1" style="color:pink;">Get Started</a></p>'))
        bank_details = False

    else:
        bank_details = True
    print(user.bank_name, 'this is the user bank name')
    return render(request, 'dashboard/index.html')


@login_required
def Logout(request):
    logout(request)
    print('the user is logged out')
    return redirect('/')


def login(request):
    context = {}
    context['title'] = 'Login'
    if request.user.is_authenticated:
        messages.info(request, 'You have been already logged in')
        return redirect('dashboard:home')
    if request.method == 'GET':
        global nxt
        nxt = request.GET.get('next')
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You are logged in ')
            print('the use is logged in ')
            return redirect('dashboard:home')
        else:
            print('the user is not logged in')
            messages.error(request, 'Username or maybe Password is incorrect')
    return render(request, 'dashboard/auth-login.html')


def register(request):
    context = {}
    context['title'] = 'Create Account'
    if request.user.is_authenticated:
        messages.info(request, 'You have been already registered')
        return redirect('dashboard:home')
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        business_address = request.POST.get(
            'business_address'
        )
        business_name = request.POST.get('business_name')
        print(password, 'password =============')
        user_created = User.objects.create_user(username=username, email=email, password=password,
                                                business_address=business_address, business_name=business_name
                                                )
        user = authenticate(
            username=username, password=password)

        print(user)
        # auth_login(request, user)
        messages.success(request, 'Account succesfully created')
        return redirect('dashboard:login')
    return render(request, 'dashboard/auth-register.html')


class FinancingPortalHomeView(View):

    def get(self, request):
        profile = request.user.profile
        return render(request, 'FinancingPortalHomePage.html', {"profile": profile})


class FinancingPortalProductsPurchasedView(View):

    def get(self, request):

        products = ProductPurchasedModel.objects.filter(user=request.user)
        return render(request, 'dashboard/FinancingPortalProductsPurchased.html', {"products": products})


class FinancingPortalConfirmPurchaseView(View):
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        credit_line = request.user.credit_line
        final_credit_line = credit_line-product.price

        return render(request, 'dashboard/FinancingPortalConfirmPurchase.html', {
            "product": product,
            "credit_line": credit_line,
            'final_credit_line': final_credit_line,

        })

    def post(self, request, pk, **kwargs):
        product = Product.objects.get(id=pk)
        current_user = User.objects.get(id=request.user.id)
        current_user.credit_line = current_user.credit_line-product.price
        purchase = ProductPurchasedModel(
            user=request.user,
            product=product,
            link=product.link,
        )

        current_user.save()
        purchase.save()
        return redirect('dashboard:products-purchased')


class FinancingPortalPurchaseProductsView(View):

    def get(self, request):
        user = request.user
        user_purchased = ProductPurchasedModel.objects.filter(
            user=request.user)
        print(user_purchased)
        if user_purchased:
            products = Product.objects.exclude(
                id=user_purchased.first().product.id)
        else:
            print('inside the else statement in products purchased view')
            products = Product.objects.all()

        if user.bank_name == "" or user.bank_routing_number == "" or user.bank_account_number == "" or user.voided_check_or_direct_deposit_form == "":
            messages.warning(
                request, 'You need to fill your bank info to purchase products')
            bank_details = False
            print('inside if statement')
        else:
            bank_details = True
        return render(request, 'dashboard/FinancialPortalPurchaseProducts.html', {
            "products": products,
            "bank_details": bank_details,

        })

    def post(self, request):

        prod_id = request.POST.get('product_id')
        user = request.user
        print(prod_id)
        return HttpResponse(prod_id)
        # ProductPurchasedModel.objects.create(user=user, product=prod_id)


class FinancingPortalPaymentsView(View):

    def get(self, request):
        prods = ProductPurchasedModel.objects.filter(user=request.user)
        amount_left = 0
        payments_left = 0
        for i in prods:
            amount_left += i.amount_left
            payments_left += i.payments_left

        return render(request, 'dashboard/FinancingPortalPayments.html', {
            "amount_left": amount_left,
            "payments_left": payments_left
        })


class FinancingPortalAccessSoftware(TemplateView):
    template_name = 'dashboard/FinancingPortalProductsAccessSoftware.html'

    def get_context_data(self, **kwargs):
        products = ProductPurchasedModel.objects.filter(user=self.request.user)
        return {"products": products}


@login_required
def apply_for_loan(request, step):
    print(step)
    context = {}
    context['basic'] = ApplyLoanPlan.objects.filter(loan_type="basic").first()
    context['standard'] = ApplyLoanPlan.objects.filter(
        loan_type="standard").first()
    context['premium'] = ApplyLoanPlan.objects.filter(
        loan_type="premium").first()
    if step == "1" or None:
        d_form = LoanApplicationForm(instance=request.user)
        context['form'] = d_form
        print("step 1")
        if request.method == "POST":
            d_form = LoanApplicationForm(request.POST, instance=request.user)
            print("p")
            print(d_form.errors)
            messages.warning(
                request, d_form.errors)
            if d_form.is_valid():
                print(d_form.cleaned_data)
                d_form.save()
                return redirect('dashboard:apply_for_loan', step=2)
    elif step == "subscriptionbasic":
        print('subscriptionbasic')
        context['allplans'] = ApplyLoanPlan.objects.filter(loan_type="basic")


    elif step == "subscriptionstandard":
        print('subscriptionstandard')
        context['allplans'] = ApplyLoanPlan.objects.filter(loan_type="standard")

    elif step == "subscriptionpremium":
        print('subscriptionpremium')
        context['allplans'] = ApplyLoanPlan.objects.filter(loan_type="premium")

    context['step'] = step

    return render(request, "dashboard/applyforloan.html", context)
