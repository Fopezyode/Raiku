from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "raiku_secret"  # Needed for flashing messages

# 10 available blocks
blocks = [None] * 10

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/main")
def main():
    return render_template("main.html", blocks=enumerate(blocks))

@app.route("/reserve", methods=["POST"])
def reserve():
    user = request.form.get("user")
    slot = request.form.get("slot")

    if not user or slot == "":
        flash("⚠️ Please fill in all fields!", "error")
        return redirect(url_for("main"))

    try:
        slot = int(slot)
        if slot < 0 or slot >= len(blocks):
            flash("❌ Invalid block number (choose 0–9).", "error")
        elif blocks[slot] is None:
            blocks[slot] = user
            flash(f"✅ Block {slot} reserved successfully by {user}!", "success")
        else:
            flash(f"❌ Block {slot} is already taken by {blocks[slot]}.", "error")
    except ValueError:
        flash("⚠️ Please enter a valid number for the block ID.", "error")

    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run(debug=True)