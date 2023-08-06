from django.db.models import Q
from django.core.exceptions import PermissionDenied
from graphene_django.filter import DjangoFilterConnectionField
import graphene_django_optimizer as gql_optimizer

from .apps import PaymentConfig
from django.utils.translation import gettext as _
from core.schema import signal_mutation_module_before_mutating, OrderedDjangoFilterConnectionField
from contribution import models as contribution_models
from policy import models as policy_models
from .models import Payment, PaymentDetail
# We do need all queries and mutations in the namespace here.
from .gql_queries import *  # lgtm [py/polluting-import]
from .gql_mutations import *  # lgtm [py/polluting-import]


class Query(graphene.ObjectType):
    payments = OrderedDjangoFilterConnectionField(
        PaymentGQLType,
        orderBy=graphene.List(of_type=graphene.String),
    )
    payment_details = OrderedDjangoFilterConnectionField(
        PaymentDetailGQLType,
        orderBy=graphene.List(of_type=graphene.String),
    )
    payments_by_premiums = OrderedDjangoFilterConnectionField(
        PaymentGQLType,
        premium_uuids=graphene.List(graphene.String, required=True),
        orderBy=graphene.List(of_type=graphene.String),
    )

    def resolve_payments(self, info, **kwargs):
        if not info.context.user.has_perms(PaymentConfig.gql_query_payments_perms):
            raise PermissionDenied(_("unauthorized"))
        pass

    def resolve_payment_details(self, info, **kwargs):
        if not info.context.user.has_perms(PaymentConfig.gql_query_payments_perms):
            raise PermissionDenied(_("unauthorized"))
        pass

    def resolve_payments_by_premiums(self, info, **kwargs):
        if not info.context.user.has_perms(PaymentConfig.gql_query_payments_perms):
            raise PermissionDenied(_("unauthorized"))
        premiums = contribution_models.Premium.objects.values_list('id').filter(Q(uuid__in=kwargs.get('premium_uuids')))
        detail_ids = PaymentDetail.objects.values_list('payment_id').filter(Q(premium_id__in=premiums),
                                                                            *filter_validity(**kwargs)).distinct()
        return Payment.objects.filter(Q(id__in=detail_ids))


def on_policy_mutation(sender, **kwargs):
    errors = []
    if kwargs.get("mutation_class") == 'DeletePoliciesMutation':
        uuids = kwargs['data'].get('uuids', [])
        policies = policy_models.Policy.objects.prefetch_related("premiums__payment_details").filter(uuid__in=uuids).all()
        for policy in policies:
            for premium in policy.premiums.all():
                for payment_detail in premium.payment_details.all():
                    errors += detach_payment_detail(payment_detail)
    return errors


class Mutation(graphene.ObjectType):
    create_payment = CreatePaymentMutation.Field()
    update_payment = UpdatePaymentMutation.Field()
    delete_payment = DeletePaymentsMutation.Field()


def bind_signals():
    signal_mutation_module_before_mutating["policy"].connect(on_policy_mutation)
