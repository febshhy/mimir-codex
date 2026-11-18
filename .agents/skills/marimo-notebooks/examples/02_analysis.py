import marimo

app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("## Calculation and known-answer check")
    # Self-contained when run alone; the combined example uses its own fixture.
    amounts = [500, 500, 800]
    total_cents = sum(amounts)
    assert total_cents == 1800
    return (amounts, total_cents)


if __name__ == "__main__":
    app.run()
