import os
from aoe_find_match_result_flask_backend import app


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=3000), host="0.0.0.0")
