# core/loaders.py
from aiodataloader import DataLoader
from core.models import DeployedApp
from asgiref.sync import sync_to_async

class AppsByUserLoader(DataLoader):
    async def batch_load_fn(self, user_ids: list[str]) -> list[list[DeployedApp]]:
        # Run the sync QuerySet in a thread and get a Python list:
        apps_list = await sync_to_async(list)(
            DeployedApp.objects.filter(owner_id__in=user_ids)
        )

        # Group them by owner_id
        apps_map: dict[str, list[DeployedApp]] = {}
        for app in apps_list:
            apps_map.setdefault(app.owner_id, []).append(app)

        # Return results in the same order as requested
        return [apps_map.get(user_id, []) for user_id in user_ids]
