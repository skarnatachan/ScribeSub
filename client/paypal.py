import requests
import json
from .models import Subscription
from django.conf import settings


def get_access_token():
    data = {
        "grant_type": "client_credentials"
    }
    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
    }

    client_id = settings.PAYPAL_CLIENT_ID
    secret_id = settings.PAYPAL_SECRET_ID
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    response = requests.post(url, data=data, headers=headers, auth=(client_id, secret_id)).json()
    access_token = response.get('access_token')
    return access_token


def cancel_subscription_paypal(access_token, subID):
    bearer_token = 'Bearer ' + access_token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }
    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subID + '/cancel'
    response = requests.post(url, headers=headers)
    print(response.status_code)


def update_subscription_paypal(access_token, subID):
    bearer_token = 'Bearer ' + access_token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }
    subDetails = Subscription.objects.get(paypal_subscription_id=subID)

    # Obtain the current subscription plan for the user/client (Standard/Premium)
    current_subscription_plan = subDetails.subscription_plan
    if current_subscription_plan == 'Standard':
        new_sub_plan = 'P-24U33182A0108840FNH3SCHA'  # To Premium
    else:
        new_sub_plan = 'P-9B0178269F0217137NH3R2NQ'  # To Standard

    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subID + '/revise'

    revision_data = {
        "plan_id": new_sub_plan
    }
    # Make the API call to update the subscription plan
    response = requests.post(url, headers=headers, data=json.dumps(revision_data))
    response_data = response.json()
    print(response_data)
    approval_url = None
    for link in response_data.get('links', []):
        if link.get('rel') == 'approve':
            approval_url = link.get('href')
    if response.status_code == 200:
        print("Subscription updated successfully")
        return approval_url
    else:
        print("Error updating subscription")
        return None


def get_current_subscription(access_token, subID):
    bearer_token = 'Bearer ' + access_token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }
    url = f'https://api.sandbox.paypal.com/v1/billing/subscriptions/{subID}/'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        current_subscription_plan = response_data.get('plan_id')
        return current_subscription_plan
    else:
        print("Failed to retrieve subscription details.")
        return None
