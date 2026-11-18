import marimo

app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("# Example: orders and refunds — source assumptions")
    # Fixture values are deliberately tiny and synthetic.
    orders = [(101, 500), (102, 500), (103, 800)]
    return (orders,)


if __name__ == "__main__":
    app.run()
