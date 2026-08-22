from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/getlocation", methods=["POST"])
def get_location():
    location = request.form["location"].strip()

    if not location:
        return render_template("index.html", error="Please enter a location.")

    try:
        # Encode location
        encoded_location = requests.utils.quote(location)

        url = f"https://photon.komoot.io/api/?q={encoded_location}&limit=1"
        headers = {
            "User-Agent": "MyGeocodingApp/1.0 (your.email@example.com)"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()

        if not data["features"]:
            return render_template(
                "index.html",
                error="Location not found. Please try again."
            )

        lon, lat = data["features"][0]["geometry"]["coordinates"]

        return render_template(
            "index.html",
            location=location,
            latitude=lat,
            longitude=lon,
        )

    except requests.exceptions.RequestException as e:
        return render_template(
            "index.html",
            error=f"An error occurred: {e}"
        )


if __name__ == "__main__":
    app.run(debug=True)