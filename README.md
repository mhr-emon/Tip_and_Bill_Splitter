# Tip & Bill Splitter

A small Streamlit app that calculates a tip and splits the total bill between
friends. It uses decimal arithmetic instead of asking a language model to do
the calculation, and distributes any leftover cents so the shares add up to
the total.

## Run the app

From this directory, install the project dependencies and start Streamlit:

```bash
uv sync
uv run streamlit run app.py
```
