from asgiref.sync import sync_to_async
from bot.models.branch import Branch

@sync_to_async
def get_all_branches_by_city(city_id):
    """Get all branches by city from database"""
    return list(Branch.objects.filter(city_id=city_id))

