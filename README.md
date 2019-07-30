Generate a more secure memorable-password, for use in Master Password.

## Common word lists

- <https://github.com/first20hours/google-10000-english/blob/master/20k.txt>
- <https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt>
- <https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt> (tentative)

## Inclusive rules

- Length > 3
- At least 5 uncommon words.

## Usage

```python
from nltkpass.nltkpass import NltkPass
np = NltkPass()
np.add_source("brown")
np.generate_password()
```

## Demo

See <https://nltkpass.herokuapp.com>
