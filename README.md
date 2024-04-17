I'd be glad to create the README text for the currency rate console utility:

**Currency Rate Console Utility**

This Python utility retrieves historical currency exchange rates from PrivatBank's API and displays them in a user-friendly format.

**Features:**

- Fetches rates for the past 1 to 10 days.
- Supports multiple currencies (USD and EUR by default, additional currencies can be specified).
- Presents results in a clear table format.

**Requirements:**

- Python 3.7+
- `aiohttp` library (`pip install aiohttp`)

**Installation:**

1. Install the required library:

   ```bash
   pip install aiohttp
   ```

2. Save the utility code (provided in the code block) as a Python script (e.g., `currency_rates.py`).

**Usage:**

1. Run the script from the command line, specifying the number of days (1-10) and optional additional currencies separated by spaces:

   ```bash
   python currency_rates.py <number_of_days> [<currency1> [<currency2> ...]]
   ```

   - `<number_of_days>`: The number of days in the past for which to retrieve rates (between 1 and 10).
   - `[<currency1> [<currency2> ...]]`: Optional list of additional currencies to include in the results (defaults to USD and EUR).

**Example:**

```bash
python currency_rates.py 5 AUD JPY
```

This command will fetch currency exchange rates for the past 5 days, including USD, EUR (default), AUD, and JPY.

**Output:**

The utility will display the retrieved rates in a table format, showing the date, currency, buy rate, and sell rate.

```
============================
Date: 2024-04-12
----------------------------
Currency  |   Buy    |  Sale
----------------------------
USD        |  28.25  |  28.80
EUR        |  32.10  |  32.70
AUD        |  24.50  |  25.00
JPY        |  0.26  |  0.27
============================
```

**Error Handling:**

- If an invalid number of days is provided (less than 1 or greater than 10), an error message will be displayed.
- If an invalid currency code is entered, it will be silently omitted from the results.

**Customization:**

- You can modify the `base_url` in the `CurrencyRateAPI` class to use a different currency exchange rate API.
- The `pretty_print_result` function can be adjusted to customize the table formatting.

I hope this README text provides a clear and comprehensive guide to using the currency rate console utility!