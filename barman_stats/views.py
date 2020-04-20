# barman-stats - plugin for barman
# Copyright © 2020 Yoann Pietri <me@nanoy.fr>
#
# barman-stats is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# barman-stats is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with barman-stats.  If not, see <https://www.gnu.org/licenses/>.

from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Avg, Count, Sum
from django.shortcuts import render
from django.utils import timezone

from barman.acl import active_required, admin_required
from management.models import (Category, Consumption, ConsumptionHistory, Keg,
                               Menu, Product, Refund, Reload)
from preferences.models import Contribution, GeneralPreferences, PaymentMethod
from users.models import School


@active_required
@login_required
@admin_required
def stats(request):
    """
    Page with statistics
    """
    users = User.objects.all()
    adherents = [x for x in users if x.profile.is_adherent]
    sum_balance = sum([x.profile.balance for x in users])
    general_preferences, _ = GeneralPreferences.objects.get_or_create(pk=1)
    nb_quotes = len(general_preferences.global_message.split("\n"))
    consumptions = ConsumptionHistory.objects.aggregate(
        Count("amount"), Avg("amount"), Sum("amount")
    )
    refunds = Refund.objects.aggregate(Count("amount"), Sum("amount"), Avg("amount"))
    reloads = Reload.objects.aggregate(Count("amount"), Sum("amount"), Avg("amount"))
    last_week = timezone.now().date() - timedelta(days=7)
    consumptions_week = ConsumptionHistory.objects.filter(date__gt=last_week).aggregate(
        Count("amount"), Sum("amount")
    )
    last_month = timezone.now().date() - timedelta(days=30)
    consumptions_month = ConsumptionHistory.objects.filter(
        date__gt=last_month
    ).aggregate(Count("amount"), Sum("amount"))
    last_year = timezone.now().date() - timedelta(days=365)
    consumptions_year = ConsumptionHistory.objects.filter(date__gt=last_year).aggregate(
        Count("amount"), Sum("amount")
    )
    nb_consumptions_month = consumptions_month["amount__count"]
    total_consumptions_month = consumptions_month["amount__sum"]
    nb_consumptions_year = consumptions_year["amount__count"]
    total_consumptions_year = consumptions_year["amount__sum"]
    mean_reload = reloads["amount__avg"]
    total_reload = reloads["amount__sum"]
    nb_reload = reloads["amount__count"]
    mean_refund = refunds["amount__avg"]
    nb_refund = refunds["amount__count"]
    total_refund = refunds["amount__sum"]
    nb_archived_accounts = User.objects.filter(is_active=False).count()
    best_product = sorted(
        [
            (
                Consumption.objects.filter(product=product).aggregate(Sum("quantity"))[
                    "quantity__sum"
                ]
                or 0,
                product,
            )
            for product in Product.objects.all()
        ],
        key=lambda x: x[0],
        reverse=True,
    )[0]
    best_buyer = sorted(
        User.objects.all(), key=lambda x: x.profile.total_debit, reverse=True
    )[0]
    return render(
        request,
        "barman_stats/stats.html",
        {
            "users": users,
            "adherents": adherents,
            "nb_consumptions": consumptions["amount__count"],
            "total_consumptions": consumptions["amount__sum"],
            "nb_consumptions_week": consumptions_week["amount__count"],
            "total_consumptions_week": consumptions_week["amount__sum"],
            "categories": Category.objects.all(),
            "categories_shown": Category.objects.exclude(order=0),
            "products": Product.objects.all(),
            "active_products": Product.objects.filter(is_active=True),
            "active_kegs": Keg.objects.filter(is_active=True),
            "sum_balance": sum_balance,
            "schools": School.objects.all(),
            "groups": Group.objects.all(),
            "admins": User.objects.filter(is_staff=True),
            "superusers": User.objects.filter(is_superuser=True),
            "menus": Menu.objects.all(),
            "payment_methods": PaymentMethod.objects.all(),
            "contributions": Contribution.objects.all(),
            "nb_quotes": nb_quotes,
            "nb_archived_accounts": nb_archived_accounts,
            "best_buyer": best_buyer,
            "best_product": best_product,
        },
    )
