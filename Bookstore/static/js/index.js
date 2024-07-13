'use strict';

const stripe = Stripe(STRIPE_PUBLISHABLE_KEY);

const elem = document.getElementById('submit');
const clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
const elements = stripe.elements();
const style = {
  base: {
    color: "#000",
    lineHeight: '2.4',
    fontSize: '16px'
  }
};

const card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', (event) => {
  const displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
    displayError.classList.add('alert', 'alert-info');
  } else {
    displayError.textContent = '';
    displayError.classList.remove('alert', 'alert-info');
  }
});

const form = document.getElementById('payment-form');

form.addEventListener('submit', (ev) => {
  ev.preventDefault();

  const custName = document.getElementById("custName").value;
  const custAdd = document.getElementById("custAdd").value;
  const custAdd2 = document.getElementById("custAdd2").value;
  const postCode = document.getElementById("postCode").value;

  fetch('http://127.0.0.1:8000/orders/add/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': CSRF_TOKEN
    },
    body: JSON.stringify({
      order_key: clientsecret,
      action: "post"
    })
  })
    .then(response => response.json())
    .then(json => {
      console.log(json.success);

      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address: {
              line1: custAdd,
              line2: custAdd2
            },
            name: custName
          }
        }
      }).then(result => {
        if (result.error) {
          console.log('payment error');
          console.log(result.error.message);
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed');
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
          }
        }
      });
    })
    .catch(error => {
      console.error('Error:', error);
    });
});
