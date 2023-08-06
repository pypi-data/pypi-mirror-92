from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError, PermissionDenied
from payment.apps import PaymentConfig
from payment.models import Payment
from typing import Optional

import graphene
from core.schema import OpenIMISMutation, logger
from django.utils.translation import gettext as _


class PaymentBase:
    id = graphene.Int(required=False, read_only=True)
    uuid = graphene.String(required=False)
    expected_amount = graphene.Decimal(max_digits=18, decimal_places=2, required=False)
    received_amount = graphene.Decimal(max_digits=18, decimal_places=2, required=False)
    officer_code = graphene.String(required=False)
    phone_number = graphene.String(required=False)
    request_date = graphene.Date(required=False)
    received_date = graphene.Date(required=False)
    status = graphene.String(required=False)
    transaction_no = graphene.String(required=False)
    origin = graphene.String(required=False)
    matched_date = graphene.Date(required=False)
    receipt_no = graphene.String(required=False)
    payment_date = graphene.Date(required=False)
    rejected_reason = graphene.String(required=False)
    date_last_sms = graphene.Date(required=False)
    language_name = graphene.String(required=False)
    type_of_payment = graphene.String(required=False)
    transfer_fee = graphene.Decimal(max_digits=18, decimal_places=2, required=False)


class CreatePaymentMutation(OpenIMISMutation):
    """
    Create a contribution for policy with or without a payer
    """
    _mutation_module = "contribution"
    _mutation_class = "CreatePaymentMutation"

    class Input(PaymentBase, OpenIMISMutation.Input):
        pass

    @classmethod
    def async_mutate(cls, user, **data) -> Optional[str]:
        try:
            if type(user) is AnonymousUser or not user.id:
                raise ValidationError(
                    _("mutation.authentication_required"))
            if not user.has_perms(PaymentConfig.gql_mutation_create_payments_perms):
                raise PermissionDenied(_("unauthorized"))
            update_or_create_payment(data, user)
            return None
        except Exception as exc:
            return [{
                'message': _("contribution.mutation.failed_to_create_premium"),
                'detail': str(exc)}
            ]


class UpdatePaymentMutation(OpenIMISMutation):
    """
    Update a contribution for policy with or without a payer
    """
    _mutation_module = "contribution"
    _mutation_class = "UpdatePaymentMutation"

    class Input(PaymentBase, OpenIMISMutation.Input):
        pass

    @classmethod
    def async_mutate(cls, user, **data) -> Optional[str]:
        try:
            if type(user) is AnonymousUser or not user.id:
                raise ValidationError(
                    _("mutation.authentication_required"))
            if not user.has_perms(PaymentConfig.gql_mutation_update_payments_perms):
                raise PermissionDenied(_("unauthorized"))
            update_or_create_payment(data, user)
            return None
        except Exception as exc:
            return [{
                'message': _("payment.mutation.failed_to_update_payment") %
                           {'id': data.get('id') if data else None},
                'detail': str(exc)}
            ]


class DeletePaymentsMutation(OpenIMISMutation):
    """
    Delete one or several Payments.
    """
    _mutation_module = "contribution"
    _mutation_class = "DeletePaymentsMutation"

    class Input(OpenIMISMutation.Input):
        uuids = graphene.List(graphene.String)

    @classmethod
    def async_mutate(cls, user, **data):
        if not user.has_perms(PaymentConfig.gql_mutation_delete_payments_perms):
            raise PermissionDenied(_("unauthorized"))
        errors = []
        for payment_uuid in data["uuids"]:
            payment = Payment.objects \
                .filter(uuid=payment_uuid) \
                .first()
            if payment is None:
                errors.append({
                    'title': payment_uuid,
                    'list': [{'message': _(
                        "contribution.validation.id_does_not_exist") % {'id': payment_uuid}}]
                })
                continue
            errors += set_payment_deleted(payment)
        if len(errors) == 1:
            errors = errors[0]['list']
        return errors
