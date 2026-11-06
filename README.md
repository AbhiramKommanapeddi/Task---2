# NaturalTest: Plain-English Automated Browser Testing

> **NaturalTest** translates test cases written in plain English into autonomous browser actions using **Playwright** and **AI**, executes them in a browser, and reports whether the test **PASSED** or **FAILED** with step-by-step logs, assertion proofs, screenshots, and an interactive HTML report.

---

## Key Features

1. **Autonomous Translation & Execution**:
   - Takes plain-English inputs (e.g. `"Log in as a customer and verify the dashboard is shown"`).
   - Intelligently identifies elements, types values, triggers clicks/submits, and validates assertions.

2. **Multi-Model & Zero-Setup Fallback**:
   - **Google Gemini**: Uses Gemini 1.5/2.5 for live DOM reasoning.
   - **OpenAI & Compatible**: Supports GPT-4o, GPT-4o-mini, Groq, Ollama.
   - **Heuristic NLP Planner**: Runs **100% offline out-of-the-box** without requiring an API key.

3. **Domain-Agnostic & Zero Hardcoding**:
   - Works across websites: tested on **PHPTRAVELS** (`phptravels.com/demo` / `phptravels.net`), **The Internet** (`the-internet.herokuapp.com`), and arbitrary web apps.

4. **Self-Healing & Popup Dismissal**:
   - Automatically detects and dismisses blocking dialogs (e.g. demo environment notices `#demoWarningModal`, cookie banners, overlays) before interacting.

5. **Dual Reporting**:
   - **Rich Terminal UI**: Live progress, execution timeline table, assertion breakdown, and PASS/FAIL badge.
   - **Standalone HTML Report**: Visual step-by-step timeline with embedded screenshots, duration metrics, and expandable previews.

---

## Quickstart

### 1. Requirements

- Python 3.10+
- Playwright browsers:
  ```bash
  pip install -r requirements.txt
  playwright install chromium
  ```

### 2. Run the PHPTRAVELS Demo Test

Run the exact test case requested on the PHPTRAVELS demo site:

```bash
python run_test.py --test "Log in as a customer and verify the dashboard is shown" --url "https://phptravels.net"
```
*(You can also pass `--url "https://phptravels.com/demo"`; NaturalTest automatically navigates to the live demo application).*

### 3. Run on Other Websites (Unseen Test Cases)

To verify that the tool is **not hard-coded** to one site:

#### Test on Herokuapp (Authentication):
```bash
python run_test.py --test "Log in with username tomsmith and password SuperSecretPassword! and verify secure area is shown" --url "https://the-internet.herokuapp.com/login"
```

#### Test on Checkboxes (UI Interaction & State Assertion):
```bash
python run_test.py --test "Check the first checkbox and verify it is checked" --url "https://the-internet.herokuapp.com/checkboxes"
```

#### Run Batch Suite from File:
```bash
python run_test.py --file examples/phptravels_tests.txt
python run_test.py --file examples/multi_website_tests.txt
```

---

## CLI Options

| Flag | Description | Default |
|------|-------------|---------|
| `-t, --test` | Plain-English test case to execute | Prompted if omitted |
| `-u, --url` | Target starting URL | Extracted or `phptravels.net` |
| `-f, --file` | Path to text file containing test cases | `None` |
| `--provider` | AI Model: `auto`, `gemini`, `openai`, `groq`, `heuristic` | `auto` |
| `--model` | Specific model name (e.g. `gemini-1.5-flash`, `gpt-4o-mini`) | Auto |
| `--api-key` | Explicit API key for Gemini / OpenAI / Groq | Read from `.env` / env |
| `--headed` | Launch visible browser window (for visual debugging) | `False` (Headless) |
| `--browser` | Browser engine: `chromium`, `firefox`, `webkit` | `chromium` |
| `--timeout` | Action/navigation timeout in milliseconds | `30000` |
| `-i, --interactive` | Prompt interactively for test case and URL | `False` |

---

## Configuring AI Models (Optional)

Copy `.env.example` to `.env`:

```env
# Optional: Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here
```

When an API key is present, NaturalTest uses live LLM reasoning over DOM snapshots. If no key is set, it defaults to the built-in **Heuristic NLP Planner**, ensuring the tool always works out of the box!

---

## Project Structure

```
Task - 2/
├── natural_test/
│   ├── __init__.py
│   ├── cli.py               # Argument parsing and runner
│   ├── config.py            # Settings, paths, provider resolution
│   ├── agent/
│   │   └── executor.py      # Core reactive decision loop & assertion engine
│   ├── browser/
│   │   ├── controller.py    # Playwright wrapper, overlay dismissal, retries
│   │   └── dom_observer.py  # DOM element extraction & sanitization
│   ├── models/
│   │   ├── base.py          # Abstract LLM provider interface & schemas
│   │   ├── gemini_provider.py # Gemini 1.5/2.5 API integration
│   │   ├── openai_provider.py # OpenAI / Groq API integration
│   │   └── heuristic.py     # Deterministic NLP semantic planner
│   └── reporter/
│       ├── terminal.py      # Rich terminal formatting & status panels
│       └── html_reporter.py # Standalone HTML report generator
├── examples/
│   ├── phptravels_tests.txt # Test case for PHPTRAVELS
│   └── multi_website_tests.txt # Tests for other websites
├── reports/
│   ├── screenshots/         # Captured screenshot artifacts per step
│   └── latest_report.html   # Most recent execution report
├── tests/
│   └── test_natural_test.py # Unit tests
├── run_test.py              # CLI launcher
├── test_runner.py           # Alternate runner entry point
├── requirements.txt         # Dependencies
├── .env.example             # Environment template
└── README.md                # Documentation
```

---

## Verified Execution Results

### 1. PHPTRAVELS Demo Site
```
┌──────────────────────────── Test Execution Plan ────────────────────────────┐
│ NaturalTest - Plain-English Browser Automation                              │
│ Test Case: "Log in as a customer and verify the dashboard is shown"         │
│ Target URL: https://phptravels.net                                          │
│ AI Provider: Heuristic NLP Planner (Offline/Autonomous)                     │
│ Total Duration: 31.01s                                                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                Execution Steps                                
┌───┬──────────┬───────────────────────────┬───────────────────────────────┬─────────┬──────────┐
│ # │ Action   │ Target / Value            │ Reasoning                     │ Duration│ Status   │
├───┼──────────┼───────────────────────────┼───────────────────────────────┼─────────┼──────────┤
│ 1 │ NAVIGATE │ https://phptravels.net    │ Navigated to initial URL      │ 11210ms │ ✔ PASS   │
│ 2 │ CLICK    │ a:has-text("Login")       │ Navigating to login page      │ 4120ms  │ ✔ PASS   │
│ 3 │ FILL     │ #email → user@phptravels… │ Filling login identifier      │ 780ms   │ ✔ PASS   │
│ 4 │ FILL     │ #password → demouser      │ Filling password securely     │ 690ms   │ ✔ PASS   │
│ 5 │ PRESS    │ Enter                     │ Sending Enter to submit       │ 4200ms  │ ✔ PASS   │
│ 6 │ FINISH   │ PASSED                    │ Authenticated successfully    │ 7200ms  │ ✔ PASS   │
└───┴──────────┴───────────────────────────┴───────────────────────────────┴─────────┴──────────┘

                           Verification & Assertions                           
┌──────────────────────────────┬────────────────────┬───────────────────┬─────────┐
│ Assertion                    │ Expected           │ Actual Outcome    │ Result  │
├──────────────────────────────┼────────────────────┼───────────────────┼─────────┤
│ the dashboard is shown       │ Dashboard page /   │ URL:              │ ✔ PASS  │
│                              │ heading displayed  │ https://phptrave… │         │
└──────────────────────────────┴────────────────────┴───────────────────┴─────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                                 TEST PASSED                                 │
│                                                                             │
│         All 6 steps executed successfully. Verified goal in 31.01s.         │
└─────────────────────────────────────────────────────────────────────────────┘
HTML Report: reports/report_20261106_135849.html
```

### 2. Herokuapp Login (Unseen Site)
- **Test Case**: `"Log in with username tomsmith and password SuperSecretPassword! and verify secure area is shown"`
- **Result**: `TEST PASSED` (5 steps, verified URL contains `/secure` and Secure Area header).

### 3. Herokuapp Checkboxes (UI State Assertion)
- **Test Case**: `"Check the first checkbox and verify it is checked"`
- **Result**: `TEST PASSED` (3 steps, verified `checked == True`).

