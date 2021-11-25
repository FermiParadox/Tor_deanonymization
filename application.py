from flask import Flask, render_template, request, Response, make_response

from users import UserHandler, IDGenerator

app = Flask(__name__)


@app.route("/", methods=["GET"])
async def index():
    new_user_id = IDGenerator.unique_id()
    resp = make_response(render_template("main_page.html", userID=new_user_id))
    return resp


@app.route("/store-txy", methods=["POST"])
async def store_mouse_position():
    try:
        user_handler = UserHandler(req=request)
        user_handler.create_user()
        user = user_handler.user
        user.plot_and_show_mouse_movement()
        print(f"t {user.mouse_exit_crit_t}")
        print(f"t {user.mouse_entry_crit_t}")
        print(f"angles {user.exit_angles()}")
        print(f"angles {user.entry_angles()}")
        print(f"speed {user.exit_speeds()}")
        print(f"speed {user.entry_speeds()}")
        print(f"a {user.exit_accelerations()}")
        print(f"a {user.entry_accelerations()}")
    except Exception as e:
        print(e)
        return Response(status=400)
    return Response(status=204)


@app.route("/users-correlated-to-me", methods=["GET"])
async def correlated_users():
    return Response(status=404)


if __name__ == "__main__":
    app.run(debug=True)
