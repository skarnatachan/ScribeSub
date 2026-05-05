from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from writer.models import Article
from .models import Subscription
from accounts.models import CustomUser
from .paypal import *
from django.http import HttpResponse


@login_required(login_url='accounts:my-login')
def client_dashboard(request):
    try:
        subDetails = Subscription.objects.get(subscription2customuser=request.user)
        subscription_plan = subDetails.subscription_plan
        context = {
            'subscription_plan': subscription_plan,
        }
        return render(request, 'client/client-dashboard.html', context)
    except:
        subscription_plan = None
        context = {
            'subscription_plan': subscription_plan,
        }
        return render(request, 'client/client-dashboard.html', context)


@login_required(login_url='accounts:my-login')
def browse_articles(request):
    try:
        subDetails = Subscription.objects.get(subscription2customuser=request.user, is_active=True)
    except:
        return render(request, 'client/subscription-locked.html')
    current_subscription_plan = subDetails.subscription_plan
    articles = None
    if current_subscription_plan == 'Standard':
        articles = Article.objects.filter(is_premium=False)
    elif current_subscription_plan == 'Premium':
        articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'client/browse-articles.html', context)


@login_required(login_url='accounts:my-login')
def subscription_locked(request):
    context = {}
    return render(request, 'client/subscription-locked.html', context)


@login_required(login_url='accounts:my-login')
def subscription_plans(request):
    context = {}
    return render(request, 'client/subscription-plans.html', context)


@login_required(login_url='accounts:my-login')
def create_subscription(request, subID, plan):
    custom_user = CustomUser.objects.get(email=request.user)
    firstName = custom_user.first_name
    lastName = custom_user.last_name
    fullName = firstName + ' ' + lastName
    selected_sub_plan = plan
    sub_cost = 0
    if selected_sub_plan == 'Standard':
        sub_cost = 4.99
    elif selected_sub_plan == 'Premium':
        sub_cost = 9.99
    subscription = Subscription.objects.update_or_create(subscription2customuser=request.user,
                                                         paypal_subscription_id=subID,
                                                         subscription_plan=selected_sub_plan, subscriber_name=fullName,
                                                         subscription_cost=sub_cost, is_active=True, )
    context = {
        'subscription': subscription,
    }
    return render(request, 'client/create-subscription.html', context)


@login_required(login_url='accounts:my-login')
def delete_subscription(request, subID):
    try:
        # Delete subscription from PayPal
        access_token = get_access_token()
        cancel_subscription_paypal(access_token, subID)

        # Delete a subscription from Django (application side)
        subscription = Subscription.objects.get(paypal_subscription_id=subID)
        subscription.delete()

        return redirect('client:client-dashboard')
    except:
        return redirect('client:client-dashboard')


@login_required(login_url='accounts:my-login')
def update_subscription(request, subID):
    access_token = get_access_token()
    approve_link = update_subscription_paypal(access_token, subID)
    if approve_link:
        return redirect(approve_link)
    else:
        return HttpResponse("Error updating subscription")


@login_required(login_url='accounts:my-login')
def paypal_update_sub_confirmed(request):
    try:
        subDetails = Subscription.objects.get(subscription2customuser=request.user)
        subscriptionID = subDetails.paypal_subscription_id
        context = {
            'subscriptionID': subscriptionID,
        }
        return render(request, 'client/paypal-update-sub-confirmed.html', context)
    except:
        return render(request, 'client/paypal-update-sub-confirmed.html')


@login_required(login_url='accounts:my-login')
def django_update_sub_confirmed(request, subID):
    access_token = get_access_token()
    current_plan_id = get_current_subscription(access_token, subID)
    if current_plan_id == 'P-9B0178269F0217137NH3R2NQ':  # Standard
        new_plan_name = 'Standard'
        new_cost = 4.99
        Subscription.objects.filter(paypal_subscription_id=subID).update(subscription_plan=new_plan_name,
                                                                         subscription_cost=new_cost, )
    if current_plan_id == 'P-24U33182A0108840FNH3SCHA':  # Premium
        new_plan_name = 'Premium'
        new_cost = 9.99
        Subscription.objects.filter(paypal_subscription_id=subID).update(subscription_plan=new_plan_name,
                                                                         subscription_cost=new_cost, )
    return render(request, 'client/django-update-sub-confirmed.html')
