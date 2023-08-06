import splitit_async


class FlexFields(object):
    def __init__(self, api_client):
        self.api_client = api_client
        self._active_init_req = splitit_async.InitiateInstallmentPlanRequest(
            plan_data=splitit_async.PlanData()
        )

    async def __aenter__(self):
        await self.api_client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.api_client.__aexit__(exc_type, exc, tb)

    def add_installments(self, installment_options, default_num_installments):
        self._active_init_req.plan_data.number_of_installments = default_num_installments
        if self._active_init_req.payment_wizard_data is None:
            self._active_init_req.payment_wizard_data = splitit_async.PaymentWizardData()

        self._active_init_req.payment_wizard_data.requested_number_of_installments = installment_options

    def add_billing_information(self, billing_address, consumer_data):
        self._active_init_req.billing_address = billing_address
        self._active_init_req.consumer_data = consumer_data

    async def get_public_token(self, amount, currency_code):
        self._active_init_req.plan_data.amount = splitit_async.MoneyWithCurrencyCode(
            amount, currency_code
        )

        resp = await self.api_client.InstallmentPlanApi.installment_plan_initiate(
            self._active_init_req
        )

        return resp.public_token

    async def verify_payment(self, plan_number, order_amount):
        resp = await self.api_client.InstallmentPlanApi.installment_plan_verify_payment(
            splitit_async.VerifyPaymentRequest(
                plan_number
            )
        )
        return resp.is_paid and resp.original_amount_paid == order_amount

    def add_3D_secure(self, redirect_urls):
        self._active_init_req.plan_data.attempt3_d_secure = True
        self._active_init_req.redirect_urls = redirect_urls

    def add_capture_settings(self, auto_capture=False, first_installment_amount=0, first_charge_date=None):
        self._active_init_req.plan_data.auto_capture = auto_capture
        if first_installment_amount > 0:
            self._active_init_req.plan_data.first_installment_amount = first_installment_amount
        if first_charge_date:
            self._active_init_req.plan_data.first_charge_date = first_charge_date
