# payments/stripe_integration.py
import stripe

stripe.api_key = "your_stripe_api_key"

def create_payment(amount, currency, description):
    try:
        payment = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            description=description
        )
        return payment
    except Exception as e:
        print(f"Error creating payment: {e}")
        return None