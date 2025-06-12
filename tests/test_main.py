import importlib
import sys
import types
from pathlib import Path


def test_list_assets_no_location():
    fake_asset_module = types.ModuleType('asset_v1')
    class FakeContentType:
        RESOURCE = 'RESOURCE'
    fake_asset_module.ContentType = FakeContentType
    class ListAssetsRequest:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
    fake_asset_module.ListAssetsRequest = ListAssetsRequest

    class FakeClient:
        def list_assets(self, request):
            from types import SimpleNamespace
            asset = SimpleNamespace(asset_type='type', name='name', resource=SimpleNamespace(data={}))
            yield asset

    fake_asset_module.AssetServiceClient = lambda: FakeClient()

    google_mod = types.ModuleType('google')
    cloud_mod = types.ModuleType('cloud')
    cloud_mod.asset_v1 = fake_asset_module
    google_mod.cloud = cloud_mod
    sys.modules['google'] = google_mod
    sys.modules['google.cloud'] = cloud_mod
    sys.modules['google.cloud.asset_v1'] = fake_asset_module

    if 'gcpri.main' in sys.modules:
        del sys.modules['gcpri.main']
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    main = importlib.import_module('gcpri.main')

    records = main.list_assets('proj')
    assert records == [{'asset_type': 'type', 'name': 'name', 'project': 'proj', 'location': None}]

