from contribution.test_helpers import create_test_premium
from core.test_helpers import create_test_officer
from django.test import TestCase
from insuree.test_helpers import create_test_insuree
from medical.test_helpers import create_test_service
from medical_pricelist.test_helpers import add_service_to_hf_pricelist
from payment.services import legacy_match_payment
from payment.test_helpers import create_test_payment2
from policy.models import Policy
from policy.test_helpers import create_test_policy2
from product.test_helpers import create_test_product, create_test_product_service


class PaymentServiceTestCase(TestCase):
    def test_simple(self):
        officer = create_test_officer(custom_props={"code": "TSTSIMP1"})
        insuree = create_test_insuree(custom_props={"chf_id": "paysimp"})
        product = create_test_product("ELI1")
        (policy, insuree_policy) = create_test_policy2(product, insuree, custom_props={
            "value": 1000, "status": Policy.STATUS_IDLE})
        service = create_test_service("A")
        svc_pl_detail = add_service_to_hf_pricelist(service)
        product_service = create_test_product_service(product, service, custom_props={"limit_no_adult": 20})
        premium = create_test_premium(policy_id=policy.id, with_payer=False)
        payment, payment_detail = create_test_payment2(
            insuree_code=insuree.chf_id,
            product_code=product.code,
            officer_code=officer.code,
        )

        legacy_match_payment(payment.id, -1)

        payment_detail.refresh_from_db()
        policy.refresh_from_db()
        self.assertIsNotNone(payment_detail.premium)
        self.assertEqual(payment_detail.premium, premium)
        self.assertEqual(policy.status, Policy.STATUS_ACTIVE)

        payment_detail.delete()
        payment.delete()
        premium.delete()
        product_service.delete()
        svc_pl_detail.delete()
        service.delete()
        policy.insuree_policies.all().delete()
        policy.delete()
        product.delete()
        insuree.delete()
        officer.delete()

