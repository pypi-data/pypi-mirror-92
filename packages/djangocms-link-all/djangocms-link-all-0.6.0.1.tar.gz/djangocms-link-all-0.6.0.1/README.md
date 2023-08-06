![](/docs/screenshot.png)

In order to add more link types add to your `settings.py` `LINK_ALL_MODELS`, eg

```python
from link_all.dataclasses import LinkAllModel


LINK_ALL_MODELS_ADDITIONAL = [
    LinkAllModel(app_label='djangocms_blog', model_name='Post'),
    LinkAllModel(app_label='djangocms_blog', model_name='BlogCategory', url_method='get_absolute_url', is_show_url_in_select=True),
]
```

The add the urls to your urls.py file:
```
urlpatterns = [
    path('', include('link_all.api.urls')),
]
```

You can also add link all field to your plugin by using the `LinkAllMixin` model mixin and inheriting from `LinkAllPlugin` setup in `link_all.cms_plugins`.


### Frontend development
- add `IS_LINK_ALL_DEV=true` to your `.env-local` file
- `cd link_all/static/link_all`
- `yarn install`
- `yarn start` or `yarn build`
