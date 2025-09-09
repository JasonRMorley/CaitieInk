// static/js/payments.js
document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('PaymentModal');
  modal.addEventListener('show.bs.modal', function (event) {
    const btn = event.relatedTarget;
    const bookingId = btn.dataset.bookingId;

    // Set the hidden WTForms field (its id is auto "booking_id" by WTForms)
    const hidden = modal.querySelector('input[name="booking_id"]');
    if (hidden) hidden.value = bookingId;

    // Optional: show labels in the modal if you added spans for them
    const clientSpan = modal.querySelector('#payment-client');
    const tattooSpan = modal.querySelector('#payment-tattoo');
    if (clientSpan) clientSpan.textContent = btn.dataset.client || '';
    if (tattooSpan) tattooSpan.textContent = btn.dataset.tattoo || '';
  });
});
