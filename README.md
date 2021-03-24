# Edge Branch

This is the development edge branch, code might **not work**. Please use the master branch for production.

### ToDo

- ~~Improve `Config` singleton to use initialized objects instead of redefined vars.~~
- ~~Include `status_code` in exceptions.~~
- Merge non API functionality into [Base](https://github.com/SQLMatches/Base/tree/Edge).
- Increase hosted version max upload to 150 MB.
- Improve `DemoQueue` to not be some messy dict.
- Use [GetPublishedFileDetails](https://steamapi.xpaw.me/#ISteamRemoteStorage/GetPublishedFil) to get workshop map images.
- Indepth scoping.
- Public / Private data for `api_schema`.
- Make `match_ender` a background timeout instead of a loop.
- Make `demo_delete` no longer a queue instead just a background task.
- Clean up websockets.
- Restructure routes.
- Add `hosted` scope, so `self-hosting` setup is simple.
- Remove `bulk_scoreboard_expire` &`bulk_community_expire`.
- Cache less, cache smarter.
- Change `CacheBase.expir` to `CacheBase.delete`.
- Add Public / Private data support for `CacheBase`.
- Change `stripe_webhook` scope to use stripes validation method instead of a key.
- Change scopes to be `camel cased`.
- Add Autosetup.
- Custom logos
- Owning multiple communities.
- Custom domain.
- Admin tools.
- Match mangement.
