from quart import Quart, request, Response
import plotly.express as px
import pandas as pd

app = Quart(__name__)


@app.route("/")
async def handle_request():
    # Get filename from url
    filename = request.args.get("filename")
    print(filename)
    df = pd.read_csv("../data/" + filename)

    x, y = pd.to_datetime(df["timestamp"], unit="s", utc=True).dt.tz_convert(
        "Europe/Zagreb"
    ), [
        "s1",
        "s2",
        "s3",
        "s4",
        "s5",
        "s6",
    ]
    # Draw graph with plotly.express
    fig = px.line(df, x=x, y=y, title=filename, labels={"x": "Date", "y": "Value"})

    if filename:
        # TODO: Sloziti da ne otvara samo u default browseru?
        fig.show()
        return Response({"Succes"}, status=200)
    else:
        pass


if __name__ == "__main__":
    app.run(port=8050, host="127.0.0.2")
