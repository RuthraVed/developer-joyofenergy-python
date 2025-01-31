from flask import abort

from service.account_service import AccountService
from service.price_plan_service import PricePlanService
from repository.price_plan_repository import price_plan_repository
from domain.price_plan import PricePlan
from .electricity_reading_controller import repository as readings_repository


def compare(smart_meter_id):
    price_plan_service = PricePlanService(readings_repository)
    account_service = AccountService()
    list_of_spend_against_price_plans = price_plan_service.get_list_of_spend_against_each_price_plan_for(
        smart_meter_id)

    if len(list_of_spend_against_price_plans) < 1:
        abort(404)
    else:
        return {
            "pricePlanId": next(iter(list_of_spend_against_price_plans[0])),
            "pricePlanComparisons": list_of_spend_against_price_plans
        }


def recommend(smart_meter_id, limit=None):
    price_plan_service = PricePlanService(readings_repository)
    list_of_spend_against_price_plans = price_plan_service.get_list_of_spend_against_each_price_plan_for(
        smart_meter_id, limit=limit)
    return list_of_spend_against_price_plans


def store_plan(plan):
    name = plan['planId']
    print(name)
    sub_dict = plan['planDetails']
    new_price_plans = [
        PricePlan(name, sub_dict.get("pricePlanSupplier"), sub_dict.get(
            "pricePlanRate"), sub_dict.get("pricePlanMultiplier"))
    ]
    price_plan_repository.store(new_price_plans)
    return plan


def view_plan_details(plan_id):
    price_plan_service = PricePlanService(readings_repository)
    plan = price_plan_service.get_plan_details(plan_id)
    plan_details = {
        "pricePlanSupplier": plan.supplier,
        "pricePlanRate": plan.unit_rate,
        "pricePlanMultiplier": plan.peak_time_multipliers
    }
    return plan_details
