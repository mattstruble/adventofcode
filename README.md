# adventofcode

Repository containing <https://adventofcode.com> solutions.

**Disclaimer:**
The solutions are a mix of leaderboard attempts at midnight, or more casual programming with my first cup of coffee in the morning.
So please look away at any hacks, duplicate code, or what have you within each day.

## Puzzle Runner

- Outbound calls to the webpage are throttled to every `10` seconds for `requests.get()` and `60` seconds for `requests.post()` in `tools.web.RequestLimiter`
  - HTML requests to the main puzzle are cached locally within `{year}/.cache`
  - Inputs and examples are cached within `{year}/inputs/{day}/`
- The `User-Agent` header in all requests is set to me, since I maintain this repo :)
