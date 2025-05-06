# Revolut Revpoints‑Plus

A compact proof‑of‑concept that shows how Revolut Points could become a daily habit instead of an after‑thought.

---

## Check it out
https://revpoints-plus-7kuw.vercel.app/

## What it does

_Looks at what the user already buys and recommends partner vendors where paying with points makes obvious sense._

1. **Ingest** the most recent transactions (mock CSV shipped with the repo).
2. **Find** partner vendors in similar categories or with overlapping products.
3. **Rank** by relevance and value of the points offer.
4. **Display** the short list inside a Streamlit mobile‑style UI.

That’s the entire loop—lightweight, fast, and transparent.

---

## Why it’s useful

| Stakeholder    | Benefit                                                                |
| -------------- | ---------------------------------------------------------------------- |
| User           | Clear places to spend points, translated into cash‑like savings.       |
| Partner vendor | Extra footfall from a highly‑targeted audience at no acquisition cost. |
| Revolut        | Higher points‑redemption rates and stickier daily engagement.          |

---

## Try it out locally

```bash
# clone & enter
$ git clone https://github.com/your‑org/revpoints‑plus.git
$ cd revpoints‑plus

# create venv
$ python -m venv .venv && source .venv/bin/activate

# install deps
$ pip install -r requirements.txt

# run demo
$ streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) and browse the "Spend Points" feed.

---

## Files to know

- `transactions.csv` – mock user transactions.
- `partners.csv` – hypothetical partner catalogue with point offers.
- `recommender.py` – k‑NN content‑based recommender (under 100 lines).
- `app.py` – Streamlit UI shell.

Tweak the CSVs to see different recommendation results.

---

Released under the MIT License.
