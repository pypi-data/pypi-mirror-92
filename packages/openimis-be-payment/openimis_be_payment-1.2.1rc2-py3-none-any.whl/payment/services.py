import logging
from gettext import gettext as _

from django.db import connection, transaction
from django.db.models import OuterRef, Sum, Exists
from insuree.models import Insuree
from payment.models import Payment, PaymentDetail
from policy.models import Policy
from product.models import Product

logger = logging.getLogger(__file__)


def set_payment_deleted(payment):
    try:
        payment.delete_history()
        return []
    except Exception as exc:
        logger.debug("Exception when deleting payment %s", payment.uuid, exc_info=exc)
        return {
            'title': payment.uuid,
            'list': [{
                'message': _("payment.mutation.failed_to_delete_payment") % {'uuid': payment.uuid},
                'detail': payment.uuid}]
        }


def detach_payment_detail(payment_detail):
    try:
        payment_detail.save_history()
        payment_detail.premium = None
        payment_detail.save()
        return []
    except Exception as exc:
        return [{
            'title': payment_detail.uuid,
            'list': [{
                'message': _("payment.mutation.failed_to_detach_payment_detail") % {'payment_detail': str(payment_detail)},
                'detail': payment_detail.uuid}]
        }]


def reset_payment_before_update(payment):
    payment.expected_amount = None
    payment.received_amount = None
    payment.officer_code = None
    payment.phone_number = None
    payment.request_date = None
    payment.received_date = None
    payment.status = None
    payment.transaction_no = None
    payment.origin = None
    payment.matched_date = None
    payment.receipt_no = None
    payment.payment_date = None
    payment.rejected_reason = None
    payment.date_last_sms = None
    payment.language_name = None
    payment.type_of_payment = None
    payment.transfer_fee = None


def update_or_create_payment(data, user):
    if "client_mutation_id" in data:
        data.pop('client_mutation_id')
    if "client_mutation_label" in data:
        data.pop('client_mutation_label')
    from core import datetime
    now = datetime.datetime.now()
    # No audit here
    # data['audit_user_id'] = user.id_for_audit
    data.pop("rejected_reason", None)
    data['validity_from'] = now
    payment_uuid = data.pop("uuid") if "uuid" in data else None
    if payment_uuid:
        payment = Payment.objects.get(uuid=payment_uuid)
        payment.save_history()
        reset_payment_before_update(payment)
        [setattr(payment, k, v) for k, v in data.items()]
        payment.save()
    else:
        payment = Payment.objects.create(**data)
    return payment


def legacy_match_payment(payment_id=None, audit_user_id=-1):
    with connection.cursor() as cur:
        sql = """
            DECLARE @ret int;
            EXEC @ret = [dbo].[uspMatchPayment] @PaymentID = %s, @AuditUserId = %s;
            SELECT @ret;
        """
        cur.execute(sql, (payment_id, audit_user_id,))

        if cur.description is None:  # 0 is considered as 'no result' by pyodbc
            return None
        res = cur.fetchone()[0]  # FETCH 'SELECT @ret' returned value
        raise Exception(res)
