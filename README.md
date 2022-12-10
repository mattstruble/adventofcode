# adventofcode

Repository containing <https://adventofcode.com> solutions.

## Puzzle Runner

- Outbound calls to the webpage are throttled to every `10` seconds for `requests.get()` and `60` seconds for `requests.post()` in `tools.web.RequestLimiter`
  - HTML requests to the main puzzle are cached locally within `{year}/.cache`
  - Inputs and examples are cached within `{year}/inputs/{day}/`
- The `User-Agent` header in all requests is set to me, since I maintain this repo :)
